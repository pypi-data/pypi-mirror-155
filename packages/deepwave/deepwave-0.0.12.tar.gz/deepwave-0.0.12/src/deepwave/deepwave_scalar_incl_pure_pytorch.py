import torch
import math
from deepwave.common import (set_dx, check_inputs, pad_model, pad_locations,
                             location_to_index,
                             extract_survey,
                             get_n_batch, upsample, downsample,
                             convert_to_contiguous, setup_pml,
                             cfl_condition)


class Scalar(torch.nn.Module):
    def __init__(self, v, dx):
        super(Scalar, self).__init__()
        if v.ndim != 2:
            raise RuntimeError("v must have two dimensions")
        self.v = torch.nn.Parameter(v, requires_grad=v.requires_grad)
        self.dx, self.dy = set_dx(dx)

    def forward(self, dt, source_amplitudes=None,
                source_locations=None, receiver_locations=None,
                accuracy=4, pml_widths=20, pml_freq=None, max_vel=None,
                survey_pad=None, wavefield_0=None, wavefield_m1=None,
                psix_m1=None, psiy_m1=None,
                zetax_m1=None, zetay_m1=None,
                origin=None, nt=None, own=True):
        # type: (float, Optional[Tensor], Optional[Tensor], Optional[Tensor], int, Union[int, List[int]], Optional[float], Optional[float], Optional[Union[int, List[Optional[int]]]], Optional[Tensor], Optional[Tensor], Optional[Tensor], Optional[Tensor], Optional[Tensor], Optional[Tensor], Optional[List[int]], Optional[int], bool)

        # Check inputs
        check_inputs(source_amplitudes, source_locations, receiver_locations,
                     [wavefield_0, wavefield_m1, psix_m1, psiy_m1,
                      zetax_m1, zetay_m1], accuracy, nt, self.v)

        if nt is None:
            nt = 0
            if source_amplitudes is not None:
                nt = source_amplitudes.shape[-1]
        v = self.v
        device = v.device
        dtype = v.dtype
        if isinstance(pml_widths, int):
            pml_widths = [pml_widths for _ in range(4)]
        fd_pad = accuracy // 2
        pad = [fd_pad + pml_width for pml_width in pml_widths]
        models, locations = extract_survey(
            [v], [source_locations, receiver_locations], survey_pad,
            [wavefield_0, wavefield_m1, psix_m1, psiy_m1, zetax_m1, zetay_m1],
            origin, pml_widths
        )
        v, = models
        source_locations, receiver_locations = locations
        shape_without_fd = (pml_widths[0] + v.shape[0] + pml_widths[1],
                            pml_widths[2] + v.shape[1] + pml_widths[3])
        v_pad = pad_model(v, pad)
        if max_vel is None:
            max_vel = v.max().item()
        max_vel = abs(max_vel)
        dt, step_ratio = cfl_condition(self.dx, self.dy, dt, max_vel)
        if source_amplitudes is not None and source_locations is not None:
            source_locations = pad_locations(source_locations, pad)
            sources_i = location_to_index(source_locations, v_pad.shape[1])
            source_amplitudes = (
                -source_amplitudes * v_pad[source_locations[..., 0],
                                           source_locations[..., 1],
                                           None] ** 2 * dt**2
            )
            source_amplitudes = upsample(source_amplitudes, step_ratio)
        else:
            sources_i = None
        if receiver_locations is not None:
            receiver_locations = pad_locations(receiver_locations, pad)
            receivers_i = location_to_index(receiver_locations, v_pad.shape[1])
        else:
            receivers_i = None
        n_batch = get_n_batch([source_locations, receiver_locations,
                               wavefield_0, wavefield_m1, psix_m1, psiy_m1,
                               zetax_m1, zetay_m1])
        ax, ay, bx, by = \
            setup_pml(pml_widths, fd_pad, dt, v_pad, max_vel, n_batch,
                      pml_freq)
        nt *= step_ratio

        if source_amplitudes is not None:
            if source_amplitudes.device == torch.device('cpu'):
                source_amplitudes = torch.movedim(source_amplitudes, -1, 1)
            else:
                source_amplitudes = torch.movedim(source_amplitudes, -1, 0)

        v_pad = convert_to_contiguous(v_pad)
        source_amplitudes = convert_to_contiguous(source_amplitudes).to(dtype).to(device)
        wavefield_0 = convert_to_contiguous(wavefield_0)
        wavefield_m1 = convert_to_contiguous(wavefield_m1)
        psix_m1 = convert_to_contiguous(psix_m1)
        psiy_m1 = convert_to_contiguous(psiy_m1)
        zetax_m1 = convert_to_contiguous(zetax_m1)
        zetay_m1 = convert_to_contiguous(zetay_m1)
        sources_i = convert_to_contiguous(sources_i)
        receivers_i = convert_to_contiguous(receivers_i)
        ax = convert_to_contiguous(ax)
        ay = convert_to_contiguous(ay)
        bx = convert_to_contiguous(bx)
        by = convert_to_contiguous(by)

        if own:
            wfc, wfp, psix, psiy, zetax, zetay, receiver_amplitudes = \
                torch.ops.deepwave.scalar(v_pad, source_amplitudes, wavefield_0,
                                          wavefield_m1, psix_m1, psiy_m1,
                                          zetax_m1, zetay_m1, ax, ay, bx, by,
                                          sources_i.long(), receivers_i.long(),
                                          self.dx, self.dy, dt, nt, n_batch, step_ratio, accuracy)
        else:
            sources_batch = (torch.arange(source_locations.shape[0]).reshape(-1, 1)
                                  .expand(source_locations.shape[:2]))
            receivers_batch = (torch.arange(receiver_locations.shape[0]).reshape(-1, 1)
                                  .expand(receiver_locations.shape[:2]))
            if receivers_i.numel() > 0:
                receiver_amplitudes = torch.zeros(receivers_i.shape[0], nt, receivers_i.shape[1], dtype=v_pad.dtype)
            else:
                receiver_amplitudes = torch.empty(0)
            v2dt2 = v_pad**2 * dt**2
            wfc = torch.nn.functional.pad(wavefield_0, (2, 2, 2, 2))
            wfp = torch.nn.functional.pad(wavefield_m1, (2, 2, 2, 2))
            psix = torch.nn.functional.pad(psix_m1, (2, 2, 2, 2))
            psiy = torch.nn.functional.pad(psiy_m1, (2, 2, 2, 2))
            zetax = torch.nn.functional.pad(zetax_m1, (2, 2, 2, 2))
            zetay = torch.nn.functional.pad(zetay_m1, (2, 2, 2, 2))
            for t in range(nt):
                wfc, wfp, psix, psiy, zetax, zetay = \
                    step(v2dt2, wfc, wfp, psix, psiy, zetax, zetay,
                         ax, ay, bx, by, 1/self.dx**2, 1/self.dy**2,
                         1/self.dx, 1/self.dy)
                if sources_i.numel() > 0:
                    wfc[sources_batch, source_locations[..., 0], source_locations[..., 1]] += source_amplitudes[:, t]# * v2dt2[sources_x, sources_y]
                if receivers_i.numel() > 0:
                    receiver_amplitudes[:, t] = wfp[receivers_batch, receiver_locations[..., 0], receiver_locations[..., 1]]
            wfc = wfc[:,2:-2,2:-2]
            wfp = wfp[:,2:-2,2:-2]
            psix = psix[:,2:-2,2:-2]
            psiy = psiy[:,2:-2,2:-2]
            zetax = zetax[:,2:-2,2:-2]
            zetay = zetay[:,2:-2,2:-2]

        if receiver_amplitudes.numel() > 0:
            if source_amplitudes.device == torch.device('cpu'):
                receiver_amplitudes = torch.movedim(receiver_amplitudes, 1, -1)
            else:
                receiver_amplitudes = torch.movedim(receiver_amplitudes, 0, -1)
            receiver_amplitudes = downsample(receiver_amplitudes, step_ratio)
                    
        return (wfc, wfp, psix, psiy, zetax, zetay, receiver_amplitudes)


def diff_x(x, one_over_dx):
    # type: (Tensor, float) -> Tensor
    return torch.nn.functional.pad((8 / 12 * (x[:, 3:-1, 2:-2] - x[:, 1:-3, 2:-2])
                                    - 1 / 12 * (x[:, 4:, 2:-2] - x[:, :-4, 2:-2]))
                                   * one_over_dx, (2, 2, 2, 2))

def diff_y(x, one_over_dy):
    # type: (Tensor, float) -> Tensor
    return torch.nn.functional.pad((8 / 12 * (x[:, 2:-2, 3:-1] - x[:, 2:-2, 1:-3])
                                    - 1 / 12 * (x[:, 2:-2, 4:] - x[:, 2:-2, :-4]))
                                   * one_over_dy, (2, 2, 2, 2))

def diffa_x(x, one_over_dx):
    # type: (Tensor, float) -> Tensor
    return -diff_x(x, one_over_dx)

def diffa_y(x, one_over_dy):
    # type: (Tensor, float) -> Tensor
    return -diff_y(x, one_over_dy)

def diff2_x(x, one_over_dx2):
    # type: (Tensor, float) -> Tensor
    return torch.nn.functional.pad((
            - 5 / 2 * x[:, 2:-2, 2:-2]
            + 4 / 3 * (x[:, 3:-1, 2:-2] + x[:, 1:-3, 2:-2])
            - 1 / 12 * (x[:, 4:, 2:-2] + x[:, :-4, 2:-2])
           ) * one_over_dx2, (2, 2, 2, 2))

def diff2_y(x, one_over_dy2):
    # type: (Tensor, float) -> Tensor
    return torch.nn.functional.pad((
            - 5 / 2 * x[:, 2:-2, 2:-2]
            + 4 / 3 * (x[:, 2:-2, 3:-1] + x[:, 2:-2, 1:-3])
            - 1 / 12 * (x[:, 2:-2, 4:] + x[:, 2:-2, :-4])
           ) * one_over_dy2, (2, 2, 2, 2))


def step(v2dt2, wfc, wfp, psix, psiy, zetax, zetay,
         ax, ay, bx, by, one_over_dx2, one_over_dy2,
         one_over_dx, one_over_dy):
    # type: (Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, float, float, float, float) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]
    d2wdx2 = diff2_x(wfc, one_over_dx2)
    d2wdy2 = diff2_y(wfc, one_over_dy2)

    psix = ax * psix + bx * diff_x(wfc, one_over_dx)
    psiy = ay * psiy + by * diff_y(wfc, one_over_dy)

    psix_x = diff_x(psix, one_over_dx)
    psiy_y = diff_y(psiy, one_over_dy)

    zetax = ax * zetax + bx * (d2wdx2 + psix_x)
    zetay = ay * zetay + by * (d2wdy2 + psiy_y)

    wfn = (v2dt2 * (d2wdx2 + d2wdy2 + psix_x + psiy_y + zetax + zetay)
           + 2 * wfc - wfp)

    return wfn, wfc, psix, psiy, zetax, zetay

def step_bwd(v2dt2, wfc, wfp, psix, psiy, zetax, zetay,
             ax, ay, bx, by, one_over_dx2, one_over_dy2,
             one_over_dx, one_over_dy):
    wfn = (
           diff2_x((1 + bx) * v2dt2 * wfc, one_over_dx2)
           + diff2_y((1 + by) * v2dt2 * wfc, one_over_dy2)
           + diffa_x(bx*diffa_x((1 + bx) * v2dt2 * wfc, one_over_dx), one_over_dx)
           + diffa_y(by*diffa_y((1 + by) * v2dt2 * wfc, one_over_dy), one_over_dy)
           + 2 * wfc
           + wfp
           + diff2_x(bx * zetax, one_over_dx2) + diffa_x(bx * diffa_x(bx * zetax, one_over_dx), one_over_dx)
           + diff2_y(by * zetay, one_over_dy2) + diffa_y(by * diffa_y(by * zetay, one_over_dy), one_over_dy)
           + diffa_x(bx * psix, one_over_dx)
           + diffa_y(by * psiy, one_over_dy))
    wfp = -wfc
    psix = ax * diffa_x((1 + bx) * v2dt2 * wfc, one_over_dx) + ax * diffa_x(bx * zetax, one_over_dx) + ax * psix
    psiy = ay * diffa_y((1 + by) * v2dt2 * wfc, one_over_dy) + ay * diffa_y(by * zetay, one_over_dy) + ay * psiy
    zetax = ax * v2dt2 * wfc + ax * zetax
    zetay = ay * v2dt2 * wfc + ay * zetay
    return wfn, wfp, psix, psiy, zetax, zetay
