module dg_matrix_vector_kernel_1_mod
  use argument_mod, only : any_discontinuous_space_1, any_space_1, arg_type, cell_column, gh_field, gh_operator, gh_read, &
&gh_readwrite, gh_real, gh_write
  use constants_mod, only : i_def, r_def
  use kernel_mod, only : kernel_type
  implicit none
  type, public, extends(kernel_type) :: dg_matrix_vector_kernel_type
  PRIVATE
  TYPE(arg_type) :: meta_args(3) = (/arg_type(gh_field, gh_real, gh_readwrite, any_discontinuous_space_1), arg_type(gh_field, &
&gh_real, gh_read, any_space_1), arg_type(gh_operator, gh_real, gh_read, any_discontinuous_space_1, any_space_1)/)
  INTEGER :: operates_on = cell_column
  CONTAINS
  PROCEDURE, NOPASS :: dg_matrix_vector_kernel_1_code
END TYPE dg_matrix_vector_kernel_type
  private

  public :: dg_matrix_vector_kernel_1_code

  contains
  subroutine dg_matrix_vector_kernel_1_code(cell, nlayers_dummy, lhs, x, ncell_3d, matrix, ndf1, undf1, map1, ndf2, undf2, map2)
    integer, parameter :: nlayers = 20
    integer(kind=i_def), intent(in) :: cell
    integer(kind=i_def), intent(in) :: ncell_3d
    integer(kind=i_def), intent(in) :: undf1
    integer(kind=i_def), intent(in) :: ndf1
    integer(kind=i_def), intent(in) :: undf2
    integer(kind=i_def), intent(in) :: ndf2
    integer(kind=i_def), dimension(ndf1), intent(in) :: map1
    integer(kind=i_def), dimension(ndf2), intent(in) :: map2
    real(kind=r_def), dimension(undf2), intent(in) :: x
    real(kind=r_def), dimension(undf1), intent(inout) :: lhs
    real(kind=r_def), dimension(ndf1,ndf2,ncell_3d), intent(in) :: matrix
    integer(kind=i_def), intent(in) :: nlayers_dummy
    integer(kind=i_def) :: df
    integer(kind=i_def) :: k
    integer(kind=i_def) :: ik
    real(kind=r_def), dimension(ndf2) :: x_e
    real(kind=r_def), dimension(ndf1) :: lhs_e

    do k = 0, nlayers - 1, 1
      do df = 1, ndf2, 1
        x_e(df) = x(map2(df) + k)
      enddo
      ik = (cell - 1) * nlayers + k + 1
      lhs_e = MATMUL(matrix(:,:,ik), x_e)
      do df = 1, ndf1, 1
        lhs(map1(df) + k) = lhs_e(df)
      enddo
    enddo

  end subroutine dg_matrix_vector_kernel_1_code

end module dg_matrix_vector_kernel_1_mod
