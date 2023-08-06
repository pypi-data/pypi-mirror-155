  MODULE main
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE main_code()
      USE update_field_mod, ONLY: update_field_code
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      IMPLICIT NONE
      INTEGER j
      INTEGER i
      REAL(KIND=8), allocatable, dimension(:,:) :: z
      REAL(KIND=8), allocatable, dimension(:,:) :: y_post
      REAL(KIND=8), allocatable, dimension(:,:) :: y
      REAL(KIND=8), allocatable, dimension(:,:) :: x_post
      REAL(KIND=8), allocatable, dimension(:,:) :: x
      REAL(KIND=8), allocatable, dimension(:,:) :: j_post
      REAL(KIND=8), allocatable, dimension(:,:) :: j
      REAL(KIND=8), allocatable, dimension(:,:) :: i_post
      REAL(KIND=8), allocatable, dimension(:,:) :: i
      REAL(KIND=8), allocatable, dimension(:,:) :: d_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: c_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: dx
      REAL(KIND=8), allocatable, dimension(:,:) :: b_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: a_fld_post
      REAL(KIND=8), allocatable, dimension(:,:) :: a_fld
      TYPE(extract_PSyDataType) extract_psy_data
      CALL extract_psy_data%OpenRead("main", "update")
      CALL extract_psy_data%ReadVariable("a_fld", a_fld)
      CALL extract_psy_data%ReadVariable("a_fld_post", a_fld_post)
      CALL extract_psy_data%ReadVariable("b_fld", b_fld)
      CALL extract_psy_data%ReadVariable("b_fld%grid%dx", dx)
      CALL extract_psy_data%ReadVariable("c_fld", c_fld)
      CALL extract_psy_data%ReadVariable("d_fld", d_fld)
      CALL extract_psy_data%ReadVariable("i_post", i_post)
      ALLOCATE (i, mold=i_post)
      i = 0.0d0
      CALL extract_psy_data%ReadVariable("j_post", j_post)
      ALLOCATE (j, mold=j_post)
      j = 0.0d0
      CALL extract_psy_data%ReadVariable("x", x)
      CALL extract_psy_data%ReadVariable("x_post", x_post)
      CALL extract_psy_data%ReadVariable("y_post", y_post)
      ALLOCATE (y, mold=y_post)
      y = 0.0d0
      CALL extract_psy_data%ReadVariable("z", z)
      !
      ! RegionStart
      DO j=ystart,ystop
        DO i=xstart,xstop
          CALL update_field_code(i, j, a_fld, b_fld, c_fld, d_fld, x, y, z, dx)
        END DO
      END DO
      ! RegionEnd
      !
      ! Check a_fld
      ! Check i
      ! Check j
      ! Check x
      ! Check y
    END SUBROUTINE main_code
  END MODULE main