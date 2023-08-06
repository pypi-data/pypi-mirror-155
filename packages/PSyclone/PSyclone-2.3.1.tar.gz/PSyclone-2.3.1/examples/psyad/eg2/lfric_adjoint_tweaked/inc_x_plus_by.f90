! Below is a manual implementation of the inc_x_plus_by builtin for
! testing purposes. If this is run through psyad 'psyad
! incx_plus_by.f90 -a field1 field2' (assuming that the fields are
! active and the scalar is not!) we find that the adjoint is the same
! as inc_x_plus_by, except that the fields are swapped. This gives a
! simple short term solution to writing the adjoint:
!
! call invoke(inc_x_plus_by(x,b,y)
!
! can simply be changed to
!
! call invoke(inc_x_plus_by(y,b,x)
!
subroutine inc_x_plus_by(field1, rscalar, field2)
  ! field1 and field2 are active
  real, intent(inout) :: field1(:)
  real, intent(in) :: field2(:), rscalar
  field1(:) = field1(:) + rscalar*field2(:)
end subroutine inc_x_plus_by
