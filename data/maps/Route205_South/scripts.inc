Route205_South_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route205_South_OnTransition
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte >>>

@ rotulo da fonte: Route205South_CoordEvent_LittleGirl
@ Uma garota (LOCALID_ROUTE205_SOUTH_LITTLE_GIRL, sprite TWIN) procura o pai
@ perto da usina. Fica visivel depois do primeiro encontro (fonte tambem nao
@ some ela aqui, so no reencontro dentro de ValleyWindworksBuilding, que esta
@ BLOQUEADO por conflito com S2, ver comentario la); ate isso ser resolvido
@ ela so fica de pe na rota, sem quebrar nada.
Route205_South_EventScript_CoordEvent_LittleGirl::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_ROUTE_205_SOUTH_LITTLE_GIRL
	addobject LOCALID_ROUTE205_SOUTH_LITTLE_GIRL
	applymovement LOCALID_ROUTE205_SOUTH_LITTLE_GIRL, Route205_South_Movement_LittleGirlNoticePlayer
	waitmovement 0
	msgbox Route205_South_Text_HelpIWantToSeeMyPapa, MSGBOX_DEFAULT
	setvar VAR_SINNOH_WINDWORKS_ESTADO, 1
	releaseall
	end

Route205_South_EventScript_LittleGirlTalk::
	msgbox Route205_South_Text_IWantToSeeMyPapa, MSGBOX_NPC
	end

Route205_South_Movement_LittleGirlNoticePlayer:
	emote_exclamation_mark
	step_end

Route205_South_Text_HelpIWantToSeeMyPapa:
	.string "Help! I can't find my papa\n"
	.string "anywhere!\p"
	.string "He was headed for the Valley\n"
	.string "Windworks, but some scary people\l"
	.string "in uniforms won't let anyone in.$"

Route205_South_Text_IWantToSeeMyPapa:
	.string "I just want to see my papa\n"
	.string "again…$"

@ rotulo da fonte: Route205South_CoordEvent_Grunts
@ Reforco do aviso antes de chegar nos grunts de verdade (LOCALID_ROUTE205_
@ SOUTH_GRUNT_EAST/WEST, ja plantados pelo S2 com FLAG_GALACTICA_WINDWORKS).
@ Nao cria bloqueio novo, so avisa uma vez; setvar evita repetir.
Route205_South_EventScript_CoordEvent_Grunts::
	lockall
	msgbox Route205_South_Text_Grunt, MSGBOX_DEFAULT
	setvar VAR_SINNOH_WINDWORKS_ESTADO, 2
	releaseall
	end

@ NPC mudo com hidden_flag na fonte (LOCALID_YOUNGSTER, FLAG_HIDE_ROUTE_205_
@ SOUTH_YOUNGSTER): so aparecia depois da MARS cair, dentro de
@ ValleyWindworksBuilding (bloqueado, ver comentario la). Nasce escondido
@ (new_game.inc) e fica assim ate o bloqueio se resolver; sem isso ele nunca
@ atrapalha o mapa.
Route205_South_EventScript_HiddenYoungsterTalk::
	msgbox Route205_South_Text_SlatherHoneyOnATree, MSGBOX_NPC
	end

Route205_South_Text_SlatherHoneyOnATree:
	.string "If you slather sweet Honey on a\n"
	.string "sweet-smelling tree…\p"
	.string "Pokémon may be attracted by that\n"
	.string "sweet scent.$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

@ ponytail: a cena e a flag sao a mesma coisa. Os dois grunts que bloqueiam o
@ caminho (LOCALID_GRUNT_M_EAST/WEST na fonte, hidden_flag
@ FLAG_HIDE_ROUTE_205_SOUTH_GRUNTS) nascem enquanto a Mars nao caiu na usina, e
@ somem depois; mesma FLAG_GALACTICA_WINDWORKS que a Valley Windworks ja usa,
@ porque e o mesmo marco (a rota liga a Floaroma com a usina). Zero var.
Route205_South_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_MARS_VALLEY_WINDWORKS, Route205_South_EventScript_HideGalactica_windworks
	end

Route205_South_EventScript_HideGalactica_windworks::
	setflag FLAG_GALACTICA_WINDWORKS
	return

@ Os dois grunts mudos de pret/pokeplatinum. Fonte usa o MESMO indice de script
@ para os dois (idx4): dizem a linha identica.
Route205_South_EventScript_Grunt::
	msgbox Route205_South_Text_Grunt, MSGBOX_NPC
	end

Route205_South_Text_Grunt:
	.string "We, Team Galactic, are conducting\n"
	.string "research in the Eterna Forest!\p"
	.string "This is as far as you will go!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route205_South_EventScript_Placa1::
	msgbox Route205_South_Text_Placa1, MSGBOX_SIGN
	end

Route205_South_Text_Placa1:
	.string "Rt. 205\nFloaroma Town$"

Route205_South_EventScript_Placa2::
	msgbox Route205_South_Text_Placa2, MSGBOX_SIGN
	end

Route205_South_Text_Placa2:
	.string "Rt. 205\nEterna Forest$"

Route205_South_EventScript_Placa3::
	msgbox Route205_South_Text_Placa3, MSGBOX_SIGN
	end

Route205_South_Text_Placa3:
	.string "Trainer Tips!\pThe items placed in your Bag are\nautomatically sorted to the\pappropriate pockets.\pIt's very convenient!\nIt's a Trainer's best friend!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route205_South_EventScript_Npc1::
	msgbox Route205_South_Text_Npc1, MSGBOX_NPC
	end

Route205_South_Text_Npc1:
	.string "Many Poison-type Pokémon make the\nEterna Forest their home.\pBut I didn't buy any Antidotes.\nWhat should I do?\pDo I press on, or do I go back?$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route205_South_EventScript_HikerDaniel::
	trainerbattle_single TRAINER_SINNOH_HIKER_DANIEL, Route205_South_Text_HikerDanielIntro, Route205_South_Text_HikerDanielDefeat
	msgbox Route205_South_Text_HikerDanielPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_HikerDanielIntro:
	.string "There's no mountain here, but I'm\ndressed to hike! Gahaha! Here goes!$"

Route205_South_Text_HikerDanielDefeat:
	.string "Oh, yeah!\nA refreshing battle that was!$"

Route205_South_Text_HikerDanielPost:
	.string "You can find the same kinds of\nPokémon in all sorts of places.\pThere's no law saying a Hiker can't\ngo searching off in the mountains!$"

Route205_South_EventScript_AromaLadyElizabeth::
	trainerbattle_single TRAINER_SINNOH_AROMA_LADY_ELIZABETH, Route205_South_Text_AromaLadyElizabethIntro, Route205_South_Text_AromaLadyElizabethDefeat
	msgbox Route205_South_Text_AromaLadyElizabethPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_AromaLadyElizabethIntro:
	.string "I love Pokémon that smell sweet.\nLike this one--get a whiff of this!$"

Route205_South_Text_AromaLadyElizabethDefeat:
	.string "Did you understand what I meant?\nDidn't my Pokémon smell nice?$"

Route205_South_Text_AromaLadyElizabethPost:
	.string "If you plant lots of Berries, you\ncan be surrounded by sweet scents.$"

Route205_South_EventScript_CamperJacob::
	trainerbattle_single TRAINER_SINNOH_CAMPER_JACOB, Route205_South_Text_CamperJacobIntro, Route205_South_Text_CamperJacobDefeat
	msgbox Route205_South_Text_CamperJacobPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_CamperJacobIntro:
	.string "Hey, how about you and me battle before\nI go into Eterna Forest?$"

Route205_South_Text_CamperJacobDefeat:
	.string "That really dampened my spirits.$"

Route205_South_Text_CamperJacobPost:
	.string "I heard that really tough Pokémon\nappear in Eterna Forest.\pI need to be more prepared than this!$"

Route205_South_EventScript_PicnickerSiena::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_SIENA, Route205_South_Text_PicnickerSienaIntro, Route205_South_Text_PicnickerSienaDefeat
	msgbox Route205_South_Text_PicnickerSienaPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_PicnickerSienaIntro:
	.string "What kinds of Pokémon live around\nhere, I wonder?$"

Route205_South_Text_PicnickerSienaDefeat:
	.string "I'm shocked!\nHow did I lose?$"

Route205_South_Text_PicnickerSienaPost:
	.string "I know all sorts of things about\nPokémon!\pLet's see... There are males and\nfemales, and some aren't either!$"

Route205_South_EventScript_HikerNicholas::
	trainerbattle_single TRAINER_SINNOH_HIKER_NICHOLAS, Route205_South_Text_HikerNicholasIntro, Route205_South_Text_HikerNicholasDefeat
	msgbox Route205_South_Text_HikerNicholasPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_HikerNicholasIntro:
	.string "I've lost my way...\nHere of all places...$"

Route205_South_Text_HikerNicholasDefeat:
	.string "Having lost his way, the Trainer lost\nthe battle too...$"

Route205_South_Text_HikerNicholasPost:
	.string "From being lost in the mountains so\nlong, I became a Hiker...$"

Route205_South_EventScript_BattleGirlKelsey::
	trainerbattle_single TRAINER_SINNOH_BATTLE_GIRL_KELSEY, Route205_South_Text_BattleGirlKelseyIntro, Route205_South_Text_BattleGirlKelseyDefeat
	msgbox Route205_South_Text_BattleGirlKelseyPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_BattleGirlKelseyIntro:
	.string "Hiyah!\nThere's no holding anything back!$"

Route205_South_Text_BattleGirlKelseyDefeat:
	.string "I... I concede!\nI think you're on a different level...$"

Route205_South_Text_BattleGirlKelseyPost:
	.string "Hiyah! You put me in my place!\nI appreciate it!$"

Route205_South_EventScript_PicnickerKarina::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_KARINA, Route205_South_Text_PicnickerKarinaIntro, Route205_South_Text_PicnickerKarinaDefeat
	msgbox Route205_South_Text_PicnickerKarinaPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_PicnickerKarinaIntro:
	.string "Oh, I don't know.\nShould I play a little?$"

Route205_South_Text_PicnickerKarinaDefeat:
	.string "Oh, boo!\nHow insulting!$"

Route205_South_Text_PicnickerKarinaPost:
	.string "Listen very closely...\nCan you hear the cries of Pokémon?$"

Route205_South_EventScript_CamperZackary::
	trainerbattle_single TRAINER_SINNOH_CAMPER_ZACKARY, Route205_South_Text_CamperZackaryIntro, Route205_South_Text_CamperZackaryDefeat
	msgbox Route205_South_Text_CamperZackaryPost, MSGBOX_AUTOCLOSE
	end

Route205_South_Text_CamperZackaryIntro:
	.string "It's a long way between Floaroma\nand Eterna City. So, let's battle!$"

Route205_South_Text_CamperZackaryDefeat:
	.string "Wawawaah!\nI'm out of Pokémon that can go!$"

Route205_South_Text_CamperZackaryPost:
	.string "Camping with Pokémon!\nDo you have any idea how fun that is?$"
