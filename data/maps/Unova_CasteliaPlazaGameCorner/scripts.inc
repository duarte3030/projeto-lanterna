@ CasteliaPlazaGameCorner do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaPlazaGameCorner_MapScripts::
	.byte 0

Unova_CasteliaPlazaGameCorner_EventScript_Placa24::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerSignText, MSGBOX_SIGN
	end

Unova_CasteliaPlazaGameCorner_EventScript_Npc1::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerReceptionistText, MSGBOX_NPC
	end

Unova_CasteliaPlazaGameCorner_EventScript_Npc2::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerTeacherText, MSGBOX_NPC
	end

Unova_CasteliaPlazaGameCorner_EventScript_Npc3::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerPokefanMText, MSGBOX_NPC
	end

Unova_CasteliaPlazaGameCorner_EventScript_Npc4::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerSuperNerdText, MSGBOX_NPC
	end

Unova_CasteliaPlazaGameCorner_EventScript_Npc5::
	msgbox Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerFisherText1, MSGBOX_NPC
	end


Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerSignText::
	.string "CASTELIA PLAZA"
	.string "\nGAME CORNER."
	.string "\pEarn coins to win"
	.string "\nfabulous prizes!$"

Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerReceptionistText::
	.string "Welcome!"
	.string "\pYou may exchange"
	.string "\nyour coins for"
	.string "\pfabulous prizes"
	.string "\nupstairs.$"

Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerTeacherText::
	.string "It's this machine"
	.string "\nI want."
	.string "\pIt cleaned me out"
	.string "\nyesterday, so it"
	.string "\pshould pay out"
	.string "\ntoday.$"

Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerPokefanMText::
	.string "Hmmm… The odds are"
	.string "\nsurely better for"
	.string "\pPIKACHU's line,"
	.string "\nbut… What to do?$"

Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerSuperNerdText::
	.string "I think this slot"
	.string "\nmachine will pay"
	.string "\lout…"
	.string "\pThe odds vary"
	.string "\namong machines.$"

Unova_CasteliaPlazaGameCorner_Text_CasteliaPlazaGameCornerFisherText1::
	.string "Gahahaha!"
	.string "\pThe coins just"
	.string "\nkeep popping out!"
	.string "\pHm? What, kid? You"
	.string "\nwant to play?"
	.string "\pI'll share my luck"
	.string "\nwith you!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Maquina de cassino do BW3G. O `special SlotMachine` do gen 2 vira o
@ caca-niquel que este repo ja tem em MauvilleCity_GameCorner; quem chama define
@ VAR_0x8004 (0 a 11) com o numero da maquina, que e o que da a sorte de cada uma.
@ ponytail: o card flip do BW3G cai aqui tambem, porque este repo nao tem
@ segundo minijogo de cassino. O certo seria portar o card flip.
Unova_EventScript_CacaNiquel::
	lockall
	checkitem ITEM_COIN_CASE
	goto_if_eq VAR_RESULT, FALSE, MauvilleCity_GameCorner_EventScript_NoCoinCase
	specialvar VAR_RESULT, GetSlotMachineId
	playslotmachine VAR_RESULT
	releaseall
	end

Unova_CasteliaPlazaGameCorner_EventScript_Maquina0::
	setvar VAR_0x8004, 0
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina1::
	setvar VAR_0x8004, 1
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina2::
	setvar VAR_0x8004, 2
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina3::
	setvar VAR_0x8004, 3
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina4::
	setvar VAR_0x8004, 4
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina5::
	setvar VAR_0x8004, 5
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina6::
	setvar VAR_0x8004, 6
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina7::
	setvar VAR_0x8004, 7
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina8::
	setvar VAR_0x8004, 8
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina9::
	setvar VAR_0x8004, 9
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina10::
	setvar VAR_0x8004, 10
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina11::
	setvar VAR_0x8004, 11
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina12::
	setvar VAR_0x8004, 0
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina13::
	setvar VAR_0x8004, 1
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina14::
	setvar VAR_0x8004, 2
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina15::
	setvar VAR_0x8004, 3
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina16::
	setvar VAR_0x8004, 4
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina17::
	setvar VAR_0x8004, 5
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina18::
	setvar VAR_0x8004, 6
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina19::
	setvar VAR_0x8004, 7
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina20::
	setvar VAR_0x8004, 8
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina21::
	setvar VAR_0x8004, 9
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina22::
	setvar VAR_0x8004, 10
	goto Unova_EventScript_CacaNiquel

Unova_CasteliaPlazaGameCorner_EventScript_Maquina23::
	setvar VAR_0x8004, 11
	goto Unova_EventScript_CacaNiquel
