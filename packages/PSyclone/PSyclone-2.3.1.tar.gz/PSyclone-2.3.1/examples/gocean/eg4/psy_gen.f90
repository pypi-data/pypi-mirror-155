  MODULE psy_alg
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0_kern_use_var(fld1)
      USE data_mod, ONLY: gravity
      TYPE(r2d_field), intent(inout) :: fld1
      INTEGER j
      INTEGER i

      fld1%data_on_device = .true.
      fld1%read_from_device_f => read_from_device
      !$acc enter data copyin(fld1,fld1%data,gravity)
      !$acc parallel default(present)
      !$acc loop independent collapse(2)
      DO j = fld1%internal%ystart, fld1%internal%ystop, 1
        DO i = fld1%internal%xstart, fld1%internal%xstop, 1
          CALL kern_use_var_code(i, j, fld1%data, gravity)
        END DO
      END DO
      !$acc end parallel

    END SUBROUTINE invoke_0_kern_use_var
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
    SUBROUTINE kern_use_var_code(i, j, fld, gravity)
      INTEGER, intent(in) :: i
      INTEGER, intent(in) :: j
      REAL(KIND=go_wp), dimension(:,:), intent(inout) :: fld
      REAL(KIND=go_wp), intent(in) :: gravity

      !$acc routine
      fld(i,j) = gravity * fld(i,j)

    END SUBROUTINE kern_use_var_code
  END MODULE psy_alg