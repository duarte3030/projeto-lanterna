IronIslandB2FRightRoom_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

IronIslandB2FRightRoom_EventScript_WorkerNoel::
	trainerbattle_single TRAINER_SINNOH_WORKER_NOEL, IronIslandB2FRightRoom_Text_WorkerNoelIntro, IronIslandB2FRightRoom_Text_WorkerNoelDefeat
	msgbox IronIslandB2FRightRoom_Text_WorkerNoelPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FRightRoom_Text_WorkerNoelIntro:
	.string "The working-class hero says hi!$"

IronIslandB2FRightRoom_Text_WorkerNoelDefeat:
	.string "The working-class hero waves bye...$"

IronIslandB2FRightRoom_Text_WorkerNoelPost:
	.string "I used to work here a long time\nago, before it shut down.\pI worked at the ironworks near\nFloaroma Town, too.\pYou might say I'm drawn by iron\nas if by magnet!$"

IronIslandB2FRightRoom_EventScript_WorkerBraden::
	trainerbattle_single TRAINER_SINNOH_WORKER_BRADEN, IronIslandB2FRightRoom_Text_WorkerBradenIntro, IronIslandB2FRightRoom_Text_WorkerBradenDefeat
	msgbox IronIslandB2FRightRoom_Text_WorkerBradenPost, MSGBOX_AUTOCLOSE
	end

IronIslandB2FRightRoom_Text_WorkerBradenIntro:
	.string "While I'm making sure the lifts are\nsafe, I'll focus on a battle with you!$"

IronIslandB2FRightRoom_Text_WorkerBradenDefeat:
	.string "A-OK! Looks safe to me!\nNot a problem in sight!$"

IronIslandB2FRightRoom_Text_WorkerBradenPost:
	.string "I routinely check the lifts here.\nYou can be sure of their safety!$"
