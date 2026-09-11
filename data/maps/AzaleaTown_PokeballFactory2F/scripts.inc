@ POKéBALL FACTORY de AZALEA TOWN, segundo andar (o chão de fábrica). ARTE do
@ Scorched Silver (g32m1, 20x14), cópia byte a byte. JOGO nosso: quem assalta é
@ a EQUIPE ROCKET de Johto, a mesma do SLOWPOKE WELL, e não a Team Phoenix do
@ hack. Nenhuma linha do Sloo entrou.
@
@ GEOMETRIA, medida no blockdata e não chutada: do alto do mapa para a metade de
@ baixo existem DOIS caminhos, e os dois passam por UM tile cada. O corredor do
@ meio aperta em (13,11) e o do depósito aperta em (19,9). Um capanga em cada um
@ desses tiles é portão de verdade: não dá para chegar na CARMEN sem derrotar um
@ dos dois. Depois de perder, cada um anda para o lado e o ON_TRANSITION repete
@ esse passo em toda carga do mapa, senão o objeto renasceria em cima do
@ corredor e trancaria o andar.
@
@ O tile (7,11) é o gargalo do corredor oeste, o único jeito de chegar em (2,12),
@ onde a CARMEN está encurralada. Por isso a cena do chefe fica ali.
@
@ Ela NÃO gasta var. O coord event do gen 3 só sabe comparar var, então o dele é
@ VAR_TEMP_0 valendo 0, que o motor zera em toda carga de mapa: o gatilho fica
@ sempre armado e quem diz se a cena roda é a PRIMEIRA linha do script, um
@ `goto_if_set FLAG_FABRICA_AZALEA_LIMPA` que sai antes de qualquer `lockall`,
@ ou seja sem travar o boneco e sem piscar nada na tela. Isso importa porque as
@ duas vagas de var que o briefing desta frente dava como reservadas (0x408B e
@ 0x4091) JÁ TÊM DONO em vars_frlg.h, medido pelo
@ dev_scripts/guarda_colisao_vars.py em 11/09/2026. Nenhuma var foi gasta aqui.

AzaleaTown_PokeballFactory2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AzaleaTown_PokeballFactory2F_OnTransition
	.byte 0

AzaleaTown_PokeballFactory2F_OnTransition:
	call AzaleaTown_PokeballFactory2F_EventScript_ArrumaCorredor
	call AzaleaTown_PokeballFactory2F_EventScript_ArrumaDeposito
	end

AzaleaTown_PokeballFactory2F_EventScript_ArrumaCorredor:
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_FABRICA_CORREDOR, AzaleaTown_PokeballFactory2F_EventScript_NaoMexe
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_CORREDOR, 14, 10
	return

AzaleaTown_PokeballFactory2F_EventScript_ArrumaDeposito:
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_FABRICA_DEPOSITO, AzaleaTown_PokeballFactory2F_EventScript_NaoMexe
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_DEPOSITO, 18, 10
	return

AzaleaTown_PokeballFactory2F_EventScript_NaoMexe:
	return

@ ----------------------------------------------------- os dois portões de chão

AzaleaTown_PokeballFactory2F_EventScript_GruntCorredor::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_CORREDOR, AzaleaTown_PokeballFactory2F_Text_CorredorVer, AzaleaTown_PokeballFactory2F_Text_CorredorPerder, AzaleaTown_PokeballFactory2F_EventScript_CorredorSai
	msgbox AzaleaTown_PokeballFactory2F_Text_CorredorDepois, MSGBOX_AUTOCLOSE
	end

AzaleaTown_PokeballFactory2F_EventScript_CorredorSai::
	msgbox AzaleaTown_PokeballFactory2F_Text_CorredorDepois, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_GRUNT_CORREDOR, AzaleaTown_PokeballFactory2F_Movement_CorredorSai
	waitmovement 0
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_CORREDOR, 14, 10
	release
	end

AzaleaTown_PokeballFactory2F_Movement_CorredorSai:
	walk_up
	walk_right
	face_left
	step_end

AzaleaTown_PokeballFactory2F_EventScript_GruntDeposito::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_DEPOSITO, AzaleaTown_PokeballFactory2F_Text_DepositoVer, AzaleaTown_PokeballFactory2F_Text_DepositoPerder, AzaleaTown_PokeballFactory2F_EventScript_DepositoSai
	msgbox AzaleaTown_PokeballFactory2F_Text_DepositoDepois, MSGBOX_AUTOCLOSE
	end

AzaleaTown_PokeballFactory2F_EventScript_DepositoSai::
	msgbox AzaleaTown_PokeballFactory2F_Text_DepositoDepois, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_GRUNT_DEPOSITO, AzaleaTown_PokeballFactory2F_Movement_DepositoSai
	waitmovement 0
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_DEPOSITO, 18, 10
	release
	end

AzaleaTown_PokeballFactory2F_Movement_DepositoSai:
	walk_down
	walk_left
	face_right
	step_end

@ ------------------------------------------------------------------- a cena

AzaleaTown_PokeballFactory2F_EventScript_Cena::
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_CenaJaRodou
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeInterroga, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_CHEFE, Common_Movement_ExclamationMark
	waitmovement 0
	delay 30
	applymovement LOCALID_FABRICA_2F_CHEFE, AzaleaTown_PokeballFactory2F_Movement_ChefeVem
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeDesafia, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_FABRICA_CHEFE, AzaleaTown_PokeballFactory2F_Text_ChefePerder
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeFoge, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_CHEFE, AzaleaTown_PokeballFactory2F_Movement_ChefeFoge
	waitmovement 0
	setflag FLAG_FABRICA_AZALEA_LIMPA
	removeobject LOCALID_FABRICA_2F_CHEFE
	removeobject LOCALID_FABRICA_2F_GRUNT_CORREDOR
	removeobject LOCALID_FABRICA_2F_GRUNT_DEPOSITO
	delay 30
	applymovement LOCALID_FABRICA_2F_CARMEN, AzaleaTown_PokeballFactory2F_Movement_CarmenVem
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenAgradece, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_QUICK_BALL, 5
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenDespede, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

AzaleaTown_PokeballFactory2F_EventScript_CenaJaRodou:
	end

AzaleaTown_PokeballFactory2F_Movement_ChefeVem:
	walk_right
	walk_right
	walk_up
	face_right
	step_end

@ (6,11) -> (6,12) -> (6,13): os dois tiles ao sul estão livres no blockdata, e
@ para o leste não há saída, porque (7,12) e (8,12) são parede e (7,11) é o
@ próprio jogador. Ele some logo em seguida, no `removeobject`.
AzaleaTown_PokeballFactory2F_Movement_ChefeFoge:
	walk_fast_down
	walk_fast_down
	step_end

AzaleaTown_PokeballFactory2F_Movement_CarmenVem:
	walk_right
	walk_right
	walk_right
	walk_up
	walk_right
	face_right
	step_end

@ -------------------------------------------------------------- a gente daqui

AzaleaTown_PokeballFactory2F_EventScript_Chefe::
	lock
	faceplayer
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeParado, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Carmen::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_CarmenDepois
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenAntes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_CarmenDepois::
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenDepois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario1::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario1Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario1Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario1Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario1Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario2::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario2Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario2Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario2Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario2Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario3::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario3Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario3Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario3Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario3Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

@ ------------------------------------------------------------------- textos

AzaleaTown_PokeballFactory2F_Text_ChefeInterroga:
	.string "GOON LEADER: For the last time,\n"
	.string "lady. Where do you keep the\l"
	.string "MASTER BALLS?\p"
	.string "CARMEN: I already told you. The\n"
	.string "last batch left for KANTO three\l"
	.string "weeks ago. There are none left.\p"
	.string "GOON LEADER: Then we take the\n"
	.string "recipe. And you with it.$"

AzaleaTown_PokeballFactory2F_Text_ChefeDesafia:
	.string "GOON LEADER: You again?\p"
	.string "I put three people on that door\n"
	.string "and not one of them was any use.\p"
	.string "Leave this to me. I'll show you\n"
	.string "what TEAM ROCKET is.$"

AzaleaTown_PokeballFactory2F_Text_ChefePerder:
	.string "No… in a BALL factory…$"

AzaleaTown_PokeballFactory2F_Text_ChefeFoge:
	.string "GOON LEADER: Remember this\n"
	.string "face, kid.\p"
	.string "TEAM ROCKET never forgets who\n"
	.string "gets in its way.$"

AzaleaTown_PokeballFactory2F_Text_ChefeParado:
	.string "GOON LEADER: Out of here.\n"
	.string "This is grown-up business.$"

AzaleaTown_PokeballFactory2F_Text_CarmenAntes:
	.string "CARMEN: Stay back, child!\p"
	.string "These people barged in barking\n"
	.string "orders, and they won't leave\l"
	.string "for nothing.$"

AzaleaTown_PokeballFactory2F_Text_CarmenAgradece:
	.string "CARMEN: They're gone…\p"
	.string "I'm CARMEN. The POKéBALL\n"
	.string "FACTORY is mine.\p"
	.string "I learned to make BALLS from\n"
	.string "KURT, next door, one at a time\l"
	.string "and by hand.\p"
	.string "The factory is here to supply the\n"
	.string "rest of JOHTO, but the recipe\l"
	.string "is his.\p"
	.string "Take these. It's all I have to\n"
	.string "thank you with.$"

AzaleaTown_PokeballFactory2F_Text_CarmenDespede:
	.string "CARMEN: The shop downstairs\n"
	.string "reopens right now.\p"
	.string "Come down whenever you like.\n"
	.string "You have credit in this house.$"

AzaleaTown_PokeballFactory2F_Text_CarmenDepois:
	.string "CARMEN: The line is running\n"
	.string "again.\p"
	.string "Seven APRICORN BALLS, the\n"
	.string "special ones, and the MASTER\l"
	.string "BALL for whoever can pay.$"

AzaleaTown_PokeballFactory2F_Text_Operario1Antes:
	.string "I froze. I can't even get up\n"
	.string "off the assembly line.$"

AzaleaTown_PokeballFactory2F_Text_Operario1Depois:
	.string "Thank you, really. I froze with\n"
	.string "fear and you didn't.$"

AzaleaTown_PokeballFactory2F_Text_Operario2Antes:
	.string "They're after the MASTER BALL.\p"
	.string "It's made from a stone that has\n"
	.string "almost run out.\l"
	.string "That's why it costs what it does.$"

AzaleaTown_PokeballFactory2F_Text_Operario2Depois:
	.string "One MASTER BALL takes half a\n"
	.string "year of work and a rare stone.\p"
	.string "Fifty thousand is cheap,\n"
	.string "believe me.$"

AzaleaTown_PokeballFactory2F_Text_Operario3Antes:
	.string "CARMEN is cornered over there,\n"
	.string "with their leader.\p"
	.string "Someone has to reach her.$"

AzaleaTown_PokeballFactory2F_Text_Operario3Depois:
	.string "CARMEN took over the factory and\n"
	.string "never changed a line of the\l"
	.string "recipe.\p"
	.string "KURT still comes by to check\n"
	.string "how the APRICORNS are cut.$"

AzaleaTown_PokeballFactory2F_Text_CorredorVer:
	.string "This corridor is closed.\n"
	.string "TEAM ROCKET's orders.$"

AzaleaTown_PokeballFactory2F_Text_CorredorPerder:
	.string "How did I lose in here?$"

AzaleaTown_PokeballFactory2F_Text_CorredorDepois:
	.string "Go on through. You'll run into\n"
	.string "the boss at the end of it.$"

AzaleaTown_PokeballFactory2F_Text_DepositoVer:
	.string "The storeroom is this way, and\n"
	.string "you are not getting into it.$"

AzaleaTown_PokeballFactory2F_Text_DepositoPerder:
	.string "All right, all right! I'm going!$"

AzaleaTown_PokeballFactory2F_Text_DepositoDepois:
	.string "We found no MASTER BALL on\n"
	.string "those shelves. Just plain BALLS.$"
