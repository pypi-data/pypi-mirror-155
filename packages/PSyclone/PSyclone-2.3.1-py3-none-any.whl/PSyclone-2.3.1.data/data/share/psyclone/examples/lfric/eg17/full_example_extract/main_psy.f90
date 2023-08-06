  MODULE main_psy
    USE constants_mod, ONLY: r_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_initialise_fields(field1, field2)
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER df
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def) undf_aspc1_field1, undf_aspc1_field2
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field2_proxy = field2%get_proxy()
      !
      ! Initialise number of DoFs for aspc1_field1
      !
      undf_aspc1_field1 = field1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_field2
      !
      undf_aspc1_field2 = field2_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = undf_aspc1_field1
      loop1_start = 1
      loop1_stop = undf_aspc1_field2
      !
      ! Call our kernels
      !
      DO df=loop0_start,loop0_stop
        field1_proxy%data(df) = 0.0_r_def
      END DO
      DO df=loop1_start,loop1_stop
        field2_proxy%data(df) = 1.0_r_def
      END DO
      !
    END SUBROUTINE invoke_initialise_fields
    SUBROUTINE invoke_testkern_w0(field1, field2)
      USE testkern_w0_kernel_mod, ONLY: testkern_w0_code
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) cell
      TYPE(extract_PSyDataType), target, save :: extract_psy_data
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def), pointer :: map_w0(:,:) => null()
      INTEGER(KIND=i_def) ndf_w0, undf_w0
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field2_proxy = field2%get_proxy()
      !
      ! Initialise number of layers
      !
      nlayers = field1_proxy%vspace%get_nlayers()
      !
      ! Look-up dofmaps for each function space
      !
      map_w0 => field1_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for w0
      !
      ndf_w0 = field1_proxy%vspace%get_ndf()
      undf_w0 = field1_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field1_proxy%vspace%get_ncell()
      !
      ! Call our kernels
      !
      !
      ! ExtractStart
      !
      CALL extract_psy_data%PreStart("main", "update", 8, 2)
      CALL extract_psy_data%PreDeclareVariable("field1", field1)
      CALL extract_psy_data%PreDeclareVariable("field2", field2)
      CALL extract_psy_data%PreDeclareVariable("loop0_start", loop0_start)
      CALL extract_psy_data%PreDeclareVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%PreDeclareVariable("map_w0", map_w0)
      CALL extract_psy_data%PreDeclareVariable("ndf_w0", ndf_w0)
      CALL extract_psy_data%PreDeclareVariable("nlayers", nlayers)
      CALL extract_psy_data%PreDeclareVariable("undf_w0", undf_w0)
      CALL extract_psy_data%PreDeclareVariable("cell_post", cell)
      CALL extract_psy_data%PreDeclareVariable("field1_post", field1)
      CALL extract_psy_data%PreEndDeclaration
      CALL extract_psy_data%ProvideVariable("field1", field1)
      CALL extract_psy_data%ProvideVariable("field2", field2)
      CALL extract_psy_data%ProvideVariable("loop0_start", loop0_start)
      CALL extract_psy_data%ProvideVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%ProvideVariable("map_w0", map_w0)
      CALL extract_psy_data%ProvideVariable("ndf_w0", ndf_w0)
      CALL extract_psy_data%ProvideVariable("nlayers", nlayers)
      CALL extract_psy_data%ProvideVariable("undf_w0", undf_w0)
      CALL extract_psy_data%PreEnd
      DO cell=loop0_start,loop0_stop
        !
        CALL testkern_w0_code(nlayers, field1_proxy%data, field2_proxy%data, ndf_w0, undf_w0, map_w0(:,cell))
      END DO
      CALL extract_psy_data%PostStart
      CALL extract_psy_data%ProvideVariable("cell_post", cell)
      CALL extract_psy_data%ProvideVariable("field1_post", field1)
      CALL extract_psy_data%PostEnd
      !
      ! ExtractEnd
      !
      !
    END SUBROUTINE invoke_testkern_w0
  END MODULE main_psy