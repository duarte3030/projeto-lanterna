@ Ginasio de AZALEA TOWN. As falas e as batalhas vieram de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py e continuam sendo daquele gerador.
@ A ARTE e a PLANTA passaram a ser a do GS Chronicles 2.7.6 (g7m5, 22x38) em
@ 11/09/2026, pelo METODO-COPIA-CIDADES, e por isso os doze gatilhos de
@ coordenada foram reescritos A MAO para a planta nova: rodar o gerador de novo
@ traria de volta saltos para tiles que nao existem mais.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_2. Zero var gasta.

AzaleaTown_Gym_MapScripts::
	.byte 0

@ >>> O quebra-cabeça do ginásio copiado (11/09/2026) >>>
@ Os doze gatilhos de salto que estavam aqui eram do ginásio de 24x60 que a
@ cópia do GS Chronicles substituiu, e apontavam para tiles que não existem
@ mais. O quebra-cabeça abaixo é NOSSO, escrito em cima da planta do autor.
@
@ A planta, medida por busca em largura no blockdata: dois fossos, cada um
@ cruzado por TRÊS fios de teia em x=5, x=11 e x=17, e cada pista desemboca numa
@ varanda ISOLADA das outras duas. Só a pista da esquerda chega no BUGSY. Errar
@ a pista custa a volta até o saguão, e é isso que faz dela um quebra-cabeça e
@ não um corredor.
@
@ O que os gatilhos acrescentam é o escorregão: o fio é teia, então quem pisa na
@ ponta dele desliza os oito tiles do fosso de uma vez. Cada gatilho está na
@ ponta de ENTRADA do fio e o escorregão para UM tile depois da ponta de saída,
@ que nunca é tile de gatilho, então nenhum escorregão dispara outro.
@   sobe:  (x,32) -> (x,24) e (x,18) -> (x,10)
@   desce: (x,25) -> (x,33) e (x,11) -> (x,19)

AzaleaTown_Gym_EventScript_FioSobe::
	lock
	playse SE_M_STRING_SHOT
	applymovement OBJ_EVENT_ID_PLAYER, AzaleaTown_Gym_Movement_FioSobe
	waitmovement 0
	release
	end

AzaleaTown_Gym_EventScript_FioDesce::
	lock
	playse SE_M_STRING_SHOT
	applymovement OBJ_EVENT_ID_PLAYER, AzaleaTown_Gym_Movement_FioDesce
	waitmovement 0
	release
	end

AzaleaTown_Gym_Movement_FioSobe:
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	step_end

AzaleaTown_Gym_Movement_FioDesce:
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	slide_down
	step_end

@ <<< O quebra-cabeça do ginásio copiado <<<

AzaleaTown_Gym_EventScript_Amy::
	trainerbattle_double TRAINER_JOHTO_TWINS_AMY_AND_MAY, AzaleaTown_Gym_Text_AmySeen, AzaleaTown_Gym_Text_AmyBeaten, AzaleaTown_Gym_Text_AmyNotEnoughMons
	msgbox AzaleaTown_Gym_Text_AmyAfter, MSGBOX_AUTOCLOSE
	end

AzaleaTown_Gym_EventScript_May::
	trainerbattle_double TRAINER_JOHTO_TWINS_AMY_AND_MAY, AzaleaTown_Gym_Text_MaySeen, AzaleaTown_Gym_Text_MayBeaten, AzaleaTown_Gym_Text_MayNotEnoughMons
	msgbox AzaleaTown_Gym_Text_MayAfter, MSGBOX_AUTOCLOSE
	end

AzaleaTown_Gym_EventScript_Benny::
	trainerbattle_single TRAINER_JOHTO_BUG_CATCHER_BENNY, AzaleaTown_Gym_Text_BennySeen, AzaleaTown_Gym_Text_BennyBeaten
	msgbox AzaleaTown_Gym_Text_BennyAfter, MSGBOX_AUTOCLOSE
	end

AzaleaTown_Gym_EventScript_Josh::
	trainerbattle_single TRAINER_JOHTO_BUG_CATCHER_JOSH, AzaleaTown_Gym_Text_JoshSeen, AzaleaTown_Gym_Text_JoshBeaten
	msgbox AzaleaTown_Gym_Text_JoshAfter, MSGBOX_AUTOCLOSE
	end

AzaleaTown_Gym_EventScript_Al::
	trainerbattle_single TRAINER_JOHTO_BUG_CATCHER_AL, AzaleaTown_Gym_Text_AlSeen, AzaleaTown_Gym_Text_AlBeaten
	msgbox AzaleaTown_Gym_Text_AlAfter, MSGBOX_AUTOCLOSE
	end

AzaleaTown_Gym_EventScript_Bugsy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_2, AzaleaTown_Gym_EventScript_BugsyDerrotado
	msgbox AzaleaTown_Gym_Text_BugsyIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_BUGSY, AzaleaTown_Gym_Text_BugsyDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox AzaleaTown_Gym_Text_BugsyBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_2
	closemessage
	release
	end

AzaleaTown_Gym_EventScript_BugsyDerrotado::
	msgbox AzaleaTown_Gym_Text_BugsyPost, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_2, AzaleaTown_Gym_EventScript_GuideAfter
	msgbox AzaleaTown_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Gym_EventScript_GuideAfter::
	msgbox AzaleaTown_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

AzaleaTown_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_2, AzaleaTown_Gym_EventScript_StatueCertified
	msgbox AzaleaTown_Gym_Text_Statue, MSGBOX_SIGN
	end

AzaleaTown_Gym_EventScript_StatueCertified::
	msgbox AzaleaTown_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

AzaleaTown_Gym_Text_AmySeen:
	.string "AMY: Hi! Are you challenging\n"
	.string "the LEADER? No way!$"

AzaleaTown_Gym_Text_AmyBeaten:
	.string "AMY & MAY: Oh, double\n"
	.string "goodness!$"

AzaleaTown_Gym_Text_AmyAfter:
	.string "AMY: You're really strong!\p"
	.string "But BUGSY's even stronger!\n"
	.string "His SCYTHER's CUT almost\l"
	.string "always makes critical hits!$"

AzaleaTown_Gym_Text_AmyNotEnoughMons:
	.string "You need two POKéMON to battle\n"
	.string "the two of us!$"

AzaleaTown_Gym_Text_MaySeen:
	.string "MAY: You want to see the\n"
	.string "LEADER? Good luck!\p"
	.string "BUGSY is so strong!\n"
	.string "His SCYTHER's CUT always\l"
	.string "seems to crit!$"

AzaleaTown_Gym_Text_MayBeaten:
	.string "AMY & MAY: Oh, double\n"
	.string "goodness!$"

AzaleaTown_Gym_Text_MayAfter:
	.string "MAY: Our bug POKéMON lost!\n"
	.string "Oh, what a shame.\p"
	.string "BUGSY's won't lose though!\p"
	.string "His PINECO makes short work\n"
	.string "of ROCK-type POKéMON!$"

AzaleaTown_Gym_Text_MayNotEnoughMons:
	.string "You need two POKéMON to battle\n"
	.string "the two of us!$"

AzaleaTown_Gym_Text_BennySeen:
	.string "Bug POKéMON evolve young. So they\n"
	.string "get stronger that much faster.$"

AzaleaTown_Gym_Text_BennyBeaten:
	.string "Just evolving isn't enough!$"

AzaleaTown_Gym_Text_BennyAfter:
	.string "POKéMON become stronger\n"
	.string "if they evolve. Really!$"

AzaleaTown_Gym_Text_JoshSeen:
	.string "You saved all the SLOWPOKE?\n"
	.string "Whew, you're mighty!\p"
	.string "But my grown-up POKéMON are\n"
	.string "pretty tough too!$"

AzaleaTown_Gym_Text_JoshBeaten:
	.string "Urrgggh!$"

AzaleaTown_Gym_Text_JoshAfter:
	.string "I guess I should teach them\n"
	.string "better moves…$"

AzaleaTown_Gym_Text_AlSeen:
	.string "Bug POKéMON are cool and tough!\n"
	.string "I'll prove it to you!$"

AzaleaTown_Gym_Text_AlBeaten:
	.string "You proved how tough you are…$"

AzaleaTown_Gym_Text_AlAfter:
	.string "They're so cool, but most girls\n"
	.string "don't like bug POKéMON.\p"
	.string "I don't know why…$"

AzaleaTown_Gym_Text_BugsyIntro:
	.string "I'm BUGSY!\p"
	.string "I never lose when it comes\n"
	.string "to bug POKéMON.\p"
	.string "My research is going to make me the\n"
	.string "authority on bug POKéMON!\p"
	.string "For example, did you know\n"
	.string "that the move CUT is\l"
	.string "actually a BUG-type move?\p"
	.string "Let me demonstrate all I've\n"
	.string "learned from my studies.$"

AzaleaTown_Gym_Text_BugsyDefeat:
	.string "Whoa, amazing! You're an\n"
	.string "expert on POKéMON!\p"
	.string "My research isn't complete\n"
	.string "yet.\p"
	.string "OK, you win. Take this\n"
	.string "BADGE.$"

AzaleaTown_Gym_Text_BugsyBadge:
	.string "Do you know the benefits\n"
	.string "of HIVEBADGE?\p"
	.string "If you have it, POKéMON up\n"
	.string "to L30 will obey you,\l"
	.string "even traded ones.\p"
	.string "POKéMON that know CUT will be able\n"
	.string "to use it outside of battle too.\p"
	.string "Here, I also want you to\n"
	.string "have this.$"

AzaleaTown_Gym_Text_BugsyPost:
	.string "Bug POKéMON are deep. There are\n"
	.string "many mysteries to be explored.\p"
	.string "Study your favorites thoroughly.$"

AzaleaTown_Gym_Text_GuideBefore:
	.string "Yo, challenger!\p"
	.string "BUGSY's young, but his knowledge\n"
	.string "of bug POKéMON is for real.\p"
	.string "It's going to be tough\n"
	.string "without my advice.\p"
	.string "Let's see… BUGSY's bagworm POKéMON\n"
	.string "knows a move that covers its\l"
	.string "ROCK-type weakness.\p"
	.string "He's also developed a new version\n"
	.string "of CUT that is BUG-type.\p"
	.string "Oh, and don't forget about those\n"
	.string "nasty critical hits! Good luck!$"

AzaleaTown_Gym_Text_GuideAfter:
	.string "Well done! That was a great\n"
	.string "clash of talented young trainers.\p"
	.string "With people like you, the\n"
	.string "future of POKéMON is bright!$"

AzaleaTown_Gym_Text_Statue:
	.string "AZALEA TOWN POKéMON GYM\n"
	.string "Leader: BUGSY$"

AzaleaTown_Gym_Text_StatueCertified:
	.string "AZALEA TOWN POKéMON GYM\p"
	.string "BUGSY'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

@ >>> B6 Johto: Pokémon de enfeite do ginásio (porta_cenas_johto.py) >>>

AzaleaTown_Gym_EventScript_GritoAriados::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ARIADOS, CRY_MODE_NORMAL
	waitmoncry
	release
	end

@ <<< B6 Johto: Pokémon de enfeite do ginásio <<<
