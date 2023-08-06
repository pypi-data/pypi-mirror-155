program adj_test
  use testkern_mod, only : testkern_code
  use testkern_mod_adj, only : testkern_code_adj
  integer, parameter :: array_extent = 20
  integer, parameter :: npts = array_extent
  real, parameter :: overall_tolerance = 1500.0
  real :: inner1
  real :: inner2
  real :: ascalar
  real :: ascalar_input
  real, dimension(npts) :: field1
  real, dimension(npts) :: field1_input
  real, dimension(npts) :: field2
  real, dimension(npts) :: field2_input
  real, dimension(npts) :: field3
  real, dimension(npts) :: field3_input
  real :: MachineTol
  real :: relative_diff

  ! Initialise the kernel arguments and keep copies of them
  CALL random_number(ascalar)
  ascalar_input = ascalar
  CALL random_number(field1)
  field1_input = field1
  CALL random_number(field2)
  field2_input = field2
  CALL random_number(field3)
  field3_input = field3
  ! Call the tangent-linear kernel
  call testkern_code(ascalar, field1, field2, field3, npts)
  ! Compute the inner product of the results of the tangent-linear kernel
  inner1 = 0.0
  inner1 = inner1 + ascalar * ascalar
  inner1 = inner1 + DOT_PRODUCT(field1, field1)
  inner1 = inner1 + DOT_PRODUCT(field2, field2)
  inner1 = inner1 + DOT_PRODUCT(field3, field3)
  ! Call the adjoint of the kernel
  call testkern_code_adj(ascalar, field1, field2, field3, npts)
  ! Compute inner product of results of adjoint kernel with the original inputs to the tangent-linear kernel
  inner2 = 0.0
  inner2 = inner2 + ascalar * ascalar_input
  inner2 = inner2 + DOT_PRODUCT(field1, field1_input)
  inner2 = inner2 + DOT_PRODUCT(field2, field2_input)
  inner2 = inner2 + DOT_PRODUCT(field3, field3_input)
  ! Test the inner-product values for equality, allowing for the precision of the active variables
  MachineTol = SPACING(MAX(ABS(inner1), ABS(inner2)))
  relative_diff = ABS(inner1 - inner2) / MachineTol
  if (relative_diff < overall_tolerance) then
    WRITE(*, *) 'Test of adjoint of ''testkern_code'' PASSED: ', inner1, inner2, relative_diff
  else
    WRITE(*, *) 'Test of adjoint of ''testkern_code'' FAILED: ', inner1, inner2, relative_diff
  end if

end program adj_test
