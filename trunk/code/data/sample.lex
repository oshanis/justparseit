Begin: Root
Root: N_ROOT V_ROOT ADJ_ROOT P_ROOT MODAL PARTICLE
AfterNoun: NounSuffix
NounSuffix: End PLURAL N_TO_ADJ
AfterPlural: End

AfterVerb: V_SUFFIX End

N_ROOT:
 prox   AfterNoun N[sem = <prox>]
 card AfterNoun   N[sem = <card>]
 data AfterNoun   N[sem = <data>]
 mit   AfterNoun   N[sem = <mit>]
 crime   AfterNoun   N[sem = <crime>]
 person  AfterNoun   N[sem = <person>]
 document   AfterNoun   N[sem = <document>]
 domain  AfterNoun   N[sem = <domain>]
 student AfterNoun   N[sem = <student>]
 authorization AfterNoun   N[sem = <authorization>]
 anyone  End   N[sem = <person>]

PLURAL:
 +s   End   []

N_TO_ADJ:
 +inal   End   ADJ[]

V_ROOT:
 use  End   V[sem = <use>]
 investigate AfterVerb V[sem = <investigate>]
 access  AfterVerb   V[sem = <access>]
 transfer   AfterVerb   V[sem = <transfer>]
 has  AfterVerb   V[sem = <has>]

V_SUFFIX:
 +ion End N[]

ADJ_ROOT:
 clear   End   ADJ[sem = <clear>]
 private End   ADJ[sem = <private>]

P_ROOT:
 for   End   FOR[sem = <for>]
 to   End   TO[sem = <to>]
 on   End   P[sem = <on>]

MODAL:
 can  End   PMOD[sem = <yes>]
 may  End   PMOD[sem = <yes>]
 cannot  End NMOD[sem = <no>]

PARTICLE:
 a End   DET[sem = <a>]
 an   End   DET[sem = <a>]
 any  End   DET[sem = <a>]
 the  End   DET[sem = <the>]
 not  End   NEG[sem = <no>]
 and  End   AND[sem = <and>]
 if   End   IF[sem = <if>]

End:
'#'   End   None
