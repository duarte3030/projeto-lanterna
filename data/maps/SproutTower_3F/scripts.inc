@ SPROUT TOWER 3F, portado de fontes-mapas/hns/data/maps/SproutTower_3F.
@ ponytail: SAGE_JIN, SAGE_NEAL, SAGE_TROY e SAGE_LI ainda nao existem como
@ TRAINER_ (zero vaga sobrando, ver PENDENCIAS-JOHTO.md secao "torres e
@ farol"). Cena montada com o nome que os treinadores DEVEM ter.
@ SAGE_LI usa OBJ_EVENT_GFX_OLD_MAN (nao OBJ_EVENT_GFX_MR_FUJI do hns, que so
@ desenha dentro de #if IS_FRLG) e entrega ITEM_HM_FLASH via
@ FLAG_RECEIVED_HM_FLASH, que ja existia em flags.h antes desta sessao.
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x266/0x267 crus
@ (flags.h esta com outro agente).
@ Nao portado: a cena do rival (SILVER) que aparece aqui no hns. Sem sprite
@ (OBJ_EVENT_GFX_SILVER so existe dentro de #if IS_FRLG), sem vaga de
@ treinador e a logica original usa VAR_SPROUT_TOWER, que e proibida aqui.
@ Ja documentado em PENDENCIAS-JOHTO.md secao 3 (Rival). Tambem cortados: os
@ tres POKéMON de decoracao (GASTLY/RATTATA via OBJ_EVENT_GFX_MON_BASE, que
@ cai no fallback POKE_BALL nesta build) e o tremor do pilar
@ (MOVEMENT_TYPE_TOWER_BEAM nao existe neste engine).

SproutTower_3F_MapScripts::
	.byte 0

SproutTower_3F_EventScript_SageJin::
	trainerbattle_single TRAINER_SAGE_JIN, SproutTower_Text_SageJin_Seen, SproutTower_Text_SageJin_Beaten
	msgbox SproutTower_Text_SageJin_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_3F_EventScript_SageNeal::
	trainerbattle_single TRAINER_SAGE_NEAL, SproutTower_Text_SageNeal_Seen, SproutTower_Text_SageNeal_Beaten
	msgbox SproutTower_Text_SageNeal_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_3F_EventScript_SageTroy::
	trainerbattle_single TRAINER_SAGE_TROY, SproutTower_Text_SageTroy_Seen, SproutTower_Text_SageTroy_Beaten
	msgbox SproutTower_Text_SageTroy_AfterBattle, MSGBOX_AUTOCLOSE
	end

SproutTower_3F_EventScript_Painting::
	lock
	msgbox SproutTower_Text_3F_Painting, MSGBOX_AUTOCLOSE
	release
	end

SproutTower_3F_EventScript_Statue::
	lock
	msgbox SproutTower_Text_3F_Statue, MSGBOX_AUTOCLOSE
	release
	end

SproutTower_3F_EventScript_SageLi::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HM_FLASH, SproutTower_3F_EventScript_SageLi_Beaten
	msgbox SproutTower_Text_SageLi_Seen, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_SAGE_LI, SproutTower_Text_SageLi_Beaten
	msgbox SproutTower_Text_SageLi_TakeFlash, MSGBOX_DEFAULT
	giveitem ITEM_HM_FLASH
	setflag FLAG_RECEIVED_HM_FLASH
	msgbox SproutTower_Text_SageLi_FlashExplain, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_3F_EventScript_SageLi_Beaten::
	msgbox SproutTower_Text_SageLi_AfterBattle, MSGBOX_DEFAULT
	closemessage
	release
	end

SproutTower_Text_SageLi_Seen:
	.string "So good of you to come here!\p"
	.string "SPROUT TOWER is a place of\n"
	.string "training.\p"
	.string "People and POKéMON test their\n"
	.string "bonds to build a bright future\l"
	.string "together.\p"
	.string "I am the final test.\p"
	.string "Allow me to check the ties\n"
	.string "between your POKéMON and you!$"

SproutTower_Text_SageLi_Beaten:
	.string "Ah, excellent!$"

SproutTower_Text_SageLi_TakeFlash:
	.string "You and your POKéMON should\n"
	.string "have no problem using this move.\p"
	.string "Take this FLASH HM.$"

SproutTower_Text_SageLi_FlashExplain:
	.string "FLASH illuminates even the\n"
	.string "darkest of all places.\p"
	.string "But to use it out of battle, you\n"
	.string "need the BADGE from VIOLET's GYM.$"

SproutTower_Text_SageLi_AfterBattle:
	.string "I hope you learn and grow from\n"
	.string "your journey.$"

SproutTower_Text_SageJin_Seen:
	.string "I train to find enlightenment\n"
	.string "in POKéMON!$"

SproutTower_Text_SageJin_Beaten:
	.string "My training is incomplete…$"

SproutTower_Text_SageJin_AfterBattle:
	.string "As POKéMON grow stronger,\n"
	.string "so does the trainer.\p"
	.string "No, wait. As the trainer\n"
	.string "grows stronger, so do the\l"
	.string "POKéMON.$"

SproutTower_Text_SageTroy_Seen:
	.string "Let me see how much you trust\n"
	.string "your POKéMON.$"

SproutTower_Text_SageTroy_Beaten:
	.string "Yes, your trust is real!$"

SproutTower_Text_SageTroy_AfterBattle:
	.string "It is not far to the ELDER.$"

SproutTower_Text_SageNeal_Seen:
	.string "The ELDER's HM lights even\n"
	.string "pitch-black darkness.$"

SproutTower_Text_SageNeal_Beaten:
	.string "It is my head that is bright!$"

SproutTower_Text_SageNeal_AfterBattle:
	.string "Let there be light on your\n"
	.string "journey.$"

SproutTower_Text_3F_Painting:
	.string "It's a powerful painting of a\n"
	.string "BELLSPROUT.$"

SproutTower_Text_3F_Statue:
	.string "A POKéMON statue…\p"
	.string "It looks very distinguished.$"
