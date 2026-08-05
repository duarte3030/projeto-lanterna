@ R22 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_R22_MapScripts::
	.byte 0

Unova_R22_EventScript_Placa0::
	msgbox Unova_R22_Text_R22SignText, MSGBOX_SIGN
	end

Unova_R22_EventScript_Placa1::
	msgbox Unova_R22_Text_R22ChasmSignText, MSGBOX_SIGN
	end

Unova_R22_EventScript_Npc3::
	msgbox Unova_R22_Text_R22YoungsterText, MSGBOX_NPC
	end

Unova_R22_EventScript_Npc4::
	msgbox Unova_R22_Text_R22LassText, MSGBOX_NPC
	end


Unova_R22_Text_R22SignText::
	.string "ROUTE 22$"

Unova_R22_Text_R22ChasmSignText::
	.string "GIANT CHASM"
	.string "\pBeware of wild"
	.string "\nPOKéMON!$"

Unova_R22_Text_R22YoungsterText::
	.string "This hill is high"
	.string "\nup! You can jump"
	.string "\poff these ledges"
	.string "\nto get down"
	.string "\lquickly!"
	.string "\pTry it, it's"
	.string "\nfun!$"

Unova_R22_Text_R22LassText::
	.string "There's a spooky"
	.string "\ncave at the end"
	.string "\lof this path."
	.string "\pBe careful if"
	.string "\nyou go in there!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 1). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_R22_EventScript_Gruta4B7::
	goto_if_set FLAG_UNOVA_GRUTA_R22, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R22
	goto Unova_EventScript_GrutaTier1
