@ Gerado por dev_scripts/cenas_galar.py (bloco c3 da fase de
@ conteudo). Rodar dev_scripts/mundo_galar.py apaga este arquivo;
@ rodar cenas_galar.py --aplicar o repoe. Corpo das cenas em
@ data/scripts/galar_cenas.inc.

Galar_Hammerlocke05_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Galar_Hammerlocke05_Tabela2
	.byte 0

Galar_Hammerlocke05_Tabela2:
	map_script_2 VAR_GALAR_G09M11_CENA, 0, GalarCena_G09M11_t2_v0
	.2byte 0
