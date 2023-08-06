MODULE helmholtz_solver_alg_mod
  CONTAINS
  SUBROUTINE apply_helmholtz_lhs(Hp, p)
    USE helmholtz_solver_alg_mod_psy, ONLY: invoke_0
    USE field_mod, ONLY: field_type
    USE operator_mod, ONLY: operator_type
    USE scaled_matrix_vector_kernel_mod, ONLY: opt_scaled_matrix_vector_kernel_type
    IMPLICIT NONE
    TYPE(field_type), INTENT(INOUT) :: Hp
    TYPE(field_type), INTENT(IN) :: p
    TYPE(field_type) :: grad_p, hb_inv, u_normalisation
    TYPE(operator_type) :: div_star
    CALL invoke_0(grad_p, p, div_star, hb_inv, u_normalisation)
  END SUBROUTINE apply_helmholtz_lhs
END MODULE helmholtz_solver_alg_mod
PROGRAM driver
  USE helmholtz_solver_alg_mod, ONLY: apply_helmholtz_lhs
  USE field_mod, ONLY: field_type
  TYPE(field_type) :: Hp, p
  CALL apply_helmholtz_lhs(Hp, p)
END PROGRAM driver