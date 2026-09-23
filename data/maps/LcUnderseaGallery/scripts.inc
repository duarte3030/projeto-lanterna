@ LcUnderseaGallery: mapa copiado de Pokémon Liquid Crystal.gba (g4m49) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ A porta em (2,40) é a escada para a LcUnderseaGlacier. O hack NÃO usava esse
@ tile como warp (ele existe na arte, com MB_SOUTH_ARROW_WARP e colisão 0, e
@ ficou sem evento), e foi aqui que a geleira ganhou entrada: no hack ela só se
@ alcançava pela poça sudeste do Chasm, que por sua vez só se alcançava por
@ warps para mapas do enredo do Liquid Crystal, que não entram.

LcUnderseaGallery_MapScripts::
	.byte 0

LcUnderseaGallery_EventScript_Drake::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_DRAKE, LcUnderseaGallery_Text_DrakeSeen, LcUnderseaGallery_Text_DrakeBeaten
	msgbox LcUnderseaGallery_Text_DrakeAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaGallery_EventScript_Gale::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_GALE, LcUnderseaGallery_Text_GaleSeen, LcUnderseaGallery_Text_GaleBeaten
	msgbox LcUnderseaGallery_Text_GaleAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaGallery_EventScript_GallerySign::
	msgbox LcUnderseaGallery_Text_GallerySign, MSGBOX_SIGN
	end

LcUnderseaGallery_Text_DrakeSeen:
	.string "The big ones come through here at\n"
	.string "high tide. You just missed them.\p"
	.string "Battle me instead.$"

LcUnderseaGallery_Text_DrakeBeaten:
	.string "You'd have beaten them too.$"

LcUnderseaGallery_Text_DrakeAfter:
	.string "A WAILORD came up this channel last\n"
	.string "spring and could not turn around.\p"
	.string "Took six of us two days to walk it\n"
	.string "back out to open water.$"

LcUnderseaGallery_Text_GaleSeen:
	.string "A mountain is a mountain, even with\n"
	.string "an ocean on top of it!$"

LcUnderseaGallery_Text_GaleBeaten:
	.string "Fair climb, fair fall.$"

LcUnderseaGallery_Text_GaleAfter:
	.string "There's a cold draught off that west\n"
	.string "stair. Cold enough to see your breath.\p"
	.string "Ice, under the sea. Explain that to me\n"
	.string "and I'll carry your bag.$"

LcUnderseaGallery_Text_GallerySign:
	.string "CORAL GALLERY\p"
	.string "“West stair: ice.\n"
	.string "Dress for it.”$"
