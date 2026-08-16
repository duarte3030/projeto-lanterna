@ OpelucidCity do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_OpelucidCity_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ IRIS ja veio importada como objeto 2 (local id 2, gfx OBJ_EVENT_GFX_PHOEBE,
@ parada em 17,6 — o mesmo NPC do script Npc1/"bloqueadora do ginasio", ja
@ existente). Sua flag de esconder, FLAG_UNOVA_OPELUCID_IRIS, ESTA na tabela
@ da Obra 1 (e setada por Unova_DragonspiralTowerRoof no fim daquela cena, A1,
@ ja feita) — wired no map.json (flag: FLAG_UNOVA_OPELUCID_IRIS).
@ `moveobject` da fonte -> `setobjectxyperm` (grava no template; mesma tecnica
@ da JUNIPER em Unova_ChampionsRoom). `appear`/`disappear` -> clearflag+
@ addobject / removeobject+setflag, tabela do PLANO.
Unova_OpelucidCity_EventScript_OpelucidCityIrisScript1::
	lockall
	setobjectxyperm 2, 38, 20
	goto Unova_OpelucidCity_EventScript_OpelucidCityIrisComum

Unova_OpelucidCity_EventScript_OpelucidCityIrisScript2::
	lockall
	setobjectxyperm 2, 38, 21
	goto Unova_OpelucidCity_EventScript_OpelucidCityIrisComum

Unova_OpelucidCity_EventScript_OpelucidCityIrisScript3::
	lockall
	setobjectxyperm 2, 38, 22
	@ cai no comum

Unova_OpelucidCity_EventScript_OpelucidCityIrisComum::
	clearflag FLAG_UNOVA_OPELUCID_IRIS
	addobject 2
	applymovement 2, Unova_OpelucidCity_Movement_IrisChega
	waitmovement 0
	msgbox Unova_OpelucidCity_Text_OpelucidCityIrisWelcomeText, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_OpelucidCity_Movement_IrisSai
	waitmovement 0
	removeobject 2
	setflag FLAG_UNOVA_OPELUCID_IRIS
	setobjectxyperm 2, 17, 6
	clearflag FLAG_UNOVA_OPELUCID_IRIS
	addobject 2
	turnobject 2, DIR_SOUTH
	setvar VAR_UNOVA_OPELUCID_CENA, 1
	releaseall
	end

Unova_OpelucidCity_Movement_IrisChega:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	step_end

Unova_OpelucidCity_Movement_IrisSai:
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_OpelucidCity_EventScript_Placa0::
	msgbox Unova_OpelucidCity_Text_OpelucidCitySignText, MSGBOX_SIGN
	end

Unova_OpelucidCity_EventScript_Placa1::
	msgbox Unova_OpelucidCity_Text_OpelucidR9SignText, MSGBOX_SIGN
	end

Unova_OpelucidCity_EventScript_Placa2::
	msgbox Unova_OpelucidCity_Text_OpelucidR11SignText, MSGBOX_SIGN
	end

Unova_OpelucidCity_EventScript_Placa3::
	msgbox Unova_OpelucidCity_Text_OpelucidDraydenHouseSignText, MSGBOX_SIGN
	end

Unova_OpelucidCity_EventScript_Npc1::
	msgbox Unova_OpelucidCity_Text_OpelucidCityBlockerText, MSGBOX_NPC
	end

Unova_OpelucidCity_EventScript_Npc3::
	msgbox Unova_OpelucidCity_Text_OpelucidCityLassText, MSGBOX_NPC
	end

Unova_OpelucidCity_EventScript_Npc4::
	msgbox Unova_OpelucidCity_Text_OpelucidCityFisherText, MSGBOX_NPC
	end

Unova_OpelucidCity_EventScript_Npc5::
	msgbox Unova_OpelucidCity_Text_OpelucidCityYoungsterText, MSGBOX_NPC
	end

Unova_OpelucidCity_EventScript_Npc6::
	msgbox Unova_OpelucidCity_Text_OpelucidCityGentlemanText, MSGBOX_NPC
	end


Unova_OpelucidCity_Text_OpelucidCitySignText::
	.string "OPELUCID CITY."
	.string "\pThe city where"
	.string "\npast and future"
	.string "\lintertwine.$"

Unova_OpelucidCity_Text_OpelucidR9SignText::
	.string "WEST to ROUTE 9."
	.string "\pPassage to"
	.string "\nICIRRUS CITY.$"

Unova_OpelucidCity_Text_OpelucidR11SignText::
	.string "EAST to ROUTE 11."
	.string "\pVILLAGE BRIDGE"
	.string "\nahead.$"

Unova_OpelucidCity_Text_OpelucidDraydenHouseSignText::
	.string "Home of DRAYDEN."
	.string "\p(and IRIS!)$"

Unova_OpelucidCity_Text_OpelucidCityBlockerText::
	.string "IRIS: Sorry"
	.string "\n{PLAYER}, my"
	.string "\pgrandpa still"
	.string "\nhasn't come back"
	.string "\lto the gym.$"

Unova_OpelucidCity_Text_OpelucidCityLassText::
	.string "Gym leader DRAYDEN"
	.string "\nleads OPELUCID"
	.string "\lCITY as its mayor."
	.string "\pHe's always train-"
	.string "\ning by wrestling"
	.string "\lwith his POKéMON.$"

Unova_OpelucidCity_Text_OpelucidCityFisherText::
	.string "UNOVA's symbols"
	.string "\nare legendary"
	.string "\ldragon POKéMON."
	.string "\pBut I wonder where"
	.string "\nthey are now?$"

Unova_OpelucidCity_Text_OpelucidCityYoungsterText::
	.string "There was a person"
	.string "\ncalled N who had a"
	.string "\plegendary POKéMON"
	.string "\nwith him. Do you"
	.string "\pthink he was"
	.string "\nreally the hero?$"

Unova_OpelucidCity_Text_OpelucidCityIrisWelcomeText::
	.string "IRIS: Hey {PLAYER}!"
	.string "\nIt's me, IRIS!"
	.string "\pWe met back at the"
	.string "\nPOKéMON WORLD"
	.string "\lTOURNAMENT,"
	.string "\lremember?"
	.string "\pCongrats on your"
	.string "\nwin, by the way!"
	.string "\pI bet you're here"
	.string "\nto challenge my"
	.string "\pgrandpa. He's the"
	.string "\nGYM LEADER here in"
	.string "\lOPELUCID CITY."
	.string "\pUnfortunately,"
	.string "\nhe's not here"
	.string "\lright now."
	.string "\pHe said something"
	.string "\nwas going on at"
	.string "\pDRAGONSPIRAL TOWER"
	.string "\nand went to go"
	.string "\pcheck it out. If"
	.string "\nyou want to get to"
	.string "\pthe tower, you can"
	.string "\nget there by going"
	.string "\pwest to ICIRRUS"
	.string "\nCITY."
	.string "\pI'm going back to"
	.string "\nthe GYM now. Good"
	.string "\lluck {PLAYER}!$"

Unova_OpelucidCity_Text_OpelucidCityGentlemanText::
	.string "Why do POKéMON"
	.string "\nstay by our sides?"
	.string "\pIf we could talk"
	.string "\nto them, we could"
	.string "\pask. I'm a bit"
	.string "\nscared about what"
	.string "\lthey'd say.$"
