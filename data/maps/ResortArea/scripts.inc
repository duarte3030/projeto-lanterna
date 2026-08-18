@ BLOQUEADO (S7, 18/08/2026), nao escrito: FLAG_SINNOH_ESCONDE_RESORT_AREA_
@ PROF_ROWAN ja tem endereco no censo do S1, mas a fonte (scripts_resort_
@ area.s:20-35) so acende ele (e os outros 4 lideres do mesmo mapa, Roark/
@ Gardenia/Maylene/Byron, nenhum deles no censo) via VAR_RESORT_VILLA_
@ VISITOR/VILLA_VISITOR_*, a mesma maquina de "visitante da Villa" que nao
@ existe aqui (ver o BLOQUEADO equivalente em Villa/scripts.inc). Volta ao
@ plano junto com o de Villa.
ResortArea_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, rotulo ResortArea_CoordEvent_SchoolKidM >>>
@ ponytail: a fonte grava um segmento de TV (SaveTVSegmentHomeAndManorNo
@ Furniture) e sorteia VAR_RESORT_VILLA_VISITOR/VILLA_VISITOR_NONE, nenhum
@ dos dois existe aqui (TV nao existe, maquina de visitante da Villa nao
@ existe, mesmo buraco documentado em Villa/scripts.inc); descartados sem
@ substituto, so o convite + porta + warp pra Villa ficam. Ramifica em 3
@ variantes de Z (472/473/474); aqui a do meio (473, a fonte nem move
@ ninguem nela: jogador e School Kid M ja ficam lado a lado).
@ O warp_event (18,21)->MAP_VILLA ja existe no map.json (a porta comum);
@ aqui so roda a cena antes de usar o MESMO destino via `warp` scriptado.
@ CONSERTO (onda 5): `opendoor`/`closedoor` miravam (18,20), que e a parede
@ ACIMA da porta (a casa da porta e a do warp, (18,21)); a animacao rodava
@ no tile errado. Corrigido para 18, 21 nos dois.
@ CONSERTO (onda 5): `setflag` ANTES do `removeobject`, molde de
@ Route203_EventScript_CoordEvent_Rival. Sem ele o School Kid renascia de pe
@ no Resort na proxima entrada (ele acabou de entrar na Villa) e a
@ FLAG_SINNOH_ESCONDE_RESORT_AREA_SCHOOL_KID_M do `flag` do objeto nunca era
@ escrita por ninguem. DESVIO DA FONTE, dito: scripts_resort_area.s:133 so
@ faz RemoveObject, sem SetFlag; la o School Kid volta a aparecer.
ResortArea_EventScript_CoordEvent_SchoolKidM::
	lockall
	msgbox ResortArea_Text_HaveThisVilla, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ResortArea_EventScript_DeclinedVilla
	msgbox ResortArea_Text_LoadOffMyMind, MSGBOX_DEFAULT
	msgbox ResortArea_Text_StepInside, MSGBOX_DEFAULT
	applymovement LOCALID_RESORT_AREA_SCHOOL_KID_M, ResortArea_Movement_SchoolKidMWalkOnSpotNorth
	waitmovement 0
	opendoor 18, 21
	waitdooranim
	applymovement LOCALID_RESORT_AREA_SCHOOL_KID_M, ResortArea_Movement_SchoolKidMEnterVilla
	applymovement OBJ_EVENT_ID_PLAYER, ResortArea_Movement_PlayerEnterVilla
	waitmovement 0
	closedoor 18, 21
	waitdooranim
	setflag FLAG_SINNOH_ESCONDE_RESORT_AREA_SCHOOL_KID_M
	removeobject LOCALID_RESORT_AREA_SCHOOL_KID_M
	setvar VAR_SINNOH_RESORT_ESTADO, 1
	warp MAP_VILLA, 3, 8
	waitstate
	releaseall
	end

ResortArea_EventScript_DeclinedVilla::
	releaseall
	end

ResortArea_Movement_SchoolKidMWalkOnSpotNorth:
	walk_in_place_up
	step_end

ResortArea_Movement_SchoolKidMEnterVilla:
	walk_up
	set_invisible
	step_end

ResortArea_Movement_PlayerEnterVilla:
	walk_up
	walk_up
	set_invisible
	step_end

ResortArea_Text_HaveThisVilla:
	.string "Psst, hey, traveler! Yes, you!\n"
	.string "I want you to have this Villa!\p"
	.string "Oh, wait, no, no, no!\n"
	.string "It's not what you're thinking!\p"
	.string "This is no scam, see.\n"
	.string "In fact, you'll be doing me a favor!\p"
	.string "See, I was given this Villa. But,\n"
	.string "to be honest, I don't need it,\l"
	.string "either.\p"
	.string "So don't say a word.\n"
	.string "Just nod and this Villa is yours!$"

ResortArea_Text_LoadOffMyMind:
	.string "Whew, that's a load off my mind.\p"
	.string "The original owner was from Hoenn,\n"
	.string "see?\p"
	.string "The owner collected up all the rare\n"
	.string "stones of Sinnoh and went back home.\p"
	.string "I somehow got saddled with this\n"
	.string "place as if it were some gift.\p"
	.string "There's no figuring what rich folks\n"
	.string "will think of next.\p"
	.string "Still, I thank you for helping me\n"
	.string "out. Come with me, will you?$"

ResortArea_Text_StepInside:
	.string "None too shabby, you have to agree.\n"
	.string "Step inside for a look-see.$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

ResortArea_EventScript_CoolTrainerF::
	lock
	faceplayer
	msgbox ResortArea_Text_CoolTrainerF, MSGBOX_DEFAULT
	release
	end

ResortArea_EventScript_MapSign::
	msgbox ResortArea_Text_MapSign, MSGBOX_SIGN
	end

ResortArea_EventScript_VillaSign::
	msgbox ResortArea_Text_VillaSign, MSGBOX_SIGN
	end

ResortArea_Text_CoolTrainerF:
	.string "Oh, how I long to become a member\n"
	.string "of the Ribbon Syndicate. My dearest\p"
	.string "Pokémon will be treated to dreamy\n"
	.string "experiences!$"

ResortArea_Text_MapSign:
	.string "RESORT AREA\n"
	.string "Where Pokémon Rest in Style$"

ResortArea_Text_VillaSign:
	.string "VILLA\n"
	.string "A getaway for trainers and their\n"
	.string "Pokémon.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

ResortArea_EventScript_Placa2::
	msgbox ResortArea_Text_Placa2, MSGBOX_SIGN
	end

ResortArea_Text_Placa2:
	.string "The Ribbon Syndicate\nMembers Only$"

ResortArea_EventScript_Placa3::
	msgbox ResortArea_Text_Placa3, MSGBOX_SIGN
	end

ResortArea_Text_Placa3:
	.string "A Somewhat Impressive Villa$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ResortArea_EventScript_Npc1::
	msgbox ResortArea_Text_Npc1, MSGBOX_NPC
	end

ResortArea_Text_Npc1:
	.string "I've traveled a long way to make my\nbeloved Pokémon even more beautiful.\pThat will make it love me even more.\nGiggle!$"

ResortArea_EventScript_Npc2::
	msgbox ResortArea_Text_Npc2, MSGBOX_NPC
	end

ResortArea_Text_Npc2:
	.string "Nothing is too good for my Pokémon.\nThere's no mountain too high to climb.\pThat's how I look at it.$"

ResortArea_EventScript_Npc3::
	msgbox ResortArea_Text_Npc3, MSGBOX_NPC
	end

ResortArea_Text_Npc3:
	.string "You know how you can dig up cool\nstuff in the Underground?\pPeople are saying they're digging up\nnew, different stuff.$"

ResortArea_EventScript_Npc4::
	msgbox ResortArea_Text_Npc4, MSGBOX_NPC
	end

ResortArea_Text_Npc4:
	.string "Nobody believes me, but something\nlurks in the Resort Area.\pIt's the hidden ruler of the area!\nYou have to believe me!\pIf you believe me, whip out your\nSuper Rod and go fishing.\pWho knows, you may just catch the\nmind-blowing ruler!$"

ResortArea_EventScript_Placa5::
	msgbox ResortArea_Text_Placa5, MSGBOX_SIGN
	end

ResortArea_Text_Placa5:
	.string "Resort Area\nRelax & Play!$"
