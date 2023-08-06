  MODULE helmholtz_solver_alg_mod_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    USE operator_mod, ONLY: operator_type, operator_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(grad_p, p, div_star, hb_inv, u_normalisation)
      USE scaled_matrix_vector_kernel_mod, ONLY: opt_scaled_matrix_vector_code
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: grad_p, p, hb_inv, u_normalisation
      TYPE(operator_type), intent(in) :: div_star
      INTEGER(KIND=i_def) cell
      INTEGER df
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers
      TYPE(operator_proxy_type) div_star_proxy
      TYPE(field_proxy_type) grad_p_proxy, p_proxy, hb_inv_proxy, u_normalisation_proxy
      INTEGER(KIND=i_def), pointer :: map_w2(:,:) => null(), map_w3(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_grad_p, undf_aspc1_grad_p, ndf_w2, undf_w2, ndf_w3, undf_w3
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      grad_p_proxy = grad_p%get_proxy()
      p_proxy = p%get_proxy()
      div_star_proxy = div_star%get_proxy()
      hb_inv_proxy = hb_inv%get_proxy()
      u_normalisation_proxy = u_normalisation%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = grad_p_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => grad_p_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_w2 => grad_p_proxy%vspace%get_whole_dofmap()
      map_w3 => p_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_grad_p
      !
      ndf_aspc1_grad_p = grad_p_proxy%vspace%get_ndf()
      undf_aspc1_grad_p = grad_p_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w2
      !
      ndf_w2 = grad_p_proxy%vspace%get_ndf()
      undf_w2 = grad_p_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for w3
      !
      ndf_w3 = p_proxy%vspace%get_ndf()
      undf_w3 = p_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = grad_p_proxy%vspace%get_last_dof_halo(1)
      loop1_start = 1
      loop1_stop = mesh%get_last_halo_cell(1)
      !
      ! Call kernels and communication routines
      !
      IF (p_proxy%is_dirty(depth=1)) THEN
        CALL p_proxy%halo_exchange_start(depth=1)
      END IF
      !
      IF (hb_inv_proxy%is_dirty(depth=1)) THEN
        CALL hb_inv_proxy%halo_exchange_start(depth=1)
      END IF
      !
      IF (u_normalisation_proxy%is_dirty(depth=1)) THEN
        CALL u_normalisation_proxy%halo_exchange_start(depth=1)
      END IF
      !
      DO df=loop0_start,loop0_stop
        grad_p_proxy%data(df) = 0.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL grad_p_proxy%set_dirty()
      CALL grad_p_proxy%set_clean(1)
      !
      IF (p_proxy%is_dirty(depth=1)) THEN
        CALL p_proxy%halo_exchange_finish(depth=1)
      END IF
      !
      IF (hb_inv_proxy%is_dirty(depth=1)) THEN
        CALL hb_inv_proxy%halo_exchange_finish(depth=1)
      END IF
      !
      IF (u_normalisation_proxy%is_dirty(depth=1)) THEN
        CALL u_normalisation_proxy%halo_exchange_finish(depth=1)
      END IF
      !
      DO cell=loop1_start,loop1_stop
        !
        CALL opt_scaled_matrix_vector_code(cell, nlayers, grad_p_proxy%data, p_proxy%data, div_star_proxy%ncell_3d, &
&div_star_proxy%local_stencil, hb_inv_proxy%data, u_normalisation_proxy%data, ndf_w2, undf_w2, map_w2(:,cell), ndf_w3, undf_w3, &
&map_w3(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL grad_p_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_0
  END MODULE helmholtz_solver_alg_mod_psy