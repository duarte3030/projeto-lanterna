	.section .rodata

@ A ROM do Pokemon Colosseum (GameCube) vinha embutida aqui inteira, 160 KB, com
@ .incbin "data/mb_colosseum.gba". Ela serve para o GameCube pedir o programa por
@ multiboot quando o cabo esta ligado, em src/intro_frlg.c.
@
@ Cortada em 05/08/2026 por espaco de ROM: o cartucho tem 32 MB fisicos e o hack
@ estava em 94,71%. Este e o maior pedaco de ROM que nao e conteudo jogavel deste
@ hack, e ele so faz alguma coisa com um GameCube rodando Colosseum ligado por
@ cabo, que nao e o caso de uso aqui.
@
@ Os simbolos continuam existindo para o codigo que os cita compilar; o que some e
@ o payload. Se algum dia o multiboot for necessario, restaurar e devolver o
@ .incbin com o arquivo original, que segue em data/mb_colosseum.gba.
gMultiBootProgram_PokemonColosseum_Start::
	.4byte 0
gMultiBootProgram_PokemonColosseum_End::
