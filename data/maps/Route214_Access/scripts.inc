Route214_Access_MapScripts::
	.byte 0

Route214_Access_EventScript_Hiker::
	msgbox Route214_Access_Text_Hiker, MSGBOX_NPC
	end

Route214_Access_EventScript_Lass::
	msgbox Route214_Access_Text_Lass, MSGBOX_NPC
	end

Route214_Access_Text_Hiker:
	.string "VEILSTONE CITY's got that big\n"
	.string "meteorite. Worth a look!$"

Route214_Access_Text_Lass:
	.string "This path connects right up to\n"
	.string "VEILSTONE. Handy shortcut.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route214_Access_EventScript_Npc1::
	msgbox Route214_Access_Text_Npc1, MSGBOX_NPC
	end

Route214_Access_Text_Npc1:
	.string "Are you going to take Route 214?\nYou're serious, aren't you?\pIt's too badly chewed up, and\nthere's nothing to see there.\pWell, I guess there is that Ruin\nManiac guy you could check out.\pThat guy's been digging his way\nthrough the bedrock all by himself.$"
