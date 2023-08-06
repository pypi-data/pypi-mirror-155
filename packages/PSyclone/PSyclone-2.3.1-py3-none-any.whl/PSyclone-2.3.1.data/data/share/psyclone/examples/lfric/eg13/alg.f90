MODULE gw_mixed_schur_preconditioner_alg_mod
  USE field_mod, ONLY: field_type
  USE field_vector_mod, ONLY: field_vector_type
  USE constants_mod, ONLY: r_def
  USE runtime_constants_mod, ONLY: get_mass_matrix, get_div, w0_id, w3_id, w3inv_id, wt_id
  USE timestepping_config_mod, ONLY: dt
  USE gravity_wave_constants_config_mod, ONLY: cs_square, b_space, gravity_wave_constants_b_space_w0, &
&gravity_wave_constants_b_space_w3, gravity_wave_constants_b_space_wtheta
  USE operator_mod, ONLY: operator_type
  USE preconditioner_mod, ONLY: abstract_preconditioner_type
  USE iterative_solver_mod, ONLY: abstract_iterative_solver_type
  USE field_indices_mod, ONLY: igw_u, igw_p, igw_b
  USE log_mod, ONLY: log_event, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
  IMPLICIT NONE
  PRIVATE
  TYPE, PUBLIC, EXTENDS(abstract_preconditioner_type) :: gw_mixed_schur_preconditioner_type
    PRIVATE
    REAL(KIND = r_def) :: alpha
    TYPE(operator_type) :: Q
    TYPE(field_type) :: p_inc, b_inc, u_inc
    TYPE(field_type) :: rhs_p_tmp
    TYPE(field_type) :: rhs_u
    TYPE(field_type) :: rhs_p
    TYPE(field_vector_type) :: pressure_b
    TYPE(field_vector_type) :: pressure_x
    TYPE(field_type) :: hb_ru
    TYPE(field_type) :: mb_rb
    TYPE(field_type) :: Mb_lumped_inv, Hb_lumped_inv
    CLASS(abstract_iterative_solver_type), POINTER :: gw_pressure_solver
    CONTAINS
    PROCEDURE, PRIVATE :: build_pressure_rhs
    FINAL :: destroy_gw_mixed_schur_preconditioner
  END TYPE gw_mixed_schur_preconditioner_type
  INTERFACE gw_mixed_schur_preconditioner_type
    MODULE PROCEDURE gw_mixed_schur_preconditioner_constructor
  END INTERFACE
  CONTAINS
  SUBROUTINE gw_mixed_schur_preconditioner_constructor(self, state, Hb_lumped_inv, pressure_solver)
    USE gw_mixed_schur_preconditioner_alg_mod_psy, ONLY: invoke_0
    USE function_space_mod, ONLY: function_space_type
    USE finite_element_config_mod, ONLY: element_order
    USE quadrature_xyoz_mod, ONLY: quadrature_xyoz_type
    USE quadrature_rule_gaussian_mod, ONLY: quadrature_rule_gaussian_type
    USE matrix_vector_kernel_mod, ONLY: matrix_vector_kernel_type
    IMPLICIT NONE
    CLASS(gw_mixed_schur_preconditioner_type), INTENT(INOUT) :: self
    TYPE(field_vector_type), INTENT(IN) :: state
    TYPE(field_type), INTENT(IN) :: Hb_lumped_inv
    CLASS(abstract_iterative_solver_type), TARGET, INTENT(IN) :: pressure_solver
    TYPE(function_space_type), POINTER :: wp => null(), wu => null(), wb => null()
    TYPE(field_type) :: ones, M_lumped
    TYPE(operator_type), POINTER :: Mb => null()
    TYPE(quadrature_xyoz_type) :: qr
    TYPE(quadrature_rule_gaussian_type) :: quadrature_rule
    CALL log_event('Constructing gravity waves mixed preconditioner...', LOG_LEVEL_INFO)
    self % alpha = 0.5_r_def
    wu => state % vector(igw_u) % get_function_space()
    wp => state % vector(igw_p) % get_function_space()
    wb => state % vector(igw_b) % get_function_space()
    self % p_inc = field_type(vector_space = wp)
    self % b_inc = field_type(vector_space = wb)
    self % u_inc = field_type(vector_space = wu)
    self % rhs_u = field_type(vector_space = wu)
    self % rhs_p = field_type(vector_space = wp)
    self % rhs_p_tmp = field_type(vector_space = wp)
    self % mb_rb = field_type(vector_space = wb)
    self % hb_ru = field_type(vector_space = wu)
    self % pressure_b = field_vector_type(1)
    self % pressure_x = field_vector_type(1)
    ones = field_type(vector_space = wb)
    M_lumped = field_type(vector_space = wb)
    self % Mb_lumped_inv = field_type(vector_space = wb)
    SELECT CASE (b_space)
    CASE (gravity_wave_constants_b_space_w0)
      Mb => get_mass_matrix(w0_id)
    CASE (gravity_wave_constants_b_space_w3)
      Mb => get_mass_matrix(w3_id)
    CASE (gravity_wave_constants_b_space_wtheta)
      Mb => get_mass_matrix(wt_id)
    END SELECT
    CALL invoke_0(ones, m_lumped, mb, self % mb_lumped_inv)
    self % Hb_lumped_inv = Hb_lumped_inv
    self % gw_pressure_solver => pressure_solver
    CALL log_event('done', LOG_LEVEL_INFO)
  END SUBROUTINE gw_mixed_schur_preconditioner_constructor
  SUBROUTINE build_pressure_rhs(self, rhs0)
    USE gw_mixed_schur_preconditioner_alg_mod_psy, ONLY: invoke_2
    USE gw_mixed_schur_preconditioner_alg_mod_psy, ONLY: invoke_1
    USE matrix_vector_kernel_mod, ONLY: matrix_vector_kernel_type
    USE dg_matrix_vector_kernel_mod, ONLY: dg_matrix_vector_kernel_type
    IMPLICIT NONE
    CLASS(gw_mixed_schur_preconditioner_type), INTENT(INOUT) :: self
    TYPE(field_vector_type), INTENT(IN) :: rhs0
    TYPE(operator_type), POINTER :: div => null(), M3_inv => null()
    REAL(KIND = r_def) :: const1, const2
    const1 = self % alpha * dt
    CALL invoke_1(self % mb_rb, rhs0 % vector(igw_b), self % mb_lumped_inv, self % rhs_u, self % q, const1, rhs0 % vector(igw_u))
    div => get_div()
    M3_inv => get_mass_matrix(w3inv_id)
    const2 = - self % alpha * dt * cs_square
    CALL invoke_2(self % hb_ru, self % rhs_u, self % hb_lumped_inv, self % rhs_p_tmp, div, self % rhs_p, m3_inv, const2, &
&rhs0 % vector(igw_p))
    CALL self % rhs_p % log_minmax(LOG_LEVEL_DEBUG, 'gw_pressure_rhs ')
  END SUBROUTINE build_pressure_rhs
  SUBROUTINE destroy_gw_mixed_schur_preconditioner(self)
    IMPLICIT NONE
    TYPE(gw_mixed_schur_preconditioner_type), INTENT(INOUT) :: self
  END SUBROUTINE destroy_gw_mixed_schur_preconditioner
END MODULE gw_mixed_schur_preconditioner_alg_mod