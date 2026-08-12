@ Treinadores de rota de Route32, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route32_MapScripts::
	.byte 0

Route32_EventScript_FisherJustin::
	trainerbattle_single TRAINER_JOHTO_JUSTIN, Route32_Text_FisherJustinSeen, Route32_Text_FisherJustinBeaten
	msgbox Route32_Text_FisherJustinAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_FisherRalph::
	trainerbattle_single TRAINER_JOHTO_RALPH, Route32_Text_FisherRalphSeen, Route32_Text_FisherRalphBeaten
	msgbox Route32_Text_FisherRalphAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_FisherHenry::
	trainerbattle_single TRAINER_JOHTO_HENRY, Route32_Text_FisherHenrySeen, Route32_Text_FisherHenryBeaten
	msgbox Route32_Text_FisherHenryAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_YoungsterAlbert::
	trainerbattle_single TRAINER_JOHTO_ALBERT, Route32_Text_YoungsterAlbertSeen, Route32_Text_YoungsterAlbertBeaten
	msgbox Route32_Text_YoungsterAlbertAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_YoungsterGordon::
	trainerbattle_single TRAINER_JOHTO_GORDON, Route32_Text_YoungsterGordonSeen, Route32_Text_YoungsterGordonBeaten
	msgbox Route32_Text_YoungsterGordonAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_CamperRoland::
	trainerbattle_single TRAINER_JOHTO_ROLAND, Route32_Text_CamperRolandSeen, Route32_Text_CamperRolandBeaten
	msgbox Route32_Text_CamperRolandAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_PicnickerLiz::
	trainerbattle_single TRAINER_JOHTO_LIZ, Route32_Text_PicnickerLizSeen, Route32_Text_PicnickerLizBeaten
	msgbox Route32_Text_PicnickerLizAfter, MSGBOX_AUTOCLOSE
	end

Route32_EventScript_BirdkeeperPeter::
	trainerbattle_single TRAINER_JOHTO_PETER, Route32_Text_BirdkeeperPeterSeen, Route32_Text_BirdkeeperPeterBeaten
	msgbox Route32_Text_BirdkeeperPeterAfter, MSGBOX_AUTOCLOSE
	end

Route32_Text_FisherJustinSeen:
	.string "Whoa!\p"
	.string "You made me lose that fish!$"

Route32_Text_FisherJustinBeaten:
	.string "Sploosh!$"

Route32_Text_FisherJustinAfter:
	.string "Calm, collected… The essence of\n"
	.string "fishing and POKéMON is the same.$"

Route32_Text_FisherRalphSeen:
	.string "I'm really good at both\n"
	.string "fishing and POKéMON.\p"
	.string "I'm not about to lose to any kid!$"

Route32_Text_FisherRalphBeaten:
	.string "Tch! I tried to rush\n"
	.string "things…$"

Route32_Text_FisherRalphAfter:
	.string "Fishing is a lifelong\n"
	.string "passion.\p"
	.string "POKéMON are lifelong friends!$"

Route32_Text_FisherHenrySeen:
	.string "My POKéMON? Freshly caught!$"

Route32_Text_FisherHenryBeaten:
	.string "SPLASH?$"

Route32_Text_FisherHenryAfter:
	.string "Freshly caught POKéMON are\n"
	.string "no match for properly raised ones.$"

Route32_Text_YoungsterAlbertSeen:
	.string "I haven't seen you around before.\n"
	.string "So you think you are pretty tough?$"

Route32_Text_YoungsterAlbertBeaten:
	.string "You're strong!$"

Route32_Text_YoungsterAlbertAfter:
	.string "I'm going to try to be the\n"
	.string "best with my favorites.\p"
	.string "I'm not using the same tough\n"
	.string "POKéMON as everyone else.$"

Route32_Text_YoungsterGordonSeen:
	.string "I found some good POKéMON\n"
	.string "in the grass!\p"
	.string "I think they'll do it for me!$"

Route32_Text_YoungsterGordonBeaten:
	.string "Darn. I thought I could win.$"

Route32_Text_YoungsterGordonAfter:
	.string "The grass is full of\n"
	.string "clingy things.$"

Route32_Text_CamperRolandSeen:
	.string "That glance… It's intriguing.$"

Route32_Text_CamperRolandBeaten:
	.string "Hmmm. This is disappointing.$"

Route32_Text_CamperRolandAfter:
	.string "If you don't want to battle,\n"
	.string "just avoid eye contact.$"

Route32_Text_PicnickerLizSeen:
	.string "Uh-huh. Yeah, and you know…\p"
	.string "Pardon? Battle? I'm on the phone.\n"
	.string "Oh, all right. But make it fast.$"

Route32_Text_PicnickerLizBeaten:
	.string "Oh! I've got to relieve\n"
	.string "my anger!$"

Route32_Text_PicnickerLizAfter:
	.string "I was having a nice chat too.$"

Route32_Text_BirdkeeperPeterSeen:
	.string "That BADGE! It's from VIOLET CITY!\n"
	.string "You beat FALKNER?$"

Route32_Text_BirdkeeperPeterBeaten:
	.string "I know what my weaknesses are.$"

Route32_Text_BirdkeeperPeterAfter:
	.string "I should train again at the\n"
	.string "GYM in VIOLET CITY.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route32_EventScript_Sign1::
	lock
	msgbox Route32_Text_Sign1, MSGBOX_SIGN
	closemessage
	release
	end

Route32_EventScript_Sign2::
	lock
	msgbox Route32_Text_Sign2, MSGBOX_SIGN
	closemessage
	release
	end

Route32_EventScript_Sign3::
	lock
	msgbox Route32_Text_Sign3, MSGBOX_SIGN
	closemessage
	release
	end

Route32_Text_Sign1::
	.string "ROUTE 32\p"
	.string "VIOLET CITY - AZALEA TOWN$"

Route32_Text_Sign2::
	.string "RUINS OF ALPH\n"
	.string "EAST ENTRANCE$"

Route32_Text_Sign3::
	.string "UNION CAVE\n"
	.string "AHEAD$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route32_Text_CooltrainerM_Experiences::
	.string "Your experiences in VIOLET CITY\n"
	.string "should be useful for your journey.$"

Route32_EventScript_BaldingManFala::
	msgbox Route32_Text_CooltrainerM_Experiences, MSGBOX_NPC
	end

Route32_Text_SlowpokeTailOffer::
	.string "How would you like to have this\n"
	.string "tasty, nutritious SLOWPOKETAIL?\p"
	.string "For you right now, just\n"
	.string "¥1,000,000!\p"
	.string "You'll want this!$"

Route32_EventScript_SlowpokeTailFala::
	msgbox Route32_Text_SlowpokeTailOffer, MSGBOX_NPC
	end

VioletCity_EventScript_LiquidJustice::
	msgbox VioletCity_Text_LiquidJustice, MSGBOX_NPC
	end

VioletCity_Text_LiquidJustice::
	.string "Look around!\p"
	.string "It's easy to see what POKéMON\n"
	.string "you can catch in an area without\l"
	.string "having to run around in tall\l"
	.string "grass all day!$"
