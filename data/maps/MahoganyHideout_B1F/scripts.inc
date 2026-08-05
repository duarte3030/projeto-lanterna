@ ESCONDERIJO DA ROCKET em MAHOGANY, B1F. A planta veio do pokecrystal
@ (maps/TeamRocketBaseB1F.blk), convertida por dev_scripts/demake_gen2.py, e o
@ texto veio de maps/TeamRocketBaseB1F.asm do mesmo disassembly.
@
@ 06/08/2026: entraram as 22 armadilhas de piso e as 5 câmeras que a sessão
@ anterior deixou de fora. ZERO var gasta nas duas coisas.
@ - Armadilha: coord_event com gatilho VAR_TEMP_0 = 0. VAR_TEMP_0 é zerado a
@   cada entrada de mapa pelo próprio motor, então o gatilho está sempre valendo
@   e não consome nenhuma das ~21 vars que sobram no jogo. Quem lembra que a
@   armadilha JÁ estourou é FLAG_MAHOGANY_TRAP_1..22, uma por armadilha: sem
@   isso o corredor viraria batalha infinita e trancaria a passagem. As 22
@   coordenadas são as mesmas do pokecrystal, 1 para 1 (o mapa é conversão
@   direta de 15x9 blocos gen 2 para 30x18 metatiles gen 3).
@ - Câmera: no pokecrystal cada uma é um coord_event que faz aparecer DOIS
@   grunts (os mesmos GRUNTM_20/21 nas cinco). Isso não traduz para gen 3:
@   trainerbattle_single não rebate treinador já derrotado, então os mesmos dois
@   grunts só dariam batalha na primeira câmera. Viraram cinco guardas de posto,
@   um por câmera, com RAIO DE VISÃO, que é o que o motor já sabe fazer sozinho
@   (e o que a instrução desta tarefa manda tentar antes de gastar recurso).
@   Zero var, zero flag: quem lembra que o guarda caiu é a flag de treinador.
@   As cinco câmeras continuam na parede como placa, com o texto do original.
@ - Os guardas usam FLAG_HIDE_MAHOGANY_HIDEOUT_ROCKETS igual ao resto do
@   esconderijo: quando o transmissor cai, somem junto com todo mundo.
@ As estátuas de PERSIAN viraram placa.

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

@ ---------------------------------------------------------------- câmeras ----

MahoganyHideout_B1F_EventScript_Guarda1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_CAMERA_1, MahoganyHideout_B1F_Text_CameraGrunt1Seen, MahoganyHideout_B1F_Text_CameraGrunt1Beaten
	msgbox MahoganyHideout_B1F_Text_CameraGruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Guarda2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_CAMERA_2, MahoganyHideout_B1F_Text_CameraGrunt2Seen, MahoganyHideout_B1F_Text_CameraGrunt2Beaten
	msgbox MahoganyHideout_B1F_Text_CameraGruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Guarda3::
	trainerbattle_single TRAINER_JOHTO_ROCKET_CAMERA_3, MahoganyHideout_B1F_Text_CameraGrunt1Seen, MahoganyHideout_B1F_Text_CameraGrunt1Beaten
	msgbox MahoganyHideout_B1F_Text_CameraGruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Guarda4::
	trainerbattle_single TRAINER_JOHTO_ROCKET_CAMERA_4, MahoganyHideout_B1F_Text_CameraGrunt2Seen, MahoganyHideout_B1F_Text_CameraGrunt2Beaten
	msgbox MahoganyHideout_B1F_Text_CameraGruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Guarda5::
	trainerbattle_single TRAINER_JOHTO_ROCKET_CAMERA_5, MahoganyHideout_B1F_Text_CameraGrunt1Seen, MahoganyHideout_B1F_Text_CameraGrunt1Beaten
	msgbox MahoganyHideout_B1F_Text_CameraGruntAfter, MSGBOX_AUTOCLOSE
	end

MahoganyHideout_B1F_EventScript_Camera::
	lockall
	msgbox MahoganyHideout_B1F_Text_Camera, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

@ ------------------------------------------------------------ armadilhas ----

MahoganyHideout_B1F_EventScript_Armadilha1::
	goto_if_set FLAG_MAHOGANY_TRAP_1, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_1
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha2::
	goto_if_set FLAG_MAHOGANY_TRAP_2, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_2
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha3::
	goto_if_set FLAG_MAHOGANY_TRAP_3, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_3
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha4::
	goto_if_set FLAG_MAHOGANY_TRAP_4, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_4
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha5::
	goto_if_set FLAG_MAHOGANY_TRAP_5, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_5
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha6::
	goto_if_set FLAG_MAHOGANY_TRAP_6, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_6
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha7::
	goto_if_set FLAG_MAHOGANY_TRAP_7, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_7
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha8::
	goto_if_set FLAG_MAHOGANY_TRAP_8, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_8
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha9::
	goto_if_set FLAG_MAHOGANY_TRAP_9, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_9
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha10::
	goto_if_set FLAG_MAHOGANY_TRAP_10, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_10
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha11::
	goto_if_set FLAG_MAHOGANY_TRAP_11, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_11
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha12::
	goto_if_set FLAG_MAHOGANY_TRAP_12, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_12
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha13::
	goto_if_set FLAG_MAHOGANY_TRAP_13, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_13
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha14::
	goto_if_set FLAG_MAHOGANY_TRAP_14, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_14
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha15::
	goto_if_set FLAG_MAHOGANY_TRAP_15, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_15
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha16::
	goto_if_set FLAG_MAHOGANY_TRAP_16, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_16
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha17::
	goto_if_set FLAG_MAHOGANY_TRAP_17, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_17
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha18::
	goto_if_set FLAG_MAHOGANY_TRAP_18, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_18
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha19::
	goto_if_set FLAG_MAHOGANY_TRAP_19, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_19
	goto MahoganyHideout_B1F_EventScript_ArmadilhaGeodude

MahoganyHideout_B1F_EventScript_Armadilha20::
	goto_if_set FLAG_MAHOGANY_TRAP_20, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_20
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_Armadilha21::
	goto_if_set FLAG_MAHOGANY_TRAP_21, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_21
	goto MahoganyHideout_B1F_EventScript_ArmadilhaKoffing

MahoganyHideout_B1F_EventScript_Armadilha22::
	goto_if_set FLAG_MAHOGANY_TRAP_22, MahoganyHideout_B1F_EventScript_ArmadilhaGasta
	setflag FLAG_MAHOGANY_TRAP_22
	goto MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb

MahoganyHideout_B1F_EventScript_ArmadilhaGasta::
	end

MahoganyHideout_B1F_EventScript_ArmadilhaVoltorb::
	lockall
	setwildbattle SPECIES_VOLTORB, 23
	waitse
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	dowildbattle
	releaseall
	end

MahoganyHideout_B1F_EventScript_ArmadilhaGeodude::
	lockall
	setwildbattle SPECIES_GEODUDE, 21
	waitse
	playmoncry SPECIES_GEODUDE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	dowildbattle
	releaseall
	end

MahoganyHideout_B1F_EventScript_ArmadilhaKoffing::
	lockall
	setwildbattle SPECIES_KOFFING, 21
	waitse
	playmoncry SPECIES_KOFFING, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	dowildbattle
	releaseall
	end

@ ----------------------------------------------------------------- placas ----

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

MahoganyHideout_B1F_Text_CameraGrunt1Seen:
	.string "Hey! Intruder alert!$"

MahoganyHideout_B1F_Text_CameraGrunt1Beaten:
	.string "Dang… I failed…$"

MahoganyHideout_B1F_Text_CameraGrunt2Seen:
	.string "It's my turn!\n"
	.string "There's no escape!$"

MahoganyHideout_B1F_Text_CameraGrunt2Beaten:
	.string "Not me too…$"

MahoganyHideout_B1F_Text_CameraGruntAfter:
	.string "Surveillance cams are in the\n"
	.string "POKéMON statues.\p"
	.string "We'll keep appearing until you\n"
	.string "trip every last one of them.$"

MahoganyHideout_B1F_Text_Camera:
	.string "A POKéMON statue with a lens\n"
	.string "where an eye should be.\p"
	.string "It is a surveillance camera, and\n"
	.string "it is watching.$"

MahoganyHideout_B1F_Text_Painel:
	.string "A secret switch!\n"
	.string "Better press it.\p"
	.string "…Nothing happened. It must be\n"
	.string "wired to something else.$"

MahoganyHideout_B1F_Text_Estante:
	.string "Crammed with files on POKéMON\n"
	.string "taken from trainers.$"
