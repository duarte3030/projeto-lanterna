@ StriatonGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5): os cinco treinadores de dentro.
@
@ Medido antes: o ginasio tinha o CILAN e mais nada batalhavel. Os dois WAITER e
@ as tres WAITRESS estavam no mapa so com o texto de DEPOIS da batalha, pelo
@ mesmo motivo de Aspertia e Lentimas: no BW3G eles sao OBJECTTYPE_SCRIPT com
@ `loadtrainer` dentro de script, e a varredura do B4 so via OBJECTTYPE_TRAINER.
@ Constantes novas 2451 a 2455, times de fontes-mapas/bw3g/data/trainers/parties.asm.
@ Trocas de classe (gen 3 nao tem as de gen 5): WAITER virou Gentleman e
@ WAITRESS virou Lady.
@
@ ONDE ISTO SE AFASTA DA FONTE, de proposito, e o que fica para o B6:
@ no BW3G os cinco ficam INVISIVEIS ate voce examinar a mesa ou a lata errada
@ (sao 12 bg_events; o `.Trainers` callback os apaga enquanto nao foram
@ derrotados) e tres desses bg_events sao interruptores que abrem a escada do
@ CILAN. Aqui eles ficam visiveis e batalham quando voce fala com eles. Duas
@ razoes medidas: (1) o "esconder ate a emboscada" e o inverso do que o campo
@ `flag` do object_event faz (ele esconde quando a flag esta ACESA), entao
@ custaria uma flag por treinador so para inverter o sentido; (2) a escada em
@ (6,2) que os tres interruptores abrem JA ESTA ABERTA no nosso blockdata
@ (colisao 0, medido), entao o interruptor nao compra caminho nenhum e seria
@ enfeite caro. Quando o B6 escrever o callback dos tres irmaos, as duas coisas
@ voltam juntas.
@
@ Custo: ZERO var e ZERO flag. A memoria do "ja perdeu" e a flag de treinador do
@ motor, que o proprio `trainerbattle_single` grava e le.
@
@ ----------------------------------------------------------------------------
@ B6, 12/08/2026: OS TRES INTERRUPTORES ENTRARAM, E A NOTA (2) ACIMA ESTAVA
@ ERRADA. Ela mediu so o quadrante de cima do bloco.
@
@ `changeblock 6, 2, $6a` da fonte ocupa QUATRO metatiles nossos, (6,2), (7,2),
@ (6,3) e (7,3), porque um bloco de gen 2 vale 2x2 metatiles. Os dois de cima ja
@ estao com colisao 0, que e o que a nota viu; os DOIS DE BAIXO, (6,3) e (7,3),
@ estao com o metatile 670, colisao 1, ou seja parede. Lido do `map.bin` do disco.
@
@ E isso nao e enfeite: na grade de colisao deste mapa a linha 3 so tem aberto o
@ 3, o 11 e o 12, e (4,1) e (4,2) sao parede. A camara do CILAN, que e o
@ retangulo (5..8, 1..2), NAO TEM NENHUMA outra ligacao com o resto do ginasio.
@ Com a escada fechada o LIDER DE GINASIO era inalcancavel a pe, e a insignia de
@ Striaton com ele.
@
@ De onde saiu cada numero: mesma tabela do B5 em Castelia (`quad2mt` de
@ tileset_gen2, tileset `game_corner` = gTileset_UnovaGameCorner), comparada tile
@ a tile com o `map.bin` atual. Dos quatro quadrantes so os dois de baixo
@ diferem: 670 -> 637 em (6,3) e 670 -> 684 em (7,3).
@
@ Custo desta parte: ZERO var e TRES flags, FLAG_UNOVA_STRIATON_CHAVE_1 a _3. Sao
@ tres bits independentes de verdade (a fonte deixa apertar em qualquer ordem e
@ cada `.done` so abre a escada se os OUTROS DOIS ja estiverem acesos), entao
@ contador em var nao serve. O ON_LOAD reaplica na entrada, que e o que faz a
@ escada continuar aberta depois de sair e voltar; o `special DrawWholeMapView`
@ so aparece no caminho do interruptor, porque no ON_LOAD o mapa ainda vai ser
@ desenhado.

Unova_StriatonGym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_StriatonGym_EventScript_Escada
	.byte 0

Unova_StriatonGym_EventScript_Escada::
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_1, Unova_StriatonGym_EventScript_EscadaFim
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_2, Unova_StriatonGym_EventScript_EscadaFim
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_3, Unova_StriatonGym_EventScript_EscadaFim
	call Unova_StriatonGym_EventScript_AbreEscada
Unova_StriatonGym_EventScript_EscadaFim::
	end

@ bloco $6A da fonte em (6,2): so os dois quadrantes de baixo diferem
Unova_StriatonGym_EventScript_AbreEscada::
	setmetatile 6, 3, 637, FALSE
	setmetatile 7, 3, 684, FALSE
	return

@ `.done` dos tres interruptores da fonte: cada um confere os OUTROS DOIS.
Unova_StriatonGym_EventScript_TalvezAbra::
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_1, Unova_StriatonGym_EventScript_AindaNao
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_2, Unova_StriatonGym_EventScript_AindaNao
	goto_if_unset FLAG_UNOVA_STRIATON_CHAVE_3, Unova_StriatonGym_EventScript_AindaNao
	call Unova_StriatonGym_EventScript_AbreEscada
	playse SE_DOOR
	special DrawWholeMapView
	waitse
	msgbox Unova_StriatonGym_Text_EscadaAbriu, MSGBOX_DEFAULT
Unova_StriatonGym_EventScript_AindaNao::
	return

@ `StriatonGymCanSwitch` da fonte: a lata de (13,17), interruptor 2.
Unova_StriatonGym_EventScript_Placa2::
	lock
	goto_if_set FLAG_UNOVA_STRIATON_CHAVE_2, Unova_StriatonGym_EventScript_ChaveJaApertada
	setflag FLAG_UNOVA_STRIATON_CHAVE_2
	msgbox Unova_StriatonGym_Text_StriatonGymPressSwitchText, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	waitse
	call Unova_StriatonGym_EventScript_TalvezAbra
	release
	end

Unova_StriatonGym_EventScript_ChaveJaApertada::
	msgbox Unova_StriatonGym_Text_ChaveJaApertada, MSGBOX_DEFAULT
	release
	end

Unova_StriatonGym_EventScript_Placa3::
	msgbox Unova_StriatonGym_Text_Waiter1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa4::
	msgbox Unova_StriatonGym_Text_Waiter2StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa5::
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa6::
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa7::
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymSeenText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa8::
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymSeenText, MSGBOX_SIGN
	end

@ `StriatonGymTableSwitch` da fonte: a mesa de (3,6), interruptor 3.
Unova_StriatonGym_EventScript_Placa9::
	lock
	goto_if_set FLAG_UNOVA_STRIATON_CHAVE_3, Unova_StriatonGym_EventScript_ChaveJaApertada
	setflag FLAG_UNOVA_STRIATON_CHAVE_3
	msgbox Unova_StriatonGym_Text_StriatonGymPressSwitchText, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	waitse
	call Unova_StriatonGym_EventScript_TalvezAbra
	release
	end

Unova_StriatonGym_EventScript_Placa10::
	msgbox Unova_StriatonGym_Text_StriatonGymTableNothingText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Placa11::
	msgbox Unova_StriatonGym_Text_StriatonGymTableNothingText, MSGBOX_SIGN
	end

Unova_StriatonGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_CILAN, Unova_StriatonGym_Text_CilanGymIntroText, Unova_StriatonGym_Text_CilanWinLossText, Unova_StriatonGym_EventScript_Insignia0
	end

Unova_StriatonGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_STRIATON
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_StriatonGym_EventScript_Npc1::
	msgbox Unova_StriatonGym_Text_StriatonGymGuyText, MSGBOX_NPC
	end

Unova_StriatonGym_EventScript_Npc2::
	msgbox Unova_StriatonGym_Text_StriatonGymBartender1Text, MSGBOX_NPC
	end

@ `StriatonGymBartender2Script` da fonte: o barman de (12,6), interruptor 1. E o
@ unico dos tres que pergunta antes, com `yesorno`.
Unova_StriatonGym_EventScript_Npc3::
	lock
	faceplayer
	goto_if_set FLAG_UNOVA_STRIATON_CHAVE_1, Unova_StriatonGym_EventScript_BarmanJaApertou
	msgbox Unova_StriatonGym_Text_StriatonGymBartender2Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Unova_StriatonGym_EventScript_BarmanFim
	setflag FLAG_UNOVA_STRIATON_CHAVE_1
	msgbox Unova_StriatonGym_Text_BarmanAperta, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	waitse
	call Unova_StriatonGym_EventScript_TalvezAbra
Unova_StriatonGym_EventScript_BarmanFim::
	release
	end

Unova_StriatonGym_EventScript_BarmanJaApertou::
	msgbox Unova_StriatonGym_Text_BarmanJaApertou, MSGBOX_DEFAULT
	release
	end

Unova_StriatonGym_EventScript_Npc4::
	trainerbattle_single TRAINER_UNOVA_WAITER_STRIATON_GYM_1, Unova_StriatonGym_Text_Waiter1Seen, Unova_StriatonGym_Text_Waiter1Beaten
	msgbox Unova_StriatonGym_Text_Waiter1StriatonGymAfterText, MSGBOX_AUTOCLOSE
	end

Unova_StriatonGym_EventScript_Npc5::
	trainerbattle_single TRAINER_UNOVA_WAITER_STRIATON_GYM_2, Unova_StriatonGym_Text_Waiter2Seen, Unova_StriatonGym_Text_Waiter2Beaten
	msgbox Unova_StriatonGym_Text_Waiter2StriatonGymAfterText, MSGBOX_AUTOCLOSE
	end

Unova_StriatonGym_EventScript_Npc6::
	trainerbattle_single TRAINER_UNOVA_WAITRESS_STRIATON_GYM_1, Unova_StriatonGym_Text_Waitress1Seen, Unova_StriatonGym_Text_Waitress1Beaten
	msgbox Unova_StriatonGym_Text_Waitress1StriatonGymAfterText, MSGBOX_AUTOCLOSE
	end

Unova_StriatonGym_EventScript_Npc7::
	trainerbattle_single TRAINER_UNOVA_WAITRESS_STRIATON_GYM_2, Unova_StriatonGym_Text_Waitress2Seen, Unova_StriatonGym_Text_Waitress2Beaten
	msgbox Unova_StriatonGym_Text_Waitress2StriatonGymAfterText, MSGBOX_AUTOCLOSE
	end

Unova_StriatonGym_EventScript_Npc8::
	trainerbattle_single TRAINER_UNOVA_WAITRESS_STRIATON_GYM_3, Unova_StriatonGym_Text_Waitress3Seen, Unova_StriatonGym_Text_Waitress3Beaten
	msgbox Unova_StriatonGym_Text_StriatonGymBartender2Text, MSGBOX_AUTOCLOSE
	end


Unova_StriatonGym_Text_StriatonGymPressSwitchText::
	.string "A secret switch!"
	.string "\nLet's press it!$"

Unova_StriatonGym_Text_Waiter1StriatonGymSeenText::
	.string "Aha! You thought"
	.string "\nthere was a switch"
	.string "\pin here, but it"
	.string "\nwas me!$"

Unova_StriatonGym_Text_Waiter2StriatonGymSeenText::
	.string "Aha! I'm a WAITER"
	.string "\nwho's also a POKé-"
	.string "\lMON trainer!$"

Unova_StriatonGym_Text_Waitress1StriatonGymSeenText::
	.string "Welcome! Would you"
	.string "\nlike a water with"
	.string "\lyour battle?$"

Unova_StriatonGym_Text_Waitress2StriatonGymSeenText::
	.string "Battling makes us"
	.string "\nthirsty, right?"
	.string "\pIf you can win"
	.string "\nagainst me, I'll"
	.string "\lgive you a drink!$"

Unova_StriatonGym_Text_StriatonGymTableNothingText::
	.string "There's nothing"
	.string "\nunderneath.$"

Unova_StriatonGym_Text_CilanGymIntroText::
	.string "Welcome to the"
	.string "\nSTRIATON CITY"
	.string "\lPOKéMON GYM."
	.string "\pMy grass POKéMON"
	.string "\nand I have taken"
	.string "\pthe resolve to"
	.string "\nrun this GYM."
	.string "\pSo, no hard"
	.string "\nfeelings, we'll"
	.string "\pbattle whatever"
	.string "\ncomes our way.$"

Unova_StriatonGym_Text_CilanWinLossText::
	.string "Er… Is it over"
	.string "\nnow?$"

Unova_StriatonGym_Text_StriatonGymGuyText::
	.string "Yo, challenger!"
	.string "\pCILAN is the"
	.string "\nleader of this"
	.string "\lGYM. Find the"
	.string "\phidden switches"
	.string "\nto open his door."
	.string "\pHe's going to be"
	.string "\ntough without my"
	.string "\ladvice."
	.string "\pLet's see…"
	.string "\nCILAN's POKéMON"
	.string "\pare all grass"
	.string "\ntype. They have"
	.string "\pmany weaknesses,"
	.string "\nbut also many"
	.string "\lstrengths."
	.string "\pFire and flying"
	.string "\nwould be your best"
	.string "\lbets!$"

Unova_StriatonGym_Text_StriatonGymBartender1Text::
	.string "Welcome to the"
	.string "\nSTRIATON CITY GYM."
	.string "\pIf you want to"
	.string "\nreach the LEADER,"
	.string "\pyou'll need to"
	.string "\nfind the three"
	.string "\psecret switches"
	.string "\nin the gym."
	.string "\pTry checking under"
	.string "\nthe tables.$"

Unova_StriatonGym_Text_StriatonGymBartender2Text::
	.string "Welcome to the"
	.string "\nSTRIATON CITY GYM."
	.string "\pOh? Did you think"
	.string "\nI have one of the"
	.string "\lsecret switches?$"

Unova_StriatonGym_Text_Waiter1StriatonGymAfterText::
	.string "It was kind of"
	.string "\nsmelly in that"
	.string "\lcan…$"

Unova_StriatonGym_Text_Waiter2StriatonGymAfterText::
	.string "Our specialty is"
	.string "\nthe best POKéMON"
	.string "\lbattles.$"

Unova_StriatonGym_Text_Waitress1StriatonGymAfterText::
	.string "I had a feeling"
	.string "\nyou would check"
	.string "\lunder there.$"

Unova_StriatonGym_Text_Waitress2StriatonGymAfterText::
	.string "At a place like"
	.string "\nthis, it's good to"
	.string "\lstay hydrated!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_StriatonGym_EventScript_EstatuaGinasio::
	msgbox Unova_StriatonGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_StriatonGym_Text_EstatuaGinasio::
	.string "STRIATON CITY\n"
	.string "POKéMON GYM$"


@ Falas de encontro e de derrota dos cinco, portadas do BW3G em 12/08/2026 (B5).

Unova_StriatonGym_Text_Waiter1Seen::
	.string "Aha! You thought"
	.string "\nthere was a switch"
	.string "\pin here, but it"
	.string "\nwas me!$"

Unova_StriatonGym_Text_Waiter1Beaten::
	.string "Wasted!$"

Unova_StriatonGym_Text_Waiter2Seen::
	.string "Aha! I'm a WAITER"
	.string "\nwho's also a"
	.string "\lPOKéMON trainer!$"

Unova_StriatonGym_Text_Waiter2Beaten::
	.string "Wonderful battle!"
	.string "\nThe experience is"
	.string "\lmy tip!$"

Unova_StriatonGym_Text_Waitress1Seen::
	.string "Welcome! Would you"
	.string "\nlike a water with"
	.string "\lyour battle?$"

Unova_StriatonGym_Text_Waitress1Beaten::
	.string "Ah, bravo!$"

Unova_StriatonGym_Text_Waitress2Seen::
	.string "Battling makes us"
	.string "\nthirsty, right?"
	.string "\pIf you can win"
	.string "\nagainst me, I'll"
	.string "\lgive you a drink!$"

Unova_StriatonGym_Text_Waitress2Beaten::
	.string "The battle made me"
	.string "\neven thirstier!$"

Unova_StriatonGym_Text_Waitress3Seen::
	.string "Nope, sorry! I'm"
	.string "\na trainer!$"

Unova_StriatonGym_Text_Waitress3Beaten::
	.string "Oh no! My POKéMON!$"

@ Textos dos tres interruptores, do BW3G (StriatonGymSwitch1Text,
@ StriatonGymSwitchPressedText e StriatonGymBartender2PressedText).
Unova_StriatonGym_Text_BarmanAperta::
	.string "Well you're right!\n"
	.string "Press the switch!$"

Unova_StriatonGym_Text_BarmanJaApertou::
	.string "Go find the other switches!$"

Unova_StriatonGym_Text_ChaveJaApertada::
	.string "The switch is already pressed.$"

Unova_StriatonGym_Text_EscadaAbriu::
	.string "A staircase appeared at the back\n"
	.string "of the GYM!$"
