Begin: Root
Root: N_ROOT V_ROOT ADJ_ROOT P_ROOT MODAL PARTICLE
AfterNoun: NounSuffix
NounSuffix: End PLURAL N_TO_ADJ
AfterPlural: End

AfterVerb: V_SUFFIX End

N_ROOT:
 prox   End   N[sem = <proxy>]
 card End   N[sem = <card>]
 data End   N[sem = <data>]
 mit   End   N[sem = <mit>]
 crime   AfterNoun   N[sem = <crime>]
 person  AfterNoun   N[sem = <person>]
 document   AfterNoun   N[sem = <document>]

PLURAL:
 +s   End   []

N_TO_ADJ:
 +inal   End   ADJ[]

V_ROOT:
 use  End   V[sem = <use>]
 investigate AfterVerb V[sem = <investigate>]
 access  AfterVerb   V[sem = <access>]

V_SUFFIX:
 +ion End N[]

ADJ_ROOT:
 clear   End   ADJ[sem = <clear>]

P_ROOT:
 for   End   FOR[sem = <for>]
 to   End   TO[sem = <to>]

MODAL:
 can  End   PMOD[sem = <yes>]
 may  End   PMOD[sem = <yes>]
 cannot  End NMOD[sem = <no>]

PARTICLE:
 a End   DET[sem = <a>]
 an   End   DET[sem = <a>]
 the  End   DET[sem = <the>]
 not  End   NEG[sem = <no>]

End:
'#'   End   None
