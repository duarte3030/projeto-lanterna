	.section .rodata

	.align 2
@ Aqui vinha embutido, com .incbin "data/mb_ereader.gba", um programa de
@ multiboot de 12 KB que NAO e deste projeto: e binario original de fabrica, do
@ acessorio e-Reader. Este hack nao usa isso.
@
@ Removido em 05/08/2026 pelo mesmo motivo do mb_berry_fix e do mb_colosseum:
@ binario de fabrica publicado atrai pedido de remocao. Original fora do git, em
@ data/mb_ereader.gba, protegido pelo .gitignore.
gMultiBootProgram_EReader_Start::
	.4byte 0
gMultiBootProgram_EReader_End::
