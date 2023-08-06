program adj_test
  use tl_kinetic_energy_gradient_kernel_mod, only : tl_kinetic_energy_gradient_code
  use tl_kinetic_energy_gradient_kernel_mod_adj, only : tl_kinetic_energy_gradient_code_adj
  use constants_mod, only : i_def, r_def
  integer, parameter :: array_extent = 20
  integer(kind=i_def), parameter :: ndf_chi = array_extent
  integer(kind=i_def), parameter :: nqp_v = array_extent
  integer(kind=i_def), parameter :: ndf_w2 = array_extent
  integer(kind=i_def), parameter :: undf_pid = array_extent
  integer(kind=i_def), parameter :: ndf_pid = array_extent
  integer(kind=i_def), parameter :: undf_w2 = array_extent
  integer(kind=i_def), parameter :: undf_chi = array_extent
  integer(kind=i_def), parameter :: nqp_h = array_extent
  real(kind=r_def), parameter :: overall_tolerance = 1500.0_r_def
  real(kind=r_def) :: inner1
  real(kind=r_def) :: inner2
  integer(kind=i_def) :: nlayers
  integer(kind=i_def) :: nlayers_input
  real(kind=r_def), dimension(undf_w2) :: r_u
  real(kind=r_def), dimension(undf_w2) :: r_u_input
  real(kind=r_def), dimension(undf_w2) :: u
  real(kind=r_def), dimension(undf_w2) :: u_input
  real(kind=r_def), dimension(undf_w2) :: ls_u
  real(kind=r_def), dimension(undf_w2) :: ls_u_input
  real(kind=r_def), dimension(undf_chi) :: chi_1
  real(kind=r_def), dimension(undf_chi) :: chi_1_input
  real(kind=r_def), dimension(undf_chi) :: chi_2
  real(kind=r_def), dimension(undf_chi) :: chi_2_input
  real(kind=r_def), dimension(undf_chi) :: chi_3
  real(kind=r_def), dimension(undf_chi) :: chi_3_input
  real(kind=r_def), dimension(undf_pid) :: panel_id
  real(kind=r_def), dimension(undf_pid) :: panel_id_input
  integer(kind=i_def), dimension(ndf_w2) :: map_w2
  integer(kind=i_def), dimension(ndf_w2) :: map_w2_input
  real(kind=r_def), dimension(3,ndf_w2,nqp_h,nqp_v) :: w2_basis
  real(kind=r_def), dimension(3,ndf_w2,nqp_h,nqp_v) :: w2_basis_input
  real(kind=r_def), dimension(1,ndf_w2,nqp_h,nqp_v) :: w2_diff_basis
  real(kind=r_def), dimension(1,ndf_w2,nqp_h,nqp_v) :: w2_diff_basis_input
  integer(kind=i_def), dimension(ndf_chi) :: map_chi
  integer(kind=i_def), dimension(ndf_chi) :: map_chi_input
  real(kind=r_def), dimension(1,ndf_chi,nqp_h,nqp_v) :: chi_basis
  real(kind=r_def), dimension(1,ndf_chi,nqp_h,nqp_v) :: chi_basis_input
  real(kind=r_def), dimension(3,ndf_chi,nqp_h,nqp_v) :: chi_diff_basis
  real(kind=r_def), dimension(3,ndf_chi,nqp_h,nqp_v) :: chi_diff_basis_input
  integer(kind=i_def), dimension(ndf_pid) :: map_pid
  integer(kind=i_def), dimension(ndf_pid) :: map_pid_input
  real(kind=r_def), dimension(nqp_h) :: wqp_h
  real(kind=r_def), dimension(nqp_h) :: wqp_h_input
  real(kind=r_def), dimension(nqp_v) :: wqp_v
  real(kind=r_def), dimension(nqp_v) :: wqp_v_input
  real(kind=r_def) :: MachineTol
  real(kind=r_def) :: relative_diff

  ! Initialise the kernel arguments and keep copies of them
  CALL random_number(nlayers)
  nlayers_input = nlayers
  CALL random_number(r_u)
  r_u_input = r_u
  CALL random_number(u)
  u_input = u
  CALL random_number(ls_u)
  ls_u_input = ls_u
  CALL random_number(chi_1)
  chi_1_input = chi_1
  CALL random_number(chi_2)
  chi_2_input = chi_2
  CALL random_number(chi_3)
  chi_3_input = chi_3
  CALL random_number(panel_id)
  panel_id_input = panel_id
  CALL random_number(map_w2)
  map_w2_input = map_w2
  CALL random_number(w2_basis)
  w2_basis_input = w2_basis
  CALL random_number(w2_diff_basis)
  w2_diff_basis_input = w2_diff_basis
  CALL random_number(map_chi)
  map_chi_input = map_chi
  CALL random_number(chi_basis)
  chi_basis_input = chi_basis
  CALL random_number(chi_diff_basis)
  chi_diff_basis_input = chi_diff_basis
  CALL random_number(map_pid)
  map_pid_input = map_pid
  CALL random_number(wqp_h)
  wqp_h_input = wqp_h
  CALL random_number(wqp_v)
  wqp_v_input = wqp_v
  ! Call the tangent-linear kernel
  call tl_kinetic_energy_gradient_code(nlayers, r_u, u, ls_u, chi_1, chi_2, chi_3, panel_id, ndf_w2, undf_w2, map_w2, w2_basis, w2_diff_basis, ndf_chi, undf_chi, map_chi, chi_basis, chi_diff_basis, ndf_pid, undf_pid, map_pid, nqp_h, nqp_v, wqp_h, wqp_v)
  ! Compute the inner product of the results of the tangent-linear kernel
  inner1 = 0.0_r_def
  inner1 = inner1 + nlayers * nlayers
  inner1 = inner1 + DOT_PRODUCT(r_u, r_u)
  inner1 = inner1 + DOT_PRODUCT(u, u)
  inner1 = inner1 + DOT_PRODUCT(ls_u, ls_u)
  inner1 = inner1 + DOT_PRODUCT(chi_1, chi_1)
  inner1 = inner1 + DOT_PRODUCT(chi_2, chi_2)
  inner1 = inner1 + DOT_PRODUCT(chi_3, chi_3)
  inner1 = inner1 + DOT_PRODUCT(panel_id, panel_id)
  inner1 = inner1 + DOT_PRODUCT(map_w2, map_w2)
  inner1 = inner1 + SUM(w2_basis(:,:,:,:) * w2_basis(:,:,:,:))
  inner1 = inner1 + SUM(w2_diff_basis(:,:,:,:) * w2_diff_basis(:,:,:,:))
  inner1 = inner1 + DOT_PRODUCT(map_chi, map_chi)
  inner1 = inner1 + SUM(chi_basis(:,:,:,:) * chi_basis(:,:,:,:))
  inner1 = inner1 + SUM(chi_diff_basis(:,:,:,:) * chi_diff_basis(:,:,:,:))
  inner1 = inner1 + DOT_PRODUCT(map_pid, map_pid)
  inner1 = inner1 + DOT_PRODUCT(wqp_h, wqp_h)
  inner1 = inner1 + DOT_PRODUCT(wqp_v, wqp_v)
  ! Call the adjoint of the kernel
  call tl_kinetic_energy_gradient_code_adj(nlayers, r_u, u, ls_u, chi_1, chi_2, chi_3, panel_id, ndf_w2, undf_w2, map_w2, w2_basis, w2_diff_basis, ndf_chi, undf_chi, map_chi, chi_basis, chi_diff_basis, ndf_pid, undf_pid, map_pid, nqp_h, nqp_v, wqp_h, wqp_v)
  ! Compute inner product of results of adjoint kernel with the original inputs to the tangent-linear kernel
  inner2 = 0.0_r_def
  inner2 = inner2 + nlayers * nlayers_input
  inner2 = inner2 + DOT_PRODUCT(r_u, r_u_input)
  inner2 = inner2 + DOT_PRODUCT(u, u_input)
  inner2 = inner2 + DOT_PRODUCT(ls_u, ls_u_input)
  inner2 = inner2 + DOT_PRODUCT(chi_1, chi_1_input)
  inner2 = inner2 + DOT_PRODUCT(chi_2, chi_2_input)
  inner2 = inner2 + DOT_PRODUCT(chi_3, chi_3_input)
  inner2 = inner2 + DOT_PRODUCT(panel_id, panel_id_input)
  inner2 = inner2 + DOT_PRODUCT(map_w2, map_w2_input)
  inner2 = inner2 + SUM(w2_basis(:,:,:,:) * w2_basis_input(:,:,:,:))
  inner2 = inner2 + SUM(w2_diff_basis(:,:,:,:) * w2_diff_basis_input(:,:,:,:))
  inner2 = inner2 + DOT_PRODUCT(map_chi, map_chi_input)
  inner2 = inner2 + SUM(chi_basis(:,:,:,:) * chi_basis_input(:,:,:,:))
  inner2 = inner2 + SUM(chi_diff_basis(:,:,:,:) * chi_diff_basis_input(:,:,:,:))
  inner2 = inner2 + DOT_PRODUCT(map_pid, map_pid_input)
  inner2 = inner2 + DOT_PRODUCT(wqp_h, wqp_h_input)
  inner2 = inner2 + DOT_PRODUCT(wqp_v, wqp_v_input)
  ! Test the inner-product values for equality, allowing for the precision of the active variables
  MachineTol = SPACING(MAX(ABS(inner1), ABS(inner2)))
  relative_diff = ABS(inner1 - inner2) / MachineTol
  if (relative_diff < overall_tolerance) then
    WRITE(*, *) 'Test of adjoint of ''tl_kinetic_energy_gradient_code'' PASSED: ', inner1, inner2, relative_diff
  else
    WRITE(*, *) 'Test of adjoint of ''tl_kinetic_energy_gradient_code'' FAILED: ', inner1, inner2, relative_diff
  end if

end program adj_test
