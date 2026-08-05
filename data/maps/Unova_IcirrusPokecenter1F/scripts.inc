@ IcirrusPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_IcirrusPokecenter1F_MapScripts::
	.byte 0

Unova_IcirrusPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_IcirrusPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_IcirrusPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_IcirrusPokecenter1F_Loja1:
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

Unova_IcirrusPokecenter1F_EventScript_Npc2::
	msgbox Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterGentlemanText, MSGBOX_NPC
	end

Unova_IcirrusPokecenter1F_EventScript_Npc3::
	msgbox Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterTwinText, MSGBOX_NPC
	end

Unova_IcirrusPokecenter1F_EventScript_Npc4::
	msgbox Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterCooltrainerMText, MSGBOX_NPC
	end


Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterGentlemanText::
	.string "The tower north of"
	.string "\ntown is called"
	.string "\pDRAGONSPIRAL"
	.string "\nTOWER."
	.string "\pA mystical power"
	.string "\nis said to rest at"
	.string "\lthat place.$"

Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterTwinText::
	.string "I went to the"
	.string "\nPOKéMON FAN CLUB,"
	.string "\pbut they said I"
	.string "\nwasn't good enough"
	.string "\lat battling POKé-"
	.string "\lMON."
	.string "\pThose guys are"
	.string "\nso picky!$"

Unova_IcirrusPokecenter1F_Text_IcirrusPokecenterCooltrainerMText::
	.string "You can't buy MAX"
	.string "\nREVIVE, but it"
	.string "\pfully restores a"
	.string "\nfainted POKéMON."
	.string "\pBeware--it won't"
	.string "\nrestore PP, the"
	.string "\pPOWER POINTS"
	.string "\nneeded for moves.$"
