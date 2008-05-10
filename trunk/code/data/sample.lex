Begin: Root
Root: N_ROOT V_ROOT P_ROOT AUX_ROOT

N_ROOT:
 proxy   End N[sem = <proxy>]
 mit   End N[sem = <mit>]
 investigation  End N[sem = <mit>]

V_ROOT:
 use  End V[sem = <use>]

AUX_ROOT:
 can End AUX[sem = <can>]
 cannot End AUX[sem = <cannot>]
 may End AUX[sem = <may>]

P_ROOT:
 for   End  P[sem = <for>]

End:
'#'   End   None
