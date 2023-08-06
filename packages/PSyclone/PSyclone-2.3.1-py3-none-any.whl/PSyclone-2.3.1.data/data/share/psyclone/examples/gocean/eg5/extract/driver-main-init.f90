program main_init
  use read_kernel_data_mod, only : ReadKernelDataType
  use init_field_mod, only : init_field_code
  integer :: i
  integer :: j
  integer :: a_fld_whole_ystart
  integer :: a_fld_whole_ystop
  integer :: a_fld_whole_xstart
  integer :: a_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: a_fld
  integer :: b_fld_whole_ystart
  integer :: b_fld_whole_ystop
  integer :: b_fld_whole_xstart
  integer :: b_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: b_fld
  integer :: c_fld_whole_ystart
  integer :: c_fld_whole_ystop
  integer :: c_fld_whole_xstart
  integer :: c_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: c_fld
  integer :: d_fld_whole_ystart
  integer :: d_fld_whole_ystop
  integer :: d_fld_whole_xstart
  integer :: d_fld_whole_xstop
  real*8, allocatable, dimension(:,:) :: d_fld
  type(ReadKernelDataType) :: extract_psy_data
  real*8, allocatable, dimension(:,:) :: a_fld_post
  real*8, allocatable, dimension(:,:) :: b_fld_post
  real*8, allocatable, dimension(:,:) :: c_fld_post
  real*8, allocatable, dimension(:,:) :: d_fld_post
  integer :: i_post
  integer :: j_post

  call extract_psy_data%OpenRead('main', 'init')
  call extract_psy_data%ReadVariable('a_fld_post', a_fld_post)
  ALLOCATE(a_fld(SIZE(a_fld_post, 1), SIZE(a_fld_post, 2)))
  a_fld = 0
  call extract_psy_data%ReadVariable('a_fld%whole%xstart', a_fld_whole_xstart)
  call extract_psy_data%ReadVariable('a_fld%whole%xstop', a_fld_whole_xstop)
  call extract_psy_data%ReadVariable('a_fld%whole%ystart', a_fld_whole_ystart)
  call extract_psy_data%ReadVariable('a_fld%whole%ystop', a_fld_whole_ystop)
  call extract_psy_data%ReadVariable('b_fld_post', b_fld_post)
  ALLOCATE(b_fld(SIZE(b_fld_post, 1), SIZE(b_fld_post, 2)))
  b_fld = 0
  call extract_psy_data%ReadVariable('b_fld%whole%xstart', b_fld_whole_xstart)
  call extract_psy_data%ReadVariable('b_fld%whole%xstop', b_fld_whole_xstop)
  call extract_psy_data%ReadVariable('b_fld%whole%ystart', b_fld_whole_ystart)
  call extract_psy_data%ReadVariable('b_fld%whole%ystop', b_fld_whole_ystop)
  call extract_psy_data%ReadVariable('c_fld_post', c_fld_post)
  ALLOCATE(c_fld(SIZE(c_fld_post, 1), SIZE(c_fld_post, 2)))
  c_fld = 0
  call extract_psy_data%ReadVariable('c_fld%whole%xstart', c_fld_whole_xstart)
  call extract_psy_data%ReadVariable('c_fld%whole%xstop', c_fld_whole_xstop)
  call extract_psy_data%ReadVariable('c_fld%whole%ystart', c_fld_whole_ystart)
  call extract_psy_data%ReadVariable('c_fld%whole%ystop', c_fld_whole_ystop)
  call extract_psy_data%ReadVariable('d_fld_post', d_fld_post)
  ALLOCATE(d_fld(SIZE(d_fld_post, 1), SIZE(d_fld_post, 2)))
  d_fld = 0
  call extract_psy_data%ReadVariable('d_fld%whole%xstart', d_fld_whole_xstart)
  call extract_psy_data%ReadVariable('d_fld%whole%xstop', d_fld_whole_xstop)
  call extract_psy_data%ReadVariable('d_fld%whole%ystart', d_fld_whole_ystart)
  call extract_psy_data%ReadVariable('d_fld%whole%ystop', d_fld_whole_ystop)
  call extract_psy_data%ReadVariable('i_post', i_post)
  i = 0
  call extract_psy_data%ReadVariable('j_post', j_post)
  j = 0
  do j = a_fld_whole_ystart, a_fld_whole_ystop, 1
    do i = a_fld_whole_xstart, a_fld_whole_xstop, 1
      call init_field_code(i, j, a_fld, 1.0)
    enddo
  enddo
  do j = b_fld_whole_ystart, b_fld_whole_ystop, 1
    do i = b_fld_whole_xstart, b_fld_whole_xstop, 1
      call init_field_code(i, j, b_fld, 2.0)
    enddo
  enddo
  do j = c_fld_whole_ystart, c_fld_whole_ystop, 1
    do i = c_fld_whole_xstart, c_fld_whole_xstop, 1
      call init_field_code(i, j, c_fld, 3.0)
    enddo
  enddo
  do j = d_fld_whole_ystart, d_fld_whole_ystop, 1
    do i = d_fld_whole_xstart, d_fld_whole_xstop, 1
      call init_field_code(i, j, d_fld, 4.0)
    enddo
  enddo
  if (ALL(a_fld - a_fld_post == 0.0)) then
    PRINT *, "a_fld correct"
  else
    PRINT *, "a_fld incorrect. Values are:"
    PRINT *, a_fld
    PRINT *, "a_fld values should be:"
    PRINT *, a_fld_post
  end if
  if (ALL(b_fld - b_fld_post == 0.0)) then
    PRINT *, "b_fld correct"
  else
    PRINT *, "b_fld incorrect. Values are:"
    PRINT *, b_fld
    PRINT *, "b_fld values should be:"
    PRINT *, b_fld_post
  end if
  if (ALL(c_fld - c_fld_post == 0.0)) then
    PRINT *, "c_fld correct"
  else
    PRINT *, "c_fld incorrect. Values are:"
    PRINT *, c_fld
    PRINT *, "c_fld values should be:"
    PRINT *, c_fld_post
  end if
  if (ALL(d_fld - d_fld_post == 0.0)) then
    PRINT *, "d_fld correct"
  else
    PRINT *, "d_fld incorrect. Values are:"
    PRINT *, d_fld
    PRINT *, "d_fld values should be:"
    PRINT *, d_fld_post
  end if
  if (i == i_post) then
    PRINT *, "i correct"
  else
    PRINT *, "i incorrect. Values are:"
    PRINT *, i
    PRINT *, "i values should be:"
    PRINT *, i_post
  end if
  if (j == j_post) then
    PRINT *, "j correct"
  else
    PRINT *, "j incorrect. Values are:"
    PRINT *, j
    PRINT *, "j values should be:"
    PRINT *, j_post
  end if

end program main_init
