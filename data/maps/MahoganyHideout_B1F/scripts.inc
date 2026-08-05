@ ESCONDERIJO DA ROCKET em MAHOGANY, B1F. A planta veio do pokecrystal
@ (maps/TeamRocketBaseB1F.blk), convertida por dev_scripts/demake_gen2.py, e o
@ texto veio de maps/TeamRocketBaseB1F.asm do mesmo disassembly.
@ ponytail: as 22 armadilhas de piso e as 5 câmeras de segurança do original
@ ficaram de fora. Cada uma é um coord_event, e coord_event exige uma var; a
@ instrução desta tarefa é zero var. As estátuas de PERSIAN viraram placa.

MahoganyHideout_B1F_MapScripts::
	.byte 0

MahoganyHideout_B1F_EventScript_Grunt::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_MAHOGANY_1, MahoganyHideout_B1F_Text_GruntSeen, MahoganyHideout_B1F_Text_GruntBeaten
	msgbox MahoganyHideout_B1F_Text_GruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Jed::
	trainerbattle_single TRAINER_JOHTO_SCIENTIST_JED, MahoganyHideout_B1F_Text_JedSeen, MahoganyHideout_B1F_Text_JedBeaten
	msgbox MahoganyHideout_B1F_Text_JedAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Painel::
	lockall
	msgbox MahoganyHideout_B1F_Text_Painel, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B1F_EventScript_Estante::
	lockall
	msgbox MahoganyHideout_B1F_Text_Estante, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

MahoganyHideout_B1F_Text_GruntSeen:
	.string "Heheh. Feeling lucky, punk?\p"
	.string "Go ahead, take another step.\p"
	.string "We've got traps set in the floor!$"

MahoganyHideout_B1F_Text_GruntBeaten:
	.string "Kaboom!$"

MahoganyHideout_B1F_Text_GruntAfter:
	.string "I don't even know where the traps\n"
	.string "are planted.\p"
	.string "You'll just have to collect your\n"
	.string "courage and walk.$"

MahoganyHideout_B1F_Text_JedSeen:
	.string "This is no place for a child.\p"
	.string "TEAM ROCKET's research must not\n"
	.string "be interrupted!$"

MahoganyHideout_B1F_Text_JedBeaten:
	.string "My machines were no use…$"

MahoganyHideout_B1F_Text_JedAfter:
	.string "The radio signal we broadcast from\n"
	.string "below drives POKéMON wild.\p"
	.string "It is science. You would not\n"
	.string "understand.$"

MahoganyHideout_B1F_Text_Painel:
	.string "A secret switch!\n"
	.string "Better press it.\p"
	.string "…Nothing happened. It must be\n"
	.string "wired to something else.$"

MahoganyHideout_B1F_Text_Estante:
	.string "Crammed with files on POKéMON\n"
	.string "taken from trainers.$"
