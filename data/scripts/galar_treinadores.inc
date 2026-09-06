@ Treinadores de Galar, balde d da fase de conteudo.
@ Gerado por dev_scripts/treinadores_galar.py; NAO editar a mao.
@ Uma batalha por objeto: a PRIMEIRA de um percurso linear.
@
@ O RABO DE TODO BLOCO E `msgbox ..., MSGBOX_AUTOCLOSE` + `release` +
@ `end`, e ele NAO e enfeite: e por ali que volta quem ganhou a batalha
@ (`gotopostbattlescript` cai na linha seguinte ao `trainerbattle`) e
@ tambem quem RE-FALA com um treinador ja vencido. Sem ele o objeto do
@ JOGADOR fica congelado pelo `lock` que o proprio molde poe, porque so
@ `ScrCmd_release` chama `UnfreezeObjectEvents`; o `end` sozinho apenas
@ solta `sLockFieldControls`. Era esta a trava dos 127 blocos de 23/08.

@ ---- fala padrao por classe (ver TEXTO_CLASSE no gerador) ----
GalarTrn_Intro_AROMA_LADY_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_AROMA_LADY_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_BEAUTY_FRLG:
	.string "You have style.\n"
	.string "But I have a team.$"

GalarTrn_Depois_BEAUTY_FRLG:
	.string "I lost with elegance.$"

GalarTrn_Intro_BIKER_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_BIKER_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_BLACK_BELT_FRLG:
	.string "Força e treino!\nEncare-me!$"

GalarTrn_Depois_BLACK_BELT_FRLG:
	.string "You trained more.$"

GalarTrn_Intro_BOSS_FRLG:
	.string "Nobody gets past me.$"

GalarTrn_Depois_BOSS_FRLG:
	.string "This isn't going to end like this.$"

GalarTrn_Intro_BUG_CATCHER_FRLG:
	.string "I caught a lot of bugs today.\n"
	.string "Want to see?$"

GalarTrn_Depois_BUG_CATCHER_FRLG:
	.string "My bugs are worn out.$"

GalarTrn_Intro_BUG_MANIAC:
	.string "How about a quick battle?$"

GalarTrn_Depois_BUG_MANIAC:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_BURGLAR_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_BURGLAR_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_CAMPER_FRLG:
	.string "I camped out here just to find a good\n"
	.string "match.$"

GalarTrn_Depois_CAMPER_FRLG:
	.string "Thanks for the battle!$"

GalarTrn_Intro_CHAMPION_FRLG:
	.string "The top of Galar is right here.\n"
	.string "Come and get me!$"

GalarTrn_Depois_CHAMPION_FRLG:
	.string "You've reached the top.$"

GalarTrn_Intro_CHANNELER_FRLG:
	.string "I've seen your future...\n"
	.string "and it is a battle.$"

GalarTrn_Depois_CHANNELER_FRLG:
	.string "O futuro me enganou.$"

GalarTrn_Intro_COLLECTOR:
	.string "How about a quick battle?$"

GalarTrn_Depois_COLLECTOR:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_COOLTRAINER_FRLG:
	.string "A real match,\n"
	.string "how about it?$"

GalarTrn_Depois_COOLTRAINER_FRLG:
	.string "That was a good match.$"

GalarTrn_Intro_COOL_COUPLE_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_COOL_COUPLE_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_CRUSH_GIRL_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_CRUSH_GIRL_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_ELITE_FOUR_FRLG:
	.string "The road narrows here.\n"
	.string "Show me your team!$"

GalarTrn_Depois_ELITE_FOUR_FRLG:
	.string "Move along,\n"
	.string "Trainer.$"

GalarTrn_Intro_FISHERMAN_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_FISHERMAN_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_GENTLEMAN_FRLG:
	.string "Excuse me. Care for a battle?$"

GalarTrn_Depois_GENTLEMAN_FRLG:
	.string "It was a pleasure.$"

GalarTrn_Intro_GUITARIST:
	.string "High five! I mean,\n"
	.string "battle me!$"

GalarTrn_Depois_GUITARIST:
	.string "You were better tuned.$"

GalarTrn_Intro_HIKER_FRLG:
	.string "I climbed this whole trail!\n"
	.string "Shall we battle?$"

GalarTrn_Depois_HIKER_FRLG:
	.string "What stamina you have!$"

GalarTrn_Intro_INTERVIEWER:
	.string "How about a quick battle?$"

GalarTrn_Depois_INTERVIEWER:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_JUGGLER_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_JUGGLER_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_KINDLER:
	.string "How about a quick battle?$"

GalarTrn_Depois_KINDLER:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_LADY_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_LADY_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_LASS_FRLG:
	.string "Hi! Want to battle me?$"

GalarTrn_Depois_LASS_FRLG:
	.string "You really are strong!$"

GalarTrn_Intro_LEADER_FRLG:
	.string "I'm the leader here.\n"
	.string "Show me what you're worth!$"

GalarTrn_Depois_LEADER_FRLG:
	.string "You battled very well.$"

GalarTrn_Intro_MAGMA_ADMIN:
	.string "Restricted area.\n"
	.string "Go back the way you came.$"

GalarTrn_Depois_MAGMA_ADMIN:
	.string "My turn ended badly.$"

GalarTrn_Intro_PICNICKER_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_PICNICKER_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_PKMN_RANGER_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_PKMN_RANGER_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_PSYCHIC_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_PSYCHIC_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_RIVAL:
	.string "You again? Then let's settle this!$"

GalarTrn_Depois_RIVAL:
	.string "Next time I'll win!$"

GalarTrn_Intro_SAILOR_FRLG:
	.string "A sailor never turns down a good scrap!$"

GalarTrn_Depois_SAILOR_FRLG:
	.string "I'm anchored for good.$"

GalarTrn_Intro_SCHOOL_KID:
	.string "How about a quick battle?$"

GalarTrn_Depois_SCHOOL_KID:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_SCIENTIST_FRLG:
	.string "My hypothesis:\n"
	.string "I win. Let's see.$"

GalarTrn_Depois_SCIENTIST_FRLG:
	.string "Hypothesis refuted.$"

GalarTrn_Intro_SUPER_NERD_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_SUPER_NERD_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_SWIMMER_M_FRLG:
	.string "The water is my home.\n"
	.string "Let's go!$"

GalarTrn_Depois_SWIMMER_M_FRLG:
	.string "Nice, you swim well.$"

GalarTrn_Intro_TAMER_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_TAMER_FRLG:
	.string "Good battle. Thank you!$"

GalarTrn_Intro_TEAM_AQUA:
	.string "Get lost, kid!$"

GalarTrn_Depois_TEAM_AQUA:
	.string "All right, all right... I'm going.$"

GalarTrn_Intro_YOUNGSTER_FRLG:
	.string "My team is new, but it's good. Come on!$"

GalarTrn_Depois_YOUNGSTER_FRLG:
	.string "I need to train more.$"

GalarTrn_Intro_YOUNG_COUPLE_FRLG:
	.string "How about a quick battle?$"

GalarTrn_Depois_YOUNG_COUPLE_FRLG:
	.string "Good battle. Thank you!$"

@ ---- Galar_Ballonlea06 ----
GalarTrn_G11M11_o11::
	trainerbattle_single TRAINER_GALAR_BEDE_312, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G11M11_o11_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G11M11_o11_Derrota:
	.string "Why did I have the misfortune of being\n"
	.string "born at the same time as you?$"

GalarTrn_G11M11_o12::
	trainerbattle_single TRAINER_GALAR_OPAL_418, GalarTrn_G11M11_o12_Intro, GalarTrn_G11M11_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G11M11_o12_Intro:
	.string "Opal: I suppose it's a little late to\n"
	.string "introduce myself, but... I'm Opal, the\l"
	.string "Gym Leader. I had a good look at how you\l"
	.string "handled those tests. The last part of\l"
	.string "the mission is me... Let me see how you\l"
	.string "and your partner Pokémon carry\l"
	.string "yourselves!$"

GalarTrn_G11M11_o12_Derrota:
	.string "You're still lacking pink, but you're an\n"
	.string "excellent Trainer with some good\l"
	.string "Pokémon.$"

@ ---- Galar_Circhester03 ----
GalarTrn_G12M00_bg10::
	lock
	goto_if_defeated TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg10_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg10_Derrota
GalarTrn_G12M00_bg10_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg10_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_bg11::
	lock
	goto_if_defeated TRAINER_GALAR_KARLA_215_2, GalarTrn_G12M00_bg11_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_KARLA_215_2, GalarTrn_G12M00_bg11_Derrota
GalarTrn_G12M00_bg11_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg11_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_bg12::
	lock
	goto_if_defeated TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg12_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg12_Derrota
GalarTrn_G12M00_bg12_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg12_Derrota:
	.string "Oh!$"

GalarTrn_G12M00_bg13::
	lock
	goto_if_defeated TRAINER_GALAR_LANA_180_2, GalarTrn_G12M00_bg13_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_LANA_180_2, GalarTrn_G12M00_bg13_Derrota
GalarTrn_G12M00_bg13_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg13_Derrota:
	.string "Oh!$"

GalarTrn_G12M00_bg2::
	lock
	goto_if_defeated TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg2_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg2_Derrota
GalarTrn_G12M00_bg2_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg2_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_bg3::
	lock
	goto_if_defeated TRAINER_GALAR_TALIA_213_2, GalarTrn_G12M00_bg3_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_TALIA_213_2, GalarTrn_G12M00_bg3_Derrota
GalarTrn_G12M00_bg3_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg3_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_bg4::
	lock
	goto_if_defeated TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg4_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg4_Derrota
GalarTrn_G12M00_bg4_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg4_Derrota:
	.string "$"

GalarTrn_G12M00_bg5::
	lock
	goto_if_defeated TRAINER_GALAR_AVA_178_2, GalarTrn_G12M00_bg5_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_AVA_178_2, GalarTrn_G12M00_bg5_Derrota
GalarTrn_G12M00_bg5_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg5_Derrota:
	.string "$"

GalarTrn_G12M00_bg6::
	lock
	goto_if_defeated TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg6_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg6_Derrota
GalarTrn_G12M00_bg6_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg6_Derrota:
	.string "Too hot!$"

GalarTrn_G12M00_bg7::
	lock
	goto_if_defeated TRAINER_GALAR_CLOTILDE_214_2, GalarTrn_G12M00_bg7_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_CLOTILDE_214_2, GalarTrn_G12M00_bg7_Derrota
GalarTrn_G12M00_bg7_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg7_Derrota:
	.string "Too hot!$"

GalarTrn_G12M00_bg8::
	lock
	goto_if_defeated TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg8_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg8_Derrota
GalarTrn_G12M00_bg8_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg8_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_bg9::
	lock
	goto_if_defeated TRAINER_GALAR_DELIA_179_2, GalarTrn_G12M00_bg9_Fim
	msgbox GalarTrn_Intro_BEAUTY_FRLG, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_NONE
	trainerbattle_no_intro TRAINER_GALAR_DELIA_179_2, GalarTrn_G12M00_bg9_Derrota
GalarTrn_G12M00_bg9_Fim:
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_bg9_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_o0::
	trainerbattle_single TRAINER_GALAR_TALIA_213_3, GalarTrn_G12M00_o0_Intro, GalarTrn_G12M00_o0_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o0_Intro:
	.string "Wrong answer, youngster.$"

GalarTrn_G12M00_o0_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_o1::
	trainerbattle_single TRAINER_GALAR_ERIKA_177, GalarTrn_G12M00_o1_Intro, GalarTrn_G12M00_o1_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o1_Intro:
	.string "Do you know how Fairy Pokémon manage\n"
	.string "to beat Dragons?$"

GalarTrn_G12M00_o1_Derrota:
	.string "Wow!\n"
	.string "Hot hot hot!$"

GalarTrn_G12M00_o2::
	trainerbattle_single TRAINER_GALAR_AVA_178_3, GalarTrn_G12M00_o2_Intro, GalarTrn_G12M00_o2_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o2_Intro:
	.string "I think I know where the power of\n"
	.string "Fairy-types comes from!$"

GalarTrn_G12M00_o2_Derrota:
	.string "Wow!\n"
	.string "My studies weren't enough!$"

GalarTrn_G12M00_o3::
	trainerbattle_single TRAINER_GALAR_CLOTILDE_214_3, GalarTrn_G12M00_o3_Intro, GalarTrn_G12M00_o3_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o3_Intro:
	.string "I was told wrong. I thought Opal was a\n"
	.string "Ghost-type Trainer.\p"
	.string "Good thing I have a Fairy-type here.$"

GalarTrn_G12M00_o3_Derrota:
	.string "Too hot!$"

GalarTrn_G12M00_o4::
	trainerbattle_single TRAINER_GALAR_DELIA_179_3, GalarTrn_G12M00_o4_Intro, GalarTrn_G12M00_o4_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o4_Intro:
	.string "Let's dance!$"

GalarTrn_G12M00_o4_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_o5::
	trainerbattle_single TRAINER_GALAR_KARLA_215_3, GalarTrn_G12M00_o5_Intro, GalarTrn_G12M00_o5_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o5_Intro:
	.string "Do you like Fairy-types?$"

GalarTrn_G12M00_o5_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_o6::
	trainerbattle_single TRAINER_GALAR_LANA_180_3, GalarTrn_G12M00_o6_Intro, GalarTrn_G12M00_o6_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M00_o6_Intro:
	.string "I know you'll want to be one of us…$"

GalarTrn_G12M00_o6_Derrota:
	.string "Oh!$"

@ ---- Galar_Circhester06 ----
GalarTrn_G12M10_o19::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_435, GalarTrn_G12M10_o19_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_435, 0, GalarTrn_G12M10_o19_Derrota, GalarTrn_G12M10_o19_Vitoria
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M10_o19_Fim:
	release
	end

GalarTrn_G12M10_o19_Derrota:
	.string "let's go$"

GalarTrn_G12M10_o19_Vitoria:
	.string "I still can't beat you, my true rival. But\n"
	.string "I think I'm starting to see the light at\l"
	.string "the end of the tunnel!$"

@ ---- Galar_Circhester08 ----
GalarTrn_G12M12_o0::
	trainerbattle_single TRAINER_GALAR_CARTER_313, GalarTrn_G12M12_o0_Intro, GalarTrn_G12M12_o0_Derrota
	msgbox GalarTrn_Depois_SAILOR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M12_o0_Intro:
	.string "Not so fast!$"

GalarTrn_G12M12_o0_Derrota:
	.string "...$"

GalarTrn_G12M12_o1::
	trainerbattle_single TRAINER_GALAR_MITCH_314, GalarTrn_G12M12_o1_Intro, GalarTrn_G12M12_o1_Derrota
	msgbox GalarTrn_Depois_SAILOR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M12_o1_Intro:
	.string "Hey, wait up!$"

GalarTrn_G12M12_o1_Derrota:
	.string "...$"

GalarTrn_G12M12_o2::
	trainerbattle_single TRAINER_GALAR_BECK_315, GalarTrn_G12M12_o2_Intro, GalarTrn_G12M12_o2_Derrota
	msgbox GalarTrn_Depois_SAILOR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M12_o2_Intro:
	.string "You're going quite far, aren't you?$"

GalarTrn_G12M12_o2_Derrota:
	.string "...$"

GalarTrn_G12M12_o3::
	trainerbattle_single TRAINER_GALAR_MARLON_316, GalarTrn_G12M12_o3_Intro, GalarTrn_G12M12_o3_Derrota
	msgbox GalarTrn_Depois_SAILOR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M12_o3_Intro:
	.string "Not if I can help it!$"

GalarTrn_G12M12_o3_Derrota:
	.string "...$"

@ ---- Galar_Circhester09 ----
GalarTrn_G12M13_o0::
	trainerbattle_single TRAINER_GALAR_MOGAN_130, GalarTrn_G12M13_o0_Intro, GalarTrn_G12M13_o0_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M13_o0_Intro:
	.string "You're going quite far, aren't you?$"

GalarTrn_G12M13_o0_Derrota:
	.string "...$"

GalarTrn_G12M13_o1::
	trainerbattle_single TRAINER_GALAR_LESLIE_173, GalarTrn_G12M13_o1_Intro, GalarTrn_G12M13_o1_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M13_o1_Intro:
	.string "Not if I can help it!$"

GalarTrn_G12M13_o1_Derrota:
	.string "...$"

GalarTrn_G12M13_o2::
	trainerbattle_single TRAINER_GALAR_ANDRE_129, GalarTrn_G12M13_o2_Intro, GalarTrn_G12M13_o2_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M13_o2_Intro:
	.string "Hey, wait up!$"

GalarTrn_G12M13_o2_Derrota:
	.string "...$"

GalarTrn_G12M13_o3::
	trainerbattle_single TRAINER_GALAR_ETHAN_128, GalarTrn_G12M13_o3_Intro, GalarTrn_G12M13_o3_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M13_o3_Intro:
	.string "Not so fast!$"

GalarTrn_G12M13_o3_Derrota:
	.string "...$"

@ ---- Galar_Circhester10 ----
GalarTrn_G12M14_o12::
	trainerbattle_single TRAINER_GALAR_MELONY_336, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G12M14_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M14_o12_Derrota:
	.string "I think you took breaking the ice a\n"
	.string "little too literally ...$"

@ ---- Galar_Circhester11 ----
GalarTrn_G12M15_o12::
	trainerbattle_single TRAINER_GALAR_GORDIE_49, GalarTrn_G12M15_o12_Intro, GalarTrn_G12M15_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M15_o12_Intro:
	.string "Gordie: Hello, my name is Gordie. I feel a\n"
	.string "little bad about having to end a Gym\l"
	.string "Challenger's dreams, but... I'm going to\l"
	.string "use this match to show the crowd that\l"
	.string "my Pokémon are unbeatable and amazing!\l"
	.string "So let's get this over with, Challenger!$"

GalarTrn_G12M15_o12_Derrota:
	.string "Looks like I fell to the bottom of the\n"
	.string "well.$"

@ ---- Galar_Circhester17 ----
GalarTrn_G13M12_o0::
	trainerbattle_single TRAINER_GALAR_MOGAN_130_2, GalarTrn_G13M12_o0_Intro, GalarTrn_G13M12_o0_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M12_o0_Intro:
	.string "You're going quite far, aren't you?$"

GalarTrn_G13M12_o0_Derrota:
	.string "...$"

GalarTrn_G13M12_o1::
	trainerbattle_single TRAINER_GALAR_LESLIE_173_2, GalarTrn_G13M12_o1_Intro, GalarTrn_G13M12_o1_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M12_o1_Intro:
	.string "Not if I can help it!$"

GalarTrn_G13M12_o1_Derrota:
	.string "...$"

GalarTrn_G13M12_o2::
	trainerbattle_single TRAINER_GALAR_ANDRE_129_2, GalarTrn_G13M12_o2_Intro, GalarTrn_G13M12_o2_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M12_o2_Intro:
	.string "Hey, wait up!$"

GalarTrn_G13M12_o2_Derrota:
	.string "...$"

GalarTrn_G13M12_o3::
	trainerbattle_single TRAINER_GALAR_ETHAN_128_2, GalarTrn_G13M12_o3_Intro, GalarTrn_G13M12_o3_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M12_o3_Intro:
	.string "Not so fast!$"

GalarTrn_G13M12_o3_Derrota:
	.string "...$"

@ ---- Galar_CrownTundra02 ----
GalarTrn_G00M15_o0::
	trainerbattle_single TRAINER_GALAR_PEONY_343, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G00M15_o0_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G00M15_o0_Derrota:
	.string "WOW$"

GalarTrn_G00M15_o2::
	trainerbattle_single TRAINER_GALAR_MEGAN_648, GalarTrn_Intro_LASS_FRLG, GalarTrn_G00M15_o2_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G00M15_o2_Derrota:
	.string "WOW$"

@ ---- Galar_CrownTundra09 ----
GalarTrn_G37M06_o31::
	trainerbattle_single TRAINER_GALAR_TOMMY_300_2, GalarTrn_G37M06_o31_Intro, GalarTrn_G37M06_o31_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G37M06_o31_Intro:
	.string "I'm Tommy. I'm from the Twilight Wings\n"
	.string "anime, and now I'm going to win!!!$"

GalarTrn_G37M06_o31_Derrota:
	.string "Congratulations$"

GalarTrn_G37M06_o42::
	trainerbattle_single TRAINER_GALAR_JON_299_2, GalarTrn_G37M06_o42_Intro, GalarTrn_G37M06_o42_Derrota
	msgbox GalarTrn_Depois_TAMER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G37M06_o42_Intro:
	.string "Twilight Wings was a good anime, wasn't\n"
	.string "it?\p"
	.string "I'm Jon. I finally got over my illness\n"
	.string "and now I'm a great Trainer!$"

GalarTrn_G37M06_o42_Derrota:
	.string "Wow, that was incredible!!!$"

@ ---- Galar_DynamaxAdventure01 ----
GalarTrn_G34M04_o0::
	trainerbattle_single TRAINER_GALAR_MEGAN_648_2, GalarTrn_Intro_LASS_FRLG, GalarTrn_G34M04_o0_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G34M04_o0_Derrota:
	.string "Wow, how incredible!$"

@ ---- Galar_GalarMine02 ----
GalarTrn_G06M28_o0::
	trainerbattle_single TRAINER_GALAR_KENT_108, GalarTrn_G06M28_o0_Intro, GalarTrn_G06M28_o0_Derrota
	msgbox GalarTrn_Depois_KINDLER, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M28_o0_Intro:
	.string "Another kid in the cave?\n"
	.string "Are you two together?$"

GalarTrn_G06M28_o0_Derrota:
	.string "You got me!$"

GalarTrn_G06M28_o1::
	trainerbattle_single TRAINER_GALAR_JOVAN_169, GalarTrn_G06M28_o1_Intro, GalarTrn_G06M28_o1_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M28_o1_Intro:
	.string "What!\n"
	.string "Don't come near me.$"

GalarTrn_G06M28_o1_Derrota:
	.string "My Pokémon is no good!$"

GalarTrn_G06M28_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_121, GalarTrn_G06M28_o2_Intro, GalarTrn_G06M28_o2_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M28_o2_Intro:
	.string "What?\p"
	.string "I'm waiting for my friends to meet me\n"
	.string "here.$"

GalarTrn_G06M28_o2_Derrota:
	.string "I lost?$"

@ ---- Galar_GalarMine03 ----
GalarTrn_G08M20_o10::
	trainerbattle_single TRAINER_GALAR_LEAH_476, GalarTrn_G08M20_o10_Intro, GalarTrn_G08M20_o10_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o10_Intro:
	.string "Eek!\p"
	.string "Don't try anything funny in the dark!$"

GalarTrn_G08M20_o10_Derrota:
	.string "It was too dark.$"

GalarTrn_G08M20_o2::
	trainerbattle_single TRAINER_GALAR_GRUNT_12, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M20_o2_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o2_Derrota:
	.string "you really are strong$"

GalarTrn_G08M20_o3::
	trainerbattle_single TRAINER_GALAR_GRUNT_12_2, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M20_o3_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o3_Derrota:
	.string "you really are strong$"

GalarTrn_G08M20_o4::
	trainerbattle_single TRAINER_GALAR_BEDE_11, GalarTrn_Intro_RIVAL, GalarTrn_G08M20_o4_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o4_Derrota:
	.string "you really are strong$"

GalarTrn_G08M20_o8::
	trainerbattle_single TRAINER_GALAR_DANA_474, GalarTrn_G08M20_o8_Intro, GalarTrn_G08M20_o8_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o8_Intro:
	.string "I came all the way here looking for a\n"
	.string "wild Pokémon.$"

GalarTrn_G08M20_o8_Derrota:
	.string "I'm out of Pokémon!$"

GalarTrn_G08M20_o9::
	trainerbattle_single TRAINER_GALAR_ARIANA_475, GalarTrn_G08M20_o9_Intro, GalarTrn_G08M20_o9_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M20_o9_Intro:
	.string "You have Pokémon!\n"
	.string "Let's get started!$"

GalarTrn_G08M20_o9_Derrota:
	.string "That game was hard.$"

@ ---- Galar_GalarMine05 ----
GalarTrn_G07M10_o1::
	trainerbattle_single TRAINER_GALAR_MARCOS_181, GalarTrn_G07M10_o1_Intro, GalarTrn_G07M10_o1_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M10_o1_Intro:
	.string "Whoa!\nYou shocked me!\l…Oh, you’re just a kid!$"

GalarTrn_G07M10_o1_Derrota:
	.string "Wow!\nShocked again!$"

GalarTrn_G07M10_o4::
	trainerbattle_single TRAINER_GALAR_BRADLEY_174, GalarTrn_G07M10_o4_Intro, GalarTrn_G07M10_o4_Derrota
	msgbox GalarTrn_Depois_SUPER_NERD_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M10_o4_Intro:
	.string "Did you come to battle Milo too?$"

GalarTrn_G07M10_o4_Derrota:
	.string "Losing stinks!\n"
	.string "It's not cool at all.$"

@ ---- Galar_GlimwoodTangle01 ----
GalarTrn_G01M109_o0::
	trainerbattle_single TRAINER_GALAR_ROBERT_157, GalarTrn_G01M109_o0_Intro, GalarTrn_G01M109_o0_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M109_o0_Intro:
	.string "I'm feeling a little dizzy. It's been a\n"
	.string "while since I walked this far.$"

GalarTrn_G01M109_o0_Derrota:
	.string "I'm very tired.\n"
	.string "I wasn't ready for that.$"

GalarTrn_G01M109_o14::
	trainerbattle_single TRAINER_GALAR_JACQUELINE_188, GalarTrn_G01M109_o14_Intro, GalarTrn_G01M109_o14_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M109_o14_Intro:
	.string "Ah!\n"
	.string "The air here is delightful!$"

GalarTrn_G01M109_o14_Derrota:
	.string "That cleared my head!$"

GalarTrn_G01M109_o15::
	trainerbattle_single TRAINER_GALAR_JUDY_163, GalarTrn_G01M109_o15_Intro, GalarTrn_G01M109_o15_Derrota
	msgbox GalarTrn_Depois_LADY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M109_o15_Intro:
	.string "Hello!\n"
	.string "Want to see my Pokémon?$"

GalarTrn_G01M109_o15_Derrota:
	.string "Oh no!\n"
	.string "My Pokémon!$"

GalarTrn_G01M109_o16::
	trainerbattle_single TRAINER_GALAR_CLARK_187, GalarTrn_G01M109_o16_Intro, GalarTrn_G01M109_o16_Derrota
	msgbox GalarTrn_Depois_KINDLER, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M109_o16_Intro:
	.string "Ha-hahah-ah-ha!$"

GalarTrn_G01M109_o16_Derrota:
	.string "Ha-haha!\nHa-hay fever! Haha-ha-choo!$"

@ ---- Galar_Hammerlocke02 ----
GalarTrn_G04M08_o0::
	trainerbattle_single TRAINER_GALAR_MARCIO_459, GalarTrn_G04M08_o0_Intro, GalarTrn_G04M08_o0_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G04M08_o0_Intro:
	.string "I represent Raihan.$"

GalarTrn_G04M08_o0_Derrota:
	.string "I lost.$"

GalarTrn_G04M08_o1::
	trainerbattle_single TRAINER_GALAR_GABRIEL_458, GalarTrn_G04M08_o1_Intro, GalarTrn_G04M08_o1_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G04M08_o1_Intro:
	.string "I represent Raihan.$"

GalarTrn_G04M08_o1_Derrota:
	.string "I lost.$"

GalarTrn_G04M08_o2::
	trainerbattle_single TRAINER_GALAR_CARLOS_457, GalarTrn_G04M08_o2_Intro, GalarTrn_G04M08_o2_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G04M08_o2_Intro:
	.string "I represent Raihan.$"

GalarTrn_G04M08_o2_Derrota:
	.string "I lost.$"

@ ---- Galar_Hammerlocke10 ----
GalarTrn_G09M17_o0::
	trainerbattle_single TRAINER_GALAR_ROSE_85, GalarTrn_Intro_MAGMA_ADMIN, GalarTrn_G09M17_o0_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G09M17_o0_Derrota:
	.string "I'd forgotten how great Pokémon\n"
	.string "battles are!\p"
	.string "It's been so long since I fought... That\n"
	.string "was definitely satisfying.$"

@ ---- Galar_Hammerlocke23 ----
GalarTrn_G03M06_o10::
	trainerbattle_single TRAINER_GALAR_HOP_429, GalarTrn_Intro_RIVAL, GalarTrn_G03M06_o10_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M06_o10_Derrota:
	.string "My strategy goes straight down the\n"
	.string "drain when I have all these bad\l"
	.string "thoughts running through my head. $"

GalarTrn_G03M06_o9::
	trainerbattle_single TRAINER_GALAR_HOP_429_2, GalarTrn_Intro_RIVAL, GalarTrn_G03M06_o9_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M06_o9_Derrota:
	.string "My strategy goes straight down the\n"
	.string "drain when I have all these bad\l"
	.string "thoughts running through my head. $"

@ ---- Galar_Hulbury06 ----
GalarTrn_G08M07_o17::
	trainerbattle_single TRAINER_GALAR_WANDA_686, GalarTrn_G08M07_o17_Intro, GalarTrn_G08M07_o17_Derrota
	msgbox GalarTrn_Depois_FISHERMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M07_o17_Intro:
	.string "{COLOR LIGHT_RED}Hey, it's dull around here.\p"
	.string "How about a battle to loosen things up?$"

GalarTrn_G08M07_o17_Derrota:
	.string "{COLOR LIGHT_RED}It's time to get back to work.$"

GalarTrn_G08M07_o39::
	trainerbattle_single TRAINER_GALAR_ROBERT_656, GalarTrn_Intro_COLLECTOR, GalarTrn_G08M07_o39_Derrota
	msgbox GalarTrn_Depois_COLLECTOR, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M07_o39_Derrota:
	.string "Darn! You won...$"

@ ---- Galar_Hulbury07 ----
GalarTrn_G08M08_o0::
	trainerbattle_single TRAINER_GALAR_JONH_5, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M08_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M08_o0_Derrota:
	.string "Team Yell: Gah ... You crushed my attempt\n"
	.string "to crush.$"

GalarTrn_G08M08_o3::
	trainerbattle_single TRAINER_GALAR_HOP_332, GalarTrn_Intro_RIVAL, GalarTrn_G08M08_o3_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M08_o3_Derrota:
	.string "We both got the Grass Badge, so how is\n"
	.string "it that you are\p"
	.string "so much stronger?! $"

@ ---- Galar_Hulbury08 ----
GalarTrn_G08M14_o0::
	trainerbattle_single TRAINER_GALAR_JULIA_234, GalarTrn_G08M14_o0_Intro, GalarTrn_G08M14_o0_Derrota
	msgbox GalarTrn_Depois_SWIMMER_M_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M14_o0_Intro:
	.string "Splash!\pI’m first up!\nLet’s do it!$"

GalarTrn_G08M14_o0_Derrota:
	.string "That can’t be!$"

GalarTrn_G08M14_o1::
	trainerbattle_single TRAINER_GALAR_DIANA_150, GalarTrn_G08M14_o1_Intro, GalarTrn_G08M14_o1_Derrota
	msgbox GalarTrn_Depois_SWIMMER_M_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M14_o1_Intro:
	.string "What? You?\nI’m more than good enough for you!\pMisty won’t have to be bothered.$"

GalarTrn_G08M14_o1_Derrota:
	.string "You overwhelmed me!$"

GalarTrn_G08M14_o2::
	trainerbattle_single TRAINER_GALAR_ANA_210, GalarTrn_G08M14_o2_Intro, GalarTrn_G08M14_o2_Derrota
	msgbox GalarTrn_Depois_BURGLAR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M14_o2_Intro:
	.string "Here’s No. 3!\nI won’t be easy!$"

GalarTrn_G08M14_o2_Derrota:
	.string "Ow!\nStomped flat!$"

@ ---- Galar_Hulbury10 ----
GalarTrn_G08M16_o12::
	trainerbattle_single TRAINER_GALAR_NESSA_307, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G08M16_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M16_o12_Derrota:
	.string "I don't get it.\p"
	.string "What do I have to do to beat you, huh?$"

@ ---- Galar_Hulbury12 ----
GalarTrn_G08M26_o0::
	trainerbattle_single TRAINER_GALAR_JONH_5_4, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M26_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M26_o0_Derrota:
	.string "Team Yell: Gah ... You crushed my attempt\n"
	.string "to crush.$"

GalarTrn_G08M26_o3::
	trainerbattle_single TRAINER_GALAR_HOP_332_2, GalarTrn_Intro_RIVAL, GalarTrn_G08M26_o3_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M26_o3_Derrota:
	.string "We both got the Grass Badge, so how is\n"
	.string "it that you are\p"
	.string "so much stronger?! $"

@ ---- Galar_IsleOfArmor05 ----
GalarTrn_G38M01_o0::
	trainerbattle_single TRAINER_GALAR_KLARA_225, GalarTrn_Intro_RIVAL, GalarTrn_G38M01_o0_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M01_o0_Derrota:
	.string "Klara: Huh?! No, no! No, no, no! There\n"
	.string "must be some kind of mistake!$"

@ ---- Galar_IsleOfArmor13 ----
GalarTrn_G38M09_o30::
	trainerbattle_single TRAINER_GALAR_CLAYTON_SA_373, GalarTrn_G38M09_o30_Intro, GalarTrn_G38M09_o30_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M09_o30_Intro:
	.string "Clayton Santos: Wow, you really found\n"
	.string "me!\p"
	.string "I thought I was hidden well enough, but\n"
	.string "anyway, since we're both here, let's\l"
	.string "battle!$"

GalarTrn_G38M09_o30_Derrota:
	.string "Clayton Santos: That was a good battle.$"

@ ---- Galar_IsleOfArmor19 ----
GalarTrn_G38M15_o0::
	trainerbattle_single TRAINER_GALAR_MUSTARD_230, GalarTrn_Intro_BLACK_BELT_FRLG, GalarTrn_G38M15_o0_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M15_o0_Derrota:
	.string "You young people grow up so fast!\p"
	.string "It never stops surprising me.$"

@ ---- Galar_IsleOfArmor25 ----
GalarTrn_G38M21_o5::
	trainerbattle_single TRAINER_GALAR_MUSTARD_230_2, GalarTrn_Intro_BLACK_BELT_FRLG, GalarTrn_G38M21_o5_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M21_o5_Derrota:
	.string "You young people grow up so fast!\p"
	.string "It never stops surprising me.$"

@ ---- Galar_IsleOfArmor32 ----
GalarTrn_G38M28_o12::
	trainerbattle_single TRAINER_GALAR_LUCAS_231, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G38M28_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M28_o12_Derrota:
	.string "Lucas: DUDE... THAT WAS AWESOME!!!$"

@ ---- Galar_IsleOfArmor33 ----
GalarTrn_G38M29_o12::
	trainerbattle_single TRAINER_GALAR_VANESSA_233, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G38M29_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M29_o12_Derrota:
	.string "...\n...\l...$"

@ ---- Galar_IsleOfArmor34 ----
GalarTrn_G38M30_o12::
	trainerbattle_single TRAINER_GALAR_C_PHENE_232, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G38M30_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G38M30_o12_Derrota:
	.string "Coronel.Phene: That strategy...\p"
	.string "That battling spirit...\p"
	.string "It reminds me a lot of the red cap, but...$"

@ ---- Galar_Motostoke06 ----
GalarTrn_G06M12_o2::
	trainerbattle_single TRAINER_GALAR_KEVIN_1, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G06M12_o2_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M12_o2_Derrota:
	.string "Give it a rest!\n"
	.string "Team Yell, avenge me!$"

@ ---- Galar_Motostoke16 ----
GalarTrn_G06M26_o1::
	trainerbattle_single TRAINER_GALAR_BIANCA_21, GalarTrn_Intro_LASS_FRLG, GalarTrn_G06M26_o1_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M26_o1_Derrota:
	.string "Wow..$"

@ ---- Galar_Motostoke18 ----
GalarTrn_G06M33_o1::
	trainerbattle_single TRAINER_GALAR_TYLER_96, GalarTrn_G06M33_o1_Intro, GalarTrn_G06M33_o1_Derrota
	msgbox GalarTrn_Depois_YOUNGSTER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M33_o1_Intro:
	.string "I love Pokémon!\nDo you?$"

GalarTrn_G06M33_o1_Derrota:
	.string "Wow! \nYou’re great!$"

GalarTrn_G06M33_o2::
	trainerbattle_single TRAINER_GALAR_ANDO_126, GalarTrn_G06M33_o2_Intro, GalarTrn_G06M33_o2_Derrota
	msgbox GalarTrn_Depois_COOLTRAINER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M33_o2_Intro:
	.string "I collected these Pokémon\nfrom all around the world!$"

GalarTrn_G06M33_o2_Derrota:
	.string "Oh, no!\nI went around the world for these!$"

GalarTrn_G06M33_o3::
	trainerbattle_single TRAINER_GALAR_BROOKS_482, GalarTrn_G06M33_o3_Intro, GalarTrn_G06M33_o3_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M33_o3_Intro:
	.string "Competing against the young keeps\nme youthful.$"

GalarTrn_G06M33_o3_Derrota:
	.string "Good match!\nAh, I feel young again!$"

@ ---- Galar_Motostoke19 ----
GalarTrn_G06M34_o9::
	trainerbattle_single TRAINER_GALAR_KABU_308, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G06M34_o9_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M34_o9_Derrota:
	.string "Good Pokémon and a great Trainer!\p"
	.string "It's no surprise that you won!$"

@ ---- Galar_Postwick10 ----
GalarTrn_G01M110_o10::
	trainerbattle_single TRAINER_GALAR_JUDY_163_2, GalarTrn_G01M110_o10_Intro, GalarTrn_G01M110_o10_Derrota
	msgbox GalarTrn_Depois_LADY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M110_o10_Intro:
	.string "Hello!\n"
	.string "Want to see my Pokémon?$"

GalarTrn_G01M110_o10_Derrota:
	.string "Oh no!\n"
	.string "My Pokémon!$"

GalarTrn_G01M110_o7::
	trainerbattle_single TRAINER_GALAR_CLARK_187_2, GalarTrn_G01M110_o7_Intro, GalarTrn_G01M110_o7_Derrota
	msgbox GalarTrn_Depois_KINDLER, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M110_o7_Intro:
	.string "Ha-hahah-ah-ha!$"

GalarTrn_G01M110_o7_Derrota:
	.string "Ha-haha!\nHa-hay fever! Haha-ha-choo!$"

GalarTrn_G01M110_o8::
	trainerbattle_single TRAINER_GALAR_ROBERT_157_2, GalarTrn_G01M110_o8_Intro, GalarTrn_G01M110_o8_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M110_o8_Intro:
	.string "I'm feeling a little dizzy. It's been a\n"
	.string "while since I walked this far.$"

GalarTrn_G01M110_o8_Derrota:
	.string "I'm very tired.\n"
	.string "I wasn't ready for that.$"

GalarTrn_G01M110_o9::
	trainerbattle_single TRAINER_GALAR_JACQUELINE_188_2, GalarTrn_G01M110_o9_Intro, GalarTrn_G01M110_o9_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M110_o9_Intro:
	.string "Ah!\n"
	.string "The air here is delightful!$"

GalarTrn_G01M110_o9_Derrota:
	.string "That cleared my head!$"

@ ---- Galar_Postwick166 ----
GalarTrn_G39M41_o0::
	trainerbattle_single TRAINER_GALAR_MARTHA_SANT_381, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M41_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M41_o0_Derrota:
	.string "Martha Santos: Aw...\n"
	.string "I did my best...$"

@ ---- Galar_Postwick40 ----
GalarTrn_G07M07_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_116_2, GalarTrn_G07M07_o2_Intro, GalarTrn_G07M07_o2_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M07_o2_Intro:
	.string "Excuse me!\n"
	.string "You looked at me, didn't you?$"

GalarTrn_G07M07_o2_Derrota:
	.string "You're mean!$"

GalarTrn_G07M07_o3::
	trainerbattle_single TRAINER_GALAR_ANA_211_2, GalarTrn_G07M07_o3_Intro, GalarTrn_G07M07_o3_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M07_o3_Intro:
	.string "Hi!\n"
	.string "I like All Stars!\p"
	.string "They're delightfully comfortable and\n"
	.string "easy to wear!$"

GalarTrn_G07M07_o3_Derrota:
	.string "I don't believe it!$"

GalarTrn_G07M07_o5::
	trainerbattle_single TRAINER_GALAR_ROBIN_118_2, GalarTrn_G07M07_o5_Intro, GalarTrn_G07M07_o5_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M07_o5_Intro:
	.string "Eek!\n"
	.string "You touched me?$"

GalarTrn_G07M07_o5_Derrota:
	.string "Is that it?$"

GalarTrn_G07M07_o6::
	trainerbattle_single TRAINER_GALAR_JAMES_107_2, GalarTrn_G07M07_o6_Intro, GalarTrn_G07M07_o6_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M07_o6_Intro:
	.string "I'll battle you with the Pokémon I just\n"
	.string "caught.$"

GalarTrn_G07M07_o6_Derrota:
	.string "I should have trained more...$"

@ ---- Galar_Postwick53 ----
GalarTrn_G08M21_o0::
	trainerbattle_single TRAINER_GALAR_JONH_5_2, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M21_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M21_o0_Derrota:
	.string "Team Yell: Gah ... You crushed my attempt\n"
	.string "to crush.$"

GalarTrn_G08M21_o3::
	trainerbattle_single TRAINER_GALAR_JONH_5_3, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G08M21_o3_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M21_o3_Derrota:
	.string "Team Yell: Gah ... You crushed my attempt\n"
	.string "to crush.$"

@ ---- Galar_RixyChamber01 ----
GalarTrn_G03M53_o0::
	trainerbattle_single TRAINER_GALAR_MIAH_588, GalarTrn_G03M53_o0_Intro, GalarTrn_G03M53_o0_Derrota
	msgbox GalarTrn_Depois_AROMA_LADY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M53_o0_Intro:
	.string "Kyahaha!\nI’ll flick you away effortlessly!$"

GalarTrn_G03M53_o0_Derrota:
	.string "Tch!\nToo strong for me!$"

GalarTrn_G03M53_o1::
	trainerbattle_single TRAINER_GALAR_MADELINE_522, GalarTrn_G03M53_o1_Intro, GalarTrn_G03M53_o1_Derrota
	msgbox GalarTrn_Depois_PKMN_RANGER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M53_o1_Intro:
	.string "I punish people who abuse\nPokémon!$"

GalarTrn_G03M53_o1_Derrota:
	.string "You don’t seem to be a problem\nTrainer.$"

GalarTrn_G03M53_o2::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589, GalarTrn_G03M53_o2_Intro, GalarTrn_G03M53_o2_Derrota, GalarTrn_G03M53_o2_Poucos
	msgbox GalarTrn_Depois_YOUNG_COUPLE_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M53_o2_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G03M53_o2_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G03M53_o2_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

GalarTrn_G03M53_o4::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589_2, GalarTrn_G03M53_o4_Intro, GalarTrn_G03M53_o4_Derrota, GalarTrn_G03M53_o4_Poucos
	msgbox GalarTrn_Depois_YOUNG_COUPLE_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M53_o4_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G03M53_o4_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G03M53_o4_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

GalarTrn_G03M53_o5::
	trainerbattle_single TRAINER_GALAR_NICOLAS_521, GalarTrn_G03M53_o5_Intro, GalarTrn_G03M53_o5_Derrota
	msgbox GalarTrn_Depois_PKMN_RANGER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M53_o5_Intro:
	.string "This island is too spread out…\nIt’s not easy patrolling the place.$"

GalarTrn_G03M53_o5_Derrota:
	.string "Uh-huh…$"

@ ---- Galar_RoseTower01 ----
GalarTrn_G01M90_o1::
	trainerbattle_single TRAINER_GALAR_CARLOS_442, GalarTrn_G01M90_o1_Intro, GalarTrn_G01M90_o1_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M90_o1_Intro:
	.string "I'm paid to stop you!$"

GalarTrn_G01M90_o1_Derrota:
	.string "Hmm?$"

@ ---- Galar_RoseTower02 ----
GalarTrn_G01M91_o0::
	trainerbattle_single TRAINER_GALAR_LAURO_445, GalarTrn_G01M91_o0_Intro, GalarTrn_G01M91_o0_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M91_o0_Intro:
	.string "Stop!\p"
	.string "This is for the good of Galar!$"

GalarTrn_G01M91_o0_Derrota:
	.string "What!$"

GalarTrn_G01M91_o1::
	trainerbattle_single TRAINER_GALAR_JODY_446, GalarTrn_G01M91_o1_Intro, GalarTrn_G01M91_o1_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M91_o1_Intro:
	.string "How careless!$"

GalarTrn_G01M91_o1_Derrota:
	.string "What?$"

@ ---- Galar_RoseTower03 ----
GalarTrn_G01M92_o1::
	trainerbattle_single TRAINER_GALAR_TAMMY_447, GalarTrn_G01M92_o1_Intro, GalarTrn_G01M92_o1_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M92_o1_Intro:
	.string "GET OUT OF HERE!$"

GalarTrn_G01M92_o1_Derrota:
	.string "Gasp!$"

@ ---- Galar_RoseTower04 ----
GalarTrn_G01M94_o1::
	trainerbattle_single TRAINER_GALAR_OLENA_80, GalarTrn_Intro_MAGMA_ADMIN, GalarTrn_G01M94_o1_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G01M94_o1_Derrota:
	.string "  sigh   I couldn't win.\n"
	.string "... Oleana ... you really are\l"
	.string "a hopeless woman.$"

@ ---- Galar_Route0202 ----
GalarTrn_G05M12_o3::
	trainerbattle_single TRAINER_GALAR_LASS_102, GalarTrn_G05M12_o3_Intro, GalarTrn_G05M12_o3_Derrota
	msgbox GalarTrn_Depois_LADY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G05M12_o3_Intro:
	.string "Hey! You have Pokémon!\n"
	.string "Let's battle!$"

GalarTrn_G05M12_o3_Derrota:
	.string "Aha, man...$"

GalarTrn_G05M12_o5::
	trainerbattle_single TRAINER_GALAR_SAMMY_104, GalarTrn_G05M12_o5_Intro, GalarTrn_G05M12_o5_Derrota
	msgbox GalarTrn_Depois_YOUNGSTER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G05M12_o5_Intro:
	.string "Hey, wait!\n"
	.string "What's the rush?$"

GalarTrn_G05M12_o5_Derrota:
	.string "I give up!\n"
	.string "You're good at this!$"

GalarTrn_G05M12_o6::
	trainerbattle_single TRAINER_GALAR_ANTHONY_531, GalarTrn_G05M12_o6_Intro, GalarTrn_G05M12_o6_Derrota
	msgbox GalarTrn_Depois_BUG_CATCHER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G05M12_o6_Intro:
	.string "I may be small, but what I won't like is\n"
	.string "you going easy on me!$"

GalarTrn_G05M12_o6_Derrota:
	.string "Ah, right.\n"
	.string "It went wrong.$"

@ ---- Galar_Route0301 ----
GalarTrn_G06M17_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_116, GalarTrn_G06M17_o2_Intro, GalarTrn_G06M17_o2_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M17_o2_Intro:
	.string "Excuse me!\n"
	.string "You looked at me, didn't you?$"

GalarTrn_G06M17_o2_Derrota:
	.string "You're mean!$"

GalarTrn_G06M17_o3::
	trainerbattle_single TRAINER_GALAR_ANA_211, GalarTrn_G06M17_o3_Intro, GalarTrn_G06M17_o3_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M17_o3_Intro:
	.string "Hi!\n"
	.string "I like All Stars!\p"
	.string "They're delightfully comfortable and\n"
	.string "easy to wear!$"

GalarTrn_G06M17_o3_Derrota:
	.string "I don't believe it!$"

GalarTrn_G06M17_o4::
	trainerbattle_single TRAINER_GALAR_CALVIN_90, GalarTrn_G06M17_o4_Intro, GalarTrn_G06M17_o4_Derrota
	msgbox GalarTrn_Depois_YOUNGSTER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M17_o4_Intro:
	.string "Hey! I saw you on TV!\n"
	.string "What have you got there?$"

GalarTrn_G06M17_o4_Derrota:
	.string "Lost!\n"
	.string "Lost! I'm Lost!$"

GalarTrn_G06M17_o5::
	trainerbattle_single TRAINER_GALAR_ROBIN_118, GalarTrn_G06M17_o5_Intro, GalarTrn_G06M17_o5_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M17_o5_Intro:
	.string "Eek!\n"
	.string "You touched me?$"

GalarTrn_G06M17_o5_Derrota:
	.string "Is that it?$"

GalarTrn_G06M17_o6::
	trainerbattle_single TRAINER_GALAR_JAMES_107, GalarTrn_G06M17_o6_Intro, GalarTrn_G06M17_o6_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G06M17_o6_Intro:
	.string "I'll battle you with the Pokémon I just\n"
	.string "caught.$"

GalarTrn_G06M17_o6_Derrota:
	.string "I should have trained more...$"

@ ---- Galar_Route0401 ----
GalarTrn_G07M17_o2::
	trainerbattle_single TRAINER_GALAR_BRADLEY_174_2, GalarTrn_G07M17_o2_Intro, GalarTrn_G07M17_o2_Derrota
	msgbox GalarTrn_Depois_SUPER_NERD_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M17_o2_Intro:
	.string "Did you come to battle Milo too?$"

GalarTrn_G07M17_o2_Derrota:
	.string "Losing stinks!\n"
	.string "It's not cool at all.$"

@ ---- Galar_Route0501 ----
GalarTrn_G08M06_o4::
	trainerbattle_single TRAINER_GALAR_JASPER_259, GalarTrn_G08M06_o4_Intro, GalarTrn_G08M06_o4_Derrota
	msgbox GalarTrn_Depois_COLLECTOR, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G08M06_o4_Intro:
	.string "Competing is the ultimate thrill.\n"
	.string "I still can't get enough of it!$"

GalarTrn_G08M06_o4_Derrota:
	.string "I had a chance!$"

@ ---- Galar_Route0601 ----
GalarTrn_G10M20_o0::
	trainerbattle_single TRAINER_GALAR_GRUNT_13, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G10M20_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o0_Derrota:
	.string "Ah, man! The posh air around here killed\n"
	.string "my buzz!$"

GalarTrn_G10M20_o1::
	trainerbattle_single TRAINER_GALAR_GRUNT_13_2, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G10M20_o1_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o1_Derrota:
	.string "Ah, man! The posh air around here killed\n"
	.string "my buzz!$"

GalarTrn_G10M20_o10::
	trainerbattle_single TRAINER_GALAR_DIANE_151, GalarTrn_G10M20_o10_Intro, GalarTrn_G10M20_o10_Derrota
	msgbox GalarTrn_Depois_PICNICKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o10_Intro:
	.string "Excuse me!\n"
	.string "This is a private conversation!\l"
	.string "With myself!$"

GalarTrn_G10M20_o10_Derrota:
	.string "Ugh!\n"
	.string "I hate losing.$"

GalarTrn_G10M20_o26::
	trainerbattle_single TRAINER_GALAR_ISABELLE_152, GalarTrn_G10M20_o26_Intro, GalarTrn_G10M20_o26_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o26_Intro:
	.string "me?\n"
	.string "Well, okay. I'll play!$"

GalarTrn_G10M20_o26_Derrota:
	.string "Things just didn't work out for me...$"

GalarTrn_G10M20_o6::
	trainerbattle_single TRAINER_GALAR_HANNA_172, GalarTrn_G10M20_o6_Intro, GalarTrn_G10M20_o6_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o6_Intro:
	.string "You have to be informed.\n"
	.string "You need strategy to win at this!$"

GalarTrn_G10M20_o6_Derrota:
	.string "That isn't logical!$"

GalarTrn_G10M20_o7::
	trainerbattle_single TRAINER_GALAR_RUTH_111, GalarTrn_G10M20_o7_Intro, GalarTrn_G10M20_o7_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o7_Intro:
	.string "There aren't many bugs here.$"

GalarTrn_G10M20_o7_Derrota:
	.string "No!\n"
	.string "You're kidding!$"

GalarTrn_G10M20_o9::
	trainerbattle_single TRAINER_GALAR_IWAN_E_EVEL_145, GalarTrn_G10M20_o9_Intro, GalarTrn_G10M20_o9_Derrota
	msgbox GalarTrn_Depois_BUG_MANIAC, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M20_o9_Intro:
	.string "Who's there?$"

GalarTrn_G10M20_o9_Derrota:
	.string "I just can't win!$"

@ ---- Galar_Route0701 ----
GalarTrn_G09M13_o0::
	trainerbattle_single TRAINER_GALAR_MILA_305, GalarTrn_G09M13_o0_Intro, GalarTrn_G09M13_o0_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G09M13_o0_Intro:
	.string "When I whistle,\n"
	.string "I can call a Pokémon.$"

GalarTrn_G09M13_o0_Derrota:
	.string "Ow!\n"
	.string "That's tragic!$"

GalarTrn_G09M13_o1::
	trainerbattle_single TRAINER_GALAR_YAZMIN_478, GalarTrn_G09M13_o1_Intro, GalarTrn_G09M13_o1_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G09M13_o1_Intro:
	.string "Want to play with my Pokémon?$"

GalarTrn_G09M13_o1_Derrota:
	.string "I was far too impatient!$"

GalarTrn_G09M13_o10::
	trainerbattle_single TRAINER_GALAR_BRUCE_306, GalarTrn_G09M13_o10_Intro, GalarTrn_G09M13_o10_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G09M13_o10_Intro:
	.string "You're good, aren't you?$"

GalarTrn_G09M13_o10_Derrota:
	.string "Just as I thought!$"

GalarTrn_G09M13_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_432, GalarTrn_G09M13_o9_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_432, 0, GalarTrn_G09M13_o9_Derrota, GalarTrn_G09M13_o9_Vitoria
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G09M13_o9_Fim:
	release
	end

GalarTrn_G09M13_o9_Derrota:
	.string "let's battle!$"

GalarTrn_G09M13_o9_Vitoria:
	.string "Damn it... My team can't battle well if I\n"
	.string "can't get my head straight.$"

@ ---- Galar_Route0801 ----
GalarTrn_G12M08_o10::
	trainerbattle_single TRAINER_GALAR_PERRY_301, GalarTrn_G12M08_o10_Intro, GalarTrn_G12M08_o10_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M08_o10_Intro:
	.string "I'm not going to lose.\p"
	.string "Not when the wind is blowing my way!$"

GalarTrn_G12M08_o10_Derrota:
	.string "The wind has changed!$"

GalarTrn_G12M08_o11::
	trainerbattle_single TRAINER_GALAR_CHARLES_302, GalarTrn_G12M08_o11_Intro, GalarTrn_G12M08_o11_Derrota
	msgbox GalarTrn_Depois_PSYCHIC_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M08_o11_Intro:
	.string "I always go with my Pokémon.\n"
	.string "I've devoted myself to them.$"

GalarTrn_G12M08_o11_Derrota:
	.string "Out of power!$"

GalarTrn_G12M08_o7::
	trainerbattle_single TRAINER_GALAR_JORDAN_469, GalarTrn_G12M08_o7_Intro, GalarTrn_G12M08_o7_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M08_o7_Intro:
	.string "My cute Pokémon want to meet yours.$"

GalarTrn_G12M08_o7_Derrota:
	.string "Good going!\n"
	.string "You won outright!$"

GalarTrn_G12M08_o9::
	trainerbattle_single TRAINER_GALAR_JOANNA_195, GalarTrn_G12M08_o9_Intro, GalarTrn_G12M08_o9_Derrota
	msgbox GalarTrn_Depois_SCIENTIST_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M08_o9_Intro:
	.string "What are you looking at?$"

GalarTrn_G12M08_o9_Derrota:
	.string "Darn!$"

@ ---- Galar_Route0802 ----
GalarTrn_G12M09_o0::
	trainerbattle_single TRAINER_GALAR_BOBBY_309, GalarTrn_G12M09_o0_Intro, GalarTrn_G12M09_o0_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G12M09_o0_Intro:
	.string "This is my territory!\n"
	.string "Get out of here!$"

GalarTrn_G12M09_o0_Derrota:
	.string "Darn!$"

@ ---- Galar_Route0901 ----
GalarTrn_G14M11_o1::
	trainerbattle_single TRAINER_GALAR_MARNIE_60, GalarTrn_Intro_RIVAL, GalarTrn_G14M11_o1_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o1_Derrota:
	.string "How is this possible?! My Pokémon didn't\n"
	.string "even get the chance to battle properly.\l"
	.string "Ugh!$"

GalarTrn_G14M11_o10::
	trainerbattle_single TRAINER_GALAR_OLIVIER_274, GalarTrn_G14M11_o10_Intro, GalarTrn_G14M11_o10_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o10_Intro:
	.string "I raise Pokémon for protection because\n"
	.string "I live alone.$"

GalarTrn_G14M11_o10_Derrota:
	.string "To me, Pokémon isn't about winning or\n"
	.string "losing.$"

GalarTrn_G14M11_o11::
	trainerbattle_single TRAINER_GALAR_GRACE_273, GalarTrn_G14M11_o11_Intro, GalarTrn_G14M11_o11_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o11_Intro:
	.string "Ah, you're adorable!\n"
	.string "Just like a Pokémon!$"

GalarTrn_G14M11_o11_Derrota:
	.string "You looked so cute before!$"

GalarTrn_G14M11_o13::
	trainerbattle_single TRAINER_GALAR_ERNEST_197, GalarTrn_G14M11_o13_Intro, GalarTrn_G14M11_o13_Derrota
	msgbox GalarTrn_Depois_SWIMMER_M_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o13_Intro:
	.string "Hey! Let's go!$"

GalarTrn_G14M11_o13_Derrota:
	.string "Why not?$"

GalarTrn_G14M11_o14::
	trainerbattle_single TRAINER_GALAR_BECKY_480, GalarTrn_G14M11_o14_Intro, GalarTrn_G14M11_o14_Derrota
	msgbox GalarTrn_Depois_SWIMMER_M_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o14_Intro:
	.string "You look nice, so I think I can beat you.\p"
	.string "I'll give it a try!$"

GalarTrn_G14M11_o14_Derrota:
	.string "No, wrong!$"

GalarTrn_G14M11_o16::
	trainerbattle_single TRAINER_GALAR_ISAIAH_252, GalarTrn_G14M11_o16_Intro, GalarTrn_G14M11_o16_Derrota
	msgbox GalarTrn_Depois_SWIMMER_M_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o16_Intro:
	.string "There's no getting rich quick by\n"
	.string "battling children.$"

GalarTrn_G14M11_o16_Derrota:
	.string "Burn, hellfire!$"

GalarTrn_G14M11_o4::
	trainerbattle_single TRAINER_GALAR_ANA_59, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G14M11_o4_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o4_Derrota:
	.string "  sigh   I want to go back to\n"
	.string "Spikemuth. That's all.$"

GalarTrn_G14M11_o45::
	trainerbattle_single TRAINER_GALAR_VIRGIL_470, GalarTrn_G14M11_o45_Intro, GalarTrn_G14M11_o45_Derrota
	msgbox GalarTrn_Depois_BIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o45_Intro:
	.string "Are you heading to Spikemuth?$"

GalarTrn_G14M11_o45_Derrota:
	.string "Crash and burn!$"

GalarTrn_G14M11_o9::
	trainerbattle_single TRAINER_GALAR_KINDRA_479, GalarTrn_G14M11_o9_Intro, GalarTrn_G14M11_o9_Derrota
	msgbox GalarTrn_Depois_GUITARIST, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M11_o9_Intro:
	.string "I just got some Pokémon in trades.\p"
	.string "Can I try them out on you?$"

GalarTrn_G14M11_o9_Derrota:
	.string "That isn't good enough!$"

@ ---- Galar_Route1001 ----
GalarTrn_G03M28_o6::
	trainerbattle_single TRAINER_GALAR_GLENN_277, GalarTrn_G03M28_o6_Intro, GalarTrn_G03M28_o6_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M28_o6_Intro:
	.string "Swimming is great!\n"
	.string "But not on ice!$"

GalarTrn_G03M28_o6_Derrota:
	.string "Shocking!$"

GalarTrn_G03M28_o7::
	trainerbattle_single TRAINER_GALAR_GILLI_E_CAM_278, GalarTrn_G03M28_o7_Intro, GalarTrn_G03M28_o7_Derrota
	msgbox GalarTrn_Depois_INTERVIEWER, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M28_o7_Intro:
	.string "How about an interview?$"

GalarTrn_G03M28_o7_Derrota:
	.string "that should do it!$"

GalarTrn_G03M28_o8::
	trainerbattle_single TRAINER_GALAR_GILLI_E_CAM_278_2, GalarTrn_G03M28_o8_Intro, GalarTrn_G03M28_o8_Derrota
	msgbox GalarTrn_Depois_INTERVIEWER, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M28_o8_Intro:
	.string "How about an interview?$"

GalarTrn_G03M28_o8_Derrota:
	.string "that should do it!$"

@ ---- Galar_Route1601 ----
GalarTrn_G10M23_o0::
	trainerbattle_single TRAINER_GALAR_EMILIA_452, GalarTrn_G10M23_o0_Intro, GalarTrn_G10M23_o0_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M23_o0_Intro:
	.string "I represent Allister!$"

GalarTrn_G10M23_o0_Derrota:
	.string "You beat me..$"

GalarTrn_G10M23_o1::
	trainerbattle_single TRAINER_GALAR_JENNIFER_453, GalarTrn_G10M23_o1_Intro, GalarTrn_G10M23_o1_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M23_o1_Intro:
	.string "I represent Allister!$"

GalarTrn_G10M23_o1_Derrota:
	.string "You beat me..$"

GalarTrn_G10M23_o2::
	trainerbattle_single TRAINER_GALAR_ANGELICA_451, GalarTrn_G10M23_o2_Intro, GalarTrn_G10M23_o2_Derrota
	msgbox GalarTrn_Depois_CHANNELER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M23_o2_Intro:
	.string "Let's battle.$"

GalarTrn_G10M23_o2_Derrota:
	.string "I lost.$"

@ ---- Galar_Route1603 ----
GalarTrn_G10M26_o0::
	trainerbattle_single TRAINER_GALAR_AARON_320, GalarTrn_G10M26_o0_Intro, GalarTrn_G10M26_o0_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M26_o0_Intro:
	.string "Hiyah!\nI have no fear for anything tough!\pI shatter boulders for training\nevery day!$"

GalarTrn_G10M26_o0_Derrota:
	.string "Yow!\nStubbed fingers!$"

GalarTrn_G10M26_o1::
	trainerbattle_single TRAINER_GALAR_HIDEKI_319, GalarTrn_G10M26_o1_Intro, GalarTrn_G10M26_o1_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M26_o1_Intro:
	.string "I hear you’re good!\nShow me!$"

GalarTrn_G10M26_o1_Derrota:
	.string "Judge!\nOne point!$"

GalarTrn_G10M26_o2::
	trainerbattle_single TRAINER_GALAR_HITOSHI_321, GalarTrn_G10M26_o2_Intro, GalarTrn_G10M26_o2_Derrota
	msgbox GalarTrn_Depois_BLACK_BELT_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M26_o2_Intro:
	.string "Hwaah!\pYou’re trespassing in our\nFighting Dojo!$"

GalarTrn_G10M26_o2_Derrota:
	.string "Oof!\nI give up!$"

@ ---- Galar_Spikemuth07 ----
GalarTrn_G14M10_o0::
	trainerbattle_single TRAINER_GALAR_GRUNT_391_2, GalarTrn_G14M10_o0_Intro, GalarTrn_G14M10_o0_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o0_Intro:
	.string "Children aren't allowed in here!$"

GalarTrn_G14M10_o0_Derrota:
	.string "Tough!$"

GalarTrn_G14M10_o1::
	trainerbattle_single TRAINER_GALAR_GRUNT_390_2, GalarTrn_G14M10_o1_Intro, GalarTrn_G14M10_o1_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o1_Intro:
	.string "I'm sorry about this, but I can't let you\n"
	.string "through!$"

GalarTrn_G14M10_o1_Derrota:
	.string "I messed up!$"

GalarTrn_G14M10_o10::
	trainerbattle_single TRAINER_GALAR_PIERS_419, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G14M10_o10_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o10_Derrota:
	.string "My team and I did what we could. Let's\n"
	.string "meet up and battle again sometime...$"

GalarTrn_G14M10_o14::
	trainerbattle_single TRAINER_GALAR_MARNIE_165, GalarTrn_Intro_RIVAL, GalarTrn_G14M10_o14_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o14_Derrota:
	.string "You won!$"

GalarTrn_G14M10_o2::
	trainerbattle_single TRAINER_GALAR_GRUNT_375_2, GalarTrn_G14M10_o2_Intro, GalarTrn_G14M10_o2_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o2_Intro:
	.string "Stop playing around with us, kid!$"

GalarTrn_G14M10_o2_Derrota:
	.string "I give up!$"

GalarTrn_G14M10_o3::
	trainerbattle_single TRAINER_GALAR_GRUNT_379_2, GalarTrn_G14M10_o3_Intro, GalarTrn_G14M10_o3_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o3_Intro:
	.string "Show some respect for Team Yell!$"

GalarTrn_G14M10_o3_Derrota:
	.string "Cough…\nCough…$"

GalarTrn_G14M10_o4::
	trainerbattle_single TRAINER_GALAR_GRUNT_378_2, GalarTrn_G14M10_o4_Intro, GalarTrn_G14M10_o4_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G14M10_o4_Intro:
	.string "I heard a child was wandering around\n"
	.string "here.$"

GalarTrn_G14M10_o4_Derrota:
	.string "Boom!$"

@ ---- Galar_Spikemuth09 ----
GalarTrn_G03M10_o0::
	trainerbattle_single TRAINER_GALAR_GRUNT_391, GalarTrn_G03M10_o0_Intro, GalarTrn_G03M10_o0_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M10_o0_Intro:
	.string "Children aren't allowed in here!$"

GalarTrn_G03M10_o0_Derrota:
	.string "Tough!$"

GalarTrn_G03M10_o1::
	trainerbattle_single TRAINER_GALAR_GRUNT_390, GalarTrn_G03M10_o1_Intro, GalarTrn_G03M10_o1_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M10_o1_Intro:
	.string "I'm sorry about this, but I can't let you\n"
	.string "through!$"

GalarTrn_G03M10_o1_Derrota:
	.string "I messed up!$"

GalarTrn_G03M10_o2::
	trainerbattle_single TRAINER_GALAR_GRUNT_375, GalarTrn_G03M10_o2_Intro, GalarTrn_G03M10_o2_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M10_o2_Intro:
	.string "Stop playing around with us, kid!$"

GalarTrn_G03M10_o2_Derrota:
	.string "I give up!$"

GalarTrn_G03M10_o3::
	trainerbattle_single TRAINER_GALAR_GRUNT_379, GalarTrn_G03M10_o3_Intro, GalarTrn_G03M10_o3_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M10_o3_Intro:
	.string "Show some respect for Team Yell!$"

GalarTrn_G03M10_o3_Derrota:
	.string "Cough…\nCough…$"

GalarTrn_G03M10_o4::
	trainerbattle_single TRAINER_GALAR_GRUNT_378, GalarTrn_G03M10_o4_Intro, GalarTrn_G03M10_o4_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M10_o4_Intro:
	.string "I heard a child was wandering around\n"
	.string "here.$"

GalarTrn_G03M10_o4_Derrota:
	.string "Boom!$"

@ ---- Galar_StowOnSide08 ----
GalarTrn_G10M21_o10::
	trainerbattle_single TRAINER_GALAR_HOP_429_3, GalarTrn_Intro_RIVAL, GalarTrn_G10M21_o10_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M21_o10_Derrota:
	.string "My strategy goes straight down the\n"
	.string "drain when I have all these bad\l"
	.string "thoughts running through my head. $"

GalarTrn_G10M21_o9::
	trainerbattle_single TRAINER_GALAR_HOP_429_4, GalarTrn_Intro_RIVAL, GalarTrn_G10M21_o9_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M21_o9_Derrota:
	.string "My strategy goes straight down the\n"
	.string "drain when I have all these bad\l"
	.string "thoughts running through my head. $"

@ ---- Galar_StowOnSide09 ----
GalarTrn_G10M25_o12::
	trainerbattle_single TRAINER_GALAR_ALLISTER_310, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G10M25_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M25_o12_Derrota:
	.string "I'm glad I have my mask... I was pulling\n"
	.string "quite a face just now ...$"

@ ---- Galar_StowOnSide10 ----
GalarTrn_G10M27_o12::
	trainerbattle_single TRAINER_GALAR_BEA_27, GalarTrn_G10M27_o12_Intro, GalarTrn_G10M27_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G10M27_o12_Intro:
	.string "Bea: Welcome, Challenger.\n"
	.string "I'm Bea.\p"
	.string "You have an unshakable spirit that will\n"
	.string "not be broken, no matter how you are\l"
	.string "attacked.\p"
	.string "I think I'll test that, shall I?$"

GalarTrn_G10M27_o12_Derrota:
	.string "Bea: Thank you for the battle. Phew...\n"
	.string "Facing you gave me all the explanation\l"
	.string "I needed.\p"
	.string "Fighting you and your team was not what\n"
	.string "I expected, but it made my heart dance.\p"
	.string "It's good to be unshakable in the face\n"
	.string "of battle. But it's also good to be\l"
	.string "carried away by it. Thank you again.$"

@ ---- Galar_Turffield05 ----
GalarTrn_G07M13_o2::
	trainerbattle_single TRAINER_GALAR_LASSA_114, GalarTrn_G07M13_o2_Intro, GalarTrn_G07M13_o2_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M13_o2_Intro:
	.string "I got up early every day to raise\nmy Pokémon from cocoons!$"

GalarTrn_G07M13_o2_Derrota:
	.string "What?\pWhat a total waste of time!$"

GalarTrn_G07M13_o4::
	trainerbattle_single TRAINER_GALAR_BRICE_186, GalarTrn_G07M13_o4_Intro, GalarTrn_G07M13_o4_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M13_o4_Intro:
	.string "Hahaha!\n"
	.string "You're not tough at all!!$"

GalarTrn_G07M13_o4_Derrota:
	.string "What is this?$"

GalarTrn_G07M13_o5::
	trainerbattle_single TRAINER_GALAR_ALICIA_154, GalarTrn_G07M13_o5_Intro, GalarTrn_G07M13_o5_Derrota
	msgbox GalarTrn_Depois_PICNICKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M13_o5_Intro:
	.string "You have Pokémon with you!\nYou’re mine!$"

GalarTrn_G07M13_o5_Derrota:
	.string "You deceived me…$"

GalarTrn_G07M13_o6::
	trainerbattle_single TRAINER_GALAR_ALAN_185, GalarTrn_G07M13_o6_Intro, GalarTrn_G07M13_o6_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M13_o6_Intro:
	.string "Hahahaha!\n"
	.string "Bring it on!$"

GalarTrn_G07M13_o6_Derrota:
	.string "Hahahaha!\n"
	.string "You beat me fair and square!$"

GalarTrn_G07M13_o7::
	trainerbattle_single TRAINER_GALAR_JEREMY_465, GalarTrn_G07M13_o7_Intro, GalarTrn_G07M13_o7_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M13_o7_Intro:
	.string "Bwahaha!\n"
	.string "Great! I was getting bored!$"

GalarTrn_G07M13_o7_Derrota:
	.string "Keep it up, huh!\p"
	.string "Oh, wait.\n"
	.string "I'm out of Pokémon!$"

@ ---- Galar_Turffield06 ----
GalarTrn_G07M14_o12::
	trainerbattle_single TRAINER_GALAR_MILO_304, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G07M14_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G07M14_o12_Derrota:
	.string "The power of Grass has withered...$"

@ ---- Galar_TurffieldIndoor01 ----
GalarTrn_G13M08_o12::
	trainerbattle_single TRAINER_GALAR_MARNIE_76, GalarTrn_G13M08_o12_Intro, GalarTrn_G13M08_o12_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M08_o12_Intro:
	.string "Marnie: Heh... I knew you'd be able to\n"
	.string "collect every Badge and meet me here.\p"
	.string "I also know a lot went on between the\n"
	.string "two of us, with my brother, with Team\l"
	.string "Yell, the help in Spikemuth and all the\l"
	.string "rest...\p"
	.string "But the truth is that when all is said\n"
	.string "and done... I really want to become the\l"
	.string "Champion on my own, so don't take it\l"
	.string "personally when I beat you!$"

GalarTrn_G13M08_o12_Derrota:
	.string "You beat me$"

@ ---- Galar_TurffieldIndoor02 ----
GalarTrn_G13M09_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_438, GalarTrn_G13M09_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_438, 0, GalarTrn_G13M09_o12_Derrota, GalarTrn_G13M09_o12_Vitoria
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M09_o12_Fim:
	release
	end

GalarTrn_G13M09_o12_Derrota:
	.string "let's fight$"

GalarTrn_G13M09_o12_Vitoria:
	.string "You crushed me…$"

@ ---- Galar_TurffieldIndoor04 ----
GalarTrn_G13M14_o12::
	trainerbattle_single TRAINER_GALAR_JON_299, GalarTrn_G13M14_o12_Intro, GalarTrn_G13M14_o12_Derrota
	msgbox GalarTrn_Depois_TAMER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M14_o12_Intro:
	.string "Twilight Wings was a good anime, wasn't\n"
	.string "it?\p"
	.string "I'm Jon. I finally got over my illness\n"
	.string "and now I'm a great Trainer!$"

GalarTrn_G13M14_o12_Derrota:
	.string "Wow, that was incredible!!!$"

@ ---- Galar_TurffieldIndoor05 ----
GalarTrn_G13M15_o12::
	trainerbattle_single TRAINER_GALAR_TOMMY_300, GalarTrn_G13M15_o12_Intro, GalarTrn_G13M15_o12_Derrota
	msgbox GalarTrn_Depois_HIKER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M15_o12_Intro:
	.string "I'm Tommy. I'm from the Twilight Wings\n"
	.string "anime, and now I'm going to win!!!$"

GalarTrn_G13M15_o12_Derrota:
	.string "Congratulations!$"

@ ---- Galar_TurffieldIndoor06 ----
GalarTrn_G13M16_o12::
	trainerbattle_single TRAINER_GALAR_ISADORA_22_2, GalarTrn_G13M16_o12_Intro, GalarTrn_G13M16_o12_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M16_o12_Intro:
	.string "Hello... My name is Isadora!\p"
	.string "And you'll have to battle me here and\n"
	.string "now!$"

GalarTrn_G13M16_o12_Derrota:
	.string "You managed to win by luck...$"

@ ---- Galar_TurffieldIndoor08 ----
GalarTrn_G13M19_o12::
	trainerbattle_single TRAINER_GALAR_LEON_739, GalarTrn_G13M19_o12_Intro, GalarTrn_G13M19_o12_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G13M19_o12_Intro:
	.string "Now that I have seen what kind of\n"
	.string "strength you have as the greatest of\l"
	.string "challengers... crushing you into the\l"
	.string "dirt will show everyone how strong your\l"
	.string "Champion really is!$"

GalarTrn_G13M19_o12_Derrota:
	.string "My time as Champion is over ...\n"
	.string "But what a time as Champion it has been!\p"
	.string "Thank you for the greatest battle I\n"
	.string "have ever had!$"

@ ---- Galar_TurffieldIndoor09 ----
GalarTrn_G35M08_o12::
	trainerbattle_single TRAINER_GALAR_ASH_402, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M08_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M08_o12_Derrota:
	.string "That was an incredible battle. Just\n"
	.string "wait, we'll battle again some other day!$"

@ ---- Galar_TurffieldIndoor10 ----
GalarTrn_G35M09_o12::
	trainerbattle_single TRAINER_GALAR_RED_403, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M09_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M09_o12_Derrota:
	.string ".... .... ....\n.... .... ....$"

@ ---- Galar_TurffieldIndoor11 ----
GalarTrn_G35M10_o12::
	trainerbattle_single TRAINER_GALAR_ETHAN_404, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M10_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M10_o12_Derrota:
	.string "Wow, I have to get better. After all, you\n"
	.string "never know when someone as strong as\l"
	.string "you will be standing in front of me\l"
	.string "again.$"

@ ---- Galar_TurffieldIndoor13 ----
GalarTrn_G35M12_o12::
	trainerbattle_single TRAINER_GALAR_MISTY_406, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G35M12_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M12_o12_Derrota:
	.string "WHAT! Don't think that was our last\n"
	.string "battle, I'll still have a rematch.$"

@ ---- Galar_TurffieldIndoor14 ----
GalarTrn_G35M13_o12::
	trainerbattle_single TRAINER_GALAR_GREEN_407, GalarTrn_Intro_COOLTRAINER_FRLG, GalarTrn_G35M13_o12_Derrota
	msgbox GalarTrn_Depois_COOLTRAINER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M13_o12_Derrota:
	.string "Well, well, it seems I underestimated\n"
	.string "you, but don't get so full of yourself\l"
	.string "just because you won once.$"

@ ---- Galar_TurffieldIndoor16 ----
GalarTrn_G35M15_o12::
	trainerbattle_single TRAINER_GALAR_HILDA_409, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M15_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M15_o12_Derrota:
	.string "My goodness, INCREDIBLE, getting the\n"
	.string "chance to battle Trainers like you is\l"
	.string "really exciting!$"

@ ---- Galar_TurffieldIndoor17 ----
GalarTrn_G35M16_o12::
	trainerbattle_single TRAINER_GALAR_SERENA_421, GalarTrn_Intro_BEAUTY_FRLG, GalarTrn_G35M16_o12_Derrota
	msgbox GalarTrn_Depois_BEAUTY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M16_o12_Derrota:
	.string "Oh... you're really strong. All that's\n"
	.string "left for me now is to root for your\l"
	.string "victory.$"

@ ---- Galar_TurffieldIndoor18 ----
GalarTrn_G35M17_o12::
	trainerbattle_single TRAINER_GALAR_BROCK_422, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G35M17_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M17_o12_Derrota:
	.string "...\p"
	.string "...\p"
	.string "That was a great battle. I hope we have\n"
	.string "another one someday.$"

@ ---- Galar_TurffieldIndoor19 ----
GalarTrn_G35M18_o12::
	trainerbattle_single TRAINER_GALAR_CYNTHIA_423, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M18_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M18_o12_Derrota:
	.string "So you're the current Champion of Galar.\n"
	.string "Champion to Champion, I can say that\l"
	.string "was one of the best battles I have ever\l"
	.string "had.$"

@ ---- Galar_TurffieldIndoor20 ----
GalarTrn_G35M19_o12::
	trainerbattle_single TRAINER_GALAR_IRIS_424, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M19_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M19_o12_Derrota:
	.string "NO, NO, NO!!!\p"
	.string "I was expecting an incredible victory\n"
	.string "today, but it was supposed to be mine!!!$"

@ ---- Galar_TurffieldIndoor21 ----
GalarTrn_G35M20_o12::
	trainerbattle_single TRAINER_GALAR_HILBERT_425, GalarTrn_Intro_GENTLEMAN_FRLG, GalarTrn_G35M20_o12_Derrota
	msgbox GalarTrn_Depois_GENTLEMAN_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M20_o12_Derrota:
	.string "Wow, that was unexpected, but don't\n"
	.string "think it ends here. I still have time for\l"
	.string "another battle against you.$"

@ ---- Galar_TurffieldIndoor22 ----
GalarTrn_G35M21_o12::
	trainerbattle_single TRAINER_GALAR_ALAN_466, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M21_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M21_o12_Derrota:
	.string "Hmmm... not bad, but just wait, one day\n"
	.string "I'll be strong enough for another\l"
	.string "battle.$"

@ ---- Galar_TurffieldIndoor23 ----
GalarTrn_G35M22_o12::
	trainerbattle_single TRAINER_GALAR_FELIPEMX_467, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M22_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M22_o12_Derrota:
	.string "I wonder if it was wrong to break the\n"
	.string "fourth wall at the start of my lines?$"

@ ---- Galar_TurffieldIndoor24 ----
GalarTrn_G35M23_o12::
	trainerbattle_single TRAINER_GALAR_MAY_471, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M23_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M23_o12_Derrota:
	.string "Amazing, Trainers like you are hard to\n"
	.string "come by. I hope to see you again.$"

@ ---- Galar_TurffieldIndoor25 ----
GalarTrn_G35M24_o12::
	trainerbattle_single TRAINER_GALAR_BRENDAN_472, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M24_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M24_o12_Derrota:
	.string "Wow, that was...$"

@ ---- Galar_TurffieldIndoor26 ----
GalarTrn_G35M25_o12::
	trainerbattle_single TRAINER_GALAR_DAWN_473, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M25_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M25_o12_Derrota:
	.string "OH.... I wasn't expecting that. I still\n"
	.string "have a lot to learn.$"

@ ---- Galar_TurffieldIndoor27 ----
GalarTrn_G35M26_o12::
	trainerbattle_single TRAINER_GALAR_STEVEN_485, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M26_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M26_o12_Derrota:
	.string "Very good, that was a great battle. May\n"
	.string "we have another one just like it\l"
	.string "someday.$"

@ ---- Galar_TurffieldIndoor28 ----
GalarTrn_G35M27_o12::
	trainerbattle_single TRAINER_GALAR_LANCE_486, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G35M27_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G35M27_o12_Derrota:
	.string "A worthy victory for a worthy Trainer.\n"
	.string "My congratulations, lad.$"

@ ---- Galar_TurffieldIndoor29 ----
GalarTrn_G36M05_o12::
	trainerbattle_single TRAINER_GALAR_PEONY_343_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M05_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M05_o12_Derrota:
	.string "This time I won't hide my face. I just\n"
	.string "hope my daughter is still proud of me…$"

@ ---- Galar_TurffieldIndoor30 ----
GalarTrn_G36M06_o12::
	trainerbattle_single TRAINER_GALAR_RAIHAN_338, GalarTrn_Intro_ELITE_FOUR_FRLG, GalarTrn_G36M06_o12_Derrota
	msgbox GalarTrn_Depois_ELITE_FOUR_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M06_o12_Derrota:
	.string "I look good even when I lose. It's a real\n"
	.string "curse.\p"
	.string "I think it's time for another selfie!$"

@ ---- Galar_TurffieldIndoor31 ----
GalarTrn_G36M07_o12::
	trainerbattle_single TRAINER_GALAR_AVERY_341, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M07_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M07_o12_Derrota:
	.string "And so you climb toward victory, leaving\n"
	.string "us behind.\p"
	.string "That irritates me, but... bravo.$"

@ ---- Galar_TurffieldIndoor32 ----
GalarTrn_G36M08_o12::
	trainerbattle_single TRAINER_GALAR_MELONY_336_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M08_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M08_o12_Derrota:
	.string "I think you took breaking the ice a\n"
	.string "little too literally ...$"

@ ---- Galar_TurffieldIndoor33 ----
GalarTrn_G36M09_o12::
	trainerbattle_single TRAINER_GALAR_GORDIE_339, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M09_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M09_o12_Derrota:
	.string "I was crushed! I'm proud of my solid\n"
	.string "Pokémon, and even so…$"

@ ---- Galar_TurffieldIndoor34 ----
GalarTrn_G36M10_o12::
	trainerbattle_single TRAINER_GALAR_LUCAS_347, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M10_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M10_o12_Derrota:
	.string "my effort here was more useless than\n"
	.string "trying to evolve a male Combee.$"

@ ---- Galar_TurffieldIndoor35 ----
GalarTrn_G36M11_o12::
	trainerbattle_single TRAINER_GALAR_NESSA_307_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M11_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M11_o12_Derrota:
	.string "I don't get it.\p"
	.string "What do I have to do to beat you, huh?$"

@ ---- Galar_TurffieldIndoor36 ----
GalarTrn_G36M12_o12::
	trainerbattle_single TRAINER_GALAR_PIERS_337, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M12_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M12_o12_Derrota:
	.string "is that it?! Piers doesn't do encores,\n"
	.string "but I admit I'm tempted now!$"

@ ---- Galar_TurffieldIndoor37 ----
GalarTrn_G36M13_o12::
	trainerbattle_single TRAINER_GALAR_MILO_304_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M13_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M13_o12_Derrota:
	.string "The power of Grass has withered...$"

@ ---- Galar_TurffieldIndoor38 ----
GalarTrn_G36M14_o12::
	trainerbattle_single TRAINER_GALAR_VANESSA_348, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M14_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M14_o12_Derrota:
	.string "I so want to fly far away...$"

@ ---- Galar_TurffieldIndoor39 ----
GalarTrn_G36M15_o12::
	trainerbattle_single TRAINER_GALAR_KABU_308_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M15_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M15_o12_Derrota:
	.string "Good Pokémon and a great Trainer!\p"
	.string "It's no surprise that you won!$"

@ ---- Galar_TurffieldIndoor40 ----
GalarTrn_G36M16_o12::
	trainerbattle_single TRAINER_GALAR_ALLISTER_310_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M16_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M16_o12_Derrota:
	.string "I'm glad I have my mask... I was pulling\n"
	.string "quite a face just now ...$"

@ ---- Galar_TurffieldIndoor41 ----
GalarTrn_G36M17_o12::
	trainerbattle_single TRAINER_GALAR_BEDE_312_2, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M17_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M17_o12_Derrota:
	.string "Why did I have the misfortune of being\n"
	.string "born at the same time as you?$"

@ ---- Galar_TurffieldIndoor42 ----
GalarTrn_G36M18_o12::
	trainerbattle_single TRAINER_GALAR_C_PHENE_349, GalarTrn_Intro_BOSS_FRLG, GalarTrn_G36M18_o12_Derrota
	msgbox GalarTrn_Depois_BOSS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M18_o12_Derrota:
	.string "looks like I'm the one who got buried...$"

@ ---- Galar_TurffieldIndoor43 ----
GalarTrn_G36M19_o12::
	trainerbattle_single TRAINER_GALAR_ALLANA_345, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M19_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M19_o12_Derrota:
	.string "Ha... darn, I thought this was going to\n"
	.string "be easy...$"

@ ---- Galar_TurffieldIndoor44 ----
GalarTrn_G36M20_o12::
	trainerbattle_single TRAINER_GALAR_BEA_311, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M20_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M20_o12_Derrota:
	.string "Your Pokémon... they're so strong\n"
	.string "they're practically dizzying!$"

@ ---- Galar_TurffieldIndoor45 ----
GalarTrn_G36M21_o12::
	trainerbattle_single TRAINER_GALAR_MARNIE_344, GalarTrn_Intro_RIVAL, GalarTrn_G36M21_o12_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M21_o12_Derrota:
	.string "I've been losing to you ever since the\n"
	.string "Gym Challenge, and I'm getting a bit fed\l"
	.string "up!\p"
	.string "You had better battle me again.$"

@ ---- Galar_TurffieldIndoor46 ----
GalarTrn_G36M22_o12::
	trainerbattle_single TRAINER_GALAR_ALEXANDER_346, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M22_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M22_o12_Derrota:
	.string "How embarrassing to lose like that. I\n"
	.string "think I'll stop by Spikemuth.$"

@ ---- Galar_TurffieldIndoor47 ----
GalarTrn_G36M23_o12::
	trainerbattle_single TRAINER_GALAR_MUSTARD_342, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G36M23_o12_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M23_o12_Derrota:
	.string "Fuhaha! I held absolutely nothing back,\n"
	.string "and you still beat me!\p"
	.string "The apprentice surpasses the master ...\p"
	.string "A truly proud moment for the master!$"

@ ---- Galar_TurffieldIndoor48 ----
GalarTrn_G36M24_o12::
	trainerbattle_single TRAINER_GALAR_KLARA_340, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G36M24_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G36M24_o12_Derrota:
	.string "Wow, strong as ever!\p"
	.string "But I think I'm starting to\n"
	.string "understand... Hey, thanks for helping\l"
	.string "me.$"

@ ---- Galar_TurffieldIndoor49 ----
GalarTrn_G39M01_o12::
	trainerbattle_single TRAINER_GALAR_GREG_106, GalarTrn_Intro_YOUNGSTER_FRLG, GalarTrn_G39M01_o12_Derrota
	msgbox GalarTrn_Depois_YOUNGSTER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M01_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor50 ----
GalarTrn_G39M02_o12::
	trainerbattle_single TRAINER_GALAR_CHAD_509, GalarTrn_Intro_YOUNGSTER_FRLG, GalarTrn_G39M02_o12_Derrota
	msgbox GalarTrn_Depois_YOUNGSTER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M02_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor51 ----
GalarTrn_G39M03_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LEON_736, GalarTrn_G39M03_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_LEON_736, 0, GalarTrn_G39M03_o12_Derrota, GalarTrn_G39M03_o12_Vitoria
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M03_o12_Fim:
	release
	end

GalarTrn_G39M03_o12_Derrota:
	.string "as I told you before ... There truly are\n"
	.string "no limits when it comes to Pokémon!\p"
	.string "We're all going to have a champion time!$"

GalarTrn_G39M03_o12_Vitoria:
	.string "Come on, remember our final match! Is\n"
	.string "this really the best you can do?!$"

@ ---- Galar_TurffieldIndoor52 ----
GalarTrn_G39M04_o12::
	trainerbattle_single TRAINER_GALAR_KAYSER_113, GalarTrn_Intro_SCHOOL_KID, GalarTrn_G39M04_o12_Derrota
	msgbox GalarTrn_Depois_SCHOOL_KID, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M04_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor53 ----
GalarTrn_G39M05_o12::
	trainerbattle_single TRAINER_GALAR_CONNER_115, GalarTrn_Intro_BUG_CATCHER_FRLG, GalarTrn_G39M05_o12_Derrota
	msgbox GalarTrn_Depois_BUG_CATCHER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M05_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor54 ----
GalarTrn_G39M06_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_733, GalarTrn_G39M06_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_733, 0, GalarTrn_G39M06_o12_Derrota, GalarTrn_G39M06_o12_Vitoria
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M06_o12_Fim:
	release
	end

GalarTrn_G39M06_o12_Derrota:
	.string "Ugh! Gutted! You're always one step\n"
	.string "ahead of me, mate!$"

GalarTrn_G39M06_o12_Vitoria:
	.string "Even the pages that detail my defeats\n"
	.string "will add to the story of my brilliant\l"
	.string "legend!\p"
	.string "But I don't intend to lose to you again!\p"
	.string "As your rival, I promise I'll win next\n"
	.string "time!\p"
	.string "Now, {PLAYER}, go to the Hall of Fame.\n"
	.string "Leon will go with you!$"

@ ---- Galar_TurffieldIndoor55 ----
GalarTrn_G39M07_o12::
	trainerbattle_single TRAINER_GALAR_ALEX_124, GalarTrn_Intro_SCIENTIST_FRLG, GalarTrn_G39M07_o12_Derrota
	msgbox GalarTrn_Depois_SCIENTIST_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M07_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor56 ----
GalarTrn_G39M08_o12::
	trainerbattle_single TRAINER_GALAR_LIAM_142, GalarTrn_Intro_CAMPER_FRLG, GalarTrn_G39M08_o12_Derrota
	msgbox GalarTrn_Depois_CAMPER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M08_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor57 ----
GalarTrn_G39M09_o12::
	trainerbattle_single TRAINER_GALAR_BEDE_147, GalarTrn_Intro_RIVAL, GalarTrn_G39M09_o12_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M09_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor58 ----
GalarTrn_G39M10_o12::
	trainerbattle_single TRAINER_GALAR_MARKA_162, GalarTrn_Intro_GUITARIST, GalarTrn_G39M10_o12_Derrota
	msgbox GalarTrn_Depois_GUITARIST, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M10_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor60 ----
GalarTrn_G39M12_o12::
	trainerbattle_single TRAINER_GALAR_MARNIE_165_2, GalarTrn_Intro_RIVAL, GalarTrn_G39M12_o12_Derrota
	msgbox GalarTrn_Depois_RIVAL, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M12_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor61 ----
GalarTrn_G39M13_o12::
	trainerbattle_single TRAINER_GALAR_WINSTON_166, GalarTrn_Intro_GUITARIST, GalarTrn_G39M13_o12_Derrota
	msgbox GalarTrn_Depois_GUITARIST, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M13_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor62 ----
GalarTrn_G39M14_o12::
	trainerbattle_single TRAINER_GALAR_DAWSON_167, GalarTrn_Intro_GUITARIST, GalarTrn_G39M14_o12_Derrota
	msgbox GalarTrn_Depois_GUITARIST, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M14_o12_Derrota:
	.string "You won!$"

@ ---- Galar_TurffieldIndoor63 ----
GalarTrn_G39M15_o12::
	trainerbattle_single TRAINER_GALAR_RAIHAN_168, GalarTrn_Intro_LEADER_FRLG, GalarTrn_G39M15_o12_Derrota
	msgbox GalarTrn_Depois_LEADER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M15_o12_Derrota:
	.string "You won!$"

@ ---- Galar_Wedgehurst08 ----
GalarTrn_G05M16_o7::
	trainerbattle_single TRAINER_GALAR_ARTHUR_23, GalarTrn_Intro_COOLTRAINER_FRLG, GalarTrn_G05M16_o7_Derrota
	msgbox GalarTrn_Depois_COOLTRAINER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G05M16_o7_Derrota:
	.string "Wow!$"

@ ---- Galar_WildArea11 ----
GalarTrn_G42M04_o2::
	trainerbattle_single TRAINER_GALAR_LEROY_599, GalarTrn_G42M04_o2_Intro, GalarTrn_G42M04_o2_Derrota
	msgbox GalarTrn_Depois_COOLTRAINER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M04_o2_Intro:
	.string "You look strong.\nLet me battle you, please!$"

GalarTrn_G42M04_o2_Derrota:
	.string "I knew it!\nYou’re as tough as I thought!$"

GalarTrn_G42M04_o3::
	trainerbattle_single TRAINER_GALAR_NICOLAS_521_2, GalarTrn_G42M04_o3_Intro, GalarTrn_G42M04_o3_Derrota
	msgbox GalarTrn_Depois_PKMN_RANGER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M04_o3_Intro:
	.string "This island is too spread out…\nIt’s not easy patrolling the place.$"

GalarTrn_G42M04_o3_Derrota:
	.string "Uh-huh…$"

@ ---- Galar_WildArea13 ----
GalarTrn_G42M06_o5::
	trainerbattle_single TRAINER_GALAR_MASON_590, GalarTrn_G42M06_o5_Intro, GalarTrn_G42M06_o5_Derrota
	msgbox GalarTrn_Depois_JUGGLER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M06_o5_Intro:
	.string "Howdy!\nAre you a member of my fan club?$"

GalarTrn_G42M06_o5_Derrota:
	.string "Oh, so you’re not a fan…\pWell, I can change that.\nLet me sing for you!$"

@ ---- Galar_WildArea14 ----
GalarTrn_G42M07_o0::
	trainerbattle_single TRAINER_GALAR_CYNDY_591, GalarTrn_G42M07_o0_Intro, GalarTrn_G42M07_o0_Derrota
	msgbox GalarTrn_Depois_CRUSH_GIRL_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M07_o0_Intro:
	.string "My conditioning’s in top form!$"

GalarTrn_G42M07_o0_Derrota:
	.string "Huh?\nSomething’s not right…$"

GalarTrn_G42M07_o1::
	trainerbattle_single TRAINER_GALAR_EVAN_593, GalarTrn_G42M07_o1_Intro, GalarTrn_G42M07_o1_Derrota
	msgbox GalarTrn_Depois_TAMER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M07_o1_Intro:
	.string "It doesn’t matter if you happen to\nhave the strongest Pokémon…\pIt doesn’t mean a thing if you don’t\nknow how to use them properly!$"

GalarTrn_G42M07_o1_Derrota:
	.string "You’re a master at this.$"

GalarTrn_G42M07_o3::
	trainerbattle_single TRAINER_GALAR_KATELYN_598, GalarTrn_G42M07_o3_Intro, GalarTrn_G42M07_o3_Derrota
	msgbox GalarTrn_Depois_PKMN_RANGER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M07_o3_Intro:
	.string "Those shoes you have are pretty\nsnazzy.$"

GalarTrn_G42M07_o3_Derrota:
	.string "You’re hot stuff in spite of your\ncute looks.$"

GalarTrn_G42M07_o6::
	trainerbattle_double TRAINER_GALAR_LEX_NYA_601, GalarTrn_G42M07_o6_Intro, GalarTrn_G42M07_o6_Derrota, GalarTrn_G42M07_o6_Poucos
	msgbox GalarTrn_Depois_COOL_COUPLE_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M07_o6_Intro:
	.string "Lex: My darling Nya, together\nwe could win!$"

GalarTrn_G42M07_o6_Derrota:
	.string "Lex: I seem to have been too\ncareless…$"

GalarTrn_G42M07_o6_Poucos:
	.string "Lex: May I ask you to battle the\nboth of us at the same time?$"

GalarTrn_G42M07_o7::
	trainerbattle_double TRAINER_GALAR_LEX_NYA_601_2, GalarTrn_G42M07_o7_Intro, GalarTrn_G42M07_o7_Derrota, GalarTrn_G42M07_o7_Poucos
	msgbox GalarTrn_Depois_COOL_COUPLE_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M07_o7_Intro:
	.string "Nya: I’ll do my best so I won’t\ndrag down my mentor, Lex!$"

GalarTrn_G42M07_o7_Derrota:
	.string "Nya: Oh, no…\nI’m so sorry, I…$"

GalarTrn_G42M07_o7_Poucos:
	.string "Nya: I’m sorry, but may we battle\nin two-on-two style?$"

@ ---- Galar_WildArea17 ----
GalarTrn_G42M10_o17::
	trainerbattle_single TRAINER_GALAR_MIAH_588_2, GalarTrn_G42M10_o17_Intro, GalarTrn_G42M10_o17_Derrota
	msgbox GalarTrn_Depois_AROMA_LADY_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M10_o17_Intro:
	.string "Kyahaha!\nI’ll flick you away effortlessly!$"

GalarTrn_G42M10_o17_Derrota:
	.string "Tch!\nToo strong for me!$"

GalarTrn_G42M10_o6::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589_3, GalarTrn_G42M10_o6_Intro, GalarTrn_G42M10_o6_Derrota, GalarTrn_G42M10_o6_Poucos
	msgbox GalarTrn_Depois_YOUNG_COUPLE_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M10_o6_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G42M10_o6_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G42M10_o6_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

@ ---- Galar_WildArea21 ----
GalarTrn_G42M14_o3::
	trainerbattle_single TRAINER_GALAR_MADELINE_522_2, GalarTrn_G42M14_o3_Intro, GalarTrn_G42M14_o3_Derrota
	msgbox GalarTrn_Depois_PKMN_RANGER_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G42M14_o3_Intro:
	.string "I punish people who abuse\nPokémon!$"

GalarTrn_G42M14_o3_Derrota:
	.string "You don’t seem to be a problem\nTrainer.$"

@ ---- Galar_WildAreaIndoor01 ----
GalarTrn_G39M16_o0::
	trainerbattle_single TRAINER_GALAR_MARCELO_AF_351, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M16_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M16_o0_Derrota:
	.string "congratulations, you're the best\n"
	.string "Pokémon Trainer, keep it up$"

@ ---- Galar_Wyndon01 ----
GalarTrn_G03M09_o22::
	trainerbattle_single TRAINER_GALAR_ISADORA_22, GalarTrn_G03M09_o22_Intro, GalarTrn_G03M09_o22_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M09_o22_Intro:
	.string "Hello... My name is Isadora! And you'll\n"
	.string "have to battle me here and now!$"

GalarTrn_G03M09_o22_Derrota:
	.string "You managed to win by luck...$"

GalarTrn_G03M09_o7::
	trainerbattle_single TRAINER_GALAR_ERIC_77, GalarTrn_Intro_MAGMA_ADMIN, GalarTrn_G03M09_o7_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M09_o7_Derrota:
	.string "I will crush you!!!$"

GalarTrn_G03M09_o8::
	trainerbattle_single TRAINER_GALAR_FELIPE_78, GalarTrn_Intro_MAGMA_ADMIN, GalarTrn_G03M09_o8_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M09_o8_Derrota:
	.string "I will crush you!!!$"

GalarTrn_G03M09_o9::
	trainerbattle_single TRAINER_GALAR_VINICIUS_79, GalarTrn_Intro_MAGMA_ADMIN, GalarTrn_G03M09_o9_Derrota
	msgbox GalarTrn_Depois_MAGMA_ADMIN, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G03M09_o9_Derrota:
	.string "I will crush you!!!$"

@ ---- Galar_Wyndon06 ----
GalarTrn_G33M02_o4::
	trainerbattle_single TRAINER_GALAR_ISADORA_22_3, GalarTrn_G33M02_o4_Intro, GalarTrn_G33M02_o4_Derrota
	msgbox GalarTrn_Depois_LASS_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G33M02_o4_Intro:
	.string "Hello... My name is Isadora! And you'll\n"
	.string "have to battle me here and now!$"

GalarTrn_G33M02_o4_Derrota:
	.string "You managed to win by luck...$"

@ ---- Galar_Wyndon10 ----
GalarTrn_G39M27_o0::
	trainerbattle_single TRAINER_GALAR_KALEDK_360, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M27_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M27_o0_Derrota:
	.string "It seems you're stronger than I\n"
	.string "expected...$"

@ ---- Galar_WyndonIndoor01 ----
GalarTrn_G39M17_o0::
	trainerbattle_single TRAINER_GALAR_GOLD_GAM2_0_352, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M17_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M17_o0_Derrota:
	.string "That really was fabulous.\n"
	.string "Congratulations.$"

@ ---- Galar_WyndonIndoor02 ----
GalarTrn_G39M18_o0::
	trainerbattle_single TRAINER_GALAR_PEDRO_GA_13_353, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M18_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M18_o0_Derrota:
	.string "What have I lost. My defeat is a\n"
	.string "disgrace to Fairy-type Pokémon.$"

@ ---- Galar_WyndonIndoor03 ----
GalarTrn_G39M19_o0::
	trainerbattle_single TRAINER_GALAR_PERG_PIKACH_354, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M19_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M19_o0_Derrota:
	.string "Ask Pikachu: Wow, impressive. Your skills\n"
	.string "as a Pokémon Trainer aren't bad at all.\l"
	.string "Until another day!!$"

@ ---- Galar_WyndonIndoor04 ----
GalarTrn_G39M20_o0::
	trainerbattle_single TRAINER_GALAR_NEO_GIF_355, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M20_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M20_o0_Derrota:
	.string "Yeah, I underestimated you, but your\n"
	.string "win doesn't count if you used a save\l"
	.string "state.$"

@ ---- Galar_WyndonIndoor05 ----
GalarTrn_G39M21_o0::
	trainerbattle_single TRAINER_GALAR_FABIO_RODR_356, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M21_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M21_o0_Derrota:
	.string "Now I see how you beat the other\n"
	.string "members.$"

@ ---- Galar_WyndonIndoor06 ----
GalarTrn_G39M22_o0::
	trainerbattle_single TRAINER_GALAR_EDUARDO_357, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M22_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M22_o0_Derrota:
	.string "Wow... that was even relaxing. It had\n"
	.string "been a while since I had such a good\l"
	.string "battle.$"

@ ---- Galar_WyndonIndoor08 ----
GalarTrn_G39M24_o0::
	trainerbattle_single TRAINER_GALAR_PCL_G_50, GalarTrn_Intro_CHAMPION_FRLG, GalarTrn_G39M24_o0_Derrota
	msgbox GalarTrn_Depois_CHAMPION_FRLG, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M24_o0_Derrota:
	.string "Did you use a save state?\n"
	.string "How did you level up so much?\l"
	.string "Either way, congratulations!!!$"

@ ---- Galar_WyndonIndoor09 ----
GalarTrn_G39M26_o0::
	trainerbattle_single TRAINER_GALAR_BRENO_MENE_359, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M26_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M26_o0_Derrota:
	.string "Have you ever heard of my hack ROM\n"
	.string "Pokemon Naki?$"

@ ---- Galar_WyndonIndoor10 ----
GalarTrn_G39M28_o0::
	trainerbattle_single TRAINER_GALAR_DEIDARA_YT_361, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M28_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M28_o0_Derrota:
	.string "Congratulations!!!$"

@ ---- Galar_WyndonIndoor12 ----
GalarTrn_G39M30_o0::
	trainerbattle_single TRAINER_GALAR_CATZU_D_NE_363, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M30_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M30_o0_Derrota:
	.string "Gahahaha... You won this time, but next\n"
	.string "time you won't stand a chance.$"

@ ---- Galar_WyndonIndoor13 ----
GalarTrn_G39M31_o0::
	trainerbattle_single TRAINER_GALAR_BISCOITOMOL_364, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M31_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M31_o0_Derrota:
	.string "My biscuits are all squashed.$"

@ ---- Galar_WyndonIndoor14 ----
GalarTrn_G39M32_o0::
	trainerbattle_single TRAINER_GALAR_SASUKEZIN69_365, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M32_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M32_o0_Derrota:
	.string "Sasukezin69: wow, that battle hurt!$"

@ ---- Galar_WyndonIndoor16 ----
GalarTrn_G39M34_o0::
	trainerbattle_single TRAINER_GALAR_LORD_367, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M34_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M34_o0_Derrota:
	.string "Lord: Man, looks like I lost.$"

@ ---- Galar_WyndonIndoor17 ----
GalarTrn_G39M35_o0::
	trainerbattle_single TRAINER_GALAR_EURICO_368, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M35_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M35_o0_Derrota:
	.string "Eurico: Wow, what power!!!$"

@ ---- Galar_WyndonIndoor18 ----
GalarTrn_G39M36_o0::
	trainerbattle_single TRAINER_GALAR_CLOVES_369, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M36_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M36_o0_Derrota:
	.string "Cloves: Congratulations, Champion!$"

@ ---- Galar_WyndonIndoor19 ----
GalarTrn_G39M37_o0::
	trainerbattle_single TRAINER_GALAR_JUAN_GRSON_370, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M37_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M37_o0_Derrota:
	.string "Juan: Let's see you do it without using\n"
	.string "items!$"

@ ---- Galar_WyndonIndoor20 ----
GalarTrn_G39M38_o0::
	trainerbattle_single TRAINER_GALAR_CELINA_FER_371, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M38_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M38_o0_Derrota:
	.string "Celina: I admit it, I love Pikachu.$"

@ ---- Galar_WyndonIndoor21 ----
GalarTrn_G39M39_o0::
	trainerbattle_single TRAINER_GALAR_RUAN_POKE_372, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M39_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M39_o0_Derrota:
	.string "Ruan: Aw, man...$"

@ ---- Galar_WyndonIndoor22 ----
GalarTrn_G39M40_o0::
	trainerbattle_single TRAINER_GALAR_PLANETA_POK_374, GalarTrn_Intro_TEAM_AQUA, GalarTrn_G39M40_o0_Derrota
	msgbox GalarTrn_Depois_TEAM_AQUA, MSGBOX_AUTOCLOSE
	release
	end

GalarTrn_G39M40_o0_Derrota:
	.string "Planeta P.: Wow, congratulations to you!$"

