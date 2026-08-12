@ VirbankPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_VirbankPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_VirbankPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_VIRBANK
	end

Unova_VirbankPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_VirbankPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_VirbankPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_VirbankPokecenter1F_Loja1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	pokemartlistend

Unova_VirbankPokecenter1F_EventScript_Npc2::
	msgbox Unova_VirbankPokecenter1F_Text_VirbankPokecenterLassText, MSGBOX_NPC
	end

Unova_VirbankPokecenter1F_EventScript_Npc3::
	msgbox Unova_VirbankPokecenter1F_Text_VirbankGymGuyText, MSGBOX_NPC
	end

Unova_VirbankPokecenter1F_EventScript_Npc4::
	msgbox Unova_VirbankPokecenter1F_Text_VirbankPokecenterRoughneckText, MSGBOX_NPC
	end


Unova_VirbankPokecenter1F_Text_VirbankPokecenterLassText::
	.string "Listen! Challenge"
	.string "\npoison type POKé-"
	.string "\lMON with poison"
	.string "\ltype POKéMON!"
	.string "\pAt least that's"
	.string "\nwhat ROXIE told"
	.string "\pme. She plays an"
	.string "\ninstrument! Pretty"
	.string "\lcool!$"

Unova_VirbankPokecenter1F_Text_VirbankGymGuyText::
	.string "The POKéMON GYM"
	.string "\ntrainers here"
	.string "\lkicked me out!"
	.string "\pThey said I was"
	.string "\nruining their"
	.string "\lvibe…"
	.string "\pHere's some ad-"
	.string "\nvice: the GYM"
	.string "\pLEADER uses the"
	.string "\npoison-type."
	.string "\pSo you should"
	.string "\nconfound her with"
	.string "\lpsychic POKéMON."
	.string "\pEarth shaking"
	.string "\nground-type moves"
	.string "\lwork well too.$"

Unova_VirbankPokecenter1F_Text_VirbankPokecenterRoughneckText::
	.string "ROXIE's band!"
	.string "\pIt's getting hard"
	.string "\nto buy tickets to"
	.string "\ptheir shows"
	.string "\nlately! Maybe"
	.string "\pthey'll go on a"
	.string "\nworld tour soon!$"
