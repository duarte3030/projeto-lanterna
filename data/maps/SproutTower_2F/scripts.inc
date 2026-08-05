@ SPROUT TOWER 2F, portado de fontes-mapas/hns/data/maps/SproutTower_2F.
@ ponytail: SAGE_NICO e SAGE_EDMOND ainda nao existem como TRAINER_ (zero
@ vaga sobrando, ver PENDENCIAS-JOHTO.md secao "torres e farol"). Cena
@ montada com o nome que os treinadores DEVEM ter.
@ Item usa Common_EventScript_FindItem (padrao vanilla) com
@ FLAG_UNUSED_0x265 cru, porque include/constants/flags.h esta com outro
@ agente e nao dava pra registrar um nome amigavel pra flag.
@ Cortado: os tres POKéMON de decoracao (RATTATA/BELLSPROUT via
@ OBJ_EVENT_GFX_MON_BASE+SPECIES_x, que cai no fallback POKE_BALL nesta
@ build) e o efeito de tremor do pilar (MOVEMENT_TYPE_TOWER_BEAM nao existe
@ neste engine).

SproutTower_2F_MapScripts::
	.byte 0

SproutTower_2F_EventScript_SageNico::
	trainerbattle_single TRAINER_SAGE_NICO, SproutTower_Text_SageNico_Seen, SproutTower_Text_SageNico_Beaten
	msgbox SproutTower_Text_SageNico_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_2F_EventScript_SageEdmond::
	trainerbattle_single TRAINER_SAGE_EDMOND, SproutTower_Text_SageEdmond_Seen, SproutTower_Text_SageEdmond_Beaten
	msgbox SproutTower_Text_SageEdmond_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_2F_EventScript_Statue::
	lock
	msgbox SproutTower_Text_2F_Statue, MSGBOX_AUTOCLOSE
	release
	end

SproutTower_Text_SageNico_Seen:
	.string "However hard we battle,\n"
	.string "the TOWER will stand strong.$"

SproutTower_Text_SageNico_Beaten:
	.string "I fought hard but I'm too weak.$"

SproutTower_Text_SageNico_AfterBattle:
	.string "The flexible pillar protects the\n"
	.string "TOWER, even from earthquakes.$"

SproutTower_Text_SageEdmond_Seen:
	.string "…Sway like leaves in the wind…$"

SproutTower_Text_SageEdmond_Beaten:
	.string "Oh, I'm weak!$"

SproutTower_Text_SageEdmond_AfterBattle:
	.string "I tried to copy BELLSPROUT's\n"
	.string "gentle movements for battle…\p"
	.string "But I didn't train well enough.$"

SproutTower_Text_2F_Statue:
	.string "A POKéMON statue…\p"
	.string "It looks very distinguished.$"
