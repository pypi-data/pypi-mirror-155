  MODULE psy_test
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(a_fld, b_fld, c_fld, d_fld)
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE init_field_mod, ONLY: init_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      TYPE(r2d_field), intent(inout) :: c_fld
      TYPE(r2d_field), intent(inout) :: d_fld
      INTEGER j
      INTEGER i
      TYPE(profile_PSyDataType), save, target :: profile_psy_data

      CALL profile_psy_data % PreStart("invoke_0", "r0", 0, 0)
      DO j = a_fld%whole%ystart, a_fld%whole%ystop, 1
        DO i = a_fld%whole%xstart, a_fld%whole%xstop, 1
          CALL init_field_code(i, j, a_fld%data, 1.0)
        END DO
      END DO
      DO j = b_fld%whole%ystart, b_fld%whole%ystop, 1
        DO i = b_fld%whole%xstart, b_fld%whole%xstop, 1
          CALL init_field_code(i, j, b_fld%data, 2.0)
        END DO
      END DO
      DO j = c_fld%whole%ystart, c_fld%whole%ystop, 1
        DO i = c_fld%whole%xstart, c_fld%whole%xstop, 1
          CALL init_field_code(i, j, c_fld%data, 3.0)
        END DO
      END DO
      DO j = d_fld%whole%ystart, d_fld%whole%ystop, 1
        DO i = d_fld%whole%xstart, d_fld%whole%xstop, 1
          CALL init_field_code(i, j, d_fld%data, 4.0)
        END DO
      END DO
      CALL profile_psy_data % PostEnd

    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1_update_field(a_fld, b_fld, c_fld, d_fld)
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      USE update_field_mod, ONLY: update_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      TYPE(r2d_field), intent(inout) :: c_fld
      TYPE(r2d_field), intent(inout) :: d_fld
      INTEGER j
      INTEGER i
      TYPE(profile_PSyDataType), save, target :: profile_psy_data

      CALL profile_psy_data % PreStart("invoke_1_update_field", "r0", 0, 0)
      DO j = a_fld%whole%ystart, a_fld%whole%ystop, 1
        DO i = a_fld%whole%xstart, a_fld%whole%xstop, 1
          CALL update_field_code(i, j, a_fld%data, b_fld%data, c_fld%data, d_fld%data)
        END DO
      END DO
      CALL profile_psy_data % PostEnd

    END SUBROUTINE invoke_1_update_field
  END MODULE psy_test