@ PWTInside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PWTInside_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ STUB A2: cena do bloco A4/A5/A6, rotulo PwtEnterFromBackScript
Unova_PWTInside_EventScript_PwtEnterFromBackScript::
	lockall
	setvar VAR_UNOVA_PWT_DENTRO_CENA, 1
	applymovement 1, Unova_PWTInside_Movement_BloqueadorSai
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Unova_PWTInside_Movement_JogadorEntra
	waitmovement 0
	applymovement 1, Unova_PWTInside_Movement_BloqueadorVolta
	waitmovement 0
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_PWTInside_EventScript_Npc0::
	msgbox Unova_PWTInside_Text_PwtInsideQualifierText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc1::
	msgbox Unova_PWTInside_Text_PwtInsideReceptionistGenericText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc2::
	msgbox Unova_PWTInside_Text_PwtInsideReceptionistGenericText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc3::
	msgbox Unova_PWTInside_Text_PwtInsideYoungsterText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc4::
	msgbox Unova_PWTInside_Text_PwtInsideCooltrainerFText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc5::
	msgbox Unova_PWTInside_Text_PwtInsideOfficerText, MSGBOX_NPC
	end

Unova_PWTInside_EventScript_Npc6::
	msgbox Unova_PWTInside_Text_PwtInsideOfficerText, MSGBOX_NPC
	end


Unova_PWTInside_Text_PwtInsideQualifierText::
	.string "Hi, welcome to the"
	.string "\nPOKéMON WORLD"
	.string "\lTOURNAMENT!"
	.string "\pWe're accepting"
	.string "\napplications for"
	.string "\lqualifiers now."
	.string "\pWould you like"
	.string "\nto enter?$"

Unova_PWTInside_Text_PwtInsideReceptionistGenericText::
	.string "Hi, welcome to the"
	.string "\nPOKéMON WORLD"
	.string "\lTOURNAMENT!"
	.string "\pIf you want to"
	.string "\napply, see the"
	.string "\lreceptionist.$"

Unova_PWTInside_Text_PwtInsideYoungsterText::
	.string "My favorite to"
	.string "\nwatch is IRIS!"
	.string "\pShe used to be"
	.string "\nthe CHAMPION!"
	.string "\pHow can you beat"
	.string "\nthat?$"

Unova_PWTInside_Text_PwtInsideCooltrainerFText::
	.string "I tried to enter,"
	.string "\nbut I got beat in"
	.string "\lthe qualifiers."
	.string "\pIt's tough!$"

Unova_PWTInside_Text_PwtInsideOfficerText::
	.string "This way leads to"
	.string "\nthe stands for"
	.string "\pwatching the"
	.string "\nmatches."
	.string "\pIf you want to"
	.string "\nenter, you should"
	.string "\pgo talk to the"
	.string "\nreceptionist.$"

@ Cenas do PWT (dev_scripts/cenas_pwt_unova.py), autorizadas em 22/08/2026

	.align 2
Unova_PWTInside_Movement_BloqueadorSai:
	walk_up
	walk_right
	walk_in_place_faster_left
	step_end

	.align 2
Unova_PWTInside_Movement_JogadorEntra:
	walk_down
	walk_down
	walk_down
	step_end

	.align 2
Unova_PWTInside_Movement_BloqueadorVolta:
	walk_left
	walk_down
	step_end
