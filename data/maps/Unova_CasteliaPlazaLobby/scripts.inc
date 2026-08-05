@ CasteliaPlazaLobby do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaPlazaLobby_MapScripts::
	.byte 0

Unova_CasteliaPlazaLobby_EventScript_Placa0::
	msgbox Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbySignText, MSGBOX_SIGN
	end

Unova_CasteliaPlazaLobby_EventScript_Npc0::
	msgbox Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyReceptionist1Text, MSGBOX_NPC
	end

Unova_CasteliaPlazaLobby_EventScript_Npc1::
	msgbox Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyReceptionist2Text, MSGBOX_NPC
	end

Unova_CasteliaPlazaLobby_EventScript_Npc2::
	msgbox Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyCooltrainerMText, MSGBOX_NPC
	end

Unova_CasteliaPlazaLobby_EventScript_Npc3::
	msgbox Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyTeacherText, MSGBOX_NPC
	end


Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbySignText::
	.string "CASTELIA GAME"
	.string "\nPLAZA."
	.string "\p2F - GAME CORNER"
	.string "\n3F - PRIZE ROOM"
	.string "\l4F - RESTAURANT$"

Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyReceptionist1Text::
	.string "Welcome to"
	.string "\nCASTELIA GAME"
	.string "\lPLAZA!"
	.string "\pYou can play games"
	.string "\nupstairs and win"
	.string "\lprizes!$"

Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyReceptionist2Text::
	.string "If you like to"
	.string "\ntravel, make sure"
	.string "\pyou also visit our"
	.string "\nsister store in"
	.string "\lVIRBANK CITY!$"

Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyCooltrainerMText::
	.string "I'm raring to go"
	.string "\nplay the slots"
	.string "\lagain today!"
	.string "\pIt's going to be a"
	.string "\ngood day, I can"
	.string "\lfeel it!$"

Unova_CasteliaPlazaLobby_Text_CasteliaPlazaLobbyTeacherText::
	.string "I prefer the slots"
	.string "\nin this GAME"
	.string "\pCORNER over the"
	.string "\none in VIRBANK"
	.string "\lCITY."
	.string "\pI feel like the"
	.string "\nodds are better"
	.string "\lsomehow.$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd elevatorbutton do BW3G: som e nada mais, igual la
Unova_EventScript_BotaoElevador::
	lockall
	playse SE_PIN
	delay 15
	playse SE_DING_DONG
	waitse
	releaseall
	end
