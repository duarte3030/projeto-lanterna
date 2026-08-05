@ RelicCastleB3F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicCastleB3F_MapScripts::
	.byte 0

Unova_RelicCastleB3F_EventScript_Npc0::
	msgbox Unova_RelicCastleB3F_Text_CoverFossilPromptText, MSGBOX_NPC
	end

Unova_RelicCastleB3F_EventScript_Npc1::
	msgbox Unova_RelicCastleB3F_Text_PlumeFossilPromptText, MSGBOX_NPC
	end


Unova_RelicCastleB3F_Text_CoverFossilPromptText::
	.string "Take the COVER"
	.string "\nFOSSIL?$"

Unova_RelicCastleB3F_Text_PlumeFossilPromptText::
	.string "Take the PLUME"
	.string "\nFOSSIL?$"
