IronIslandB1FRightRoom_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
IronIslandB1FRightRoom_EventScript_CoordEvent_PlatformLift::
	@ TODO S?: cena da fonte, rotulo IronIslandB1FRightRoom_CoordEvent_PlatformLift
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

IronIslandB1FRightRoom_EventScript_PicnickerSummer::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_SUMMER, IronIslandB1FRightRoom_Text_PicnickerSummerIntro, IronIslandB1FRightRoom_Text_PicnickerSummerDefeat
	msgbox IronIslandB1FRightRoom_Text_PicnickerSummerPost, MSGBOX_AUTOCLOSE
	end

IronIslandB1FRightRoom_Text_PicnickerSummerIntro:
	.string "May we have a battle, please?\pIt will be something to lighten up this\nboring picnic with.$"

IronIslandB1FRightRoom_Text_PicnickerSummerDefeat:
	.string "We're not going to win if we play\naround like that...$"

IronIslandB1FRightRoom_Text_PicnickerSummerPost:
	.string "I'm going home to play with my\nPokémon!$"
