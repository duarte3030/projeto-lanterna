@ OpelucidBattleHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_OpelucidBattleHouse_MapScripts::
	.byte 0

Unova_OpelucidBattleHouse_EventScript_Placa0::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseStatueText, MSGBOX_SIGN
	end

Unova_OpelucidBattleHouse_EventScript_Placa1::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseStatueText, MSGBOX_SIGN
	end

Unova_OpelucidBattleHouse_EventScript_Npc0::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseGymGuyText, MSGBOX_NPC
	end

Unova_OpelucidBattleHouse_EventScript_Npc1::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseMarlonIntroText, MSGBOX_NPC
	end

Unova_OpelucidBattleHouse_EventScript_Npc2::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseBurghIntroText, MSGBOX_NPC
	end

Unova_OpelucidBattleHouse_EventScript_Npc3::
	msgbox Unova_OpelucidBattleHouse_Text_BattleHouseCilanIntroText, MSGBOX_NPC
	end


Unova_OpelucidBattleHouse_Text_BattleHouseStatueText::
	.string "OPELUCID CITY"
	.string "\nBATTLE HOUSE"
	.string "\pWhere the best"
	.string "\ncome to battle!$"

Unova_OpelucidBattleHouse_Text_BattleHouseGymGuyText::
	.string "Hi, welcome to the"
	.string "\nBATTLE HOUSE!"
	.string "\pGYM LEADERS from"
	.string "\nall over UNOVA"
	.string "\pcome here to spar"
	.string "\nwith each other!"
	.string "\pA different LEADER"
	.string "\ncomes by each day,"
	.string "\pso you never know"
	.string "\nwho you'll be up"
	.string "\lagainst!"
	.string "\pHow exciting!$"

Unova_OpelucidBattleHouse_Text_BattleHouseMarlonIntroText::
	.string "Hey there,"
	.string "\n{PLAYER}!"
	.string "\pYou ready for a"
	.string "\nbattle? Show me"
	.string "\lwhat you've got!$"

Unova_OpelucidBattleHouse_Text_BattleHouseBurghIntroText::
	.string "Why hello there,"
	.string "\nyoung trainer!"
	.string "\pHow would you like"
	.string "\nto experience the"
	.string "\pincredible art-"
	.string "\nistry of my POKé-"
	.string "\lMON and I?$"

Unova_OpelucidBattleHouse_Text_BattleHouseCilanIntroText::
	.string "I've been working"
	.string "\non a recipe for a"
	.string "\pnew type of POKé-"
	.string "\nMON strategy."
	.string "\pHere, I'll give"
	.string "\nyou a taste!$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_OpelucidBattleHouse_EventScript_CHEREN_2::
	trainerbattle_single TRAINER_UNOVA_CHEREN_2, Unova_OpelucidBattleHouse_Text_CHEREN_2Seen, Unova_OpelucidBattleHouse_Text_CHEREN_2Beaten
	msgbox Unova_OpelucidBattleHouse_Text_CHEREN_2Depois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_CHEREN_2
	removeobject LOCALID_UNOVA_OPELUCID_CHEREN
	release
	end

Unova_OpelucidBattleHouse_Text_CHEREN_2Seen::
	.string "Ah, {PLAYER}.\n"
	.string "Welcome to the\l"
	.string "BATTLE HOUSE.\p"
	.string "How'd you like to\n"
	.string "be my opponent\l"
	.string "today?$"

Unova_OpelucidBattleHouse_Text_CHEREN_2Beaten::
	.string "I see, so that was\n"
	.string "your strategy.$"

Unova_OpelucidBattleHouse_Text_CHEREN_2Depois::
	.string "If you want to be\n"
	.string "a great POKéMON\l"
	.string "trainer, you've got\l"
	.string "to keep improving\l"
	.string "yourself.$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
