Route212_North_MapScripts::
	.byte 0

Route212_North_EventScript_RichBoy::
	msgbox Route212_North_Text_RichBoy, MSGBOX_NPC
	end

Route212_North_EventScript_Lady::
	msgbox Route212_North_Text_Lady, MSGBOX_NPC
	end

Route212_North_EventScript_Youngster::
	msgbox Route212_North_Text_Youngster, MSGBOX_NPC
	end

Route212_North_EventScript_Collector::
	msgbox Route212_North_Text_Collector, MSGBOX_NPC
	end

Route212_North_Text_RichBoy:
	.string "This road leads straight to\n"
	.string "Hearthome City. Nice, huh?$"

Route212_North_Text_Lady:
	.string "I love strolling this path\n"
	.string "in the afternoon.$"

Route212_North_Text_Youngster:
	.string "I'm gonna be a great Trainer\n"
	.string "someday, just you watch!$"

Route212_North_Text_Collector:
	.string "I collect Shards along this\n"
	.string "route. Found a few already.$"

Route212_North_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_RICH_BOY_JASON, Route212_North_Text_Trainer1Intro, Route212_North_Text_Trainer1Defeat
	msgbox Route212_North_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer1Intro:
	.string "My Pokémon sleeps in a bed I got from\n"
	.string "overseas.\pI'm very well off, if you haven't\n"
	.string "noticed!$"

Route212_North_Text_Trainer1Defeat:
	.string "What? Over already?\n"
	.string "Well, that's fine.\pRich people like me don't fight.$"

Route212_North_Text_Trainer1Post:
	.string "Oh, no.\n"
	.string "My Pokémon is worn out.\pI'd better let it sleep it off in the\n"
	.string "bed I had sent from overseas.$"

Route212_North_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_LADY_MELISSA, Route212_North_Text_Trainer2Intro, Route212_North_Text_Trainer2Defeat
	msgbox Route212_North_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer2Intro:
	.string "I'd like to begin now.\n"
	.string "Are you quite prepared?$"

Route212_North_Text_Trainer2Defeat:
	.string "Oh!\n"
	.string "How terrible of you...$"

Route212_North_Text_Trainer2Post:
	.string "You... You must have one fantastic\n"
	.string "teacher to be so good.$"

Route212_North_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_GENTLEMAN_JEREMY, Route212_North_Text_Trainer3Intro, Route212_North_Text_Trainer3Defeat
	msgbox Route212_North_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer3Intro:
	.string "If it pleases you, may I challenge you\n"
	.string "to a battle?$"

Route212_North_Text_Trainer3Defeat:
	.string "Bravo! Your technique is impeccable\n"
	.string "for someone so young.$"

Route212_North_Text_Trainer3Post:
	.string "Hahaha! I was invited by the master of\n"
	.string "the Pokémon Mansion.\pHe's promised to show me through\n"
	.string "his prized garden of Pokémon.$"

Route212_North_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_SOCIALITE_REINA, Route212_North_Text_Trainer4Intro, Route212_North_Text_Trainer4Defeat
	msgbox Route212_North_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer4Intro:
	.string "I've never battled a young Trainer like\n"
	.string "yourself. It's quite nerve wracking.$"

Route212_North_Text_Trainer4Defeat:
	.string "Oh, dear... That wasn't anything like\n"
	.string "battling with my friends.$"

Route212_North_Text_Trainer4Post:
	.string "Usually, I'll have matches with\n"
	.string "members of my social club.$"

Route212_North_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_POLICEMAN_BOBBY, Route212_North_Text_Trainer5Intro, Route212_North_Text_Trainer5Defeat
	msgbox Route212_North_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer5Intro:
	.string "Hold it right there, citizen!\n"
	.string "Walking around at night is unsafe!$"

Route212_North_Text_Trainer5Defeat:
	.string "You've got tough partners with you.\n"
	.string "Carry on, citizen. Carry on.$"

Route212_North_Text_Trainer5Post:
	.string "Out so late? Does your mother\n"
	.string "know you're out so late?$"

Route212_North_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_POLICEMAN_ALEX, Route212_North_Text_Trainer6Intro, Route212_North_Text_Trainer6Defeat
	msgbox Route212_North_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer6Intro:
	.string "I'm keeping my eyes open for crime.\n"
	.string "Anyone arousing suspicion here?$"

Route212_North_Text_Trainer6Defeat:
	.string "Now, just hold on. I didn't say that\n"
	.string "you were shady looking!$"

Route212_North_Text_Trainer6Post:
	.string "Don't go hanging out with any\n"
	.string "shady-looking characters! You hear?$"

Route212_North_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_POLICEMAN_DYLAN, Route212_North_Text_Trainer7Intro, Route212_North_Text_Trainer7Defeat
	msgbox Route212_North_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer7Intro:
	.string "Let's enjoy a fierce battle in the\n"
	.string "chilly night winds! Brrrr! Refreshing!$"

Route212_North_Text_Trainer7Defeat:
	.string "I need to explain, all right?\n"
	.string "It was too dark and hard to see.$"

Route212_North_Text_Trainer7Post:
	.string "Oops, I'd better get back to my\n"
	.string "beat before the boss radios me...$"

Route212_North_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_POLICEMAN_CALEB, Route212_North_Text_Trainer8Intro, Route212_North_Text_Trainer8Defeat
	msgbox Route212_North_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route212_North_Text_Trainer8Intro:
	.string "Whether there are problems or not, or\n"
	.string "if crimes have been committed or not,\pI still go out on patrol.$"

Route212_North_Text_Trainer8Defeat:
	.string "Big trouble! Officer in need\n"
	.string "of assistance!$"

Route212_North_Text_Trainer8Post:
	.string "Your toughness is too much!\n"
	.string "I'm in serious trouble!$"
