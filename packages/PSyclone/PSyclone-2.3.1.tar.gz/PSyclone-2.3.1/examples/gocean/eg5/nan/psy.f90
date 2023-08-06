  MODULE psy_test
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(a_fld, b_fld)
      USE nan_test_psy_data_mod, ONLY: nan_test_PSyDataType
      USE init_field_mod, ONLY: init_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      INTEGER j
      INTEGER i
      TYPE(nan_test_PSyDataType), save, target :: nan_test_psy_data

      CALL nan_test_psy_data % PreStart("main", "init", 8, 4)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld%whole%xstart", b_fld % whole % xstart)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld%whole%xstop", b_fld % whole % xstop)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld%whole%ystart", b_fld % whole % ystart)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld%whole%ystop", b_fld % whole % ystop)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld", a_fld)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld", b_fld)
      CALL nan_test_psy_data % PreDeclareVariable("i", i)
      CALL nan_test_psy_data % PreDeclareVariable("j", j)
      CALL nan_test_psy_data % PreEndDeclaration
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL nan_test_psy_data % ProvideVariable("b_fld%whole%xstart", b_fld % whole % xstart)
      CALL nan_test_psy_data % ProvideVariable("b_fld%whole%xstop", b_fld % whole % xstop)
      CALL nan_test_psy_data % ProvideVariable("b_fld%whole%ystart", b_fld % whole % ystart)
      CALL nan_test_psy_data % ProvideVariable("b_fld%whole%ystop", b_fld % whole % ystop)
      CALL nan_test_psy_data % PreEnd
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
      CALL nan_test_psy_data % PostStart
      CALL nan_test_psy_data % ProvideVariable("a_fld", a_fld)
      CALL nan_test_psy_data % ProvideVariable("b_fld", b_fld)
      CALL nan_test_psy_data % ProvideVariable("i", i)
      CALL nan_test_psy_data % ProvideVariable("j", j)
      CALL nan_test_psy_data % PostEnd

    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1_update_field(a_fld, b_fld)
      USE nan_test_psy_data_mod, ONLY: nan_test_PSyDataType
      USE update_field_mod, ONLY: update_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      INTEGER j
      INTEGER i
      TYPE(nan_test_PSyDataType), save, target :: nan_test_psy_data

      CALL nan_test_psy_data % PreStart("main", "update", 6, 3)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld", a_fld)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL nan_test_psy_data % PreDeclareVariable("b_fld", b_fld)
      CALL nan_test_psy_data % PreDeclareVariable("a_fld", a_fld)
      CALL nan_test_psy_data % PreDeclareVariable("i", i)
      CALL nan_test_psy_data % PreDeclareVariable("j", j)
      CALL nan_test_psy_data % PreEndDeclaration
      CALL nan_test_psy_data % ProvideVariable("a_fld", a_fld)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL nan_test_psy_data % ProvideVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL nan_test_psy_data % ProvideVariable("b_fld", b_fld)
      CALL nan_test_psy_data % PreEnd
      DO j = a_fld%whole%ystart, a_fld%whole%ystop, 1
        DO i = a_fld%whole%xstart, a_fld%whole%xstop, 1
          CALL update_field_code(i, j, a_fld%data, b_fld%data)
        END DO
      END DO
      CALL nan_test_psy_data % PostStart
      CALL nan_test_psy_data % ProvideVariable("a_fld", a_fld)
      CALL nan_test_psy_data % ProvideVariable("i", i)
      CALL nan_test_psy_data % ProvideVariable("j", j)
      CALL nan_test_psy_data % PostEnd

    END SUBROUTINE invoke_1_update_field
  END MODULE psy_test