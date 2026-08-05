@ Rt8 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt8_MapScripts::
	.byte 0

Unova_Rt8_EventScript_Placa0::
	msgbox Unova_Rt8_Text_R8SignText, MSGBOX_SIGN
	end

Unova_Rt8_EventScript_Placa1::
	msgbox Unova_Rt8_Text_R8TubelineSignText, MSGBOX_SIGN
	end

Unova_Rt8_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_R8, Unova_Rt8_Text_PkmnRangerMR8SeenText, Unova_Rt8_Text_PkmnRangerMR8BeatenText
	end

Unova_Rt8_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_R8, Unova_Rt8_Text_PkmnRangerFR8SeenText, Unova_Rt8_Text_PkmnRangerFR8BeatenText
	end

Unova_Rt8_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_FISHER_R8, Unova_Rt8_Text_FisherR8SeenText, Unova_Rt8_Text_FisherR8BeatenText
	end

Unova_Rt8_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PARASOL_LADY_R8, Unova_Rt8_Text_ParasolLadyR8SeenText, Unova_Rt8_Text_ParasolLadyR8BeatenText
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

Unova_Rt8_Text_PkmnRangerMR8BeatenText::
	.string "What… I mean how?$"

Unova_Rt8_Text_PkmnRangerFR8SeenText::
	.string "The splish-splosh"
	.string "\nsounds! Those were"
	.string "\pyour footsteps,"
	.string "\nweren't they?"
	.string "\pSo cute!$"

Unova_Rt8_Text_PkmnRangerFR8BeatenText::
	.string "You're so strong!"
	.string "\nToo strong to be"
	.string "\lcute!$"

Unova_Rt8_Text_FisherR8SeenText::
	.string "Argh! It got away!"
	.string "\nI almost caught"
	.string "\lit, too!$"

Unova_Rt8_Text_FisherR8BeatenText::
	.string "I lost again, but"
	.string "\nit was nice to"
	.string "\ptake my mind off"
	.string "\nof fishing for a"
	.string "\lbit.$"

Unova_Rt8_Text_ParasolLadyR8SeenText::
	.string "If you turn a"
	.string "\nparasol around,"
	.string "\pit's like a flower"
	.string "\nblossoming in the"
	.string "\lrain!$"

Unova_Rt8_Text_ParasolLadyR8BeatenText::
	.string "I'll spin my para-"
	.string "\nsol around and"
	.string "\psend some water"
	.string "\ndroplets your way!$"
