@ OpelucidGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_OpelucidGym_MapScripts::
	.byte 0

Unova_OpelucidGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_DRAYDEN, Unova_OpelucidGym_Text_DraydenGymIntroText, Unova_OpelucidGym_Text_DraydenWinLossText, Unova_OpelucidGym_EventScript_Insignia0
	end

Unova_OpelucidGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_OPELUCID
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_OpelucidGym_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_VETERANM_OPELUCID_GYM_1, Unova_OpelucidGym_Text_VeteranM1OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranM1OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_VETERANM_OPELUCID_GYM_2, Unova_OpelucidGym_Text_VeteranM2OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranM2OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_VETERANM_OPELUCID_GYM_3, Unova_OpelucidGym_Text_VeteranM3OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranM3OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_VETERANF_OPELUCID_GYM_1, Unova_OpelucidGym_Text_VeteranF1OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranF1OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_VETERANF_OPELUCID_GYM_2, Unova_OpelucidGym_Text_VeteranF2OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranF2OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_VETERANF_OPELUCID_GYM_3, Unova_OpelucidGym_Text_VeteranF3OpelucidGymSeenText, Unova_OpelucidGym_Text_VeteranF3OpelucidGymBeatenText
	end

Unova_OpelucidGym_EventScript_Npc7::
	msgbox Unova_OpelucidGym_Text_OpelucidGymGuyText, MSGBOX_NPC
	end


Unova_OpelucidGym_Text_DraydenGymIntroText::
	.string "Welcome. Thank you"
	.string "\nfor coming. I am"
	.string "\pthe OPELUCID GYM"
	.string "\nLEADER, DRAYDEN."
	.string "\pAs mayor, I've"
	.string "\ngiven everything"
	.string "\pto developing the"
	.string "\ncity. As a"
	.string "\ptrainer, I've been"
	.string "\npursuing greater"
	.string "\lstrength."
	.string "\pWhat I'm searching"
	.string "\nfor now is a young"
	.string "\ptrainer who can"
	.string "\nshow me a bright"
	.string "\pfuture. Perhaps"
	.string "\nyou can show me"
	.string "\pthat future, the"
	.string "\nway IRIS has?$"

Unova_OpelucidGym_Text_DraydenWinLossText::
	.string "This bitterness"
	.string "\nthat floods me"
	.string "\lafter a defeat…"
	.string "\pThe heart that"
	.string "\ndoes not succumb"
	.string "\pto such a feeling"
	.string "\nis filled with"
	.string "\lenergy and life!$"

Unova_OpelucidGym_Text_VeteranM1OpelucidGymSeenText::
	.string "Always aim for the"
	.string "\ntop, like a dragon"
	.string "\ltaking flight!$"

Unova_OpelucidGym_Text_VeteranM1OpelucidGymBeatenText::
	.string "The energy I feel"
	.string "\nfrom you… It's just"
	.string "\llike a dragon!$"

Unova_OpelucidGym_Text_VeteranM2OpelucidGymSeenText::
	.string "A strong defense"
	.string "\nis everything!$"

Unova_OpelucidGym_Text_VeteranM2OpelucidGymBeatenText::
	.string "Your defense is"
	.string "\nbeyond comparison!$"

Unova_OpelucidGym_Text_VeteranM3OpelucidGymSeenText::
	.string "Use your POKéMON"
	.string "\nin combination to"
	.string "\praise their"
	.string "\ndestructive power!$"

Unova_OpelucidGym_Text_VeteranM3OpelucidGymBeatenText::
	.string "The POKéMON you"
	.string "\npicked gave me a"
	.string "\lrun for my money!$"

Unova_OpelucidGym_Text_VeteranF1OpelucidGymSeenText::
	.string "I believe the best"
	.string "\ndefense is a"
	.string "\lstrong offense!$"

Unova_OpelucidGym_Text_VeteranF1OpelucidGymBeatenText::
	.string "Such energy… You"
	.string "\nare truly without"
	.string "\lequal!$"

Unova_OpelucidGym_Text_VeteranF2OpelucidGymSeenText::
	.string "In battles, how"
	.string "\nyour POKéMON"
	.string "\pfollow each other"
	.string "\nis key.$"

Unova_OpelucidGym_Text_VeteranF2OpelucidGymBeatenText::
	.string "Your POKéMON all"
	.string "\nsupported each"
	.string "\lother well.$"

Unova_OpelucidGym_Text_VeteranF3OpelucidGymSeenText::
	.string "I just felt a"
	.string "\ngreat wind… Are"
	.string "\pyou the one who"
	.string "\nkicked it up?$"

Unova_OpelucidGym_Text_VeteranF3OpelucidGymBeatenText::
	.string "This defeat will"
	.string "\nalso be blown far"
	.string "\laway…$"

Unova_OpelucidGym_Text_OpelucidGymGuyText::
	.string "Yo, challenger!"
	.string "\pThis GYM's LEADER"
	.string "\nis DRAYDEN, the"
	.string "\lmaster of dragons."
	.string "\pAll of his pupils"
	.string "\ntrain with dragon-"
	.string "\ltype POKéMON too."
	.string "\pThey're wild and"
	.string "\nunpredictable!"
	.string "\pYour best bet"
	.string "\nwould be to bring"
	.string "\la fairy-type POKé-"
	.string "\lMON."
	.string "\pDragons also don't"
	.string "\nlike the cold, so"
	.string "\ptry using ice-type"
	.string "\nmoves too!$"
