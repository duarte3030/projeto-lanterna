@ CUME DO MT. SILVER. O duelo com o RED (decisao 3 do Gui, 15/08/2026) esta no
@ bloco portado mais abaixo; este cabecalho e o PORTAO dele, e e escrito a mao
@ de proposito: precisa de um rotulo de desvio que nao existe na fonte, e o
@ porte automatico reprova rotulo que nao acha la.
@
@ Na fonte quem revela o RED e o barco para Kanto (hns, SSAqua_1F). Aqui o
@ marcador honesto de "Johto acabou" e a OITAVA insignia, a da CLAIR em
@ Blackthorn, que ja existe. Depois de derrotado ele nao volta: a flag do
@ treinador basta, sem flag de enredo nova.
@
@ Sem o `setflag` da primeira linha o RED ficaria em pe no cume desde o
@ primeiro minuto de jogo novo, porque FLAG_HIDE_MTSILVER_RED nasce apagada.

MtSilver_SummitDay_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtSilver_SummitDay_OnTransition
	.byte 0

MtSilver_SummitDay_OnTransition:
	setflag FLAG_HIDE_MTSILVER_RED
	goto_if_unset FLAG_INSIGNIA_JOHTO_8, MtSilver_SummitDay_EventScript_SemRed
	goto_if_defeated TRAINER_JOHTO_RED, MtSilver_SummitDay_EventScript_SemRed
	clearflag FLAG_HIDE_MTSILVER_RED
MtSilver_SummitDay_EventScript_SemRed:
	end

@ >>> B6 Johto: cena portada do hns (porta_cenas_johto.py) >>>
@ o duelo com o RED no cume, o ultimo treinador de Johto
.set LOCALID_MTSILVER_SUMMITDAY_MTSILVER_RED, 1

MtSilver_SummitDay_EventScript_Red::
	lock
	faceplayer
	msgbox MtSilver_SummitDay_Text_Red, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_JOHTO_RED, MtSilver_SummitDay_Text_RedBeaten
	playse SE_M_BLIZZARD
	msgbox MtSilver_SummitDay_Text_Red, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	setflag FLAG_HIDE_MTSILVER_RED
	removeobject LOCALID_MTSILVER_SUMMITDAY_MTSILVER_RED
	fadescreenswapbuffers FADE_FROM_BLACK
	releaseall
	end

MtSilver_SummitDay_Text_Red::
	.string ".........................\n"
	.string ".........................$"

MtSilver_SummitDay_Text_RedBeaten::
	.string "...!$"

@ <<< B6 Johto: cena portada do hns <<<
