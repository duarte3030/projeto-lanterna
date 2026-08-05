@ ESCONDERIJO DA ROCKET em MAHOGANY, B2F. Planta do pokecrystal
@ (maps/TeamRocketBaseB2F.blk), texto de maps/TeamRocketBaseB2F.asm.
@ 06/08/2026: os seis ELECTRODE entraram, ZERO var. Cada um é um coord_event
@ com gatilho VAR_TEMP_0 = 0 (o motor zera VAR_TEMP_0 a cada entrada de mapa,
@ então o gatilho vale sempre e não gasta var nenhuma) e uma
@ FLAG_MAHOGANY_ELECTRODE_1..6 para não renascer. Ficam nos mesmos seis tiles
@ do pokecrystal, (7,5)/(7,7)/(7,9) e (22,5)/(22,7)/(22,9), os dois corredores
@ que ladeiam o transmissor. Não são objeto: esta build não desenha ELECTRODE
@ no overworld, então em vez de sprite o jogador pisa no tile e leva o grito e
@ a batalha, que é o efeito que importa. A cena grande da ARIANA com o LANCE e
@ o DRAGONITE continua fora (depende de VAR_MAHOGANY_TOWN_STATE), e derrubar
@ os seis NÃO abre nada: quem abre a porta do transmissor continua sendo o
@ setmetatile do ON_LOAD com as duas senhas do B3F. Ficou o que dá para jogar sem var nenhuma:
@ a ARIANA é treinadora normal, e a porta do transmissor abre por setmetatile
@ no ON_LOAD assim que as DUAS senhas do B3F foram arrancadas.
@ O metatile 552 é o chão do gTileset_Facility (o mesmo do AquaHideout).

MahoganyHideout_B2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MahoganyHideout_B2F_OnLoad
	.byte 0

MahoganyHideout_B2F_OnLoad:
	goto_if_set FLAG_MAHOGANY_HIDEOUT_DOOR_B2F, MahoganyHideout_B2F_EventScript_PoePortaAberta
	end

MahoganyHideout_B2F_EventScript_PoePortaAberta::
	setmetatile 14, 12, 552, FALSE
	setmetatile 15, 12, 552, FALSE
	end

MahoganyHideout_B2F_EventScript_Porta::
	lockall
	goto_if_set FLAG_MAHOGANY_HIDEOUT_DOOR_B2F, MahoganyHideout_B2F_EventScript_PortaJaAberta
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_5, MahoganyHideout_B2F_EventScript_PortaSemSenha
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_6, MahoganyHideout_B2F_EventScript_PortaSemSenha
	msgbox MahoganyHideout_B2F_Text_PortaAbre, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	setflag FLAG_MAHOGANY_HIDEOUT_DOOR_B2F
	setmetatile 14, 12, 552, FALSE
	setmetatile 15, 12, 552, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

MahoganyHideout_B2F_EventScript_PortaSemSenha::
	msgbox MahoganyHideout_B2F_Text_PortaSemSenha, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B2F_EventScript_PortaJaAberta::
	releaseall
	end

MahoganyHideout_B2F_EventScript_Electrode1::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_1, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_1
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_Electrode2::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_2, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_2
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_Electrode3::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_3, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_3
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_Electrode4::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_4, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_4
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_Electrode5::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_5, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_5
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_Electrode6::
	goto_if_set FLAG_MAHOGANY_ELECTRODE_6, MahoganyHideout_B2F_EventScript_ElectrodeGasto
	setflag FLAG_MAHOGANY_ELECTRODE_6
	goto MahoganyHideout_B2F_EventScript_ElectrodeBatalha

MahoganyHideout_B2F_EventScript_ElectrodeGasto::
	end

MahoganyHideout_B2F_EventScript_ElectrodeBatalha::
	lockall
	setwildbattle SPECIES_ELECTRODE, 23
	waitse
	playmoncry SPECIES_ELECTRODE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	dowildbattle
	releaseall
	end

MahoganyHideout_B2F_EventScript_Transmissor::
	lockall
	goto_if_set FLAG_HIDE_MAHOGANY_HIDEOUT_ROCKETS, MahoganyHideout_B2F_EventScript_TransmissorMorto
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_PETREL_MAHOGANY, MahoganyHideout_B2F_EventScript_TransmissorTrancado
	msgbox MahoganyHideout_B2F_Text_TransmissorLigado, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_HIDE_MAHOGANY_HIDEOUT_ROCKETS
	playse SE_PC_LOGIN
	removeobject LOCALID_MAHOGANY_HIDEOUT_B2F_GRUNT1
	removeobject LOCALID_MAHOGANY_HIDEOUT_B2F_GRUNT2
	removeobject LOCALID_MAHOGANY_HIDEOUT_B2F_GRUNT3
	removeobject LOCALID_MAHOGANY_HIDEOUT_B2F_ARIANA
	delay 60
	fadescreen FADE_FROM_BLACK
	special DrawWholeMapView
	msgbox MahoganyHideout_B2F_Text_TransmissorMorto, MSGBOX_DEFAULT
	msgbox MahoganyHideout_B2F_Text_LanceRadioTower, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B2F_EventScript_TransmissorTrancado::
	msgbox MahoganyHideout_B2F_Text_TransmissorGuardado, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B2F_EventScript_TransmissorMorto::
	msgbox MahoganyHideout_B2F_Text_TransmissorMorto, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B2F_EventScript_Lance::
	lock
	faceplayer
	msgbox MahoganyHideout_B2F_Text_LanceHeal1, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_WHITE
	playse SE_USE_ITEM
	special HealPlayerParty
	waitse
	fadescreen FADE_FROM_WHITE
	msgbox MahoganyHideout_B2F_Text_LanceHeal2, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyHideout_B2F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_2, MahoganyHideout_B2F_Text_Grunt1Seen, MahoganyHideout_B2F_Text_Grunt1Beaten
	msgbox MahoganyHideout_B2F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B2F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_3, MahoganyHideout_B2F_Text_Grunt2Seen, MahoganyHideout_B2F_Text_Grunt2Beaten
	msgbox MahoganyHideout_B2F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B2F_EventScript_Grunt3::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_4, MahoganyHideout_B2F_Text_Grunt3Seen, MahoganyHideout_B2F_Text_Grunt3Beaten
	msgbox MahoganyHideout_B2F_Text_Grunt3After, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B2F_EventScript_Ariana::
	trainerbattle_single TRAINER_JOHTO_ROCKET_ARIANA_MAHOGANY, MahoganyHideout_B2F_Text_ArianaSeen, MahoganyHideout_B2F_Text_ArianaBeaten
	msgbox MahoganyHideout_B2F_Text_ArianaAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B2F_Text_LanceHeal1:
	.string "LANCE: Are you all right?\p"
	.string "Your POKéMON are hurt and tired.\p"
	.string "Here, give them some of my\n"
	.string "medicine.$"

MahoganyHideout_B2F_Text_LanceHeal2:
	.string "LANCE: {PLAYER}, let's give it our\n"
	.string "best for POKéMON.\p"
	.string "The stairs on the far side lead\n"
	.string "deeper in. I will keep looking here.$"

MahoganyHideout_B2F_Text_Grunt1Seen:
	.string "The door won't open?\p"
	.string "Well, duh.\n"
	.string "It has to have a password that only\l"
	.string "TEAM ROCKET knows.$"

MahoganyHideout_B2F_Text_Grunt1Beaten:
	.string "What? I lost?$"

MahoganyHideout_B2F_Text_Grunt1After:
	.string "Heh, I'm just a GRUNT.\p"
	.string "I don't know the password.\n"
	.string "Too bad for you.$"

MahoganyHideout_B2F_Text_Grunt2Seen:
	.string "Oh, a kid? I don't really like this,\n"
	.string "but eliminate you I must.$"

MahoganyHideout_B2F_Text_Grunt2Beaten:
	.string "I knew I'd lose…$"

MahoganyHideout_B2F_Text_Grunt2After:
	.string "I got wiped out on the last mission\n"
	.string "by a kid too.\p"
	.string "This kid with long red hair and\n"
	.string "mean-looking eyes just creamed me…$"

MahoganyHideout_B2F_Text_Grunt3Seen:
	.string "You rotten little pest!$"

MahoganyHideout_B2F_Text_Grunt3Beaten:
	.string "Grrrr…$"

MahoganyHideout_B2F_Text_Grunt3After:
	.string "Heh, only the boss knows the\n"
	.string "password for that door.\p"
	.string "Where's the boss? Who knows?\n"
	.string "Go look for yourself.$"

MahoganyHideout_B2F_Text_ArianaSeen:
	.string "Hold it right there, little one.\p"
	.string "You are meddling with TEAM ROCKET.\n"
	.string "That is a mistake you make once.$"

MahoganyHideout_B2F_Text_ArianaBeaten:
	.string "You brat! How dare you!$"

MahoganyHideout_B2F_Text_ArianaAfter:
	.string "Don't get carried away.\p"
	.string "TEAM ROCKET is bigger than this\n"
	.string "hideout, and you will learn that.$"

MahoganyHideout_B2F_Text_PortaSemSenha:
	.string "The door's closed…\p"
	.string "It needs a password to open.$"

MahoganyHideout_B2F_Text_PortaAbre:
	.string "The door's closed…\p"
	.string "{PLAYER} entered the password.\p"
	.string "The door opened!$"

MahoganyHideout_B2F_Text_TransmissorGuardado:
	.string "It's the radio transmitter that's\n"
	.string "sending the sinister signal.\p"
	.string "It's working at full capacity, and\n"
	.string "the controls are locked.$"

MahoganyHideout_B2F_Text_TransmissorLigado:
	.string "It's the radio transmitter that's\n"
	.string "sending the sinister signal.\p"
	.string "With the executive gone, the\n"
	.string "controls answer.\p"
	.string "{PLAYER} shut the transmitter down.$"

MahoganyHideout_B2F_Text_TransmissorMorto:
	.string "The radio transmitter has finally\n"
	.string "stopped its evil broadcast.$"

MahoganyHideout_B2F_Text_LanceRadioTower:
	.string "LANCE: Well done. The signal that\n"
	.string "maddened the POKéMON is dead.\p"
	.string "But TEAM ROCKET is not.\p"
	.string "They have seized the RADIO TOWER\n"
	.string "in GOLDENROD CITY.\p"
	.string "Go there, {PLAYER}. I will follow.$"
