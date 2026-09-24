@ MtChimney_GymEntrance: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 33.1) por dev_scripts/copia_planta_ex.py.

MtChimney_GymEntrance_MapScripts::
	.byte 0

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
MtChimney_GymEntrance_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_HOENN_16, MtChimney_GymEntrance_EventScript_GymGuidePostVictory
	msgbox MtChimney_GymEntrance_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

MtChimney_GymEntrance_EventScript_GymGuidePostVictory::
	msgbox MtChimney_GymEntrance_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	releaseall
	end

MtChimney_GymEntrance_Text_GymGuideAdvice:
	.string "Welcome to one of the secret GYMS!\p"
	.string "Sorry I never mentioned it, I’d lose my\n"
	.string "job if I did.\p"
	.string "Anyways this is where the legendary\n"
	.string "BLAINE trains.\p"
	.string "Like FLANNERY he uses FIRE TYPES!\p"
	.string "So use a the same strategy of WATER,\n"
	.string "GROUND, and ROCK to bring the\l"
	.string "strongest GYM LEADER to his knees!$"

MtChimney_GymEntrance_Text_GymGuidePostVictory:
	.string "{PLAYER}, you’ve beaten the\n"
	.string "strongest GYM LEADER in the HOENN\l"
	.string "REGION!$"

