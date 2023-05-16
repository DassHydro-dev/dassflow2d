PROGRAM gen_obs

   implicit none

   !===================================================================================================================!
   !  SW model parameters
   !===================================================================================================================!

   real(8), parameter  ::  slope         =  0.0025_8
   real(8), parameter  ::  manning_coef  =  0.05_8

   !===================================================================================================================!
   !  Parameters defining problem
   !===================================================================================================================!

   real(8), parameter  ::  h_n  =  1._8

   integer(4), parameter  ::  nx  =  100
   integer(4), parameter  ::  ny  =  10

   real(8), parameter  ::  lx = 1000.
   real(8), parameter  ::  ly = 100.

   integer(4), parameter  ::  nx_obs  =  2
   integer(4), parameter  ::  ny_obs  =  1

   real(8), parameter  ::  dt_obs  =  60.

   real(8), parameter  ::  xmin_obs  =  400.
   real(8), parameter  ::  xmax_obs  =  600.

   real(8), parameter  ::  ymin_obs  =  50.
   real(8), parameter  ::  ymax_obs  =  50.

   integer(4), parameter  ::  nb_rat  =  100

   real(8), dimension(nx_obs)  ::  x_obs
   real(8), dimension(ny_obs)  ::  y_obs

   integer(4)  ::  i , j , k

   real(8)  ::  dx , dy

   real(8), parameter  ::  pi  =  3.14159265358979_8

   !===================================================================================================================!
   !
   !===================================================================================================================!

   open(10,file='channel.geo',status='replace',form='formatted')

   write(10,'(A)') '# Simple channel mesh'
   write(10,'(2I8,E15.7)')  nx * ny , (nx-1)*(ny-1) , 0._8

   write(10,'(A)') '# Nodes'

   dx = lx / real( nx - 1 , 8 )
   dy = ly / real( ny - 1 , 8 )

   k = 0

   do j = 1,ny
      do i = 1,nx

         k = k + 1

         write(10,'(I8,3E15.7)') k , &
                                 ( i - 1 ) * dx , &
                                 ( j - 1 ) * dy , &
                                 0._8

      end do
   end do

   write(10,'(A)') '# Cells'

   k = 0

   do j = 1,ny-1
      do i = 1,nx-1

         k = k + 1

         write(10,'(6I8,E15.7)') k , &
                                 i + ( j - 1 ) * nx , &
                                 i + ( j - 1 ) * nx + 1 , &
                                 i + ( j - 1 ) * nx + nx + 1 , &
                                 i + ( j - 1 ) * nx + nx , &
                                 1 , &
                                 bathy_user( 0.5_8 * dx + ( i - 1 ) * dx , &
                                             0.5_8 * dy + ( j - 1 ) * dy )

      end do
   end do

   write(10,'(A)') '# Boundary conditions'

   write(10,'(A,2I8)') 'INLET' , ny - 1 , 0

   do j = 1,ny-1

      write(10,'(3I8,E15.7)') 1 + ( j - 1 ) * ( nx - 1 ) , 4 , 1 , &
                              bathy_user( - 0.5_8 * dx , 0.5_8 * dy + ( j - 1 ) * dy )

   end do

   write(10,'(A,2I8)') 'OUTLET' , ny - 1 , 0

   do j = 1,ny-1

      write(10,'(3I8,E15.7)') j * ( nx - 1 ) , 2 , 2 , &
                              bathy_user( lx + 0.5_8 * dx , 0.5_8 * dy + ( j - 1 ) * dy )

   end do

   close(10)

   !===================================================================================================================!
   !
   !===================================================================================================================!

   open(10,file='bc.txt',status='replace',form='formatted')

   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!  Number of boundary conditions'
   write(10,'(A)') '!=================================================================================================!'

   write(10,'(I1)') 2

   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!   List of boundary conditions'
   write(10,'(A)') '!=================================================================================================!'

   write(10,'(I1,A,A)') 1 , char(9)//'discharg1' , char(9)//'file'
   write(10,'(I1,A,A)') 2 , char(9)//'ratcurve'  , char(9)//'file'

   close(10)

   !===================================================================================================================!
   !
   !===================================================================================================================!

   dx = ( xmax_obs - xmin_obs ) / real( nx_obs - 1 , 8 )
   dy = ( ymax_obs - ymin_obs ) / real( ny_obs - 1 , 8 )

   do i = 1,nx_obs

      x_obs(i)  =  xmin_obs + dx * ( i - 1 )

   end do

   do j = 1,ny_obs

      y_obs(j)  =  ymin_obs + dy * ( j - 1 )

   end do

   open(10,file='obs.txt',status='replace',form='formatted')

   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '! File Defining Points and/or Lines to output result in files at a prescribed temporal frequency'
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)')
   write(10,'(A,I6)')  'stations' , nx_obs * ny_obs
   write(10,'(A)')

   do j = 1,ny_obs
      do i = 1,nx_obs

         write(10,'(3E15.7)') x_obs(i) , y_obs(j) , dt_obs

      end do
   end do

   close(10)

   !===================================================================================================================!
   !
   !===================================================================================================================!

   open(10,file='rating_curve.txt',status='replace',form='formatted')

   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!  Number of ratcurve'
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(I1)') 1
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!  Number of ratcurve'
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(I4,E22.15)') nb_rat+1 , 0.

   do i = 0,nb_rat

      write(10,'(3E15.7)') i*2./nb_rat , 100._8 * (i*2./nb_rat)**(5./3.)

   end do

   close(10)

   !===================================================================================================================!
   !
   !===================================================================================================================!

   open(10,file='land_uses.txt',status='replace',form='formatted')

   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!  Number of Land Uses'
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(I1)') 1
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(A)') '!  List of Land Uses'
   write(10,'(A)') '!=================================================================================================!'
   write(10,'(I4,E22.15)') 1 , manning_coef

   close(10)


CONTAINS

   !===================================================================================================================!
   !
   !===================================================================================================================!


!~    real(8) FUNCTION bathy_user( x , y )

!~       implicit none

!~       real(8), intent(in)  ::  x , y

!~       bathy_user  =  slope * ( lx - x )

!~       if ( x >= 0.25 * lx .and. x <= 0.75_rp * lx ) then

!~          bathy_user  =  slope * ( lx - x )  +  0.5_rp * h_n * sin( 4.0_rp * pi * x / lx ) * &
!~                                                               sin( 1.0_rp * pi * y / ly )

!~       end if

!~    END FUNCTION bathy_user

	real(rp) FUNCTION bathy_user( x , y )

      implicit none

		real(rp), intent(in)  ::  x , y

      integer(ip)  ::  ite

      real(rp)  ::  xx , sum_b

      bathy_user  =  0.5 * q**2 / g * ( 1 / h_ex(lx,y)**2 - 1 / h_ex(x,y)**2 ) + h_ex(lx,y) - h_ex(x,y)

      bathy_user  =  bathy_user - manning_coef**2 * q**2 * FUNSimpson( h_ex_p , lx , x , int( 200 * abs( lx - x ) / dx ) )

	END FUNCTION bathy_user
!======================================================================================================================!
!  Exact water depth / derivate
!======================================================================================================================!

	real(rp) FUNCTION h_ex( x , y )

      implicit none

		real(rp), intent(in)  ::  x , y

      h_ex  =  (4._rp/g)**d1p3 * ( one + demi * exp( - 16._rp * ( x / lx - demi )**2 ) )

	END FUNCTION h_ex

	real(rp) FUNCTION h_ex_p( x )

      implicit none

		real(rp), intent(in)  ::  x

      h_ex_p  =  one / h_ex(x,0._rp)**d10p3

	END FUNCTION h_ex_p

	real(rp) FUNCTION dh_ex( x , y )

      implicit none

		real(rp), intent(in)  ::  x , y

      dh_ex  =  - 16._rp / lx * (4._rp/g)**d1p3 * ( x / lx - demi ) * exp( - 16._rp * ( x / lx - demi )**2 )

	END FUNCTION dh_ex
	
	
	
   
!> \brief  Numerical integration using Simpson rule
!! \details  USED for macdonnald's benchmark with perturbated topography
real(rp) FUNCTION FUNSimpson( f , xmin , xmax , nbp )

  USE m_common

  implicit none
  
  real(rp)  ::  f ; external f
!~ 	real(rp), external  ::  f

  real(rp), intent(in)  ::  xmin , xmax

  integer(ip), intent(in)  ::  nbp

  real(rp)  ::  step , sum_s , x_stage

  integer(ip)  ::  i_stage , nb_stage

  if ( modulo( nbp , 2 ) == 0 ) then

	 nb_stage = nbp

  else

	 nb_stage = nbp + 1

  end if

  step  =  ( xmax - xmin ) / real( nb_stage , 8 )

  sum_s  =  f( xmin )

  do i_stage = 1,nb_stage,2

	 x_stage  =  xmin  +  real( i_stage , 8 ) * step

	 sum_s  =  sum_s  +  4._rp * f( x_stage )

  end do

  do i_stage = 2,nb_stage-1,2

	 x_stage  =  xmin  +  real( i_stage , 8 ) * step

	 sum_s  =  sum_s  +  2._rp * f( x_stage )

  end do

  sum_s  =  sum_s  +  f( xmax )

  FUNSimpson = step * sum_s / 3._rp

END FUNCTION FUNSimpson


END PROGRAM gen_obs