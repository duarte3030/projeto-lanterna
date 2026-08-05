@ OLIVINE LIGHTHOUSE, portado de fontes-mapas/hns/data/maps/OlivineCity_Lighthouse.
@ ponytail: os nove treinadores abaixo ainda nao existem como TRAINER_ (zero
@ vaga sobrando, ver PENDENCIAS-JOHTO.md secao "torres e farol"). Cena
@ montada com o nome que cada um DEVE ter. Sprite de overworld trocado onde
@ a classe original nao existe nesta build: os dois BIRD_KEEPER (THEO,
@ DENIS) e a COOLTRAINER_F (CONNIE, virou LASS) so tem grafico dentro de #if
@ IS_FRLG; SAILOR e GENTLEMAN sao seguros e ficaram como no hns.
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x26C a 0x26F crus
@ (flags.h esta com outro agente). O TM SHOCK WAVE que o hns tambem deixa
@ nesta sala foi cortado: o script dele e da OlivineCity, que nao e minha
@ nesta tarefa, e nem ITEM_TM_SHOCK_WAVE existe aqui.
@ A JASMINE nao tem sprite (OBJ_EVENT_GFX_JASMINE nem existe como constante),
@ entao a cena da AMPHY doente virou um bg_event (sign) sem NPC visivel: o
@ jogador acha a AMPHY e um bilhete com a fala da JASMINE, igual foi feito
@ com Dialga/Palkia no Spear Pillar. NAO fecha a historia (curar a AMPHY com
@ o Secret Potion e liberar a JASMINE no ginasio): ITEM_SECRET_POTION nao
@ existe, e o unlock mexe em OlivineCity_Gym, que nao e meu. Ver
@ PENDENCIAS-JOHTO.md.

OlivineCity_Lighthouse_MapScripts::
	.byte 0

OlivineLighthouse_EventScript_1FSailor::
	lock
	faceplayer
	msgbox OlivineLighthouse_Text_1FSailor, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineLighthouse_EventScript_1FPokefanF::
	lock
	faceplayer
	msgbox OlivineLighthouse_Text_1FPokefanF, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineLighthouse_EventScript_Huey::
	trainerbattle_single TRAINER_SAILOR_HUEY, OlivineLighthouse_Text_SailorHueySeen, OlivineLighthouse_Text_SailorHueyBeaten
	msgbox OlivineLighthouse_Text_SailorHueyAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_GentlemanAlfred::
	trainerbattle_single TRAINER_GENTLEMAN_ALFRED, OlivineLighthouse_Text_GentlemanAlfredSeen, OlivineLighthouse_Text_GentlemanAlfredBeaten
	msgbox OlivineLighthouse_Text_GentlemanAlfredAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_BirdKeeperTheo::
	trainerbattle_single TRAINER_BIRD_KEEPER_THEO, OlivineLighthouse_Text_BirdKeeperTheoSeen, OlivineLighthouse_Text_BirdKeeperTheoBeaten
	msgbox OlivineLighthouse_Text_BirdKeeperTheoAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_SailorTerrell::
	trainerbattle_single TRAINER_SAILOR_TERRELL, OlivineLighthouse_Text_SailorTerrellSeen, OlivineLighthouse_Text_SailorTerrellBeaten
	msgbox OlivineLighthouse_Text_SailorTerrellAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_GentlemanPreston::
	trainerbattle_single TRAINER_GENTLEMAN_PRESTON, OlivineLighthouse_Text_GentlemanPrestonSeen, OlivineLighthouse_Text_GentlemanPrestonBeaten
	msgbox OlivineLighthouse_Text_GentlemanPrestonAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_SailorKent::
	trainerbattle_single TRAINER_SAILOR_KENT, OlivineLighthouse_Text_SailorKentSeen, OlivineLighthouse_Text_SailorKentBeaten
	msgbox OlivineLighthouse_Text_SailorKentAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_LassConnie::
	trainerbattle_single TRAINER_LASS_CONNIE, OlivineLighthouse_Text_LassConnieSeen, OlivineLighthouse_Text_LassConnieBeaten
	msgbox OlivineLighthouse_Text_LassConnieAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_SailorErnest::
	trainerbattle_single TRAINER_SAILOR_ERNEST, OlivineLighthouse_Text_SailorErnestSeen, OlivineLighthouse_Text_SailorErnestBeaten
	msgbox OlivineLighthouse_Text_SailorErnestAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_BirdKeeperDenis::
	trainerbattle_single TRAINER_BIRD_KEEPER_DENIS, OlivineLighthouse_Text_BirdKeeperDenisSeen, OlivineLighthouse_Text_BirdKeeperDenisBeaten
	msgbox OlivineLighthouse_Text_BirdKeeperDenisAfter, MSGBOX_AUTOCLOSE
	end

OlivineLighthouse_EventScript_Ampharos::
	lock
	msgbox OlivineLighthouse_Text_JasmineNote, MSGBOX_DEFAULT
	playmoncry SPECIES_AMPHAROS, CRY_MODE_NORMAL
	msgbox OlivineLighthouse_Text_AmphyBreathingLabored, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

OlivineLighthouse_Text_1FSailor:
	.string "People train at this LIGHTHOUSE.\p"
	.string "It's not easy to climb with all\n"
	.string "the trainers waiting inside.$"

OlivineLighthouse_Text_1FPokefanF:
	.string "In the past, POKéMON used to light\n"
	.string "the sea around OLIVINE at night.\p"
	.string "The LIGHTHOUSE was built in honor\n"
	.string "of those noble POKéMON.$"

OlivineLighthouse_Text_SailorHueySeen:
	.string "Men of the sea are always\n"
	.string "spoiling for a good fight!$"

OlivineLighthouse_Text_SailorHueyBeaten:
	.string "Urf!\n"
	.string "I lose!$"

OlivineLighthouse_Text_SailorHueyAfter:
	.string "What power! How would you like\n"
	.string "to sail the seas with me?$"

OlivineLighthouse_Text_GentlemanAlfredSeen:
	.string "Hm? This is no place\n"
	.string "for playing.$"

OlivineLighthouse_Text_GentlemanAlfredBeaten:
	.string "Ah! I can see that you're\n"
	.string "serious.$"

OlivineLighthouse_Text_GentlemanAlfredAfter:
	.string "Up top is a POKéMON that keeps\n"
	.string "the LIGHTHOUSE lit.\p"
	.string "But I hear that it's sick now,\n"
	.string "and can't be cured normally.$"

OlivineLighthouse_Text_BirdKeeperTheoSeen:
	.string "Why are you here? Are you just\n"
	.string "going to gawk? I suggest you leave!$"

OlivineLighthouse_Text_BirdKeeperTheoBeaten:
	.string "You really are concerned about\n"
	.string "the sick POKéMON…$"

OlivineLighthouse_Text_BirdKeeperTheoAfter:
	.string "How the heck do you go up?\p"
	.string "I want to visit the sick POKéMON,\n"
	.string "but I can't get up there…$"

OlivineLighthouse_Text_SailorTerrellSeen:
	.string "Sailors are both kind and strong.\n"
	.string "How about you?$"

OlivineLighthouse_Text_SailorTerrellBeaten:
	.string "You are both kind and strong…$"

OlivineLighthouse_Text_SailorTerrellAfter:
	.string "Every time I return to OLIVINE,\n"
	.string "I visit the GYM.\p"
	.string "The GYM LEADER's POKéMON type\n"
	.string "changed without me noticing.$"

OlivineLighthouse_Text_GentlemanPrestonSeen:
	.string "I travel the world to train my\n"
	.string "POKéMON. I wish to battle you.$"

OlivineLighthouse_Text_GentlemanPrestonBeaten:
	.string "…sigh… I must train some more…$"

OlivineLighthouse_Text_GentlemanPrestonAfter:
	.string "JASMINE used to use ROCK-type\n"
	.string "POKéMON like ONIX.$"

OlivineLighthouse_Text_SailorKentSeen:
	.string "JASMINE must be worried sick about\n"
	.string "the POKéMON here.\p"
	.string "She won't even smile these days.$"

OlivineLighthouse_Text_SailorKentBeaten:
	.string "I can't manage a smile either…$"

OlivineLighthouse_Text_SailorKentAfter:
	.string "Speaking of sick, I've heard there's\n"
	.string "a good PHARMACY in CIANWOOD.$"

OlivineLighthouse_Text_LassConnieSeen:
	.string "JASMINE is this city's GYM LEADER.\p"
	.string "I mean to bring her back with me.\p"
	.string "Nobody had better get in my way!$"

OlivineLighthouse_Text_LassConnieBeaten:
	.string "Aaack! My POKéMON!$"

OlivineLighthouse_Text_LassConnieAfter:
	.string "Right. Anybody would be worried if\n"
	.string "his or her own POKéMON were hurt.\p"
	.string "I'll pray for the POKéMON here, so\n"
	.string "JASMINE can come back to the GYM.$"

OlivineLighthouse_Text_SailorErnestSeen:
	.string "I wanted to battle JASMINE, but she's\n"
	.string "not up to it now.\p"
	.string "So, how about you?$"

OlivineLighthouse_Text_SailorErnestBeaten:
	.string "Whoa, whoa. You're overwhelming!$"

OlivineLighthouse_Text_SailorErnestAfter:
	.string "A GYM LEADER isn't just about being\n"
	.string "strong.\p"
	.string "A LEADER also needs to be\n"
	.string "compassionate.$"

OlivineLighthouse_Text_BirdKeeperDenisSeen:
	.string "We're pretty high up here. My bird\n"
	.string "POKéMON are in prime form.$"

OlivineLighthouse_Text_BirdKeeperDenisBeaten:
	.string "Oops… They crashed…$"

OlivineLighthouse_Text_BirdKeeperDenisAfter:
	.string "My POKéMON learned how to use FLY in\n"
	.string "CIANWOOD.\p"
	.string "Well, since I'm a loser, I'll FLY\n"
	.string "across the sea…$"

OlivineLighthouse_Text_JasmineNote:
	.string "AMPHY lies curled up at the top of\n"
	.string "the LIGHTHOUSE, breathing hard.\p"
	.string "Beside it is a note in JASMINE's\n"
	.string "handwriting:\p"
	.string "“…This POKéMON always kept the\n"
	.string "sea lit at night. But it suddenly\l"
	.string "got sick… It's gasping for air…\p"
	.string "…I understand there is a wonderful\n"
	.string "PHARMACY in CIANWOOD, across the\l"
	.string "sea… but I can't leave AMPHY\l"
	.string "unattended…”$"

OlivineLighthouse_Text_AmphyBreathingLabored:
	.string "Its breathing is terribly\n"
	.string "labored…$"
