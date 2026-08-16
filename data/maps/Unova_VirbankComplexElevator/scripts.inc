@ VirbankComplexElevator do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2, 15/08/2026: o elevador estava DESLIGADO. O importador trouxe a
@ sala mas nenhum dos warps: o mapa tinha `warp_events` vazio, e nem o
@ VirbankComplexOutside, nem o B1F, nem o B2F apontavam para cá. Como o único
@ jeito de entrar no complexo, na fonte, é este elevador (VirbankComplexOutside
@ tem `warp_event 15, 45, VIRBANK_COMPLEX_ELEVATOR, 1` e mais nada), o B1F e o
@ B2F inteiros estavam inalcançáveis jogando. Os warps entraram SEMPRE NO FIM
@ da lista de cada map.json, para não renumerar índice que já existia.
@ Nenhum byte de map.bin mudou: as cinco casas de porta ((15,45) lá fora,
@ (7,0) no B1F, (11,0) no B2F e (1,3)/(2,3) aqui) já tinham
@ MB_NON_ANIMATED_DOOR, medido.
@
@ ponytail: a fonte usa o comando `elevator` do gen 2, que é menu de andar com
@ saída DINÂMICA (`elevfloor ... VIRBANK_COMPLEX_*`, e os dois warps daqui vão
@ para `VIRBANK_COMPLEX_OUTSIDE, -1`, o "-1" de "volta de onde veio"). Aqui o
@ painel é uma escada de três perguntas SIM/NÃO e a porta é warp fixo para o
@ térreo, que é o mapa que a própria fonte escreveu no destino. Custo: zero
@ tabela de multichoice nova, zero warp dinâmico. Se um dia o menu de verdade
@ valer o trabalho, o lugar é aqui.
@
@ ponytail: a trava de LIFT_KEY da fonte NÃO foi portada. `ITEM_LIFT_KEY`
@ existe (items.h:919) mas em Unova NINGUÉM entrega a chave nesta build (o único
@ uso no repo é o RocketHideout_B4F de Kanto), então a trava fecharia o complexo
@ para sempre. O texto da fonte fica guardado abaixo para quando a chave entrar
@ no roteiro.
@
@ `.SetPipes` da fonte (MAPCALLBACK_NEWMAP) apaga os quatro interruptores do
@ B2F ao entrar aqui; portado no ON_LOAD, igual ao que o B1F faz.

Unova_VirbankComplexElevator_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VirbankComplexElevator_EventScript_AoCarregar
	.byte 0

Unova_VirbankComplexElevator_EventScript_AoCarregar::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4
	end

@ `VirbankComplexElevatorScript` da fonte: o painel de (3,0).
Unova_VirbankComplexElevator_EventScript_Placa0::
	lock
	msgbox Unova_VirbankComplexElevator_Text_Andar1F, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Unova_VirbankComplexElevator_EventScript_Vai1F
	msgbox Unova_VirbankComplexElevator_Text_AndarB1F, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Unova_VirbankComplexElevator_EventScript_VaiB1F
	msgbox Unova_VirbankComplexElevator_Text_AndarB2F, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Unova_VirbankComplexElevator_EventScript_VaiB2F
	release
	end

Unova_VirbankComplexElevator_EventScript_Vai1F::
	call Unova_VirbankComplexElevator_EventScript_Sobe
	warp MAP_UNOVA_VIRBANK_COMPLEX_OUTSIDE, 4
	waitstate
	end

Unova_VirbankComplexElevator_EventScript_VaiB1F::
	call Unova_VirbankComplexElevator_EventScript_Sobe
	warp MAP_UNOVA_VIRBANK_COMPLEX_B1F, 1
	waitstate
	end

Unova_VirbankComplexElevator_EventScript_VaiB2F::
	call Unova_VirbankComplexElevator_EventScript_Sobe
	warp MAP_UNOVA_VIRBANK_COMPLEX_B2F, 1
	waitstate
	end

@ o `playsound SFX_ELEVATOR` + `earthquake 60` da fonte
Unova_VirbankComplexElevator_EventScript_Sobe::
	closemessage
	playse SE_ELEVATOR
	setvar VAR_0x8004, 1  @ Vertical pan
	setvar VAR_0x8005, 0  @ Horizontal pan
	setvar VAR_0x8006, 12 @ Num shakes
	setvar VAR_0x8007, 3  @ Shake delay
	special ShakeScreen
	delay 60
	waitse
	return

@ Uma PÁGINA por pergunta, de propósito: `\p` exige um A só para virar a
@ página antes de a caixa de SIM/NÃO aparecer, e isso é armadilha de leitura
@ (e de roteiro de teste). Medido no emulador em 15/08/2026.
Unova_VirbankComplexElevator_Text_Andar1F::
	.string "Go up to 1F, outside?$"

Unova_VirbankComplexElevator_Text_AndarB1F::
	.string "Go to B1F?$"

Unova_VirbankComplexElevator_Text_AndarB2F::
	.string "Go down to B2F?$"

@ Guardado da fonte, ainda sem uso: ver a nota de LIFT_KEY no cabeçalho.
Unova_VirbankComplexElevator_Text_VirbankComplexElevatorNoKeyText::
	.string "A LIFT KEY is"
	.string "\nrequired…$"
