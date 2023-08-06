__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_cu_code(
  __global double * restrict cu,
  __global double * restrict p,
  __global double * restrict u,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int cuLEN1 = get_global_size(0);
  int cuLEN2 = get_global_size(1);
  int pLEN1 = get_global_size(0);
  int pLEN2 = get_global_size(1);
  int uLEN1 = get_global_size(0);
  int uLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  cu[i + j * cuLEN1] = ((0.5e0 * (p[i + j * pLEN1] + p[(i - 1) + j * pLEN1])) * u[i + j * uLEN1]);
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_cv_code(
  __global double * restrict cv,
  __global double * restrict p,
  __global double * restrict v,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int cvLEN1 = get_global_size(0);
  int cvLEN2 = get_global_size(1);
  int pLEN1 = get_global_size(0);
  int pLEN2 = get_global_size(1);
  int vLEN1 = get_global_size(0);
  int vLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  cv[i + j * cvLEN1] = ((0.5e0 * (p[i + j * pLEN1] + p[i + (j - 1) * pLEN1])) * v[i + j * vLEN1]);
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_z_code(
  __global double * restrict z,
  __global double * restrict p,
  __global double * restrict u,
  __global double * restrict v,
  double dx,
  double dy,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int zLEN1 = get_global_size(0);
  int zLEN2 = get_global_size(1);
  int pLEN1 = get_global_size(0);
  int pLEN2 = get_global_size(1);
  int uLEN1 = get_global_size(0);
  int uLEN2 = get_global_size(1);
  int vLEN1 = get_global_size(0);
  int vLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  z[i + j * zLEN1] = ((((4.0e0 / dx) * (v[i + j * vLEN1] - v[(i - 1) + j * vLEN1])) - ((4.0e0 / dy) * (u[i + j * uLEN1] - u[i + (j - 1) * uLEN1]))) / (((p[(i - 1) + (j - 1) * pLEN1] + p[i + (j - 1) * pLEN1]) + p[i + j * pLEN1]) + p[(i - 1) + j * pLEN1]));
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_h_code(
  __global double * restrict h,
  __global double * restrict p,
  __global double * restrict u,
  __global double * restrict v,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int hLEN1 = get_global_size(0);
  int hLEN2 = get_global_size(1);
  int pLEN1 = get_global_size(0);
  int pLEN2 = get_global_size(1);
  int uLEN1 = get_global_size(0);
  int uLEN2 = get_global_size(1);
  int vLEN1 = get_global_size(0);
  int vLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  h[i + j * hLEN1] = (p[i + j * pLEN1] + (0.25e0 * ((((u[(i + 1) + j * uLEN1] * u[(i + 1) + j * uLEN1]) + (u[i + j * uLEN1] * u[i + j * uLEN1])) + (v[i + (j + 1) * vLEN1] * v[i + (j + 1) * vLEN1])) + (v[i + j * vLEN1] * v[i + j * vLEN1]))));
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_unew_code(
  __global double * restrict unew,
  __global double * restrict uold,
  __global double * restrict z,
  __global double * restrict cv,
  __global double * restrict h,
  double tdt,
  double dx,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  double tdts8;
  double tdtsdx;
  int unewLEN1 = get_global_size(0);
  int unewLEN2 = get_global_size(1);
  int uoldLEN1 = get_global_size(0);
  int uoldLEN2 = get_global_size(1);
  int zLEN1 = get_global_size(0);
  int zLEN2 = get_global_size(1);
  int cvLEN1 = get_global_size(0);
  int cvLEN2 = get_global_size(1);
  int hLEN1 = get_global_size(0);
  int hLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  tdts8 = (tdt / 8.0e0);
  tdtsdx = (tdt / dx);
  unew[i + j * unewLEN1] = ((uold[i + j * uoldLEN1] + ((tdts8 * (z[i + (j + 1) * zLEN1] + z[i + j * zLEN1])) * (((cv[i + (j + 1) * cvLEN1] + cv[(i - 1) + (j + 1) * cvLEN1]) + cv[(i - 1) + j * cvLEN1]) + cv[i + j * cvLEN1]))) - (tdtsdx * (h[i + j * hLEN1] - h[(i - 1) + j * hLEN1])));
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_vnew_code(
  __global double * restrict vnew,
  __global double * restrict vold,
  __global double * restrict z,
  __global double * restrict cu,
  __global double * restrict h,
  double tdt,
  double dy,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  double tdts8;
  double tdtsdy;
  int vnewLEN1 = get_global_size(0);
  int vnewLEN2 = get_global_size(1);
  int voldLEN1 = get_global_size(0);
  int voldLEN2 = get_global_size(1);
  int zLEN1 = get_global_size(0);
  int zLEN2 = get_global_size(1);
  int cuLEN1 = get_global_size(0);
  int cuLEN2 = get_global_size(1);
  int hLEN1 = get_global_size(0);
  int hLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  tdts8 = (tdt / 8.0e0);
  tdtsdy = (tdt / dy);
  vnew[i + j * vnewLEN1] = ((vold[i + j * voldLEN1] - ((tdts8 * (z[(i + 1) + j * zLEN1] + z[i + j * zLEN1])) * (((cu[(i + 1) + j * cuLEN1] + cu[i + j * cuLEN1]) + cu[i + (j - 1) * cuLEN1]) + cu[(i + 1) + (j - 1) * cuLEN1]))) - (tdtsdy * (h[i + j * hLEN1] - h[i + (j - 1) * hLEN1])));
}

__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void compute_pnew_code(
  __global double * restrict pnew,
  __global double * restrict pold,
  __global double * restrict cu,
  __global double * restrict cv,
  double tdt,
  double dx,
  double dy,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  double tdtsdx;
  double tdtsdy;
  int pnewLEN1 = get_global_size(0);
  int pnewLEN2 = get_global_size(1);
  int poldLEN1 = get_global_size(0);
  int poldLEN2 = get_global_size(1);
  int cuLEN1 = get_global_size(0);
  int cuLEN2 = get_global_size(1);
  int cvLEN1 = get_global_size(0);
  int cvLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  tdtsdx = (tdt / dx);
  tdtsdy = (tdt / dy);
  pnew[i + j * pnewLEN1] = ((pold[i + j * poldLEN1] - (tdtsdx * (cu[(i + 1) + j * cuLEN1] - cu[i + j * cuLEN1]))) - (tdtsdy * (cv[i + (j + 1) * cvLEN1] - cv[i + j * cvLEN1])));
}

