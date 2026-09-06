@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de
@ map script da fonte (0x0169E9A) esta anotado no censo para a fase de conteudo.

Galar_Wedgehurst01_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Galar_Wedgehurst01_EventScript_DexDistribuicaoGalar::
	lock
	faceplayer
	goto_if_set FLAG_DEX_PRESENTE_EVENTO_GALAR, Galar_Wedgehurst01_EventScript_DexDistribuicaoGalarJaDeu
	msgbox Galar_Wedgehurst01_Text_DexDistribuicaoGalar, MSGBOX_DEFAULT
	givemon SPECIES_ETERNATUS_ETERNAMAX, 5
	givemon SPECIES_ZARUDE_DADA, 5
	setflag FLAG_DEX_PRESENTE_EVENTO_GALAR
	msgbox Galar_Wedgehurst01_Text_DexDistribuicaoGalarFim, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst01_EventScript_DexDistribuicaoGalarJaDeu::
	msgbox Galar_Wedgehurst01_Text_DexDistribuicaoGalarFim, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst01_Text_DexDistribuicaoGalar:
	.string "I keep the POKéMON from every\n"
	.string "event that never came to GALAR.\p"
	.string "You should have them.$"

Galar_Wedgehurst01_Text_DexDistribuicaoGalarFim:
	.string "Whatever does not fit in your\n"
	.string "party goes to your PC.$"

@ <<< Dex completa <<<
