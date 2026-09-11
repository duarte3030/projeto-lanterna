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

## 3. Medidas, todas de 11/09/2026

### 3.1 Fidelidade real do desenho atual (primário compartilhado, de-para)

| mapa | interior | anel | limite de de-para escolhido |
|---|---|---|---|
| Jubilife | 84,30% | 24,59% | 0,40 |
| Sandgem | 66,03% | 24,51% | 0,10 |
| Floaroma | 59,32% | 39,74% | 0,20 |
| Twinleaf | 55,13% | 43,48% | 0,10 |
| Oreburgh norte | 42,81% | 19,66% | 0,10 |

(Medidas com o anel de 8 tiles nos quatro lados; com o anel só nos lados
conectados os números mudam, e a tabela é regravada quando a corrida fechar.)

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

### 3.5 O PAR PRÓPRIO construído e medido (11/09/2026)

O modo `--par-proprio` da ferramenta dá a cada cidade um primário NOVO e um
secundário NOVO. O orçamento passa a ser 13 paletas, 944 slots de tile (1024
menos os 80 da animação) e 1024 metatiles, e o interior deixa de precisar do
de-para: a arte de lá é a deles, copiada.

    python3 dev_scripts/copia_cidade_fonte.py --cidade JubilifeCity \
        --par-proprio --pinar-so-necessario \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json --render <pasta>
    ... --aplicar --simbolo JubilifeRetro

#### Fidelidade do interior, antes e depois

| mapa | antes (primário compartilhado) | depois (par próprio) |
|---|---|---|
| Twinleaf | 55,13% | **100,00%** |
| Sandgem | 66,03% | **98,00%** |
| Jubilife | 84,30% | **98,51%** |
| Floaroma | 59,32% | **97,42%** |
| Oreburgh norte (sozinha) | 42,81% | **98,71%** |
| Oreburgh sul (sozinha) | nunca medida | **99,89%** |

#### O que a costura exige, medido

Pinar significa: o mesmo NÚMERO de índice, desenhando a MESMA imagem de hoje,
com o mesmo `behavior` e o mesmo `layerType`. A PROVA C compara, metatile a
metatile, o par NOVO com o par de HOJE, e deu **0 pixel de diferença em 100% dos
índices pinados** nos seis mapas (Twinleaf 46, Sandgem 46, Jubilife 78,
Floaroma 83, Oreburgh norte 28, Oreburgh sul 29).

**O anel de HOJE não precisa ser pinado, e pinar custa caro.** O briefing pedia a
união de (a) o que a rota vizinha desenha e (b) o que a NOSSA cidade de hoje usa
no anel. Só que (b) deixa de existir no instante em que o `map.bin` é
substituído: quem a rota passa a desenhar é o anel do mapa NOVO, e esse entra no
conjunto pinado sozinho. A janela do motor é `MAP_OFFSET` 7, menor que os 8 do
`ANEL_COSTURA`, então a faixa medida cobre com folga. Custo de pinar o anel
velho, medido:

| cidade | com o anel velho | só o necessário |
|---|---|---|
| Twinleaf | 99,98% | 100,00% |
| Sandgem | 77,18% | 98,00% |
| Jubilife | 89,49% | 98,51% |
| Floaroma | 94,18% | 97,42% |

A flag `--pinar-so-necessario` liga a coluna da direita. Sem ela, o
comportamento continua sendo o do briefing.

#### O que aperta é a PALETA, não o tile

Nenhuma das seis chega perto dos 944 slots de tile (o máximo foi Oreburgh norte,
com 698; Jubilife ficou em 644). As 13 paletas, sim, fecham em todas: o mapa pede
de 111 (Twinleaf) a 179 (Floaroma) cores distintas para 13 x 15 = 195 vagas, e a
restrição de verdade é que TODA cor de um tile tem de caber numa paleta só.

O empacotador é aglomerativo (funde aos pares pelo menor tamanho de união,
desempate pela maior interseção), com fusão aproximada só quando não existe mais
nenhuma exata e nunca em balde que tenha cor de costura dentro. Ele roda duas
sementes e fica com a que RENDERIZA mais parecido: `cor` (um balde por conjunto
de cor distinto) e `paleta` (um balde por paleta de origem, que nasce com a arte
deles exata por construção). Nenhuma ganha sempre: Jubilife e Twinleaf fecham com
`cor`, Sandgem, Floaroma e as duas Oreburgh com `paleta`.

| cidade | paletas | verbatim | fusões exatas | aproximadas | pior erro de fusão | blocos quantizados | pior erro |
|---|---|---|---|---|---|---|---|
| Twinleaf | 13 | 1 | 152 | 3 | 2432 | 2 | 576 |
| Sandgem | 13 | 1 | 49 | 8 | 8768 | 58 | 6464 |
| Jubilife | 13 | 2 | 293 | 7 | 6336 | 177 | 6336 |
| Floaroma | 13 | 2 | 49 | 10 | 5632 | 177 | 3200 |
| Oreburgh norte | 13 | 0 | 60 | 7 | 4608 | 100 | 1856 |
| Oreburgh sul | 13 | 0 | 53 | 6 | 3200 | 16 | 2240 |

Nenhum bloco PINADO foi quantizado em mapa nenhum: 0 recusa.

#### A faixa de animação

`InitTilesetAnim_General` reescreve todo quadro os slots 432 a 511 do primário.
O primário novo reserva os 80 slots com uma cópia byte a byte dos nossos e mantém
`.callback = InitTilesetAnim_General`. A PROVA DA ANIMAÇÃO confere as duas
coisas: os 80 tiles são byte a byte iguais aos do `general_sinnoh`, e **nenhum
metatile do par novo aponta para a faixa fora dos que já apontavam hoje**
(0 intruso nos seis mapas). Como os bytes que o callback escreve são ÍNDICES de
cor fixos, a paleta que um metatile usa para desenhar um tile dessa faixa entra
no par novo VERBATIM, com as 16 entradas na mesma ordem.

#### O anel continua sendo a nossa arte, e isso é visível

O motor desenha o mapa conectado com os tilesets do mapa ATUAL. A rota usa o
`general_sinnoh`, então o que estiver no anel da cidade TEM de existir nele: a
faixa de 8 tiles da borda conectada é, por força, arte nossa. Onde o de-para não
cobre o metatile deles, o substituto sai de um VOCABULÁRIO restrito (os metatiles
que a rota vizinha e a borda da nossa cidade de hoje já usam), e não dos 512 do
primário inteiro: escolher entre os 512 pelo pixel mais próximo punha ponte, água
e escada de tijolo na borda de Jubilife, porque a única coisa parecida com
concreto azulado no `general_sinnoh` é justamente isso.

**Risco aberto, para o portão de gosto:** a borda LESTE de Jubilife, que encosta
na Rota 203, sai de tijolo e escada, porque é isso que o vocabulário da Rota 203
tem. O interior é cópia fiel; a moldura de 8 tiles é decisão de desenho, não
defeito de conversão.

#### Oreburgh: cada uma cabe sozinha, as duas juntas não

| mapa | tiles pedidos | de 944 | metatiles | interior |
|---|---|---|---|---|
| Oreburgh norte (72x32) | 698 | folga 246 | 314 no primário, 344 no secundário | 98,71% |
| Oreburgh sul (58x44) | 503 | folga 441 | 174 no primário, 344 no secundário | 99,89% |

Fundidas num mapa só continuam sem caber (1441 tiles para 944 vagas, medida de
3.3). O recorte é decisão do Gui, pergunta 92, e a ferramenta não inventa nada.

### 3.6 Jubilife aplicada, e a correção de dois números da mensagem do commit

`gTileset_JubilifeRetroPrim` + `gTileset_JubilifeRetroSec`, layout 74x66 no lugar
de 70x64, `mapLayoutId` intacto, `guarda_save.py` SAVE COMPATIVEL. Números
conferidos de novo DEPOIS do commit, rodando a ferramenta contra o estado
imediatamente anterior à aplicação:

| medida | valor |
|---|---|
| fidelidade do interior | 98,51% |
| semente de paleta escolhida | `cor` (a `paleta` dava 94,88%) |
| índices pinados | 78, e os 78 batem pixel a pixel e no atributo |
| tiles | 432 do primário + 212 do secundário = **644 de 944** |
| metatiles | **349** ocupados no primário (arquivo de 512) e **353** no secundário |
| paletas | 13, sendo 2 verbatim da animação |
| blocos quantizados | **177**, pior erro quadrático **6336** |

A mensagem do commit `37def5ac87` saiu com dois números velhos, de uma rodada
anterior à do vocabulário restrito do anel: disse "512 metatiles no primário" (é
349 ocupados) e "183 blocos quantizados, pior erro quadrático 10809" (é 177 e
6336). O resto da mensagem confere. E o commit `3889ef18a5` disse que trazia o
caderno junto com a ferramenta: não trouxe, porque a âncora do texto estava
escrita com dois `#` e a seção usa três, e o `replace` passou calado. As duas
coisas ficam registradas aqui, porque `--amend` é proibido nesta frente.

**O build não pôde ser conferido nesta máquina**, e não por causa desta mudança:
o `arm-none-eabi-gcc` 16.1.0 do Homebrew está sem libc, e `#include <string.h>`
falha até em `src/agb_flash.c`, que ninguém tocou. Não há newlib nem devkitARM
instalado (o INSTALL.md pede um toolchain com o subdiretório `arm-none-eabi`).
O que passou sem compilador: `tools/gbagfx` converteu os dois `tiles.png` (512 e
212 tiles, sem aviso de `num_tiles`) e as 32 paletas; `tools/compresSmol`
comprimiu o `.4bpp` do primário; `tools/mapjson` gerou `layouts.inc` com
`JubilifeCity_Layout` em 74x66 apontando para o par novo e `bigPrimary` FALSE; e
todo índice de metatile do `map.bin` e do `border.bin` cai dentro do que os dois
`metatiles.bin` oferecem (maior índice usado 498).

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
