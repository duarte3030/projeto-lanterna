@ NuvemaLab do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NuvemaLab_MapScripts::
	.byte 0

Unova_NuvemaLab_EventScript_Placa2::
	msgbox Unova_NuvemaLab_Text_BiancasLabFridgeText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa3::
	msgbox Unova_NuvemaLab_Text_BiancasLabSinkText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa4::
	msgbox Unova_NuvemaLab_Text_BiancasLabStoveText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Placa5::
	msgbox Unova_NuvemaLab_Text_BiancasLabPCText, MSGBOX_SIGN
	end

Unova_NuvemaLab_EventScript_Npc0::
	msgbox Unova_NuvemaLab_Text_BiancaLabP2LocationText, MSGBOX_NPC
	end

Unova_NuvemaLab_EventScript_Npc1::
	msgbox Unova_NuvemaLab_Text_BiancasAssistant1Text, MSGBOX_NPC
	end

Unova_NuvemaLab_EventScript_Npc2::
	msgbox Unova_NuvemaLab_Text_BiancasAssistant2Text, MSGBOX_NPC
	end


Unova_NuvemaLab_Text_BiancasLabFridgeText::
	.string "It's the PROF's"
	.string "\nfridge!"
	.string "\pBetter not snoop"
	.string "\naround in here…$"

Unova_NuvemaLab_Text_BiancasLabSinkText::
	.string "There are dishes"
	.string "\nand glass bottles"
	.string "\lin the sink."
	.string "\pSomeone should"
	.string "\nreally clean this"
	.string "\lup!$"

Unova_NuvemaLab_Text_BiancasLabStoveText::
	.string "It looks like the"
	.string "\nstove hasn't been"
	.string "\lused in a while…$"

Unova_NuvemaLab_Text_BiancasLabPCText::
	.string "There's an e-mail"
	.string "\nmessage on the PC."
	.string "\p…"
	.string "\pPROF.BIANCA, I"
	.string "\ngot news about"
	.string "\lthat thing…"
	.string "\pThere was a break"
	.string "\nin at my GYM. I"
	.string "\lthink someone was"
	.string "\ptryin' ta get"
	.string "\ntheir hands on"
	.string "\lthat thing."
	.string "\pI'm gonna move"
	.string "\nit to a more"
	.string "\lsecure place."
	.string "\pOnly members of"
	.string "\nthe POKéMON league"
	.string "\lwill be able to"
	.string "\lget to it."
	.string "\pThis thing is"
	.string "\nturnin' out to be"
	.string "\la load of trouble…"
	.string "\pThanks for the"
	.string "\nPOKéDEX, by the"
	.string "\lway. {PLAYER}"
	.string "\lis a natural!"
	.string "\pGood vibes,"
	.string "\n-MARLON$"

Unova_NuvemaLab_Text_BiancaLabP2LocationText::
	.string "BIANCA: Are you"
	.string "\ngoing to join"
	.string "\pPROF.JUNIPER at"
	.string "\nthat secret lab?"
	.string "\pYou can reach"
	.string "\nROUTE 17 if you"
	.string "\pgo north, then"
	.string "\ncross the water"
	.string "\lto the west.$"

Unova_NuvemaLab_Text_BiancasAssistant1Text::
	.string "Whew, I've got a"
	.string "\nlot to keep up"
	.string "\pwith. The PROF's"
	.string "\nalways busy with"
	.string "\lsomething!$"

Unova_NuvemaLab_Text_BiancasAssistant2Text::
	.string "The PROF is young,"
	.string "\nbut she's done a"
	.string "\lgreat job so far!$"

@ Trecho devolvido em 06/08/2026: o commit das placas (febde977c3)
@ reescreveu este arquivo a partir da fonte do BW3G e levou junto os
@ scripts dos tres iniciais, que nao vem do BW3G e sim da decisao 68 do Gui.
Unova_NuvemaLab_EventScript_BallSnivy::
	lock
	faceplayer
	showmonpic SPECIES_SNIVY, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_SNIVY
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_SNIVY, 70
	setvar VAR_STARTER_MON, 0
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_BallTepig::
	lock
	faceplayer
	showmonpic SPECIES_TEPIG, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_TEPIG
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_TEPIG, 70
	setvar VAR_STARTER_MON, 1
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_BallOshawott::
	lock
	faceplayer
	showmonpic SPECIES_OSHAWOTT, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_OSHAWOTT
	msgbox Unova_NuvemaLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_OSHAWOTT, 70
	setvar VAR_STARTER_MON, 2
	goto Unova_NuvemaLab_EventScript_ChoseStarter

Unova_NuvemaLab_EventScript_DeclinedStarter::
	hidemonpic
	release
	end

Unova_NuvemaLab_EventScript_ChoseStarter::
	setflag FLAG_INICIAL_UNOVA
	setflag FLAG_SYS_POKEMON_GET
	message Unova_NuvemaLab_Text_ReceivedStarter
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_NuvemaLab_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call Common_EventScript_NameReceivedPartyMon
	goto Unova_NuvemaLab_EventScript_AfterStarter

Unova_NuvemaLab_EventScript_AfterStarter::
	removeobject LOCALID_JUNIPER_LAB_BALL_SNIVY
	removeobject LOCALID_JUNIPER_LAB_BALL_TEPIG
	removeobject LOCALID_JUNIPER_LAB_BALL_OSHAWOTT
	release
	end

@ Aviso mecanico, nao e fala do BW3G.
Unova_NuvemaLab_Text_WillYouTakeThisOne::
	.string "This POKé BALL holds a\n"
	.string "{STR_VAR_1}.\p"
	.string "Will you take this one?$"

@ Aviso mecanico, nao e fala do BW3G.
Unova_NuvemaLab_Text_ReceivedStarter::
	.string "{PLAYER} received the\n"
	.string "{STR_VAR_1}!$"
