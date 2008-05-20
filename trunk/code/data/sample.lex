Begin: Root
Root: N_ROOT V_ROOT ADJ_ROOT P_ROOT PARTICLE
AfterNoun: NounSuffix
NounSuffix: End GENITIVE  PLURAL N_TO_ADJ
AfterPlural: End

AfterVerb: V_SUFFIX End

N_ROOT:
 prox   AfterNoun N[sem = <prox>]
 proximity   AfterNoun N[sem = <prox>]
 card AfterNoun   N[sem = <card>]
 data AfterNoun   N[sem = <data>]
 records AfterNoun   N[sem = <data>]
 mit   AfterNoun   N[sem = <mit>]
 crime   AfterNoun   N[sem = <crime>]
 person  AfterNoun   N[sem = <person>]
 document   AfterNoun   N[sem = <document>]
 domain  AfterNoun   N[sem = <domain>]
 student AfterNoun   N[sem = <student>]
 one  End   N[sem = <person>]
 anyone  End   N[sem = <person>]
 committee  AfterNoun   N[sem = <committee>]
 discipline AfterNoun   N[sem = <discipline>]
 service AfterNoun   N[sem = <service>]
 provider   AfterNoun   N[sem = <provider>]
 phone   AfterNoun N[sem = <phone>]
 record AfterNoun   N[sem = <record>]
 request AfterNoun   N[sem = <request>]
 customer  AfterNoun   N[sem = <customer>]
 terrorism  AfterNoun   N[sem = <terrorism>]
 record  AfterNoun   N[sem = <record>]
 tsa  AfterNoun   N[sem = <tsa>]
 fbi  AfterNoun   N[sem = <fbi>]
 committee  AfterNoun   N[sem = <committee>]
 discipline AfterNoun   N[sem = <discipline>]
 permission AfterNoun   N[sem = <permission>]
 police  AfterNoun   N[sem = <police>]
 people  AfterNoun   N[sem = <people>]
 home AfterNoun   N[sem = <home>]
 tsa  AfterNoun   N[sem = <tsa>]
 fbi  AfterNoun   N[sem = <fbi>]
 possession AfterNoun   N[sem = <possession>]
 state   AfterNoun   N[sem = <state>]
 massachusetts AfterNoun   N[sem = <massachusetts>]
 purpose AfterNoun N[sem = <purpose>]

GENITIVE:
 's   End   []

PLURAL:
 +s   End   []

N_TO_ADJ:
 +inal   End   ADJ[]

V_ROOT:
 is   End   IS[sem = <is>, so = false]
 was  End   IS[sem = <was>, so = false]
 has  End   V[sem = <has>, so = false]
 use  AfterVerb   V[sem = <use>, so = false]
 discriminate  AfterVerb   V[sem = <discriminate>, so = false]
 investigate AfterVerb V[sem = <investigate>, so = false]
 access  AfterVerb   V[sem = <access>, so = false]
 transfer   AfterVerb   V[sem = <transfer>, so = true]
 deny AfterVerb   V[sem = <deny>, so = true]
 request AfterVerb   V[sem = <request>, so = true]
 reside  AfterVerb   V[sem = <reside>, so = false]
 associate  AfterVerb   V[sem = <associate>, so = true]
 search  AfterVerb   V[sem = <search>, so = false]
 have AfterVerb   V[sem = <have>, so = false]
 give	AfterVerb	V[sem = <give>, so = true]

V_SUFFIX:
 +ion End N[]
 +s   End   V[]
 +ed  End   V[]
 +ed  End   ADJ[]
 +ing End   V[]

ADJ_ROOT:
 clear   End   ADJ[sem = <clear>]
 private End   ADJ[sem = <private>]
 specific   End   ADJ[sem = <specific>]

P_ROOT:
 for   End   FOR[sem = <for>]
 for  End   P[sem = <for>]
 to   End   TO[sem = <to>]
 to   End   P[sem = <to>]
 on   End   P[sem = <on>]
 with End   P[sem = <with>]
 in   End   P[sem = <in>]
 of   End   P[sem = <of>]

PARTICLE:
 can  End   PMOD[sem = <yes>]
 may  End   PMOD[sem = <yes>]
 cannot  End NMOD[sem = <no>]
 a End   DET[sem = <a>]
 another End   DET[sem = <another>]
 an   End   DET[sem = <a>]
 any  End   DET[sem = <a>]
 the  End   DET[sem = <the>]
 that  End   DET[sem = <that>]
 not  End   NEG[sem = <no>]
 and  End   AND[sem = <and>]
 if   End   IF[sem = <if>]
 his  End   DET[sem = <his>]
 her  End   DET[sem = <her>]
 their   End   DET[sem = <their>]
 its  End   DET[sem = <its>]

End:
'#'   End   None
