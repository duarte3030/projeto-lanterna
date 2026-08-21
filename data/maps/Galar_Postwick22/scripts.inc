@ Gerado por dev_scripts/cenas_galar.py (bloco c3 da fase de
@ conteudo). Rodar dev_scripts/mundo_galar.py apaga este arquivo;
@ rodar cenas_galar.py --aplicar o repoe. Corpo das cenas em
@ data/scripts/galar_cenas.inc.

Galar_Postwick22_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Galar_Postwick22_Tabela4
	.byte 0

Galar_Postwick22_Tabela4:
	map_script_2 VAR_GALAR_G04M03_CENA, 1, GalarCena_G04M03_t4_v1
	.2byte 0
