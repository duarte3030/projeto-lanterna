@ StrangeHouseRooms do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_StrangeHouseRooms_MapScripts::
	.byte 0

Unova_StrangeHouseRooms_EventScript_Placa0::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Placa1::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Placa2::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Placa3::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Placa4::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Placa5::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText, MSGBOX_SIGN
	end

Unova_StrangeHouseRooms_EventScript_Npc0::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseGuyText, MSGBOX_NPC
	end

Unova_StrangeHouseRooms_EventScript_Npc1::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseGuy2Text, MSGBOX_NPC
	end

Unova_StrangeHouseRooms_EventScript_Npc2::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseGirlText, MSGBOX_NPC
	end

Unova_StrangeHouseRooms_EventScript_Npc4::
	msgbox Unova_StrangeHouseRooms_Text_StrangeHouseRoomGhostText, MSGBOX_NPC
	end


Unova_StrangeHouseRooms_Text_StrangeHouseRoomTriggerText::
	.string "Something moved…$"

Unova_StrangeHouseRooms_Text_StrangeHouseGuyText::
	.string "Are you exploring"
	.string "\nthis haunted"
	.string "\lhouse too?"
	.string "\pGet this! I was"
	.string "\nchecking out that"
	.string "\ldesk, when"
	.string "\pall of a sudden,"
	.string "\nthere was a sound!"
	.string "\pWhen I left the"
	.string "\nroom, the furni-"
	.string "\lture outside had"
	.string "\lmoved!"
	.string "\pI'm telling you,"
	.string "\nthis is the work"
	.string "\lof a ghost!$"

Unova_StrangeHouseRooms_Text_StrangeHouseGuy2Text::
	.string "Hmm…"
	.string "\pSo it seems that"
	.string "\nthe furniture will"
	.string "\prearrange itself"
	.string "\nwhen I investigate"
	.string "\lcertain objects…"
	.string "\pThere must be"
	.string "\nsomething in this"
	.string "\lroom too."
	.string "\pMaybe the bed? Or"
	.string "\na bookshelf…?$"

Unova_StrangeHouseRooms_Text_StrangeHouseGirlText::
	.string "I think there must"
	.string "\nbe something"
	.string "\lhidden in the"
	.string "\lback room."
	.string "\pBut the furniture"
	.string "\nalways seems to"
	.string "\lblock the way…"
	.string "\pMaybe if I go"
	.string "\nthrough the"
	.string "\lbasement…$"

Unova_StrangeHouseRooms_Text_StrangeHouseRoomGhostText::
	.string "… … … …"
	.string "\p…That was fun…"
	.string "\pI hope you come"
	.string "\nto play again…$"

@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
Unova_StrangeHouseRooms_EventScript_Troca::
	lock
	faceplayer
	setvar VAR_0x8008, INGAME_TRADE_UNOVA_STRANGE
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set FLAG_UNOVA_TROCA_STRANGE, Unova_StrangeHouseRooms_EventScript_TrocaFeita
	msgbox Unova_Text_Troca3Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_StrangeHouseRooms_EventScript_TrocaNao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, Unova_StrangeHouseRooms_EventScript_TrocaNao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, Unova_StrangeHouseRooms_EventScript_TrocaErrada
	call EventScript_DoInGameTrade
	msgbox Unova_Text_Troca3Complete
	setflag FLAG_UNOVA_TROCA_STRANGE
	release
	end

Unova_StrangeHouseRooms_EventScript_TrocaNao::
	msgbox Unova_Text_Troca3Cancel
	release
	end

Unova_StrangeHouseRooms_EventScript_TrocaErrada::
	msgbox Unova_Text_Troca3Wrong
	release
	end

Unova_StrangeHouseRooms_EventScript_TrocaFeita::
	msgbox Unova_Text_Troca3After
	release
	end
