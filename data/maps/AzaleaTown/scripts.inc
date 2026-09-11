@ AZALEA TOWN, portado de fontes-mapas/hns/data/maps/AzaleaTown/scripts.inc.
@ ponytail: o enredo de VAR_AZALEA_TOWN_STATE do hns foi cortado inteiro. Aqui
@ a cidade e a Rocket bloqueando o ginasio ate o PROTON cair no Slowpoke Well.
@ Quem lembra que a Rocket ja foi embora: FLAG_HIDE_AZALEA_TOWN_ROCKETS, unica
@ flag pedida por este arco. Zero var. As falas que dependem do progresso usam
@ goto_if_defeated TRAINER_JOHTO_ROCKET_PROTON, que o motor grava de graca.
@ Nao portado: GS Ball e a cena do Kurt na porta de casa. Ver PENDENCIAS-JOHTO.md.
@
@ 06/08/2026: o SILVER entrou. Segunda batalha do rival, texto do pokecrystal
@ (maps/AzaleaTown.asm). Time fixo e gatilho por raio de visao, pelos mesmos
@ dois motivos explicados em data/maps/CherrygroveCity/scripts.inc. A ORDEM dos
@ encontros sai do ON_TRANSITION: aqui ele so aparece depois que o SILVER de
@ Cherrygrove caiu, e some quando este cair. Zero var.

AzaleaTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AzaleaTown_OnTransition
	.byte 0

AzaleaTown_OnTransition:
	call AzaleaTown_EventScript_PoeGruntNaPortaDoGinasio
	setflag FLAG_HIDE_SILVER_AZALEA
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_1, AzaleaTown_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_2, AzaleaTown_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_AZALEA
AzaleaTown_EventScript_SilverFim:
	end

AzaleaTown_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_2, AzaleaTown_Text_SilverSeen, AzaleaTown_Text_SilverBeaten
	msgbox AzaleaTown_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_AZALEA
	removeobject LOCALID_AZALEA_TOWN_SILVER
	release
	end

AzaleaTown_EventScript_Rocket1::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Rocket1, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_Rocket2::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Rocket2, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_Gramps::
	lock
	faceplayer
	goto_if_defeated TRAINER_JOHTO_ROCKET_PROTON, AzaleaTown_EventScript_GrampsAfter
	msgbox AzaleaTown_Text_GrampsBefore, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_GrampsAfter::
	msgbox AzaleaTown_Text_GrampsAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_Lass::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Teacher, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_Youngster::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_GymSign::
	lock
	msgbox AzaleaTown_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_EventScript_KurtSign::
	lock
	msgbox AzaleaTown_Text_KurtsHouseSign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_EventScript_KilnSign::
	lock
	msgbox AzaleaTown_Text_CharcoalKilnSign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_EventScript_IlexSign::
	lock
	msgbox AzaleaTown_Text_IlexForestSign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_EventScript_WellSign::
	lock
	msgbox AzaleaTown_Text_SlowpokeWellSign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_EventScript_AzaleaSign::
	lock
	msgbox AzaleaTown_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

AzaleaTown_Text_Rocket1:
	.string "It's unsafe to go in there,\n"
	.string "so I'm standing guard.\p"
	.string "Aren't I a good Samaritan?$"

AzaleaTown_Text_Rocket2:
	.string "Do you know about SLOWPOKETAIL?\n"
	.string "I heard it's tasty!\p"
	.string "Aren't you glad I told you that?\p"
	.string "Now beat it. Nobody uses this GYM\n"
	.string "while we're working.$"

AzaleaTown_Text_GrampsBefore:
	.string "The SLOWPOKE have disappeared\n"
	.string "from town…\p"
	.string "I heard their TAILS are being\n"
	.string "sold somewhere.$"

AzaleaTown_Text_GrampsAfter:
	.string "The SLOWPOKE have returned.\p"
	.string "Knowing them, they could've just\n"
	.string "been goofing off somewhere.$"

AzaleaTown_Text_Teacher:
	.string "Did you come to get KURT to make\n"
	.string "some BALLS?\p"
	.string "A lot of people do just that.$"

AzaleaTown_Text_Youngster:
	.string "Cut through AZALEA and you'll be\n"
	.string "in ILEX FOREST.\p"
	.string "But these skinny trees make it\n"
	.string "impossible to get through.\p"
	.string "The CHARCOAL MAN's POKéMON\n"
	.string "can CUT down trees.$"

AzaleaTown_Text_Sign:
	.string "AZALEA TOWN\n"
	.string "Where People and POKéMON Live in\l"
	.string "Happy Harmony.$"

AzaleaTown_Text_KurtsHouseSign:
	.string "KURT'S HOUSE$"

AzaleaTown_Text_GymSign:
	.string "AZALEA TOWN\n"
	.string "POKéMON GYM\p"
	.string "LEADER: BUGSY\p"
	.string "The Walking Bug POKéMON\n"
	.string "Encyclopedia$"

AzaleaTown_Text_SlowpokeWellSign:
	.string "SLOWPOKE WELL\p"
	.string "Also known as the RAINMAKER WELL.\p"
	.string "Locals believe that a SLOWPOKE's\n"
	.string "yawn summons rain.\p"
	.string "Records show that a SLOWPOKE's\n"
	.string "yawn ended a drought 400 years ago.$"

AzaleaTown_Text_CharcoalKilnSign:
	.string "CHARCOAL KILN$"

AzaleaTown_Text_IlexForestSign:
	.string "ILEX FOREST\p"
	.string "Enter through the gate.$"

AzaleaTown_Text_SilverSeen:
	.string "…Tell me something.\p"
	.string "Is it true that TEAM ROCKET has\n"
	.string "returned?\p"
	.string "What? You beat them? Hah!\n"
	.string "Quit lying.\p"
	.string "You're not joking? Then let's see\n"
	.string "how good you are.$"

AzaleaTown_Text_SilverBeaten:
	.string "… Humph! Useless POKéMON!\p"
	.string "Listen, you. You only won because\n"
	.string "my POKéMON were weak.$"

AzaleaTown_Text_SilverAfter:
	.string "I hate the weak.\p"
	.string "POKéMON, trainers. It doesn't\n"
	.string "matter who or what.\p"
	.string "I'm going to be strong and wipe\n"
	.string "out the weak.\p"
	.string "That goes for TEAM ROCKET too.\p"
	.string "They act big and tough in a group.\p"
	.string "But get them alone, and they're\n"
	.string "weak.\p"
	.string "I hate them all.\p"
	.string "You stay out of my way. A weakling\n"
	.string "like you is only a distraction.$"

@ >>> POKéBALL FACTORY (cópia do Scorched Silver, resposta 67) >>>
@ O prédio azul alto do canto noroeste é a POKéBALL FACTORY, e a fachada dele
@ veio junto com o desenho da cidade. A porta é o warp 8 da Azalea do Sloo, em
@ (13,15), que aqui entrou como o warp 7, no FIM da lista (a save guarda índice
@ de warp, então warp novo nunca entra no meio).
@
@ O capanga colado na porta do ginásio, em (22,34), é o portão do ginásio, como
@ no hack. Ele não tem flag própria: o campo `flag` do objeto é
@ FLAG_FABRICA_AZALEA_LIMPA, e "escondido quando a flag está acesa" já resolve.

@ O capanga da fábrica é o portão do ginásio, então o lugar dele é (22,34), o
@ tile de onde se entra na porta em (22,33). Só que (22,34) também é onde o warp
@ 6 LARGA quem sai do ginásio, e template parado ali acende a regra A3 do
@ dev_scripts/qa/mapas_qa.py. Por isso o template dele mora em (21,34) e é o
@ ON_TRANSITION que o empurra para a porta enquanto a fábrica não foi limpa.
@ Na prática ninguém sai do ginásio com ele lá: para ter entrado, a flag já
@ estava acesa, e com ela acesa o objeto nem existe.
@ `setobjectxyperm` grava no template dentro da save, então os DOIS lados são
@ escritos, senão ele ficaria preso na porta para sempre.
AzaleaTown_EventScript_PoeGruntNaPortaDoGinasio:
	goto_if_set FLAG_FABRICA_AZALEA_LIMPA, AzaleaTown_EventScript_TiraGruntDaPortaDoGinasio
	setobjectxyperm LOCALID_AZALEA_TOWN_GRUNT_FABRICA, 22, 34
	return

AzaleaTown_EventScript_TiraGruntDaPortaDoGinasio:
	setobjectxyperm LOCALID_AZALEA_TOWN_GRUNT_FABRICA, 21, 34
	return

AzaleaTown_EventScript_GruntFabrica::
	lock
	faceplayer
	msgbox AzaleaTown_Text_GruntFabrica, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_EventScript_FabricaSign::
	lock
	msgbox AzaleaTown_Text_FabricaSign, MSGBOX_SIGN
	closemessage
	release
	end

@ A casa do meio do norte, em (27,12), é o terceiro prédio de morar do desenho
@ do Sloo, e a nossa Azalea só tem duas casas (a do KURT e o CHARCOAL KILN).
@ Prédio do hack sem equivalente nosso leva a placa `closed` em inglês, que é o
@ molde das 31 portas fechadas de Johto (data/scripts/portas_fechadas.inc).
AzaleaTown_EventScript_PortaFechada::
	msgbox Common_Text_PortaFechada, MSGBOX_SIGN
	end

AzaleaTown_Text_GruntFabrica:
	.string "Some daqui, moleque.\p"
	.string "Ninguém entra no ginásio enquanto\n"
	.string "a EQUIPE ROCKET estiver trabalhando\l"
	.string "na fábrica de bolas.\p"
	.string "E não, você não vai olhar.$"

AzaleaTown_Text_FabricaSign:
	.string "POKéBALL FACTORY\p"
	.string "Toda bola de APRICORN de JOHTO\n"
	.string "sai daqui.$"

@ <<< POKéBALL FACTORY <<<

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

AzaleaTown_EventScript_Povoa1::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Text_Povoa1:
	.string "KURT makes BALLS out of\nAPRICORNS. By hand, one at a time.$"

AzaleaTown_EventScript_Povoa2::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Text_Povoa2:
	.string "SLOWPOKE WELL is under the town.\nThe SLOWPOKE are back, thankfully.$"

AzaleaTown_EventScript_Povoa3::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Text_Povoa3:
	.string "ILEX FOREST is west through the\ngate. It is easy to get lost.$"

AzaleaTown_EventScript_Povoa4::
	lock
	faceplayer
	msgbox AzaleaTown_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Text_Povoa4:
	.string "The GYM here is bugs.\nFire and Flying moves end it fast.$"

@ <<< Povoamento: fim do bloco gerado <<<
