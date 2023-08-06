program simple
  use kind_params_mod, only : go_wp
  use grid_mod
  use field_mod
  use gocean_mod, only : gocean_initialise
  use compute_cu_mod, only : compute_cu
  use compute_cv_mod, only : compute_cv
  use compute_z_mod, only : compute_z
  use compute_h_mod, only : compute_h
  use psy_simple, only : invoke_0
  TYPE(grid_type), TARGET :: model_grid
  integer, allocatable, dimension(:,:) :: tmask
  type(r2d_field) :: p_fld
  type(r2d_field) :: u_fld
  type(r2d_field) :: v_fld
  type(r2d_field) :: cu_fld
  type(r2d_field) :: cv_fld
  type(r2d_field) :: z_fld
  type(r2d_field) :: h_fld
  integer :: ncycle
  integer :: ierr
  integer :: jpiglo
  integer :: jpjglo

  jpiglo = 50
  jpjglo = 50
  call gocean_initialise()
  model_grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call model_grid%decompose(jpiglo, jpjglo)
  ALLOCATE(tmask(model_grid % subdomain % global % nx, model_grid % subdomain % global % ny), STAT = ierr)
  if (ierr /= 0) then
    STOP 'Failed to allocate T mask'
  end if
  tmask(:,:) = 0
  call grid_init(model_grid, 1000.0_go_wp, 1000.0_go_wp, tmask)
  p_fld = r2d_field(model_grid,GO_T_POINTS)
  u_fld = r2d_field(model_grid,GO_U_POINTS)
  v_fld = r2d_field(model_grid,GO_V_POINTS)
  cu_fld = r2d_field(model_grid,GO_U_POINTS)
  cv_fld = r2d_field(model_grid,GO_V_POINTS)
  z_fld = r2d_field(model_grid,GO_F_POINTS)
  h_fld = r2d_field(model_grid,GO_T_POINTS)
  WRITE(*, *) "Simulation start"
  do ncycle = 1, 100, 1
    call invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
  enddo
  WRITE(*, *) "Simulation end"

end program simple
