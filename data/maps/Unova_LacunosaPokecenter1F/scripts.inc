@ LacunosaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LacunosaPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_LacunosaPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_LacunosaPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_LACUNOSA
	end

Unova_LacunosaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_LacunosaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_LacunosaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_LacunosaPokecenter1F_Loja1:
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

Unova_LacunosaPokecenter1F_EventScript_Npc2::
	msgbox Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterGameboyKidText, MSGBOX_NPC
	end

Unova_LacunosaPokecenter1F_EventScript_Npc3::
	msgbox Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterGentlemanText, MSGBOX_NPC
	end

Unova_LacunosaPokecenter1F_EventScript_Npc4::
	msgbox Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterYoungsterText, MSGBOX_NPC
	end


Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterGameboyKidText::
	.string "A lady named"
	.string "\nAMANITA made the"
	.string "\pPOKéMON PC storage"
	.string "\nsystem.$"

Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterGentlemanText::
	.string "It was several"
	.string "\nyears ago now."
	.string "\pTEAM PLASMA was up"
	.string "\nto no good with"
	.string "\lPOKéMON."
	.string "\pBut justice pre-"
	.string "\nvailed--a young"
	.string "\lkid broke 'em up."
	.string "\pWait, that's twice"
	.string "\nnow it's happened.$"

Unova_LacunosaPokecenter1F_Text_LacunosaPokecenterYoungsterText::
	.string "Here is a little"
	.string "\nadvice! Keep a lot"
	.string "\pof POTIONs! Keep a"
	.string "\nlot of POKéBALLs"
	.string "\ltoo!$"
