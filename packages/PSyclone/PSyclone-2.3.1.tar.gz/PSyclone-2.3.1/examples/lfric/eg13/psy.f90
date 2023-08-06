  MODULE gw_mixed_schur_preconditioner_alg_mod_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    USE operator_mod, ONLY: operator_type, operator_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(ones, m_lumped, mb, self_mb_lumped_inv)
      USE matrix_vector_kernel_0_mod, ONLY: matrix_vector_kernel_0_code
      USE mesh_mod, ONLY: mesh_type
      TYPE(field_type), intent(in) :: ones, m_lumped, self_mb_lumped_inv
      TYPE(operator_type), intent(in) :: mb
      INTEGER(KIND=i_def) cell
      INTEGER df
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers
      TYPE(operator_proxy_type) mb_proxy
      TYPE(field_proxy_type) ones_proxy, m_lumped_proxy, self_mb_lumped_inv_proxy
      INTEGER(KIND=i_def), pointer :: map_aspc1_m_lumped(:,:) => null(), map_aspc2_ones(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_ones, undf_aspc1_ones, ndf_aspc1_m_lumped, undf_aspc1_m_lumped, ndf_aspc2_ones, &
&undf_aspc2_ones, ndf_aspc1_self_mb_lumped_inv, undf_aspc1_self_mb_lumped_inv
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      ones_proxy = ones%get_proxy()
      m_lumped_proxy = m_lumped%get_proxy()
      mb_proxy = mb%get_proxy()
      self_mb_lumped_inv_proxy = self_mb_lumped_inv%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = ones_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => ones_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_aspc1_m_lumped => m_lumped_proxy%vspace%get_whole_dofmap()
      map_aspc2_ones => ones_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_ones
      !
      ndf_aspc1_ones = ones_proxy%vspace%get_ndf()
      undf_aspc1_ones = ones_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_m_lumped
      !
      ndf_aspc1_m_lumped = m_lumped_proxy%vspace%get_ndf()
      undf_aspc1_m_lumped = m_lumped_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc2_ones
      !
      ndf_aspc2_ones = ones_proxy%vspace%get_ndf()
      undf_aspc2_ones = ones_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_self_mb_lumped_inv
      !
      ndf_aspc1_self_mb_lumped_inv = self_mb_lumped_inv_proxy%vspace%get_ndf()
      undf_aspc1_self_mb_lumped_inv = self_mb_lumped_inv_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = ones_proxy%vspace%get_last_dof_owned()
      loop1_start = 1
      loop1_stop = m_lumped_proxy%vspace%get_last_dof_owned()
      loop2_start = 1
      loop2_stop = mesh%get_last_halo_cell(1)
      loop3_start = 1
      loop3_stop = self_mb_lumped_inv_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      DO df=loop0_start,loop0_stop
        ones_proxy%data(df) = 1.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL ones_proxy%set_dirty()
      !
      DO df=loop1_start,loop1_stop
        m_lumped_proxy%data(df) = 0.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL m_lumped_proxy%set_dirty()
      !
      CALL m_lumped_proxy%halo_exchange(depth=1)
      !
      CALL ones_proxy%halo_exchange(depth=1)
      !
      DO cell=loop2_start,loop2_stop
        !
        CALL matrix_vector_kernel_0_code(cell, nlayers, m_lumped_proxy%data, ones_proxy%data, mb_proxy%ncell_3d, &
&mb_proxy%local_stencil, ndf_aspc1_m_lumped, undf_aspc1_m_lumped, map_aspc1_m_lumped(:,cell), ndf_aspc2_ones, undf_aspc2_ones, &
&map_aspc2_ones(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL m_lumped_proxy%set_dirty()
      !
      DO df=loop3_start,loop3_stop
        self_mb_lumped_inv_proxy%data(df) = ones_proxy%data(df) / m_lumped_proxy%data(df)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_mb_lumped_inv_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_0
    SUBROUTINE invoke_1(self_mb_rb, rhs0_vector, self_mb_lumped_inv, self_rhs_u, self_q, const1, rhs0_vector_1)
      USE matrix_vector_kernel_1_mod, ONLY: matrix_vector_kernel_1_code
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(in) :: const1
      TYPE(field_type), intent(in) :: self_mb_rb, rhs0_vector, self_mb_lumped_inv, self_rhs_u, rhs0_vector_1
      TYPE(operator_type), intent(in) :: self_q
      INTEGER(KIND=i_def) cell
      INTEGER df
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers
      TYPE(operator_proxy_type) self_q_proxy
      TYPE(field_proxy_type) self_mb_rb_proxy, rhs0_vector_proxy, self_mb_lumped_inv_proxy, self_rhs_u_proxy, rhs0_vector_1_proxy
      INTEGER(KIND=i_def), pointer :: map_aspc1_self_rhs_u(:,:) => null(), map_aspc2_self_mb_rb(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_self_mb_rb, undf_aspc1_self_mb_rb, ndf_aspc1_self_rhs_u, undf_aspc1_self_rhs_u, &
&ndf_aspc2_self_mb_rb, undf_aspc2_self_mb_rb
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      self_mb_rb_proxy = self_mb_rb%get_proxy()
      rhs0_vector_proxy = rhs0_vector%get_proxy()
      self_mb_lumped_inv_proxy = self_mb_lumped_inv%get_proxy()
      self_rhs_u_proxy = self_rhs_u%get_proxy()
      self_q_proxy = self_q%get_proxy()
      rhs0_vector_1_proxy = rhs0_vector_1%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = self_mb_rb_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => self_mb_rb_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_aspc1_self_rhs_u => self_rhs_u_proxy%vspace%get_whole_dofmap()
      map_aspc2_self_mb_rb => self_mb_rb_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_self_mb_rb
      !
      ndf_aspc1_self_mb_rb = self_mb_rb_proxy%vspace%get_ndf()
      undf_aspc1_self_mb_rb = self_mb_rb_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_self_rhs_u
      !
      ndf_aspc1_self_rhs_u = self_rhs_u_proxy%vspace%get_ndf()
      undf_aspc1_self_rhs_u = self_rhs_u_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc2_self_mb_rb
      !
      ndf_aspc2_self_mb_rb = self_mb_rb_proxy%vspace%get_ndf()
      undf_aspc2_self_mb_rb = self_mb_rb_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = self_mb_rb_proxy%vspace%get_last_dof_owned()
      loop1_start = 1
      loop1_stop = self_rhs_u_proxy%vspace%get_last_dof_owned()
      loop2_start = 1
      loop2_stop = mesh%get_last_halo_cell(1)
      loop3_start = 1
      loop3_stop = self_rhs_u_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      DO df=loop0_start,loop0_stop
        self_mb_rb_proxy%data(df) = rhs0_vector_proxy%data(df) * self_mb_lumped_inv_proxy%data(df)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_mb_rb_proxy%set_dirty()
      !
      DO df=loop1_start,loop1_stop
        self_rhs_u_proxy%data(df) = 0.0_r_def
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_u_proxy%set_dirty()
      !
      CALL self_rhs_u_proxy%halo_exchange(depth=1)
      !
      CALL self_mb_rb_proxy%halo_exchange(depth=1)
      !
      DO cell=loop2_start,loop2_stop
        !
        CALL matrix_vector_kernel_1_code(cell, nlayers, self_rhs_u_proxy%data, self_mb_rb_proxy%data, self_q_proxy%ncell_3d, &
&self_q_proxy%local_stencil, ndf_aspc1_self_rhs_u, undf_aspc1_self_rhs_u, map_aspc1_self_rhs_u(:,cell), ndf_aspc2_self_mb_rb, &
&undf_aspc2_self_mb_rb, map_aspc2_self_mb_rb(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_u_proxy%set_dirty()
      !
      DO df=loop3_start,loop3_stop
        self_rhs_u_proxy%data(df) = const1 * self_rhs_u_proxy%data(df) + rhs0_vector_1_proxy%data(df)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_u_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_1
    SUBROUTINE invoke_2(self_hb_ru, self_rhs_u, self_hb_lumped_inv, self_rhs_p_tmp, div, self_rhs_p, m3_inv, const2, rhs0_vector)
      USE dg_matrix_vector_kernel_1_mod, ONLY: dg_matrix_vector_kernel_1_code
      USE dg_matrix_vector_kernel_0_mod, ONLY: dg_matrix_vector_kernel_0_code
      USE mesh_mod, ONLY: mesh_type
      REAL(KIND=r_def), intent(in) :: const2
      TYPE(field_type), intent(in) :: self_hb_ru, self_rhs_u, self_hb_lumped_inv, self_rhs_p_tmp, self_rhs_p, rhs0_vector
      TYPE(operator_type), intent(in) :: div, m3_inv
      INTEGER(KIND=i_def) cell
      INTEGER df
      INTEGER(KIND=i_def) loop3_start, loop3_stop
      INTEGER(KIND=i_def) loop2_start, loop2_stop
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers
      TYPE(operator_proxy_type) div_proxy, m3_inv_proxy
      TYPE(field_proxy_type) self_hb_ru_proxy, self_rhs_u_proxy, self_hb_lumped_inv_proxy, self_rhs_p_tmp_proxy, self_rhs_p_proxy, &
&rhs0_vector_proxy
      INTEGER(KIND=i_def), pointer :: map_adspc1_self_rhs_p(:,:) => null(), map_adspc1_self_rhs_p_tmp(:,:) => null(), &
&map_aspc1_self_hb_ru(:,:) => null(), map_aspc1_self_rhs_p_tmp(:,:) => null()
      INTEGER(KIND=i_def) ndf_aspc1_self_hb_ru, undf_aspc1_self_hb_ru, ndf_adspc1_self_rhs_p_tmp, undf_adspc1_self_rhs_p_tmp, &
&ndf_adspc1_self_rhs_p, undf_adspc1_self_rhs_p, ndf_aspc1_self_rhs_p_tmp, undf_aspc1_self_rhs_p_tmp, ndf_aspc1_self_rhs_p, &
&undf_aspc1_self_rhs_p
      INTEGER(KIND=i_def) max_halo_depth_mesh
      TYPE(mesh_type), pointer :: mesh => null()
      !
      ! Initialise field and/or operator proxies
      !
      self_hb_ru_proxy = self_hb_ru%get_proxy()
      self_rhs_u_proxy = self_rhs_u%get_proxy()
      self_hb_lumped_inv_proxy = self_hb_lumped_inv%get_proxy()
      self_rhs_p_tmp_proxy = self_rhs_p_tmp%get_proxy()
      div_proxy = div%get_proxy()
      self_rhs_p_proxy = self_rhs_p%get_proxy()
      m3_inv_proxy = m3_inv%get_proxy()
      rhs0_vector_proxy = rhs0_vector%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = self_hb_ru_proxy%vspace%get_nlayers()
      !
      ! Create a mesh object
      !
      mesh => self_hb_ru_proxy%vspace%get_mesh()
      max_halo_depth_mesh = mesh%get_halo_depth()
      !
      ! Look-up dofmaps for each function space
      !
      map_adspc1_self_rhs_p_tmp => self_rhs_p_tmp_proxy%vspace%get_whole_dofmap()
      map_aspc1_self_hb_ru => self_hb_ru_proxy%vspace%get_whole_dofmap()
      map_adspc1_self_rhs_p => self_rhs_p_proxy%vspace%get_whole_dofmap()
      map_aspc1_self_rhs_p_tmp => self_rhs_p_tmp_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for aspc1_self_hb_ru
      !
      ndf_aspc1_self_hb_ru = self_hb_ru_proxy%vspace%get_ndf()
      undf_aspc1_self_hb_ru = self_hb_ru_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for adspc1_self_rhs_p_tmp
      !
      ndf_adspc1_self_rhs_p_tmp = self_rhs_p_tmp_proxy%vspace%get_ndf()
      undf_adspc1_self_rhs_p_tmp = self_rhs_p_tmp_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for adspc1_self_rhs_p
      !
      ndf_adspc1_self_rhs_p = self_rhs_p_proxy%vspace%get_ndf()
      undf_adspc1_self_rhs_p = self_rhs_p_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_self_rhs_p_tmp
      !
      ndf_aspc1_self_rhs_p_tmp = self_rhs_p_tmp_proxy%vspace%get_ndf()
      undf_aspc1_self_rhs_p_tmp = self_rhs_p_tmp_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_self_rhs_p
      !
      ndf_aspc1_self_rhs_p = self_rhs_p_proxy%vspace%get_ndf()
      undf_aspc1_self_rhs_p = self_rhs_p_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = self_hb_ru_proxy%vspace%get_last_dof_owned()
      loop1_start = 1
      loop1_stop = mesh%get_last_edge_cell()
      loop2_start = 1
      loop2_stop = mesh%get_last_edge_cell()
      loop3_start = 1
      loop3_stop = self_rhs_p_proxy%vspace%get_last_dof_owned()
      !
      ! Call kernels and communication routines
      !
      DO df=loop0_start,loop0_stop
        self_hb_ru_proxy%data(df) = self_rhs_u_proxy%data(df) * self_hb_lumped_inv_proxy%data(df)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_hb_ru_proxy%set_dirty()
      !
      CALL self_hb_ru_proxy%halo_exchange(depth=1)
      !
      DO cell=loop1_start,loop1_stop
        !
        CALL dg_matrix_vector_kernel_0_code(cell, nlayers, self_rhs_p_tmp_proxy%data, self_hb_ru_proxy%data, div_proxy%ncell_3d, &
&div_proxy%local_stencil, ndf_adspc1_self_rhs_p_tmp, undf_adspc1_self_rhs_p_tmp, map_adspc1_self_rhs_p_tmp(:,cell), &
&ndf_aspc1_self_hb_ru, undf_aspc1_self_hb_ru, map_aspc1_self_hb_ru(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_p_tmp_proxy%set_dirty()
      !
      CALL self_rhs_p_tmp_proxy%halo_exchange(depth=1)
      !
      DO cell=loop2_start,loop2_stop
        !
        CALL dg_matrix_vector_kernel_1_code(cell, nlayers, self_rhs_p_proxy%data, self_rhs_p_tmp_proxy%data, &
&m3_inv_proxy%ncell_3d, m3_inv_proxy%local_stencil, ndf_adspc1_self_rhs_p, undf_adspc1_self_rhs_p, map_adspc1_self_rhs_p(:,cell), &
&ndf_aspc1_self_rhs_p_tmp, undf_aspc1_self_rhs_p_tmp, map_aspc1_self_rhs_p_tmp(:,cell))
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_p_proxy%set_dirty()
      !
      DO df=loop3_start,loop3_stop
        self_rhs_p_proxy%data(df) = const2 * self_rhs_p_proxy%data(df) + rhs0_vector_proxy%data(df)
      END DO
      !
      ! Set halos dirty/clean for fields modified in the above loop
      !
      CALL self_rhs_p_proxy%set_dirty()
      !
      !
    END SUBROUTINE invoke_2
  END MODULE gw_mixed_schur_preconditioner_alg_mod_psy