@ Rt8 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt8_MapScripts::
	.byte 0

Unova_Rt8_EventScript_Placa0::
	msgbox Unova_Rt8_Text_R8SignText, MSGBOX_SIGN
	end

Unova_Rt8_EventScript_Placa1::
	msgbox Unova_Rt8_Text_R8TubelineSignText, MSGBOX_SIGN
	end

Unova_Rt8_EventScript_Npc4::
	msgbox Unova_Rt8_Text_PkmnRangerMR8SeenText, MSGBOX_NPC
	end

Unova_Rt8_EventScript_Npc5::
	msgbox Unova_Rt8_Text_PkmnRangerFR8SeenText, MSGBOX_NPC
	end

Unova_Rt8_EventScript_Npc6::
	msgbox Unova_Rt8_Text_FisherR8SeenText, MSGBOX_NPC
	end

Unova_Rt8_EventScript_Npc7::
	msgbox Unova_Rt8_Text_ParasolLadyR8SeenText, MSGBOX_NPC
	end


Unova_Rt8_Text_R8SignText::
	.string "ROUTE 8"
	.string "\pICIRRUS CITY"
	.string "\nahead.$"

Unova_Rt8_Text_R8TubelineSignText::
	.string "TUBELINE BRIDGE"
	.string "\pPassage to"
	.string "\nOPELUCID CITY.$"

Unova_Rt8_Text_PkmnRangerMR8SeenText::
	.string "I trained my body"
	.string "\nand mind by"
	.string "\pstanding under a"
	.string "\nwaterfall! Nothing"
	.string "\lwill faze me now!$"

Unova_Rt8_Text_PkmnRangerFR8SeenText::
	.string "The splish-splosh"
	.string "\nsounds! Those were"
	.string "\pyour footsteps,"
	.string "\nweren't they?"
	.string "\pSo cute!$"

Unova_Rt8_Text_FisherR8SeenText::
	.string "Argh! It got away!"
	.string "\nI almost caught"
	.string "\lit, too!$"

Unova_Rt8_Text_ParasolLadyR8SeenText::
	.string "If you turn a"
	.string "\nparasol around,"
	.string "\pit's like a flower"
	.string "\nblossoming in the"
	.string "\lrain!$"
