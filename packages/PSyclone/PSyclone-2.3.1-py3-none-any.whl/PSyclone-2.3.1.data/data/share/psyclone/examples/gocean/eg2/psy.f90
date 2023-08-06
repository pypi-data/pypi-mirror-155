  MODULE psy_alg
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0_inc_field(fld1, nx, ny, this_step)
      USE inc_field_0_mod, ONLY: inc_field_0_code
      TYPE(r2d_field), intent(inout) :: fld1
      INTEGER, intent(inout) :: nx
      INTEGER, intent(inout) :: ny
      INTEGER, intent(inout) :: this_step
      INTEGER j
      INTEGER i

      fld1%data_on_device = .true.
      fld1%read_from_device_f => read_from_device
      !$acc enter data copyin(fld1,fld1%data,nx,ny,this_step)
      !$acc parallel default(present)
      !$acc loop independent collapse(2)
      DO j = fld1%internal%ystart, fld1%internal%ystop, 1
        DO i = fld1%internal%xstart, fld1%internal%xstop, 1
          CALL inc_field_0_code(i, j, fld1%data, nx, ny, this_step)
        END DO
      END DO
      !$acc end parallel

    END SUBROUTINE invoke_0_inc_field
    SUBROUTINE read_from_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_ptr
      USE kind_params_mod, ONLY: go_wp
      TYPE(c_ptr), intent(in) :: from
      REAL(KIND=go_wp), DIMENSION(:, :), INTENT(INOUT), TARGET :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking

      !$acc update host(to)

    END SUBROUTINE read_from_device
  END MODULE psy_alg