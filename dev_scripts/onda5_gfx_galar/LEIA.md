# Onde estão os 58 PNG do lote R

Os **58 PNG** que o lote R da onda 5 gerou (o primeiro quadro de cada gráfico
recusado por descrição vaga, ampliado 8x e olhado um por um) **não moram no
repositório**. Eles são prova de trabalho, não fonte do build: nada em `make` os
lê, e binário de imagem não entra na árvore desta branch.

Eles estão fora do repo, em:

```
/Users/duarte/Projetos/pokemon-claude/fontes-mapas/galar-swsh/onda5-gfx/
```

Nomes `gfx_NNN.png`, onde `NNN` é o índice do gráfico na tabela viva do demake.

O que fica aqui é o **`laudo.json`**, que é texto e é a conclusão: para cada um
dos 58 gráficos, o que a imagem mostrou, a espécie ou categoria decidida e o
efeito na `dev_scripts/tabela_gfx_galar.py` (50 gráficos destravados, 8 sem arte
`OVERWORLD` correspondente). Quem for retomar a onda 5 lê o laudo; só precisa
abrir os PNG quem quiser conferir um julgamento visual específico.

Registrado em 07/09/2026, no fechamento e commit da onda 5 pausada.
