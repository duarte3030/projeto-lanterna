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
