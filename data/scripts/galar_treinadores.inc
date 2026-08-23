@ Treinadores de Galar, balde d da fase de conteudo.
@ Gerado por dev_scripts/treinadores_galar.py; NAO editar a mao.
@ Uma batalha por objeto: a PRIMEIRA de um percurso linear.

@ ---- Galar_Ballonlea06 ----
GalarTrn_G11M11_o11::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BEDE_312, GalarTrn_G11M11_o11_Fim
	trainerbattle_no_intro TRAINER_GALAR_BEDE_312, GalarTrn_G11M11_o11_Derrota
	end

GalarTrn_G11M11_o11_Fim:
	release
	end

GalarTrn_G11M11_o11_Derrota:
	.string "Por que eu tive a infelicidade\nde nascer na mesma época que você?$"

GalarTrn_G11M11_o12::
	trainerbattle_single TRAINER_GALAR_OPAL_418, GalarTrn_G11M11_o12_Intro, GalarTrn_G11M11_o12_Derrota
	end

GalarTrn_G11M11_o12_Intro:
	.string "Opal:Suponho que seja um pouco\ntarde para me apresentar,mas...eu\lsou Opal,a lider do ginásio.Eu\ldei uma boa olhada em como você\llidou com esses testes.\lA última parte da missäo sou eu...\lDeixe-me ver como você e seu\lparceiro pokémon se comportam!$"

GalarTrn_G11M11_o12_Derrota:
	.string "Ainda falta rosa em você,mas\nvocê é um excelente treinador\lcom alguns bons pokémons.$"

@ ---- Galar_Circhester03 ----
GalarTrn_G12M00_bg10::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg10_Fim
	trainerbattle_no_intro TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg10_Derrota
	end

GalarTrn_G12M00_bg10_Fim:
	release
	end

GalarTrn_G12M00_bg10_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_bg11::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg11_Fim
	trainerbattle_no_intro TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_bg11_Derrota
	end

GalarTrn_G12M00_bg11_Fim:
	release
	end

GalarTrn_G12M00_bg11_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_bg12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg12_Fim
	trainerbattle_no_intro TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg12_Derrota
	end

GalarTrn_G12M00_bg12_Fim:
	release
	end

GalarTrn_G12M00_bg12_Derrota:
	.string "Oh!$"

GalarTrn_G12M00_bg13::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg13_Fim
	trainerbattle_no_intro TRAINER_GALAR_LANA_180, GalarTrn_G12M00_bg13_Derrota
	end

GalarTrn_G12M00_bg13_Fim:
	release
	end

GalarTrn_G12M00_bg13_Derrota:
	.string "Oh!$"

GalarTrn_G12M00_bg2::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg2_Fim
	trainerbattle_no_intro TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg2_Derrota
	end

GalarTrn_G12M00_bg2_Fim:
	release
	end

GalarTrn_G12M00_bg2_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_bg3::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg3_Fim
	trainerbattle_no_intro TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_bg3_Derrota
	end

GalarTrn_G12M00_bg3_Fim:
	release
	end

GalarTrn_G12M00_bg3_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_bg4::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg4_Fim
	trainerbattle_no_intro TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg4_Derrota
	end

GalarTrn_G12M00_bg4_Fim:
	release
	end

GalarTrn_G12M00_bg4_Derrota:
	.string "$"

GalarTrn_G12M00_bg5::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg5_Fim
	trainerbattle_no_intro TRAINER_GALAR_AVA_178, GalarTrn_G12M00_bg5_Derrota
	end

GalarTrn_G12M00_bg5_Fim:
	release
	end

GalarTrn_G12M00_bg5_Derrota:
	.string "$"

GalarTrn_G12M00_bg6::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg6_Fim
	trainerbattle_no_intro TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg6_Derrota
	end

GalarTrn_G12M00_bg6_Fim:
	release
	end

GalarTrn_G12M00_bg6_Derrota:
	.string "Quente demais!$"

GalarTrn_G12M00_bg7::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg7_Fim
	trainerbattle_no_intro TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_bg7_Derrota
	end

GalarTrn_G12M00_bg7_Fim:
	release
	end

GalarTrn_G12M00_bg7_Derrota:
	.string "Quente demais!$"

GalarTrn_G12M00_bg8::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg8_Fim
	trainerbattle_no_intro TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg8_Derrota
	end

GalarTrn_G12M00_bg8_Fim:
	release
	end

GalarTrn_G12M00_bg8_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_bg9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg9_Fim
	trainerbattle_no_intro TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_bg9_Derrota
	end

GalarTrn_G12M00_bg9_Fim:
	release
	end

GalarTrn_G12M00_bg9_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_o0::
	trainerbattle_single TRAINER_GALAR_TALIA_213, GalarTrn_G12M00_o0_Intro, GalarTrn_G12M00_o0_Derrota
	end

GalarTrn_G12M00_o0_Intro:
	.string "Resposta errada jovenzinho$"

GalarTrn_G12M00_o0_Derrota:
	.string "Eu me rendo!$"

GalarTrn_G12M00_o1::
	trainerbattle_single TRAINER_GALAR_ERIKA_177, GalarTrn_G12M00_o1_Intro, GalarTrn_G12M00_o1_Derrota
	end

GalarTrn_G12M00_o1_Intro:
	.string "Você sabe como os Pokémon fadas\nconseguem vencer os dragoes?$"

GalarTrn_G12M00_o1_Derrota:
	.string "Uau!\nQuente quente quente!$"

GalarTrn_G12M00_o2::
	trainerbattle_single TRAINER_GALAR_AVA_178, GalarTrn_G12M00_o2_Intro, GalarTrn_G12M00_o2_Derrota
	end

GalarTrn_G12M00_o2_Intro:
	.string "Acho que sei de onde \nvem o poder das fadas!$"

GalarTrn_G12M00_o2_Derrota:
	.string "Uau!\nMeus estudos foram insuficientes!$"

GalarTrn_G12M00_o3::
	trainerbattle_single TRAINER_GALAR_CLOTILDE_214, GalarTrn_G12M00_o3_Intro, GalarTrn_G12M00_o3_Derrota
	end

GalarTrn_G12M00_o3_Intro:
	.string "Me informaram errado, achei\nque a Opal era treinadora\lde tipo fantasma.\painda bem, que tenho uma fada aqui.$"

GalarTrn_G12M00_o3_Derrota:
	.string "Quente demais!$"

GalarTrn_G12M00_o4::
	trainerbattle_single TRAINER_GALAR_DELIA_179, GalarTrn_G12M00_o4_Intro, GalarTrn_G12M00_o4_Derrota
	end

GalarTrn_G12M00_o4_Intro:
	.string "Vamos dançar!$"

GalarTrn_G12M00_o4_Derrota:
	.string "Ow!$"

GalarTrn_G12M00_o5::
	trainerbattle_single TRAINER_GALAR_KARLA_215, GalarTrn_G12M00_o5_Intro, GalarTrn_G12M00_o5_Derrota
	end

GalarTrn_G12M00_o5_Intro:
	.string "Gosta de fadas?$"

GalarTrn_G12M00_o5_Derrota:
	.string "Yowza!$"

GalarTrn_G12M00_o6::
	trainerbattle_single TRAINER_GALAR_LANA_180, GalarTrn_G12M00_o6_Intro, GalarTrn_G12M00_o6_Derrota
	end

GalarTrn_G12M00_o6_Intro:
	.string "Sei que você vai querer ser\numa de nós…$"

GalarTrn_G12M00_o6_Derrota:
	.string "Oh!$"

@ ---- Galar_Circhester06 ----
GalarTrn_G12M10_o19::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_435, GalarTrn_G12M10_o19_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_435, 0, GalarTrn_G12M10_o19_Derrota, GalarTrn_G12M10_o19_Vitoria
	end

GalarTrn_G12M10_o19_Fim:
	release
	end

GalarTrn_G12M10_o19_Derrota:
	.string "vamos lá$"

GalarTrn_G12M10_o19_Vitoria:
	.string "Ainda näo consigo derrotar\nvocê,meu verdadeiro rival.\lMas acho que estou come ando a ver\la luz no fim do t nel!$"

@ ---- Galar_Circhester08 ----
GalarTrn_G12M12_o0::
	trainerbattle_single TRAINER_GALAR_CARTER_313, GalarTrn_G12M12_o0_Intro, GalarTrn_G12M12_o0_Derrota
	end

GalarTrn_G12M12_o0_Intro:
	.string "Näo täo rapido!$"

GalarTrn_G12M12_o0_Derrota:
	.string "...$"

GalarTrn_G12M12_o1::
	trainerbattle_single TRAINER_GALAR_MITCH_314, GalarTrn_G12M12_o1_Intro, GalarTrn_G12M12_o1_Derrota
	end

GalarTrn_G12M12_o1_Intro:
	.string "Ei espera ai!$"

GalarTrn_G12M12_o1_Derrota:
	.string "...$"

GalarTrn_G12M12_o2::
	trainerbattle_single TRAINER_GALAR_BECK_315, GalarTrn_G12M12_o2_Intro, GalarTrn_G12M12_o2_Derrota
	end

GalarTrn_G12M12_o2_Intro:
	.string "Esta indo bem longe\nnäo é?$"

GalarTrn_G12M12_o2_Derrota:
	.string "...$"

GalarTrn_G12M12_o3::
	trainerbattle_single TRAINER_GALAR_MARLON_316, GalarTrn_G12M12_o3_Intro, GalarTrn_G12M12_o3_Derrota
	end

GalarTrn_G12M12_o3_Intro:
	.string "Näo se eu poder impedir!$"

GalarTrn_G12M12_o3_Derrota:
	.string "...$"

@ ---- Galar_Circhester09 ----
GalarTrn_G12M13_o0::
	trainerbattle_single TRAINER_GALAR_MOGAN_130, GalarTrn_G12M13_o0_Intro, GalarTrn_G12M13_o0_Derrota
	end

GalarTrn_G12M13_o0_Intro:
	.string "Esta indo bem longe\nnäo é?$"

GalarTrn_G12M13_o0_Derrota:
	.string "...$"

GalarTrn_G12M13_o1::
	trainerbattle_single TRAINER_GALAR_LESLIE_173, GalarTrn_G12M13_o1_Intro, GalarTrn_G12M13_o1_Derrota
	end

GalarTrn_G12M13_o1_Intro:
	.string "Näo se eu poder impedir!$"

GalarTrn_G12M13_o1_Derrota:
	.string "...$"

GalarTrn_G12M13_o2::
	trainerbattle_single TRAINER_GALAR_ANDRE_129, GalarTrn_G12M13_o2_Intro, GalarTrn_G12M13_o2_Derrota
	end

GalarTrn_G12M13_o2_Intro:
	.string "Ei espera ai!$"

GalarTrn_G12M13_o2_Derrota:
	.string "...$"

GalarTrn_G12M13_o3::
	trainerbattle_single TRAINER_GALAR_ETHAN_128, GalarTrn_G12M13_o3_Intro, GalarTrn_G12M13_o3_Derrota
	end

GalarTrn_G12M13_o3_Intro:
	.string "Näo täo rapido!$"

GalarTrn_G12M13_o3_Derrota:
	.string "...$"

@ ---- Galar_Circhester10 ----
GalarTrn_G12M14_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MELONY_336, GalarTrn_G12M14_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MELONY_336, GalarTrn_G12M14_o12_Derrota
	end

GalarTrn_G12M14_o12_Fim:
	release
	end

GalarTrn_G12M14_o12_Derrota:
	.string "Eu acho que você interpretou\nquebrar o gelo um pouco\lliteralmente demais ...$"

@ ---- Galar_Circhester11 ----
GalarTrn_G12M15_o12::
	trainerbattle_single TRAINER_GALAR_GORDIE_49, GalarTrn_G12M15_o12_Intro, GalarTrn_G12M15_o12_Derrota
	end

GalarTrn_G12M15_o12_Intro:
	.string "Gordie:Olá Meu nome é Gordie.\nMe sinto um pouco mal por ter que\lacabar com os sonhos de um\ldesafiante de ginásio,mas...\lVou usar essa partida para mostrar\lá multidäo que meus pokémons säo\limbativeis e incriveis!\lEntäo,vamos acabar logo com\lisso,Desafiante!$"

GalarTrn_G12M15_o12_Derrota:
	.string "Parece que eu cair no fundo do poco$"

@ ---- Galar_Circhester17 ----
GalarTrn_G13M12_o0::
	trainerbattle_single TRAINER_GALAR_MOGAN_130, GalarTrn_G13M12_o0_Intro, GalarTrn_G13M12_o0_Derrota
	end

GalarTrn_G13M12_o0_Intro:
	.string "Esta indo bem longe\nnäo é?$"

GalarTrn_G13M12_o0_Derrota:
	.string "...$"

GalarTrn_G13M12_o1::
	trainerbattle_single TRAINER_GALAR_LESLIE_173, GalarTrn_G13M12_o1_Intro, GalarTrn_G13M12_o1_Derrota
	end

GalarTrn_G13M12_o1_Intro:
	.string "Näo se eu poder impedir!$"

GalarTrn_G13M12_o1_Derrota:
	.string "...$"

GalarTrn_G13M12_o2::
	trainerbattle_single TRAINER_GALAR_ANDRE_129, GalarTrn_G13M12_o2_Intro, GalarTrn_G13M12_o2_Derrota
	end

GalarTrn_G13M12_o2_Intro:
	.string "Ei espera ai!$"

GalarTrn_G13M12_o2_Derrota:
	.string "...$"

GalarTrn_G13M12_o3::
	trainerbattle_single TRAINER_GALAR_ETHAN_128, GalarTrn_G13M12_o3_Intro, GalarTrn_G13M12_o3_Derrota
	end

GalarTrn_G13M12_o3_Intro:
	.string "Näo täo rapido!$"

GalarTrn_G13M12_o3_Derrota:
	.string "...$"

@ ---- Galar_CrownTundra02 ----
GalarTrn_G00M15_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PEONY_343, GalarTrn_G00M15_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_PEONY_343, GalarTrn_G00M15_o0_Derrota
	end

GalarTrn_G00M15_o0_Fim:
	release
	end

GalarTrn_G00M15_o0_Derrota:
	.string "WOW$"

GalarTrn_G00M15_o2::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MEGAN_648, GalarTrn_G00M15_o2_Fim
	trainerbattle_no_intro TRAINER_GALAR_MEGAN_648, GalarTrn_G00M15_o2_Derrota
	end

GalarTrn_G00M15_o2_Fim:
	release
	end

GalarTrn_G00M15_o2_Derrota:
	.string "WOW$"

@ ---- Galar_CrownTundra09 ----
GalarTrn_G37M06_o31::
	trainerbattle_single TRAINER_GALAR_TOMMY_300, GalarTrn_G37M06_o31_Intro, GalarTrn_G37M06_o31_Derrota
	end

GalarTrn_G37M06_o31_Intro:
	.string "Eu sou Tommy, Sou do anime de\ntwilight wings, e agora eu vou\lganhar!!!$"

GalarTrn_G37M06_o31_Derrota:
	.string "Parabéns$"

GalarTrn_G37M06_o42::
	trainerbattle_single TRAINER_GALAR_JON_299, GalarTrn_G37M06_o42_Intro, GalarTrn_G37M06_o42_Derrota
	end

GalarTrn_G37M06_o42_Intro:
	.string "twilight wings foi um bom anime,\nnäo é?\peu sou Jon finalmente me curei da\nminha doença e agora sou um grande\ltreinador!$"

GalarTrn_G37M06_o42_Derrota:
	.string "Wow isso foi incrivel!!!$"

@ ---- Galar_DynamaxAdventure01 ----
GalarTrn_G34M04_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MEGAN_648, GalarTrn_G34M04_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_MEGAN_648, GalarTrn_G34M04_o0_Derrota
	end

GalarTrn_G34M04_o0_Fim:
	release
	end

GalarTrn_G34M04_o0_Derrota:
	.string "Wow, que incrivel!$"

@ ---- Galar_GalarMine02 ----
GalarTrn_G06M28_o0::
	trainerbattle_single TRAINER_GALAR_KENT_108, GalarTrn_G06M28_o0_Intro, GalarTrn_G06M28_o0_Derrota
	end

GalarTrn_G06M28_o0_Intro:
	.string "Outro muleque na caverna?\nVocês estäo juntos?$"

GalarTrn_G06M28_o0_Derrota:
	.string "Você me pegou!$"

GalarTrn_G06M28_o1::
	trainerbattle_single TRAINER_GALAR_JOVAN_169, GalarTrn_G06M28_o1_Intro, GalarTrn_G06M28_o1_Derrota
	end

GalarTrn_G06M28_o1_Intro:
	.string "O que!\nNäo se aproxime de mim$"

GalarTrn_G06M28_o1_Derrota:
	.string "Meu Pokémon näo serve!$"

GalarTrn_G06M28_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_121, GalarTrn_G06M28_o2_Intro, GalarTrn_G06M28_o2_Derrota
	end

GalarTrn_G06M28_o2_Intro:
	.string "O que?\pEstou esperando meus amigos\nencontrarem eu aqui.$"

GalarTrn_G06M28_o2_Derrota:
	.string "Eu perdi?$"

@ ---- Galar_GalarMine03 ----
GalarTrn_G08M20_o10::
	trainerbattle_single TRAINER_GALAR_LEAH_476, GalarTrn_G08M20_o10_Intro, GalarTrn_G08M20_o10_Derrota
	end

GalarTrn_G08M20_o10_Intro:
	.string "Eek!\pNäo tente nada engraçado no\nescuro!$"

GalarTrn_G08M20_o10_Derrota:
	.string "Estava muito escuro.$"

GalarTrn_G08M20_o2::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GRUNT_12, GalarTrn_G08M20_o2_Fim
	trainerbattle_no_intro TRAINER_GALAR_GRUNT_12, GalarTrn_G08M20_o2_Derrota
	end

GalarTrn_G08M20_o2_Fim:
	release
	end

GalarTrn_G08M20_o2_Derrota:
	.string "realmente voce e forte$"

GalarTrn_G08M20_o3::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GRUNT_12, GalarTrn_G08M20_o3_Fim
	trainerbattle_no_intro TRAINER_GALAR_GRUNT_12, GalarTrn_G08M20_o3_Derrota
	end

GalarTrn_G08M20_o3_Fim:
	release
	end

GalarTrn_G08M20_o3_Derrota:
	.string "realmente voce e forte$"

GalarTrn_G08M20_o4::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BEDE_11, GalarTrn_G08M20_o4_Fim
	trainerbattle_no_intro TRAINER_GALAR_BEDE_11, GalarTrn_G08M20_o4_Derrota
	end

GalarTrn_G08M20_o4_Fim:
	release
	end

GalarTrn_G08M20_o4_Derrota:
	.string "realmente voce e forte$"

GalarTrn_G08M20_o8::
	trainerbattle_single TRAINER_GALAR_DANA_474, GalarTrn_G08M20_o8_Intro, GalarTrn_G08M20_o8_Derrota
	end

GalarTrn_G08M20_o8_Intro:
	.string "Eu vim até aqui procurando por\nalgum Pokémon selvagem.$"

GalarTrn_G08M20_o8_Derrota:
	.string "Estou sem Pokémon!$"

GalarTrn_G08M20_o9::
	trainerbattle_single TRAINER_GALAR_ARIANA_475, GalarTrn_G08M20_o9_Intro, GalarTrn_G08M20_o9_Derrota
	end

GalarTrn_G08M20_o9_Intro:
	.string "Você tem Pokémon!\nVamos começar!$"

GalarTrn_G08M20_o9_Derrota:
	.string "Essa brincadeira foi dificil$"

@ ---- Galar_GalarMine05 ----
GalarTrn_G07M10_o1::
	trainerbattle_single TRAINER_GALAR_MARCOS_181, GalarTrn_G07M10_o1_Intro, GalarTrn_G07M10_o1_Derrota
	end

GalarTrn_G07M10_o1_Intro:
	.string "Whoa!\nYou shocked me!\l…Oh, you’re just a kid!$"

GalarTrn_G07M10_o1_Derrota:
	.string "Wow!\nShocked again!$"

GalarTrn_G07M10_o4::
	trainerbattle_single TRAINER_GALAR_BRADLEY_174, GalarTrn_G07M10_o4_Intro, GalarTrn_G07M10_o4_Derrota
	end

GalarTrn_G07M10_o4_Intro:
	.string "Você veio batalhar contra o Milo,\ntambém?$"

GalarTrn_G07M10_o4_Derrota:
	.string "Perder fede!\nNo é nada legal.$"

@ ---- Galar_GlimwoodTangle01 ----
GalarTrn_G01M109_o0::
	trainerbattle_single TRAINER_GALAR_ROBERT_157, GalarTrn_G01M109_o0_Intro, GalarTrn_G01M109_o0_Derrota
	end

GalarTrn_G01M109_o0_Intro:
	.string "Estou me sentindo um pouco tonto.\nFaz algum tempo que näo caminho.$"

GalarTrn_G01M109_o0_Derrota:
	.string "Eu estou muito cansado.\nnäo estava preparado para isso.$"

GalarTrn_G01M109_o14::
	trainerbattle_single TRAINER_GALAR_JACQUELINE_188, GalarTrn_G01M109_o14_Intro, GalarTrn_G01M109_o14_Derrota
	end

GalarTrn_G01M109_o14_Intro:
	.string "Ah!\nEsse ar daqui é uma delícia!$"

GalarTrn_G01M109_o14_Derrota:
	.string "Isso clareou minha cabeça!$"

GalarTrn_G01M109_o15::
	trainerbattle_single TRAINER_GALAR_JUDY_163, GalarTrn_G01M109_o15_Intro, GalarTrn_G01M109_o15_Derrota
	end

GalarTrn_G01M109_o15_Intro:
	.string "Olá!\nQuer ver meu Pokémon?$"

GalarTrn_G01M109_o15_Derrota:
	.string "Oh näo!\nMeu Pokémon!$"

GalarTrn_G01M109_o16::
	trainerbattle_single TRAINER_GALAR_CLARK_187, GalarTrn_G01M109_o16_Intro, GalarTrn_G01M109_o16_Derrota
	end

GalarTrn_G01M109_o16_Intro:
	.string "Ha-hahah-ah-ha!$"

GalarTrn_G01M109_o16_Derrota:
	.string "Ha-haha!\nHa-hay fever! Haha-ha-choo!$"

@ ---- Galar_Hammerlocke02 ----
GalarTrn_G04M08_o0::
	trainerbattle_single TRAINER_GALAR_MARCIO_459, GalarTrn_G04M08_o0_Intro, GalarTrn_G04M08_o0_Derrota
	end

GalarTrn_G04M08_o0_Intro:
	.string "Eu represento o Raihan.$"

GalarTrn_G04M08_o0_Derrota:
	.string "Perdi$"

GalarTrn_G04M08_o1::
	trainerbattle_single TRAINER_GALAR_GABRIEL_458, GalarTrn_G04M08_o1_Intro, GalarTrn_G04M08_o1_Derrota
	end

GalarTrn_G04M08_o1_Intro:
	.string "Eu represento o Raihan.$"

GalarTrn_G04M08_o1_Derrota:
	.string "Perdi$"

GalarTrn_G04M08_o2::
	trainerbattle_single TRAINER_GALAR_CARLOS_457, GalarTrn_G04M08_o2_Intro, GalarTrn_G04M08_o2_Derrota
	end

GalarTrn_G04M08_o2_Intro:
	.string "Eu represento o Raihan.$"

GalarTrn_G04M08_o2_Derrota:
	.string "Perdi$"

@ ---- Galar_Hammerlocke10 ----
GalarTrn_G09M17_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ROSE_85, GalarTrn_G09M17_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_ROSE_85, GalarTrn_G09M17_o0_Derrota
	end

GalarTrn_G09M17_o0_Fim:
	release
	end

GalarTrn_G09M17_o0_Derrota:
	.string "Eu tinha esquecido como as\nbatalhas Pokémon säo otimas!\pFaz tanto tempo que eu näo luto...\nIsso com certeza foi satisfatorio.$"

@ ---- Galar_Hammerlocke23 ----
GalarTrn_G03M06_o10::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_429, GalarTrn_G03M06_o10_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_429, GalarTrn_G03M06_o10_Derrota
	end

GalarTrn_G03M06_o10_Fim:
	release
	end

GalarTrn_G03M06_o10_Derrota:
	.string "Minha estratégia vai direto ao buraco \nquando tenho todos esses pensamentos\lruins passando pela minha cabeça. $"

GalarTrn_G03M06_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_429, GalarTrn_G03M06_o9_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_429, GalarTrn_G03M06_o9_Derrota
	end

GalarTrn_G03M06_o9_Fim:
	release
	end

GalarTrn_G03M06_o9_Derrota:
	.string "Minha estratégia vai direto ao buraco \nquando tenho todos esses pensamentos\lruins passando pela minha cabeça. $"

@ ---- Galar_Hulbury06 ----
GalarTrn_G08M07_o17::
	trainerbattle_single TRAINER_GALAR_WANDA_686, GalarTrn_G08M07_o17_Intro, GalarTrn_G08M07_o17_Derrota
	end

GalarTrn_G08M07_o17_Intro:
	.string "{COLOR LIGHT_RED}Ei, está uma chatice isso aqui.\pQue tal uma batalha para\ndescontrair?$"

GalarTrn_G08M07_o17_Derrota:
	.string "{COLOR LIGHT_RED}É hora de voltar ao trabalho.$"

GalarTrn_G08M07_o39::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ROBERT_656, GalarTrn_G08M07_o39_Fim
	trainerbattle_no_intro TRAINER_GALAR_ROBERT_656, GalarTrn_G08M07_o39_Derrota
	end

GalarTrn_G08M07_o39_Fim:
	release
	end

GalarTrn_G08M07_o39_Derrota:
	.string "Droga! Você ganhou...$"

@ ---- Galar_Hulbury07 ----
GalarTrn_G08M08_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_JONH_5, GalarTrn_G08M08_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_JONH_5, GalarTrn_G08M08_o0_Derrota
	end

GalarTrn_G08M08_o0_Fim:
	release
	end

GalarTrn_G08M08_o0_Derrota:
	.string "Team Yell: Gah ... Voce esmagou\nminha tentativa de esmaga$"

GalarTrn_G08M08_o3::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_332, GalarTrn_G08M08_o3_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_332, GalarTrn_G08M08_o3_Derrota
	end

GalarTrn_G08M08_o3_Fim:
	release
	end

GalarTrn_G08M08_o3_Derrota:
	.string "Nós dois conseguimos a insiguina\nde grama,entao como e que você e\pmuito mais forte?! $"

@ ---- Galar_Hulbury08 ----
GalarTrn_G08M14_o0::
	trainerbattle_single TRAINER_GALAR_JULIA_234, GalarTrn_G08M14_o0_Intro, GalarTrn_G08M14_o0_Derrota
	end

GalarTrn_G08M14_o0_Intro:
	.string "Splash!\pI’m first up!\nLet’s do it!$"

GalarTrn_G08M14_o0_Derrota:
	.string "That can’t be!$"

GalarTrn_G08M14_o1::
	trainerbattle_single TRAINER_GALAR_DIANA_150, GalarTrn_G08M14_o1_Intro, GalarTrn_G08M14_o1_Derrota
	end

GalarTrn_G08M14_o1_Intro:
	.string "What? You?\nI’m more than good enough for you!\pMisty won’t have to be bothered.$"

GalarTrn_G08M14_o1_Derrota:
	.string "You overwhelmed me!$"

GalarTrn_G08M14_o2::
	trainerbattle_single TRAINER_GALAR_ANA_210, GalarTrn_G08M14_o2_Intro, GalarTrn_G08M14_o2_Derrota
	end

GalarTrn_G08M14_o2_Intro:
	.string "Here’s No. 3!\nI won’t be easy!$"

GalarTrn_G08M14_o2_Derrota:
	.string "Ow!\nStomped flat!$"

@ ---- Galar_Hulbury10 ----
GalarTrn_G08M16_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_NESSA_307, GalarTrn_G08M16_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_NESSA_307, GalarTrn_G08M16_o12_Derrota
	end

GalarTrn_G08M16_o12_Fim:
	release
	end

GalarTrn_G08M16_o12_Derrota:
	.string "Eu näo entendo.\pO que eu tenho que fazer para\nvencer você, hein?$"

@ ---- Galar_Hulbury12 ----
GalarTrn_G08M26_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_JONH_5, GalarTrn_G08M26_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_JONH_5, GalarTrn_G08M26_o0_Derrota
	end

GalarTrn_G08M26_o0_Fim:
	release
	end

GalarTrn_G08M26_o0_Derrota:
	.string "Team Yell: Gah ... Voce esmagou\nminha tentativa de esmaga$"

GalarTrn_G08M26_o3::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_332, GalarTrn_G08M26_o3_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_332, GalarTrn_G08M26_o3_Derrota
	end

GalarTrn_G08M26_o3_Fim:
	release
	end

GalarTrn_G08M26_o3_Derrota:
	.string "Nós dois conseguimos a insiguina\nde grama,entao como e que você e\pmuito mais forte?! $"

@ ---- Galar_IsleOfArmor05 ----
GalarTrn_G38M01_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KLARA_225, GalarTrn_G38M01_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_KLARA_225, GalarTrn_G38M01_o0_Derrota
	end

GalarTrn_G38M01_o0_Fim:
	release
	end

GalarTrn_G38M01_o0_Derrota:
	.string "Klara:Huh ?! Näo, näo! Näo, näo,\nnäo!Deve haver algum tipo de\lengano!$"

@ ---- Galar_IsleOfArmor13 ----
GalarTrn_G38M09_o30::
	trainerbattle_single TRAINER_GALAR_CLAYTON_SA_373, GalarTrn_G38M09_o30_Intro, GalarTrn_G38M09_o30_Derrota
	end

GalarTrn_G38M09_o30_Intro:
	.string "Clayton Santos:Wow, você me achou\nmesmo!\pachei que estava escondido\no suficiente, mas enfim ja que\lestamos aqui vamos batalhar!$"

GalarTrn_G38M09_o30_Derrota:
	.string "Clayton Santos:Foi uma boa batalha$"

@ ---- Galar_IsleOfArmor19 ----
GalarTrn_G38M15_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MUSTARD_230, GalarTrn_G38M15_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_MUSTARD_230, GalarTrn_G38M15_o0_Derrota
	end

GalarTrn_G38M15_o0_Fim:
	release
	end

GalarTrn_G38M15_o0_Derrota:
	.string "Vocês, jovens, crescem täo rápido!\pIsso nunca deixa de me\nsurpreender.$"

@ ---- Galar_IsleOfArmor25 ----
GalarTrn_G38M21_o5::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MUSTARD_230, GalarTrn_G38M21_o5_Fim
	trainerbattle_no_intro TRAINER_GALAR_MUSTARD_230, GalarTrn_G38M21_o5_Derrota
	end

GalarTrn_G38M21_o5_Fim:
	release
	end

GalarTrn_G38M21_o5_Derrota:
	.string "Vocês, jovens, crescem täo rápido!\pIsso nunca deixa de me\nsurpreender.$"

@ ---- Galar_IsleOfArmor32 ----
GalarTrn_G38M28_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LUCAS_231, GalarTrn_G38M28_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_LUCAS_231, GalarTrn_G38M28_o12_Derrota
	end

GalarTrn_G38M28_o12_Fim:
	release
	end

GalarTrn_G38M28_o12_Derrota:
	.string "Lucas: MANO...ISSO FOI DEMAIS!!!$"

@ ---- Galar_IsleOfArmor33 ----
GalarTrn_G38M29_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_VANESSA_233, GalarTrn_G38M29_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_VANESSA_233, GalarTrn_G38M29_o12_Derrota
	end

GalarTrn_G38M29_o12_Fim:
	release
	end

GalarTrn_G38M29_o12_Derrota:
	.string "...\n...\l...$"

@ ---- Galar_IsleOfArmor34 ----
GalarTrn_G38M30_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_C_PHENE_232, GalarTrn_G38M30_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_C_PHENE_232, GalarTrn_G38M30_o12_Derrota
	end

GalarTrn_G38M30_o12_Fim:
	release
	end

GalarTrn_G38M30_o12_Derrota:
	.string "Coronel.Phene: essa estratégia...\pessa alma de batalha...\pme lembra muito o boné vermelho,\nmas...$"

@ ---- Galar_Motostoke06 ----
GalarTrn_G06M12_o2::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KEVIN_1, GalarTrn_G06M12_o2_Fim
	trainerbattle_no_intro TRAINER_GALAR_KEVIN_1, GalarTrn_G06M12_o2_Derrota
	end

GalarTrn_G06M12_o2_Fim:
	release
	end

GalarTrn_G06M12_o2_Derrota:
	.string "Da um tempo ai!\nTeam Yell se vinguem por mim$"

@ ---- Galar_Motostoke16 ----
GalarTrn_G06M26_o1::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BIANCA_21, GalarTrn_G06M26_o1_Fim
	trainerbattle_no_intro TRAINER_GALAR_BIANCA_21, GalarTrn_G06M26_o1_Derrota
	end

GalarTrn_G06M26_o1_Fim:
	release
	end

GalarTrn_G06M26_o1_Derrota:
	.string "Nossa..$"

@ ---- Galar_Motostoke18 ----
GalarTrn_G06M33_o1::
	trainerbattle_single TRAINER_GALAR_TYLER_96, GalarTrn_G06M33_o1_Intro, GalarTrn_G06M33_o1_Derrota
	end

GalarTrn_G06M33_o1_Intro:
	.string "I love Pokémon!\nDo you?$"

GalarTrn_G06M33_o1_Derrota:
	.string "Wow! \nYou’re great!$"

GalarTrn_G06M33_o2::
	trainerbattle_single TRAINER_GALAR_ANDO_126, GalarTrn_G06M33_o2_Intro, GalarTrn_G06M33_o2_Derrota
	end

GalarTrn_G06M33_o2_Intro:
	.string "I collected these Pokémon\nfrom all around the world!$"

GalarTrn_G06M33_o2_Derrota:
	.string "Oh, no!\nI went around the world for these!$"

GalarTrn_G06M33_o3::
	trainerbattle_single TRAINER_GALAR_BROOKS_482, GalarTrn_G06M33_o3_Intro, GalarTrn_G06M33_o3_Derrota
	end

GalarTrn_G06M33_o3_Intro:
	.string "Competing against the young keeps\nme youthful.$"

GalarTrn_G06M33_o3_Derrota:
	.string "Good match!\nAh, I feel young again!$"

@ ---- Galar_Motostoke19 ----
GalarTrn_G06M34_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KABU_308, GalarTrn_G06M34_o9_Fim
	trainerbattle_no_intro TRAINER_GALAR_KABU_308, GalarTrn_G06M34_o9_Derrota
	end

GalarTrn_G06M34_o9_Fim:
	release
	end

GalarTrn_G06M34_o9_Derrota:
	.string "Bom Pokémon e um otimo Treinador!\pNäo é nenhuma surpresa que você\nganhou!$"

@ ---- Galar_Postwick10 ----
GalarTrn_G01M110_o10::
	trainerbattle_single TRAINER_GALAR_JUDY_163, GalarTrn_G01M110_o10_Intro, GalarTrn_G01M110_o10_Derrota
	end

GalarTrn_G01M110_o10_Intro:
	.string "Olá!\nQuer ver meu Pokémon?$"

GalarTrn_G01M110_o10_Derrota:
	.string "Oh näo!\nMeu Pokémon!$"

GalarTrn_G01M110_o7::
	trainerbattle_single TRAINER_GALAR_CLARK_187, GalarTrn_G01M110_o7_Intro, GalarTrn_G01M110_o7_Derrota
	end

GalarTrn_G01M110_o7_Intro:
	.string "Ha-hahah-ah-ha!$"

GalarTrn_G01M110_o7_Derrota:
	.string "Ha-haha!\nHa-hay fever! Haha-ha-choo!$"

GalarTrn_G01M110_o8::
	trainerbattle_single TRAINER_GALAR_ROBERT_157, GalarTrn_G01M110_o8_Intro, GalarTrn_G01M110_o8_Derrota
	end

GalarTrn_G01M110_o8_Intro:
	.string "Estou me sentindo um pouco tonto.\nFaz algum tempo que näo caminho.$"

GalarTrn_G01M110_o8_Derrota:
	.string "Eu estou muito cansado.\nnäo estava preparado para isso.$"

GalarTrn_G01M110_o9::
	trainerbattle_single TRAINER_GALAR_JACQUELINE_188, GalarTrn_G01M110_o9_Intro, GalarTrn_G01M110_o9_Derrota
	end

GalarTrn_G01M110_o9_Intro:
	.string "Ah!\nEsse ar daqui é uma delícia!$"

GalarTrn_G01M110_o9_Derrota:
	.string "Isso clareou minha cabeça!$"

@ ---- Galar_Postwick166 ----
GalarTrn_G39M41_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARTHA_SANT_381, GalarTrn_G39M41_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARTHA_SANT_381, GalarTrn_G39M41_o0_Derrota
	end

GalarTrn_G39M41_o0_Fim:
	release
	end

GalarTrn_G39M41_o0_Derrota:
	.string "Martha Santos:poxa...\nfiz o meu melhor...$"

@ ---- Galar_Postwick40 ----
GalarTrn_G07M07_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_116, GalarTrn_G07M07_o2_Intro, GalarTrn_G07M07_o2_Derrota
	end

GalarTrn_G07M07_o2_Intro:
	.string "Com licença!\nVocê olhou para mim, näo foi?$"

GalarTrn_G07M07_o2_Derrota:
	.string "Você é mau!$"

GalarTrn_G07M07_o3::
	trainerbattle_single TRAINER_GALAR_ANA_211, GalarTrn_G07M07_o3_Intro, GalarTrn_G07M07_o3_Derrota
	end

GalarTrn_G07M07_o3_Intro:
	.string "Oi!\nEu gosto de All Stars!\pEles säo deliciosamente confortáveis e\nfácil de usar!$"

GalarTrn_G07M07_o3_Derrota:
	.string "Eu no acredito!$"

GalarTrn_G07M07_o5::
	trainerbattle_single TRAINER_GALAR_ROBIN_118, GalarTrn_G07M07_o5_Intro, GalarTrn_G07M07_o5_Derrota
	end

GalarTrn_G07M07_o5_Intro:
	.string "Eek!\nVocê me tocou?$"

GalarTrn_G07M07_o5_Derrota:
	.string "É isso?$"

GalarTrn_G07M07_o6::
	trainerbattle_single TRAINER_GALAR_JAMES_107, GalarTrn_G07M07_o6_Intro, GalarTrn_G07M07_o6_Derrota
	end

GalarTrn_G07M07_o6_Intro:
	.string "Eu vou lutar com você com o Pokémon\nAcabei de pegar.$"

GalarTrn_G07M07_o6_Derrota:
	.string "Devia ter treinado mais...$"

@ ---- Galar_Postwick53 ----
GalarTrn_G08M21_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_JONH_5, GalarTrn_G08M21_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_JONH_5, GalarTrn_G08M21_o0_Derrota
	end

GalarTrn_G08M21_o0_Fim:
	release
	end

GalarTrn_G08M21_o0_Derrota:
	.string "Team Yell: Gah ... Voce esmagou\nminha tentativa de esmaga$"

GalarTrn_G08M21_o3::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_JONH_5, GalarTrn_G08M21_o3_Fim
	trainerbattle_no_intro TRAINER_GALAR_JONH_5, GalarTrn_G08M21_o3_Derrota
	end

GalarTrn_G08M21_o3_Fim:
	release
	end

GalarTrn_G08M21_o3_Derrota:
	.string "Team Yell: Gah ... Voce esmagou\nminha tentativa de esmaga$"

@ ---- Galar_RixyChamber01 ----
GalarTrn_G03M53_o0::
	trainerbattle_single TRAINER_GALAR_MIAH_588, GalarTrn_G03M53_o0_Intro, GalarTrn_G03M53_o0_Derrota
	end

GalarTrn_G03M53_o0_Intro:
	.string "Kyahaha!\nI’ll flick you away effortlessly!$"

GalarTrn_G03M53_o0_Derrota:
	.string "Tch!\nToo strong for me!$"

GalarTrn_G03M53_o1::
	trainerbattle_single TRAINER_GALAR_MADELINE_522, GalarTrn_G03M53_o1_Intro, GalarTrn_G03M53_o1_Derrota
	end

GalarTrn_G03M53_o1_Intro:
	.string "I punish people who abuse\nPokémon!$"

GalarTrn_G03M53_o1_Derrota:
	.string "You don’t seem to be a problem\nTrainer.$"

GalarTrn_G03M53_o2::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589, GalarTrn_G03M53_o2_Intro, GalarTrn_G03M53_o2_Derrota, GalarTrn_G03M53_o2_Poucos
	end

GalarTrn_G03M53_o2_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G03M53_o2_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G03M53_o2_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

GalarTrn_G03M53_o4::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589, GalarTrn_G03M53_o4_Intro, GalarTrn_G03M53_o4_Derrota, GalarTrn_G03M53_o4_Poucos
	end

GalarTrn_G03M53_o4_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G03M53_o4_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G03M53_o4_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

GalarTrn_G03M53_o5::
	trainerbattle_single TRAINER_GALAR_NICOLAS_521, GalarTrn_G03M53_o5_Intro, GalarTrn_G03M53_o5_Derrota
	end

GalarTrn_G03M53_o5_Intro:
	.string "This island is too spread out…\nIt’s not easy patrolling the place.$"

GalarTrn_G03M53_o5_Derrota:
	.string "Uh-huh…$"

@ ---- Galar_RoseTower01 ----
GalarTrn_G01M90_o1::
	trainerbattle_single TRAINER_GALAR_CARLOS_442, GalarTrn_G01M90_o1_Intro, GalarTrn_G01M90_o1_Derrota
	end

GalarTrn_G01M90_o1_Intro:
	.string "Sou pago para te impedir!$"

GalarTrn_G01M90_o1_Derrota:
	.string "Hmm?$"

@ ---- Galar_RoseTower02 ----
GalarTrn_G01M91_o0::
	trainerbattle_single TRAINER_GALAR_LAURO_445, GalarTrn_G01M91_o0_Intro, GalarTrn_G01M91_o0_Derrota
	end

GalarTrn_G01M91_o0_Intro:
	.string "Pare!\pIsso é pelo bem de galar!$"

GalarTrn_G01M91_o0_Derrota:
	.string "What!$"

GalarTrn_G01M91_o1::
	trainerbattle_single TRAINER_GALAR_JODY_446, GalarTrn_G01M91_o1_Intro, GalarTrn_G01M91_o1_Derrota
	end

GalarTrn_G01M91_o1_Intro:
	.string "Que descuido!$"

GalarTrn_G01M91_o1_Derrota:
	.string "O que?$"

@ ---- Galar_RoseTower03 ----
GalarTrn_G01M92_o1::
	trainerbattle_single TRAINER_GALAR_TAMMY_447, GalarTrn_G01M92_o1_Intro, GalarTrn_G01M92_o1_Derrota
	end

GalarTrn_G01M92_o1_Intro:
	.string "SAIA DAQUI!$"

GalarTrn_G01M92_o1_Derrota:
	.string "Gasp!$"

@ ---- Galar_RoseTower04 ----
GalarTrn_G01M94_o1::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_OLENA_80, GalarTrn_G01M94_o1_Fim
	trainerbattle_no_intro TRAINER_GALAR_OLENA_80, GalarTrn_G01M94_o1_Derrota
	end

GalarTrn_G01M94_o1_Fim:
	release
	end

GalarTrn_G01M94_o1_Derrota:
	.string "  suspiro   Eu näo consegui vencer\n... Oleana ... você realmente é\luma mulher sem esperança.$"

@ ---- Galar_Route0202 ----
GalarTrn_G05M12_o3::
	trainerbattle_single TRAINER_GALAR_LASS_102, GalarTrn_G05M12_o3_Intro, GalarTrn_G05M12_o3_Derrota
	end

GalarTrn_G05M12_o3_Intro:
	.string "Ei! Você tem Pokémon!\nVamos batalhar!$"

GalarTrn_G05M12_o3_Derrota:
	.string "AHa, Cara...$"

GalarTrn_G05M12_o5::
	trainerbattle_single TRAINER_GALAR_SAMMY_104, GalarTrn_G05M12_o5_Intro, GalarTrn_G05M12_o5_Derrota
	end

GalarTrn_G05M12_o5_Intro:
	.string "Ei, espere!\nQual é a pressa?$"

GalarTrn_G05M12_o5_Derrota:
	.string "Eu desisto!\nVocê é bom nisso!$"

GalarTrn_G05M12_o6::
	trainerbattle_single TRAINER_GALAR_ANTHONY_531, GalarTrn_G05M12_o6_Intro, GalarTrn_G05M12_o6_Derrota
	end

GalarTrn_G05M12_o6_Intro:
	.string "Posso ser pequeno, mas no vou\ngostar é se você pegar leve comigo!$"

GalarTrn_G05M12_o6_Derrota:
	.string "Ah, Certo.\ndeu erradio.$"

@ ---- Galar_Route0301 ----
GalarTrn_G06M17_o2::
	trainerbattle_single TRAINER_GALAR_HANNAH_116, GalarTrn_G06M17_o2_Intro, GalarTrn_G06M17_o2_Derrota
	end

GalarTrn_G06M17_o2_Intro:
	.string "Com licença!\nVocê olhou para mim, näo foi?$"

GalarTrn_G06M17_o2_Derrota:
	.string "Você é mau!$"

GalarTrn_G06M17_o3::
	trainerbattle_single TRAINER_GALAR_ANA_211, GalarTrn_G06M17_o3_Intro, GalarTrn_G06M17_o3_Derrota
	end

GalarTrn_G06M17_o3_Intro:
	.string "Oi!\nEu gosto de All Stars!\pEles säo deliciosamente confortáveis e\nfácil de usar!$"

GalarTrn_G06M17_o3_Derrota:
	.string "Eu no acredito!$"

GalarTrn_G06M17_o4::
	trainerbattle_single TRAINER_GALAR_CALVIN_90, GalarTrn_G06M17_o4_Intro, GalarTrn_G06M17_o4_Derrota
	end

GalarTrn_G06M17_o4_Intro:
	.string "Ei! Eu te vi na TV!\nO que você tem ai?$"

GalarTrn_G06M17_o4_Derrota:
	.string "Perdido!\nPerdido! estou Perdido!$"

GalarTrn_G06M17_o5::
	trainerbattle_single TRAINER_GALAR_ROBIN_118, GalarTrn_G06M17_o5_Intro, GalarTrn_G06M17_o5_Derrota
	end

GalarTrn_G06M17_o5_Intro:
	.string "Eek!\nVocê me tocou?$"

GalarTrn_G06M17_o5_Derrota:
	.string "É isso?$"

GalarTrn_G06M17_o6::
	trainerbattle_single TRAINER_GALAR_JAMES_107, GalarTrn_G06M17_o6_Intro, GalarTrn_G06M17_o6_Derrota
	end

GalarTrn_G06M17_o6_Intro:
	.string "Eu vou lutar com você com o Pokémon\nAcabei de pegar.$"

GalarTrn_G06M17_o6_Derrota:
	.string "Devia ter treinado mais...$"

@ ---- Galar_Route0401 ----
GalarTrn_G07M17_o2::
	trainerbattle_single TRAINER_GALAR_BRADLEY_174, GalarTrn_G07M17_o2_Intro, GalarTrn_G07M17_o2_Derrota
	end

GalarTrn_G07M17_o2_Intro:
	.string "Você veio batalhar contra o Milo,\ntambém?$"

GalarTrn_G07M17_o2_Derrota:
	.string "Perder fede!\nNo é nada legal.$"

@ ---- Galar_Route0501 ----
GalarTrn_G08M06_o4::
	trainerbattle_single TRAINER_GALAR_JASPER_259, GalarTrn_G08M06_o4_Intro, GalarTrn_G08M06_o4_Derrota
	end

GalarTrn_G08M06_o4_Intro:
	.string "Competir é a emoçäo final.\nEu ainda näo me canso!$"

GalarTrn_G08M06_o4_Derrota:
	.string "Eu tive uma chance!$"

@ ---- Galar_Route0601 ----
GalarTrn_G10M20_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GRUNT_13, GalarTrn_G10M20_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_GRUNT_13, GalarTrn_G10M20_o0_Derrota
	end

GalarTrn_G10M20_o0_Fim:
	release
	end

GalarTrn_G10M20_o0_Derrota:
	.string "Ah, cara! O ar sofisticado daqui\ncortou meu barato!$"

GalarTrn_G10M20_o1::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GRUNT_13, GalarTrn_G10M20_o1_Fim
	trainerbattle_no_intro TRAINER_GALAR_GRUNT_13, GalarTrn_G10M20_o1_Derrota
	end

GalarTrn_G10M20_o1_Fim:
	release
	end

GalarTrn_G10M20_o1_Derrota:
	.string "Ah, cara! O ar sofisticado daqui\ncortou meu barato!$"

GalarTrn_G10M20_o10::
	trainerbattle_single TRAINER_GALAR_DIANE_151, GalarTrn_G10M20_o10_Intro, GalarTrn_G10M20_o10_Derrota
	end

GalarTrn_G10M20_o10_Intro:
	.string "Com licença!\nEsta é uma conversa privada!\lcomigo mesmo!$"

GalarTrn_G10M20_o10_Derrota:
	.string "Eca!\nEu odeio perder.$"

GalarTrn_G10M20_o26::
	trainerbattle_single TRAINER_GALAR_ISABELLE_152, GalarTrn_G10M20_o26_Intro, GalarTrn_G10M20_o26_Derrota
	end

GalarTrn_G10M20_o26_Intro:
	.string "eu?\nBem, ok. Eu vou jogar!$"

GalarTrn_G10M20_o26_Derrota:
	.string "As coisas simplesmente näo\nfuncionaram pra mim...$"

GalarTrn_G10M20_o6::
	trainerbattle_single TRAINER_GALAR_HANNA_172, GalarTrn_G10M20_o6_Intro, GalarTrn_G10M20_o6_Derrota
	end

GalarTrn_G10M20_o6_Intro:
	.string "Você deve estar informado.\nVocê precisa de estratégia\lpara vencer nisso!$"

GalarTrn_G10M20_o6_Derrota:
	.string "Näo é lógico!$"

GalarTrn_G10M20_o7::
	trainerbattle_single TRAINER_GALAR_RUTH_111, GalarTrn_G10M20_o7_Intro, GalarTrn_G10M20_o7_Derrota
	end

GalarTrn_G10M20_o7_Intro:
	.string "Näo há muitos insetos aqui.$"

GalarTrn_G10M20_o7_Derrota:
	.string "Näo!\nVocê está brincando!$"

GalarTrn_G10M20_o9::
	trainerbattle_single TRAINER_GALAR_IWAN_E_EVEL_145, GalarTrn_G10M20_o9_Intro, GalarTrn_G10M20_o9_Derrota
	end

GalarTrn_G10M20_o9_Intro:
	.string "Quem está aí?$"

GalarTrn_G10M20_o9_Derrota:
	.string "Eu simplesmente näo consigo vencer!$"

@ ---- Galar_Route0701 ----
GalarTrn_G09M13_o0::
	trainerbattle_single TRAINER_GALAR_MILA_305, GalarTrn_G09M13_o0_Intro, GalarTrn_G09M13_o0_Derrota
	end

GalarTrn_G09M13_o0_Intro:
	.string "Quando eu assobio,\nposso invocar um Pokémon.$"

GalarTrn_G09M13_o0_Derrota:
	.string "Ai!\nIsso é trágico!$"

GalarTrn_G09M13_o1::
	trainerbattle_single TRAINER_GALAR_YAZMIN_478, GalarTrn_G09M13_o1_Intro, GalarTrn_G09M13_o1_Derrota
	end

GalarTrn_G09M13_o1_Intro:
	.string "Quer brincar com meu Pokémon?$"

GalarTrn_G09M13_o1_Derrota:
	.string "Eu estava muito impaciente!$"

GalarTrn_G09M13_o10::
	trainerbattle_single TRAINER_GALAR_BRUCE_306, GalarTrn_G09M13_o10_Intro, GalarTrn_G09M13_o10_Derrota
	end

GalarTrn_G09M13_o10_Intro:
	.string "Você é bom, näo é?$"

GalarTrn_G09M13_o10_Derrota:
	.string "Assim como pensei!$"

GalarTrn_G09M13_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_432, GalarTrn_G09M13_o9_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_432, 0, GalarTrn_G09M13_o9_Derrota, GalarTrn_G09M13_o9_Vitoria
	end

GalarTrn_G09M13_o9_Fim:
	release
	end

GalarTrn_G09M13_o9_Derrota:
	.string "vamos batalhar!$"

GalarTrn_G09M13_o9_Vitoria:
	.string "Que merda...Minha equipe näo pode\nbatalhar bem se eu näo conseguir\lcolocar minha cabeça no lugar.$"

@ ---- Galar_Route0801 ----
GalarTrn_G12M08_o10::
	trainerbattle_single TRAINER_GALAR_PERRY_301, GalarTrn_G12M08_o10_Intro, GalarTrn_G12M08_o10_Derrota
	end

GalarTrn_G12M08_o10_Intro:
	.string "Eu näo vou perder.\pNäo quando o vento sopra\nna minha direçäo!$"

GalarTrn_G12M08_o10_Derrota:
	.string "O vento mudou!$"

GalarTrn_G12M08_o11::
	trainerbattle_single TRAINER_GALAR_CHARLES_302, GalarTrn_G12M08_o11_Intro, GalarTrn_G12M08_o11_Derrota
	end

GalarTrn_G12M08_o11_Intro:
	.string "Eu sempre vou com meus Pokémon\nEu me dediquei a eles.$"

GalarTrn_G12M08_o11_Derrota:
	.string "Fora do poder!$"

GalarTrn_G12M08_o7::
	trainerbattle_single TRAINER_GALAR_JORDAN_469, GalarTrn_G12M08_o7_Intro, GalarTrn_G12M08_o7_Derrota
	end

GalarTrn_G12M08_o7_Intro:
	.string "Meus Pokémon fofos desejam\nconhecer o seu.$"

GalarTrn_G12M08_o7_Derrota:
	.string "Bom andamento!\nVocê ganhou totalmente!$"

GalarTrn_G12M08_o9::
	trainerbattle_single TRAINER_GALAR_JOANNA_195, GalarTrn_G12M08_o9_Intro, GalarTrn_G12M08_o9_Derrota
	end

GalarTrn_G12M08_o9_Intro:
	.string "O que você está olhando?$"

GalarTrn_G12M08_o9_Derrota:
	.string "Droga!$"

@ ---- Galar_Route0802 ----
GalarTrn_G12M09_o0::
	trainerbattle_single TRAINER_GALAR_BOBBY_309, GalarTrn_G12M09_o0_Intro, GalarTrn_G12M09_o0_Derrota
	end

GalarTrn_G12M09_o0_Intro:
	.string "Este é o meu território!\nSaia daqui!$"

GalarTrn_G12M09_o0_Derrota:
	.string "Droga!$"

@ ---- Galar_Route0901 ----
GalarTrn_G14M11_o1::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARNIE_60, GalarTrn_G14M11_o1_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARNIE_60, GalarTrn_G14M11_o1_Derrota
	end

GalarTrn_G14M11_o1_Fim:
	release
	end

GalarTrn_G14M11_o1_Derrota:
	.string "Como isso é possivel?!\nMeus pokémons näo tiveram a chance\lnem de batalhar direito.Ugh!$"

GalarTrn_G14M11_o10::
	trainerbattle_single TRAINER_GALAR_OLIVIER_274, GalarTrn_G14M11_o10_Intro, GalarTrn_G14M11_o10_Derrota
	end

GalarTrn_G14M11_o10_Intro:
	.string "Eu crio Pokémon para proteçäo\nporque moro sozinho.$"

GalarTrn_G14M11_o10_Derrota:
	.string "Pokémon näo é sobre vencer ou\nperdendo para mim.$"

GalarTrn_G14M11_o11::
	trainerbattle_single TRAINER_GALAR_GRACE_273, GalarTrn_G14M11_o11_Intro, GalarTrn_G14M11_o11_Derrota
	end

GalarTrn_G14M11_o11_Intro:
	.string "Ah, você é uma gracinha!\ncomo um Pokémon!$"

GalarTrn_G14M11_o11_Derrota:
	.string "Você parecia täo fofo antes!$"

GalarTrn_G14M11_o13::
	trainerbattle_single TRAINER_GALAR_ERNEST_197, GalarTrn_G14M11_o13_Intro, GalarTrn_G14M11_o13_Derrota
	end

GalarTrn_G14M11_o13_Intro:
	.string "Ei! Vamos lá!$"

GalarTrn_G14M11_o13_Derrota:
	.string "Por que näo?$"

GalarTrn_G14M11_o14::
	trainerbattle_single TRAINER_GALAR_BECKY_480, GalarTrn_G14M11_o14_Intro, GalarTrn_G14M11_o14_Derrota
	end

GalarTrn_G14M11_o14_Intro:
	.string "Você parece gentil, entäo acho\nque posso bater em você.\pVou tentar!$"

GalarTrn_G14M11_o14_Derrota:
	.string "Näo, errado!$"

GalarTrn_G14M11_o16::
	trainerbattle_single TRAINER_GALAR_ISAIAH_252, GalarTrn_G14M11_o16_Intro, GalarTrn_G14M11_o16_Derrota
	end

GalarTrn_G14M11_o16_Intro:
	.string "Näo há como ficar rico rapidamente\nlutando contra crianças.$"

GalarTrn_G14M11_o16_Derrota:
	.string "Queima inferno!$"

GalarTrn_G14M11_o4::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ANA_59, GalarTrn_G14M11_o4_Fim
	trainerbattle_no_intro TRAINER_GALAR_ANA_59, GalarTrn_G14M11_o4_Derrota
	end

GalarTrn_G14M11_o4_Fim:
	release
	end

GalarTrn_G14M11_o4_Derrota:
	.string "  suspiro   Eu quero voltar para\nSpikemuth.So isso.$"

GalarTrn_G14M11_o45::
	trainerbattle_single TRAINER_GALAR_VIRGIL_470, GalarTrn_G14M11_o45_Intro, GalarTrn_G14M11_o45_Derrota
	end

GalarTrn_G14M11_o45_Intro:
	.string "Você está indo para Spikemurth?$"

GalarTrn_G14M11_o45_Derrota:
	.string "Bate e queima!$"

GalarTrn_G14M11_o9::
	trainerbattle_single TRAINER_GALAR_KINDRA_479, GalarTrn_G14M11_o9_Intro, GalarTrn_G14M11_o9_Derrota
	end

GalarTrn_G14M11_o9_Intro:
	.string "Acabei de receber alguns Pokémon\nem trocas.\pPosso experimentá-los em você?$"

GalarTrn_G14M11_o9_Derrota:
	.string "Näo esta bom o suficiente!$"

@ ---- Galar_Route1001 ----
GalarTrn_G03M28_o6::
	trainerbattle_single TRAINER_GALAR_GLENN_277, GalarTrn_G03M28_o6_Intro, GalarTrn_G03M28_o6_Derrota
	end

GalarTrn_G03M28_o6_Intro:
	.string "Nadar é ótimo!\nMas no gelo näo!$"

GalarTrn_G03M28_o6_Derrota:
	.string "Chocante!$"

GalarTrn_G03M28_o7::
	trainerbattle_single TRAINER_GALAR_GILLI_E_CAM_278, GalarTrn_G03M28_o7_Intro, GalarTrn_G03M28_o7_Derrota
	end

GalarTrn_G03M28_o7_Intro:
	.string "Que tal uma entrevista?$"

GalarTrn_G03M28_o7_Derrota:
	.string "isso deve bastar!$"

GalarTrn_G03M28_o8::
	trainerbattle_single TRAINER_GALAR_GILLI_E_CAM_278, GalarTrn_G03M28_o8_Intro, GalarTrn_G03M28_o8_Derrota
	end

GalarTrn_G03M28_o8_Intro:
	.string "Que tal uma entrevista?$"

GalarTrn_G03M28_o8_Derrota:
	.string "isso deve bastar!$"

@ ---- Galar_Route1601 ----
GalarTrn_G10M23_o0::
	trainerbattle_single TRAINER_GALAR_EMILIA_452, GalarTrn_G10M23_o0_Intro, GalarTrn_G10M23_o0_Derrota
	end

GalarTrn_G10M23_o0_Intro:
	.string "Eu represento o Allister1$"

GalarTrn_G10M23_o0_Derrota:
	.string "Você me derrotou..$"

GalarTrn_G10M23_o1::
	trainerbattle_single TRAINER_GALAR_JENNIFER_453, GalarTrn_G10M23_o1_Intro, GalarTrn_G10M23_o1_Derrota
	end

GalarTrn_G10M23_o1_Intro:
	.string "Eu represento o Allister1$"

GalarTrn_G10M23_o1_Derrota:
	.string "Você me derrotou..$"

GalarTrn_G10M23_o2::
	trainerbattle_single TRAINER_GALAR_ANGELICA_451, GalarTrn_G10M23_o2_Intro, GalarTrn_G10M23_o2_Derrota
	end

GalarTrn_G10M23_o2_Intro:
	.string "Vamos batalhar$"

GalarTrn_G10M23_o2_Derrota:
	.string "Perdi$"

@ ---- Galar_Route1603 ----
GalarTrn_G10M26_o0::
	trainerbattle_single TRAINER_GALAR_AARON_320, GalarTrn_G10M26_o0_Intro, GalarTrn_G10M26_o0_Derrota
	end

GalarTrn_G10M26_o0_Intro:
	.string "Hiyah!\nI have no fear for anything tough!\pI shatter boulders for training\nevery day!$"

GalarTrn_G10M26_o0_Derrota:
	.string "Yow!\nStubbed fingers!$"

GalarTrn_G10M26_o1::
	trainerbattle_single TRAINER_GALAR_HIDEKI_319, GalarTrn_G10M26_o1_Intro, GalarTrn_G10M26_o1_Derrota
	end

GalarTrn_G10M26_o1_Intro:
	.string "I hear you’re good!\nShow me!$"

GalarTrn_G10M26_o1_Derrota:
	.string "Judge!\nOne point!$"

GalarTrn_G10M26_o2::
	trainerbattle_single TRAINER_GALAR_HITOSHI_321, GalarTrn_G10M26_o2_Intro, GalarTrn_G10M26_o2_Derrota
	end

GalarTrn_G10M26_o2_Intro:
	.string "Hwaah!\pYou’re trespassing in our\nFighting Dojo!$"

GalarTrn_G10M26_o2_Derrota:
	.string "Oof!\nI give up!$"

@ ---- Galar_Spikemuth07 ----
GalarTrn_G14M10_o0::
	trainerbattle_single TRAINER_GALAR_GRUNT_391, GalarTrn_G14M10_o0_Intro, GalarTrn_G14M10_o0_Derrota
	end

GalarTrn_G14M10_o0_Intro:
	.string "Näo säo permitidas crianças aqui!$"

GalarTrn_G14M10_o0_Derrota:
	.string "Difícil!$"

GalarTrn_G14M10_o1::
	trainerbattle_single TRAINER_GALAR_GRUNT_390, GalarTrn_G14M10_o1_Intro, GalarTrn_G14M10_o1_Derrota
	end

GalarTrn_G14M10_o1_Intro:
	.string "Me desculpa por isso mas eu näo\nposso te deixar passar!$"

GalarTrn_G14M10_o1_Derrota:
	.string "Eu errei!$"

GalarTrn_G14M10_o10::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PIERS_419, GalarTrn_G14M10_o10_Fim
	trainerbattle_no_intro TRAINER_GALAR_PIERS_419, GalarTrn_G14M10_o10_Derrota
	end

GalarTrn_G14M10_o10_Fim:
	release
	end

GalarTrn_G14M10_o10_Derrota:
	.string "Eu e minha equipe fizemos o\npossivel.Vamos nos encontrar para\lbatalhar novamente em alguma\lhora...$"

GalarTrn_G14M10_o14::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARNIE_165, GalarTrn_G14M10_o14_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARNIE_165, GalarTrn_G14M10_o14_Derrota
	end

GalarTrn_G14M10_o14_Fim:
	release
	end

GalarTrn_G14M10_o14_Derrota:
	.string "Você ganhou!$"

GalarTrn_G14M10_o2::
	trainerbattle_single TRAINER_GALAR_GRUNT_375, GalarTrn_G14M10_o2_Intro, GalarTrn_G14M10_o2_Derrota
	end

GalarTrn_G14M10_o2_Intro:
	.string "Pare de brincar com a gente, criança!$"

GalarTrn_G14M10_o2_Derrota:
	.string "Desisto!$"

GalarTrn_G14M10_o3::
	trainerbattle_single TRAINER_GALAR_GRUNT_379, GalarTrn_G14M10_o3_Intro, GalarTrn_G14M10_o3_Derrota
	end

GalarTrn_G14M10_o3_Intro:
	.string "Mostre um pouco de respeito ao Team Yell!$"

GalarTrn_G14M10_o3_Derrota:
	.string "Cough…\nCough…$"

GalarTrn_G14M10_o4::
	trainerbattle_single TRAINER_GALAR_GRUNT_378, GalarTrn_G14M10_o4_Intro, GalarTrn_G14M10_o4_Derrota
	end

GalarTrn_G14M10_o4_Intro:
	.string "Ouvi dizer que uma criança estava\nvagando em volta.$"

GalarTrn_G14M10_o4_Derrota:
	.string "Boom!$"

@ ---- Galar_Spikemuth09 ----
GalarTrn_G03M10_o0::
	trainerbattle_single TRAINER_GALAR_GRUNT_391, GalarTrn_G03M10_o0_Intro, GalarTrn_G03M10_o0_Derrota
	end

GalarTrn_G03M10_o0_Intro:
	.string "Näo säo permitidas crianças aqui!$"

GalarTrn_G03M10_o0_Derrota:
	.string "Difícil!$"

GalarTrn_G03M10_o1::
	trainerbattle_single TRAINER_GALAR_GRUNT_390, GalarTrn_G03M10_o1_Intro, GalarTrn_G03M10_o1_Derrota
	end

GalarTrn_G03M10_o1_Intro:
	.string "Me desculpa por isso mas eu näo\nposso te deixar passar!$"

GalarTrn_G03M10_o1_Derrota:
	.string "Eu errei!$"

GalarTrn_G03M10_o2::
	trainerbattle_single TRAINER_GALAR_GRUNT_375, GalarTrn_G03M10_o2_Intro, GalarTrn_G03M10_o2_Derrota
	end

GalarTrn_G03M10_o2_Intro:
	.string "Pare de brincar com a gente, criança!$"

GalarTrn_G03M10_o2_Derrota:
	.string "Desisto!$"

GalarTrn_G03M10_o3::
	trainerbattle_single TRAINER_GALAR_GRUNT_379, GalarTrn_G03M10_o3_Intro, GalarTrn_G03M10_o3_Derrota
	end

GalarTrn_G03M10_o3_Intro:
	.string "Mostre um pouco de respeito ao Team Yell!$"

GalarTrn_G03M10_o3_Derrota:
	.string "Cough…\nCough…$"

GalarTrn_G03M10_o4::
	trainerbattle_single TRAINER_GALAR_GRUNT_378, GalarTrn_G03M10_o4_Intro, GalarTrn_G03M10_o4_Derrota
	end

GalarTrn_G03M10_o4_Intro:
	.string "Ouvi dizer que uma criança estava\nvagando em volta.$"

GalarTrn_G03M10_o4_Derrota:
	.string "Boom!$"

@ ---- Galar_StowOnSide08 ----
GalarTrn_G10M21_o10::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_429, GalarTrn_G10M21_o10_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_429, GalarTrn_G10M21_o10_Derrota
	end

GalarTrn_G10M21_o10_Fim:
	release
	end

GalarTrn_G10M21_o10_Derrota:
	.string "Minha estratégia vai direto ao buraco \nquando tenho todos esses pensamentos\lruins passando pela minha cabeça. $"

GalarTrn_G10M21_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_429, GalarTrn_G10M21_o9_Fim
	trainerbattle_no_intro TRAINER_GALAR_HOP_429, GalarTrn_G10M21_o9_Derrota
	end

GalarTrn_G10M21_o9_Fim:
	release
	end

GalarTrn_G10M21_o9_Derrota:
	.string "Minha estratégia vai direto ao buraco \nquando tenho todos esses pensamentos\lruins passando pela minha cabeça. $"

@ ---- Galar_StowOnSide09 ----
GalarTrn_G10M25_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALLISTER_310, GalarTrn_G10M25_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALLISTER_310, GalarTrn_G10M25_o12_Derrota
	end

GalarTrn_G10M25_o12_Fim:
	release
	end

GalarTrn_G10M25_o12_Derrota:
	.string "Estou feliz por ter minha máscara\n...Eu estava fazendo uma careta e\ltanto agora ...$"

@ ---- Galar_StowOnSide10 ----
GalarTrn_G10M27_o12::
	trainerbattle_single TRAINER_GALAR_BEA_27, GalarTrn_G10M27_o12_Intro, GalarTrn_G10M27_o12_Derrota
	end

GalarTrn_G10M27_o12_Intro:
	.string "Bea:Bem-vindo,Desafiante\nEu sou Bea.\pVocê tem um espirito\ninabalável que näo será\lquebrado,näo importa como\lvocê seja atacado.\pAcho que vou testar isso,devo?$"

GalarTrn_G10M27_o12_Derrota:
	.string "Bea:Obrigado pela batalha\nUfa...Enfrentar você me deu toda\la explicaçäo que eu\lprecisava.\pLutando contra você e\nsua equipe Eu näo\lesperava,mas,isso fez meu coraçäo\ldançar. \pbom ser inabalavel diante da batalha.\nMas é também bom ser levado\lpela batalha.Mais uma vez obrigado.$"

@ ---- Galar_Turffield05 ----
GalarTrn_G07M13_o2::
	trainerbattle_single TRAINER_GALAR_LASSA_114, GalarTrn_G07M13_o2_Intro, GalarTrn_G07M13_o2_Derrota
	end

GalarTrn_G07M13_o2_Intro:
	.string "I got up early every day to raise\nmy Pokémon from cocoons!$"

GalarTrn_G07M13_o2_Derrota:
	.string "What?\pWhat a total waste of time!$"

GalarTrn_G07M13_o4::
	trainerbattle_single TRAINER_GALAR_BRICE_186, GalarTrn_G07M13_o4_Intro, GalarTrn_G07M13_o4_Derrota
	end

GalarTrn_G07M13_o4_Intro:
	.string "Hahaha!\nVocê näo é um pouco duräo!!$"

GalarTrn_G07M13_o4_Derrota:
	.string "O que é isso?$"

GalarTrn_G07M13_o5::
	trainerbattle_single TRAINER_GALAR_ALICIA_154, GalarTrn_G07M13_o5_Intro, GalarTrn_G07M13_o5_Derrota
	end

GalarTrn_G07M13_o5_Intro:
	.string "You have Pokémon with you!\nYou’re mine!$"

GalarTrn_G07M13_o5_Derrota:
	.string "You deceived me…$"

GalarTrn_G07M13_o6::
	trainerbattle_single TRAINER_GALAR_ALAN_185, GalarTrn_G07M13_o6_Intro, GalarTrn_G07M13_o6_Derrota
	end

GalarTrn_G07M13_o6_Intro:
	.string "Hahahaha!\nPode vir!$"

GalarTrn_G07M13_o6_Derrota:
	.string "Hahahaha!\nVocê me venceu de forma justa!$"

GalarTrn_G07M13_o7::
	trainerbattle_single TRAINER_GALAR_JEREMY_465, GalarTrn_G07M13_o7_Intro, GalarTrn_G07M13_o7_Derrota
	end

GalarTrn_G07M13_o7_Intro:
	.string "Bwahaha!\nÓtimo! Fiquei entediado, né!$"

GalarTrn_G07M13_o7_Derrota:
	.string "Continue assim, hein!\pOh espere.\nEstou sem Pokémon!$"

@ ---- Galar_Turffield06 ----
GalarTrn_G07M14_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MILO_304, GalarTrn_G07M14_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MILO_304, GalarTrn_G07M14_o12_Derrota
	end

GalarTrn_G07M14_o12_Fim:
	release
	end

GalarTrn_G07M14_o12_Derrota:
	.string "O poder da grama foi murchado...$"

@ ---- Galar_TurffieldIndoor01 ----
GalarTrn_G13M08_o12::
	trainerbattle_single TRAINER_GALAR_MARNIE_76, GalarTrn_G13M08_o12_Intro, GalarTrn_G13M08_o12_Derrota
	end

GalarTrn_G13M08_o12_Intro:
	.string "Marnie: heh...Sabia que você seria\ncapa de pegar todas as insignias\le me encontrar aqui.\ptambem sei que muitas coisas\nocorreram entre n s dois com meu\lirmäo,com o team yell, a ajuda em\lspikemuth e tudo mais...\pMas a verdade é que quando tudo\nque foi dito for feito...\leu realmente quero me tornar a\lcampeän por conta propria entäo\lnäo leve pro pessoal quando eu te\lderrotar!$"

GalarTrn_G13M08_o12_Derrota:
	.string "Você me derrotou$"

@ ---- Galar_TurffieldIndoor02 ----
GalarTrn_G13M09_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_438, GalarTrn_G13M09_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_438, 0, GalarTrn_G13M09_o12_Derrota, GalarTrn_G13M09_o12_Vitoria
	end

GalarTrn_G13M09_o12_Fim:
	release
	end

GalarTrn_G13M09_o12_Derrota:
	.string "vamos lutar$"

GalarTrn_G13M09_o12_Vitoria:
	.string "You crushed me…$"

@ ---- Galar_TurffieldIndoor04 ----
GalarTrn_G13M14_o12::
	trainerbattle_single TRAINER_GALAR_JON_299, GalarTrn_G13M14_o12_Intro, GalarTrn_G13M14_o12_Derrota
	end

GalarTrn_G13M14_o12_Intro:
	.string "Twilight Wings foi um bom anime,\nnäo é?\peu sou Jon finalmente me curei da\nminha doença e agora sou um grande\ltreinador!$"

GalarTrn_G13M14_o12_Derrota:
	.string "Wow isso foi incrivel!!!$"

@ ---- Galar_TurffieldIndoor05 ----
GalarTrn_G13M15_o12::
	trainerbattle_single TRAINER_GALAR_TOMMY_300, GalarTrn_G13M15_o12_Intro, GalarTrn_G13M15_o12_Derrota
	end

GalarTrn_G13M15_o12_Intro:
	.string "Eu sou Tommy, Sou do anime de\nTwilight Wings, e agora eu vou\lganhar!!!$"

GalarTrn_G13M15_o12_Derrota:
	.string "Parabéns!$"

@ ---- Galar_TurffieldIndoor06 ----
GalarTrn_G13M16_o12::
	trainerbattle_single TRAINER_GALAR_ISADORA_22, GalarTrn_G13M16_o12_Intro, GalarTrn_G13M16_o12_Derrota
	end

GalarTrn_G13M16_o12_Intro:
	.string "Olá... Meu nome é Isadora!\pE você terá que batalhar comigo\naqui, e agora!$"

GalarTrn_G13M16_o12_Derrota:
	.string "Por sorte você conseguiu ganhar...$"

@ ---- Galar_TurffieldIndoor08 ----
GalarTrn_G13M19_o12::
	trainerbattle_single TRAINER_GALAR_LEON_739, GalarTrn_G13M19_o12_Intro, GalarTrn_G13M19_o12_Derrota
	end

GalarTrn_G13M19_o12_Intro:
	.string "Agora que eu vi que tipo de força\nvocê possui como o maior dos\ldesafiadores ... esmagá-lo na\lsujeira mostrará a todos o quäo\lforte seu campeäo realmente é!$"

GalarTrn_G13M19_o12_Derrota:
	.string "Meu tempo como campeäo acabou ...\nMas que tempo de campeäo tem sido!\p\nObrigado pela maior batalha\lque já tive!$"

@ ---- Galar_TurffieldIndoor09 ----
GalarTrn_G35M08_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ASH_402, GalarTrn_G35M08_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ASH_402, GalarTrn_G35M08_o12_Derrota
	end

GalarTrn_G35M08_o12_Fim:
	release
	end

GalarTrn_G35M08_o12_Derrota:
	.string "Foi uma batalha incrivel,\nespere so, batalharemos de novo\lalgum outro dia!$"

@ ---- Galar_TurffieldIndoor10 ----
GalarTrn_G35M09_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_RED_403, GalarTrn_G35M09_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_RED_403, GalarTrn_G35M09_o12_Derrota
	end

GalarTrn_G35M09_o12_Fim:
	release
	end

GalarTrn_G35M09_o12_Derrota:
	.string ".... .... ....\n.... .... ....$"

@ ---- Galar_TurffieldIndoor11 ----
GalarTrn_G35M10_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ETHAN_404, GalarTrn_G35M10_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ETHAN_404, GalarTrn_G35M10_o12_Derrota
	end

GalarTrn_G35M10_o12_Fim:
	release
	end

GalarTrn_G35M10_o12_Derrota:
	.string "Uau, tenho que melhorar mais,\nafinal, nunca se sabe quando\lalguém forte como você vai estar\lna minha frente novamente.$"

@ ---- Galar_TurffieldIndoor13 ----
GalarTrn_G35M12_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MISTY_406, GalarTrn_G35M12_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MISTY_406, GalarTrn_G35M12_o12_Derrota
	end

GalarTrn_G35M12_o12_Fim:
	release
	end

GalarTrn_G35M12_o12_Derrota:
	.string "QUê! näo pense que esse\nfoi nossa ultima batalha, eu\lainda terei uma revanche.$"

@ ---- Galar_TurffieldIndoor14 ----
GalarTrn_G35M13_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GREEN_407, GalarTrn_G35M13_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_GREEN_407, GalarTrn_G35M13_o12_Derrota
	end

GalarTrn_G35M13_o12_Fim:
	release
	end

GalarTrn_G35M13_o12_Derrota:
	.string "Ora ora, parece que eu subestimei\nvocê, mas näo fique täo convencido\lso porquê venceu uma vez.$"

@ ---- Galar_TurffieldIndoor16 ----
GalarTrn_G35M15_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HILDA_409, GalarTrn_G35M15_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_HILDA_409, GalarTrn_G35M15_o12_Derrota
	end

GalarTrn_G35M15_o12_Fim:
	release
	end

GalarTrn_G35M15_o12_Derrota:
	.string "Minha nossa, INCRiVEL, ter a\noportunidade de batalhar contra\ltreinadores como você, é realmente\lanimador!$"

@ ---- Galar_TurffieldIndoor17 ----
GalarTrn_G35M16_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_SERENA_421, GalarTrn_G35M16_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_SERENA_421, GalarTrn_G35M16_o12_Derrota
	end

GalarTrn_G35M16_o12_Fim:
	release
	end

GalarTrn_G35M16_o12_Derrota:
	.string "Oh...você é bem forte, agora o\nque me restou é torcer pela sua\lvitoria.$"

@ ---- Galar_TurffieldIndoor18 ----
GalarTrn_G35M17_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BROCK_422, GalarTrn_G35M17_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_BROCK_422, GalarTrn_G35M17_o12_Derrota
	end

GalarTrn_G35M17_o12_Fim:
	release
	end

GalarTrn_G35M17_o12_Derrota:
	.string "...\p...\pFoi uma otima batalha, espero que\ntenhamos outra algum dia.$"

@ ---- Galar_TurffieldIndoor19 ----
GalarTrn_G35M18_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CYNTHIA_423, GalarTrn_G35M18_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_CYNTHIA_423, GalarTrn_G35M18_o12_Derrota
	end

GalarTrn_G35M18_o12_Fim:
	release
	end

GalarTrn_G35M18_o12_Derrota:
	.string "Entäo você é o atual campeäo de\nGalar, de campeäo para campeäo, eu\lposso afirmar que essa foi umas\ldas melhores batalhas que eu\ljá fiz.$"

@ ---- Galar_TurffieldIndoor20 ----
GalarTrn_G35M19_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_IRIS_424, GalarTrn_G35M19_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_IRIS_424, GalarTrn_G35M19_o12_Derrota
	end

GalarTrn_G35M19_o12_Fim:
	release
	end

GalarTrn_G35M19_o12_Derrota:
	.string "NäO, NäO, NäO!!!\pEu esperava uma incrivel vitoria\nhoje, mas deveria ser a minha!!!$"

@ ---- Galar_TurffieldIndoor21 ----
GalarTrn_G35M20_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HILBERT_425, GalarTrn_G35M20_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_HILBERT_425, GalarTrn_G35M20_o12_Derrota
	end

GalarTrn_G35M20_o12_Fim:
	release
	end

GalarTrn_G35M20_o12_Derrota:
	.string "Nossa, isso foi inesperado, mas\nnäo pense que acaba aqui, ainda\ltenho tempo para ter outra batalha\lcontra você.$"

@ ---- Galar_TurffieldIndoor22 ----
GalarTrn_G35M21_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALAN_466, GalarTrn_G35M21_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALAN_466, GalarTrn_G35M21_o12_Derrota
	end

GalarTrn_G35M21_o12_Fim:
	release
	end

GalarTrn_G35M21_o12_Derrota:
	.string "Hmmm...nada mal, mas espere, um\ndia serei mais forte para outra\lbatalha.$"

@ ---- Galar_TurffieldIndoor23 ----
GalarTrn_G35M22_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_FELIPEMX_467, GalarTrn_G35M22_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_FELIPEMX_467, GalarTrn_G35M22_o12_Derrota
	end

GalarTrn_G35M22_o12_Fim:
	release
	end

GalarTrn_G35M22_o12_Derrota:
	.string "Sera que foi errado ter quebrado\na quarta parede no começo das\lminhas falas?$"

@ ---- Galar_TurffieldIndoor24 ----
GalarTrn_G35M23_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MAY_471, GalarTrn_G35M23_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MAY_471, GalarTrn_G35M23_o12_Derrota
	end

GalarTrn_G35M23_o12_Fim:
	release
	end

GalarTrn_G35M23_o12_Derrota:
	.string "Incrivel, treinadores como você\nsäo algo dificil de encontrar,\lespero ver você novamente.$"

@ ---- Galar_TurffieldIndoor25 ----
GalarTrn_G35M24_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BRENDAN_472, GalarTrn_G35M24_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_BRENDAN_472, GalarTrn_G35M24_o12_Derrota
	end

GalarTrn_G35M24_o12_Fim:
	release
	end

GalarTrn_G35M24_o12_Derrota:
	.string "Nossa, isso foi...$"

@ ---- Galar_TurffieldIndoor26 ----
GalarTrn_G35M25_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_DAWN_473, GalarTrn_G35M25_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_DAWN_473, GalarTrn_G35M25_o12_Derrota
	end

GalarTrn_G35M25_o12_Fim:
	release
	end

GalarTrn_G35M25_o12_Derrota:
	.string "OH....eu näo esperava por essa,\nainda tenho muito a aprender.$"

@ ---- Galar_TurffieldIndoor27 ----
GalarTrn_G35M26_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_STEVEN_485, GalarTrn_G35M26_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_STEVEN_485, GalarTrn_G35M26_o12_Derrota
	end

GalarTrn_G35M26_o12_Fim:
	release
	end

GalarTrn_G35M26_o12_Derrota:
	.string "Muito bom, foi uma otima batalha,\nque tenhamos outra igual a essa\lalgum dia.$"

@ ---- Galar_TurffieldIndoor28 ----
GalarTrn_G35M27_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LANCE_486, GalarTrn_G35M27_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_LANCE_486, GalarTrn_G35M27_o12_Derrota
	end

GalarTrn_G35M27_o12_Fim:
	release
	end

GalarTrn_G35M27_o12_Derrota:
	.string "Uma vitoria digna para um\ntreinador digno, meu parabéns\lgaroto.$"

@ ---- Galar_TurffieldIndoor29 ----
GalarTrn_G36M05_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PEONY_343, GalarTrn_G36M05_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_PEONY_343, GalarTrn_G36M05_o12_Derrota
	end

GalarTrn_G36M05_o12_Fim:
	release
	end

GalarTrn_G36M05_o12_Derrota:
	.string "Dessa vez näo vou esconder meu\nrosto, Apenas espero que minha\lfilha ainda tenha orgulho de mim…$"

@ ---- Galar_TurffieldIndoor30 ----
GalarTrn_G36M06_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_RAIHAN_338, GalarTrn_G36M06_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_RAIHAN_338, GalarTrn_G36M06_o12_Derrota
	end

GalarTrn_G36M06_o12_Fim:
	release
	end

GalarTrn_G36M06_o12_Derrota:
	.string "Eu fico bem assim mesmo quando\nperco. é uma verdadeira maldiçäo.\pAcho que é hora de outra selfie!$"

@ ---- Galar_TurffieldIndoor31 ----
GalarTrn_G36M07_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_AVERY_341, GalarTrn_G36M07_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_AVERY_341, GalarTrn_G36M07_o12_Derrota
	end

GalarTrn_G36M07_o12_Fim:
	release
	end

GalarTrn_G36M07_o12_Derrota:
	.string "E entäo você escala em direçäo  \nvitoria, nos deixando para trás.\pIsso me irrita, mas ... bravo.$"

@ ---- Galar_TurffieldIndoor32 ----
GalarTrn_G36M08_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MELONY_336, GalarTrn_G36M08_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MELONY_336, GalarTrn_G36M08_o12_Derrota
	end

GalarTrn_G36M08_o12_Fim:
	release
	end

GalarTrn_G36M08_o12_Derrota:
	.string "Eu acho que você interpretou\nquebrar o gelo um pouco\lliteralmente demais ...$"

@ ---- Galar_TurffieldIndoor33 ----
GalarTrn_G36M09_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GORDIE_339, GalarTrn_G36M09_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_GORDIE_339, GalarTrn_G36M09_o12_Derrota
	end

GalarTrn_G36M09_o12_Fim:
	release
	end

GalarTrn_G36M09_o12_Derrota:
	.string "Eu fui arrasado!Tenho orgulho de\nmeu Pokémon solido,e ainda assim…$"

@ ---- Galar_TurffieldIndoor34 ----
GalarTrn_G36M10_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LUCAS_347, GalarTrn_G36M10_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_LUCAS_347, GalarTrn_G36M10_o12_Derrota
	end

GalarTrn_G36M10_o12_Fim:
	release
	end

GalarTrn_G36M10_o12_Derrota:
	.string "meu esforço aqui foi mais\ninutil do que tentar evoluir um\lcombee macho.$"

@ ---- Galar_TurffieldIndoor35 ----
GalarTrn_G36M11_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_NESSA_307, GalarTrn_G36M11_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_NESSA_307, GalarTrn_G36M11_o12_Derrota
	end

GalarTrn_G36M11_o12_Fim:
	release
	end

GalarTrn_G36M11_o12_Derrota:
	.string "Eu näo entendo.\pO que eu tenho que fazer para\nvencer você, hein?$"

@ ---- Galar_TurffieldIndoor36 ----
GalarTrn_G36M12_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PIERS_337, GalarTrn_G36M12_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_PIERS_337, GalarTrn_G36M12_o12_Derrota
	end

GalarTrn_G36M12_o12_Fim:
	release
	end

GalarTrn_G36M12_o12_Derrota:
	.string "é isso?! Piers näo faz bis, mas\nadmito que estou tentado agora!$"

@ ---- Galar_TurffieldIndoor37 ----
GalarTrn_G36M13_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MILO_304, GalarTrn_G36M13_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MILO_304, GalarTrn_G36M13_o12_Derrota
	end

GalarTrn_G36M13_o12_Fim:
	release
	end

GalarTrn_G36M13_o12_Derrota:
	.string "O poder da grama foi murchado...$"

@ ---- Galar_TurffieldIndoor38 ----
GalarTrn_G36M14_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_VANESSA_348, GalarTrn_G36M14_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_VANESSA_348, GalarTrn_G36M14_o12_Derrota
	end

GalarTrn_G36M14_o12_Fim:
	release
	end

GalarTrn_G36M14_o12_Derrota:
	.string "que vontade de voar pra longe...$"

@ ---- Galar_TurffieldIndoor39 ----
GalarTrn_G36M15_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KABU_308, GalarTrn_G36M15_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_KABU_308, GalarTrn_G36M15_o12_Derrota
	end

GalarTrn_G36M15_o12_Fim:
	release
	end

GalarTrn_G36M15_o12_Derrota:
	.string "Bom Pokémon e um otimo Treinador!\pNäo é nenhuma surpresa que você\nganhou!$"

@ ---- Galar_TurffieldIndoor40 ----
GalarTrn_G36M16_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALLISTER_310, GalarTrn_G36M16_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALLISTER_310, GalarTrn_G36M16_o12_Derrota
	end

GalarTrn_G36M16_o12_Fim:
	release
	end

GalarTrn_G36M16_o12_Derrota:
	.string "Estou feliz por ter minha máscara\n...Eu estava fazendo uma careta e\ltanto agora ...$"

@ ---- Galar_TurffieldIndoor41 ----
GalarTrn_G36M17_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BEDE_312, GalarTrn_G36M17_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_BEDE_312, GalarTrn_G36M17_o12_Derrota
	end

GalarTrn_G36M17_o12_Fim:
	release
	end

GalarTrn_G36M17_o12_Derrota:
	.string "Por que eu tive a infelicidade\nde nascer na mesma época que você?$"

@ ---- Galar_TurffieldIndoor42 ----
GalarTrn_G36M18_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_C_PHENE_349, GalarTrn_G36M18_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_C_PHENE_349, GalarTrn_G36M18_o12_Derrota
	end

GalarTrn_G36M18_o12_Fim:
	release
	end

GalarTrn_G36M18_o12_Derrota:
	.string "parece que eu que foi enterrado...$"

@ ---- Galar_TurffieldIndoor43 ----
GalarTrn_G36M19_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALLANA_345, GalarTrn_G36M19_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALLANA_345, GalarTrn_G36M19_o12_Derrota
	end

GalarTrn_G36M19_o12_Fim:
	release
	end

GalarTrn_G36M19_o12_Derrota:
	.string "Há...que droga achei que ia ser\nfácil isso...$"

@ ---- Galar_TurffieldIndoor44 ----
GalarTrn_G36M20_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BEA_311, GalarTrn_G36M20_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_BEA_311, GalarTrn_G36M20_o12_Derrota
	end

GalarTrn_G36M20_o12_Fim:
	release
	end

GalarTrn_G36M20_o12_Derrota:
	.string "Seus Pokémon...eles säo täo\nfortes que säo praticamente\lvertiginosos!$"

@ ---- Galar_TurffieldIndoor45 ----
GalarTrn_G36M21_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARNIE_344, GalarTrn_G36M21_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARNIE_344, GalarTrn_G36M21_o12_Derrota
	end

GalarTrn_G36M21_o12_Fim:
	release
	end

GalarTrn_G36M21_o12_Derrota:
	.string "Estou perdendo para você desde o\nGym Challenge, e estou ficando um\lpouco farto!\pé melhor você lutar comigo de novo$"

@ ---- Galar_TurffieldIndoor46 ----
GalarTrn_G36M22_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALEXANDER_346, GalarTrn_G36M22_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALEXANDER_346, GalarTrn_G36M22_o12_Derrota
	end

GalarTrn_G36M22_o12_Fim:
	release
	end

GalarTrn_G36M22_o12_Derrota:
	.string "Que vergonha perder assim, acho\nque vou passar em spikemuth$"

@ ---- Galar_TurffieldIndoor47 ----
GalarTrn_G36M23_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MUSTARD_342, GalarTrn_G36M23_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MUSTARD_342, GalarTrn_G36M23_o12_Derrota
	end

GalarTrn_G36M23_o12_Fim:
	release
	end

GalarTrn_G36M23_o12_Derrota:
	.string "Fuhaha! Eu näo segurei\nabsolutamente nada, e ainda assim\lvocê me derrotou!\pO aprendiz supera seu mestre ...\pUm verdadeiro momento de orgulho\npara o mestre!$"

@ ---- Galar_TurffieldIndoor48 ----
GalarTrn_G36M24_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KLARA_340, GalarTrn_G36M24_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_KLARA_340, GalarTrn_G36M24_o12_Derrota
	end

GalarTrn_G36M24_o12_Fim:
	release
	end

GalarTrn_G36M24_o12_Derrota:
	.string "Nossa, forte como sempre!\pMas acho que estou começando a\nentender...Ei, obrigado por me\lajudar.$"

@ ---- Galar_TurffieldIndoor49 ----
GalarTrn_G39M01_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GREG_106, GalarTrn_G39M01_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_GREG_106, GalarTrn_G39M01_o12_Derrota
	end

GalarTrn_G39M01_o12_Fim:
	release
	end

GalarTrn_G39M01_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor50 ----
GalarTrn_G39M02_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CHAD_509, GalarTrn_G39M02_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_CHAD_509, GalarTrn_G39M02_o12_Derrota
	end

GalarTrn_G39M02_o12_Fim:
	release
	end

GalarTrn_G39M02_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor51 ----
GalarTrn_G39M03_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LEON_736, GalarTrn_G39M03_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_LEON_736, 0, GalarTrn_G39M03_o12_Derrota, GalarTrn_G39M03_o12_Vitoria
	end

GalarTrn_G39M03_o12_Fim:
	release
	end

GalarTrn_G39M03_o12_Derrota:
	.string "como eu disse a você antes ...\nHá verdadeiramente sem limites\lquando se trata de Pokémon!\pTodos nos vamos ter um tempo de\ncampeäo!$"

GalarTrn_G39M03_o12_Vitoria:
	.string "Vamos - lembre-se de nossa\npartida final! Isso é realmente o\lmelhor que você pode fazer ?!$"

@ ---- Galar_TurffieldIndoor52 ----
GalarTrn_G39M04_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KAYSER_113, GalarTrn_G39M04_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_KAYSER_113, GalarTrn_G39M04_o12_Derrota
	end

GalarTrn_G39M04_o12_Fim:
	release
	end

GalarTrn_G39M04_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor53 ----
GalarTrn_G39M05_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CONNER_115, GalarTrn_G39M05_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_CONNER_115, GalarTrn_G39M05_o12_Derrota
	end

GalarTrn_G39M05_o12_Fim:
	release
	end

GalarTrn_G39M05_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor54 ----
GalarTrn_G39M06_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_HOP_733, GalarTrn_G39M06_o12_Fim
	trainerbattle_earlyrival TRAINER_GALAR_HOP_733, 0, GalarTrn_G39M06_o12_Derrota, GalarTrn_G39M06_o12_Vitoria
	end

GalarTrn_G39M06_o12_Fim:
	release
	end

GalarTrn_G39M06_o12_Derrota:
	.string "Ugh! Estripado! Você está sempre\num passo a frente de mim, cara!$"

GalarTrn_G39M06_o12_Vitoria:
	.string "Mesmo as páginas que detalham\nminhas derrotas iräo adicionar a\lhist ria da minha lenda\lbrilhante!\pMas näo pretendo perder para você\nde novo!\pComo seu rival, prometo que\nvencerei da proxima vez!\pagora,{PLAYER},va para o hall da\nfama o leon vai te acompanhar!$"

@ ---- Galar_TurffieldIndoor55 ----
GalarTrn_G39M07_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ALEX_124, GalarTrn_G39M07_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_ALEX_124, GalarTrn_G39M07_o12_Derrota
	end

GalarTrn_G39M07_o12_Fim:
	release
	end

GalarTrn_G39M07_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor56 ----
GalarTrn_G39M08_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LIAM_142, GalarTrn_G39M08_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_LIAM_142, GalarTrn_G39M08_o12_Derrota
	end

GalarTrn_G39M08_o12_Fim:
	release
	end

GalarTrn_G39M08_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor57 ----
GalarTrn_G39M09_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BEDE_147, GalarTrn_G39M09_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_BEDE_147, GalarTrn_G39M09_o12_Derrota
	end

GalarTrn_G39M09_o12_Fim:
	release
	end

GalarTrn_G39M09_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor58 ----
GalarTrn_G39M10_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARKA_162, GalarTrn_G39M10_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARKA_162, GalarTrn_G39M10_o12_Derrota
	end

GalarTrn_G39M10_o12_Fim:
	release
	end

GalarTrn_G39M10_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor60 ----
GalarTrn_G39M12_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARNIE_165, GalarTrn_G39M12_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARNIE_165, GalarTrn_G39M12_o12_Derrota
	end

GalarTrn_G39M12_o12_Fim:
	release
	end

GalarTrn_G39M12_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor61 ----
GalarTrn_G39M13_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_WINSTON_166, GalarTrn_G39M13_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_WINSTON_166, GalarTrn_G39M13_o12_Derrota
	end

GalarTrn_G39M13_o12_Fim:
	release
	end

GalarTrn_G39M13_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor62 ----
GalarTrn_G39M14_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_DAWSON_167, GalarTrn_G39M14_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_DAWSON_167, GalarTrn_G39M14_o12_Derrota
	end

GalarTrn_G39M14_o12_Fim:
	release
	end

GalarTrn_G39M14_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_TurffieldIndoor63 ----
GalarTrn_G39M15_o12::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_RAIHAN_168, GalarTrn_G39M15_o12_Fim
	trainerbattle_no_intro TRAINER_GALAR_RAIHAN_168, GalarTrn_G39M15_o12_Derrota
	end

GalarTrn_G39M15_o12_Fim:
	release
	end

GalarTrn_G39M15_o12_Derrota:
	.string "Você ganhou!$"

@ ---- Galar_Wedgehurst08 ----
GalarTrn_G05M16_o7::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ARTHUR_23, GalarTrn_G05M16_o7_Fim
	trainerbattle_no_intro TRAINER_GALAR_ARTHUR_23, GalarTrn_G05M16_o7_Derrota
	end

GalarTrn_G05M16_o7_Fim:
	release
	end

GalarTrn_G05M16_o7_Derrota:
	.string "Wow!$"

@ ---- Galar_WildArea11 ----
GalarTrn_G42M04_o2::
	trainerbattle_single TRAINER_GALAR_LEROY_599, GalarTrn_G42M04_o2_Intro, GalarTrn_G42M04_o2_Derrota
	end

GalarTrn_G42M04_o2_Intro:
	.string "You look strong.\nLet me battle you, please!$"

GalarTrn_G42M04_o2_Derrota:
	.string "I knew it!\nYou’re as tough as I thought!$"

GalarTrn_G42M04_o3::
	trainerbattle_single TRAINER_GALAR_NICOLAS_521, GalarTrn_G42M04_o3_Intro, GalarTrn_G42M04_o3_Derrota
	end

GalarTrn_G42M04_o3_Intro:
	.string "This island is too spread out…\nIt’s not easy patrolling the place.$"

GalarTrn_G42M04_o3_Derrota:
	.string "Uh-huh…$"

@ ---- Galar_WildArea13 ----
GalarTrn_G42M06_o5::
	trainerbattle_single TRAINER_GALAR_MASON_590, GalarTrn_G42M06_o5_Intro, GalarTrn_G42M06_o5_Derrota
	end

GalarTrn_G42M06_o5_Intro:
	.string "Howdy!\nAre you a member of my fan club?$"

GalarTrn_G42M06_o5_Derrota:
	.string "Oh, so you’re not a fan…\pWell, I can change that.\nLet me sing for you!$"

@ ---- Galar_WildArea14 ----
GalarTrn_G42M07_o0::
	trainerbattle_single TRAINER_GALAR_CYNDY_591, GalarTrn_G42M07_o0_Intro, GalarTrn_G42M07_o0_Derrota
	end

GalarTrn_G42M07_o0_Intro:
	.string "My conditioning’s in top form!$"

GalarTrn_G42M07_o0_Derrota:
	.string "Huh?\nSomething’s not right…$"

GalarTrn_G42M07_o1::
	trainerbattle_single TRAINER_GALAR_EVAN_593, GalarTrn_G42M07_o1_Intro, GalarTrn_G42M07_o1_Derrota
	end

GalarTrn_G42M07_o1_Intro:
	.string "It doesn’t matter if you happen to\nhave the strongest Pokémon…\pIt doesn’t mean a thing if you don’t\nknow how to use them properly!$"

GalarTrn_G42M07_o1_Derrota:
	.string "You’re a master at this.$"

GalarTrn_G42M07_o3::
	trainerbattle_single TRAINER_GALAR_KATELYN_598, GalarTrn_G42M07_o3_Intro, GalarTrn_G42M07_o3_Derrota
	end

GalarTrn_G42M07_o3_Intro:
	.string "Those shoes you have are pretty\nsnazzy.$"

GalarTrn_G42M07_o3_Derrota:
	.string "You’re hot stuff in spite of your\ncute looks.$"

GalarTrn_G42M07_o6::
	trainerbattle_double TRAINER_GALAR_LEX_NYA_601, GalarTrn_G42M07_o6_Intro, GalarTrn_G42M07_o6_Derrota, GalarTrn_G42M07_o6_Poucos
	end

GalarTrn_G42M07_o6_Intro:
	.string "Lex: My darling Nya, together\nwe could win!$"

GalarTrn_G42M07_o6_Derrota:
	.string "Lex: I seem to have been too\ncareless…$"

GalarTrn_G42M07_o6_Poucos:
	.string "Lex: May I ask you to battle the\nboth of us at the same time?$"

GalarTrn_G42M07_o7::
	trainerbattle_double TRAINER_GALAR_LEX_NYA_601, GalarTrn_G42M07_o7_Intro, GalarTrn_G42M07_o7_Derrota, GalarTrn_G42M07_o7_Poucos
	end

GalarTrn_G42M07_o7_Intro:
	.string "Nya: I’ll do my best so I won’t\ndrag down my mentor, Lex!$"

GalarTrn_G42M07_o7_Derrota:
	.string "Nya: Oh, no…\nI’m so sorry, I…$"

GalarTrn_G42M07_o7_Poucos:
	.string "Nya: I’m sorry, but may we battle\nin two-on-two style?$"

@ ---- Galar_WildArea17 ----
GalarTrn_G42M10_o17::
	trainerbattle_single TRAINER_GALAR_MIAH_588, GalarTrn_G42M10_o17_Intro, GalarTrn_G42M10_o17_Derrota
	end

GalarTrn_G42M10_o17_Intro:
	.string "Kyahaha!\nI’ll flick you away effortlessly!$"

GalarTrn_G42M10_o17_Derrota:
	.string "Tch!\nToo strong for me!$"

GalarTrn_G42M10_o6::
	trainerbattle_double TRAINER_GALAR_EVE_JON_589, GalarTrn_G42M10_o6_Intro, GalarTrn_G42M10_o6_Derrota, GalarTrn_G42M10_o6_Poucos
	end

GalarTrn_G42M10_o6_Intro:
	.string "Eve: I’ll team up with Jon and\nbattle together.$"

GalarTrn_G42M10_o6_Derrota:
	.string "Eve: Me and Jon, we lost.\nEhehe.$"

GalarTrn_G42M10_o6_Poucos:
	.string "Eve: I want to team up with Jon\nwhen I battle you.\pCome back with two Pokémon, okay?$"

@ ---- Galar_WildArea21 ----
GalarTrn_G42M14_o3::
	trainerbattle_single TRAINER_GALAR_MADELINE_522, GalarTrn_G42M14_o3_Intro, GalarTrn_G42M14_o3_Derrota
	end

GalarTrn_G42M14_o3_Intro:
	.string "I punish people who abuse\nPokémon!$"

GalarTrn_G42M14_o3_Derrota:
	.string "You don’t seem to be a problem\nTrainer.$"

@ ---- Galar_WildAreaIndoor01 ----
GalarTrn_G39M16_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_MARCELO_AF_351, GalarTrn_G39M16_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_MARCELO_AF_351, GalarTrn_G39M16_o0_Derrota
	end

GalarTrn_G39M16_o0_Fim:
	release
	end

GalarTrn_G39M16_o0_Derrota:
	.string "parabéns vc e o melhor treinador\npokemon continue assim$"

@ ---- Galar_Wyndon01 ----
GalarTrn_G03M09_o22::
	trainerbattle_single TRAINER_GALAR_ISADORA_22, GalarTrn_G03M09_o22_Intro, GalarTrn_G03M09_o22_Derrota
	end

GalarTrn_G03M09_o22_Intro:
	.string "Olá... Meu nome é Isadora! E você\nterá que batalhar comigo aqui, e\lagora!$"

GalarTrn_G03M09_o22_Derrota:
	.string "Por sorte você conseguiu ganhar...$"

GalarTrn_G03M09_o7::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_ERIC_77, GalarTrn_G03M09_o7_Fim
	trainerbattle_no_intro TRAINER_GALAR_ERIC_77, GalarTrn_G03M09_o7_Derrota
	end

GalarTrn_G03M09_o7_Fim:
	release
	end

GalarTrn_G03M09_o7_Derrota:
	.string "I will crush you!!!$"

GalarTrn_G03M09_o8::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_FELIPE_78, GalarTrn_G03M09_o8_Fim
	trainerbattle_no_intro TRAINER_GALAR_FELIPE_78, GalarTrn_G03M09_o8_Derrota
	end

GalarTrn_G03M09_o8_Fim:
	release
	end

GalarTrn_G03M09_o8_Derrota:
	.string "I will crush you!!!$"

GalarTrn_G03M09_o9::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_VINICIUS_79, GalarTrn_G03M09_o9_Fim
	trainerbattle_no_intro TRAINER_GALAR_VINICIUS_79, GalarTrn_G03M09_o9_Derrota
	end

GalarTrn_G03M09_o9_Fim:
	release
	end

GalarTrn_G03M09_o9_Derrota:
	.string "I will crush you!!!$"

@ ---- Galar_Wyndon06 ----
GalarTrn_G33M02_o4::
	trainerbattle_single TRAINER_GALAR_ISADORA_22, GalarTrn_G33M02_o4_Intro, GalarTrn_G33M02_o4_Derrota
	end

GalarTrn_G33M02_o4_Intro:
	.string "Olá... Meu nome é Isadora! E você\nterá que batalhar comigo aqui, e\lagora!$"

GalarTrn_G33M02_o4_Derrota:
	.string "Por sorte você conseguiu ganhar...$"

@ ---- Galar_Wyndon10 ----
GalarTrn_G39M27_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_KALEDK_360, GalarTrn_G39M27_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_KALEDK_360, GalarTrn_G39M27_o0_Derrota
	end

GalarTrn_G39M27_o0_Fim:
	release
	end

GalarTrn_G39M27_o0_Derrota:
	.string "Parece que você e mais forte do\nque eu esperava...$"

@ ---- Galar_WyndonIndoor01 ----
GalarTrn_G39M17_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_GOLD_GAM2_0_352, GalarTrn_G39M17_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_GOLD_GAM2_0_352, GalarTrn_G39M17_o0_Derrota
	end

GalarTrn_G39M17_o0_Fim:
	release
	end

GalarTrn_G39M17_o0_Derrota:
	.string "Isso realmente foi fabuloso\nparabens$"

@ ---- Galar_WyndonIndoor02 ----
GalarTrn_G39M18_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PEDRO_GA_13_353, GalarTrn_G39M18_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_PEDRO_GA_13_353, GalarTrn_G39M18_o0_Derrota
	end

GalarTrn_G39M18_o0_Fim:
	release
	end

GalarTrn_G39M18_o0_Derrota:
	.string "O que eu perdi,minha perda e uma\ndesonra para os Pokemon de tipo\lfada$"

@ ---- Galar_WyndonIndoor03 ----
GalarTrn_G39M19_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PERG_PIKACH_354, GalarTrn_G39M19_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_PERG_PIKACH_354, GalarTrn_G39M19_o0_Derrota
	end

GalarTrn_G39M19_o0_Fim:
	release
	end

GalarTrn_G39M19_o0_Derrota:
	.string "Pergunte ao Pikachu: Nossa\nimpressionante suas abilidades\lcomo treinador Pokémon näo säo\lnada mal até outro dia!!$"

@ ---- Galar_WyndonIndoor04 ----
GalarTrn_G39M20_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_NEO_GIF_355, GalarTrn_G39M20_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_NEO_GIF_355, GalarTrn_G39M20_o0_Derrota
	end

GalarTrn_G39M20_o0_Fim:
	release
	end

GalarTrn_G39M20_o0_Derrota:
	.string "É, te subestimei, mas sua vitoria\nnäo conta se usou o SaveState.$"

@ ---- Galar_WyndonIndoor05 ----
GalarTrn_G39M21_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_FABIO_RODR_356, GalarTrn_G39M21_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_FABIO_RODR_356, GalarTrn_G39M21_o0_Derrota
	end

GalarTrn_G39M21_o0_Fim:
	release
	end

GalarTrn_G39M21_o0_Derrota:
	.string "Ja entendi como você derrotou os\noutros membros.$"

@ ---- Galar_WyndonIndoor06 ----
GalarTrn_G39M22_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_EDUARDO_357, GalarTrn_G39M22_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_EDUARDO_357, GalarTrn_G39M22_o0_Derrota
	end

GalarTrn_G39M22_o0_Fim:
	release
	end

GalarTrn_G39M22_o0_Derrota:
	.string "Uau...isso foi ate relaxante\nfazia tempo q näo tinha uma\lbatalha täo boa.$"

@ ---- Galar_WyndonIndoor08 ----
GalarTrn_G39M24_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PCL_G_50, GalarTrn_G39M24_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_PCL_G_50, GalarTrn_G39M24_o0_Derrota
	end

GalarTrn_G39M24_o0_Fim:
	release
	end

GalarTrn_G39M24_o0_Derrota:
	.string "Você usou savesate?\ncomo upou tanto?\lde qualquer forma parabens!!!$"

@ ---- Galar_WyndonIndoor09 ----
GalarTrn_G39M26_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BRENO_MENE_359, GalarTrn_G39M26_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_BRENO_MENE_359, GalarTrn_G39M26_o0_Derrota
	end

GalarTrn_G39M26_o0_Fim:
	release
	end

GalarTrn_G39M26_o0_Derrota:
	.string "Você ja ouviu falar da minha\nhack rom Pokemon Naki?$"

@ ---- Galar_WyndonIndoor10 ----
GalarTrn_G39M28_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_DEIDARA_YT_361, GalarTrn_G39M28_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_DEIDARA_YT_361, GalarTrn_G39M28_o0_Derrota
	end

GalarTrn_G39M28_o0_Fim:
	release
	end

GalarTrn_G39M28_o0_Derrota:
	.string "Parabens!!!$"

@ ---- Galar_WyndonIndoor12 ----
GalarTrn_G39M30_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CATZU_D_NE_363, GalarTrn_G39M30_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_CATZU_D_NE_363, GalarTrn_G39M30_o0_Derrota
	end

GalarTrn_G39M30_o0_Fim:
	release
	end

GalarTrn_G39M30_o0_Derrota:
	.string "Gahahaha... venceu dessa vez mas\nna proxima näo terá chance.$"

@ ---- Galar_WyndonIndoor13 ----
GalarTrn_G39M31_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_BISCOITOMOL_364, GalarTrn_G39M31_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_BISCOITOMOL_364, GalarTrn_G39M31_o0_Derrota
	end

GalarTrn_G39M31_o0_Fim:
	release
	end

GalarTrn_G39M31_o0_Derrota:
	.string "Meus biscoitos estäo amassados$"

@ ---- Galar_WyndonIndoor14 ----
GalarTrn_G39M32_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_SASUKEZIN69_365, GalarTrn_G39M32_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_SASUKEZIN69_365, GalarTrn_G39M32_o0_Derrota
	end

GalarTrn_G39M32_o0_Fim:
	release
	end

GalarTrn_G39M32_o0_Derrota:
	.string "Sasukezin69: nossa que doara essa\nbatalha!$"

@ ---- Galar_WyndonIndoor16 ----
GalarTrn_G39M34_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_LORD_367, GalarTrn_G39M34_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_LORD_367, GalarTrn_G39M34_o0_Derrota
	end

GalarTrn_G39M34_o0_Fim:
	release
	end

GalarTrn_G39M34_o0_Derrota:
	.string "Lord: A cara parece que eu perdi.$"

@ ---- Galar_WyndonIndoor17 ----
GalarTrn_G39M35_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_EURICO_368, GalarTrn_G39M35_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_EURICO_368, GalarTrn_G39M35_o0_Derrota
	end

GalarTrn_G39M35_o0_Fim:
	release
	end

GalarTrn_G39M35_o0_Derrota:
	.string "Eurico: Nossa que poder!!!$"

@ ---- Galar_WyndonIndoor18 ----
GalarTrn_G39M36_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CLOVES_369, GalarTrn_G39M36_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_CLOVES_369, GalarTrn_G39M36_o0_Derrota
	end

GalarTrn_G39M36_o0_Fim:
	release
	end

GalarTrn_G39M36_o0_Derrota:
	.string "Cloves: Parabéns campeäo!$"

@ ---- Galar_WyndonIndoor19 ----
GalarTrn_G39M37_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_JUAN_GRSON_370, GalarTrn_G39M37_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_JUAN_GRSON_370, GalarTrn_G39M37_o0_Derrota
	end

GalarTrn_G39M37_o0_Fim:
	release
	end

GalarTrn_G39M37_o0_Derrota:
	.string "Juan: Quero ver sem usar item!$"

@ ---- Galar_WyndonIndoor20 ----
GalarTrn_G39M38_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_CELINA_FER_371, GalarTrn_G39M38_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_CELINA_FER_371, GalarTrn_G39M38_o0_Derrota
	end

GalarTrn_G39M38_o0_Fim:
	release
	end

GalarTrn_G39M38_o0_Derrota:
	.string "Celina: adimito eu adoro pikachu$"

@ ---- Galar_WyndonIndoor21 ----
GalarTrn_G39M39_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_RUAN_POKE_372, GalarTrn_G39M39_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_RUAN_POKE_372, GalarTrn_G39M39_o0_Derrota
	end

GalarTrn_G39M39_o0_Fim:
	release
	end

GalarTrn_G39M39_o0_Derrota:
	.string "Ruan: Puts...$"

@ ---- Galar_WyndonIndoor22 ----
GalarTrn_G39M40_o0::
	lock
	faceplayer
	goto_if_set TRAINER_FLAGS_START + TRAINER_GALAR_PLANETA_POK_374, GalarTrn_G39M40_o0_Fim
	trainerbattle_no_intro TRAINER_GALAR_PLANETA_POK_374, GalarTrn_G39M40_o0_Derrota
	end

GalarTrn_G39M40_o0_Fim:
	release
	end

GalarTrn_G39M40_o0_Derrota:
	.string "Planeta P.:Caraca, você está de\nparabéns!$"

