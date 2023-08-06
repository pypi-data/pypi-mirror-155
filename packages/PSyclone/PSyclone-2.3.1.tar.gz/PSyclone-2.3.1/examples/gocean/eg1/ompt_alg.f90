program shallow
  use kind_params_mod
  use shallow_io_mod
  use timing_mod
  use gocean_mod, only : model_write_log
  use model_mod
  use grid_mod
  use field_mod
  use initial_conditions_mod
  use time_smooth_mod, only : time_smooth
  use apply_bcs_mod, only : invoke_apply_bcs
  use compute_cu_mod, only : compute_cu
  use compute_cv_mod, only : compute_cv
  use compute_z_mod, only : compute_z
  use compute_h_mod, only : compute_h
  use compute_unew_mod, only : compute_unew
  use compute_vnew_mod, only : compute_vnew
  use compute_pnew_mod, only : compute_pnew
  use infrastructure_mod, only : copy
  use psy_shallow, only : invoke_0, invoke_1, invoke_2, invoke_3
  TYPE(grid_type), TARGET :: model_grid
  type(r2d_field) :: p_fld
  type(r2d_field) :: pold_fld
  type(r2d_field) :: pnew_fld
  type(r2d_field) :: u_fld
  type(r2d_field) :: uold_fld
  type(r2d_field) :: unew_fld
  type(r2d_field) :: v_fld
  type(r2d_field) :: vold_fld
  type(r2d_field) :: vnew_fld
  type(r2d_field) :: cu_fld
  type(r2d_field) :: cv_fld
  type(r2d_field) :: z_fld
  type(r2d_field) :: h_fld
  type(r2d_field) :: psi_fld
  integer :: ncycle
  integer :: itmax
  integer :: idxt0
  integer :: idxt1
  real(kind=go_wp) :: dt
  real(kind=go_wp) :: tdt

  model_grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call model_init(model_grid)
  p_fld = r2d_field(model_grid,GO_T_POINTS)
  pold_fld = r2d_field(model_grid,GO_T_POINTS)
  pnew_fld = r2d_field(model_grid,GO_T_POINTS)
  u_fld = r2d_field(model_grid,GO_U_POINTS)
  uold_fld = r2d_field(model_grid,GO_U_POINTS)
  unew_fld = r2d_field(model_grid,GO_U_POINTS)
  v_fld = r2d_field(model_grid,GO_V_POINTS)
  vold_fld = r2d_field(model_grid,GO_V_POINTS)
  vnew_fld = r2d_field(model_grid,GO_V_POINTS)
  cu_fld = r2d_field(model_grid,GO_U_POINTS)
  cv_fld = r2d_field(model_grid,GO_V_POINTS)
  z_fld = r2d_field(model_grid,GO_F_POINTS)
  h_fld = r2d_field(model_grid,GO_T_POINTS)
  psi_fld = r2d_field(model_grid,GO_F_POINTS)
  tdt = dt
  call init_initial_condition_params(p_fld)
  call invoke_init_stream_fn_kernel(psi_fld)
  call init_pressure(p_fld)
  call init_velocity_u(u_fld, psi_fld)
  call init_velocity_v(v_fld, psi_fld)
  call invoke_apply_bcs(u_fld)
  call invoke_apply_bcs(v_fld)
  call model_write_log("('psi initial CHECKSUM = ',E24.16)", field_checksum(psi_fld))
  call model_write_log("('P initial CHECKSUM = ',E24.16)", field_checksum(p_fld))
  call model_write_log("('U initial CHECKSUM = ',E24.16)", field_checksum(u_fld))
  call model_write_log("('V initial CHECKSUM = ',E24.16)", field_checksum(v_fld))
  call copy_field(u_fld, uold_fld)
  call copy_field(v_fld, vold_fld)
  call copy_field(p_fld, pold_fld)
  call ascii_write(0, 'psifld.dat', psi_fld%data, psi_fld%internal%nx, psi_fld%internal%ny, psi_fld%internal%xstart, &
&psi_fld%internal%ystart)
  call model_write(0, p_fld, u_fld, v_fld)
  call timer_start('Time-stepping', idxt0)
  do ncycle = 1, itmax, 1
    call timer_start('Compute c{u,v},z,h', idxt1)
    call invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
    call timer_stop(idxt1)
    call timer_start('PBCs-1', idxt1)
    call invoke_apply_bcs(cu_fld)
    call invoke_apply_bcs(cv_fld)
    call invoke_apply_bcs(h_fld)
    call invoke_apply_bcs(z_fld)
    call timer_stop(idxt1)
    call timer_start('Compute new fields', idxt1)
    call invoke_1(unew_fld, uold_fld, z_fld, cv_fld, h_fld, tdt, vnew_fld, vold_fld, cu_fld, pnew_fld, pold_fld)
    call timer_stop(idxt1)
    call timer_start('PBCs-2', idxt1)
    call invoke_apply_bcs(unew_fld)
    call invoke_apply_bcs(vnew_fld)
    call invoke_apply_bcs(pnew_fld)
    call timer_stop(idxt1)
    call model_write(ncycle, p_fld, u_fld, v_fld)
    if (ncycle > 1) then
      call timer_start('Time smoothing', idxt1)
      call invoke_2(u_fld, unew_fld, uold_fld, v_fld, vnew_fld, vold_fld, p_fld, pnew_fld, pold_fld)
      call timer_stop(idxt1)
    else
      tdt = tdt + dt
    end if
    call timer_start('Field copy', idxt1)
    call invoke_3(u_fld, unew_fld, v_fld, vnew_fld, p_fld, pnew_fld)
    call timer_stop(idxt1)
  enddo
  call timer_stop(idxt0)
  call model_write_log("('P CHECKSUM after ',I6,' steps = ',E24.16)", itmax, field_checksum(pnew_fld))
  call model_write_log("('U CHECKSUM after ',I6,' steps = ',E24.16)", itmax, field_checksum(unew_fld))
  call model_write_log("('V CHECKSUM after ',I6,' steps = ',E24.16)", itmax, field_checksum(vnew_fld))
  call model_finalise()

end program shallow
