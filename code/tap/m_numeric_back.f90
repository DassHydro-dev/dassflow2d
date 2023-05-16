!        Generated by TAPENADE     (INRIA, Ecuador team)
!  Tapenade 3.16 (master) -  9 Oct 2020 17:47
!
MODULE M_NUMERIC_BACK

  USE M_TAP_VARS

CONTAINS

!  Differentiation of linear_interp in reverse (adjoint) mode (with options fixinterface noISIZE):
!   gradient     of useful results: tx ty x linear_interp
!   with respect to varying inputs: tx ty x
  SUBROUTINE LINEAR_INTERP_BACK0(tx, tx_back, ty, ty_back, x, x_back, &
&   linear_interp_back)
    IMPLICIT NONE
    REAL(rp), DIMENSION(:), INTENT(IN) :: tx, ty
    REAL(rp), DIMENSION(:) :: tx_back, ty_back
    REAL(rp), INTENT(IN) :: x
    REAL(rp) :: x_back
    REAL(rp) :: alpha
    REAL(rp) :: alpha_back
    INTEGER(ip) :: ind, imin, imax
    INTRINSIC LBOUND
    INTRINSIC UBOUND
    REAL(rp) :: temp_back
    REAL(rp) :: temp_back0
    REAL(rp) :: linear_interp
    REAL(rp) :: linear_interp_back
    imin = LBOUND(tx(:), dim=1)
    imax = UBOUND(tx(:), dim=1)
    IF (x + zerom .LT. tx(imin)) THEN
      alpha = (x-tx(imin))/(tx(imin+1)-tx(imin))
      alpha_back = (ty(imin+1)-ty(imin))*linear_interp_back
      ty_back(imin) = ty_back(imin) + (one-alpha)*linear_interp_back
      ty_back(imin+1) = ty_back(imin+1) + alpha*linear_interp_back
      temp_back = alpha_back/(tx(imin+1)-tx(imin))
      x_back = x_back + temp_back
      temp_back0 = -((x-tx(imin))*temp_back/(tx(imin+1)-tx(imin)))
      tx_back(imin) = tx_back(imin) - temp_back - temp_back0
      tx_back(imin+1) = tx_back(imin+1) + temp_back0
    ELSE IF (x + zerom .LT. tx(imax)) THEN
      ind = imin + 1
      DO WHILE (tx(ind) .LT. x + zerom)
        ind = ind + 1
      END DO
      alpha = (x-tx(ind-1))/(tx(ind)-tx(ind-1))
      alpha_back = (ty(ind)-ty(ind-1))*linear_interp_back
      ty_back(ind-1) = ty_back(ind-1) + (one-alpha)*linear_interp_back
      ty_back(ind) = ty_back(ind) + alpha*linear_interp_back
      temp_back0 = alpha_back/(tx(ind)-tx(ind-1))
      x_back = x_back + temp_back0
      temp_back = -((x-tx(ind-1))*temp_back0/(tx(ind)-tx(ind-1)))
      tx_back(ind-1) = tx_back(ind-1) - temp_back0 - temp_back
      tx_back(ind) = tx_back(ind) + temp_back
    ELSE
      alpha = (x-tx(imax-1))/(tx(imax)-tx(imax-1))
      alpha_back = (ty(imax)-ty(imax-1))*linear_interp_back
      ty_back(imax-1) = ty_back(imax-1) + (one-alpha)*linear_interp_back
      ty_back(imax) = ty_back(imax) + alpha*linear_interp_back
      temp_back0 = alpha_back/(tx(imax)-tx(imax-1))
      x_back = x_back + temp_back0
      temp_back = -((x-tx(imax-1))*temp_back0/(tx(imax)-tx(imax-1)))
      tx_back(imax-1) = tx_back(imax-1) - temp_back0 - temp_back
      tx_back(imax) = tx_back(imax) + temp_back
    END IF
  END SUBROUTINE LINEAR_INTERP_BACK0



END MODULE M_NUMERIC_BACK
