module testkern_w0_kernel_0_mod
  use argument_mod
  use kernel_mod
  use fs_continuity_mod, only : w0
  use constants_mod
  implicit none
  type, public, extends(kernel_type) :: testkern_w0_kernel_type
  PRIVATE
  TYPE(arg_type), DIMENSION(2) :: meta_args = (/arg_type(gh_field, gh_real, gh_inc, w0), arg_type(gh_field, gh_real, gh_read, w0)/)
  INTEGER :: operates_on = cell_column
  CONTAINS
  PROCEDURE, NOPASS :: code => testkern_w0_0_code
END TYPE testkern_w0_kernel_type
  private

  public :: testkern_w0_0_code

  contains
  subroutine testkern_w0_0_code(nlayers, fld1, fld2, ndf_w0, undf_w0, map_w0)
    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_w0
    integer(kind=i_def), intent(in) :: undf_w0
    real(kind=r_def), dimension(undf_w0), intent(inout) :: fld1
    real(kind=r_def), dimension(undf_w0), intent(in) :: fld2
    integer(kind=i_def), dimension(ndf_w0), intent(in) :: map_w0
    integer(kind=i_def) :: i
    integer(kind=i_def) :: k

    !$acc routine
    do k = 0, nlayers - 1, 1
      do i = 1, ndf_w0, 1
        fld1(map_w0(i) + k) = fld1(map_w0(i) + k) + fld2(map_w0(i) + k)
      enddo
    enddo

  end subroutine testkern_w0_0_code

end module testkern_w0_kernel_0_mod
