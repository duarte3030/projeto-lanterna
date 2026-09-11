@ POKéBALL FACTORY de AZALEA TOWN, segundo andar (o chão de fábrica). ARTE do
@ Scorched Silver (g32m1, 20x14), cópia byte a byte. JOGO nosso: quem assalta é
@ a EQUIPE ROCKET de Johto, a mesma do SLOWPOKE WELL, e não a Team Phoenix do
@ hack. Nenhuma linha do Sloo entrou.
@
@ GEOMETRIA, medida no blockdata e não chutada: do alto do mapa para a metade de
@ baixo existem DOIS caminhos, e os dois passam por UM tile cada. O corredor do
@ meio aperta em (13,11) e o do depósito aperta em (19,9). Um capanga em cada um
@ desses tiles é portão de verdade: não dá para chegar na CARMEN sem derrotar um
@ dos dois. Depois de perder, cada um anda para o lado e o ON_TRANSITION repete
@ esse passo em toda carga do mapa, senão o objeto renasceria em cima do
@ corredor e trancaria o andar.
@
@ O tile (7,11) é o gargalo do corredor oeste, o único jeito de chegar em (2,12),
@ onde a CARMEN está encurralada. Por isso a cena do chefe fica ali.
@
@ Ela NÃO gasta var. O coord event do gen 3 só sabe comparar var, então o dele é
@ VAR_TEMP_0 valendo 0, que o motor zera em toda carga de mapa: o gatilho fica
@ sempre armado e quem diz se a cena roda é a PRIMEIRA linha do script, um
@ `goto_if_set FLAG_FABRICA_AZALEA_LIMPA` que sai antes de qualquer `lockall`,
@ ou seja sem travar o boneco e sem piscar nada na tela. Isso importa porque as
@ duas vagas de var que o briefing desta frente dava como reservadas (0x408B e
@ 0x4091) JÁ TÊM DONO em vars_frlg.h, medido pelo
@ dev_scripts/guarda_colisao_vars.py em 11/09/2026. Nenhuma var foi gasta aqui.

AzaleaTown_PokeballFactory2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AzaleaTown_PokeballFactory2F_OnTransition
	.byte 0

AzaleaTown_PokeballFactory2F_OnTransition:
	call AzaleaTown_PokeballFactory2F_EventScript_ArrumaCorredor
	call AzaleaTown_PokeballFactory2F_EventScript_ArrumaDeposito
	end

AzaleaTown_PokeballFactory2F_EventScript_ArrumaCorredor:
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_FABRICA_CORREDOR, AzaleaTown_PokeballFactory2F_EventScript_NaoMexe
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_CORREDOR, 14, 10
	return

AzaleaTown_PokeballFactory2F_EventScript_ArrumaDeposito:
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_FABRICA_DEPOSITO, AzaleaTown_PokeballFactory2F_EventScript_NaoMexe
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_DEPOSITO, 18, 10
	return

AzaleaTown_PokeballFactory2F_EventScript_NaoMexe:
	return

@ ----------------------------------------------------- os dois portões de chão

AzaleaTown_PokeballFactory2F_EventScript_GruntCorredor::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_CORREDOR, AzaleaTown_PokeballFactory2F_Text_CorredorVer, AzaleaTown_PokeballFactory2F_Text_CorredorPerder, AzaleaTown_PokeballFactory2F_EventScript_CorredorSai
	msgbox AzaleaTown_PokeballFactory2F_Text_CorredorDepois, MSGBOX_AUTOCLOSE
	end

AzaleaTown_PokeballFactory2F_EventScript_CorredorSai::
	msgbox AzaleaTown_PokeballFactory2F_Text_CorredorDepois, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_GRUNT_CORREDOR, AzaleaTown_PokeballFactory2F_Movement_CorredorSai
	waitmovement 0
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_CORREDOR, 14, 10
	release
	end

AzaleaTown_PokeballFactory2F_Movement_CorredorSai:
	walk_up
	walk_right
	face_left
	step_end

AzaleaTown_PokeballFactory2F_EventScript_GruntDeposito::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_DEPOSITO, AzaleaTown_PokeballFactory2F_Text_DepositoVer, AzaleaTown_PokeballFactory2F_Text_DepositoPerder, AzaleaTown_PokeballFactory2F_EventScript_DepositoSai
	msgbox AzaleaTown_PokeballFactory2F_Text_DepositoDepois, MSGBOX_AUTOCLOSE
	end

AzaleaTown_PokeballFactory2F_EventScript_DepositoSai::
	msgbox AzaleaTown_PokeballFactory2F_Text_DepositoDepois, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_GRUNT_DEPOSITO, AzaleaTown_PokeballFactory2F_Movement_DepositoSai
	waitmovement 0
	setobjectxyperm LOCALID_FABRICA_2F_GRUNT_DEPOSITO, 18, 10
	release
	end

AzaleaTown_PokeballFactory2F_Movement_DepositoSai:
	walk_down
	walk_left
	face_right
	step_end

@ ------------------------------------------------------------------- a cena

AzaleaTown_PokeballFactory2F_EventScript_Cena::
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_CenaJaRodou
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeInterroga, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_CHEFE, Common_Movement_ExclamationMark
	waitmovement 0
	delay 30
	applymovement LOCALID_FABRICA_2F_CHEFE, AzaleaTown_PokeballFactory2F_Movement_ChefeVem
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeDesafia, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_FABRICA_CHEFE, AzaleaTown_PokeballFactory2F_Text_ChefePerder
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeFoge, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_2F_CHEFE, AzaleaTown_PokeballFactory2F_Movement_ChefeFoge
	waitmovement 0
	setflag FLAG_FABRICA_AZALEA_LIMPA
	removeobject LOCALID_FABRICA_2F_CHEFE
	removeobject LOCALID_FABRICA_2F_GRUNT_CORREDOR
	removeobject LOCALID_FABRICA_2F_GRUNT_DEPOSITO
	delay 30
	applymovement LOCALID_FABRICA_2F_CARMEN, AzaleaTown_PokeballFactory2F_Movement_CarmenVem
	waitmovement 0
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenAgradece, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_QUICK_BALL, 5
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenDespede, MSGBOX_DEFAULT
	closemessage
	releaseall
	end

AzaleaTown_PokeballFactory2F_EventScript_CenaJaRodou:
	end

AzaleaTown_PokeballFactory2F_Movement_ChefeVem:
	walk_right
	walk_right
	walk_up
	face_right
	step_end

@ (6,11) -> (6,12) -> (6,13): os dois tiles ao sul estão livres no blockdata, e
@ para o leste não há saída, porque (7,12) e (8,12) são parede e (7,11) é o
@ próprio jogador. Ele some logo em seguida, no `removeobject`.
AzaleaTown_PokeballFactory2F_Movement_ChefeFoge:
	walk_fast_down
	walk_fast_down
	step_end

AzaleaTown_PokeballFactory2F_Movement_CarmenVem:
	walk_right
	walk_right
	walk_right
	walk_up
	walk_right
	face_right
	step_end

@ -------------------------------------------------------------- a gente daqui

AzaleaTown_PokeballFactory2F_EventScript_Chefe::
	lock
	faceplayer
	msgbox AzaleaTown_PokeballFactory2F_Text_ChefeParado, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Carmen::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_CarmenDepois
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenAntes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_CarmenDepois::
	msgbox AzaleaTown_PokeballFactory2F_Text_CarmenDepois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario1::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario1Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario1Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario1Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario1Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario2::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario2Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario2Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario2Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario2Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario3::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory2F_EventScript_Operario3Depois
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario3Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory2F_EventScript_Operario3Depois::
	msgbox AzaleaTown_PokeballFactory2F_Text_Operario3Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

@ ------------------------------------------------------------------- textos

AzaleaTown_PokeballFactory2F_Text_ChefeInterroga:
	.string "CHEFE DOS CAPANGAS: Pela última\n"
	.string "vez, dona. Onde guardam as\l"
	.string "MASTER BALL?\p"
	.string "CARMEN: Já disse. O último lote\n"
	.string "saiu daqui para KANTO faz três\l"
	.string "semanas. Não sobrou nenhuma.\p"
	.string "CHEFE DOS CAPANGAS: Então a gente\n"
	.string "leva a receita. E a senhora junto.$"

AzaleaTown_PokeballFactory2F_Text_ChefeDesafia:
	.string "CHEFE DOS CAPANGAS: Você de novo?\p"
	.string "Eu mandei três pessoas cuidarem da\n"
	.string "porta e nenhuma serviu para nada.\p"
	.string "Deixa comigo. Vou te mostrar o que\n"
	.string "é a EQUIPE ROCKET.$"

AzaleaTown_PokeballFactory2F_Text_ChefePerder:
	.string "Não… numa fábrica de bola…$"

AzaleaTown_PokeballFactory2F_Text_ChefeFoge:
	.string "CHEFE DOS CAPANGAS: Guarde essa\n"
	.string "cara, moleque.\p"
	.string "A EQUIPE ROCKET não esquece quem\n"
	.string "atravessa o caminho dela.$"

AzaleaTown_PokeballFactory2F_Text_ChefeParado:
	.string "CHEFE DOS CAPANGAS: Fora daqui.\n"
	.string "Isto é assunto de gente grande.$"

AzaleaTown_PokeballFactory2F_Text_CarmenAntes:
	.string "CARMEN: Fique longe, criança!\p"
	.string "Essa gente entrou atirando ordens\n"
	.string "e não vai embora de graça.$"

AzaleaTown_PokeballFactory2F_Text_CarmenAgradece:
	.string "CARMEN: Eles foram embora…\p"
	.string "Eu sou a CARMEN. A POKéBALL\n"
	.string "FACTORY é minha.\p"
	.string "Aprendi a fazer bola com o KURT,\n"
	.string "aqui do lado, uma por uma e na mão.\p"
	.string "A fábrica é para dar conta do resto\n"
	.string "de JOHTO, mas a receita é dele.\p"
	.string "Leve isto. É o que eu tenho para\n"
	.string "agradecer.$"

AzaleaTown_PokeballFactory2F_Text_CarmenDespede:
	.string "CARMEN: A loja lá embaixo reabre\n"
	.string "agora mesmo.\p"
	.string "Desça quando quiser. Você tem\n"
	.string "crédito nesta casa.$"

AzaleaTown_PokeballFactory2F_Text_CarmenDepois:
	.string "CARMEN: A linha voltou a andar.\p"
	.string "Sete bolas de APRICORN, mais as\n"
	.string "especiais, e a MASTER BALL para\l"
	.string "quem puder pagar.$"

AzaleaTown_PokeballFactory2F_Text_Operario1Antes:
	.string "Travei. Não consigo nem levantar\n"
	.string "da linha de montagem.$"

AzaleaTown_PokeballFactory2F_Text_Operario1Depois:
	.string "Obrigado mesmo. Eu travei de medo\n"
	.string "e você não travou.$"

AzaleaTown_PokeballFactory2F_Text_Operario2Antes:
	.string "Eles querem a MASTER BALL.\p"
	.string "A matéria-prima dela vem de uma\n"
	.string "pedra que quase não existe mais.\l"
	.string "Por isso ela custa o que custa.$"

AzaleaTown_PokeballFactory2F_Text_Operario2Depois:
	.string "Uma MASTER BALL leva meio ano de\n"
	.string "trabalho e uma pedra rara.\p"
	.string "Cinquenta mil é barato, acredite.$"

AzaleaTown_PokeballFactory2F_Text_Operario3Antes:
	.string "A CARMEN está encurralada lá no\n"
	.string "canto, com o chefe deles.\p"
	.string "Alguém precisa chegar até ela.$"

AzaleaTown_PokeballFactory2F_Text_Operario3Depois:
	.string "A CARMEN assumiu a fábrica e não\n"
	.string "mudou uma linha da receita.\p"
	.string "O KURT ainda passa aqui para\n"
	.string "conferir o corte do APRICORN.$"

AzaleaTown_PokeballFactory2F_Text_CorredorVer:
	.string "Este corredor está fechado.\n"
	.string "Ordem da EQUIPE ROCKET.$"

AzaleaTown_PokeballFactory2F_Text_CorredorPerder:
	.string "Como é que eu perdi aqui?$"

AzaleaTown_PokeballFactory2F_Text_CorredorDepois:
	.string "Passa logo. Você vai topar com o\n"
	.string "chefe no fim do corredor.$"

AzaleaTown_PokeballFactory2F_Text_DepositoVer:
	.string "O depósito é por aqui, e você não\n"
	.string "vai entrar nele.$"

AzaleaTown_PokeballFactory2F_Text_DepositoPerder:
	.string "Tudo bem, tudo bem! Eu saio!$"

AzaleaTown_PokeballFactory2F_Text_DepositoDepois:
	.string "Não achamos nenhuma MASTER BALL\n"
	.string "nas prateleiras. Só bola comum.$"
