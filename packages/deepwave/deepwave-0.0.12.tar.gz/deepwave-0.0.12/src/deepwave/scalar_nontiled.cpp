#include <torch/script.h>
#include <torch/torch.h>

#include <iostream>

TORCH_LIBRARY_FRAGMENT(deepwave, m) {
  m.def(
      "scalar(Tensor v, Tensor f, Tensor wfc0, Tensor wfp0, Tensor psix0, "
      "Tensor psiy0, Tensor zetax0, Tensor zetay0, Tensor ax, Tensor ay, "
      "Tensor bx, Tensor by, Tensor sources_i, Tensor receivers_i, float dx, "
      "float dy, float dt, int nt, int n_batch, int step_ratio, int accuracy, "
      "int pml_width0, int pml_width1, int pml_width2, int pml_width3) "
      "-> Tensor[]");
}

std::vector<torch::Tensor> scalar(
    torch::Tensor const &v, torch::Tensor const &f, torch::Tensor const &wfc0,
    torch::Tensor const &wfp0, torch::Tensor const &psix0,
    torch::Tensor const &psiy0, torch::Tensor const &zetax0,
    torch::Tensor const &zetay0, torch::Tensor const &ax,
    torch::Tensor const &ay, torch::Tensor const &bx, torch::Tensor const &by,
    torch::Tensor const &sources_i, torch::Tensor const &receivers_i, double dx,
    double dy, double dt, int64_t nt, int64_t n_batch, int64_t step_ratio,
    int64_t accuracy, int64_t pml_width0, int64_t pml_width1,
    int64_t pml_width2, int64_t pml_width3) {
  static auto op = torch::Dispatcher::singleton()
                       .findSchemaOrThrow("deepwave::scalar", "")
                       .typed<decltype(scalar)>();
  return op.call(v, f, wfc0, wfp0, psix0, psiy0, zetax0, zetay0, ax, ay, bx, by,
                 sources_i, receivers_i, dx, dy, dt, nt, n_batch, step_ratio,
                 accuracy, pml_width0, pml_width1, pml_width2, pml_width3);
}

namespace {
template <typename T, int A>
inline T diffx(T const *__restrict a, T one_over_dx, int64_t ny) {
  if (A == 2) {
    return static_cast<T>(1.0 / 2.0) * (a[ny] - a[-ny]) * one_over_dx;
  } else if (A == 4) {
    return (static_cast<T>(8.0 / 12.0) * (a[ny] - a[-ny]) -
            static_cast<T>(1.0 / 12.0) * (a[2 * ny] - a[-2 * ny])) *
           one_over_dx;
  } else if (A == 6) {
    return (static_cast<T>(3.0 / 4.0) * (a[ny] - a[-ny]) -
            static_cast<T>(3.0 / 20.0) * (a[2 * ny] - a[-2 * ny]) +
            static_cast<T>(1.0 / 60.0) * (a[3 * ny] - a[-3 * ny])) *
           one_over_dx;
  } else {
    return (static_cast<T>(4.0 / 5.0) * (a[ny] - a[-ny]) -
            static_cast<T>(1.0 / 5.0) * (a[2 * ny] - a[-2 * ny]) +
            static_cast<T>(4.0 / 105.0) * (a[3 * ny] - a[-3 * ny]) -
            static_cast<T>(1.0 / 280.0) * (a[4 * ny] - a[-4 * ny])) *
           one_over_dx;
  }
}

template <typename T, int A>
inline T diffx2(T const *__restrict a, T one_over_dx2, int64_t ny) {
  if (A == 2) {
    return (-static_cast<T>(2.0) * a[0] + a[ny] + a[-ny]) * one_over_dx2;
  } else if (A == 4) {
    return (-static_cast<T>(5.0 / 2.0) * a[0] +
            static_cast<T>(4.0 / 3.0) * (a[ny] + a[-ny]) -
            static_cast<T>(1.0 / 12.0) * (a[2 * ny] + a[-2 * ny])) *
           one_over_dx2;
  } else if (A == 6) {
    return (-static_cast<T>(49.0 / 18.0) * a[0] +
            static_cast<T>(3.0 / 2.0) * (a[ny] + a[-ny]) -
            static_cast<T>(3.0 / 20.0) * (a[2 * ny] + a[-2 * ny]) +
            static_cast<T>(1.0 / 90.0) * (a[3 * ny] + a[-3 * ny])) *
           one_over_dx2;
  } else {
    return (-static_cast<T>(205.0 / 72.0) * a[0] +
            static_cast<T>(8.0 / 5.0) * (a[ny] + a[-ny]) -
            static_cast<T>(1.0 / 5.0) * (a[2 * ny] + a[-2 * ny]) +
            static_cast<T>(8.0 / 315.0) * (a[3 * ny] + a[-3 * ny]) -
            static_cast<T>(1.0 / 560.0) * (a[4 * ny] + a[-4 * ny])) *
           one_over_dx2;
  }
}

template <typename T, int A>
inline T diffy(T const *__restrict a, T one_over_dy) {
  if (A == 2) {
    return static_cast<T>(1.0 / 2.0) * (a[1] - a[-1]) * one_over_dy;
  } else if (A == 4) {
    return (static_cast<T>(8.0 / 12.0) * (a[1] - a[-1]) -
            static_cast<T>(1.0 / 12.0) * (a[2] - a[-2])) *
           one_over_dy;
  } else if (A == 6) {
    return (static_cast<T>(3.0 / 4.0) * (a[1] - a[-1]) -
            static_cast<T>(3.0 / 20.0) * (a[2] - a[-2]) +
            static_cast<T>(1.0 / 60.0) * (a[3] - a[-3])) *
           one_over_dy;
  } else {
    return (static_cast<T>(4.0 / 5.0) * (a[1] - a[-1]) -
            static_cast<T>(1.0 / 5.0) * (a[2] - a[-2]) +
            static_cast<T>(4.0 / 105.0) * (a[3] - a[-3]) -
            static_cast<T>(1.0 / 280.0) * (a[4] - a[-4])) *
           one_over_dy;
  }
}

template <typename T, int A>
inline T diffy2(T const *__restrict a, T one_over_dy2) {
  if (A == 2) {
    return (-static_cast<T>(2.0) * a[0] + a[1] + a[-1]) * one_over_dy2;
  } else if (A == 4) {
    return (-static_cast<T>(5.0 / 2.0) * a[0] +
            static_cast<T>(4.0 / 3.0) * (a[1] + a[-1]) -
            static_cast<T>(1.0 / 12.0) * (a[2] + a[-2])) *
           one_over_dy2;
  } else if (A == 6) {
    return (-static_cast<T>(49.0 / 18.0) * a[0] +
            static_cast<T>(3.0 / 2.0) * (a[1] + a[-1]) -
            static_cast<T>(3.0 / 20.0) * (a[2] + a[-2]) +
            static_cast<T>(1.0 / 90.0) * (a[3] + a[-3])) *
           one_over_dy2;
  } else {
    return (-static_cast<T>(205.0 / 72.0) * a[0] +
            static_cast<T>(8.0 / 5.0) * (a[1] + a[-1]) -
            static_cast<T>(1.0 / 5.0) * (a[2] + a[-2]) +
            static_cast<T>(8.0 / 315.0) * (a[3] + a[-3]) -
            static_cast<T>(1.0 / 560.0) * (a[4] + a[-4])) *
           one_over_dy2;
  }
}

torch::Tensor create_or_pad(torch::Tensor const &tensor, int64_t fd_pad,
                            at::TensorOptions const &options,
                            std::array<int64_t, 3> const &size) {
  if (tensor.numel() == 0) {
    return at::zeros(size, options);
  } else {
    return at::constant_pad_nd(tensor, {fd_pad, fd_pad, fd_pad, fd_pad});
  }
}

template <typename T, int A, bool v_requires_grad>
void forward_kernel(T const *__restrict wfc, T *__restrict wfp,
                    T const *__restrict psix, T const *__restrict psiy,
                    T *__restrict psixn, T *__restrict psiyn,
                    T *__restrict zetax, T *__restrict zetay,
                    T *__restrict dwdv, T const *__restrict v,
                    T const *__restrict ax, T const *__restrict ay,
                    T const *__restrict bx, T const *__restrict by,
                    T const *__restrict daxdx, T const *__restrict daydy,
                    T const *__restrict dbxdx, T const *__restrict dbydy,
                    int64_t nx, int64_t ny, T dt2, T one_over_dx, T one_over_dy,
                    T one_over_dx2, T one_over_dy2) {
  constexpr int fd_pad{A / 2};
  for (int64_t x = fd_pad; x < nx - fd_pad; ++x) {
    int64_t xi{x * ny};
    auto axi{ax[x]};
    auto bxi{bx[x]};
    auto daxdxi{daxdx[x]};
    auto dbxdxi{dbxdx[x]};
    for (int64_t y = fd_pad; y < ny - fd_pad; ++y) {
      int64_t i{xi + y};
      T dwdx{diffx<T, A>(wfc + i, one_over_dx, ny)};
      T dwdy{diffy<T, A>(wfc + i, one_over_dy)};
      T d2wdx2{diffx2<T, A>(wfc + i, one_over_dx2, ny)};
      T d2wdy2{diffy2<T, A>(wfc + i, one_over_dy2)};
      T tmpx{(1 + bxi) * d2wdx2 + dbxdxi * dwdx + daxdxi * psix[i] +
             axi * diffx<T, A>(psix + i, one_over_dx, ny)};
      T tmpy{(1 + by[y]) * d2wdy2 + dbydy[y] * dwdy + daydy[y] * psiy[i] +
             ay[y] * diffy<T, A>(psiy + i, one_over_dy)};
      T w_sum{(1 + bxi) * tmpx + (1 + by[y]) * tmpy + axi * zetax[i] +
              ay[y] * zetay[i]};
      if (v_requires_grad) {
        dwdv[i] = 2 * v[i] * dt2 * w_sum;
      }
      wfp[i] = v[i] * v[i] * dt2 * w_sum + 2 * wfc[i] - wfp[i];
      psixn[i] = bxi * dwdx + axi * psix[i];
      psiyn[i] = by[y] * dwdy + ay[y] * psiy[i];
      zetax[i] = bxi * tmpx + axi * zetax[i];
      zetay[i] = by[y] * tmpy + ay[y] * zetay[i];
    }
  }
}

template <typename T>
void add_sources(T *__restrict wf, T const *__restrict f,
                 int64_t const *__restrict sources_i,
                 int64_t n_sources_per_shot) {
  for (int64_t source_idx{}; source_idx < n_sources_per_shot; ++source_idx) {
    wf[sources_i[source_idx]] += f[source_idx];
  }
}

template <typename T>
void record_receivers(T *__restrict r, T const *__restrict wf,
                      int64_t const *__restrict receivers_i,
                      int64_t n_receivers_per_shot) {
  for (int64_t receiver_idx{}; receiver_idx < n_receivers_per_shot;
       ++receiver_idx) {
    r[receiver_idx] = wf[receivers_i[receiver_idx]];
  }
}

template <typename T, int A>
void add_to_grad_v(T *__restrict grad_v, T const *__restrict wfc,
                   T const *__restrict dwdv, int64_t step_ratio, int64_t nx,
                   int64_t ny) {
  constexpr int fd_pad{A / 2};
  for (int64_t x = fd_pad; x < nx - fd_pad; ++x) {
    int64_t xi{x * ny};
    for (int64_t y = fd_pad; y < ny - fd_pad; ++y) {
      int64_t i{xi + y};
      grad_v[i] += wfc[i] * dwdv[i] * step_ratio;
    }
  }
}

template <typename T, int A>
void backward_kernel(T const *__restrict wfc, T *__restrict wfp,
                     T *__restrict wfcn, T const *__restrict psix,
                     T const *__restrict psiy, T *__restrict psixn,
                     T *__restrict psiyn, T const *__restrict zetax,
                     T const *__restrict zetay, T *__restrict zetaxn,
                     T *__restrict zetayn, T const *__restrict v,
                     T const *__restrict dvdx, T const *__restrict dvdy,
                     T const *__restrict d2vdx2, T const *__restrict d2vdy2,
                     T const *__restrict ax, T const *__restrict ay,
                     T const *__restrict bx, T const *__restrict by,
                     T const *__restrict dbxdx, T const *__restrict dbydy,
                     T const *__restrict d2bxdx2, T const *__restrict d2bydy2,
                     int64_t nx, int64_t ny, T dt2, T one_over_dx,
                     T one_over_dy, T one_over_dx2, T one_over_dy2) {
  constexpr int fd_pad{A / 2};
  for (int64_t x = fd_pad; x < nx - fd_pad; ++x) {
    int64_t xi{x * ny};
    auto axi{ax[x]};
    auto bxi{bx[x]};
    auto dbxdxi{dbxdx[x]};
    auto d2bxdx2i{d2bxdx2[x]};
    for (int64_t y = fd_pad; y < ny - fd_pad; ++y) {
      int64_t i{xi + y};
      T dzetaxdx{diffx<T, A>(zetax + i, one_over_dx, ny)};
      T dzetaydy{diffy<T, A>(zetay + i, one_over_dy)};
      T d2zetaxdx2{diffx2<T, A>(zetax + i, one_over_dx2, ny)};
      T d2zetaydy2{diffy2<T, A>(zetay + i, one_over_dy2)};
      T dwfcdx{diffx<T, A>(wfc + i, one_over_dx, ny)};
      T dwfcdy{diffy<T, A>(wfc + i, one_over_dy)};
      T d2wfcdx2{diffx2<T, A>(wfc + i, one_over_dx2, ny)};
      T d2wfcdy2{diffy2<T, A>(wfc + i, one_over_dy2)};
      T v2{v[i] * v[i]};
      T tmp1x{v[i] * dt2 *
                  ((1 + bxi) * v[i] * dwfcdx +
                   2 * (1 + bxi) * wfc[i] * dvdx[i] + v[i] * wfc[i] * dbxdxi) +
              bxi * dzetaxdx + zetax[i] * dbxdxi - psix[i]};
      T tmp1y{v[i] * dt2 *
                  ((1 + by[y]) * v[i] * dwfcdy +
                   2 * (1 + by[y]) * wfc[i] * dvdy[i] +
                   v[i] * wfc[i] * dbydy[y]) +
              by[y] * dzetaydy + zetay[i] * dbydy[y] - psiy[i]};
      wfp[i] =
          tmp1x * dbxdxi + tmp1y * dbydy[y] +
          dt2 *
              (2 * (v[i] * d2vdx2[i] + dvdx[i] * dvdx[i]) * (1 + bxi) * wfc[i] +
               (1 + bxi) * v2 * d2wfcdx2 +
               4 * (1 + bxi) * v[i] * dvdx[i] * dwfcdx +
               v2 * wfc[i] * d2bxdx2i + 2 * v2 * dbxdxi * dwfcdx +
               4 * v[i] * wfc[i] * dbxdxi * dvdx[i]) +
          dt2 * (2 * (v[i] * d2vdy2[i] + dvdy[i] * dvdy[i]) * (1 + by[y]) *
                     wfc[i] +
                 (1 + by[y]) * v2 * d2wfcdy2 +
                 4 * (1 + by[y]) * v[i] * dvdy[i] * dwfcdy +
                 v2 * wfc[i] * d2bydy2[y] + 2 * v2 * dbydy[y] * dwfcdy +
                 4 * v[i] * wfc[i] * dbydy[y] * dvdy[i]) +
          dt2 *
              ((1 + bxi) * v2 * d2wfcdx2 +
               2 * (1 + bxi) * v[i] * wfc[i] * d2vdx2[i] +
               4 * (1 + bxi) * v[i] * dvdx[i] * dwfcdx +
               2 * (1 + bxi) * wfc[i] * dvdx[i] * dvdx[i] +
               v2 * wfc[i] * d2bxdx2i + 2 * v2 * dbxdxi * dwfcdx +
               4 * v[i] * wfc[i] * dbxdxi * dvdx[i]) *
              bxi +
          dt2 *
              ((1 + by[y]) * v2 * d2wfcdy2 +
               2 * (1 + by[y]) * v[i] * wfc[i] * d2vdy2[i] +
               4 * (1 + by[y]) * v[i] * dvdy[i] * dwfcdy +
               2 * (1 + by[y]) * wfc[i] * dvdy[i] * dvdy[i] +
               v2 * wfc[i] * d2bydy2[y] + 2 * v2 * dbydy[y] * dwfcdy +
               4 * v[i] * wfc[i] * dbydy[y] * dvdy[i]) *
              by[y] +
          (bxi * d2zetaxdx2 + zetax[i] * d2bxdx2i + 2 * dbxdxi * dzetaxdx) *
              bxi -
          bxi * diffx<T, A>(psix + i, one_over_dx, ny) + bxi * d2zetaxdx2 +
          zetax[i] * d2bxdx2i + 2 * dbxdxi * dzetaxdx +
          (by[y] * d2zetaydy2 + zetay[i] * d2bydy2[y] +
           2 * dbydy[y] * dzetaydy) *
              by[y] -
          by[y] * diffy<T, A>(psiy + i, one_over_dy) + by[y] * d2zetaydy2 +
          zetay[i] * d2bydy2[y] + 2 * dbydy[y] * dzetaydy + wfp[i] + 2 * wfc[i];
      wfcn[i] = -wfc[i];
      psixn[i] = -tmp1x * axi;
      psiyn[i] = -tmp1y * ay[y];
      zetaxn[i] = axi * v2 * dt2 * wfc[i] + axi * zetax[i];
      zetayn[i] = ay[y] * v2 * dt2 * wfc[i] + ay[y] * zetay[i];
    }
  }
}

// def step_bwd(v, wfc, wfp, psix, zetax,
//         ax, bx, dx, dt):
//    v2dt2 = v**2*dt**2
//    wfp = (
//        diff2((1+bx)**2*v2dt2*wfc, dx) - diff(diff(bx, dx)*(1+bx)*v2dt2*wfc,
//        dx) + 2*wfc
//        + wfp
//        + diff2((1+bx)*bx*zetax, dx) - diff(diff(bx, dx)*bx*zetax, dx)
//        - diff(bx * psix, dx)
//    )
//
//    psix = (-diff(ax*(1+bx)*v2dt2*wfc, dx) + diff(ax, dx) * (1+bx)*v2dt2*wfc
//            +diff(ax, dx)*bx*zetax - diff(ax*bx*zetax, dx)
//            +ax*psix)
//    zetax = ax*v2dt2*wfc + ax*zetax
//    return wfp, -wfc, psix, zetax

template <typename T, int A>
void forward_shot(T *wfc, T *wfp, T *psix, T *psiy, T *psixn, T *psiyn,
                  T *zetax, T *zetay, int64_t const *sources_i,
                  int64_t const *receivers_i, T *dwdv, T const *v, T const *f,
                  T *r, T const *ax, T const *ay, T const *bx, T const *by,
                  T const *daxdx, T const *daydy, T const *dbxdx,
                  T const *dbydy, T dt2, T one_over_dx, T one_over_dy,
                  T one_over_dx2, T one_over_dy2, int64_t n_sources_per_shot,
                  int64_t n_receivers_per_shot, int64_t nx, int64_t ny,
                  int64_t nt, int64_t step_ratio, bool v_requires_grad) {
  for (int64_t t{}; t < nt; ++t) {
    if (t % step_ratio == 0 and v_requires_grad) {
      forward_kernel<T, A, true>(wfc, wfp, psix, psiy, psixn, psiyn, zetax,
                                 zetay, dwdv + (t / step_ratio) * nx * ny, v,
                                 ax, ay, bx, by, daxdx, daydy, dbxdx, dbydy, nx,
                                 ny, dt2, one_over_dx, one_over_dy,
                                 one_over_dx2, one_over_dy2);
    } else {
      forward_kernel<T, A, false>(wfc, wfp, psix, psiy, psixn, psiyn, zetax,
                                  zetay, nullptr, v, ax, ay, bx, by, daxdx,
                                  daydy, dbxdx, dbydy, nx, ny, dt2, one_over_dx,
                                  one_over_dy, one_over_dx2, one_over_dy2);
    }
    if (n_sources_per_shot > 0) {
      add_sources(wfp, f + t * n_sources_per_shot, sources_i,
                  n_sources_per_shot);
    }
    if (n_receivers_per_shot > 0) {
      record_receivers(r + t * n_receivers_per_shot, wfc, receivers_i,
                       n_receivers_per_shot);
    }
    std::swap(wfp, wfc);
    std::swap(psixn, psix);
    std::swap(psiyn, psiy);
  }
}

template <typename T, int A>
void combine_grad_v(T *__restrict grad_v, T const *__restrict grad_v_batch,
                    int64_t n_parallel, int64_t nx, int64_t ny) {
  constexpr int fd_pad{A / 2};
  int64_t nxny{nx * ny};
  for (int64_t x = fd_pad; x < nx - fd_pad; ++x) {
    int64_t xi{x * ny};
    for (int64_t y = fd_pad; y < ny - fd_pad; ++y) {
      int64_t i{xi + y};
      for (int64_t batch{}; batch < n_parallel; ++batch) {
        grad_v[i] += grad_v_batch[batch * nxny + i];
      }
    }
  }
}

template <typename T, int A>
void backward_shot(T *wfc, T *wfp, T *wfcn, T *psix, T *psiy, T *psixn,
                   T *psiyn, T *zetax, T *zetay, T *zetaxn, T *zetayn,
                   int64_t const *sources_i, int64_t const *receivers_i,
                   T *dwdv, T const *v, T const *dvdx, T const *dvdy,
                   T const *d2vdx2, T const *d2vdy2, T *f, T const *r,
                   T *grad_v, T const *ax, T const *ay, T const *bx,
                   T const *by, T const *dbxdx, T const *dbydy,
                   T const *d2bxdx2, T const *d2bydy2, T dt2, T one_over_dx,
                   T one_over_dy, T one_over_dx2, T one_over_dy2,
                   int64_t n_sources_per_shot, int64_t n_receivers_per_shot,
                   int64_t nx, int64_t ny, int64_t nt, int64_t step_ratio,
                   bool v_requires_grad) {
  for (int64_t t{nt - 1}; t >= 0; --t) {
    if (n_receivers_per_shot > 0) {
      add_sources(wfp, r + t * n_receivers_per_shot, receivers_i,
                  n_receivers_per_shot);
    }
    if (n_sources_per_shot > 0) {
      record_receivers(f + t * n_sources_per_shot, wfc, sources_i,
                       n_sources_per_shot);
    }
    if (t % step_ratio == 0 and v_requires_grad) {
      add_to_grad_v<T, A>(grad_v, wfc, dwdv + (t / step_ratio) * nx * ny,
                          step_ratio, nx, ny);
    }
    backward_kernel<T, A>(wfc, wfp, wfcn, psix, psiy, psixn, psiyn, zetax,
                          zetay, zetaxn, zetayn, v, dvdx, dvdy, d2vdx2, d2vdy2,
                          ax, ay, bx, by, dbxdx, dbydy, d2bxdx2, d2bydy2, nx,
                          ny, dt2, one_over_dx, one_over_dy, one_over_dx2,
                          one_over_dy2);
    T *tmp{wfc};
    wfc = wfp;
    wfp = wfcn;
    wfcn = tmp;
    std::swap(psixn, psix);
    std::swap(psiyn, psiy);
    std::swap(zetaxn, zetax);
    std::swap(zetayn, zetay);
  }
}

void zero_interior(torch::Tensor tensor, int64_t nx, int64_t ny, int fd_pad,
                   int64_t const pml_width[4]) {
  at::indexing::TensorIndex all_slice{torch::indexing::Slice()};
  at::indexing::TensorIndex slicex{torch::indexing::Slice(
      fd_pad + pml_width[0], nx - pml_width[1] - fd_pad)};
  at::indexing::TensorIndex slicey{torch::indexing::Slice(
      fd_pad + pml_width[2], ny - pml_width[3] - fd_pad)};
  tensor.index_put_({all_slice, slicex, slicey}, 0);
}

}  // namespace

class ScalarCPUFunction : public torch::autograd::Function<ScalarCPUFunction> {
 public:
  static std::vector<torch::Tensor> forward(
      torch::autograd::AutogradContext *ctx, torch::Tensor const &v,
      torch::Tensor const &f, torch::Tensor const &wfc0,
      torch::Tensor const &wfp0, torch::Tensor const &psix0,
      torch::Tensor const &psiy0, torch::Tensor const &zetax0,
      torch::Tensor const &zetay0, torch::Tensor const &ax,
      torch::Tensor const &ay, torch::Tensor const &bx, torch::Tensor const &by,
      torch::Tensor const &sources_i, torch::Tensor const &receivers_i,
      double dx, double dy, double dt, int64_t nt, int64_t n_batch,
      int64_t step_ratio, int64_t accuracy, int64_t pml_width0,
      int64_t pml_width1, int64_t pml_width2, int64_t pml_width3) {
    at::AutoDispatchBelowADInplaceOrView g;
    auto options{at::device(v.device()).dtype(v.scalar_type())};
    auto nx{v.size(0)};
    auto ny{v.size(1)};
    std::array<int64_t, 3> size_with_batch{n_batch, nx, ny};
    auto fd_pad{accuracy / 2};
    int64_t const pml_width[4] = {pml_width0, pml_width1, pml_width2,
                                  pml_width3};
    int64_t n_sources_per_shot{};
    if (sources_i.numel() > 0) {
      n_sources_per_shot = sources_i.size(1);
    }
    int64_t n_receivers_per_shot{};
    if (receivers_i.numel() > 0) {
      n_receivers_per_shot = receivers_i.size(1);
    }
    auto wfc{create_or_pad(wfc0, fd_pad, options, size_with_batch)};
    auto wfp{create_or_pad(wfp0, fd_pad, options, size_with_batch)};
    auto psix{create_or_pad(psix0, fd_pad, options, size_with_batch)};
    auto psiy{create_or_pad(psiy0, fd_pad, options, size_with_batch)};
    auto zetax{create_or_pad(zetax0, fd_pad, options, size_with_batch)};
    auto zetay{create_or_pad(zetay0, fd_pad, options, size_with_batch)};
    auto psixn{at::zeros_like(psix)};
    auto psiyn{at::zeros_like(psiy)};
    auto r{at::empty({n_batch, nt, n_receivers_per_shot}, options)};
    torch::Tensor dwdv;
    auto daxdx{at::zeros_like(ax)};
    auto daydy{at::zeros_like(ay)};
    auto dbxdx{at::zeros_like(bx)};
    auto dbydy{at::zeros_like(by)};
    if (v.requires_grad()) {
      dwdv = at::empty({n_batch, (nt + step_ratio - 1) / step_ratio, nx, ny},
                       options);
    }

    zero_interior(psix, nx, ny, fd_pad, pml_width);
    zero_interior(psiy, nx, ny, fd_pad, pml_width);
    zero_interior(zetax, nx, ny, fd_pad, pml_width);
    zero_interior(zetay, nx, ny, fd_pad, pml_width);

    AT_DISPATCH_FLOATING_TYPES(
        v.scalar_type(), "scalar_cpu_forward", ([&] {
          scalar_t dt2_a = dt * dt;
          scalar_t one_over_dx_a = 1.0 / dx;
          scalar_t one_over_dy_a = 1.0 / dy;
          scalar_t one_over_dx2_a = 1.0 / (dx * dx);
          scalar_t one_over_dy2_a = 1.0 / (dy * dy);
          auto v_a{v.data_ptr<scalar_t>()};
          auto f_a{f.data_ptr<scalar_t>()};
          auto r_a{r.data_ptr<scalar_t>()};
          auto wfc_a{wfc.data_ptr<scalar_t>()};
          auto wfp_a{wfp.data_ptr<scalar_t>()};
          auto psix_a{psix.data_ptr<scalar_t>()};
          auto psiy_a{psiy.data_ptr<scalar_t>()};
          auto psixn_a{psixn.data_ptr<scalar_t>()};
          auto psiyn_a{psiyn.data_ptr<scalar_t>()};
          auto zetax_a{zetax.data_ptr<scalar_t>()};
          auto zetay_a{zetay.data_ptr<scalar_t>()};
          auto ax_a{ax.data_ptr<scalar_t>()};
          auto ay_a{ay.data_ptr<scalar_t>()};
          auto bx_a{bx.data_ptr<scalar_t>()};
          auto by_a{by.data_ptr<scalar_t>()};
          auto daxdx_a{daxdx.data_ptr<scalar_t>()};
          auto daydy_a{daydy.data_ptr<scalar_t>()};
          auto dbxdx_a{dbxdx.data_ptr<scalar_t>()};
          auto dbydy_a{dbydy.data_ptr<scalar_t>()};
          auto sources_i_a{sources_i.data_ptr<int64_t>()};
          auto receivers_i_a{receivers_i.data_ptr<int64_t>()};
          scalar_t *dwdv_a{};
          if (v.requires_grad()) {
            dwdv_a = dwdv.data_ptr<scalar_t>();
          }
          constexpr scalar_t (*diffys[])(scalar_t const *__restrict, scalar_t){
              diffy<scalar_t, 2>, diffy<scalar_t, 4>, diffy<scalar_t, 6>,
              diffy<scalar_t, 8>};
          auto diffyi{diffys[accuracy / 2 - 1]};
          for (int64_t x{fd_pad}; x < nx - fd_pad; ++x) {
            daxdx_a[x] = diffyi(ax_a + x, one_over_dx_a);
          }
          for (int64_t y{fd_pad}; y < ny - fd_pad; ++y) {
            daydy_a[y] = diffyi(ay_a + y, one_over_dy_a);
          }
          for (int64_t x{fd_pad}; x < nx - fd_pad; ++x) {
            dbxdx_a[x] = diffyi(bx_a + x, one_over_dx_a);
          }
          for (int64_t y{fd_pad}; y < ny - fd_pad; ++y) {
            dbydy_a[y] = diffyi(by_a + y, one_over_dy_a);
          }
          constexpr void (*forward_shots[])(
              scalar_t * wfc, scalar_t * wfp, scalar_t * psix, scalar_t * psiy,
              scalar_t * psixn, scalar_t * psiyn, scalar_t * zetax,
              scalar_t * zetay, int64_t const *sources_i,
              int64_t const *receivers_i, scalar_t *dwdv, scalar_t const *v,
              scalar_t const *f, scalar_t *r, scalar_t const *ax,
              scalar_t const *ay, scalar_t const *bx, scalar_t const *by,
              scalar_t const *daxdx, scalar_t const *daydy,
              scalar_t const *dbxdx, scalar_t const *dbydy, scalar_t dt2,
              scalar_t one_over_dx, scalar_t one_over_dy, scalar_t one_over_dx2,
              scalar_t one_over_dy2, int64_t n_sources_per_shot,
              int64_t n_receivers_per_shot, int64_t nx, int64_t ny, int64_t nt,
              int64_t step_ratio, bool v_requires_grad){
              forward_shot<scalar_t, 2>, forward_shot<scalar_t, 4>,
              forward_shot<scalar_t, 6>, forward_shot<scalar_t, 8>};
          at::parallel_for(0, n_batch, 0, [&](int64_t bstart, int64_t bend) {
            for (int64_t shot = bstart; shot < bend; ++shot) {
              auto i{shot * nx * ny};
              auto si{shot * n_sources_per_shot};
              auto ri{shot * n_receivers_per_shot};
              forward_shots[accuracy / 2 - 1](
                  wfc_a + i, wfp_a + i, psix_a + i, psiy_a + i, psixn_a + i,
                  psiyn_a + i, zetax_a + i, zetay_a + i, sources_i_a + si,
                  receivers_i_a + ri, dwdv_a + i * (nt / step_ratio), v_a,
                  f_a + si * nt, r_a + ri * nt, ax_a, ay_a, bx_a, by_a, daxdx_a,
                  daydy_a, dbxdx_a, dbydy_a, dt2_a, one_over_dx_a,
                  one_over_dy_a, one_over_dx2_a, one_over_dy2_a,
                  n_sources_per_shot, n_receivers_per_shot, nx, ny, nt,
                  step_ratio, v.requires_grad());
            }
          });
        }));

    if (v.requires_grad() or f.requires_grad() or wfc0.requires_grad() or
        wfp0.requires_grad() or psix0.requires_grad() or
        psiy0.requires_grad() or zetax0.requires_grad() or
        zetay0.requires_grad()) {
      ctx->save_for_backward({v, ax, ay, bx, by, sources_i, receivers_i});
      ctx->saved_data["dwdv"] = dwdv;
      ctx->saved_data["dx"] = dx;
      ctx->saved_data["dy"] = dy;
      ctx->saved_data["dt"] = dt;
      ctx->saved_data["nt"] = nt;
      ctx->saved_data["n_batch"] = n_batch;
      ctx->saved_data["step_ratio"] = step_ratio;
      ctx->saved_data["accuracy"] = accuracy;
      ctx->saved_data["pml_width0"] = pml_width[0];
      ctx->saved_data["pml_width1"] = pml_width[1];
      ctx->saved_data["pml_width2"] = pml_width[2];
      ctx->saved_data["pml_width3"] = pml_width[3];
    }
    auto all_slice{torch::indexing::Slice()};
    auto slicex{torch::indexing::Slice(fd_pad, nx - fd_pad)};
    auto slicey{torch::indexing::Slice(fd_pad, ny - fd_pad)};
    if (nt & 1) {
      return {wfp.index({all_slice, slicex, slicey}),
              wfc.index({all_slice, slicex, slicey}),
              psixn.index({all_slice, slicex, slicey}),
              psiyn.index({all_slice, slicex, slicey}),
              zetax.index({all_slice, slicex, slicey}),
              zetay.index({all_slice, slicex, slicey}),
              r};
    }
    return {wfc.index({all_slice, slicex, slicey}),
            wfp.index({all_slice, slicex, slicey}),
            psix.index({all_slice, slicex, slicey}),
            psiy.index({all_slice, slicex, slicey}),
            zetax.index({all_slice, slicex, slicey}),
            zetay.index({all_slice, slicex, slicey}),
            r};
  }

  static torch::autograd::tensor_list backward(
      torch::autograd::AutogradContext *ctx,
      torch::autograd::tensor_list const &grad_outputs) {
    at::AutoDispatchBelowADInplaceOrView g;
    auto saved{ctx->get_saved_variables()};
    auto const &v{saved[0]};
    auto const &ax{saved[1]};
    auto const &ay{saved[2]};
    auto const &bx{saved[3]};
    auto const &by{saved[4]};
    auto const &sources_i{saved[5]};
    auto const &receivers_i{saved[6]};
    auto const &dwdv{ctx->saved_data["dwdv"].toTensor()};
    auto dx{ctx->saved_data["dx"].toDouble()};
    auto dy{ctx->saved_data["dy"].toDouble()};
    auto dt{ctx->saved_data["dt"].toDouble()};
    auto nt{ctx->saved_data["nt"].toInt()};
    auto n_batch{ctx->saved_data["n_batch"].toInt()};
    auto step_ratio{ctx->saved_data["step_ratio"].toInt()};
    auto accuracy{ctx->saved_data["accuracy"].toInt()};
    int64_t const pml_width[4] = {ctx->saved_data["pml_width0"].toInt(),
                                  ctx->saved_data["pml_width1"].toInt(),
                                  ctx->saved_data["pml_width2"].toInt(),
                                  ctx->saved_data["pml_width3"].toInt()};
    auto fd_pad{accuracy / 2};

    auto wfc =
        at::constant_pad_nd(grad_outputs[0], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto wfp =
        at::constant_pad_nd(grad_outputs[1], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto psix =
        at::constant_pad_nd(grad_outputs[2], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto psiy =
        at::constant_pad_nd(grad_outputs[3], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto zetax =
        at::constant_pad_nd(grad_outputs[4], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto zetay =
        at::constant_pad_nd(grad_outputs[5], {fd_pad, fd_pad, fd_pad, fd_pad});
    auto wfcn{at::zeros_like(wfc)};
    auto psixn{at::zeros_like(psix)};
    auto psiyn{at::zeros_like(psiy)};
    auto zetaxn{at::zeros_like(zetax)};
    auto zetayn{at::zeros_like(zetay)};
    auto grad_r{grad_outputs[6].contiguous()};
    auto dbxdx{at::zeros_like(bx)};
    auto dbydy{at::zeros_like(by)};
    auto d2bxdx2{at::zeros_like(bx)};
    auto d2bydy2{at::zeros_like(by)};
    auto dvdx{torch::zeros_like(v)};
    auto dvdy{torch::zeros_like(v)};
    auto d2vdx2{torch::zeros_like(v)};
    auto d2vdy2{torch::zeros_like(v)};
    auto options{at::device(v.device()).dtype(v.scalar_type())};
    auto nx{v.size(0)};
    auto ny{v.size(1)};
    int64_t n_sources_per_shot{};
    if (sources_i.numel() > 0) {
      n_sources_per_shot = sources_i.size(1);
    }
    int64_t n_receivers_per_shot{};
    if (receivers_i.numel() > 0) {
      n_receivers_per_shot = receivers_i.size(1);
    }

    int64_t n_parallel{
        std::min(static_cast<int>(n_batch), at::get_num_threads())};
    auto grad_v{at::zeros({nx, ny}, options)};
    auto grad_v_batch{n_parallel > 1 ? at::zeros({n_parallel, nx, ny}, options)
                                     : at::empty(0)};
    auto grad_f{at::empty({n_batch, nt, n_sources_per_shot}, options)};

    AT_DISPATCH_FLOATING_TYPES(
        v.scalar_type(), "scalar_cpu_backward", ([&] {
          scalar_t dt2_a = dt * dt;
          scalar_t one_over_dx_a = 1.0 / dx;
          scalar_t one_over_dy_a = 1.0 / dy;
          scalar_t one_over_dx2_a = 1.0 / (dx * dx);
          scalar_t one_over_dy2_a = 1.0 / (dy * dy);
          auto v_a{v.data_ptr<scalar_t>()};
          auto grad_v_a{grad_v.data_ptr<scalar_t>()};
          auto grad_v_batch_a{n_parallel > 1 ? grad_v_batch.data_ptr<scalar_t>()
                                             : grad_v_a};
          auto grad_r_a{grad_r.data_ptr<scalar_t>()};
          auto grad_f_a{grad_f.data_ptr<scalar_t>()};
          auto wfc_a{wfc.data_ptr<scalar_t>()};
          auto wfp_a{wfp.data_ptr<scalar_t>()};
          auto wfcn_a{wfcn.data_ptr<scalar_t>()};
          auto psix_a{psix.data_ptr<scalar_t>()};
          auto psiy_a{psiy.data_ptr<scalar_t>()};
          auto psixn_a{psixn.data_ptr<scalar_t>()};
          auto psiyn_a{psiyn.data_ptr<scalar_t>()};
          auto zetax_a{zetax.data_ptr<scalar_t>()};
          auto zetay_a{zetay.data_ptr<scalar_t>()};
          auto zetaxn_a{zetaxn.data_ptr<scalar_t>()};
          auto zetayn_a{zetayn.data_ptr<scalar_t>()};
          auto ax_a{ax.data_ptr<scalar_t>()};
          auto ay_a{ay.data_ptr<scalar_t>()};
          auto bx_a{bx.data_ptr<scalar_t>()};
          auto by_a{by.data_ptr<scalar_t>()};
          auto dbxdx_a{dbxdx.data_ptr<scalar_t>()};
          auto dbydy_a{dbydy.data_ptr<scalar_t>()};
          auto d2bxdx2_a{d2bxdx2.data_ptr<scalar_t>()};
          auto d2bydy2_a{d2bydy2.data_ptr<scalar_t>()};
          auto sources_i_a{sources_i.data_ptr<int64_t>()};
          auto receivers_i_a{receivers_i.data_ptr<int64_t>()};
          auto dvdx_a{dvdx.data_ptr<scalar_t>()};
          auto dvdy_a{dvdy.data_ptr<scalar_t>()};
          auto d2vdx2_a{d2vdx2.data_ptr<scalar_t>()};
          auto d2vdy2_a{d2vdy2.data_ptr<scalar_t>()};
          scalar_t *dwdv_a{};
          if (v.requires_grad()) {
            dwdv_a = dwdv.data_ptr<scalar_t>();
          }
          constexpr scalar_t (*diffxs[])(scalar_t const *__restrict, scalar_t,
                                         int64_t){
              diffx<scalar_t, 2>, diffx<scalar_t, 4>, diffx<scalar_t, 6>,
              diffx<scalar_t, 8>};
          constexpr scalar_t (*diffys[])(scalar_t const *__restrict, scalar_t){
              diffy<scalar_t, 2>, diffy<scalar_t, 4>, diffy<scalar_t, 6>,
              diffy<scalar_t, 8>};
          constexpr scalar_t (*diffx2s[])(scalar_t const *__restrict, scalar_t,
                                          int64_t){
              diffx2<scalar_t, 2>, diffx2<scalar_t, 4>, diffx2<scalar_t, 6>,
              diffx2<scalar_t, 8>};
          constexpr scalar_t (*diffy2s[])(scalar_t const *__restrict, scalar_t){
              diffy2<scalar_t, 2>, diffy2<scalar_t, 4>, diffy2<scalar_t, 6>,
              diffy2<scalar_t, 8>};
          auto diffxi{diffxs[accuracy / 2 - 1]};
          auto diffyi{diffys[accuracy / 2 - 1]};
          auto diffx2i{diffx2s[accuracy / 2 - 1]};
          auto diffy2i{diffy2s[accuracy / 2 - 1]};
          for (int64_t x{fd_pad}; x < nx - fd_pad; ++x) {
            dbxdx_a[x] = diffyi(bx_a + x, one_over_dx_a);
            d2bxdx2_a[x] = diffy2i(bx_a + x, one_over_dx_a);
          }
          for (int64_t y{fd_pad}; y < ny - fd_pad; ++y) {
            dbydy_a[y] = diffyi(by_a + y, one_over_dy_a);
            d2bydy2_a[y] = diffy2i(by_a + y, one_over_dy_a);
          }
          for (int64_t x{fd_pad}; x < nx - fd_pad; ++x) {
            int64_t xi{x * ny};
            for (int64_t y{fd_pad}; y < ny - fd_pad; ++y) {
              int64_t i{xi + y};
              dvdx_a[i] = diffxi(v_a + i, one_over_dx_a, ny);
              d2vdx2_a[i] = diffx2i(v_a + i, one_over_dx_a, ny);
              dvdy_a[i] = diffyi(v_a + i, one_over_dy_a);
              d2vdy2_a[i] = diffy2i(v_a + i, one_over_dy_a);
            }
          }
          constexpr void (*backward_shots[])(
              scalar_t * wfc, scalar_t * wfp, scalar_t * wfcn, scalar_t * psix,
              scalar_t * psiy, scalar_t * psixn, scalar_t * psiyn,
              scalar_t * zetax, scalar_t * zetay, scalar_t * zetaxn,
              scalar_t * zetayn, int64_t const *sources_i,
              int64_t const *receivers_i, scalar_t *dwdv, scalar_t const *v,
              scalar_t const *dvdx, scalar_t const *dvdy,
              scalar_t const *d2vdx2, scalar_t const *d2vdy2, scalar_t *f,
              scalar_t const *r, scalar_t *grad_v, scalar_t const *ax,
              scalar_t const *ay, scalar_t const *bx, scalar_t const *by,
              scalar_t const *dbxdx, scalar_t const *dbydy,
              scalar_t const *d2bxdx2, scalar_t const *d2bydy2, scalar_t dt2,
              scalar_t one_over_dx, scalar_t one_over_dy, scalar_t one_over_dx2,
              scalar_t one_over_dy2, int64_t n_sources_per_shot,
              int64_t n_receivers_per_shot, int64_t nx, int64_t ny, int64_t nt,
              int64_t step_ratio, bool v_requires_grad){
              backward_shot<scalar_t, 2>, backward_shot<scalar_t, 4>,
              backward_shot<scalar_t, 6>, backward_shot<scalar_t, 8>};
          at::parallel_for(0, n_batch, 0, [&](int64_t bstart, int64_t bend) {
            for (int64_t shot = bstart; shot < bend; ++shot) {
              auto i{shot * nx * ny};
              auto si{shot * n_sources_per_shot};
              auto ri{shot * n_receivers_per_shot};
              backward_shots[accuracy / 2 - 1](
                  wfc_a + i, wfp_a + i, wfcn_a + i, psix_a + i, psiy_a + i,
                  psixn_a + i, psiyn_a + i, zetax_a + i, zetay_a + i,
                  zetaxn_a + i, zetayn_a + i, sources_i_a + si,
                  receivers_i_a + ri, dwdv_a + i * (nt / step_ratio), v_a,
                  dvdx_a, dvdy_a, d2vdx2_a, d2vdy2_a, grad_f_a + si * nt,
                  grad_r_a + ri * nt,
                  grad_v_batch_a + at::get_thread_num() * nx * ny, ax_a, ay_a,
                  bx_a, by_a, dbxdx_a, dbydy_a, d2bxdx2_a, d2bydy2_a, dt2_a,
                  one_over_dx_a, one_over_dy_a, one_over_dx2_a, one_over_dy2_a,
                  n_sources_per_shot, n_receivers_per_shot, nx, ny, nt,
                  step_ratio, v.requires_grad());
            }
          });
          if (v.requires_grad() and n_parallel > 1) {
            if (accuracy == 2) {
              combine_grad_v<scalar_t, 2>(grad_v_a, grad_v_batch_a, n_parallel,
                                          nx, ny);
            } else if (accuracy == 4) {
              combine_grad_v<scalar_t, 4>(grad_v_a, grad_v_batch_a, n_parallel,
                                          nx, ny);
            } else if (accuracy == 6) {
              combine_grad_v<scalar_t, 6>(grad_v_a, grad_v_batch_a, n_parallel,
                                          nx, ny);
            } else {
              combine_grad_v<scalar_t, 8>(grad_v_a, grad_v_batch_a, n_parallel,
                                          nx, ny);
            }
          }
        }));

    auto all_slice{torch::indexing::Slice()};
    auto slicex{torch::indexing::Slice(fd_pad, nx - fd_pad)};
    auto slicey{torch::indexing::Slice(fd_pad, ny - fd_pad)};
    torch::Tensor *wfnt;
    torch::Tensor *wfntm1;
    torch::Tensor *psixntm1{nt & 1 ? &psixn : &psix};
    torch::Tensor *psiyntm1{nt & 1 ? &psiyn : &psiy};
    torch::Tensor *zetaxntm1{nt & 1 ? &zetaxn : &zetax};
    torch::Tensor *zetayntm1{nt & 1 ? &zetayn : &zetay};
    if (nt % 1 == 0) {
      wfnt = &wfp;
      wfntm1 = &wfcn;
    } else if (nt % 2 == 0) {
      wfnt = &wfcn;
      wfntm1 = &wfc;
    } else {
      wfnt = &wfc;
      wfntm1 = &wfp;
    }

    zero_interior(*psixntm1, nx, ny, fd_pad, pml_width);
    zero_interior(*psiyntm1, nx, ny, fd_pad, pml_width);
    zero_interior(*zetaxntm1, nx, ny, fd_pad, pml_width);
    zero_interior(*zetayntm1, nx, ny, fd_pad, pml_width);

    return {grad_v,
            grad_f,
            wfnt->index({all_slice, slicex, slicey}),
            wfntm1->index({all_slice, slicex, slicey}),
            psixntm1->index({all_slice, slicex, slicey}),
            psiyntm1->index({all_slice, slicex, slicey}),
            zetaxntm1->index({all_slice, slicex, slicey}),
            zetayntm1->index({all_slice, slicex, slicey}),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor(),
            torch::Tensor()};
  }
};

std::vector<torch::Tensor> scalar_cpu_autograd(
    torch::Tensor const &v, torch::Tensor const &f, torch::Tensor const &wfc0,
    torch::Tensor const &wfp0, torch::Tensor const &psix0,
    torch::Tensor const &psiy0, torch::Tensor const &zetax0,
    torch::Tensor const &zetay0, torch::Tensor const &ax,
    torch::Tensor const &ay, torch::Tensor const &bx, torch::Tensor const &by,
    torch::Tensor const &sources_i, torch::Tensor const &receivers_i, double dx,
    double dy, double dt, int64_t nt, int64_t n_batch, int64_t step_ratio,
    int64_t accuracy, int64_t pml_width0, int64_t pml_width1,
    int64_t pml_width2, int64_t pml_width3) {
  return ScalarCPUFunction::apply(
      v, f, wfc0, wfp0, psix0, psiy0, zetax0, zetay0, ax, ay, bx, by, sources_i,
      receivers_i, dx, dy, dt, nt, n_batch, step_ratio, accuracy, pml_width0,
      pml_width1, pml_width2, pml_width3);
}

TORCH_LIBRARY_IMPL(deepwave, AutogradCPU, m) {
  m.impl("scalar", scalar_cpu_autograd);
}
