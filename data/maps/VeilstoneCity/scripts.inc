@ Textos vindos de pret/pokeplatinum (res/text/veilstone_city.json), em ingles.
@ Counterpart (Dawn/Lucas), Grunt_M (warehouse norte/sul/southeast/storage key),
@ Crasher Wake e Looker ficaram de fora: dependem de flag de historia
@ (FLAG_HIDE_VEILSTONE_*), que este agente nao pode inventar.
@ OBJ_EVENT_GFX_GUITARIST, OBJ_EVENT_GFX_ROUGHNECK e OBJ_EVENT_GFX_LADY nao
@ existem em event_objects.h: trocados por MAN_3, MAN_5 e WOMAN_3.

VeilstoneCity_MapScripts::
	.byte 0

VeilstoneCity_EventScript_Guitarist1::
	msgbox VeilstoneCity_Text_Guitarist1, MSGBOX_NPC
	end

VeilstoneCity_EventScript_PokefanM::
	msgbox VeilstoneCity_Text_PokefanM, MSGBOX_NPC
	end

VeilstoneCity_EventScript_BattleGirl1::
	msgbox VeilstoneCity_Text_BattleGirl1, MSGBOX_NPC
	end

VeilstoneCity_EventScript_Lady::
	msgbox VeilstoneCity_Text_Lady, MSGBOX_NPC
	end

VeilstoneCity_EventScript_BattleGirl2::
	msgbox VeilstoneCity_Text_BattleGirl2, MSGBOX_NPC
	end

VeilstoneCity_EventScript_Roughneck::
	msgbox VeilstoneCity_Text_Roughneck, MSGBOX_NPC
	end

VeilstoneCity_EventScript_Guitarist2::
	msgbox VeilstoneCity_Text_Guitarist2, MSGBOX_NPC
	end

VeilstoneCity_EventScript_BattleGirl3::
	msgbox VeilstoneCity_Text_BattleGirl3, MSGBOX_NPC
	end

VeilstoneCity_EventScript_Guitarist3::
	msgbox VeilstoneCity_Text_Guitarist3, MSGBOX_NPC
	end

VeilstoneCity_EventScript_MeteoriteSign::
	msgbox VeilstoneCity_Text_MeteoriteSign, MSGBOX_SIGN
	end

VeilstoneCity_EventScript_DepartmentStoreSign::
	msgbox VeilstoneCity_Text_DepartmentStoreSign, MSGBOX_SIGN
	end

VeilstoneCity_Text_Guitarist1:
	.string "VEILSTONE is the city of stone.\n"
	.string "We even have meteorites!$"

VeilstoneCity_Text_PokefanM:
	.string "That's the VEILSTONE DEPARTMENT\n"
	.string "STORE over there. They sell all\l"
	.string "sorts of rare goods.$"

VeilstoneCity_Text_BattleGirl1:
	.string "The GYM here is run by a kid, but\n"
	.string "don't let that fool you!$"

VeilstoneCity_Text_Lady:
	.string "I love shopping at the department\n"
	.string "store. There's always something\l"
	.string "new to find.$"

VeilstoneCity_Text_BattleGirl2:
	.string "If someone uses Embargo on your\n"
	.string "POKéMON, it becomes impossible to\l"
	.string "use any items on it.$"

VeilstoneCity_Text_Roughneck:
	.string "VEILSTONE is the city of stone. We\n"
	.string "even have meteorites! Anyway,\l"
	.string "enjoy your visit here.$"

VeilstoneCity_Text_Guitarist2:
	.string "Hey there, Trainer! You like\n"
	.string "POKéMON?$"

VeilstoneCity_Text_BattleGirl3:
	.string "There's a GAME CORNER and a PRIZE\n"
	.string "EXCHANGE around here. Worth a\l"
	.string "look if you like games.$"

VeilstoneCity_Text_Guitarist3:
	.string "I can hardly believe it myself...\n"
	.string "just look at how strong you seem!$"

VeilstoneCity_Text_MeteoriteSign:
	.string "It's a mysterious meteorite that\n"
	.string "fell from the stars...$"

VeilstoneCity_Text_DepartmentStoreSign:
	.string "VEILSTONE DEPARTMENT STORE$"

@ Historia: a Galactica em Veilstone. O QG (galactic_hq_*) e o armazem ainda nao
@ existem como mapa, entao o grunt so guarda a rua. Texto de pret/pokeplatinum,
@ res/text/lake_acuity.json e veilstone_city.json.

VeilstoneCity_EventScript_GalacticGrunt::
	msgbox VeilstoneCity_Text_GalacticGrunt, MSGBOX_NPC
	end

VeilstoneCity_Text_GalacticGrunt:
	.string "This is Team Galactic's turf.\p"
	.string "Our headquarters is right here in\n"
	.string "Veilstone, but don't waste your\l"
	.string "time. You'll never get in.\p"
	.string "Now, if you'll excuse me.$"
