Begin: Root
Root: N_ROOT V_ROOT ADJ_ROOT P_ROOT MODAL NEGATION

N_ROOT:
 proxy   End   N[sem = <proxy>]
 card End   N[sem = <card>]
 data End   N[sem = <data>]
 mit   End   N[sem = <mit>]

V_ROOT:
 use  End   V[sem = <use>]
 investigate V_SUFFIX V[sem = <investigate>]

V_SUFFIX:
 +ion End N[]

ADJ_ROOT:
 criminal   End   ADJ[sem = <criminal>]

P_ROOT:
 for   End   P[sem = <for>]

MODAL:
 can  End   PMOD[sem = <yes>]
 may  End   PMOD[sem = <yes>]
 cannot  End NMOD[sem = <no>]

NEGATION:
 not  End   NEG[sem = <no>]

End:
'#'   End   None
