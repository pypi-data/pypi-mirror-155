program test
  use field_mod
  use grid_mod
  use decomposition_mod, only : decomposition_type
  use parallel_mod, only : parallel_init
  use init_field_mod, only : init_field
  use update_field_mod, only : update_field
  use read_only_verify_psy_data_mod, only : read_only_verify_psydatainit, read_only_verify_psydatashutdown, &
&read_only_verify_psydatastart
  use psy_test, only : invoke_0, invoke_1_update_field
  type(r2d_field) :: a_fld
  type(r2d_field) :: b_fld
  type(r2d_field) :: c_fld
  type(r2d_field) :: d_fld
  double precision :: x
  double precision :: y
  double precision :: z
  TYPE(grid_type), TARGET :: grid

  call parallel_init()
  call read_only_verify_psydatainit()
  call read_only_verify_psydatastart()
  grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call grid%decompose(3, 3, 1, 1, 1, halo_width=1)
  call grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid,GO_T_POINTS)
  b_fld = r2d_field(grid,GO_T_POINTS)
  c_fld = r2d_field(grid,GO_T_POINTS)
  d_fld = r2d_field(grid,GO_T_POINTS)
  call invoke_0(a_fld, b_fld, c_fld, d_fld)
  x = 0.0d0
  z = 1.0d0
  call invoke_1_update_field(a_fld, b_fld, c_fld, d_fld, x, y, z)
  call read_only_verify_psydatashutdown()

end program test
