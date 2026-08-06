	.section .rodata

@ Aqui vinha embutido, com .incbin "data/mb_berry_fix.gba", um programa de
@ multiboot de 15 KB que NAO e deste projeto: e binario original de fabrica, e
@ servia para um cartucho mandar o conserto do bug da berry para outro por cabo
@ link. Este hack nao usa isso.
@
@ Removido em 05/08/2026, junto com a abertura do repositorio: binario de
@ fabrica publicado e o tipo de coisa que atrai pedido de remocao, e este aqui
@ nao paga nem os 15 KB que ocupa. O arquivo original ficou FORA do git, em
@ data/mb_berry_fix.gba, protegido pelo .gitignore.
@
@ Os simbolos continuam existindo para o codigo que os cita compilar; o que some
@ e o payload.
gMultiBootProgram_BerryGlitchFix_Start::
	.4byte 0
gMultiBootProgram_BerryGlitchFix_End::
