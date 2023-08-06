program test
  use field_mod
  use grid_mod
  use decomposition_mod, only : decomposition_type
  use parallel_mod, only : parallel_init
  use init_field_mod, only : init_field
  use update_field_mod, only : update_field
  use nan_test_psy_data_mod, only : nan_test_psydatainit, nan_test_psydatashutdown, nan_test_psydatastart
  use psy_test, only : invoke_0, invoke_1_update_field
  type(r2d_field) :: a_fld
  type(r2d_field) :: b_fld
  TYPE(grid_type), TARGET :: grid

  call parallel_init()
  call nan_test_psydatainit()
  call nan_test_psydatastart()
  grid = grid_type(GO_ARAKAWA_C,(/GO_BC_PERIODIC, GO_BC_PERIODIC, GO_BC_NONE/),GO_OFFSET_SW)
  call grid%decompose(3, 3, 1, 1, 1, halo_width=1)
  call grid_init(grid, 1.0_8, 1.0_8)
  a_fld = r2d_field(grid,GO_T_POINTS)
  b_fld = r2d_field(grid,GO_T_POINTS)
  call invoke_0(a_fld, b_fld)
  call invoke_1_update_field(a_fld, b_fld)
  PRINT *, "a_fld is", a_fld % data
  call nan_test_psydatashutdown()

end program test
