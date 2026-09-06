@ A placa das PORTAS MORTAS de Galar, e ela e UMA SO para a regiao inteira.
@
@ Porta morta e warp que a fonte de Galar tem e que nao tem para onde levar aqui:
@ ou o destino e mapa vanilla do FireRed que o demake nao redesenhou, ou o warp
@ de chegada que a fonte cita nao existe no destino. O G3 apontou os 226 para
@ eles mesmos, e auto-warp em porta de verdade e defeito visivel: o jogador
@ encosta na porta, a tela apaga e ele reaparece no mesmo lugar.
@
@ O molde e o mesmo das 44 portas fechadas da rodada 13
@ (`dev_scripts/remove_mapas_cortados.py`, funcao `fecha_portas`): a entrada de
@ warp vira lapide na celula de um doador do proprio mapa, o tile da porta fica
@ sem warp em cima e uma placa `sign` na parede vizinha diz por que.
@
@ O TEXTO E O DO MASTER, e nao uma copia: `Common_Text_PortaFechada` mora em
@ `data/scripts/portas_fechadas.inc`, em ingles, porque o jogo fala ingles do
@ inicio ao fim (a unica fala em portugues que sobrava foi a que o Gui achou na
@ porta da igreja de Hearthome, no playtest de 06/09/2026). Aqui ha UM rotulo
@ para a regiao inteira em vez de um por mapa, que era so heranca de como o
@ gerador do corte funcionava.
GalarPortaFechada::
	msgbox Common_Text_PortaFechada, MSGBOX_SIGN
	end
