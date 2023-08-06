  MODULE psy_test
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(a_fld, b_fld, c_fld, d_fld)
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      USE init_field_mod, ONLY: init_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      TYPE(r2d_field), intent(inout) :: c_fld
      TYPE(r2d_field), intent(inout) :: d_fld
      INTEGER j
      INTEGER i
      TYPE(extract_PSyDataType), save, target :: extract_psy_data

      CALL extract_psy_data % PreStart("main", "init", 16, 6)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL extract_psy_data % PreDeclareVariable("b_fld%whole%xstart", b_fld % whole % xstart)
      CALL extract_psy_data % PreDeclareVariable("b_fld%whole%xstop", b_fld % whole % xstop)
      CALL extract_psy_data % PreDeclareVariable("b_fld%whole%ystart", b_fld % whole % ystart)
      CALL extract_psy_data % PreDeclareVariable("b_fld%whole%ystop", b_fld % whole % ystop)
      CALL extract_psy_data % PreDeclareVariable("c_fld%whole%xstart", c_fld % whole % xstart)
      CALL extract_psy_data % PreDeclareVariable("c_fld%whole%xstop", c_fld % whole % xstop)
      CALL extract_psy_data % PreDeclareVariable("c_fld%whole%ystart", c_fld % whole % ystart)
      CALL extract_psy_data % PreDeclareVariable("c_fld%whole%ystop", c_fld % whole % ystop)
      CALL extract_psy_data % PreDeclareVariable("d_fld%whole%xstart", d_fld % whole % xstart)
      CALL extract_psy_data % PreDeclareVariable("d_fld%whole%xstop", d_fld % whole % xstop)
      CALL extract_psy_data % PreDeclareVariable("d_fld%whole%ystart", d_fld % whole % ystart)
      CALL extract_psy_data % PreDeclareVariable("d_fld%whole%ystop", d_fld % whole % ystop)
      CALL extract_psy_data % PreDeclareVariable("a_fld_post", a_fld)
      CALL extract_psy_data % PreDeclareVariable("b_fld_post", b_fld)
      CALL extract_psy_data % PreDeclareVariable("c_fld_post", c_fld)
      CALL extract_psy_data % PreDeclareVariable("d_fld_post", d_fld)
      CALL extract_psy_data % PreDeclareVariable("i_post", i)
      CALL extract_psy_data % PreDeclareVariable("j_post", j)
      CALL extract_psy_data % PreEndDeclaration
      CALL extract_psy_data % ProvideVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL extract_psy_data % ProvideVariable("b_fld%whole%xstart", b_fld % whole % xstart)
      CALL extract_psy_data % ProvideVariable("b_fld%whole%xstop", b_fld % whole % xstop)
      CALL extract_psy_data % ProvideVariable("b_fld%whole%ystart", b_fld % whole % ystart)
      CALL extract_psy_data % ProvideVariable("b_fld%whole%ystop", b_fld % whole % ystop)
      CALL extract_psy_data % ProvideVariable("c_fld%whole%xstart", c_fld % whole % xstart)
      CALL extract_psy_data % ProvideVariable("c_fld%whole%xstop", c_fld % whole % xstop)
      CALL extract_psy_data % ProvideVariable("c_fld%whole%ystart", c_fld % whole % ystart)
      CALL extract_psy_data % ProvideVariable("c_fld%whole%ystop", c_fld % whole % ystop)
      CALL extract_psy_data % ProvideVariable("d_fld%whole%xstart", d_fld % whole % xstart)
      CALL extract_psy_data % ProvideVariable("d_fld%whole%xstop", d_fld % whole % xstop)
      CALL extract_psy_data % ProvideVariable("d_fld%whole%ystart", d_fld % whole % ystart)
      CALL extract_psy_data % ProvideVariable("d_fld%whole%ystop", d_fld % whole % ystop)
      CALL extract_psy_data % PreEnd
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
      CALL extract_psy_data % PostStart
      CALL extract_psy_data % ProvideVariable("a_fld_post", a_fld)
      CALL extract_psy_data % ProvideVariable("b_fld_post", b_fld)
      CALL extract_psy_data % ProvideVariable("c_fld_post", c_fld)
      CALL extract_psy_data % ProvideVariable("d_fld_post", d_fld)
      CALL extract_psy_data % ProvideVariable("i_post", i)
      CALL extract_psy_data % ProvideVariable("j_post", j)
      CALL extract_psy_data % PostEnd

    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1_update_field(a_fld, b_fld, c_fld, d_fld, x, y, z)
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      USE update_field_mod, ONLY: update_field_code
      TYPE(r2d_field), intent(inout) :: a_fld
      TYPE(r2d_field), intent(inout) :: b_fld
      TYPE(r2d_field), intent(inout) :: c_fld
      TYPE(r2d_field), intent(inout) :: d_fld
      REAL(KIND=go_wp), intent(inout) :: x
      REAL(KIND=go_wp), intent(inout) :: y
      REAL(KIND=go_wp), intent(inout) :: z
      INTEGER j
      INTEGER i
      TYPE(extract_PSyDataType), save, target :: extract_psy_data

      CALL extract_psy_data % PreStart("main", "update", 11, 5)
      CALL extract_psy_data % PreDeclareVariable("a_fld", a_fld)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL extract_psy_data % PreDeclareVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL extract_psy_data % PreDeclareVariable("b_fld", b_fld)
      CALL extract_psy_data % PreDeclareVariable("b_fld%grid%dx", b_fld % grid % dx)
      CALL extract_psy_data % PreDeclareVariable("c_fld", c_fld)
      CALL extract_psy_data % PreDeclareVariable("d_fld", d_fld)
      CALL extract_psy_data % PreDeclareVariable("x", x)
      CALL extract_psy_data % PreDeclareVariable("z", z)
      CALL extract_psy_data % PreDeclareVariable("a_fld_post", a_fld)
      CALL extract_psy_data % PreDeclareVariable("i_post", i)
      CALL extract_psy_data % PreDeclareVariable("j_post", j)
      CALL extract_psy_data % PreDeclareVariable("x_post", x)
      CALL extract_psy_data % PreDeclareVariable("y_post", y)
      CALL extract_psy_data % PreEndDeclaration
      CALL extract_psy_data % ProvideVariable("a_fld", a_fld)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%xstart", a_fld % whole % xstart)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%xstop", a_fld % whole % xstop)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%ystart", a_fld % whole % ystart)
      CALL extract_psy_data % ProvideVariable("a_fld%whole%ystop", a_fld % whole % ystop)
      CALL extract_psy_data % ProvideVariable("b_fld", b_fld)
      CALL extract_psy_data % ProvideVariable("b_fld%grid%dx", b_fld % grid % dx)
      CALL extract_psy_data % ProvideVariable("c_fld", c_fld)
      CALL extract_psy_data % ProvideVariable("d_fld", d_fld)
      CALL extract_psy_data % ProvideVariable("x", x)
      CALL extract_psy_data % ProvideVariable("z", z)
      CALL extract_psy_data % PreEnd
      DO j = a_fld%whole%ystart, a_fld%whole%ystop, 1
        DO i = a_fld%whole%xstart, a_fld%whole%xstop, 1
          CALL update_field_code(i, j, a_fld%data, b_fld%data, c_fld%data, d_fld%data, x, y, z, b_fld%grid%dx)
        END DO
      END DO
      CALL extract_psy_data % PostStart
      CALL extract_psy_data % ProvideVariable("a_fld_post", a_fld)
      CALL extract_psy_data % ProvideVariable("i_post", i)
      CALL extract_psy_data % ProvideVariable("j_post", j)
      CALL extract_psy_data % ProvideVariable("x_post", x)
      CALL extract_psy_data % ProvideVariable("y_post", y)
      CALL extract_psy_data % PostEnd

    END SUBROUTINE invoke_1_update_field
  END MODULE psy_test