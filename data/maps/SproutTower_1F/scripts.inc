@ SPROUT TOWER 1F, portado de fontes-mapas/hns/data/maps/SproutTower_1F.
@ ponytail: SAGE_CHOW ainda nao existe como TRAINER_ (zero vaga sobrando no
@ jogo inteiro, ver PENDENCIAS-JOHTO.md secao "torres e farol"). A cena esta
@ montada com o nome que o treinador DEVE ter; so falta criar.
@ Cortado: os dois BELLSPROUT de decoracao e o efeito de tremor do pilar
@ (MOVEMENT_TYPE_TOWER_BEAM com OBJ_EVENT_GFX_RAYQUAZA de paleta de feixe e
@ feature propria do hns; esse movement type nao existe neste engine).

SproutTower_1F_MapScripts::
	.byte 0

SproutTower_1F_EventScript_SageChow::
	trainerbattle_single TRAINER_SAGE_CHOW, SproutTower_Text_SageChow_Seen, SproutTower_Text_SageChow_Beaten
	msgbox SproutTower_Text_SageChow_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_1F_EventScript_Sage1::
	lock
	faceplayer
	msgbox SproutTower_Text_1F_Sage1, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_1F_EventScript_Sage2::
	lock
	faceplayer
	msgbox SproutTower_Text_1F_Sage2, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_1F_EventScript_Granny::
	lock
	faceplayer
	msgbox SproutTower_Text_1F_Granny, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_1F_EventScript_Teacher::
	lock
	faceplayer
	msgbox SproutTower_Text_1F_Teacher, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_1F_EventScript_Statue::
	lock
	msgbox SproutTower_Text_1F_Statue, MSGBOX_AUTOCLOSE
	release
	end

SproutTower_Text_SageChow_Seen:
	.string "We stand guard in this tower.\p"
	.string "Here, we express our gratitude\n"
	.string "to honor all POKéMON.$"

SproutTower_Text_SageChow_Beaten:
	.string "Th-Thank you!$"

SproutTower_Text_SageChow_AfterBattle:
	.string "All living beings coexist\n"
	.string "through cooperation.\p"
	.string "We must always be thankful\n"
	.string "for this.$"

SproutTower_Text_1F_Sage1:
	.string "Only if you reach the top will\n"
	.string "you obtain an HM.$"

SproutTower_Text_1F_Sage2:
	.string "SPROUT TOWER was built long ago\n"
	.string "as a place for POKéMON training.$"

SproutTower_Text_1F_Granny:
	.string "A BELLSPROUT over 100 feet\n"
	.string "tall…\p"
	.string "People say that it became the\n"
	.string "center pillar here.$"

SproutTower_Text_1F_Teacher:
	.string "See the pillar shaking?\p"
	.string "People are training upstairs.$"

SproutTower_Text_1F_Statue:
	.string "A POKéMON statue…\p"
	.string "It looks very distinguished.$"
