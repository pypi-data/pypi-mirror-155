__attribute__((reqd_work_group_size(64, 1, 1)))
__kernel void kern_use_var_code(
  __global double * restrict fld,
  double gravity,
  int xstart,
  int xstop,
  int ystart,
  int ystop
  ){
  int fldLEN1 = get_global_size(0);
  int fldLEN2 = get_global_size(1);
  int i = get_global_id(0);
  int j = get_global_id(1);
  if ((((i < xstart) || (i > xstop)) || ((j < ystart) || (j > ystop)))) {
    return;
  }
  fld[i + j * fldLEN1] = (gravity * fld[i + j * fldLEN1]);
}

