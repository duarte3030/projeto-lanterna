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

### 3.7 Espaço de ROM

Medido nesta branch, com build de verdade em 11/09/2026 (toolchain
`$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi` em
`DEVKITARM`, que é o que `dev_scripts/antes_de_empurrar.sh` usa):

| ROM | bytes usados | livres |
|---|---|---|
| controle da frente (HEAD antes de Jubilife) | 31.552.016 | 2,00 MB |
| com o par próprio de Jubilife aplicado | 31.583.424 | 1,97 MB |

O par de Jubilife custou **31.408 bytes**, ou seja 30,7 KB, e as cinco cidades
devem custar algo como 150 KB. Cabe com folga. O que merece olho é a SOMA das cinco frentes de cópia rodando juntas: se
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

## 6. Floaroma aplicada (11/09/2026), e o que ela mediu

### 6.1 A arte, com RECORTE

    python3 dev_scripts/copia_cidade_fonte.py --cidade FloaromaTown \
        --par-proprio --sem-conexao --recorte 0,0,34,38 \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json \
        --aplicar --simbolo FloaromaRetro

| medida | valor |
|---|---|
| planta | 42x44 na fonte, recorte `0,0,34,38`, layout 34x36 -> **34x38** |
| fidelidade do MAPA INTEIRO (sem conexão, tudo é interior) | **99,34%** (2.176 pixels de 330.752) |
| semente de paleta escolhida | `paleta` (a `cor` dava 98,97%) |
| tiles | 432 do primário + 85 do secundário + 80 reservados de animação = **517 de 944** |
| metatiles | **234** no primário, 1 no secundário |
| paletas | 13 de 13; 54 fusões exatas, 5 aproximadas, pior erro de fusão 9.216 |
| blocos quantizados | **40**, pior erro quadrático **6.208** |
| índices pinados | 0 (PROVA C sem objeto: a cidade não tem conexão) |
| PROVA DO TILE 0 | ok, slot 0 do primário novo vazio |
| ROM | 31.552.020 B no controle (HEAD 26f897bc88) -> 31.573.980 B, ou seja **+21.960 B** |

O recorte é a **exceção autorizada pela resposta 91 do Fable, e o motivo é medido**:
as colunas 34..41 e as linhas 38..43 da planta do autor estão ALÉM das setas de
saída que ele próprio desenhou (x=33 e y=37), e no nosso mundo são Route 205 e
Route 204. Sem o recorte a fidelidade cai para 98,88% e o tile sobe para 587.
**Este é o registro que o ESTADO tem de receber na consolidação.**

### 6.2 A animação de flor PARA, e é a maior perda visível

Medido, não estimado:

- Floaroma de HOJE: **48 células animadas**, todas de flor (metatile 4 do
  `general_sinnoh`, faixa de VRAM 508-511), **0 de água**.
- Floaroma do HACK dentro do recorte: **512 células** apontam para os 16 tiles
  que `InitTilesetAnim_Floaroma` reescreve (`TILE_OFFSET_4BPP(1)`, quatro
  quadros que diferem entre si: 327, 388 e 240 pixels de diferença do quadro 0
  para o 1, o 2 e o 3). São os campos de flor, quase 40% do mapa.
- Depois da cópia: **0 célula animada**. A PROVA DA ANIMAÇÃO diz "0 referências
  novas à faixa 432-511", ou seja nenhum metatile novo entra na faixa que o
  `InitTilesetAnim_General` reescreve, e os 80 slots continuam reservados.
- Água: 0 antes e 0 depois, então nada se perdeu ali.

Ou seja: a cidade ganha 99,34% de fidelidade de DESENHO e perde o movimento das
flores. Decisão de gosto do condutor e do Gui, não da execução. O conserto
possível (não feito) é pôr os 16 tiles de flor do autor dentro de 508-511 e
trocar o callback do primário novo, o que custa arte nova naquela faixa.

### 6.3 As saídas por warp, e a seta do autor

O Retro Platinum já resolvia a saída de Floaroma por seta, e as nove células
vieram na cópia: LESTE x=33 em y=25..28, SUL y=37 em x=10 e 12..14, e uma NORTE
interna em (22,17). A ferramenta reaproveitou o metatile de seta dele: **0
gêmeos mintados no primário da cidade**, 7 nos secundários das rotas.

    python3 dev_scripts/saidas_por_warp.py --cidade FloaromaTown \
        --offsets <json> --so-seta-do-autor --aplicar

**`--so-seta-do-autor` é nova, e nasceu de uma medida.** Sem ela a ferramenta
abria SETE saídas no sul, porque o recorte transforma chão de MEIO DE MAPA em
borda: (6,37), (7,37), (8,37) e (23,37) são andáveis dos dois lados e viravam
saída, mesmo sem seta nenhuma do autor e sem existirem no nosso jogo de hoje (a
borda sul da Floaroma de 34x36 é andável em x=10 e 12..14, e só). A flag restringe
a travessia às células que já têm o `MB_<DIR>_ARROW_WARP` da arte copiada; o
comportamento sem a flag não mudou (conferido rodando Twinleaf).

| saída | offset hoje | offset novo | conta lida nos dois `map.bin` | travessias |
|---|---|---|---|---|
| sul, MAP_ROUTE204 | 2 | **2** | `x_rota = x_cidade - 2`; 10,12,13 -> 8,10,11, que são andáveis no topo da Route 204 | **3** |
| leste, MAP_ROUTE205_SOUTH | -64 | **-60** | `y_rota = y_cidade + 60`; 25..28 -> 85..88, o mesmo corredor de hoje. Com -64 cairia em 89..92, que é parede | **4** |

A quarta seta do sul, (14,37), fica SEM warp: a célula espelhada na rota,
(12,0), tem um `object_event` (YOUNGSTER, índice 6) em cima. **Hoje essa coluna
também é intransponível**, pelo mesmo NPC, então não há regressão.

Mudança nas rotas irmãs, declarada: **3 células** na Route 204 ((8,0), (10,0),
(11,0)) e **4** na Route 205 South ((0,85..88)) trocam de índice de metatile
para o gêmeo de seta. Os gêmeos foram escritos em vagas que NENHUM layout da
árvore referencia (mauville_sinnoh 512-515, rustboro_sinnoh 513, 517, 519;
0 colisão com o uso do HEAD) e copiam as 8 palavras do chão original, então o
render das duas rotas dá **0 pixel de diferença**.

### 6.4 O jogo

Dossiê aplicado inteiro: 7 warps de porta nos MESMOS ids (só a coordenada desce
4 linhas), 15 `object_events` na MESMA ordem e nos mesmos índices, 4 `bg_events`
idem, `mapLayoutId` intacto, nenhuma flag e nenhuma var nova.
`guarda_save.py` diz **SAVE COMPATIVEL**.

No tileset novo: os metatiles de porta do autor (143, 196, 123, 124) foram
PROMOVIDOS de `MB_NON_ANIMATED_DOOR` para `MB_ANIMATED_DOOR`, e o metatile 52
(o centro do toldo da floricultura, que o hack desenhou sem warp) recebeu o
mesmo comportamento para receber o warp 3. Cada um desses metatiles é usado por
UMA ou DUAS células do mapa e por nenhuma da borda, conferido antes de mexer.
O metatile 147, a placa de cidade do autor, recebeu `MB_SIGNPOST`; as outras
três placas ficaram em `MB_NORMAL` bloqueante, porque as células para onde o
dossiê as empurrou são PAREDE DE PRÉDIO e não poste, conferido por recorte do
render.

**Aviso de gosto:** as 4 portas de Floaroma animavam hoje
(`MB_ANIMATED_DOOR` sobre metatiles do `general_sinnoh`, que têm entrada em
`sDoorAnimGraphicsTable`). O par novo não tem entrada nessa tabela e o Retro
Platinum não tem arte de porta abrindo (as portas dele são
`MB_NON_ANIMATED_DOOR`), então **a porta passa a não animar**. O warp funciona
(medido: T262.1 a T262.5 verdes) porque `StartDoorOpenAnimation` devolve -1 e
`Task_DoDoorWarp` trata `tDoorTask < 0`. Ligar a animação pede arte nova.

### 6.5 As provas, e os três achados que NÃO são da cópia

Verde: `make -j8` limpo (md5 da ROM `4ffef9ede56bb9e8e55ee52eef188182`),
`guarda_save.py` SAVE COMPATIVEL, `valida_conectividade.py` 0 warps quebrados,
`valida_warp_tile.py --piso 60` (Sinnoh 98,3%), `lente_warps.py` nenhum achado,
`valida_mapas_sinnoh.py` 0 mapas com problema e nenhuma linha de Floaroma nem
das duas rotas, render das rotas irmãs com 0 pixel de diferença, prova de
alcance a pé (841 células alcançadas das 910 andáveis com a moldura tapada;
14 de 14 warps, 15 de 15 objetos e 4 de 4 placas alcançáveis), bloco novo
**T262** (6 casos) e **T263** (5 casos) verdes, e os casos antigos que passam
pela cidade verdes depois de receberem a coordenada nova.

Achados abertos, todos MEDIDOS, nenhum criado por esta rodada:

1. **`lente_portas.py` acusa `trava` em FloaromaTown (22,17)**: "porta desenhada
   ao ar livre e sem warp: MB_NORTH_ARROW_WARP". É a seta INTERNA do autor,
   debaixo da porta da floricultura. `TryArrowWarp` não dispara sem
   `warp_event`, e quem responde ao UP naquela célula é a porta de (22,16), um
   tile ao norte (T262.5 prova). A lente conta a mesma classe em JubilifeCity,
   Route208, Route212_North, SnowpointCity e SpearPillar_Distorted: eram 5,
   passam a ser 6.
2. **`mapas_qa.py` ganha 17 achados E3 em Floaroma** ("bloco preto andável:
   metatile desenha por cima do jogador"), inclusive nas três células de saída
   leste (33,25), (33,26) e (33,28). Não é defeito de conversão: no
   `metatiles.bin` da FONTE esses metatiles têm fundo e meio VAZIOS e só a
   camada de TOPO preenchida, e o `DrawMetatile` do Retro Platinum
   (`src/field_camera.c`) IGNORA o `layerType` e manda a camada de topo para o
   BG1, que cobre sprite. Ou seja, o jogador some em cima do passadiço no jogo
   do autor também; a cópia reproduziu isso fielmente. É decisão de gosto, e a
   foto do emulador mostra o caso.
3. **`mapas_qa.py` ganha 2 achados C2 na Route 205 South** (as árvores de berry
   de (10,82) e (11,82) ficam inalcançáveis). Elas estão numa bolsa de elevação
   1 que só a BORDA ESQUERDA inteira alcançava, e a lente tratava toda a borda
   conectada como chegada. No jogo de verdade isso já era falso ANTES: a borda
   leste da Floaroma de 34x36 era andável só em y=21..24, que cai em y=85..88 da
   rota, tudo elevação 3. Medido: partindo das quatro células de travessia, a
   bolsa de 287 células (as berries dentro) não é alcançada nem hoje nem depois.
   A troca de conexão por warp só deixou a lente honesta.

Fora do escopo, mas anotado porque a foto do emulador mostrou: os interiores
**MAP_FLOAROMA_TOWN_MART** e **MAP_FLOAROMA_TOWN_HOUSE2** desenham a borda em
lixo magenta. O `border.bin` dos dois aponta para os metatiles 468, 469, 476 e
477, e o primário deles (`gTileset_Building`) tem **8** metatiles. Isso é
PREEXISTENTE: a ROM de controle (HEAD 26f897bc88) dá o mesmo quadro, 0 pixel de
diferença. A regra E1 do `mapas_qa.py` deveria pegar (ela existe para "metatile
fora do teto do tileset") e diz 0, porque ela lê só o `map.bin` e nunca o
`border.bin`.

## 7. Os consertos 93, 94 e a regra 3.2 (11/09/2026, condutor da onda 3)

Vieram das respostas 93 a 96 do Fable, que olhou Twinleaf e Floaroma e aprovou o
desenho, mas recusou três coisas. Cada uma virou um modo da ferramenta, e não uma
edição à mão, porque `--aplicar` regera o par inteiro e conserto fora da
ferramenta some na primeira regeração (foi o que aconteceu com a promoção das
portas de Floaroma, ver 7.4).

### 7.1 A ANIMAÇÃO DE FLOR VOLTA (`--anim-fonte`)

A perda registrada em 6.2 está desfeita: **512 células de Floaroma voltam a
animar**, que é exatamente o número que o hack anima dentro do recorte.

O que foi medido antes de escrever uma linha:

| medida | valor |
|---|---|
| o que `InitTilesetAnim_Floaroma` da fonte reescreve | 16 tiles a partir do slot **1** (`TILE_OFFSET_4BPP(1)`), 4 quadros, um a cada 32 quadros de tela |
| quadro 00 da fonte contra o `tiles.png` dela | **0 byte de diferença**: o quadro 0 É a arte parada |
| diferença entre quadros, na fonte | 327, 388 e 240 pixels do quadro 0 para o 1, o 2 e o 3 |
| palavras de metatile que pedem a faixa | 176, todas na camada do MEIO, todas na paleta 3 |
| dessas, CRUAS (o tile entra direto) | 1.684 células-palavra, 16 tiles distintos |
| dessas, COMPOSTAS (metatile de três camadas) | 364 células-palavra, **20 pares (fundo, flor) distintos** |

O segundo número é o que quase passou batido. O achatamento de três camadas funde
FUNDO com MEIO, e a flor mora no meio: sem tratamento, quase um quinto do campo de
flor viraria tile parado. A ferramenta passou a gerar um quadro COMPOSTO por
quadro de flor, e o par (fundo, flor) ganha slot próprio na faixa animada. São
**16 + 20 = 36 slots** dos 80 de 432 a 511.

A faixa deixa de guardar a cópia byte a byte dos nossos 80 slots (que o
`InitTilesetAnim_General` reescrevia sem ninguém desenhar, porque o par novo não
aponta para lá) e passa a guardar a arte animada DELE. O `.callback` do primário
vira `InitTilesetAnim_FloaromaRetro`, escrito em `src/tileset_anims.c` pela
própria ferramenta, e os quadros saem como PNG indexado em
`data/tilesets/primary/floaroma_retro_prim/anim/flowers/0k.png`.

**O DMA é quebrado em duas metades de 18 tiles**, nas fases 0 e 1 do mesmo período
de 32. As duas leem `timer / 32`, que é o MESMO valor nas duas fases, então as
metades nunca ficam em quadros diferentes; o que se ganha é não pedir 1.152 bytes
de DMA num VBlank só (a água do `general` pede 960).

PROVA DA ANIMAÇÃO DA FONTE, quatro afirmações medidas na camada em que valem:
quadro 0 bate byte a byte com o `tiles.png` do primário novo (senão a tela daria
um pulo no instante em que o callback roda pela primeira vez), os quadros 1 a 3
diferem do 0 em **714, 858 e 529 pixels**, **0** metatile aponta para a faixa fora
dos 36 slots, e **512 células do mapa animam**. No emulador, quatro fotos a 32
quadros de distância dão 1.115 e 1.398 pixels de diferença, e a quarta fecha o
ciclo voltando a 0.

### 7.2 O JOGADOR NÃO SOME MAIS (conserto de `layerType`)

`DrawMetatile` (`src/field_camera.c`) manda a camada de CIMA para o BG1 nos tipos
NORMAL e SPLIT, e o BG1 é desenhado acima de todo sprite de overworld. O autor do
Retro Platinum desenha passadiço, parede e telhado com as duas camadas de baixo
VAZIAS e só a de topo cheia, e o `DrawMetatile` DELE ignora o `layerType`: o
jogador some no jogo dele também. A cópia reproduziu isso fielmente, e fidelidade
ao hack não vale para jogador sumir.

A ferramenta passou a varrer, depois de escrever o `map.bin` novo, toda célula
ANDÁVEL (colisão 0) cujo metatile tem a camada de cima 100% opaca e a de baixo
vazia (ou repetida em 2 dos 4 quadrantes, que é a régua do `mapas_qa.py`). Esses
metatiles viram COVERED. **O desenho não muda um pixel**: com a camada de baixo
vazia, COVERED e SPLIT pintam os mesmos pixels, em BGs diferentes; o que muda é
quem fica na frente do sprite.

Três guardas, cada uma com motivo:

- só célula ANDÁVEL. Célula sólida com topo opaco é copa de árvore e beiral, e
  ali o topo TEM de ficar sobre o jogador: é assim que se passa atrás do prédio;
- metatile que serve aos DOIS papéis não é trocado nem escolhido no chute: a
  ferramenta MINTA um gêmeo COVERED (imagem idêntica, palavra por palavra) e manda
  só as células andáveis para ele. Twinleaf pediu 2 gêmeos (518 -> 632 em 18
  células, 519 -> 633 em 6) e Floaroma 3 (5 -> 235 em 56, 6 -> 236 em 48,
  11 -> 237 em 5);
- índice PINADO não é trocado, porque é da costura e a PROVA C compara o atributo.

Resultado medido com `dev_scripts/qa/mapas_qa.py`: **E3 vai de 17 para 0 em
Floaroma e de 26 para 0 em Twinleaf**, o total da árvore cai de 902 para 859, e
**nenhuma outra regra muda um achado** (o total de itens cai de 2.003 para 1.960,
que é exatamente os 43 E3).

### 7.3 TWINLEAF VOLTA PARA O SECUNDÁRIO (regra 3.2, `--so-secundario`)

A cidade cabe, e o número é este:

| medida | valor | teto |
|---|---|---|
| tiles | **273** | 512 |
| metatiles | **122** | 512 |
| paletas próprias | **7** | 7 (mais as 6 do primário compartilhado, de graça) |
| fidelidade do INTERIOR | **98,97%** | era 100,00% com par próprio |

O primário volta a ser o `gTileset_GeneralSinnoh` e **a conexão NORTE com a Route
201 volta a existir**: os três warps de seta (ids 4, 5 e 6) saíram do fim da lista
de Twinleaf, os três da Route 201 saíram junto, e o `map.bin` da Route 201 e o
`petalburg_sinnoh` voltaram ao estado do controle (os gêmeos de seta eram só
deles, conferido: `git diff ea8e664fad HEAD` nesses caminhos é vazio).

PROVA S (costura por primário compartilhado), que substitui a PROVA C neste modo:
**0 metatiles >= 512 no anel do mapa novo, 0 no de-para do anel e 0 na faixa que a
Route 201 desenha**. Índice alto de um lado seria desenhado com o secundário do
outro; a resposta certa aqui é "não existe nenhum" em vez de "são os mesmos".

O `gTileset_TwinleafRetroPrim` ficou sem dono e foi removido por
`dev_scripts/remove_tileset_registrado.py`, que RECUSA apagar tileset que algum
layout ainda usa. Eram 512 tiles e 512 metatiles de peso morto.

**A CONEXÃO SUL, com a Route 220, continua FECHADA, e isso é decisão, não
esquecimento.** Medido: com a arte do hack, a linha 33 de Twinleaf tem 8 células
de `MB_POND_WATER` em elevação 1 que casam, coluna a coluna, com 8 de
`MB_OCEAN_WATER` em elevação 1 no topo da Route 220. Devolver a conexão abriria
uma travessia de SURF que o jogo de hoje não tem (a borda sul da Twinleaf de
24x30 não tinha uma única célula andável). Passagem nova é decisão do Gui, não da
execução: é a pergunta 97.

**O preço da regra 3.2, e ele é visível:** a faixa de 8 tiles da borda conectada é,
por força, arte do primário compartilhado. São as 8 primeiras linhas de Twinleaf,
23% da altura da cidade, e lá o canteiro de flor branca e a cerca do autor viram
arte nossa. A costura com a Route 201 fica perfeita (a prancha
`TwinleafTown-costura-Route201.png` mostra a grama, a árvore e o caminho
continuando), mas fica uma linha de tom de grama dentro da cidade, na fronteira do
anel. Comparação lado a lado em
`amostras-tileset/copia-cidades/feito/DECISAO-Twinleaf-anel-regra-3.2.png`.

Quatro metatiles do anel foram julgados NA MÃO, em
`dev_scripts/anel_sinnoh_retro.json`, porque a conta errou feio:

| fonte | conta escolheu | julgado | por quê |
|---|---|---|---|
| 17 (grama sobre areia, no alto do caminho) | 9 | **289** | o 9 é o TOLDO LISTRADO de barraca: duas células de listra laranja plantadas no meio da rua |
| 9 (canteiro de flor branca) | 1 (grama lisa) | **4** | o 4 é flor sobre grama e ainda é um dos metatiles que o `InitTilesetAnim_General` anima |
| 598 e 606 (poste de cerca) | 111 | **1** | o 111 tem uma PEDRA MARROM no meio da grama, aparecendo do nada na entrada da cidade |

### 7.4 A TABELA DE COMPORTAMENTO, e o conserto que tinha sumido

`--aplicar` regera o `metatile_attributes.bin` inteiro. As promoções de porta de
Floaroma (143, 196, 52, 123 e 124 para `MB_ANIMATED_DOOR`) e a placa 147
(`MB_SIGNPOST`) tinham sido feitas fora da ferramenta e **morreram na primeira
regeração**. Agora elas moram em `dev_scripts/comportamentos_sinnoh_retro.json`,
com o porquê de cada linha, e a ferramenta as aplica depois da arte.

Dois defeitos de emissão que só apareceram ao REAPLICAR uma cidade já registrada,
os dois medidos e consertados:

1. `registra_tileset_par` pulava o tileset que já existia, então o `.callback`
   continuava `InitTilesetAnim_General` com a arte animada do autor na faixa: o
   callback escrevia água e flor do `general_sinnoh` por cima dela, todo quadro.
   A emenda que troca o campo tinha o regex `\.callback = [^;]*;`, e o `[^;]*`
   engolia a linha seguinte e o `};` do struct inteiro. O fim do campo é a
   VÍRGULA, não o ponto e vírgula.
2. o `-num_tiles` também ficava velho. O secundário de Floaroma foi de 85 para 49
   tiles quando a arte animada saiu para a faixa, e o `gbagfx` parou o build com
   "The specified number of tiles (85) is greater than the maximum possible value
   (64)".

### 7.5 O que ficou aberto

- **3 conflitos de camada em Floaroma viraram gêmeos** (metatiles 5, 6 e 11), mas
  o `mapas_qa.py` nunca os acusou: as células andáveis deles não são alcançáveis
  pela busca do E3. A troca é gratuita e mais correta, e está registrada aqui para
  ninguém procurar de novo.
- **O jogador fica VISÍVEL EM CIMA do telhado** nas células que o autor deixou com
  colisão 0 (foto em `FloaromaTown-emulador.png`, painel "sobre o passadiço"). É
  melhor do que sumir, e é o que a resposta 94 mandou; o conserto de verdade seria
  fechar a colisão dessas células, que muda o mapa andável do autor. Pergunta 98.

## 8. As portas ABREM (conserto 95, executor de 11/09/2026)

O "aviso de gosto" da seção 6.4 (a porta copiada não anima) está RESOLVIDO, e
Twinleaf entrou junto. Ferramenta nova: `dev_scripts/porta_anima_copiada.py`,
re-rodável, que compõe a porta fechada a partir do par de tilesets do disco,
deriva os três quadros de abertura, grava `graphics/door_anims/<slug>.png`
(16x96, indexado) e imprime a linha do `sDoorAnimGraphicsTable` e o
`sDoorAnimPalettes_*`. Depois de regerar um par, rodar o script de novo.

    python3 dev_scripts/porta_anima_copiada.py --prova --rebaixa

### 8.1 A porta de UMA CÉLULA (`DOOR_SIZE_ONE_CELL`), e a medida que a exigiu

`sDoorAnimGraphicsTable` casa só metatile + tileset (`GetDoorGraphics`,
`src/field_door.c`), e `size` 1 REDESENHA a célula de cima. Medido no `map.bin`:
o mesmo metatile de porta aparece debaixo de paredes diferentes.

| porta | células | metatile ACIMA | pixels diferentes |
|---|---|---|---|
| Floaroma 143 | (26,23) Loja / (18,32) Centro | 163 / 135 | **249 de 256** |
| Floaroma 196 | (13,20) Casa 1 / (26,32) Casa 2 | 190 / 226 | 0 de 256 |
| Twinleaf 78 | (5,13) e (16,23) / (16,13) e (6,23) | 71 / 113 | **229 de 256** |

Com `size` 1, três das sete células de porta piscariam a parede do prédio
errado durante a animação. Medido também que a folha da porta cabe INTEIRA no
metatile de baixo nas três (a célula de cima é parede e telhado), então
`src/field_door.c` ganhou `size` 0: o motor anima só o metatile de baixo e a
parede fica intacta em todas as células. A prova no emulador mostra a Loja
(parede azul) e o Centro (parede laranja) abrindo a MESMA porta, cada um com a
sua parede.

### 8.2 A arte, e o que ela custou de quantização

Regra mecânica, sem arte inventada: o vão escurece com a cor mais escura da
paleta do quadrante. A porta de madeira (Floaroma 196, Twinleaf 78) escurece de
cima para baixo, e a de vidro (Floaroma 143, que é do Centro e da Loja) corre
para os lados com `DOOR_SOUND_SLIDING`. As linhas de CHÃO de baixo (soleira e
grama) nunca escurecem, como o quadro aberto da porta de fábrica também não
escurece o chão do vão.

| porta | paletas dos 4 quadrantes | pior erro de quadrante |
|---|---|---|
| Floaroma 143 (vidro) | 12, 12, 12, 12 | **0**, cabe exata |
| Floaroma 196 (madeira) | 11, 11, 5, 5 | 7.168 (marrom deslocado 128 por pixel) |
| Twinleaf 78 (madeira) | 10, 10, 1, 1 | 20.992 (marrom 128 e 320; a soleira, 8 pixels, 1.280) |

A quantização existe porque o quadrante junta cores de DUAS paletas (o chão da
camada de baixo e a folha da camada de cima), e o hardware dá uma paleta por
tile de 8x8. Nenhuma paleta do par contém as duas famílias.

### 8.3 As três "portas" que não eram porta

`52` (centro do toldo da floricultura), `123` e `124` (o vão entre as árvores
para o Floaroma Meadow) foram rebaixadas de `MB_ANIMATED_DOOR` para
`MB_NON_ANIMATED_DOOR` no `metatile_attributes.bin` do primário de Floaroma,
pela opção `--rebaixa` do script (nunca à mão, porque o par é regerado).
`MB_NON_ANIMATED_DOOR` continua sendo comportamento de warp
(`IsWarpMetatileBehavior`, `src/field_control_avatar.c`), e as três células têm
colisão 0, então o warp dispara quando o jogador PISA nelas. Provado no
emulador depois do rebaixamento: T262 6/6 (inclui o T262.5, a floricultura),
T148 12/12 e T181 6/6 (os do Floaroma Meadow) e T263 5/5.

### 8.4 A armadilha do `#else`, que quase passou verde

O bloco da tabela é `#if !IS_FRLG` ... `#else` ... `#endif // !IS_FRLG`. Pôr as
entradas "antes do `#endif`" as põe no ramo do FRLG, que NÃO compila nesta
build: elas somem caladas, a ROM não cresce um byte e os testes de warp
continuam verdes, porque o warp nunca dependeu da animação. Quem pegou foi a
conta de bytes contra o controle (0 em vez de +2.400). As entradas vão no fim do
PRIMEIRO ramo, logo antes do `#else`, e o script imprime esse aviso.

### 8.6 O que mudou na integração com a onda 3 do condutor (11/09/2026)

O executor das portas trabalhou em cima do par de Twinleaf ANTERIOR à regra 3.2.
Ao integrar, três coisas foram refeitas, e todas estão medidas:

1. **A porta de Twinleaf mudou de número e de tileset.** Era o metatile 78 do
   `gTileset_TwinleafRetroPrim`, que deixou de existir; passa a ser o **576**
   (local 64) do `gTileset_TwinleafRetroSec`. `GetDoorGraphics` compara o tileset
   com o primário OU o secundário do layout, então a entrada com o secundário
   casa do mesmo jeito.
2. **A quantização dela caiu de 20.992 para ZERO.** Com o primário compartilhado,
   as 6 paletas do `general_sinnoh` ficam disponíveis para os quadrantes: as
   escolhas passam de `{10,10,1,1}` para `{2,7,9,9}`, todas exatas.
3. **O rebaixamento das não-portas saiu do script e entrou na tabela**
   (`dev_scripts/comportamentos_sinnoh_retro.json`), junto com a promoção das que
   SÃO porta. O `--rebaixa` do script continua funcionando e é idempotente, mas o
   dono da verdade passa a ser a tabela, que a ferramenta de cópia aplica em toda
   regeração. `porta_anima_copiada.py` também deixou de chutar
   `gTileset_<simbolo>Prim`/`Sec` e passou a ler o par do `layouts.json`, que é o
   que serve aos dois arranjos.

As imagens do portão de gosto ficam no workspace, em
`amostras-tileset/copia-cidades/feito/`, e NÃO no repositório: a árvore do HEAD
não tem nenhuma, e o executor as tinha commitado por engano.

### 8.7 O T187.11, que é vermelho e NÃO é desta frente

A suíte inteira fechou **838 de 840** na ROM desta onda. Os dois vermelhos:

- **T100.3 e T100.4** estavam com o roteiro medido no map.bin de 24x30 de
  Twinleaf, que deixou de existir na onda anterior. Refeitos por busca em largura
  no map.bin novo e o bloco T100 volta a **16 de 16**. Registro honesto: o
  T100.4 já estava vermelho no HEAD `8305fa9c70`, porque lá a cidade não tinha
  conexão nenhuma e o caso PEDE que o jogador saia a pé pela borda norte; quem o
  devolveu ao verde foi a regra 3.2.
- **T187.11 continua vermelho, e não é conserto desta frente.** Ele prova que a
  música de vitória é da região lendo o DRIVER de som depois de ganhar uma
  batalha selvagem em Eterna Forest, contando quadros. A seção 0.x do ESTADO já
  o descreve como loteria de contagem de quadro: "dez apertos ficam VERDES na ROM
  base e VERMELHOS na desta onda", e a receita de então foi remedir o número de
  apertos de A. **Desta vez remedir não resolve:** varri 11, 12, 13, 14, 15, 16,
  18, 20, 24 e 28 apertos e TODOS leem a faixa 744 (`MUS_DP_VS_WILD`), ou seja a
  batalha nunca termina, em vez de terminar cedo ou tarde. O diff desta onda não
  tem um único arquivo de som, de batalha ou de tabela de música (conferido com
  `git diff --name-only`), então a causa está fora daqui. Vai para a fila de bugs
  do ESTADO, com a medida acima, e o arquivo do caso ficou como estava.

## 10. Oreburgh aplicada (11/09/2026, executor OREBURGH da onda 4)

A cidade INTEIRA deles entrou, os dois mapas fundidos num só nosso, e **nada do
desenho foi cortado**: a pilha de carvão do pátio, que a receita de `--fundir`
apagava, voltou. Quem fez caber foi a resposta 92 do Fable, na ordem que ela
mandou: fundir metatile quase idêntico ATÉ CABER, e só cortar se ainda faltasse.

    python3 dev_scripts/copia_cidade_fonte.py --cidade OreburghCity \
        --fundir --par-proprio --sem-conexao --sem-animacao --sem-cortes \
        --funde-metatiles 60000 \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json \
        --aplicar --simbolo OreburghRetro
    python3 dev_scripts/saidas_por_warp.py --cidade OreburghCity \
        --offsets <json com MAP_ROUTE207: 39> --apesar-de MB_BERRY_TREE_SOIL --aplicar

### 10.1 A medida que decidiu o caminho (par próprio, e não a regra 3.2)

A regra 3.2 do contrato manda tentar primeiro a cidade inteira no SECUNDÁRIO,
compartilhando o primário com a vizinha. Em Oreburgh isso não existe, e a
medida é esta, refeita nesta rodada e não herdada:

| medida | valor |
|---|---|
| vizinhas de Oreburgh | UMA, `up -> MAP_ROUTE207`, offset 35 |
| metatiles que a Route 207 usa do secundário dela (`gTileset_Jubilife`) | **15** (515, 516, 517, 521, 523, 524, 536, 850, 852, 853, 855, 859, 860, 861, 868), em **264 células** |
| índices >= 512 na faixa da rota que a cidade desenha | **3** (515, 516, 521) |
| arte que a fusão pede | 1.097 blocos de 8x8 distintos, para as 512 vagas de um secundário |

Apontar a Route 207 para um par novo arrastaria o `gTileset_Jubilife` inteiro
junto, e parado na cidade a faixa da rota traz três índices que um secundário
novo de Oreburgh não teria. Então: **par próprio, e a saída norte vira warp**.

### 10.2 A FUSÃO DE METATILE QUASE IDÊNTICO (resposta 92), medida e listada

`--funde-metatiles LIMIAR` é nova na ferramenta. Depois de montado o vocabulário
do mapa, ela agrupa metatiles cuja distância de pixel é pequena e aponta as
células do mapa para o representante (o mais USADO do grupo). Duas guardas: só
funde metatile com o MESMO atributo da fonte e o MESMO `layerType` depois do
achatamento, e a nota de fidelidade continua sendo tirada contra a arte do autor
ANTES da fusão (`d["blocos_alvo"]`), senão fundir sempre daria 100% e a régua
viraria a mesma fraude da seção 2.

A régua é o erro quadrático somado sobre os 256 pixels RGB do metatile achatado.
Varredura do limiar, com a cidade inteira (sem corte nenhum) e `--sem-animacao`:

| limiar | fusões (erro 0 / aprox.) | blocos de 8x8 | cabe nos 1.024? | fidelidade |
|---|---|---|---|---|
| sem fundir | 0 | 1.097 | **não**, 27 blocos sem slot | 98,19% |
| 0 | 78 / 0 | 1.097 | **não**, 27 sem slot | 98,15% |
| 25.000 | 72 / 14 | 1.090 | não, 21 sem slot | 98,11% |
| 50.000 | 72 / 29 | 1.072 | não, 8 sem slot | 98,36% |
| **58.000** | 71 / 35 | 1.065 | **sim**, 1.023 de 1.024 | 98,35% |
| 60.000 (o escolhido) | 71 / 36 | 1.064 | sim, 1.023 de 1.024 | **98,35%** |
| 90.000 | 71 / 52 | 1.041 | sim, 999 | 98,18% |
| 200.000 | 64 / 101 | 982 | sim, 950 | 97,96% |

Duas coisas que a tabela diz e que não eram óbvias:

1. **Fundir só o IDÊNTICO não devolve tile nenhum.** As 78 fusões de erro zero
   (metatiles que a renumeração dos dois mapas criou em duplicata) tiram 78
   números de metatile e **zero** blocos de 8x8, porque o empacotador já
   deduplicava bloco repetido. Quem devolve tile é a fusão APROXIMADA.
2. **A fusão não piorou a nota; melhorou.** Sem fundir, 98,19%; com o limiar
   escolhido, 98,35%. O que se perde nas 36 fusões aproximadas volta em
   quantização evitada, porque sobra vaga de tile para a arte que ficava de fora.

O limiar escolhido é **60.000**, um passo acima do MENOR que faz caber (58.000,
medido). As 36 fusões aproximadas, todas elas, com o número do metatile no
vocabulário FUNDIDO da fonte (não no par novo):

| saiu | ficou | erro | células | | saiu | ficou | erro | células |
|---|---|---|---|---|---|---|---|---|
| 518 | 187 | 58.432 | 1 | | 21 | 20 | 34.560 | 3 |
| 163 | 164 | 57.856 | 1 | | 34 | 33 | 34.560 | 3 |
| 51 | 14 | 57.792 | 2 | | 367 | 365 | 33.792 | 1 |
| 340 | 14 | 57.792 | 1 | | 356 | 339 | 33.664 | 1 |
| 355 | 353 | 55.616 | 1 | | 279 | 179 | 29.120 | 1 |
| 482 | 481 | 55.296 | 2 | | 283 | 179 | 26.368 | 1 |
| 422 | 420 | 50.176 | 1 | | 284 | 179 | 26.368 | 1 |
| 436 | 310 | 48.704 | 1 | | 278 | 186 | 23.936 | 1 |
| 379 | 311 | 45.568 | 2 | | 184 | 179 | 21.504 | 3 |
| 395 | 394 | 45.504 | 1 | | 434 | 179 | 21.504 | 1 |
| 176 | 179 | 42.944 | 3 | | 354 | 353 | 20.928 | 1 |
| 183 | 179 | 42.944 | 2 | | 317 | 301 | 20.800 | 11 |
| 35 | 22 | 41.472 | 3 | | 319 | 301 | 20.800 | 7 |
| 173 | 179 | 40.256 | 3 | | 140 | 301 | 20.800 | 3 |
| 175 | 179 | 40.256 | 3 | | 198 | 301 | 20.800 | 1 |
| 225 | 179 | 40.256 | 2 | | 268 | 264 | 19.584 | 1 |
| 433 | 179 | 40.256 | 1 | | 376 | 375 | 38.272 | 1 |
| 280 | 179 | 35.136 | 1 | | 393 | 373 | 35.200 | 1 |

Mais 71 fusões de erro ZERO, que não estão listadas porque não há o que julgar
nelas: são metatiles byte a byte iguais. Ao todo **1.945 células** migraram de
número, e o vocabulário caiu de 519 para 412 metatiles.

**O que NÃO foi cortado, e o que o corte devolveria:** a pilha de carvão do pátio
(o retângulo (41..50, 36..43) do mapa fundido) continua na lista `apagar` da
receita, agora desligada por `--sem-cortes`, porque ela é a MEDIDA do que o corte
devolve: **122 tiles** (1.023 com a pilha, 901 sem ela). A fábrica branca, o
outro corte da opção 3, nunca chegou a ser considerada. A descida norte-sul está
intacta e provada (10.6).

### 10.3 A cópia, medida

| medida | valor |
|---|---|
| planta | dois mapas do hack (norte 72x32 em (0,0), sul 58x44 em (14,32)) fundidos em **72x76**, 520 metatiles renumerados |
| `mapLayoutId` | `LAYOUT_OREBURGH_CITY`, intacto (era 70x59) |
| fidelidade do mapa inteiro (sem conexão, tudo é interior) | **98,34%** (23.196 pixels de 1.400.832) |
| semente de paleta escolhida | `cor` (a `paleta` dava 97,15%) |
| tiles | 512 do primário + 511 do secundário = **1.023 de 1.024** |
| metatiles | **426** ocupados no primário, 1 no secundário, mais 14 gêmeos COVERED e 5 gêmeos de seta |
| paletas | **13 de 13**, 457 fusões exatas, 16 aproximadas, pior erro de fusão 6.464 |
| blocos quantizados | **314**, pior erro quadrático **6.464** |
| índices pinados | 0 (sem conexão, PROVA C sem objeto) |
| PROVA DO TILE 0 | ok, slot 0 do primário novo VAZIO |
| ROM | controle (HEAD `2b057a4368`) **31.589.124 B** -> **31.621.440 B**, ou seja **+32.316 B** |

**O remendo de dois buracos do autor:** as células (26,32) e (30,32) do mapa
fundido, que são o fim das duas rampas de carvão do armazém, têm metatile 100%
VAZIO na fonte. No render de referência do próprio hack elas saem em magenta
(248,0,248), a cor 0 da paleta 0: é buraco, não desenho. As duas receberam a
palavra da célula (22,32), o chão liso do mesmo pátio (`remendos`, na receita de
`FUSOES`). Copiar buraco não é fidelidade.

**--sem-animacao é legítimo, e o número é este:** a Oreburgh de HOJE tem **ZERO**
célula animada (nenhuma das 4.130 células usa a faixa 432-511 do
`gTileset_GeneralSinnoh`). O hack, esse sim, anima: `gTileset_OreburghSouth` tem
`.callback = InitTilesetAnim_Oreburgh`, que reescreve os slots 512 a 543 (carvão
em 8 quadros, período 16), e **82 células** do mapa sul apontam para lá, todas
FORA do retângulo da pilha de carvão: são as esteiras transportadoras do pátio.
Na cópia elas ficam PARADAS. Trazer a animação custaria os 80 slots da faixa
432-511 do primário novo (a ferramenta reserva a faixa inteira, não só o que o
callback escreve), e o orçamento não tem 80 slots: seria preciso cortar a pilha
de carvão ou subir o limiar de fusão para cerca de 200.000. Ou seja, **animar a
esteira custa desenho**, e a resposta 92 mandou preferir o desenho. Fica
registrado como perda medida, com o caminho do conserto.

### 10.4 O TELHADO SÓLIDO (resposta 98), célula a célula

Célula ANDÁVEL em que o jogador apareceria de pé EM CIMA de telhado virou
SÓLIDA. A lista é fechada e mora em `dev_scripts/telhado_solido_sinnoh.json`,
que a ferramenta lê em toda regeração (nunca uma edição à mão, PLANO 7.4).

Como as candidatas foram achadas, e por que a lista não é uma regra automática:
o conserto 94 marca COVERED todo metatile andável de topo opaco; cruzando essas
células com a busca em largura a partir de (54,24) saíram **119 candidatas, 77
alcançáveis a pé**. Cada uma foi olhada no render. Resultado:

| grupo | células | o que é |
|---|---|---|
| esteira de carvão elevada | 47 | os tubos azuis sobre pilares de tijolo do pátio da mina |
| telhado dos armazéns cinza | 5 | meio do telhado ondulado, sem escada |
| telhado do ginásio + batente da porta | 8 | a linha 20 e a célula (33,22), logo acima do warp 6 |
| telhado do Centro Pokémon + batente | 4 | idem, warp 8 |
| telhado do mercado | 2 | alto do prédio octogonal |
| telhado do Museu de Mineração | 8 | quina noroeste e a ala direita |
| parede lateral da Tower C | 2 | fachada, não passagem |
| **total** | **76** | |

**A 77ª ficou ABERTA, e é a única passagem de verdade:** (50,46), a travessia
leste-oeste do pátio POR BAIXO do tubo. Fechá-la deixa **121 células** do pátio
oeste inalcançáveis, medido por busca em largura, e ali estão quatro NPC. O
jogador atravessa ali visível em cima do tubo, que é o que a resposta 94 pediu.

Prova de que a planta andável muda SÓ ali: busca em largura antes e depois, com
o mesmo ponto de partida. **1.371 -> 1.272 células alcançadas**, e a diferença
são as 76 fechadas mais 23 bolsões que só se alcançava andando POR CIMA delas (a
varanda do ginásio e a do Centro, atrás da porta, e a faixa atrás dos armazéns do
norte). **Nenhum warp, NPC, placa, gatilho ou saída ficou inalcançável**: 22 de
22 warps, 23 de 23 objetos, 9 de 9 placas e 6 de 6 `coord_event` continuam
alcançáveis (a conta está em 10.6).

### 10.5 O JOGO: 16 warps, 23 objetos, 9 placas, 6 gatilhos

O dossiê `dev_scripts/dossies_sinnoh/OreburghCity.json` foi aplicado inteiro.
Os **16 warps mantêm os ids e a ordem** (só mudam de coordenada), os **23
`object_events` mantêm a ordem e os índices**, e os 9 `bg_events` e 6
`coord_events` idem. `mapLayoutId` intacto, nenhuma flag e nenhuma var nova,
`guarda_save.py` **SAVE COMPATIVEL**.

Seis warps NOVOS entraram no FIM da lista, que é o que a regra de save permite:

| id | onde | o que é |
|---|---|---|
| 16 | (51,64) | a QUINTA boca da mina. O hack desenhou cinco células de warp na boca e nós temos quatro warps de mina; o dossiê recomendava exatamente isto (opção b), para a boca ficar com a largura que o autor desenhou |
| 17 a 21 | (48,0), (49,0), (50,0), (52,0), (53,0) | a saída norte, convertida em par de warps de seta com a Route 207 |

Três ajustes do dossiê, todos medidos nesta rodada e escritos de volta no JSON:

- **objeto 15** (MACHOP, `Npc13`) saiu de (62,45) para (62,46): (62,45) é o topo
  da esteira, fechada pelo telhado sólido;
- **objeto 3** (HIKER, `Npc1`) saiu de (54,24) para (52,25): (54,24) é a ÚNICA
  célula andável em frente à porta do Centro Pokémon, e com
  `MOVEMENT_TYPE_WANDER_AROUND` o NPC podia ficar parado no caminho de quem sai
  (a regra B8 do `mapas_qa.py` já o acusava). De (52,25) o alcance dele não toca
  nem (54,23) nem (54,24);
- **objeto 2** (WOMAN_3, `BattleGirl`) saiu de (63,32) para (62,32), pelo mesmo
  motivo, na porta da Tower C (warp 9);
- **placa 8** saiu de (57,61) para (60,61): a primeira escolha do dossiê ficou
  sem uma só vizinha alcançável depois do telhado sólido, que é o mesmo defeito
  que ela tinha antes, em (0,58).

**Comportamentos** (`dev_scripts/comportamentos_sinnoh_retro.json`, chave
`OreburghCity`, acrescentada no fim sem tocar nas outras cidades):

| metatile | vira | por quê |
|---|---|---|
| 129 | `MB_ANIMATED_DOOR` | porta das três torres de apartamento (warps 1, 2, 9) |
| 133 | `MB_ANIMATED_DOOR` | porta de vidro da Loja e do Centro (warps 3, 8) |
| 181 | `MB_ANIMATED_DOOR` | porta das três casas (warps 5, 7, 10) |
| 231 | `MB_ANIMATED_DOOR` | porta do Ginásio (warp 6) |
| 144 | `MB_NON_ANIMATED_DOOR` | o vão escuro da rotativa do museu (warps 4 e 15). NÃO tem folha: prometer animação ali seria inventar arte. Continua sendo comportamento de warp, e as duas células têm colisão 0 |
| 146 | `MB_NORMAL` | o BATENTE do portão, (8,14), única célula deste metatile. O autor lhe deu porta, mas a porta de verdade é (9,14), que tem o warp 0. Sem rebaixar, a `lente_portas.py` acusava P1 trava |
| 3 | `MB_SIGNPOST` | a placa de poste do autor, nas duas células em que ela aparece: (51,4) e (11,12) |

**O ENCAIXE** (`dev_scripts/encaixes_sinnoh_retro.json`, arquivo novo): o hack
desenhou UMA entrada de museu e nós temos DOIS warps de museu (o 4, do
`LILYCOVE_MUSEUM`, e o 15, do `MINING_MUSEUM`). A célula (59,13), na ala direita
da mesma fachada, recebe a palavra inteira de (56,13). O encaixe roda DEPOIS de
o alvo de fidelidade ser tirado, de propósito: a nota conta a célula trocada
como diferença em vez de escondê-la.

### 10.6 As provas

| portão | resultado |
|---|---|
| `make -j8` | verde, md5 da ROM **`6f8df137efd26d3c29e693549e0f282f`** |
| `guarda_save.py` | **SAVE COMPATIVEL** |
| `valida_conectividade.py` | **warps quebrados: 0** |
| `valida_warp_tile.py --piso 60` | Sinnoh 98,3%, nenhuma região abaixo do piso |
| `valida_mapas_sinnoh.py` | **0 mapas com problema**, nenhuma linha de Oreburgh nem da Route 207 |
| `qa/lente_warps.py` | **NENHUM ACHADO** |
| `qa/lente_portas.py` | travas do cartucho 1 continuam **6**, as mesmas do controle |
| `qa/mapas_qa.py` | nenhum achado novo, e **sete a menos** em Sinnoh (provável 206 -> 201, cosmético 177 -> 174): B8 23 -> 22, C2 242 -> 239, C3 183 -> 180. **E3 = 859, igual ao controle, ou seja 0 em Oreburgh** |
| render da Route 207 | **0 pixel de diferença** contra o controle |
| alcance a pé | 1.272 células alcançadas de 4.144 andáveis; **22 de 22 warps, 23 de 23 objetos, 9 de 9 placas, 6 de 6 gatilhos** |
| blocos novos | **T267** 6/6, **T268** 3/3, **T269** 4/4 |
| casos antigos que passam por Oreburgh | T50, T55, T100, T101, T103, T112, T115, T116, T121, T122, T124, T140, T148, T155, T157, T158, T166, T260 a T263 verdes; **T171.11 e T175.4 refeitos** (ver abaixo); T187.11 continua vermelho e não é desta frente (PLANO 8.7) |

**O `antes_de_empurrar.sh` NÃO pôde rodar como ele se propõe, e o motivo não é o
commit:** o disco da máquina está cheio (926 GiB de capacidade, **2,0 GiB
livres**), e o script cria uma worktree descartável e builda o HEAD dentro dela,
o que pede cerca de 2,5 GiB. Ele falhou em dez passos com
`No space left on device` antes de rodar qualquer verificação. No lugar, os DEZ
passos dele foram rodados um a um na árvore de trabalho, **depois de provar que
ela é idêntica ao commit** (`git diff HEAD` vazio, `git status` limpo): build,
guarda de save, música, `valida_rom.py`, teto de grupo, conectividade, sprites e
objetos, warp em tile que dispara, treinador sem time e `testa_percurso.py`
(6 percursos). **Os dez deram ok.**

**O md5 da ROM mudou depois do commit da arte, e isso é o esperado:** dois
atributos de metatile (o 146 e o 144) foram gravados direto no
`metatile_attributes.bin` depois do primeiro build, para não regerar o par e
perder os gêmeos de seta (10.7, item 3). A ROM que vale é a do build final,
`6f8df137efd26d3c29e693549e0f282f`, e os blocos T267, T268 e T269 foram rodados
de novo contra ela. O T267.1 reprovava de forma intermitente nessa rodada (passava
sozinho e caía com o bloco inteiro) porque o caminho pela linha 24 raspava na
faixa dos NPC de `MOVEMENT_TYPE_WANDER_AROUND`; o roteiro desce três células antes
de atravessar e o bloco fecha 6/6 em três rodadas seguidas.

**Os dois casos antigos refeitos, e o motivo de cada um:**

- **T171.11** (o museu de Lilycove pela porta de Sinnoh) media a saída em
  (54,15). O warp 4 mudou de lugar com a planta: agora é (56,13) e larga o
  jogador em (56,14). Só a coordenada da prova mudou.
- **T175.4** media que um arbusto do `enfeita_cidades.py`, em (48,23) da planta
  VELHA, era sólido. Esse arbusto não existe mais: a cidade inteira virou arte do
  hack. O caso foi refeito na mesma família de prova (descer do warp 7 e parar na
  parede, em (44,29)), e a prova do carimbo continua viva em Eterna, no T175.5.

**A saída norte, medida célula a célula:** offset novo **39** (o de hoje é 35, e
o próprio hack usa 39 na Oreburgh dele). Com ele, 6 colunas da cidade casam com
6 da rota; **5 viraram warp** e uma ficou de fora:

| cidade | rota | virou saída? |
|---|---|---|
| (48,0) | (9,31) | sim, warp 17 |
| (49,0) | (10,31) | sim, warp 18 |
| (50,0) | (11,31) | sim, warp 19 |
| (51,0) | (12,31) | **não**: a placa `Sinnoh_EventScript_PlacaImportada` está em cima de (12,31) da rota |
| (52,0) | (13,31) | sim, warp 20 |
| (53,0) | (14,31) | sim, warp 21 |

Duas mudanças de regra que isso exigiu no `saidas_por_warp.py`, as duas medidas:

1. `ocupadas()` passou a contar **`bg_event`** além de `object_event`. Seta de
   warp e placa na mesma célula brigam: quem anda para a placa é teleportado
   antes de poder ler. É o caso de (12,31) acima.
2. `--apesar-de MB_BERRY_TREE_SOIL`: o metatile 268 do `general_sinnoh`, que é o
   chão da entrada da cidade na Route 207, carrega `MB_BERRY_TREE_SOIL`, e a
   ferramenta bloqueava a saída inteira por causa disso. Medido: **nenhuma** das
   6 células tem árvore de berry em cima; as 4 da Route 207 estão em (2..5, 2).
   Bloquear ali era proteger uma cova que não existe.

Os 5 gêmeos de seta foram escritos em vagas mortas: **5 no primário novo de
Oreburgh e 5 no `gTileset_Jubilife`** (o secundário da rota), e é por isso que o
render da rota dá 0 pixel de diferença.

### 10.7 O que ficou aberto

1. **As 4 portas de Oreburgh não ANIMAM ainda.** `porta_anima_copiada.py --prova`
   já gerou a arte dos quatro quadros (`graphics/door_anims/oreburgh_retro_*.png`,
   três com erro de quantização ZERO e a do ginásio com 71.232 em dois
   quadrantes, o arco branco e marrom que não cabe numa paleta só) e imprimiu as
   12 linhas para `sDoorAnimGraphicsTable`, mas **este executor não tocou em
   `src/field_door.c`**, porque o briefing proibiu. O warp funciona sem elas
   (`StartDoorOpenAnimation` devolve -1 e `Task_DoDoorWarp` trata `tDoorTask < 0`,
   medido em Floaroma e provado aqui pelo T267 6/6). As linhas estão no relatório
   do executor, prontas para colar no FIM DO PRIMEIRO RAMO do `#if !IS_FRLG`.
2. **A esteira de carvão não anima** (10.3): 82 células do hack, e trazer a
   animação custa a pilha de carvão ou fusões grosseiras.
3. **Regerar o par de Oreburgh apaga os 5 gêmeos de seta do primário.** Depois de
   qualquer `--aplicar` novo, rodar `saidas_por_warp.py` de novo. O mesmo vale
   para os dois atributos que foram gravados direto no
   `metatile_attributes.bin` (146 e 144): a tabela de comportamentos os repõe na
   regeração, mas a ordem certa é regerar e só então rodar as saídas.
4. **O jogador atravessa (50,46) por cima do tubo da esteira**, e não por baixo
   como o autor desenhou. É a única célula da esteira que ficou andável, e a
   alternativa (deixá-la NORMAL, com o tubo por cima do sprite) é o sumiço que a
   resposta 94 proibiu.
