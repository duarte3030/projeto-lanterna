@ Gerado por dev_scripts/cenas_galar.py (bloco c3 da fase de
@ conteudo). Rodar dev_scripts/mundo_galar.py apaga este arquivo;
@ rodar cenas_galar.py --aplicar o repoe. Corpo das cenas em
@ data/scripts/galar_cenas.inc.

Galar_Circhester16_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Galar_Circhester16_Tabela2
	.byte 0

Galar_Circhester16_Tabela2:
	map_script_2 VAR_GALAR_G03M08_CENA, 3, GalarCena_G03M08_t2_v3
	.2byte 0
