@ Ginasio de CIANWOOD CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_6. Zero var gasta.
@
@ 12/08/2026 (B5), no map.json e nao aqui: o QUEBRA-CABECA do ginasio estava
@ faltando inteiro. O hns tem 3 OBJ_EVENT_GFX_PUSHABLE_BOULDER em (10,8), (10,6)
@ e (10,4) com EventScript_StrengthBoulder, mais 2 OBJ_EVENT_GFX_BREAKABLE_ROCK
@ em (9,2) e (11,2) com EventScript_RockSmash; o importador trouxe so os cinco
@ humanos. Sem eles a coluna 10 e um corredor livre da porta ate o CHUCK.
@ Medido: o blockdata de LAYOUT_CIANWOOD_GYM aqui e byte a byte igual ao do hns
@ (21x17, metatiles 746 nos tres tiles de pedra e 744 nos dois de rocha), entao
@ as coordenadas da fonte valem sem correcao. Os cinco entraram no FIM da lista
@ de object_events, para nao renumerar os cinco que ja existiam (a save do Gui
@ guarda indice de objeto). Zero var, zero flag: EventScript_StrengthBoulder e
@ EventScript_RockSmash sao os scripts comuns do motor
@ (data/scripts/field_move_scripts.inc).

CianwoodGym_MapScripts::
	.byte 0

CianwoodGym_EventScript_Nob::
	trainerbattle_single TRAINER_JOHTO_BLACK_BELT_NOB, CianwoodGym_Text_NobSeen, CianwoodGym_Text_NobBeaten
	msgbox CianwoodGym_Text_NobAfter, MSGBOX_AUTOCLOSE
	end

CianwoodGym_EventScript_Yoshi::
	trainerbattle_single TRAINER_JOHTO_BLACK_BELT_YOSHI, CianwoodGym_Text_YoshiSeen, CianwoodGym_Text_YoshiBeaten
	msgbox CianwoodGym_Text_YoshiAfter, MSGBOX_AUTOCLOSE
	end

CianwoodGym_EventScript_Lao::
	trainerbattle_single TRAINER_JOHTO_BLACK_BELT_LAO, CianwoodGym_Text_LaoSeen, CianwoodGym_Text_LaoBeaten
	msgbox CianwoodGym_Text_LaoAfter, MSGBOX_AUTOCLOSE
	end

CianwoodGym_EventScript_Lung::
	trainerbattle_single TRAINER_JOHTO_BLACK_BELT_LUNG, CianwoodGym_Text_LungSeen, CianwoodGym_Text_LungBeaten
	msgbox CianwoodGym_Text_LungAfter, MSGBOX_AUTOCLOSE
	end

CianwoodGym_EventScript_Chuck::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_6, CianwoodGym_EventScript_ChuckDerrotado
	msgbox CianwoodGym_Text_ChuckIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_CHUCK, CianwoodGym_Text_ChuckDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox CianwoodGym_Text_ChuckBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_6
	closemessage
	release
	end

CianwoodGym_EventScript_ChuckDerrotado::
	msgbox CianwoodGym_Text_ChuckPost, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodGym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_6, CianwoodGym_EventScript_StatueCertified
	msgbox CianwoodGym_Text_Statue, MSGBOX_SIGN
	end

CianwoodGym_EventScript_StatueCertified::
	msgbox CianwoodGym_Text_StatueCertified, MSGBOX_SIGN
	end

CianwoodGym_Text_NobSeen:
	.string "Words are useless.\n"
	.string "Let your fists do the talking!$"

CianwoodGym_Text_NobBeaten:
	.string "…$"

CianwoodGym_Text_NobAfter:
	.string "I lost! I'm speechless!$"

CianwoodGym_Text_YoshiSeen:
	.string "My POKéMON and I are bound togeth-\n"
	.string "er by friendship.\p"
	.string "Our bond will never be broken!$"

CianwoodGym_Text_YoshiBeaten:
	.string "This isn't real!$"

CianwoodGym_Text_YoshiAfter:
	.string "You seem to have a strong bond\n"
	.string "with your POKéMON too!$"

CianwoodGym_Text_LaoSeen:
	.string "We martial artists fear nothing!$"

CianwoodGym_Text_LaoBeaten:
	.string "That's shocking!$"

CianwoodGym_Text_LaoAfter:
	.string "Fighting POKéMON are afraid of\n"
	.string "psychics…$"

CianwoodGym_Text_LungSeen:
	.string "My raging fists will shatter your\n"
	.string "POKéMON!$"

CianwoodGym_Text_LungBeaten:
	.string "I got shattered!$"

CianwoodGym_Text_LungAfter:
	.string "My POKéMON lost…\n"
	.string "My… my pride is shattered…$"

CianwoodGym_Text_ChuckIntro:
	.string "WAHAHAH!\p"
	.string "So you've come this far!\p"
	.string "Let me tell you, I'm tough!\p"
	.string "My POKéMON will crush stones and\n"
	.string "shatter bones!\p"
	.string "Watch this!$"

CianwoodGym_Text_ChuckDefeat:
	.string "CHUCK: Urggh!\n"
	.string "…\p"
	.string "Oooarrgh!$"

CianwoodGym_Text_ChuckBadge:
	.string "STORMBADGE makes all POKéMON up to\n"
	.string "L70 obey, even traded ones.\p"
	.string "It also lets your POKéMON use FLY\n"
	.string "when you're not in a battle.\p"
	.string "Here, take this too!$"

CianwoodGym_Text_ChuckPost:
	.string "WAHAHAH! I enjoyed battling you!\p"
	.string "But a loss is a loss!\p"
	.string "From now on, I'm going to train\n"
	.string "24 hours a day!$"

CianwoodGym_Text_Statue:
	.string "CIANWOOD CITY POKéMON GYM\n"
	.string "Leader: CHUCK$"

CianwoodGym_Text_StatueCertified:
	.string "CIANWOOD CITY POKéMON GYM\p"
	.string "CHUCK'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
