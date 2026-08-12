@ AspertiaGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5): a EMBOSCADA, que e o quebra-cabeca do ginasio.
@
@ Medido antes: o ginasio tinha o CHEREN e mais nada. Os dois treinadores de
@ dentro estavam la como objeto, mas so com o texto de DEPOIS da batalha, e a
@ batalha nunca acontecia. O ponto cego do B4: no BW3G esses dois nao sao
@ OBJECTTYPE_TRAINER, sao OBJECTTYPE_SCRIPT com o `loadtrainer` dentro de um
@ script chamado por `coord_event`, entao a varredura de treinador passou por
@ cima deles. As constantes nasceram agora (2449 e 2450) e os times vieram de
@ fontes-mapas/bw3g/data/trainers/parties.asm.
@
@ Medido na grade de colisao: as linhas 7, 13 e 19 sao parede menos nas colunas
@ 4 e 5. Sao esses trES estrangulamentos que fazem do ginasio um corredor, e e
@ por isso que a fonte poe QUATRO coord_events (4,17), (5,17), (4,11) e (5,11),
@ dois por treinador: raio de visao de treinador so pega UMA coluna, e o jogador
@ desviaria pela outra. Por isso aqui e coord_event e nao a tecnica 3 do
@ SINNOH-PADRAO.md.
@
@ Custo: ZERO var e ZERO flag. O gatilho e VAR_TEMP_0 com valor 0 (tecnica 1 do
@ SINNOH-PADRAO.md: o motor zera os VAR_TEMP_* a cada entrada de mapa, entao o
@ coord_event dispara sempre), e quem lembra que a batalha ja aconteceu e a flag
@ de treinador derrotado que o proprio motor grava, lida por goto_if_defeated.
@
@ Cortado de proposito (nao muda o jogo): a coreografia de applymovement da
@ fonte, em que o jogador anda dois passos e o treinador se vira. Volta junto com
@ o bloco B6 se alguem quiser.

Unova_AspertiaGym_MapScripts::
	.byte 0

Unova_AspertiaGym_EventScript_EmboscadaYoungster::
	lock
	goto_if_defeated TRAINER_UNOVA_YOUNGSTER_ASPERTIA_GYM, Unova_AspertiaGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_ASPERTIA_GYM, Unova_AspertiaGym_Text_YoungsterSeen, Unova_AspertiaGym_Text_YoungsterBeaten
	release
	end

Unova_AspertiaGym_EventScript_EmboscadaLass::
	lock
	goto_if_defeated TRAINER_UNOVA_LASS_ASPERTIA_GYM, Unova_AspertiaGym_EventScript_EmboscadaFim
	trainerbattle_single TRAINER_UNOVA_LASS_ASPERTIA_GYM, Unova_AspertiaGym_Text_LassSeen, Unova_AspertiaGym_Text_LassBeaten
	release
	end

Unova_AspertiaGym_EventScript_EmboscadaFim::
	release
	end

Unova_AspertiaGym_Text_YoungsterSeen::
	.string "CHEREN saw"
	.string "\npotential in me"
	.string "\pand made me a"
	.string "\ntrainer in this"
	.string "\lGYM!$"

Unova_AspertiaGym_Text_YoungsterBeaten::
	.string "You're strong. Or"
	.string "\nshould I say your"
	.string "\pPOKéMON are"
	.string "\nstrong?$"

Unova_AspertiaGym_Text_LassSeen::
	.string "Now I'll show you"
	.string "\nall of the things"
	.string "\pI learned from"
	.string "\nCHEREN!$"

Unova_AspertiaGym_Text_LassBeaten::
	.string "For knowledge to"
	.string "\nbecome your own,"
	.string "\pyou need to test"
	.string "\nit out yourself.$"

Unova_AspertiaGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_CHEREN, Unova_AspertiaGym_Text_CherenGymIntroText, Unova_AspertiaGym_Text_CherenWinLossText, Unova_AspertiaGym_EventScript_Insignia0
	end

Unova_AspertiaGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_ASPERTIA
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_AspertiaGym_EventScript_Npc1::
	msgbox Unova_AspertiaGym_Text_AspertiaGymGuyText, MSGBOX_NPC
	end

Unova_AspertiaGym_EventScript_Npc2::
	msgbox Unova_AspertiaGym_Text_YoungsterAspertiaGymAfterText, MSGBOX_NPC
	end

Unova_AspertiaGym_EventScript_Npc3::
	msgbox Unova_AspertiaGym_Text_LassAspertiaGymAfterText, MSGBOX_NPC
	end


Unova_AspertiaGym_Text_CherenGymIntroText::
	.string "{PLAYER}! Welcome"
	.string "\nto ASPERTIA CITY"
	.string "\lPOKéMON GYM."
	.string "\pI'm grateful for"
	.string "\nyour help before,"
	.string "\pbut this is"
	.string "\ndifferent."
	.string "\pHere, I accept"
	.string "\nyour challenge as"
	.string "\pthe ASPERTIA CITY"
	.string "\nGYM LEADER."
	.string "\pLet's both do our"
	.string "\nbest and have a"
	.string "\pbattle we can be"
	.string "\nproud of.$"

Unova_AspertiaGym_Text_CherenWinLossText::
	.string "This! This is what"
	.string "\na real POKéMON"
	.string "\lbattle is!$"

Unova_AspertiaGym_Text_AspertiaGymGuyText::
	.string "Yo, challenger!"
	.string "\pCHEREN is the"
	.string "\nleader of this"
	.string "\lGYM. He teaches"
	.string "\pstudents how to"
	.string "\ntrain POKéMON."
	.string "\pHe's going to be"
	.string "\ntough without my"
	.string "\ladvice."
	.string "\pLet's see…"
	.string "\nCHEREN's POKéMON"
	.string "\pare all normal"
	.string "\ntype. Their only"
	.string "\pweakness is the"
	.string "\nfighting type.$"

Unova_AspertiaGym_Text_YoungsterAspertiaGymAfterText::
	.string "The reason he saw"
	.string "\npotential in me"
	.string "\pwas that there was"
	.string "\nno one else?"
	.string "\pNo way! Even if"
	.string "\nthat's true, I"
	.string "\pjust have to get"
	.string "\nstronger!$"

Unova_AspertiaGym_Text_LassAspertiaGymAfterText::
	.string "I have to learn"
	.string "\neven more about"
	.string "\lmy POKéMON!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_AspertiaGym_EventScript_EstatuaGinasio::
	msgbox Unova_AspertiaGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_AspertiaGym_Text_EstatuaGinasio::
	.string "ASPERTIA CITY\n"
	.string "POKéMON GYM$"
