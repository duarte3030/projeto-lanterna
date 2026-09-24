@ Route122_Ex26_0: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 26.0) por dev_scripts/copia_planta_ex.py.

Route122_Ex26_0_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 26.0), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route122_Ex26_0_EventScript_ExNpc3::
	msgbox Route122_Ex26_0_Text_ExNpc3, MSGBOX_NPC
	end

Route122_Ex26_0_Text_ExNpc3:
	.string "I am resting here before I travel up the\n"
	.string "mountain.$"

Route122_Ex26_0_EventScript_ExNpc4::
	msgbox Route122_Ex26_0_Text_ExNpc4, MSGBOX_NPC
	end

Route122_Ex26_0_Text_ExNpc4:
	.string "The community here wouldn’t exist\n"
	.string "without this little rest stop.\p"
	.string "We’d all have to move to a real town if\n"
	.string "we weren’t able to heal our POKéMON!$"


@ AVA do EX (26.0): treinador de conversa que cura o time depois da batalha; reescrito do
@ bytecode e do texto da ROM (trainerbattle, msgbox, a cura comum, msgbox), na ordem do EX.
Route122_Ex26_0_EventScript_ExAva::
	trainerbattle_single TRAINER_HOENNEX_ROUTE122_EX26_0_AVA, Route122_Ex26_0_Text_ExAvaIntro, Route122_Ex26_0_Text_ExAvaDefeat
	msgbox Route122_Ex26_0_Text_ExAvaVouCurar, MSGBOX_AUTOCLOSE
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox Route122_Ex26_0_Text_ExAvaRespeite, MSGBOX_AUTOCLOSE
	end

Route122_Ex26_0_Text_ExAvaIntro:
	.string "The path up MT. PYRE is a treacherous\n"
	.string "one.\p"
	.string "Only the worthy may travel it.\p"
	.string "Prove your worth and I shall assist you.$"

Route122_Ex26_0_Text_ExAvaDefeat:
	.string "There have been many unworthy GRUNTS\n"
	.string "around recently. I needed to be sure\l"
	.string "you were kindhearted.$"

Route122_Ex26_0_Text_ExAvaVouCurar:
	.string "I shall now restore your POKéMON.$"

Route122_Ex26_0_Text_ExAvaRespeite:
	.string "Please, respect the departed on the\n"
	.string "mountain.$"

