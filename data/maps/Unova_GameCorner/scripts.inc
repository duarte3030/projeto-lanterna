@ GameCorner do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_GameCorner_MapScripts::
	.byte 0

Unova_GameCorner_EventScript_Placa30::
	msgbox Unova_GameCorner_Text_GameCornerLeftTheirDrinkText, MSGBOX_SIGN
	end

Unova_GameCorner_EventScript_Npc1::
	msgbox Unova_GameCorner_Text_GameCornerPrizeVendorIntroText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc2::
	msgbox Unova_GameCorner_Text_GameCornerPrizeVendorIntroText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc3::
	msgbox Unova_GameCorner_Text_GameCornerPharmacistText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc4::
	msgbox Unova_GameCorner_Text_GameCornerPharmacistText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc5::
	msgbox Unova_GameCorner_Text_GameCornerMusicianText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc6::
	msgbox Unova_GameCorner_Text_GameCornerRoughneckText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc7::
	msgbox Unova_GameCorner_Text_GameCornerPokefanFText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc8::
	msgbox Unova_GameCorner_Text_GameCornerCooltrainerFText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc9::
	msgbox Unova_GameCorner_Text_GameCornerGentlemanText, MSGBOX_NPC
	end

Unova_GameCorner_EventScript_Npc10::
	msgbox Unova_GameCorner_Text_GameCornerPokefanMText, MSGBOX_NPC
	end


Unova_GameCorner_Text_GameCornerLeftTheirDrinkText::
	.string "Someone left their"
	.string "\ndrink."
	.string "\pIt smells sweet.$"

Unova_GameCorner_Text_GameCornerPrizeVendorIntroText::
	.string "Welcome!"
	.string "\pWe exchange your"
	.string "\ngame coins for"
	.string "\lfabulous prizes!$"

Unova_GameCorner_Text_GameCornerPharmacistText::
	.string "I always play this"
	.string "\nslot machine. It"
	.string "\ppays out more than"
	.string "\nothers, I think.$"

Unova_GameCorner_Text_GameCornerMusicianText::
	.string "I just love this"
	.string "\nnew slot machine.$"

Unova_GameCorner_Text_GameCornerRoughneckText::
	.string "Life is a gamble."
	.string "\nI'm going to flip"
	.string "\lcards till I drop!$"

Unova_GameCorner_Text_GameCornerPokefanFText::
	.string "Card flip…"
	.string "\pI prefer it over"
	.string "\nthe slots because"
	.string "\pit's easier to"
	.string "\nfigure the odds."
	.string "\pBut the payout is"
	.string "\nmuch lower.$"

Unova_GameCorner_Text_GameCornerCooltrainerFText::
	.string "I won't quit until"
	.string "\nI win!$"

Unova_GameCorner_Text_GameCornerGentlemanText::
	.string "I used an ICE"
	.string "\nSTONE on my POKé-"
	.string "\lMON."
	.string "\pIt was hard to get"
	.string "\nenough coins for"
	.string "\pit, but it was"
	.string "\nworth it.$"

Unova_GameCorner_Text_GameCornerPokefanMText::
	.string "I'd sure like that"
	.string "\nDEINO, but I don't"
	.string "\pthink I'll ever"
	.string "\nearn enough coins…"
	.string "\pGambling sure is"
	.string "\ntough!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

Unova_GameCorner_EventScript_Maquina0::
	setvar VAR_0x8004, 0
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina1::
	setvar VAR_0x8004, 1
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina2::
	setvar VAR_0x8004, 2
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina3::
	setvar VAR_0x8004, 3
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina4::
	setvar VAR_0x8004, 4
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina5::
	setvar VAR_0x8004, 5
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina6::
	setvar VAR_0x8004, 6
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina7::
	setvar VAR_0x8004, 7
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina8::
	setvar VAR_0x8004, 8
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina9::
	setvar VAR_0x8004, 9
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina10::
	setvar VAR_0x8004, 10
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina11::
	setvar VAR_0x8004, 11
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina12::
	setvar VAR_0x8004, 0
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina13::
	setvar VAR_0x8004, 1
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina14::
	setvar VAR_0x8004, 2
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina15::
	setvar VAR_0x8004, 3
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina16::
	setvar VAR_0x8004, 4
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina17::
	setvar VAR_0x8004, 5
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina18::
	setvar VAR_0x8004, 6
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina19::
	setvar VAR_0x8004, 7
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina20::
	setvar VAR_0x8004, 8
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina21::
	setvar VAR_0x8004, 9
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina22::
	setvar VAR_0x8004, 10
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina23::
	setvar VAR_0x8004, 11
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina24::
	setvar VAR_0x8004, 0
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina25::
	setvar VAR_0x8004, 1
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina26::
	setvar VAR_0x8004, 2
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina27::
	setvar VAR_0x8004, 3
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina28::
	setvar VAR_0x8004, 4
	goto Unova_EventScript_CacaNiquel

Unova_GameCorner_EventScript_Maquina29::
	setvar VAR_0x8004, 5
	goto Unova_EventScript_CacaNiquel
