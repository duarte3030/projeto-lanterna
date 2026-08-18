AcuityLakefront_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ rotulo da fonte: AcuityLakefront_CoordEvent_Rival (script 4). BARRY
@ (LOCALID_ACUITY_LAKEFRONT_RIVAL, sprite trocado para OBJ_EVENT_GFX_RICH_BOY,
@ mesma tabela de dev_scripts/valida_mapas_sinnoh.py) ja fica de pe la em cima,
@ visivel: a fonte NUNCA da SetFlag/ClearFlag em FLAG_HIDE_ACUITY_LAKEFRONT_
@ RIVAL em lugar nenhum (grep em res/ inteiro), so o campo hidden_flag do
@ objeto aponta pra ela; sem SetFlag em new_game.inc (regra do plano: so entra
@ com prova na fonte), a flag fica limpa e o objeto nasce visivel sozinho. A
@ cena so puxa a camera pra cima pra revelar ele e mostrar a fala.
AcuityLakefront_EventScript_CoordEvent_Rival::
	lockall
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, AcuityLakefront_Movement_CameraMoveNorth
	waitmovement 0
	delay 15
	msgbox AcuityLakefront_Text_CantClimbWithoutBadge, MSGBOX_DEFAULT
	applymovement LOCALID_ACUITY_LAKEFRONT_RIVAL, AcuityLakefront_Movement_RivalLeave
	waitmovement 0
	@ CONSERTO 18/08/2026: `setflag` ANTES do `removeobject`, molde da casa
	@ (Route203, Route209_Access, Pastoria). `removeobject` sozinho so tira o
	@ sprite da tela; o objeto renasce do template na proxima entrada no mapa,
	@ e o rival voltava a ficar plantado la em cima para sempre depois da cena.
	@ A fonte tem o MESMO buraco (RemoveObject sem SetFlag, e o `grep` em res/
	@ inteiro nao acha nenhum SetFlag/ClearFlag de FLAG_HIDE_ACUITY_LAKEFRONT_
	@ RIVAL, nem em res/field/scripts/scripts_init_new_game.s): desvio
	@ deliberado, o campo `flag` do objeto no map.json ja aponta para o alias e
	@ estava sem ninguem para acender.
	setflag FLAG_SINNOH_ESCONDE_ACUITY_LAKEFRONT_RIVAL
	removeobject LOCALID_ACUITY_LAKEFRONT_RIVAL
	applymovement LOCALID_CAMERA, AcuityLakefront_Movement_CameraMoveSouth
	waitmovement 0
	special RemoveCameraObject
	setvar VAR_SINNOH_ACUITY_BEIRA_ESTADO, 1
	releaseall
	end

AcuityLakefront_Movement_CameraMoveNorth:
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	step_end

AcuityLakefront_Movement_CameraMoveSouth:
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	step_end

AcuityLakefront_Movement_RivalLeave:
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

@ Texto literal de res/text/acuity_lakefront.json (BARRY: {STRVAR_1 3,0,0},
@ jogador: {STRVAR_1 3,1,0}); requebrado para a largura daqui.
AcuityLakefront_Text_CantClimbWithoutBadge:
	.string "BARRY: Hey, {PLAYER}!\n"
	.string "What, you finally come along now?\p"
	.string "Slooow! Way too slow!\p"
	.string "Listen, {PLAYER}.\n"
	.string "See how the rocks are all lumpy\l"
	.string "here?\p"
	.string "You can't climb those rocks until\n"
	.string "you get the Snowpoint Gym Badge.\p"
	.string "Anyway, I'm off.\n"
	.string "Team Galactic! I'm coming for you!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

AcuityLakefront_EventScript_Hiker::
	msgbox AcuityLakefront_Text_Hiker, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Pokefan::
	msgbox AcuityLakefront_Text_Pokefan, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Lass::
	msgbox AcuityLakefront_Text_Lass, MSGBOX_NPC
	end

AcuityLakefront_EventScript_Gentleman::
	msgbox AcuityLakefront_Text_Gentleman, MSGBOX_NPC
	end

AcuityLakefront_Text_Hiker:
	.string "The snow up here never really\n"
	.string "melts. Bundle up if you're heading\l"
	.string "further north.$"

AcuityLakefront_Text_Pokefan:
	.string "SNOWPOINT CITY is just past the\n"
	.string "lake. Almost there!$"

AcuityLakefront_Text_Lass:
	.string "Brr! I love the cold, but even\n"
	.string "I need a break sometimes.$"

AcuityLakefront_Text_Gentleman:
	.string "LAKE ACUITY is said to be the\n"
	.string "calmest of the three lakes.$"

@ Historia: a guarda da Galactica no caminho do Lago Acuity.
@ Texto de pret/pokeplatinum, res/text/acuity_lakefront.json. So conversa: em
@ Platinum esses dois nao batalham, e o Lago Acuity depende da insignia de
@ Snowpoint (FLAG_INSIGNIA_SINNOH_7), que ja existe.

AcuityLakefront_EventScript_GalacticGrunt1::
	msgbox AcuityLakefront_Text_GalacticGrunt1, MSGBOX_NPC
	end

AcuityLakefront_EventScript_GalacticGrunt2::
	msgbox AcuityLakefront_Text_GalacticGrunt2, MSGBOX_NPC
	end

AcuityLakefront_Text_GalacticGrunt1:
	.string "We're here to make sure Snowpoint's\n"
	.string "Gym Leader doesn't disturb us!\p"
	.string "You're here to see the lake Pokémon,\n"
	.string "too?\p"
	.string "You must be bored to fight your\n"
	.string "way through the snow to get here...$"

AcuityLakefront_Text_GalacticGrunt2:
	.string "The Pokémon of the three lakes\n"
	.string "appear to be connected somehow.\p"
	.string "When they blew up Lake Valor, a\n"
	.string "cavern appeared in the middle of\l"
	.string "this lake!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

AcuityLakefront_EventScript_Placa1::
	msgbox AcuityLakefront_Text_Placa1, MSGBOX_SIGN
	end

AcuityLakefront_Text_Placa1:
	.string "Lake Acuity ahead$"
