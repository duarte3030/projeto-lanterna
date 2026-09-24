@ MtChimney_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 33.7) por dev_scripts/copia_planta_ex.py.

MtChimney_Gym_MapScripts::
	.byte 0

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
MtChimney_Gym_EventScript_Blaine::
	trainerbattle_single TRAINER_HOENNEX_BLAINE, MtChimney_Gym_Text_BlaineIntro, MtChimney_Gym_Text_BlaineDefeat, MtChimney_Gym_EventScript_BlaineDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_FIRE_BLAST, MtChimney_Gym_EventScript_GiveFireBlast
	msgbox MtChimney_Gym_Text_BlainePostBattle, MSGBOX_NPC
	end

MtChimney_Gym_EventScript_BlaineDefeated::
	message MtChimney_Gym_Text_ReceivedVolcanoBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox MtChimney_Gym_Text_BlaineTakeThis, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_16
	goto MtChimney_Gym_EventScript_GiveFireBlast

MtChimney_Gym_EventScript_GiveFireBlast::
	giveitem ITEM_TM38
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_FIRE_BLAST
	msgbox MtChimney_Gym_Text_ExplainFireBlast, MSGBOX_NPC
	release
	end

MtChimney_Gym_Text_BlaineIntro:
	.string "I’ve been expecting you ever since my\n"
	.string "niece said you got her badge at the\l"
	.string "bottom of this mountain.\p"
	.string "It was my idea, you know, for Hoenn to\n"
	.string "have 16 certified GYMS.\p"
	.string "And it seems you’re almost through them\n"
	.string "all.\p"
	.string "All but one.\n"
	.string "FLANNERY’s young and her fire is\l"
	.string "artificial.\p"
	.string "But my lava comes from the Earth itself.\p"
	.string "Ready yourself for raw geothermal\n"
	.string "power!$"

MtChimney_Gym_Text_BlaineDefeat:
	.string "You truly are something to be reckoned\n"
	.string "with.\p"
	.string "This is the last of the VOLCANO BADGES\n"
	.string "that was forged from the magma of MT.\l"
	.string "CINNABAR before it erupted.$"

MtChimney_Gym_Text_ReceivedVolcanoBadge:
	.string "{PLAYER} received the VOLCANO BADGE\n"
	.string "from BLAINE.$"

MtChimney_Gym_Text_BlaineTakeThis:
	.string "\p"
	.string "Take this TM as well.$"

MtChimney_Gym_Text_ExplainFireBlast:
	.string "TM38 contains FIRE BLAST.\p"
	.string "The pinnacle of FIRE TYPE moves.\p"
	.string "Go now.\n"
	.string "I have trained with the elite 4.\p"
	.string "They will be no match for you.$"

MtChimney_Gym_Text_BlainePostBattle:
	.string "I have trained with the elite 4.\p"
	.string "They will be no match for you.$"

