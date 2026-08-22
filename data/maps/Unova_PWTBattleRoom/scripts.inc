@ PWTBattleRoom do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PWTBattleRoom_MapScripts::
	.byte 0

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_PWTBattleRoom_EventScript_BIANCA::
	trainerbattle_single TRAINER_UNOVA_BIANCA, Unova_PWTBattleRoom_Text_BIANCASeen, Unova_PWTBattleRoom_Text_BIANCABeaten
	msgbox Unova_PWTBattleRoom_Text_BIANCADepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_BIANCA
	removeobject LOCALID_UNOVA_PWT_BIANCA
	release
	end

Unova_PWTBattleRoom_Text_BIANCASeen::
	.string "BIANCA: Now I'll\n"
	.string "get to see first\l"
	.string "hand how strong of\l"
	.string "a trainer you've\l"
	.string "become, {PLAYER}!$"

Unova_PWTBattleRoom_Text_BIANCABeaten::
	.string "Oh! You are good!$"

Unova_PWTBattleRoom_Text_BIANCADepois::
	.string "BIANCA: Wow, you\n"
	.string "are good! MARLON\l"
	.string "sure was right to\l"
	.string "pick you to be a\l"
	.string "POKéMON trainer!$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
