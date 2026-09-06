@ Gerado por dev_scripts/cenas_galar.py (blocos c3 e c6 da fase
@ de conteudo). Rodar dev_scripts/mundo_galar.py apaga este
@ arquivo; rodar cenas_galar.py --aplicar o repoe. Corpo das
@ cenas em data/scripts/galar_cenas.inc.

Galar_Wedgehurst03_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, GalarCena_G05M04_t5_x
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
@ Gerado por dev_scripts/distribui_dex.py --galar-objetos. Nao editar a mao.

@ Wedgehurst NAO tem laboratorio nesta arvore (medido em 07/09/2026:
@ nenhum dos 17 mapas Galar_Wedgehurst* tem NPC de cientista). O predio
@ e o CENTRO POKEMON, reconhecido por MUS_RG_POKE_CENTER e pela
@ enfermeira do balcao. Os tres iniciais sairam do MATO por decisao da
@ condutora da onda 2: eles caiam em slot duplicado de tabela selvagem,
@ e um deles em mapa submerso.
Galar_Wedgehurst03_EventScript_DexIniciaisGalar::
	lock
	faceplayer
	goto_if_set FLAG_INICIAL_GALAR, Galar_Wedgehurst03_EventScript_DexIniciaisGalarJaDeu
	msgbox Galar_Wedgehurst03_Text_DexIniciaisGalarPergunta, MSGBOX_DEFAULT
	dynmultipush Galar_Wedgehurst03_Text_DexInicialGalarGrookey, 0
	dynmultipush Galar_Wedgehurst03_Text_DexInicialGalarScorbunny, 1
	dynmultipush Galar_Wedgehurst03_Text_DexInicialGalarSobble, 2
	dynmultistack 0, 0, FALSE, 4, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	compare VAR_RESULT, MULTI_B_PRESSED
	goto_if_eq Galar_Wedgehurst03_EventScript_DexIniciaisGalarSai
	goto_if_eq VAR_RESULT, 0, Galar_Wedgehurst03_EventScript_DexInicialGalarGrookey
	goto_if_eq VAR_RESULT, 1, Galar_Wedgehurst03_EventScript_DexInicialGalarScorbunny
	goto_if_eq VAR_RESULT, 2, Galar_Wedgehurst03_EventScript_DexInicialGalarSobble
	goto Galar_Wedgehurst03_EventScript_DexIniciaisGalarSai

Galar_Wedgehurst03_EventScript_DexInicialGalarGrookey::
	givemon SPECIES_GROOKEY, 5
	setflag FLAG_INICIAL_GALAR
	msgbox Galar_Wedgehurst03_Text_DexIniciaisGalarEntregue, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst03_EventScript_DexInicialGalarScorbunny::
	givemon SPECIES_SCORBUNNY, 5
	setflag FLAG_INICIAL_GALAR
	msgbox Galar_Wedgehurst03_Text_DexIniciaisGalarEntregue, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst03_EventScript_DexInicialGalarSobble::
	givemon SPECIES_SOBBLE, 5
	setflag FLAG_INICIAL_GALAR
	msgbox Galar_Wedgehurst03_Text_DexIniciaisGalarEntregue, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst03_EventScript_DexIniciaisGalarJaDeu::
	msgbox Galar_Wedgehurst03_Text_DexIniciaisGalarJaDeu, MSGBOX_DEFAULT
	release
	end

Galar_Wedgehurst03_EventScript_DexIniciaisGalarSai::
	release
	end

Galar_Wedgehurst03_Text_DexIniciaisGalarPergunta:
	.string "The LEAGUE sends us three POKéMON\n"
	.string "for new TRAINERS every year.\p"
	.string "Nobody came for these. Pick one!$"

Galar_Wedgehurst03_Text_DexInicialGalarGrookey:
	.string "GROOKEY$"

Galar_Wedgehurst03_Text_DexInicialGalarScorbunny:
	.string "SCORBUNNY$"

Galar_Wedgehurst03_Text_DexInicialGalarSobble:
	.string "SOBBLE$"

Galar_Wedgehurst03_Text_DexIniciaisGalarEntregue:
	.string "Take good care of it!$"

Galar_Wedgehurst03_Text_DexIniciaisGalarJaDeu:
	.string "I hope the one you chose is\ndoing well.$"

@ <<< Dex completa <<<
