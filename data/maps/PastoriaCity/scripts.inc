@ Textos vindos de pret/pokeplatinum (res/text/pastoria_city.json), em ingles.
@ Grunt_M, Rival, Crasher Wake, Croagunk e o Collector/Arrow_Signpost de
@ Route 212 South ficaram de fora: dependem de flag ou de MAP_HEADER
@ condicional, que este agente nao pode inventar.
@ OBJ_EVENT_GFX_PARASOL_LADY e OBJ_EVENT_GFX_BEAUTY nao existem em
@ event_objects.h: trocados por WOMAN_4 e WOMAN_5.

PastoriaCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Os 4 gatilhos de Pastoria formam UMA corrente de historia (RivalBattle ->
@ Bomb -> BlockGreatMarsh, nessa ordem, mais o FaceBoard solto). Bloqueados
@ os 4, motivos anotados um a um; nenhum foi escrito pela metade.
@
@ RivalBattle (var=1): BLOQUEADO. TRAINER_RIVAL_PASTORIA_CITY_TURTWIG /
@ _CHIMCHAR / _PIPLUP nao existem em opponents.h. Fica para o executor de
@ treinadores desta onda.
PastoriaCity_EventScript_CoordEvent_RivalBattle::
	end

@ Bomb (var=4): BLOQUEADO. Cena de clima da Equipe Galactica (explosao,
@ Grunt_M, Crasher Wake, o rival), grande (~15 sub-rotulos na fonte) e
@ precisa de FLAG_PASTORIA_CITY_GRUNT_M_MOVED_EAST, que NAO esta na tabela
@ do plano (nao segue o padrao FLAG_HIDE_*, o censo de hidden_flag nao pega)
@ e nao pode ser inventada aqui. Termina com SetFlag FLAG_HIDE_VEILSTONE_
@ CITY_GALACTIC_WAREHOUSE_LOOKER, flag de OUTRO mapa (Veilstone), e Crasher
@ Wake e o lider do ginasio (presenca de historia, nao bate na regra do
@ time dele, mas o porte inteiro depende da flag interna acima). Volta ao
@ plano antes de escrever.
PastoriaCity_EventScript_CoordEvent_Bomb::
	end

@ BlockGreatMarsh (var=5): BLOQUEADO. So dispara depois do Bomb (var vira 5
@ so no fecho dele), e o objeto LOCALID_RIVAL que a cena move e escondido/
@ mostrado em 3 lugares fora de Pastoria (scripts_valor_lakefront.s,
@ scripts_veilstone_city.s) sem SetFlag em new_game.inc: o estado padrao
@ dele nao fecha sozinho, e escrever agora arriscava plantar objeto com
@ visibilidade errada. Junto com o Bomb quando a corrente inteira for
@ desenhada.
PastoriaCity_EventScript_CoordEvent_BlockGreatMarsh::
	end

@ FaceBoard, Croagunk (var=0): BLOQUEADO. Precisa de FLAG_BLOCK_PASTORIA_
@ CITY_CROAGUNK_EVENT, tambem fora da tabela do plano (nao e FLAG_HIDE_*):
@ acende em scripts_pastoria_city_gym.s (ginasio, ainda que nao seja
@ batalha do lider) e apaga em scripts_valor_lakefront.s (S7). Volta ao
@ plano.
PastoriaCity_EventScript_CoordEvent_FaceBoard::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

PastoriaCity_EventScript_ParasolLady::
	msgbox PastoriaCity_Text_ParasolLady, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer1::
	msgbox PastoriaCity_Text_AceTrainer1, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer2::
	msgbox PastoriaCity_Text_AceTrainer2, MSGBOX_NPC
	end

PastoriaCity_EventScript_GreatMarshSign::
	msgbox PastoriaCity_Text_GreatMarshSign, MSGBOX_SIGN
	end

PastoriaCity_EventScript_GymSign::
	msgbox PastoriaCity_Text_GymSign, MSGBOX_SIGN
	end

PastoriaCity_Text_ParasolLady:
	.string "Someone gave me a Berry, so I\n"
	.string "planted it and grew some more.\p"
	.string "Then I took the Berries and cooked\n"
	.string "them into Poffins. All the work\l"
	.string "is worth it when I see how happy\l"
	.string "they make my POKéMON!$"

PastoriaCity_Text_AceTrainer1:
	.string "PASTORIA POKéMON are tough. The\n"
	.string "marsh air toughens them right up.$"

PastoriaCity_Text_AceTrainer2:
	.string "I've battled all over PASTORIA.\n"
	.string "Care to test your skills with me?$"

PastoriaCity_Text_GreatMarshSign:
	.string "GREAT MARSH$"

PastoriaCity_Text_GymSign:
	.string "PASTORIA CITY POKéMON GYM\p"
	.string "The Water-Type Technique Style!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

PastoriaCity_EventScript_Placa2::
	msgbox PastoriaCity_Text_Placa2, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa2:
	.string "Pastoria City Pokémon Gym\nLeader: Crasher Wake\pThe Torrential Masked Master!$"

PastoriaCity_EventScript_Placa3::
	msgbox PastoriaCity_Text_Placa3, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa3:
	.string "Pastoria Great Marsh\nObservatory Gate$"

PastoriaCity_EventScript_Placa4::
	msgbox PastoriaCity_Text_Placa4, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa4:
	.string "Try the Safari Game in\nPastoria's Great Marsh!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_EventScript_Npc1::
	msgbox PastoriaCity_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Text_Npc1:
	.string "Some Trainers deliberately prevent\ntheir Pokémon from evolving.\pThey wait until the Pokémon levels up\nand learns certain moves.$"

PastoriaCity_EventScript_Npc2::
	msgbox PastoriaCity_Text_Npc2, MSGBOX_NPC
	end

PastoriaCity_Text_Npc2:
	.string "Pastoria's Gym Leader is awesome with\nhis water attacks.\pYou'll know what I mean when you\nchallenge him.$"

PastoriaCity_EventScript_Npc3::
	msgbox PastoriaCity_Text_Npc3, MSGBOX_NPC
	end

PastoriaCity_Text_Npc3:
	.string "CLEFAIRY: Fiiih?!$"

PastoriaCity_EventScript_Npc4::
	msgbox PastoriaCity_Text_Npc4, MSGBOX_NPC
	end

PastoriaCity_Text_Npc4:
	.string "The Great Marsh keeps the weather\ncool in the summertime.\pThis is a good town for Water-type\nPokémon.$"

PastoriaCity_EventScript_Npc5::
	msgbox PastoriaCity_Text_Npc5, MSGBOX_NPC
	end

PastoriaCity_Text_Npc5:
	.string "Here where I am standing, I'm\nsmack-dab in the middle of town.$"

PastoriaCity_EventScript_Npc6::
	msgbox PastoriaCity_Text_Npc6, MSGBOX_NPC
	end

PastoriaCity_Text_Npc6:
	.string "I study rare Pokémon that appear\nonly in the Great Marsh.$"

PastoriaCity_EventScript_Npc7::
	msgbox PastoriaCity_Text_Npc7, MSGBOX_NPC
	end

PastoriaCity_Text_Npc7:
	.string "I'm visiting here to see the Great\nMarsh.\pI'm staying at the lakeside hotel.$"

PastoriaCity_EventScript_Npc8::
	msgbox PastoriaCity_Text_Npc8, MSGBOX_NPC
	end

PastoriaCity_Text_Npc8:
	.string "I can't use the hidden move Surf until\nI beat the local Gym Leader.$"

PastoriaCity_EventScript_Npc9::
	msgbox PastoriaCity_Text_Npc9, MSGBOX_NPC
	end

PastoriaCity_Text_Npc9:
	.string "Have you been to the Pokémon Mansion?\nIt's on Route 212.\pThe owner, Mr. Backlot, likes to brag\nabout his herd of rare Pokémon.$"

PastoriaCity_EventScript_Placa10::
	msgbox PastoriaCity_Text_Placa10, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa10:
	.string "Pastoria City\nThe Marsh City$"
