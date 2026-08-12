@ NEW BARK TOWN, LABORATORIO DO PROFESSOR ELM.
@
@ Entrega do trio de iniciais de Johto (decisao 68): CHIKORITA, CYNDAQUIL e
@ TOTODILE, nas tres Poke Bolas da mesa, em (8,4), (9,4) e (10,4). Ate
@ 05/08/2026 este mapa nao entregava inicial nenhum: os sete objetos vieram da
@ importacao como OBJ_EVENT_GFX_ITEM_BALL inertes, com script "0". Tres deles
@ viraram as bolas do trio; os outros quatro continuam decoracao.
@
@ Padrao copiado de Kanto (data/maps/PalletTown_ProfessorOaksLab_Frlg) e de
@ Sinnoh (data/maps/SandgemTown_House1), sem mecanica nova:
@
@ 1. VAR_STARTER_MON e escrita aqui: 0=CHIKORITA, 1=CYNDAQUIL, 2=TOTODILE
@    (grama, fogo, agua, a mesma ordem de Hoenn e de Sinnoh). E ela que permite
@    um rival montar time por triangulo de tipos. Foi a falta dela que obrigou o
@    time do SILVER a ser fixo, ver o cabecalho de
@    data/maps/CherrygroveCity/scripts.inc.
@
@ 2. As tres bolas somem depois da escolha por DOIS caminhos, e os dois sao
@    necessarios: o campo "flag" das tres no map.json aponta para
@    FLAG_INICIAL_JOHTO, o que impede o objeto de nascer nas proximas entradas
@    no mapa, e os tres `removeobject` abaixo tiram as outras duas da tela AGORA.
@    Sem o removeobject o jogador pega os tres iniciais na mesma visita, porque
@    a flag so e lida quando o mapa carrega.
@
@ 3. A flag e FLAG_INICIAL_JOHTO, e nao FLAG_SYS_POKEMON_GET: com a ordem
@    cronologica (decisao 66) quem acende a FLAG_SYS_POKEMON_GET e o Oak, em
@    Kanto, antes de o jogador pisar em Johto. Ver o bloco "Trio de iniciais por
@    regiao" em include/constants/flags.h.
@
@ Nivel 20: e o piso da faixa de Johto na curva nova (Johto vai de 22 a 58, ver
@ dev_scripts/curva_de_nivel.py). Um inicial de nivel 5 na segunda regiao seria
@ inutil no minuto seguinte.
@
@ Ponytail: nao ha NPC do ELM neste mapa. Ele nao e necessario para a entrega
@ (as bolas falam por si, como em Kanto), e inventar falas para ele seria
@ escrever enredo, o que a decisao 69 proibe. Se um dia o texto do pokecrystal
@ for portado, o objeto 2, em (6,3), e o lugar dele.
@
@ As duas unicas falas daqui NAO sao do pokecrystal: sao avisos mecanicos (a
@ pergunta sim/nao de cada bola e a linha de "recebeu"), porque no jogo original
@ quem escolhe e uma tela de menu que este mapa nao tem. Mesma solucao que o
@ laboratorio do ROWAN ja usa.

NewBarkTown_Lab_MapScripts::
	.byte 0

NewBarkTown_Lab_EventScript_BallChikorita::
	lock
	faceplayer
	showmonpic SPECIES_CHIKORITA, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_CHIKORITA
	msgbox NewBarkTown_Lab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NewBarkTown_Lab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_CHIKORITA, 20
	setvar VAR_STARTER_MON, 0
	goto NewBarkTown_Lab_EventScript_ChoseStarter

NewBarkTown_Lab_EventScript_BallCyndaquil::
	lock
	faceplayer
	showmonpic SPECIES_CYNDAQUIL, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_CYNDAQUIL
	msgbox NewBarkTown_Lab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NewBarkTown_Lab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_CYNDAQUIL, 20
	setvar VAR_STARTER_MON, 1
	goto NewBarkTown_Lab_EventScript_ChoseStarter

NewBarkTown_Lab_EventScript_BallTotodile::
	lock
	faceplayer
	showmonpic SPECIES_TOTODILE, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_TOTODILE
	msgbox NewBarkTown_Lab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NewBarkTown_Lab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_TOTODILE, 20
	setvar VAR_STARTER_MON, 2
	goto NewBarkTown_Lab_EventScript_ChoseStarter

NewBarkTown_Lab_EventScript_DeclinedStarter::
	hidemonpic
	release
	end

NewBarkTown_Lab_EventScript_ChoseStarter::
	setflag FLAG_INICIAL_JOHTO
	setflag FLAG_SYS_POKEMON_GET
	message NewBarkTown_Lab_Text_ReceivedStarter
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NewBarkTown_Lab_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call Common_EventScript_NameReceivedPartyMon
	goto NewBarkTown_Lab_EventScript_AfterStarter

NewBarkTown_Lab_EventScript_AfterStarter::
	removeobject LOCALID_ELM_LAB_BALL_CHIKORITA
	removeobject LOCALID_ELM_LAB_BALL_CYNDAQUIL
	removeobject LOCALID_ELM_LAB_BALL_TOTODILE
	release
	end

@ Aviso mecanico, nao e fala do pokecrystal: no jogo original a escolha e uma tela.
NewBarkTown_Lab_Text_WillYouTakeThisOne:
	.string "This POKé BALL holds a\n"
	.string "{STR_VAR_1}.\p"
	.string "Will you take this one?$"

@ Aviso mecanico, nao e fala do pokecrystal.
NewBarkTown_Lab_Text_ReceivedStarter:
	.string "{PLAYER} received the\n"
	.string "{STR_VAR_1}!$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

NewBarkTown_Lab_EventScript_HealingMachine1::
	lock
	goto_if_set FLAG_SYS_POKEMON_GET, NewBarkTown_Lab_EventScript_HealingMachine2
	msgbox LittlerootTown_ProfessorBirchsLab_Text_SeriousLookingMachine, MSGBOX_SIGN
	closemessage
	release
	end

NewBarkTown_Lab_EventScript_HealingMachine2::
	call Common_EventScript_OutOfCenterPartyHeal
	release
	end

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

NewBarkTown_EventScript_Aide1::
	lock
	faceplayer
	msgbox NewBarkTown_Lab_Text_AideAlwaysBusy, MSGBOX_DEFAULT
	closemessage
	release
	end

NewBarkTown_Lab_Text_AideAlwaysBusy::
	.string "There are only three of us, so\n"
	.string "we're always busy.$"
