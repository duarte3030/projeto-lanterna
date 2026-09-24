VioletCity_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

VioletCity_EventScript_GymSign::
	msgbox VioletCity_Text_GymSign, MSGBOX_SIGN
	end

VioletCity_Text_GymSign::
	.string "VIOLET CITY POKéMON GYM\p"
	.string "LEADER: FALKNER, The Elegant\n"
	.string "Master of Flying POKéMON$"

@ As três placas que o GS Chronicles desenhou na Violet copiada (23/09/2026):
@ a da cidade na calçada, a da SPROUT TOWER na margem norte do lago e a da
@ ACADEMY ao lado da porta dela. O desenho é do autor; o texto é nosso.

VioletCity_EventScript_CitySign::
	msgbox VioletCity_Text_CitySign, MSGBOX_SIGN
	end

VioletCity_Text_CitySign::
	.string "VIOLET CITY\n"
	.string "The City of Nostalgic Scents$"

VioletCity_EventScript_SproutTowerSign::
	msgbox VioletCity_Text_SproutTowerSign, MSGBOX_SIGN
	end

VioletCity_Text_SproutTowerSign::
	.string "SPROUT TOWER\n"
	.string "Experience the Way of POKéMON$"

VioletCity_EventScript_AcademySign::
	msgbox VioletCity_Text_AcademySign, MSGBOX_SIGN
	end

VioletCity_Text_AcademySign::
	.string "EARL'S POKéMON ACADEMY$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

VioletCity_EventScript_Lass::
	lock
	faceplayer
	msgbox VioletCity_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_Text_Lass::
	.string "Ghosts are rumored to appear\n"
	.string "in SPROUT TOWER.\p"
	.string "They say that GHOST-type\n"
	.string "moves can bypass the defenses\p"
	.string "of tough POKéMON like ONIX\n"
	.string "and GEODUDE.$"

VioletCity_EventScript_Boy::
	lock
	faceplayer
	msgbox VioletCity_Text_Boy, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_Text_Boy::
	.string "Hey, you're a POKéMON trainer?\p"
	.string "If you head to the ACADEMY,\n"
	.string "you might learn something new!$"

VioletCity_EventScript_Gramps::
	lock
	faceplayer
	msgbox VioletCity_Text_Gramps, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_Text_Gramps::
	.string "FALKNER, from the VIOLET\n"
	.string "POKéMON GYM, is a fine trainer!\p"
	.string "He inherited his father's gym\n"
	.string "and has done a great job with\l"
	.string "it.$"

VioletCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox VioletCity_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_Text_Youngster::
	.string "I saw a wiggly tree up ahead!\p"
	.string "If you touch it, it squirms\n"
	.string "and dances! Cool!$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

VioletCity_EventScript_Povoa1::
	lock
	faceplayer
	msgbox VioletCity_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

VioletCity_Text_Povoa1:
	.string "SPROUT TOWER sways all night.\nThe pillar inside moves it.$"

VioletCity_EventScript_Povoa2::
	lock
	faceplayer
	msgbox VioletCity_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

VioletCity_Text_Povoa2:
	.string "The TRAINER SCHOOL is right\nthere. The tests are hard.$"

VioletCity_EventScript_Povoa3::
	lock
	faceplayer
	msgbox VioletCity_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

VioletCity_Text_Povoa3:
	.string "The GYM here flies.\nElectric and Rock moves answer it.$"

VioletCity_EventScript_Povoa4::
	lock
	faceplayer
	msgbox VioletCity_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

VioletCity_Text_Povoa4:
	.string "Three roads leave VIOLET:\n31 east, 32 south, 36 west.$"

@ <<< Povoamento: fim do bloco gerado <<<
