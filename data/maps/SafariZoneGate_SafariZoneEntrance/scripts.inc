SafariZoneGate_SafariZoneEntrance_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route121_SafariZoneGate_SafariZoneEntrance_EventScript_WelcomeAttendant::
	msgbox Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeToSafariZone, MSGBOX_NPC
	end

Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeToSafariZone::
	.string "Welcome to the SAFARI ZONE!\p"
	.string "Here, you may witness many kinds of\n"
	.string "POKéMON rarely seen in JOHTO.\p"
	.string "And, you'll see them in their wild,\n"
	.string "untamed state in natural habitats.\p"
	.string "What's more, we've thrown open the\n"
	.string "gates to POKéMON TRAINERS.\p"
	.string "You're encouraged to catch POKéMON\n"
	.string "for keeps!\p"
	.string "Come in and enjoy the SAFARI ZONE!$"

Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeFirstTime::
	.string "Welcome to the SAFARI ZONE!\n"
	.string "Is it your first time here?$"

SafariZoneGate_SafariZoneEntrance_EventScript_InfoAttendantFala::
	msgbox Route121_SafariZoneGate_SafariZoneEntrance_Text_WelcomeFirstTime, MSGBOX_NPC
	end

SafariZoneGate_SafariZoneEntrance_EventScript_Boy::
	lock
	faceplayer
	msgbox SafariZoneGate_SafariZoneEntrance_Text_Boy, MSGBOX_DEFAULT
	closemessage
	release
	end

SafariZoneGate_SafariZoneEntrance_Text_Boy::
	.string "I heard the new zone they\n"
	.string "are working on has dragons!$"
