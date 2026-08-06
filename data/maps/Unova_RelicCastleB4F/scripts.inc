@ RelicCastleB4F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicCastleB4F_MapScripts::
	.byte 0

Unova_RelicCastleB4F_EventScript_Npc2::
	msgbox Unova_RelicCastleB4F_Text_LarvestaText, MSGBOX_NPC
	end


Unova_RelicCastleB4F_Text_LarvestaText::
	.string "Screee!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ CoverFossilB4FScript do BW3G: o `disappear` de la vira a flag do
@ proprio objeto, que e o que esconde o sprite depois de pegar.
Unova_RelicCastleB4F_EventScript_CoverFossilB4F::
	lock
	giveitem ITEM_COVER_FOSSIL
	setflag FLAG_UNOVA_ITEM_COVERFOSSILB4F
	removeobject VAR_LAST_TALKED
	release
	end

@ PlumeFossilB4FScript do BW3G: o `disappear` de la vira a flag do
@ proprio objeto, que e o que esconde o sprite depois de pegar.
Unova_RelicCastleB4F_EventScript_PlumeFossilB4F::
	lock
	giveitem ITEM_PLUME_FOSSIL
	setflag FLAG_UNOVA_ITEM_PLUMEFOSSILB4F
	removeobject VAR_LAST_TALKED
	release
	end
