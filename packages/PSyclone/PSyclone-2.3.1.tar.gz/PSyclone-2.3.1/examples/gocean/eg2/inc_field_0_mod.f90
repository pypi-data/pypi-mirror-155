module inc_field_0_mod
  use kind_params_mod
  use kernel_mod
  use argument_mod
  use grid_mod, only : go_offset_sw
  implicit none
  type, extends(kernel_type), public :: inc_field
  TYPE(go_arg), DIMENSION(4) :: meta_args = (/go_arg(go_write, go_ct, go_pointwise), go_arg(go_read, go_i_scalar, go_pointwise), &
&go_arg(go_read, go_i_scalar, go_pointwise), go_arg(go_read, go_i_scalar, go_pointwise)/)
  INTEGER :: iterates_over = go_internal_pts
  INTEGER :: index_offset = go_offset_sw
  CONTAINS
  PROCEDURE, NOPASS :: code => inc_field_0_code
END TYPE inc_field
  public

  public :: inc_field_0_code

  contains
  subroutine inc_field_0_code(ji, jj, fld1, nx, ny, istp)
    integer, intent(in) :: ji
    integer, intent(in) :: jj
    integer, intent(in) :: nx
    integer, intent(in) :: ny
    real(kind=go_wp), dimension(nx,ny), intent(inout) :: fld1
    integer, intent(in) :: istp

    !$acc routine
    fld1(ji,jj) = fld1(ji,jj) + REAL(istp, go_wp)

  end subroutine inc_field_0_code

end module inc_field_0_mod
