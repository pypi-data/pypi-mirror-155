  MODULE psy_simple
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0(cu_fld, p_fld, u_fld, cv_fld, v_fld, z_fld, h_fld)
      USE fortcl, ONLY: get_cmd_queues, get_kernel_by_name, get_num_cmd_queues
      USE clfortran, ONLY: clEnqueueNDRangeKernel, clFinish
      USE iso_c_binding, ONLY: C_LOC, C_NULL_PTR
      TYPE(r2d_field), intent(inout) :: cu_fld
      TYPE(r2d_field), intent(inout) :: p_fld
      TYPE(r2d_field), intent(inout) :: u_fld
      TYPE(r2d_field), intent(inout) :: cv_fld
      TYPE(r2d_field), intent(inout) :: v_fld
      TYPE(r2d_field), intent(inout) :: z_fld
      TYPE(r2d_field), intent(inout) :: h_fld
      INTEGER j
      INTEGER i
      INTEGER xstart
      INTEGER xstop
      INTEGER ystart
      INTEGER ystop
      INTEGER xstart_1
      INTEGER xstop_1
      INTEGER ystart_1
      INTEGER ystop_1
      INTEGER xstart_2
      INTEGER xstop_2
      INTEGER ystart_2
      INTEGER ystop_2
      INTEGER xstart_3
      INTEGER xstop_3
      INTEGER ystart_3
      INTEGER ystop_3
      INTEGER(KIND=c_intptr_t), pointer, save :: cmd_queues(:)
      LOGICAL, save :: first_time = .true.
      INTEGER ierr
      INTEGER(KIND=c_size_t), target :: globalsize(2)
      INTEGER(KIND=c_size_t), target :: localsize(2)
      INTEGER(KIND=c_intptr_t), TARGET, SAVE :: kernel_compute_cu_code
      INTEGER(KIND=c_intptr_t), TARGET, SAVE :: kernel_compute_cv_code
      INTEGER(KIND=c_intptr_t), TARGET, SAVE :: kernel_compute_z_code
      INTEGER(KIND=c_intptr_t), TARGET, SAVE :: kernel_compute_h_code
      INTEGER(KIND=c_intptr_t) cu_fld_cl_mem
      INTEGER(KIND=c_intptr_t) p_fld_cl_mem
      INTEGER(KIND=c_intptr_t) u_fld_cl_mem
      INTEGER(KIND=c_intptr_t) cv_fld_cl_mem
      INTEGER(KIND=c_intptr_t) v_fld_cl_mem
      INTEGER(KIND=c_intptr_t) z_fld_cl_mem
      INTEGER(KIND=c_intptr_t) h_fld_cl_mem

      xstart = cu_fld%internal%xstart
      xstop = cu_fld%internal%xstop
      ystart = cu_fld%internal%ystart
      ystop = cu_fld%internal%ystop
      xstart_1 = cv_fld%internal%xstart
      xstop_1 = cv_fld%internal%xstop
      ystart_1 = cv_fld%internal%ystart
      ystop_1 = cv_fld%internal%ystop
      xstart_2 = z_fld%internal%xstart
      xstop_2 = z_fld%internal%xstop
      ystart_2 = z_fld%internal%ystart
      ystop_2 = z_fld%internal%ystop
      xstart_3 = h_fld%internal%xstart
      xstop_3 = h_fld%internal%xstop
      ystart_3 = h_fld%internal%ystart
      ystop_3 = h_fld%internal%ystop
      ! Initialise OpenCL runtime, kernels and buffers
      IF (first_time) THEN
        CALL psy_init
        cmd_queues => get_cmd_queues()
        kernel_compute_cu_code = get_kernel_by_name('compute_cu_code')
        kernel_compute_cv_code = get_kernel_by_name('compute_cv_code')
        kernel_compute_z_code = get_kernel_by_name('compute_z_code')
        kernel_compute_h_code = get_kernel_by_name('compute_h_code')
        CALL initialise_device_buffer(cu_fld)
        CALL initialise_device_buffer(p_fld)
        CALL initialise_device_buffer(u_fld)
        CALL initialise_device_buffer(cv_fld)
        CALL initialise_device_buffer(v_fld)
        CALL initialise_device_buffer(z_fld)
        CALL initialise_device_buffer(h_fld)
        ! Do a set_args now so subsequent writes place the data appropriately
        cu_fld_cl_mem = TRANSFER(cu_fld%device_ptr, cu_fld_cl_mem)
        p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
        u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
        CALL compute_cu_code_set_args(kernel_compute_cu_code, cu_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, xstart - 1, xstop - 1, &
&ystart - 1, ystop - 1)
        cv_fld_cl_mem = TRANSFER(cv_fld%device_ptr, cv_fld_cl_mem)
        p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
        v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_cv_code_set_args(kernel_compute_cv_code, cv_fld_cl_mem, p_fld_cl_mem, v_fld_cl_mem, xstart_1 - 1, &
&xstop_1 - 1, ystart_1 - 1, ystop_1 - 1)
        z_fld_cl_mem = TRANSFER(z_fld%device_ptr, z_fld_cl_mem)
        p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
        u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
        v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_z_code_set_args(kernel_compute_z_code, z_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, p_fld%grid%dx, &
&p_fld%grid%dy, xstart_2 - 1, xstop_2 - 1, ystart_2 - 1, ystop_2 - 1)
        h_fld_cl_mem = TRANSFER(h_fld%device_ptr, h_fld_cl_mem)
        p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
        u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
        v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
        CALL compute_h_code_set_args(kernel_compute_h_code, h_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, xstart_3 - 1, &
&xstop_3 - 1, ystart_3 - 1, ystop_3 - 1)
        ! Write data to the device
        CALL u_fld%write_to_device
        CALL cv_fld%write_to_device
        CALL cu_fld%write_to_device
        CALL z_fld%write_to_device
        CALL p_fld%write_to_device
        CALL v_fld%write_to_device
        CALL h_fld%write_to_device
      END IF
      globalsize = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize = (/4, 1/)
      cu_fld_cl_mem = TRANSFER(cu_fld%device_ptr, cu_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      CALL compute_cu_code_set_args(kernel_compute_cu_code, cu_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, xstart - 1, xstop - 1, &
&ystart - 1, ystop - 1)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(1), kernel_compute_cu_code, 2, C_NULL_PTR, C_LOC(globalsize), C_LOC(localsize), 0, &
&C_NULL_PTR, C_NULL_PTR)
      globalsize = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize = (/4, 1/)
      cv_fld_cl_mem = TRANSFER(cv_fld%device_ptr, cv_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_cv_code_set_args(kernel_compute_cv_code, cv_fld_cl_mem, p_fld_cl_mem, v_fld_cl_mem, xstart_1 - 1, xstop_1 - 1, &
&ystart_1 - 1, ystop_1 - 1)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(2), kernel_compute_cv_code, 2, C_NULL_PTR, C_LOC(globalsize), C_LOC(localsize), 0, &
&C_NULL_PTR, C_NULL_PTR)
      globalsize = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize = (/4, 1/)
      z_fld_cl_mem = TRANSFER(z_fld%device_ptr, z_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_z_code_set_args(kernel_compute_z_code, z_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, p_fld%grid%dx, &
&p_fld%grid%dy, xstart_2 - 1, xstop_2 - 1, ystart_2 - 1, ystop_2 - 1)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(3), kernel_compute_z_code, 2, C_NULL_PTR, C_LOC(globalsize), C_LOC(localsize), 0, &
&C_NULL_PTR, C_NULL_PTR)
      globalsize = (/p_fld%grid%nx, p_fld%grid%ny/)
      localsize = (/4, 1/)
      h_fld_cl_mem = TRANSFER(h_fld%device_ptr, h_fld_cl_mem)
      p_fld_cl_mem = TRANSFER(p_fld%device_ptr, p_fld_cl_mem)
      u_fld_cl_mem = TRANSFER(u_fld%device_ptr, u_fld_cl_mem)
      v_fld_cl_mem = TRANSFER(v_fld%device_ptr, v_fld_cl_mem)
      CALL compute_h_code_set_args(kernel_compute_h_code, h_fld_cl_mem, p_fld_cl_mem, u_fld_cl_mem, v_fld_cl_mem, xstart_3 - 1, &
&xstop_3 - 1, ystart_3 - 1, ystop_3 - 1)
      ! Launch the kernel
      ierr = clEnqueueNDRangeKernel(cmd_queues(4), kernel_compute_h_code, 2, C_NULL_PTR, C_LOC(globalsize), C_LOC(localsize), 0, &
&C_NULL_PTR, C_NULL_PTR)
      ! Wait until all kernels have finished
      ierr = clFinish(cmd_queues(1))
      ierr = clFinish(cmd_queues(2))
      ierr = clFinish(cmd_queues(3))
      ierr = clFinish(cmd_queues(4))
      ! Unset the first time flag
      first_time = .false.

    END SUBROUTINE invoke_0
    SUBROUTINE psy_init()
      USE fortcl, ONLY: add_kernels, ocl_env_init
      CHARACTER(LEN=30) kernel_names(4)
      INTEGER :: ocl_device_num = 1
      LOGICAL, SAVE :: initialised = .FALSE.

      IF (.NOT.initialised) THEN
        initialised = .true.
        CALL ocl_env_init(4, ocl_device_num, .false., .false.)
        kernel_names(1) = 'compute_h_code'
        kernel_names(2) = 'compute_cu_code'
        kernel_names(3) = 'compute_cv_code'
        kernel_names(4) = 'compute_z_code'
        CALL add_kernels(4, kernel_names)
      END IF

    END SUBROUTINE psy_init
    SUBROUTINE initialise_grid_device_buffers(field)
      USE fortcl, ONLY: create_ronly_buffer
      USE field_mod
      TYPE(r2d_field), INTENT(INOUT), TARGET :: field
      INTEGER(KIND=c_size_t) size_in_bytes

      IF (.NOT.c_associated(field%grid%tmask_device)) THEN
        size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%grid%tmask(1,1))
        field%grid%tmask_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%tmask_device)
        size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%grid%area_t(1,1))
        field%grid%area_t_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%area_t_device)
        field%grid%area_u_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%area_u_device)
        field%grid%area_v_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%area_v_device)
        field%grid%dx_t_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dx_t_device)
        field%grid%dx_u_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dx_u_device)
        field%grid%dx_v_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dx_v_device)
        field%grid%dy_t_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dy_t_device)
        field%grid%dy_u_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dy_u_device)
        field%grid%dy_v_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%dy_v_device)
        field%grid%gphiu_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%gphiu_device)
        field%grid%gphiv_device = TRANSFER(create_ronly_buffer(size_in_bytes), field%grid%gphiv_device)
      END IF

    END SUBROUTINE initialise_grid_device_buffers
    SUBROUTINE write_grid_buffers(field)
      USE fortcl, ONLY: get_cmd_queues
      USE iso_c_binding, ONLY: c_intptr_t, c_size_t, c_sizeof
      USE clfortran
      USE ocl_utils_mod, ONLY: check_status
      TYPE(r2d_field), INTENT(INOUT), TARGET :: field
      INTEGER(KIND=c_size_t) size_in_bytes
      INTEGER(KIND=c_intptr_t), POINTER :: cmd_queues(:)
      INTEGER(KIND=c_intptr_t) cl_mem
      INTEGER ierr

      cmd_queues => get_cmd_queues()
      size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%grid%tmask(1,1))
      cl_mem = TRANSFER(field%grid%tmask_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%tmask),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer tmask', ierr)
      size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%grid%area_t(1,1))
      cl_mem = TRANSFER(field%grid%area_t_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%area_t),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer area_t_device', ierr)
      cl_mem = TRANSFER(field%grid%area_u_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%area_u),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer area_u_device', ierr)
      cl_mem = TRANSFER(field%grid%area_v_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%area_v),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer area_v_device', ierr)
      cl_mem = TRANSFER(field%grid%dx_u_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dx_u),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dx_u_device', ierr)
      cl_mem = TRANSFER(field%grid%dx_v_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dx_v),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dx_v_device', ierr)
      cl_mem = TRANSFER(field%grid%dx_t_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dx_t),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dx_t_device', ierr)
      cl_mem = TRANSFER(field%grid%dy_u_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dy_u),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dy_u_device', ierr)
      cl_mem = TRANSFER(field%grid%dy_v_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dy_v),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dy_v_device', ierr)
      cl_mem = TRANSFER(field%grid%dy_t_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%dy_t),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer dy_t_device', ierr)
      cl_mem = TRANSFER(field%grid%gphiu_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%gphiu),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer gphiu_device', ierr)
      cl_mem = TRANSFER(field%grid%gphiv_device, cl_mem)
      ierr = clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,0_8,size_in_bytes,c_loc(field%grid%gphiv),0,C_NULL_PTR,C_NULL_PTR)
      CALL check_status('clEnqueueWriteBuffer gphiv_device', ierr)

    END SUBROUTINE write_grid_buffers
    SUBROUTINE read_from_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_intptr_t, c_ptr, c_size_t, c_sizeof
      USE ocl_utils_mod, ONLY: check_status
      USE kind_params_mod, ONLY: go_wp
      USE clfortran
      USE fortcl, ONLY: get_cmd_queues
      TYPE(c_ptr), intent(in) :: from
      REAL(KIND=go_wp), INTENT(INOUT), DIMENSION(:, :), TARGET :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking
      INTEGER(KIND=c_size_t) size_in_bytes
      INTEGER(KIND=c_size_t) offset_in_bytes
      INTEGER(KIND=c_intptr_t) cl_mem
      INTEGER(KIND=c_intptr_t), POINTER :: cmd_queues(:)
      INTEGER ierr
      INTEGER i

      cl_mem = TRANSFER(from, cl_mem)
      cmd_queues => get_cmd_queues()
      IF (nx < SIZE(to, 1) / 2) THEN
        DO i = starty, starty + ny, 1
          size_in_bytes = INT(nx, 8) * c_sizeof(to(1,1))
          offset_in_bytes = INT(SIZE(to, 1) * (i - 1) + (startx - 1)) * c_sizeof(to(1,1))
          ierr = &
&clenqueuereadbuffer(cmd_queues(1),cl_mem,CL_FALSE,offset_in_bytes,size_in_bytes,c_loc(to(startx,i)),0,C_NULL_PTR,C_NULL_PTR)
          CALL check_status('clEnqueueReadBuffer', ierr)
        END DO
        IF (blocking) THEN
          CALL check_status('clFinish on read', clfinish(cmd_queues(1)))
        END IF
      ELSE
        size_in_bytes = INT(SIZE(to, 1) * ny, 8) * c_sizeof(to(1,1))
        offset_in_bytes = INT(SIZE(to, 1) * (starty - 1), 8) * c_sizeof(to(1,1))
        ierr = &
&clenqueuereadbuffer(cmd_queues(1),cl_mem,CL_TRUE,offset_in_bytes,size_in_bytes,c_loc(to(1,starty)),0,C_NULL_PTR,C_NULL_PTR)
        CALL check_status('clEnqueueReadBuffer', ierr)
      END IF

    END SUBROUTINE read_from_device
    SUBROUTINE write_to_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_intptr_t, c_ptr, c_size_t, c_sizeof
      USE ocl_utils_mod, ONLY: check_status
      USE kind_params_mod, ONLY: go_wp
      USE clfortran
      USE fortcl, ONLY: get_cmd_queues
      REAL(KIND=go_wp), INTENT(IN), DIMENSION(:, :), TARGET :: from
      TYPE(c_ptr), intent(in) :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking
      INTEGER(KIND=c_intptr_t) cl_mem
      INTEGER(KIND=c_size_t) size_in_bytes
      INTEGER(KIND=c_size_t) offset_in_bytes
      INTEGER(KIND=c_intptr_t), POINTER :: cmd_queues(:)
      INTEGER ierr
      INTEGER i

      cl_mem = TRANSFER(to, cl_mem)
      cmd_queues => get_cmd_queues()
      IF (nx < SIZE(from, 1) / 2) THEN
        DO i = starty, starty + ny, 1
          size_in_bytes = INT(nx, 8) * c_sizeof(from(1,1))
          offset_in_bytes = INT(SIZE(from, 1) * (i - 1) + (startx - 1)) * c_sizeof(from(1,1))
          ierr = &
&clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_FALSE,offset_in_bytes,size_in_bytes,c_loc(from(startx,i)),0,C_NULL_PTR,C_NULL_PTR)
          CALL check_status('clEnqueueWriteBuffer', ierr)
        END DO
        IF (blocking) THEN
          CALL check_status('clFinish on write', clfinish(cmd_queues(1)))
        END IF
      ELSE
        size_in_bytes = INT(SIZE(from, 1) * ny, 8) * c_sizeof(from(1,1))
        offset_in_bytes = INT(SIZE(from, 1) * (starty - 1)) * c_sizeof(from(1,1))
        ierr = &
&clenqueuewritebuffer(cmd_queues(1),cl_mem,CL_TRUE,offset_in_bytes,size_in_bytes,c_loc(from(1,starty)),0,C_NULL_PTR,C_NULL_PTR)
        CALL check_status('clEnqueueWriteBuffer', ierr)
      END IF

    END SUBROUTINE write_to_device
    SUBROUTINE initialise_device_buffer(field)
      USE fortcl, ONLY: create_rw_buffer
      USE field_mod
      TYPE(r2d_field), INTENT(INOUT), TARGET :: field
      INTEGER(KIND=c_size_t) size_in_bytes

      IF (.NOT.field%data_on_device) THEN
        size_in_bytes = INT(field%grid%nx * field%grid%ny, 8) * c_sizeof(field%data(1,1))
        field%device_ptr = TRANSFER(create_rw_buffer(size_in_bytes), field%device_ptr)
        field%data_on_device = .true.
        field%read_from_device_f => read_from_device
        field%write_to_device_f => write_to_device
      END IF

    END SUBROUTINE initialise_device_buffer
    SUBROUTINE compute_cu_code_set_args(kernel_obj, cu_fld, p_fld, u_fld, xstart, xstop, ystart, ystop)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: C_LOC, C_SIZEOF, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), TARGET :: kernel_obj
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: cu_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: p_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: u_fld
      INTEGER, INTENT(IN), TARGET :: xstart
      INTEGER, INTENT(IN), TARGET :: xstop
      INTEGER, INTENT(IN), TARGET :: ystart
      INTEGER, INTENT(IN), TARGET :: ystop
      INTEGER ierr

      ! Set the arguments for the compute_cu_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(cu_fld), C_LOC(cu_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(xstart), C_LOC(xstart))
      CALL check_status('clSetKernelArg: arg 3 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstop), C_LOC(xstop))
      CALL check_status('clSetKernelArg: arg 4 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(ystart), C_LOC(ystart))
      CALL check_status('clSetKernelArg: arg 5 of compute_cu_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystop), C_LOC(ystop))
      CALL check_status('clSetKernelArg: arg 6 of compute_cu_code', ierr)

    END SUBROUTINE compute_cu_code_set_args
    SUBROUTINE compute_cv_code_set_args(kernel_obj, cv_fld, p_fld, v_fld, xstart_1, xstop_1, ystart_1, ystop_1)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: C_LOC, C_SIZEOF, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), TARGET :: kernel_obj
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: cv_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: p_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: v_fld
      INTEGER, INTENT(IN), TARGET :: xstart_1
      INTEGER, INTENT(IN), TARGET :: xstop_1
      INTEGER, INTENT(IN), TARGET :: ystart_1
      INTEGER, INTENT(IN), TARGET :: ystop_1
      INTEGER ierr

      ! Set the arguments for the compute_cv_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(cv_fld), C_LOC(cv_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(xstart_1), C_LOC(xstart_1))
      CALL check_status('clSetKernelArg: arg 3 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstop_1), C_LOC(xstop_1))
      CALL check_status('clSetKernelArg: arg 4 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(ystart_1), C_LOC(ystart_1))
      CALL check_status('clSetKernelArg: arg 5 of compute_cv_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystop_1), C_LOC(ystop_1))
      CALL check_status('clSetKernelArg: arg 6 of compute_cv_code', ierr)

    END SUBROUTINE compute_cv_code_set_args
    SUBROUTINE compute_z_code_set_args(kernel_obj, z_fld, p_fld, u_fld, v_fld, dx, dy, xstart_2, xstop_2, ystart_2, ystop_2)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: C_LOC, C_SIZEOF, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), TARGET :: kernel_obj
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: z_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: p_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: u_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: v_fld
      REAL(KIND=go_wp), INTENT(IN), TARGET :: dx
      REAL(KIND=go_wp), INTENT(IN), TARGET :: dy
      INTEGER, INTENT(IN), TARGET :: xstart_2
      INTEGER, INTENT(IN), TARGET :: xstop_2
      INTEGER, INTENT(IN), TARGET :: ystart_2
      INTEGER, INTENT(IN), TARGET :: ystop_2
      INTEGER ierr

      ! Set the arguments for the compute_z_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(z_fld), C_LOC(z_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 3 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(dx), C_LOC(dx))
      CALL check_status('clSetKernelArg: arg 4 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(dy), C_LOC(dy))
      CALL check_status('clSetKernelArg: arg 5 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(xstart_2), C_LOC(xstart_2))
      CALL check_status('clSetKernelArg: arg 6 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 7, C_SIZEOF(xstop_2), C_LOC(xstop_2))
      CALL check_status('clSetKernelArg: arg 7 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 8, C_SIZEOF(ystart_2), C_LOC(ystart_2))
      CALL check_status('clSetKernelArg: arg 8 of compute_z_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 9, C_SIZEOF(ystop_2), C_LOC(ystop_2))
      CALL check_status('clSetKernelArg: arg 9 of compute_z_code', ierr)

    END SUBROUTINE compute_z_code_set_args
    SUBROUTINE compute_h_code_set_args(kernel_obj, h_fld, p_fld, u_fld, v_fld, xstart_3, xstop_3, ystart_3, ystop_3)
      USE clfortran, ONLY: clSetKernelArg
      USE iso_c_binding, ONLY: C_LOC, C_SIZEOF, c_intptr_t
      USE ocl_utils_mod, ONLY: check_status
      INTEGER(KIND=c_intptr_t), TARGET :: kernel_obj
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: h_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: p_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: u_fld
      INTEGER(KIND=c_intptr_t), INTENT(IN), TARGET :: v_fld
      INTEGER, INTENT(IN), TARGET :: xstart_3
      INTEGER, INTENT(IN), TARGET :: xstop_3
      INTEGER, INTENT(IN), TARGET :: ystart_3
      INTEGER, INTENT(IN), TARGET :: ystop_3
      INTEGER ierr

      ! Set the arguments for the compute_h_code OpenCL Kernel
      ierr = clSetKernelArg(kernel_obj, 0, C_SIZEOF(h_fld), C_LOC(h_fld))
      CALL check_status('clSetKernelArg: arg 0 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 1, C_SIZEOF(p_fld), C_LOC(p_fld))
      CALL check_status('clSetKernelArg: arg 1 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 2, C_SIZEOF(u_fld), C_LOC(u_fld))
      CALL check_status('clSetKernelArg: arg 2 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 3, C_SIZEOF(v_fld), C_LOC(v_fld))
      CALL check_status('clSetKernelArg: arg 3 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 4, C_SIZEOF(xstart_3), C_LOC(xstart_3))
      CALL check_status('clSetKernelArg: arg 4 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 5, C_SIZEOF(xstop_3), C_LOC(xstop_3))
      CALL check_status('clSetKernelArg: arg 5 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 6, C_SIZEOF(ystart_3), C_LOC(ystart_3))
      CALL check_status('clSetKernelArg: arg 6 of compute_h_code', ierr)
      ierr = clSetKernelArg(kernel_obj, 7, C_SIZEOF(ystop_3), C_LOC(ystop_3))
      CALL check_status('clSetKernelArg: arg 7 of compute_h_code', ierr)

    END SUBROUTINE compute_h_code_set_args
  END MODULE psy_simple