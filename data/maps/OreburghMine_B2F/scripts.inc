OreburghMine_B2F_MapScripts::
	.byte 0

OreburghMine_B2F_EventScript_Miner1::
	msgbox OreburghMine_B2F_Text_Miner1, MSGBOX_NPC
	end

OreburghMine_B2F_EventScript_Miner2::
	msgbox OreburghMine_B2F_Text_Miner2, MSGBOX_NPC
	end

OreburghMine_B2F_Text_Miner1:
	.string "The deeper tunnels wind on forever.\p"
	.string "I still get turned around down\n"
	.string "here.$"

OreburghMine_B2F_Text_Miner2:
	.string "Found a nice vein of ore a while\n"
	.string "back.\p"
	.string "The company's still working through\n"
	.string "it.$"

@ Treinador do pokeplatinum que os dois scripts irmaos nao alcancam
@ (dev_scripts/treinadores_faltantes_sinnoh.py)

OreburghMine_B2F_EventScript_WorkerColin::
	trainerbattle_single TRAINER_SINNOH_WORKER_COLIN, OreburghMine_B2F_Text_WorkerColinIntro, OreburghMine_B2F_Text_WorkerColinDefeat
	msgbox OreburghMine_B2F_Text_WorkerColinPost, MSGBOX_AUTOCLOSE
	end

OreburghMine_B2F_Text_WorkerColinIntro:
	.string "Fine, all righty then.\nJust a quick battle on my break!$"

OreburghMine_B2F_Text_WorkerColinDefeat:
	.string "Wahaha!\nMercy, I cry mercy!$"

OreburghMine_B2F_Text_WorkerColinPost:
	.string "I'd better get on back to work...\pYou know, I'd rather be traveling\naround with Pokémon the way you do.$"

OreburghMine_B2F_EventScript_WorkerMason::
	trainerbattle_single TRAINER_SINNOH_WORKER_MASON, OreburghMine_B2F_Text_WorkerMasonIntro, OreburghMine_B2F_Text_WorkerMasonDefeat
	msgbox OreburghMine_B2F_Text_WorkerMasonPost, MSGBOX_AUTOCLOSE
	end

OreburghMine_B2F_Text_WorkerMasonIntro:
	.string "I'm gonna let you in on a secret...\nI snuck my Pokémon to work!$"

OreburghMine_B2F_Text_WorkerMasonDefeat:
	.string "Well, now aren't you something!$"

OreburghMine_B2F_Text_WorkerMasonPost:
	.string "OK, OK, time for work! I'll work up\na thirst with my Pokémon!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghMine_B2F_EventScript_Npc1::
	msgbox OreburghMine_B2F_Text_Npc1, MSGBOX_NPC
	end

OreburghMine_B2F_Text_Npc1:
	.string "I met these MACHOP on Route 207.\pThey've now become my most trusted\npartners!$"

OreburghMine_B2F_EventScript_Npc2::
	msgbox OreburghMine_B2F_Text_Npc2, MSGBOX_NPC
	end

OreburghMine_B2F_Text_Npc2:
	.string "MACHOP: Maaacho!$"

OreburghMine_B2F_EventScript_Npc3::
	msgbox OreburghMine_B2F_Text_Npc3, MSGBOX_NPC
	end

OreburghMine_B2F_Text_Npc3:
	.string "MACHOP: Chopmacho!$"
