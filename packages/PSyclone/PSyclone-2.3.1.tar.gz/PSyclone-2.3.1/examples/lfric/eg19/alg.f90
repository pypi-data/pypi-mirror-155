PROGRAM mixed_precision
  USE mixed_precision_psy, ONLY: invoke_0
  USE constants_mod, ONLY: r_def, r_solver, r_tran
  USE mixed_kernel_mod, ONLY: mixed_kernel_type
  REAL(KIND = r_def) :: scalar_r_def
  REAL(KIND = r_solver) :: scalar_r_solver
  REAL(KIND = r_tran) :: scalar_r_tran
  TYPE(field_type) :: field_r_def
  TYPE(r_solver_field_type) :: field_r_solver
  TYPE(r_tran_field_type) :: field_r_tran
  TYPE(operator_type) :: operator_r_def
  TYPE(r_solver_operator_type) :: operator_r_solver
  CALL invoke_0(scalar_r_def, field_r_def, operator_r_def, scalar_r_solver, field_r_solver, operator_r_solver, scalar_r_tran, &
&field_r_tran)
END PROGRAM mixed_precision