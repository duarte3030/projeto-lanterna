@ MistraltonPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonPokecenter1F_MapScripts::
	.byte 0

Unova_MistraltonPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_MistraltonPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_MistraltonPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_MistraltonPokecenter1F_Loja1:
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

Unova_MistraltonPokecenter1F_EventScript_Npc2::
	msgbox Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterCooltrainerMText, MSGBOX_NPC
	end

Unova_MistraltonPokecenter1F_EventScript_Npc3::
	msgbox Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterCooltrainerFText, MSGBOX_NPC
	end

Unova_MistraltonPokecenter1F_EventScript_Npc4::
	msgbox Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterBugCatcherText, MSGBOX_NPC
	end


Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterCooltrainerMText::
	.string "Where in the world"
	.string "\nis MISTRALTON's"
	.string "\pGYM LEADER? I want"
	.string "\nto challenge her.$"

Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterCooltrainerFText::
	.string "MISTRALTON CITY"
	.string "\nused to be a"
	.string "\pdesolate patch of"
	.string "\nland… This place"
	.string "\pwas built through"
	.string "\nthe cooperation of"
	.string "\lpeople and POKé-"
	.string "\lMON.$"

Unova_MistraltonPokecenter1F_Text_MistraltonPokecenterBugCatcherText::
	.string "My dream is to be-"
	.string "\ncome a GYM LEADER.$"
