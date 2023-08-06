  MODULE psy_shallow
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
      USE compute_cu_mod, ONLY: compute_cu_code
      USE compute_cv_mod, ONLY: compute_cv_code
      USE compute_z_mod, ONLY: compute_z_code
      USE compute_h_mod, ONLY: compute_h_code
      TYPE(r2d_field), intent(inout) :: cu_fld
      TYPE(r2d_field), intent(inout) :: p_fld
      TYPE(r2d_field), intent(inout) :: u_fld
      TYPE(r2d_field), intent(inout) :: cv_fld
      TYPE(r2d_field), intent(inout) :: v_fld
      TYPE(r2d_field), intent(inout) :: z_fld
      TYPE(r2d_field), intent(inout) :: h_fld
      INTEGER j
      INTEGER i

      !$omp parallel default(shared), private(i,j)
      !$omp single
      !$omp taskloop
      DO j = cu_fld%internal%ystart, cu_fld%internal%ystop, 1
        DO i = cu_fld%internal%xstart, cu_fld%internal%xstop, 1
          CALL compute_cu_code(i, j, cu_fld%data, p_fld%data, u_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = cv_fld%internal%ystart, cv_fld%internal%ystop, 1
        DO i = cv_fld%internal%xstart, cv_fld%internal%xstop, 1
          CALL compute_cv_code(i, j, cv_fld%data, p_fld%data, v_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = z_fld%internal%ystart, z_fld%internal%ystop, 1
        DO i = z_fld%internal%xstart, z_fld%internal%xstop, 1
          CALL compute_z_code(i, j, z_fld%data, p_fld%data, u_fld%data, v_fld%data, p_fld%grid%dx, p_fld%grid%dy)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = h_fld%internal%ystart, h_fld%internal%ystop, 1
        DO i = h_fld%internal%xstart, h_fld%internal%xstop, 1
          CALL compute_h_code(i, j, h_fld%data, p_fld%data, u_fld%data, v_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp end single
      !$omp end parallel

    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1(unew_fld, uold_fld, z_fld, cv_fld, h_fld, tdt, vnew_fld, vold_fld, cu_fld, pnew_fld, pold_fld)
      USE compute_unew_mod, ONLY: compute_unew_code
      USE compute_vnew_mod, ONLY: compute_vnew_code
      USE compute_pnew_mod, ONLY: compute_pnew_code
      TYPE(r2d_field), intent(inout) :: unew_fld
      TYPE(r2d_field), intent(inout) :: uold_fld
      TYPE(r2d_field), intent(inout) :: z_fld
      TYPE(r2d_field), intent(inout) :: cv_fld
      TYPE(r2d_field), intent(inout) :: h_fld
      REAL(KIND=go_wp), intent(inout) :: tdt
      TYPE(r2d_field), intent(inout) :: vnew_fld
      TYPE(r2d_field), intent(inout) :: vold_fld
      TYPE(r2d_field), intent(inout) :: cu_fld
      TYPE(r2d_field), intent(inout) :: pnew_fld
      TYPE(r2d_field), intent(inout) :: pold_fld
      INTEGER j
      INTEGER i

      !$omp parallel default(shared), private(i,j)
      !$omp single
      !$omp taskloop
      DO j = unew_fld%internal%ystart, unew_fld%internal%ystop, 1
        DO i = unew_fld%internal%xstart, unew_fld%internal%xstop, 1
          CALL compute_unew_code(i, j, unew_fld%data, uold_fld%data, z_fld%data, cv_fld%data, h_fld%data, tdt, uold_fld%grid%dy)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = vnew_fld%internal%ystart, vnew_fld%internal%ystop, 1
        DO i = vnew_fld%internal%xstart, vnew_fld%internal%xstop, 1
          CALL compute_vnew_code(i, j, vnew_fld%data, vold_fld%data, z_fld%data, cu_fld%data, h_fld%data, tdt, vold_fld%grid%dy)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = pnew_fld%internal%ystart, pnew_fld%internal%ystop, 1
        DO i = pnew_fld%internal%xstart, pnew_fld%internal%xstop, 1
          CALL compute_pnew_code(i, j, pnew_fld%data, pold_fld%data, cu_fld%data, cv_fld%data, tdt, pold_fld%grid%dx, &
&pold_fld%grid%dy)
        END DO
      END DO
      !$omp end taskloop
      !$omp end single
      !$omp end parallel

    END SUBROUTINE invoke_1
    SUBROUTINE invoke_2(u_fld, unew_fld, uold_fld, v_fld, vnew_fld, vold_fld, p_fld, pnew_fld, pold_fld)
      USE time_smooth_mod, ONLY: time_smooth_code
      TYPE(r2d_field), intent(inout) :: u_fld
      TYPE(r2d_field), intent(inout) :: unew_fld
      TYPE(r2d_field), intent(inout) :: uold_fld
      TYPE(r2d_field), intent(inout) :: v_fld
      TYPE(r2d_field), intent(inout) :: vnew_fld
      TYPE(r2d_field), intent(inout) :: vold_fld
      TYPE(r2d_field), intent(inout) :: p_fld
      TYPE(r2d_field), intent(inout) :: pnew_fld
      TYPE(r2d_field), intent(inout) :: pold_fld
      INTEGER j
      INTEGER i

      !$omp parallel default(shared), private(i,j)
      !$omp single
      !$omp taskloop
      DO j = 1, SIZE(uold_fld%data, 2), 1
        DO i = 1, SIZE(uold_fld%data, 1), 1
          CALL time_smooth_code(i, j, u_fld%data, unew_fld%data, uold_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = 1, SIZE(vold_fld%data, 2), 1
        DO i = 1, SIZE(vold_fld%data, 1), 1
          CALL time_smooth_code(i, j, v_fld%data, vnew_fld%data, vold_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = 1, SIZE(pold_fld%data, 2), 1
        DO i = 1, SIZE(pold_fld%data, 1), 1
          CALL time_smooth_code(i, j, p_fld%data, pnew_fld%data, pold_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp end single
      !$omp end parallel

    END SUBROUTINE invoke_2
    SUBROUTINE invoke_3(u_fld, unew_fld, v_fld, vnew_fld, p_fld, pnew_fld)
      USE infrastructure_mod, ONLY: field_copy_code
      TYPE(r2d_field), intent(inout) :: u_fld
      TYPE(r2d_field), intent(inout) :: unew_fld
      TYPE(r2d_field), intent(inout) :: v_fld
      TYPE(r2d_field), intent(inout) :: vnew_fld
      TYPE(r2d_field), intent(inout) :: p_fld
      TYPE(r2d_field), intent(inout) :: pnew_fld
      INTEGER j
      INTEGER i

      !$omp parallel default(shared), private(i,j)
      !$omp single
      !$omp taskloop
      DO j = 1, SIZE(u_fld%data, 2), 1
        DO i = 1, SIZE(u_fld%data, 1), 1
          CALL field_copy_code(i, j, u_fld%data, unew_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = 1, SIZE(v_fld%data, 2), 1
        DO i = 1, SIZE(v_fld%data, 1), 1
          CALL field_copy_code(i, j, v_fld%data, vnew_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp taskloop
      DO j = 1, SIZE(p_fld%data, 2), 1
        DO i = 1, SIZE(p_fld%data, 1), 1
          CALL field_copy_code(i, j, p_fld%data, pnew_fld%data)
        END DO
      END DO
      !$omp end taskloop
      !$omp end single
      !$omp end parallel

    END SUBROUTINE invoke_3
  END MODULE psy_shallow