  MODULE main
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE main_code()
      USE init_field_mod, ONLY: init_field_code
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      IMPLICIT NONE
      INTEGER j
      INTEGER i
      REAL(KIND=8), allocatable, dimension(:,:) :: j_post
      REAL(KIND=8), allocatable, dimension(:,:) :: j
      REAL(KIND=8), allocatable, dimension(:,:) :: i_post
      REAL(KIND=8), allocatable, dimension(:,:) :: i
      REAL(KIND=8), allocatable, dimension(:,:) :: d_fld_post
      REAL(KIND=8), allocatable, dimension(:,:) :: d_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: c_fld_post
      REAL(KIND=8), allocatable, dimension(:,:) :: c_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: b_fld_post
      REAL(KIND=8), allocatable, dimension(:,:) :: b_fld
      REAL(KIND=8), allocatable, dimension(:,:) :: a_fld_post
      REAL(KIND=8), allocatable, dimension(:,:) :: a_fld
      TYPE(extract_PSyDataType) extract_psy_data
      CALL extract_psy_data%OpenRead("main", "init")
      CALL extract_psy_data%ReadVariable("a_fld_post", a_fld_post)
      ALLOCATE (a_fld, mold=a_fld_post)
      a_fld = 0.0d0
      CALL extract_psy_data%ReadVariable("b_fld_post", b_fld_post)
      ALLOCATE (b_fld, mold=b_fld_post)
      b_fld = 0.0d0
      CALL extract_psy_data%ReadVariable("c_fld_post", c_fld_post)
      ALLOCATE (c_fld, mold=c_fld_post)
      c_fld = 0.0d0
      CALL extract_psy_data%ReadVariable("d_fld_post", d_fld_post)
      ALLOCATE (d_fld, mold=d_fld_post)
      d_fld = 0.0d0
      CALL extract_psy_data%ReadVariable("i_post", i_post)
      ALLOCATE (i, mold=i_post)
      i = 0.0d0
      CALL extract_psy_data%ReadVariable("j_post", j_post)
      ALLOCATE (j, mold=j_post)
      j = 0.0d0
      !
      ! RegionStart
      DO j=ystart,ystop
        DO i=xstart,xstop
          CALL init_field_code(i, j, a_fld, 1.0)
        END DO
      END DO
      DO j=ystart,ystop
        DO i=xstart,xstop
          CALL init_field_code(i, j, b_fld, 2.0)
        END DO
      END DO
      DO j=ystart,ystop
        DO i=xstart,xstop
          CALL init_field_code(i, j, c_fld, 3.0)
        END DO
      END DO
      DO j=ystart,ystop
        DO i=xstart,xstop
          CALL init_field_code(i, j, d_fld, 4.0)
        END DO
      END DO
      ! RegionEnd
      !
      ! Check a_fld
      ! Check b_fld
      ! Check c_fld
      ! Check d_fld
      ! Check i
      ! Check j
    END SUBROUTINE main_code
  END MODULE main