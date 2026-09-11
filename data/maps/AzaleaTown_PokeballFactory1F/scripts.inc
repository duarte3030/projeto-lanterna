@ POKéBALL FACTORY de AZALEA TOWN, térreo. A ARTE é do Scorched Silver (g32m0,
@ 19x12, cópia byte a byte pelo método de `Pokemon Claude/METODO-COPIA-CIDADES.md`).
@ O JOGO é nosso: os capangas são da EQUIPE ROCKET de Johto, não da Team Phoenix
@ do hack, e nenhuma linha de texto do Sloo entrou aqui.
@
@ UMA flag segura o arco inteiro, FLAG_FABRICA_AZALEA_LIMPA:
@   apagada -> capangas de pé, loja fechada, ginásio de Azalea trancado;
@   acesa   -> capangas somem (é a flag de esconder deles), loja abre, ginásio abre.
@ Zero `special` novo, zero C novo: só pokemart, checkflag, setflag, msgbox,
@ trainerbattle, applymovement e giveitem. Nem uma var foi gasta.
@
@ Nenhum capanga tem RAIO DE VISÃO: os cinco são porteiros, e a batalha começa
@ quando o jogador fala com eles. É de propósito, e por duas razões. A primeira
@ é de desenho: quem trabalha na porta manda o jogador parar, não corre atrás
@ dele. A segunda é de teste: capanga que puxa batalha sozinho torna qualquer
@ percurso do harness dependente de sorte de posição.
@
@ O capanga da ESCADA fica em cima de (12,5), que é o ÚNICO tile de onde se
@ alcança a porta do segundo andar em (12,4): ele é o portão de verdade, não
@ enfeite. Depois de perder ele anda um passo para a direita.
@ O TEMPLATE dele no map.json fica em (13,5), e não em (12,5), e o ON_TRANSITION
@ é que o empurra para cima da escada enquanto ele não foi derrotado. É de
@ propósito: (12,5) é o tile de CHEGADA de quem desce do segundo andar, e
@ template parado ali acende a regra A3 do dev_scripts/qa/mapas_qa.py ("o warp
@ larga o jogador em cima de um objeto sólido"). Com a ordem invertida, quem
@ desce nunca cai em cima dele, porque para ter subido já precisou derrotá-lo.

AzaleaTown_PokeballFactory1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AzaleaTown_PokeballFactory1F_OnTransition
	.byte 0

AzaleaTown_PokeballFactory1F_OnTransition:
	goto_if_defeated TRAINER_JOHTO_ROCKET_FABRICA_ESCADA, AzaleaTown_PokeballFactory1F_EventScript_EscadaLivre
	setobjectxyperm LOCALID_FABRICA_1F_GRUNT_ESCADA, 12, 5
	end

@ `setobjectxyperm` grava no template DENTRO da save, e por isso os dois lados
@ precisam ser escritos: só o "põe na escada" deixaria o capanga de volta em
@ cima dela na carga seguinte, mesmo depois de derrotado.
AzaleaTown_PokeballFactory1F_EventScript_EscadaLivre:
	setobjectxyperm LOCALID_FABRICA_1F_GRUNT_ESCADA, 13, 5
	end

@ ---------------------------------------------------------------- a loja

AzaleaTown_PokeballFactory1F_EventScript_Balconista::
	lock
	faceplayer
	goto_if_unset FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory1F_EventScript_LojaFechada
	message AzaleaTown_PokeballFactory1F_Text_LojaAberta
	waitmessage
	pokemart AzaleaTown_PokeballFactory1F_Pokemart
	msgbox AzaleaTown_PokeballFactory1F_Text_LojaVolteSempre, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_LojaFechada::
	msgbox AzaleaTown_PokeballFactory1F_Text_LojaFechada, MSGBOX_DEFAULT
	closemessage
	release
	end

	.align 2
AzaleaTown_PokeballFactory1F_Pokemart:
	.2byte ITEM_LEVEL_BALL
	.2byte ITEM_LURE_BALL
	.2byte ITEM_MOON_BALL
	.2byte ITEM_FRIEND_BALL
	.2byte ITEM_LOVE_BALL
	.2byte ITEM_FAST_BALL
	.2byte ITEM_HEAVY_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_LUXURY_BALL
	.2byte ITEM_MASTER_BALL
	pokemartlistend

@ ------------------------------------------------------------- os capangas

AzaleaTown_PokeballFactory1F_EventScript_GruntEscada::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_ESCADA, AzaleaTown_PokeballFactory1F_Text_EscadaVer, AzaleaTown_PokeballFactory1F_Text_EscadaPerder, AzaleaTown_PokeballFactory1F_EventScript_EscadaSaiDaFrente
	msgbox AzaleaTown_PokeballFactory1F_Text_EscadaDepois, MSGBOX_AUTOCLOSE
	end

AzaleaTown_PokeballFactory1F_EventScript_EscadaSaiDaFrente::
	msgbox AzaleaTown_PokeballFactory1F_Text_EscadaDepois, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FABRICA_1F_GRUNT_ESCADA, AzaleaTown_PokeballFactory1F_Movement_EscadaSai
	waitmovement 0
	setobjectxyperm LOCALID_FABRICA_1F_GRUNT_ESCADA, 13, 5
	release
	end

AzaleaTown_PokeballFactory1F_Movement_EscadaSai:
	walk_right
	face_left
	step_end

AzaleaTown_PokeballFactory1F_EventScript_GruntTerreo::
	trainerbattle_single TRAINER_JOHTO_ROCKET_FABRICA_TERREO, AzaleaTown_PokeballFactory1F_Text_TerreoVer, AzaleaTown_PokeballFactory1F_Text_TerreoPerder
	msgbox AzaleaTown_PokeballFactory1F_Text_TerreoDepois, MSGBOX_AUTOCLOSE
	end

@ ------------------------------------------------------------- os clientes

AzaleaTown_PokeballFactory1F_EventScript_Cliente1::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory1F_EventScript_Cliente1Depois
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente1Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_Cliente1Depois::
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente1Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_Cliente2::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory1F_EventScript_Cliente2Depois
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente2Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_Cliente2Depois::
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente2Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_Cliente3::
	lock
	faceplayer
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_PokeballFactory1F_EventScript_Cliente3Depois
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente3Antes, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokeballFactory1F_EventScript_Cliente3Depois::
	msgbox AzaleaTown_PokeballFactory1F_Text_Cliente3Depois, MSGBOX_DEFAULT
	closemessage
	release
	end

@ ------------------------------------------------------------------ textos

AzaleaTown_PokeballFactory1F_Text_LojaFechada:
	.string "Sorry, the shop is closed.\p"
	.string "Those guys in black went up to\n"
	.string "the factory floor and told us all\l"
	.string "to keep quiet down here.\p"
	.string "Please, help our boss!$"

AzaleaTown_PokeballFactory1F_Text_LojaAberta:
	.string "Welcome to the POKéBALL FACTORY!\n"
	.string "How may I help you?$"

AzaleaTown_PokeballFactory1F_Text_LojaVolteSempre:
	.string "Please come again!$"

AzaleaTown_PokeballFactory1F_Text_EscadaVer:
	.string "Hold it right there.\p"
	.string "Nobody goes upstairs until the\n"
	.string "job is done. Boss's orders.$"

AzaleaTown_PokeballFactory1F_Text_EscadaPerder:
	.string "I lost… to a kid?$"

AzaleaTown_PokeballFactory1F_Text_EscadaDepois:
	.string "Go up, then. You'll regret ever\n"
	.string "climbing those stairs.$"

AzaleaTown_PokeballFactory1F_Text_TerreoVer:
	.string "Get lost! The factory is\n"
	.string "closed today!$"

AzaleaTown_PokeballFactory1F_Text_TerreoPerder:
	.string "Ow! Nobody warned me about this!$"

AzaleaTown_PokeballFactory1F_Text_TerreoDepois:
	.string "TEAM ROCKET came here for a\n"
	.string "MASTER BALL, and we'll get one.$"

AzaleaTown_PokeballFactory1F_Text_Cliente1Antes:
	.string "I came in to buy a LEVEL BALL\n"
	.string "and walked into all of this.\p"
	.string "I'm pretending I saw nothing.$"

AzaleaTown_PokeballFactory1F_Text_Cliente1Depois:
	.string "The BALLS in the window are\n"
	.string "just for show.\p"
	.string "The real ones are behind the\n"
	.string "counter and up on the floor.$"

AzaleaTown_PokeballFactory1F_Text_Cliente2Antes:
	.string "I came for BALLS for my farm and\n"
	.string "found the shop like this.\p"
	.string "What a day to go shopping…$"

AzaleaTown_PokeballFactory1F_Text_Cliente2Depois:
	.string "I always take HEAVY BALLS back\n"
	.string "to the farm. Big beasts are\l"
	.string "stubborn.$"

AzaleaTown_PokeballFactory1F_Text_Cliente3Antes:
	.string "Fifty thousand for one\n"
	.string "MASTER BALL!\p"
	.string "It's dear, but the BALL that\n"
	.string "never misses is worth it.$"

AzaleaTown_PokeballFactory1F_Text_Cliente3Depois:
	.string "CARMEN makes every BALL here\n"
	.string "with the recipe KURT taught her.\p"
	.string "That's why they beat the ones\n"
	.string "from the shop on the corner.$"
