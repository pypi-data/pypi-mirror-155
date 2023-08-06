! ================================================== !
! THIS FILE IS CREATED FROM THE JINJA TEMPLATE FILE  !
! DO NOT MODIFY DIRECTLY                             !
! ================================================== !





! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2020-2021, Science and Technology Facilities Council.
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author J. Henrichs, Bureau of Meteorology
! Modified I. Kavcic, Met Office

!> This module implements a PSyData-based verification that floating point
!! input and output parameters are not NAN and not infinite.
!!

module nan_test_base_mod

    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr => Error_Unit
    use psy_data_base_mod, only : PSyDataBaseType, &
        nan_test_PSyDataShutdown, &
        nan_test_PSyDataInit, is_enabled, &
        nan_test_PSyDataStart, nan_test_PSyDataStop

    implicit none

    type, extends(PSyDataBaseType), public :: NANTestBaseType

    contains

        ! The various procedures used

        procedure :: ProvideScalarInt
        procedure :: ProvideArray2dInt
        procedure :: ProvideScalarReal
        procedure :: ProvideArray2dReal
        procedure :: ProvideScalarDouble
        procedure :: ProvideArray2dDouble

        !> The generic interface for providing the value of variables:
        generic, public :: ProvideVariable => &
            ProvideScalarInt, &
            ProvideArray2dInt, &
            ProvideScalarReal, &
            ProvideArray2dReal, &
            ProvideScalarDouble, &
            ProvideArray2dDouble

    end type NANTestBaseType

contains

    ! =========================================================================
    ! Jinja created code.
    ! =========================================================================


    ! =========================================================================
    ! Implementation for all integer(kind=int32) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> This subroutine checks if a floating point value is NAN or infinite
    !! using the IEEE_IS_FINIT function (and does nothing for integer types).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarInt(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in)                      :: name
        integer(kind=int32), intent(in)                          :: value

        ! Variables of type integer(kind=int32) do not have NANs
        ! So nothing to do here.

        call this%PSyDataBaseType%ProvideScalarInt(name, value)

    end subroutine ProvideScalarInt



    ! -------------------------------------------------------------------------
    !> This method checks if an array contains NAN or infinite IEEE values (it
    !! does nothing in case that the array is an integer type).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dInt(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        integer(kind=int32), dimension(:,:), intent(in) :: value

        ! Variables of type integer(kind=int32) do not have NANs
        ! So nothing to do here.

        call this%PSyDataBaseType%ProvideArray2dInt(name, value)

    end subroutine ProvideArray2dInt


    ! =========================================================================
    ! Implementation for all real(kind=real32) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> This subroutine checks if a floating point value is NAN or infinite
    !! using the IEEE_IS_FINIT function (and does nothing for integer types).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarReal(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in)                      :: name
        real(kind=real32), intent(in)                          :: value

        if (.not. is_enabled) return

        if (IEEE_SUPPORT_DATATYPE(value)) then
            if (.not. IEEE_IS_FINITE(value)) then
                write(stderr, '(8G0)') "PSyData: Variable ", name," has invalid value ", &
                                 value, " in module '", trim(this%module_name), &
                                 "' region '", trim(this%region_name),"'."
            endif
        endif

        call this%PSyDataBaseType%ProvideScalarReal(name, value)

    end subroutine ProvideScalarReal



    ! -------------------------------------------------------------------------
    !> This method checks if an array contains NAN or infinite IEEE values (it
    !! does nothing in case that the array is an integer type).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dReal(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real32), dimension(:,:), intent(in) :: value

        integer :: i1, i2

        if (.not. is_enabled) return
        if (IEEE_SUPPORT_DATATYPE(value)) then
            do i2=1, size(value, 2)
               do i1=1, size(value, 1)
                  if (.not. IEEE_IS_FINITE(value(i1, i2))) then
                      write(stderr, '(5G0,2(G0,X),5G0)') "PSyData: Variable ", &
                                       name," has the invalid value ", &
                                       value(i1, i2), " at index/indices ", i1, i2, &
                                       "in module '", trim(this%module_name), &
                                       "' region '", trim(this%region_name),"'."
                  endif
               enddo
            enddo
        endif

        call this%PSyDataBaseType%ProvideArray2dReal(name, value)

    end subroutine ProvideArray2dReal


    ! =========================================================================
    ! Implementation for all real(kind=real64) types
    ! =========================================================================
    ! -------------------------------------------------------------------------
    !> This subroutine checks if a floating point value is NAN or infinite
    !! using the IEEE_IS_FINIT function (and does nothing for integer types).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideScalarDouble(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in)                      :: name
        real(kind=real64), intent(in)                          :: value

        if (.not. is_enabled) return

        if (IEEE_SUPPORT_DATATYPE(value)) then
            if (.not. IEEE_IS_FINITE(value)) then
                write(stderr, '(8G0)') "PSyData: Variable ", name," has invalid value ", &
                                 value, " in module '", trim(this%module_name), &
                                 "' region '", trim(this%region_name),"'."
            endif
        endif

        call this%PSyDataBaseType%ProvideScalarDouble(name, value)

    end subroutine ProvideScalarDouble



    ! -------------------------------------------------------------------------
    !> This method checks if an array contains NAN or infinite IEEE values (it
    !! does nothing in case that the array is an integer type).
    !! @param[in,out] this The instance of the NANTestBaseType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideArray2dDouble(this, name, value)

        use, intrinsic :: ieee_arithmetic

        implicit none

        class(NANTestBaseType), intent(inout), target :: this
        character(*), intent(in) :: name
        real(kind=real64), dimension(:,:), intent(in) :: value

        integer :: i1, i2

        if (.not. is_enabled) return
        if (IEEE_SUPPORT_DATATYPE(value)) then
            do i2=1, size(value, 2)
               do i1=1, size(value, 1)
                  if (.not. IEEE_IS_FINITE(value(i1, i2))) then
                      write(stderr, '(5G0,2(G0,X),5G0)') "PSyData: Variable ", &
                                       name," has the invalid value ", &
                                       value(i1, i2), " at index/indices ", i1, i2, &
                                       "in module '", trim(this%module_name), &
                                       "' region '", trim(this%region_name),"'."
                  endif
               enddo
            enddo
        endif

        call this%PSyDataBaseType%ProvideArray2dDouble(name, value)

    end subroutine ProvideArray2dDouble


    ! -------------------------------------------------------------------------

end module nan_test_base_mod
