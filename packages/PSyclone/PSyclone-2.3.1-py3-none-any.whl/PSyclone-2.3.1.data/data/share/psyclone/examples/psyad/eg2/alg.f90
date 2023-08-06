PROGRAM main
  USE main_psy, ONLY: invoke_1
  USE main_psy, ONLY: invoke_0
  USE mesh_mod, ONLY: mesh_type, plane
  USE partition_mod, ONLY: partition_type, partitioner_interface, partitioner_planar
  USE global_mesh_base_mod, ONLY: global_mesh_base_type
  USE extrusion_mod, ONLY: uniform_extrusion_type
  USE field_mod, ONLY: field_type
  USE function_space_mod, ONLY: function_space_type
  USE fs_continuity_mod, ONLY: w0, w3, wtheta
  USE constants_mod, ONLY: i_def, r_def
  USE operator_mod, ONLY: operator_type
  USE tl_rhs_eos_kernel_mod, ONLY: tl_rhs_eos_kernel_type
  USE tl_rhs_eos_kernel_mod_adj, ONLY: tl_rhs_eos_kernel_type_adj
  USE quadrature_xyoz_mod, ONLY: quadrature_xyoz_type
  USE quadrature_rule_gaussian_mod, ONLY: quadrature_rule_gaussian_type
  INTEGER, PARAMETER :: element_order = 1
  REAL(KIND = r_def), PARAMETER :: overall_tolerance = 1500.0_r_def
  TYPE(partition_type) :: partition
  TYPE(mesh_type), TARGET :: mesh
  TYPE(global_mesh_base_type), TARGET :: global_mesh
  CLASS(global_mesh_base_type), POINTER :: global_mesh_ptr
  TYPE(uniform_extrusion_type), TARGET :: extrusion
  TYPE(uniform_extrusion_type), POINTER :: extrusion_ptr
  PROCEDURE(partitioner_interface), POINTER :: partitioner_ptr
  INTEGER :: ndata_sz
  TYPE(function_space_type), TARGET :: vector_space_w0
  TYPE(function_space_type), POINTER :: vector_space_w0_ptr
  TYPE(function_space_type), TARGET :: vector_space_w3
  TYPE(function_space_type), POINTER :: vector_space_w3_ptr
  TYPE(function_space_type), TARGET :: vector_space_wtheta
  TYPE(function_space_type), POINTER :: vector_space_wtheta_ptr
  TYPE(field_type) :: field_1
  TYPE(field_type) :: field_2
  TYPE(field_type) :: field_3
  TYPE(field_type) :: field_4
  TYPE(field_type) :: field_5
  TYPE(field_type) :: field_6
  TYPE(field_type) :: field_7
  TYPE(field_type) :: field_8
  TYPE(field_type) :: field_9
  TYPE(field_type), DIMENSION(3) :: field_10
  TYPE(field_type) :: field_11
  REAL(KIND = r_def) :: rscalar_12
  REAL(KIND = r_def) :: rscalar_13
  REAL(KIND = r_def) :: rscalar_14
  TYPE(quadrature_xyoz_type) :: qr_xyoz
  TYPE(quadrature_rule_gaussian_type) :: quadrature_rule
  TYPE(field_type) :: field_1_input
  TYPE(field_type) :: field_2_input
  TYPE(field_type) :: field_3_input
  TYPE(field_type) :: field_4_input
  TYPE(field_type) :: field_5_input
  TYPE(field_type) :: field_6_input
  TYPE(field_type) :: field_7_input
  TYPE(field_type) :: field_8_input
  TYPE(field_type) :: field_9_input
  TYPE(field_type), DIMENSION(3) :: field_10_input
  TYPE(field_type) :: field_11_input
  REAL(KIND = r_def) :: rscalar_12_input
  REAL(KIND = r_def) :: rscalar_13_input
  REAL(KIND = r_def) :: rscalar_14_input
  TYPE(quadrature_xyoz_type) :: qr_xyoz_input
  REAL(KIND = r_def) :: field_1_inner_prod
  REAL(KIND = r_def) :: field_2_inner_prod
  REAL(KIND = r_def) :: field_3_inner_prod
  REAL(KIND = r_def) :: field_4_inner_prod
  REAL(KIND = r_def) :: field_5_inner_prod
  REAL(KIND = r_def) :: field_6_inner_prod
  REAL(KIND = r_def) :: field_7_inner_prod
  REAL(KIND = r_def) :: field_8_inner_prod
  REAL(KIND = r_def) :: field_9_inner_prod
  REAL(KIND = r_def), DIMENSION(3) :: field_10_inner_prod
  REAL(KIND = r_def) :: field_11_inner_prod
  REAL(KIND = r_def) :: inner1
  REAL(KIND = r_def) :: inner2
  REAL(KIND = r_def) :: MachineTol
  REAL(KIND = r_def) :: relative_diff
  global_mesh = global_mesh_base_type()
  global_mesh_ptr => global_mesh
  partitioner_ptr => partitioner_planar
  partition = partition_type(global_mesh_ptr, partitioner_ptr, 1, 1, 0, 0, 1)
  extrusion = uniform_extrusion_type(0.0_r_def, 100.0_r_def, 100)
  extrusion_ptr => extrusion
  mesh = mesh_type(global_mesh_ptr, partition, extrusion_ptr)
  WRITE(*, *) "Mesh has", mesh % get_nlayers(), "layers."
  ndata_sz = 1
  vector_space_w0 = function_space_type(mesh, element_order, w0, ndata_sz)
  vector_space_w0_ptr => vector_space_w0
  vector_space_w3 = function_space_type(mesh, element_order, w3, ndata_sz)
  vector_space_w3_ptr => vector_space_w3
  vector_space_wtheta = function_space_type(mesh, element_order, wtheta, ndata_sz)
  vector_space_wtheta_ptr => vector_space_wtheta
  CALL field_1 % initialise(vector_space = vector_space_w3_ptr, name = 'field_1')
  CALL field_2 % initialise(vector_space = vector_space_w3_ptr, name = 'field_2')
  CALL field_3 % initialise(vector_space = vector_space_w3_ptr, name = 'field_3')
  CALL field_4 % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_4')
  CALL field_5 % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_5')
  CALL field_6 % initialise(vector_space = vector_space_w3_ptr, name = 'field_6')
  CALL field_7 % initialise(vector_space = vector_space_w3_ptr, name = 'field_7')
  CALL field_8 % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_8')
  CALL field_9 % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_9')
  CALL field_10(1) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10')
  CALL field_10(2) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10')
  CALL field_10(3) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10')
  CALL field_11 % initialise(vector_space = vector_space_w3_ptr, name = 'field_11')
  qr_xyoz = quadrature_xyoz_type(element_order + 3, quadrature_rule)
  CALL random_number(rscalar_12)
  rscalar_12_input = rscalar_12
  CALL random_number(rscalar_13)
  rscalar_13_input = rscalar_13
  CALL random_number(rscalar_14)
  rscalar_14_input = rscalar_14
  CALL field_1_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_1_input')
  CALL field_2_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_2_input')
  CALL field_3_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_3_input')
  CALL field_4_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_4_input')
  CALL field_5_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_5_input')
  CALL field_6_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_6_input')
  CALL field_7_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_7_input')
  CALL field_8_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_8_input')
  CALL field_9_input % initialise(vector_space = vector_space_wtheta_ptr, name = 'field_9_input')
  CALL field_10_input(1) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10_input')
  CALL field_10_input(2) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10_input')
  CALL field_10_input(3) % initialise(vector_space = vector_space_w0_ptr, name = 'field_10_input')
  CALL field_11_input % initialise(vector_space = vector_space_w3_ptr, name = 'field_11_input')
  field_1_inner_prod = 0.0_r_def
  field_2_inner_prod = 0.0_r_def
  field_3_inner_prod = 0.0_r_def
  field_4_inner_prod = 0.0_r_def
  field_5_inner_prod = 0.0_r_def
  field_6_inner_prod = 0.0_r_def
  field_7_inner_prod = 0.0_r_def
  field_8_inner_prod = 0.0_r_def
  field_9_inner_prod = 0.0_r_def
  field_10_inner_prod(1) = 0.0_r_def
  field_10_inner_prod(2) = 0.0_r_def
  field_10_inner_prod(3) = 0.0_r_def
  field_11_inner_prod = 0.0_r_def
  CALL invoke_0(field_1, field_1_input, field_2, field_2_input, field_3, field_3_input, field_4, field_4_input, field_5, &
&field_5_input, field_6, field_6_input, field_7, field_7_input, field_8, field_8_input, field_9, field_9_input, field_10(1), &
&field_10_input(1), field_10(2), field_10_input(2), field_10(3), field_10_input(3), field_11, field_11_input, field_10, &
&rscalar_12, rscalar_13, rscalar_14, field_1_inner_prod, field_2_inner_prod, field_3_inner_prod, field_4_inner_prod, &
&field_5_inner_prod, field_6_inner_prod, field_7_inner_prod, field_8_inner_prod, field_9_inner_prod, field_10_inner_prod(1), &
&field_10_inner_prod(2), field_10_inner_prod(3), field_11_inner_prod, qr_xyoz)
  inner1 = 0.0_r_def
  inner1 = inner1 + rscalar_12 * rscalar_12
  inner1 = inner1 + rscalar_13 * rscalar_13
  inner1 = inner1 + rscalar_14 * rscalar_14
  inner1 = inner1 + field_1_inner_prod
  inner1 = inner1 + field_2_inner_prod
  inner1 = inner1 + field_3_inner_prod
  inner1 = inner1 + field_4_inner_prod
  inner1 = inner1 + field_5_inner_prod
  inner1 = inner1 + field_6_inner_prod
  inner1 = inner1 + field_7_inner_prod
  inner1 = inner1 + field_8_inner_prod
  inner1 = inner1 + field_9_inner_prod
  inner1 = inner1 + field_10_inner_prod(1)
  inner1 = inner1 + field_10_inner_prod(2)
  inner1 = inner1 + field_10_inner_prod(3)
  inner1 = inner1 + field_11_inner_prod
  field_1_inner_prod = 0.0_r_def
  field_2_inner_prod = 0.0_r_def
  field_3_inner_prod = 0.0_r_def
  field_4_inner_prod = 0.0_r_def
  field_5_inner_prod = 0.0_r_def
  field_6_inner_prod = 0.0_r_def
  field_7_inner_prod = 0.0_r_def
  field_8_inner_prod = 0.0_r_def
  field_9_inner_prod = 0.0_r_def
  field_10_inner_prod(1) = 0.0_r_def
  field_10_inner_prod(2) = 0.0_r_def
  field_10_inner_prod(3) = 0.0_r_def
  field_11_inner_prod = 0.0_r_def
  CALL invoke_1(field_1, field_2, field_3, field_4, field_5, field_6, field_7, field_8, field_9, field_10, field_11, rscalar_12, &
&rscalar_13, rscalar_14, field_1_inner_prod, field_1_input, field_2_inner_prod, field_2_input, field_3_inner_prod, field_3_input, &
&field_4_inner_prod, field_4_input, field_5_inner_prod, field_5_input, field_6_inner_prod, field_6_input, field_7_inner_prod, &
&field_7_input, field_8_inner_prod, field_8_input, field_9_inner_prod, field_9_input, field_10_inner_prod(1), field_10(1), &
&field_10_input(1), field_10_inner_prod(2), field_10(2), field_10_input(2), field_10_inner_prod(3), field_10(3), &
&field_10_input(3), field_11_inner_prod, field_11_input, qr_xyoz)
  inner2 = 0.0_r_def
  inner2 = inner2 + rscalar_12 * rscalar_12_input
  inner2 = inner2 + rscalar_13 * rscalar_13_input
  inner2 = inner2 + rscalar_14 * rscalar_14_input
  inner2 = inner2 + field_1_inner_prod
  inner2 = inner2 + field_2_inner_prod
  inner2 = inner2 + field_3_inner_prod
  inner2 = inner2 + field_4_inner_prod
  inner2 = inner2 + field_5_inner_prod
  inner2 = inner2 + field_6_inner_prod
  inner2 = inner2 + field_7_inner_prod
  inner2 = inner2 + field_8_inner_prod
  inner2 = inner2 + field_9_inner_prod
  inner2 = inner2 + field_10_inner_prod(1)
  inner2 = inner2 + field_10_inner_prod(2)
  inner2 = inner2 + field_10_inner_prod(3)
  inner2 = inner2 + field_11_inner_prod
  MachineTol = SPACING(MAX(ABS(inner1), ABS(inner2)))
  relative_diff = ABS(inner1 - inner2) / MachineTol
  IF (relative_diff < overall_tolerance) THEN
    WRITE(*, *) 'Test of adjoint of ''tl_rhs_eos_kernel_type'' PASSED: ', inner1, inner2, relative_diff
  ELSE
    WRITE(*, *) 'Test of adjoint of ''tl_rhs_eos_kernel_type'' FAILED: ', inner1, inner2, relative_diff
  END IF
END PROGRAM main