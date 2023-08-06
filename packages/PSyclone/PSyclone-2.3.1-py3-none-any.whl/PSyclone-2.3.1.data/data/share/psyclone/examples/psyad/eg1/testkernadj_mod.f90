module testkern_mod_adj
  implicit none
  public

  public :: testkern_code_adj

  contains
  subroutine testkern_code_adj(ascalar, field1, field2, field3, npts)
    real, intent(in) :: ascalar
    integer, intent(in) :: npts
    real, dimension(npts), intent(inout) :: field2
    real, dimension(npts), intent(inout) :: field1
    real, dimension(npts), intent(inout) :: field3
    real :: tmp
    real :: tmp2
    real :: tmp3
    integer :: i
    integer :: idx

    tmp = ascalar * ascalar
    do idx = UBOUND(field2, 1), LBOUND(field2, 1), -1
      field1(idx) = field1(idx) + field2(idx)
      field3(idx) = field3(idx) - tmp * field2(idx)
      field2(idx) = 0.0
    enddo
    field1(1) = field1(1) + field2(npts)
    do i = npts, 1, -1
      tmp2 = tmp * i
      tmp3 = tmp2 * 3.0
      field1(i) = field1(i) + field2(i) / tmp2
      field2(i) = field2(i) + field1(i)
      field3(i) = field3(i) + field1(i)
      field1(i) = tmp * field1(i)
    enddo

  end subroutine testkern_code_adj

end module testkern_mod_adj
