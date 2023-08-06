program test
  use field_mod
  use grid_mod
  use decomposition_mod, only : decomposition_type
  use parallel_mod, only : parallel_init
  use profile_psy_data_mod, only : profile_psydatainit, profile_psydatashutdown
  use init_field_mod, only : init_field
  use update_field_mod, only : update_field
  use psy_test, only : invoke_0, invoke_1_update_field
  type(r2d_field) :: a_fld
  type(r2d_field) :: b_fld
  type(r2d_field) :: c_fld
  type(r2d_field) :: d_fld
  TYPE(grid_type), TARGET :: grid
  type(decomposition_type) :: decomp

  call profile_psydatainit()
  call parallel_init()
  grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call grid%decompose(3, 3, 1, 1, 1, halo_width=1)
  call grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid,GO_T_POINTS)
  b_fld = r2d_field(grid,GO_T_POINTS)
  c_fld = r2d_field(grid,GO_T_POINTS)
  d_fld = r2d_field(grid,GO_T_POINTS)
  call invoke_0(a_fld, b_fld, c_fld, d_fld)
  call invoke_1_update_field(a_fld, b_fld, c_fld, d_fld)
  PRINT *, a_fld % data(1 : 5, 1 : 5)
  call profile_psydatashutdown()

end program test
