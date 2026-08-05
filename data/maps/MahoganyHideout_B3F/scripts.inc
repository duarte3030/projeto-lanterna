@ ESCONDERIJO DA ROCKET em MAHOGANY, B3F. Planta do pokecrystal
@ (maps/TeamRocketBaseB3F.blk), texto de maps/TeamRocketBaseB3F.asm.
@ ponytail: o rival e o MURKROW que canta a senha não entraram. O rival precisa
@ de VAR_STARTER_MON e de três treinadores, e o MURKROW não tem sprite fora de
@ #if IS_FRLG. As duas senhas ficaram onde estavam, na boca dos dois grunts, e
@ quem lembra que você venceu os dois é goto_if_defeated, não var.
@ A porta do escritório abre por setmetatile no ON_LOAD. 552 = chão do Facility.

MahoganyHideout_B3F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, MahoganyHideout_B3F_OnLoad
	.byte 0

MahoganyHideout_B3F_OnLoad:
	goto_if_set FLAG_MAHOGANY_HIDEOUT_DOOR_B3F, MahoganyHideout_B3F_EventScript_PoePortaAberta
	end

MahoganyHideout_B3F_EventScript_PoePortaAberta::
	setmetatile 10, 9, 552, FALSE
	setmetatile 11, 9, 552, FALSE
	end

MahoganyHideout_B3F_EventScript_Porta::
	lockall
	goto_if_set FLAG_MAHOGANY_HIDEOUT_DOOR_B3F, MahoganyHideout_B3F_EventScript_PortaJaAberta
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_5, MahoganyHideout_B3F_EventScript_PortaSemSenha
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_6, MahoganyHideout_B3F_EventScript_PortaSemSenha
	msgbox MahoganyHideout_B3F_Text_PortaAbre, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	setflag FLAG_MAHOGANY_HIDEOUT_DOOR_B3F
	setmetatile 10, 9, 552, FALSE
	setmetatile 11, 9, 552, FALSE
	special DrawWholeMapView
	waitse
	releaseall
	end

MahoganyHideout_B3F_EventScript_PortaSemSenha::
	msgbox MahoganyHideout_B3F_Text_PortaSemSenha, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B3F_EventScript_PortaJaAberta::
	releaseall
	end

MahoganyHideout_B3F_EventScript_Lance::
	lock
	faceplayer
	msgbox MahoganyHideout_B3F_Text_Lance, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyHideout_B3F_EventScript_Caido::
	lock
	faceplayer
	msgbox MahoganyHideout_B3F_Text_Caido, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyHideout_B3F_EventScript_Senha1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_5, MahoganyHideout_B3F_Text_Senha1Seen, MahoganyHideout_B3F_Text_Senha1Beaten
	msgbox MahoganyHideout_B3F_Text_Senha1After, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B3F_EventScript_Senha2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_6, MahoganyHideout_B3F_Text_Senha2Seen, MahoganyHideout_B3F_Text_Senha2Beaten
	msgbox MahoganyHideout_B3F_Text_Senha2After, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B3F_EventScript_Ross::
	trainerbattle_single TRAINER_JOHTO_SCIENTIST_ROSS, MahoganyHideout_B3F_Text_RossSeen, MahoganyHideout_B3F_Text_RossBeaten
	msgbox MahoganyHideout_B3F_Text_RossAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B3F_EventScript_Mitch::
	trainerbattle_single TRAINER_JOHTO_SCIENTIST_MITCH, MahoganyHideout_B3F_Text_MitchSeen, MahoganyHideout_B3F_Text_MitchBeaten
	msgbox MahoganyHideout_B3F_Text_MitchAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B3F_EventScript_Petrel::
	lock
	faceplayer
	goto_if_defeated TRAINER_JOHTO_ROCKET_PETREL_MAHOGANY, MahoganyHideout_B3F_EventScript_PetrelDone
	msgbox MahoganyHideout_B3F_Text_PetrelSeen, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_PETREL_MAHOGANY, MahoganyHideout_B3F_Text_PetrelBeaten
	msgbox MahoganyHideout_B3F_Text_PetrelAfter, MSGBOX_DEFAULT
	closemessage
	delay 30
	playse SE_EXIT
	removeobject LOCALID_MAHOGANY_HIDEOUT_B3F_PETREL
	release
	end

MahoganyHideout_B3F_EventScript_PetrelDone::
	msgbox MahoganyHideout_B3F_Text_PetrelAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyHideout_B3F_EventScript_Juramento::
	lockall
	msgbox MahoganyHideout_B3F_Text_Juramento, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B3F_Text_Lance:
	.string "LANCE: It takes two passwords to\n"
	.string "get into the boss's quarters.\p"
	.string "Those passwords are known only to\n"
	.string "a few ROCKETS.\p"
	.string "That ROCKET there very graciously\n"
	.string "told me so.\p"
	.string "{PLAYER}, let's go get the\n"
	.string "passwords.$"

MahoganyHideout_B3F_Text_Caido:
	.string "Urrggh… The guy in the cape is\n"
	.string "incredibly tough…$"

MahoganyHideout_B3F_Text_Senha1Seen:
	.string "Do I know the password?\p"
	.string "Maybe.\p"
	.string "But no weakling's going to get it!$"

MahoganyHideout_B3F_Text_Senha1Beaten:
	.string "All right. Stop.\n"
	.string "I'll tell you.$"

MahoganyHideout_B3F_Text_Senha1After:
	.string "The password to the boss's room is\n"
	.string "SLOWPOKETAIL.\p"
	.string "But it's useless unless you have\n"
	.string "two passwords.$"

MahoganyHideout_B3F_Text_Senha2Seen:
	.string "Hyuck-hyuck-hyuck!\p"
	.string "You're challenging me to a battle?\p"
	.string "Hah! You're nuts, but you have guts!\p"
	.string "If you can beat me, I'll tell you\n"
	.string "a password to the boss's room!$"

MahoganyHideout_B3F_Text_Senha2Beaten:
	.string "Hyuck-hyuck-hyuck!\n"
	.string "You're good!$"

MahoganyHideout_B3F_Text_Senha2After:
	.string "Hyuck-hyuck-hyuck!\p"
	.string "The password to the boss's room…\p"
	.string "Uh…, I think it is RATICATE TAIL.$"

MahoganyHideout_B3F_Text_RossSeen:
	.string "I used to work for SILPH, but now I\n"
	.string "run research for TEAM ROCKET.\p"
	.string "A meddlesome child like you needs\n"
	.string "to be punished.$"

MahoganyHideout_B3F_Text_RossBeaten:
	.string "A mere tactical error cost me…$"

MahoganyHideout_B3F_Text_RossAfter:
	.string "A radio signal that drives POKéMON\n"
	.string "mad…\p"
	.string "My experiment is a complete\n"
	.string "success.$"

MahoganyHideout_B3F_Text_MitchSeen:
	.string "You should not be down here.\p"
	.string "I will have to erase you from the\n"
	.string "record myself.$"

MahoganyHideout_B3F_Text_MitchBeaten:
	.string "My data was flawed…$"

MahoganyHideout_B3F_Text_MitchAfter:
	.string "The MAGIKARP in the LAKE OF RAGE\n"
	.string "evolved because of our signal.\p"
	.string "Sell the GYARADOS, sell the scales.\n"
	.string "That is all TEAM ROCKET wanted.$"

MahoganyHideout_B3F_Text_PetrelSeen:
	.string "What? Who are you?\n"
	.string "This is the office of our leader,\l"
	.string "GIOVANNI.\p"
	.string "Since disbanding TEAM ROCKET three\n"
	.string "years ago, he has been in training.\p"
	.string "But we're certain he will be back\n"
	.string "some day to assume command again.\p"
	.string "That's why we're standing guard.\p"
	.string "I won't let anyone disturb this\n"
	.string "place!$"

MahoganyHideout_B3F_Text_PetrelBeaten:
	.string "I… I couldn't do a thing…\p"
	.string "GIOVANNI, please forgive me…$"

MahoganyHideout_B3F_Text_PetrelAfter:
	.string "No, I can't let this affect me.\p"
	.string "I have to inform the others…\p"
	.string "The transmitter on the floor above\n"
	.string "is yours now. Much good may it do.$"

MahoganyHideout_B3F_Text_PortaSemSenha:
	.string "The door's closed…\p"
	.string "It needs two passwords to open.$"

MahoganyHideout_B3F_Text_PortaAbre:
	.string "The door's closed…\p"
	.string "{PLAYER} entered SLOWPOKETAIL and\n"
	.string "RATICATE TAIL.\p"
	.string "The door opened!$"

MahoganyHideout_B3F_Text_Juramento:
	.string "It's the TEAM ROCKET oath.\p"
	.string "Steal POKéMON for profit.\p"
	.string "Exploit POKéMON for profit.\p"
	.string "All POKéMON exist for the glory of\n"
	.string "TEAM ROCKET.$"
