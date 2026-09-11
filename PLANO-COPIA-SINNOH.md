# Frente C, cópia das cinco cidades de Sinnoh do Retro Platinum

Contrato: `Pokemon Claude/METODO-COPIA-CIDADES.md` (10/09/2026). Fonte:
`fontes-mapas/romhacks/retro-platinum/fonte`, clone do `master` de
https://github.com/sinnoh-remakes/pokeemerald-platinum no commit
`caece4fb104cf6285607465696df54294e47a7f6`, autor **blloop**. O Gui resolveu a
licença direto com o autor, que é amigo dele (resposta 73, de 11/09/2026): o
crédito vai no CREDITS.md e a frente segue sem trava.

As cinco cidades, por decisão do Gui (resposta 72): **Twinleaf, Sandgem,
Jubilife, Oreburgh e Floaroma**. As outras nove de Sinnoh ficam como estão.
A Oreburgh deles são DOIS mapas (norte e sul) e a nossa é um só: tem de fundir.

Este arquivo é o caderno da frente. Ele guarda o que foi MEDIDO, para ninguém
medir de novo nem presumir, e o que ainda está aberto.

## 1. A ferramenta

`dev_scripts/copia_cidade_fonte.py` lê o decomp da fonte e escreve a cópia aqui.

    python3 dev_scripts/copia_cidade_fonte.py --cidade JubilifeCity --demo
    python3 dev_scripts/copia_cidade_fonte.py --cidade JubilifeCity \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json \
        --converte --render <pasta>
    ... --aplicar --simbolo JubilifeSinnohRP

Etapas: leitura de três camadas, achatamento para duas, de-para do primário,
empacotamento do secundário novo, escolha de paleta, emissão (tileset novo,
registro em `graphics.h`, `metatiles.h` e `headers.h`, religação do layout,
escrita do `map.bin` e do `border.bin`). O layout é substituído NO LUGAR: o
`mapLayoutId` não muda, porque a save guarda o layout por id.

`--demo` roda as provas negativas (fronteira de VRAM em 512, metatile de 12
entradas, achatamento que compõe, tile fora da faixa saindo magenta) e
`--prova-fonte` compara o render da fonte com o render de referência dela, que
dá 0 pixel de diferença nos seis mapas.

## 2. O ponto cego da medida, achado em 11/09/2026

A ferramenta vinha dizendo **Jubilife 98,83%, Sandgem 94,91%, Twinleaf 94,33%**.
Os números eram falsos, e o defeito não estava na cópia: estava na CONTA.

A conta antiga descontava do denominador toda célula cujo metatile o de-para
tivesse trocado por um nosso, com a justificativa (correta em si) de que a
moldura de mata e de grama é nossa de propósito, por causa da costura. Só que é
exatamente ali que o de-para erra. Em **Sandgem**, os metatiles 24, 25 e 26 da
fonte, que são a rua de terra batida (esquerda, meio e direita), foram casados
por FUNÇÃO com os nossos 331, 289 e 333 do `general_sinnoh`, que são tábua de
madeira e pedrisco: a rua da cidade saiu de tábua, e a nota subiu para 94,91%
porque essas células saíram da conta. **Quanto mais o de-para trocasse, maior a
nota.** É a mesma família de erro da seção 0.ae do ESTADO ("tile nada a ver"),
com um número verde por cima.

A conta agora é por POSIÇÃO, que não dá para fraudar:

- **anel**: a faixa de `ANEL_COSTURA` = 8 tiles ao longo de cada borda que TEM
  conexão. É o que o motor desenha do outro lado (parado na rota, o jogador vê
  essa faixa da cidade com os tilesets da ROTA). Ali a arte tem de continuar
  sendo a nossa, e diferir da fonte é o certo. Fica fora da nota, reportado à
  parte.
- **interior**: todo o resto, inclusive as bordas SEM conexão (o oeste de
  Twinleaf, por exemplo, que rota nenhuma desenha). Ali a arte tem de ser
  DELES, e cada pixel diferente é erro.

O número do motor é **7**, não 8, e está lido, não presumido: `MAP_OFFSET` vale
7 em `include/fieldmap.h`, e `FillSouthConnection` (e as três irmãs) chamam
`FillConnection(..., width, MAP_OFFSET)` em `src/fieldmap.c`, ou seja copiam 7
linhas do mapa conectado para dentro do `gBackupMapLayout` do mapa atual. A
ferramenta usa `ANEL_COSTURA` = 8 de propósito, uma faixa a mais de margem.

## 3. Medidas, todas de 11/09/2026

### 3.1 Fidelidade real do desenho atual (primário compartilhado, de-para)

Anel contado só nos lados que TÊM conexão, que é a definição certa.

| mapa | interior | anel | limite de de-para escolhido | tiles no secundário |
|---|---|---|---|---|
| Jubilife | 84,30% | 24,59% | 0,40 | 512 de 512 |
| Sandgem | 62,31% | 18,35% | 0,10 | 512 de 512 |
| Twinleaf | 58,03% | 30,69% | 0,10 | 277 de 512 |
| Floaroma | 53,97% | 34,67% | 0,20 | 512 de 512 |
| Oreburgh norte | 34,11% | 12,32% | 0,10 | 512 de 512 |
| Oreburgh sul | 26,04% | 33,00% | 0,10 | 512 de 512 |

Cinco dos seis mapas enchem os 512 slots do secundário e continuam faltando
tile, o que é o mesmo que dizer que o teto é de orçamento.

### 3.2 Por que o desenho atual tem teto

A cidade copiada usa o NOSSO primário `gTileset_GeneralSinnoh`, e isso deixa
para a arte deles **7 paletas** (as 6-12) e **512 slots de tile** do secundário
novo. A arte que os mapas deles usam de verdade pede mais que isso:

| mapa da fonte | metatiles usados | tiles (t,paleta) distintos | cores distintas | paletas mínimas |
|---|---|---|---|---|
| Twinleaf | 137 | 300 | 90 | 6 |
| Sandgem | 232 | 565 | 117 | 8 |
| Jubilife | 314 | 515 | 109 | 8 |
| Oreburgh norte | 300 | 662 | 125 | 9 |
| Oreburgh sul | 220 | 585 | 123 | 9 |
| Floaroma | 270 | 548 | 148 | 10 |

Ou seja: **nenhuma das cinco cabe em 7 paletas, e quatro das seis não cabem em
512 tiles.** O que falta vira quantização e aproximação, e é isso que se vê no
render: a rua de tábua de Sandgem e o campo de flor de Floaroma virando mato.

### 3.3 O par de tilesets próprio (contrato, seção 3; medida do orçamento)

Dar a cada cidade um PAR próprio (primário novo + secundário novo) dobra o
orçamento para **13 paletas, 1024 tiles e 1024 metatiles**, e acaba com a
necessidade do de-para no interior. Em troca, os índices que a costura exige
passam a ter de ser PINADOS: o mesmo número de índice, desenhando a mesma
imagem de hoje, com o mesmo comportamento e o mesmo `layerType`.

Quantos índices são, medido mapa a mapa (faixa de 8 tiles do lado conectado de
cada rota vizinha, mais o `border.bin` dela, mais o anel da nossa cidade):

| cidade | índices da rota | índices do anel da cidade | união | cores que esses índices usam |
|---|---|---|---|---|
| Twinleaf | 29 | 62 | 73 | 36 |
| Sandgem | 33 | 89 | 102 | 24 |
| Jubilife | 64 | 132 | 166 | 47 |
| Oreburgh | 23 | 81 | 89 | 19 |
| Floaroma | 75 | 69 | 119 | 37 |

Orçamento do par próprio, medido:

| cidade | tiles nossos (costura) | tiles deles | total (teto 1024) | paletas depois de fundir só o que casa exato (teto 13) |
|---|---|---|---|---|
| Twinleaf | 128 | 300 | 428 | 16 |
| Sandgem | 183 | 565 | 748 | 18 |
| Jubilife | 235 | 515 | 750 | 17 |
| Floaroma | 195 | 548 | 743 | 19 |
| Oreburgh (norte + sul) | 194 | **1247** | **1441** | 26 |

Leitura honesta disso:

1. **O tile cabe** em quatro das cinco, com folga de 270 a 600 slots.
2. **A paleta não cabe de graça em nenhuma.** Fundir só os pares cuja união dá
   15 cores ou menos para em 16 a 19 paletas, e o teto é 13. Faltam de 3 a 6
   fusões, e essas têm de ser por COR APROXIMADA, com erro medido e mostrado.
   A soma de cores (nossa costura + arte deles) vai de 126 (Twinleaf) a 195
   (Floaroma) para 13 x 15 = 195 vagas de cor: Floaroma é o caso no limite.
3. **Oreburgh fundida não cabe**: 1441 tiles para 1024 vagas. A fusão dos dois
   mapas deles num só nosso precisa de decisão de recorte antes de qualquer
   conversão (ver a pergunta 92).

### 3.4 Animação de tileset

`gTileset_GeneralSinnoh` usa `.callback = InitTilesetAnim_General`, o mesmo do
`general` do Emerald. Esse callback reescreve, todo quadro, os slots de VRAM
**432 a 511** do primário: água 432-461, borda de areia com água 464-473, borda
de terra com água 480-489, cachoeira 496-501 e flor 508-511. Um primário novo
que guarde arte deles nessa faixa tem a arte apagada em tela. As duas saídas são
`.callback = NULL` (sem água nem flor animada na cidade copiada, e a água da
rota vizinha animando ao lado da parada, no anel) ou reservar os 80 slots com
uma cópia byte a byte dos nossos, que é o que mantém a costura idêntica. A
segunda é a certa e custa 80 dos 512 slots do primário novo.

### 3.5 Espaço de ROM

Medido na última ROM gravada (`roms/pokemon-claude-2026-09-08-c1-onda1.gba`):
33.554.432 bytes de cartucho, **29.585.124 usados e 3,79 MB livres**. Um par de
tilesets novo custa da ordem de 30 KB (tiles comprimidos, metatiles, atributos e
paletas), então as cinco cidades custam algo como 150 a 350 KB. Cabe com folga
larga. O que merece olho é a SOMA das cinco frentes de cópia rodando juntas: se
as cinco encherem na mesma proporção, dá de 1 a 2 MB, e aí a folga deixa de ser
confortável. Medir de novo na consolidação.

## 4. Arquivos da frente

- `dev_scripts/copia_cidade_fonte.py` — a ferramenta.
- `dev_scripts/depara_sinnoh_retro_platinum.json` — de-para do primário deles
  para o nosso, por função, com prova e distância de desenho. Três seções:
  `outdoor_jubilife` (117 metatiles, 179 tiles), `outdoor_oreburgh` (174, 292) e
  `outdoor_floaroma` (111, 222). Continua valendo para o ANEL mesmo no desenho
  de par próprio: é ele que diz qual metatile nosso corresponde a qual deles.
- `dev_scripts/dossies_sinnoh/<Cidade>.json` — o plano do JOGO de cada cidade:
  para onde vai cada warp, cada NPC, cada placa e cada gatilho na planta deles,
  quais prédios nossos são encaixados, quais portas deles ficam com placa
  `closed`, os offsets de conexão recalculados e a prova de alcance. Hoje só
  Jubilife está pronto.

## 5. O que a execução de cada cidade tem de entregar

Seções 4 e 5 do contrato, sem corte: commit na branch da frente com a árvore
conferida (~35.039 arquivos), render triplo em
`amostras-tileset/copia-cidades/feito/<Cidade>-antes-depois.png`, foto do
emulador em `feito/<Cidade>-emulador.png` (a cidade, cada conexão dos dois
lados, cada porta entrando, um NPC falando), prova de alcance, warp em porta e
NPC em chão andável, `valida_conectividade.py` com 0 quebrados, render das rotas
irmãs, build verde, `guarda_save.py` SAVE COMPATIVEL e um bloco de teste novo.
Blocos reservados para esta frente: **T260 a T269**. Nenhuma flag nem var nova.
