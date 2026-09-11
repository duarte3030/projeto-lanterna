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

## 9. Onda 4 (11/09/2026): o anel de Twinleaf vira arte do autor, e o telhado fecha

Vieram das respostas 97 a 100 do Fable. Esta seção é do CONDUTOR; Sandgem,
Oreburgh e Jubilife têm seções próprias.

### 9.1 Resposta 99: a Route 201 recebe o PAR de Twinleaf

A pergunta era se valia devolver o desenho do autor ao anel de Twinleaf (o
canteiro de flor branca cercado e a cerca, que a regra 3.2 tinha trocado pela
nossa grama nas 8 primeiras linhas, 23% da altura da cidade). A resposta mandou
MEDIR primeiro, e a medida fechou o caso:

| medida | valor |
|---|---|
| metatiles >= 512 no `map.bin` da Route 201 | **0** |
| metatiles >= 512 no `border.bin` dela | **0** |

Ou seja a Route 201 não usa **um único** metatile do secundário dela
(`gTileset_PetalburgSinnoh`). Trocar o secundário dela não apaga desenho nenhum,
e é o caso que a resposta 99 descreve. A `Route201_Layout` passou a apontar para
o MESMO par de Twinleaf (`gTileset_GeneralSinnoh` + `gTileset_TwinleafRetroSec`),
o lado norte deixou de ser anel e **a arte da borda voltou a ser a do autor, com
a conexão de mapa aberta**. Os dois ganhos juntos, que era o que a resposta
pedia.

Modo novo da ferramenta: `--vizinho-compartilha-par Route201`. Ele tira o lado do
conjunto de anel e, com `--aplicar`, troca o `secondary_tileset` da rota no
`layouts.json` (não à mão: conserto fora da ferramenta morre na primeira
regeração, seção 7.4).

**PROVA P**, nova, mede TRÊS coisas, e a terceira é a que ninguém lembra:

1. a rota não usa o secundário dela (senão a troca apaga desenho);
2. o layout dela aponta para o secundário da cidade (quem faz é o `--aplicar`);
3. **os OUTROS vizinhos da rota continuam legíveis**: parado na Route 201, o
   jogador também vê a faixa de quem mais está conectado a ela, agora desenhada
   com o secundário da CIDADE. Cada um desses mapas tem de ter 0 índice >= 512 na
   faixa que encosta na rota.

Resultado medido:

| afirmação | resultado |
|---|---|
| 1. Route 201 usa 0 metatile do `petalburg_sinnoh` | ok |
| 2. `Route201_Layout` -> `gTileset_TwinleafRetroSec` | ok, aplicado |
| 3. parado na Route 201, anel leste da **VerityLakefront** | ok, 0 índices >= 512 |
| 3. parado na Route 201, anel oeste da **SandgemTown** | **10 índices >= 512** (552, 560, 568, 576, 584, 592, 600, 601, 608, 616) |

**O furo da Sandgem é conhecido, é desta onda e fecha sozinho.** A Sandgem está
sendo copiada em paralelo: ou ela vai de regra 3.2, e aí o de-para do anel zera a
faixa oeste, ou ela vai de par próprio e a conexão com a Route 201 deixa de
existir. Nos dois casos o furo some. Enquanto ele existir, quem estiver parado na
Route 201 olhando para o leste vê lixo em 10 metatiles da beirada de Sandgem.
A ferramenta RECUSA aplicar com esse furo; para seguir foi preciso nomear o mapa
devedor em `--vizinho-furo-conhecido SandgemTown`, que é de propósito: furo
adiável tem de ter dono e nome. **Na consolidação, rodar a PROVA P de novo e
exigir as três afirmações verdes antes de qualquer merge.**

#### O que a arte ganhou e o que ela custou

| medida | onda 3 (anel de-para) | onda 4 (anel do autor) |
|---|---|---|
| fidelidade do INTERIOR | 98,97% (só o miolo; o anel era 100% nosso) | **97,78% do MAPA INTEIRO** (4.249 pixels de 191.488) |
| tiles do secundário | 273 / 512 | **305 / 512** |
| metatiles | 122 / 512 | **140 / 512** |
| paletas próprias | 7 / 7 | 7 / 7 |
| semente de paleta | `cor` | `cor` (a `paleta` dava 95,99%) |
| blocos quantizados | 28 | **41**, pior erro quadrático 4.416 |
| índices pinados | 0 | 0 |
| PROVA S | 0 furos | 0 furos |
| travessia norte | 4 colunas (x 10..13 da cidade, 14..17 da rota) | as MESMAS 4 |

A nota de 97,78% NÃO é pior que a de 98,97%: ela cobre o mapa inteiro, anel
incluído, e antes o anel ficava fora da conta justamente por ser arte nossa. O
que a tabela mostra é o preço em orçamento (32 tiles e 18 metatiles a mais) de
copiar mais 8 linhas de desenho do autor.

### 9.2 Resposta 98: o telhado fecha

Regra do motor, lida em `DrawMetatile` (`src/field_camera.c`): NORMAL e SPLIT
mandam a camada de cima para o **BG1**, que fica ACIMA de todo sprite (o jogador
SOME); COVERED manda para o **BG2**, abaixo dos sprites (o jogador aparece EM
CIMA). O autor do Retro Platinum deixa colisão 0 no corpo dos prédios, então no
jogo DELE o jogador sobe no telhado e some; depois do conserto 94 ele deixaria de
sumir e passaria a aparecer de pé sobre o telhado. As duas são erradas, e a causa
é a mesma: a célula não devia ser andável.

Ferramenta nova, `dev_scripts/telhado_andavel.py --lente`, que lista toda célula
ANDÁVEL com a camada de cima desenhando e grava o render com elas marcadas em
vermelho. **Não existe regra de pixel que separe telhado de passadiço**, então
quem separa é olho humano olhando a marca, e a lista JULGADA mora em
`dev_scripts/telhados_sinnoh_retro.json`, aplicada pela própria ferramenta de
cópia (`fecha_telhado_andavel`, antes do conserto de camada, para a célula
fechada nem entrar na régua de "andável").

| cidade | candidatas da lente | fechadas | o que ficou de fora, e por quê |
|---|---|---|---|
| Twinleaf | 80 | **26** | a porta (warp), o degrau de grama embaixo dela, 12 células de flor do anel norte e 24 de mata da borda (todas inalcançáveis), e o passadiço de tábua sobre a água na linha 29, onde o jogador TEM de aparecer |
| Floaroma | 556 | **16** | 512 células de CAMPO DE FLOR, onde o jogador anda por cima e tem de aparecer; as duas portas e o poste da saída leste (warps); a grama da frente do Centro Pokémon (linha 24, com o capacho); os cantos da Loja na linha 33; as 5 células da borda leste, que são o corredor de saída |

As 26 de Twinleaf são EXATAMENTE as 26 que o conserto 94 convertia para COVERED
(13 metatiles, 2 células cada): fechada a colisão, a conversão deixa de ter
objeto e o relatório passa a dizer "0 metatiles andáveis passaram para COVERED".
Em Floaroma a conversão cai de 17 metatiles para 3 (42, 49 e 63, que são flor e
poste).

**Duas células que a lente NÃO achou e a guarda de conectividade achou.** Fechar
só a parede (18,31) do Centro de Floaroma ilhava (17,31) e (19,31), que são
andáveis, têm o topo sem desenho (por isso ficaram fora da lente) e tinham a
parede como única vizinha. A ferramenta RECUSOU a tabela inteira ("a planta
andável partiria de 3 para 5 componentes") e a resposta certa era fechar as três:
as três são corpo de prédio. **A guarda é o que impede "a planta andável muda só
ali" de virar promessa.**

Diferença medida no `map.bin` de Floaroma depois da regeração: **16 células, só o
bit de colisão**; `metatiles.bin` byte a byte igual, e o `metatile_attributes.bin`
muda só nos 14 metatiles que deixaram de precisar de COVERED.

### 9.3 O número cravado que mentiu calado, e o conserto

`--aplicar` renumera o par. Com o anel livre, a numeração de Twinleaf andou 13
casas e **a porta saiu do metatile 576 para o 589**. Três coisas que apontavam
para o 576 seguiram apontando:

1. `comportamentos_sinnoh_retro.json` promoveu a `MB_ANIMATED_DOOR` o 576, que
   agora é PAREDE de casa, e a porta de verdade ficou com o
   `MB_NON_ANIMATED_DOOR` que veio da arte. **Nada acusou**, porque
   `MB_NON_ANIMATED_DOOR` também warpa (`IsWarpMetatileBehavior`): o warp
   continuava funcionando e só a ANIMAÇÃO se perdia, e animação não tinha portão;
2. a receita do `porta_anima_copiada.py` compôs a arte da porta a partir do 576,
   ou seja gerou a animação de uma parede;
3. a entrada do `sDoorAnimGraphicsTable` em `src/field_door.c` casava o 576.

Os três passaram a ser resolvidos pela **CÉLULA**, que é estável porque a planta
do autor não anda: a tabela de comportamento ganhou o bloco `"celulas"`
(`"5,13": {"mb": "MB_ANIMATED_DOOR", ...}`), a receita da porta ganhou o campo
`celula=(5, 13)` e passou a ler o número do `map.bin` (avisando em voz alta
quando ele andou), e nasceu a **PROVA W**: todo `warp_event` do mapa tem de cair
em metatile que dispara warp, com o MB dito por nome. Ela é portão de
`--aplicar`.

| cidade | PROVA W |
|---|---|
| Twinleaf | 4 de 4 warps em `MB_ANIMATED_DOOR`, metatile 589, colisão 0 |
| Floaroma | 14 de 14 warps, metatiles 143, 196, 52, 123, 124 e as setas |

**Custo medido, e é o risco aberto desta seção:** com o anel livre, o
empacotamento de paleta mudou e os quadrantes da porta de Twinleaf saíram de
`{2, 7, 9, 9}` para `{2, 7, 3, 8}`. Os dois de baixo passaram a QUANTIZAR, com
pior erro de quadrante **45.568** (era 0 na onda 3). A causa é a da seção 8.2: o
quadrante junta a cor do CHÃO (camada de baixo) com a da FOLHA (camada de cima),
e o hardware dá uma paleta por tile de 8x8; na onda 3 a paleta 9 continha as duas
famílias e agora nenhuma contém. **Correção de registro: o "caiu de 20.992 para
ZERO" da seção 8.6 estava medido no metatile ERRADO** (o 576, que já era parede
naquela leitura); o número da porta de verdade nunca foi 0.

### 9.4 Resposta 97 e resposta 100

- **97**: a conexão SUL de Twinleaf com a Route 220 fica FECHADA. Nada a fazer, e
  o registro da medida está na seção 7.3.
- **100**: `DOOR_SIZE_ONE_CELL` autorizado. O `src/field_door.c` recebeu o
  parágrafo de AUTORIZAÇÃO ao lado da medida que já estava lá: o valor 0 não
  existia na tabela de fábrica (os tamanhos do Emerald são 1 e 2), nenhum `size`
  antigo muda de comportamento e o ramo novo só roda para as três portas
  copiadas.

### 9.5 As provas da onda

| portão | resultado |
|---|---|
| `make -j8` | verde, md5 `c190503f70735f0fcbdd8ffa90cd2ff7` |
| ROM | controle (HEAD `2b057a4368`) 31.589.124 B -> **31.590.116 B**, ou seja **+992 B** |
| `guarda_save.py` | **SAVE COMPATIVEL**, 1594 mapas, 0 novos |
| `valida_conectividade.py` | warps quebrados: **0** |
| `valida_warp_tile.py --piso 60` | Sinnoh 98,3%, nenhuma região abaixo do piso |
| `valida_mapas_sinnoh.py` | `'sprite': 0`, 0 mapas com problema |
| `qa/mapas_qa.py` | E3 **859**, o mesmo da onda 3; nenhuma regra muda um achado |
| `qa/lente_portas.py` | 6 travas em Sinnoh, as mesmas da onda 3 |
| bloco novo **T260.5 a T260.9** | 5 de 5, rodado duas vezes |
| T260.1 a T260.4, T261, T262, T263 | 4+4+6+5 de 4+4+6+5, todos verdes |

**Uma armadilha de suíte que custou duas rodadas vermelhas**: a primeira versão
dos casos de telhado passava por células que um NPC de
`MOVEMENT_TYPE_WANDER_AROUND` pode ocupar (o object_event 3 de Floaroma anda num
quadrado de 1x1 em volta de (15,28)). O caso ficava vermelho conforme o boneco
tivesse andado ou não, que é o pior tipo de teste. As rotas passaram a ser
buscadas com TODA célula alcançável por NPC que anda tratada como bloqueio, e aí
ficaram estáveis. Vale para quem escrever bloco novo nas outras três cidades.

### 9.6 Aberto

1. **A quantização da porta de Twinleaf (45.568)**, seção 9.3. É decisão de
   gosto: ou se aceita o desvio de cor nos quadros de abertura, ou se tira a
   entrada da porta do `sDoorAnimGraphicsTable` (o warp continua funcionando sem
   ela, `StartDoorOpenAnimation` devolve -1 e `Task_DoDoorWarp` trata).
2. **O furo da afirmação 3 da PROVA P** enquanto a Sandgem não entrar, seção 9.1.
3. Fila de bugs herdada e NÃO tocada nesta onda: metatile 268
   `MB_BERRY_TREE_SOIL`, a borda magenta do Mart e da House2 de Floaroma (visível
   na foto do emulador, preexistente, a regra E1 do `mapas_qa.py` não pega porque
   ela lê só o `map.bin` e nunca o `border.bin`), e o T187.11.

## 10. Sandgem aplicada (11/09/2026, executor SANDGEM da onda 4)

A ordem de tentativa da seção 3.2 foi cumprida na ordem, e a regra 3.2 **não
coube**. O número que decidiu está abaixo, e não é estimativa: é a saída da
ferramenta.

### 10.1 Por que a regra 3.2 não serve para Sandgem

    python3 dev_scripts/copia_cidade_fonte.py --cidade SandgemTown \
        --par-proprio --so-secundario \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json

| medida | Sandgem em 3.2 | teto |
|---|---|---|
| tiles do secundário | **512, CHEIO, e 23 blocos de 8x8 ficaram SEM SLOT** | 512 |
| metatiles | 209 | 512 |
| paletas próprias | 7 | 7 |
| fidelidade do INTERIOR | **92,73%** (semente `paleta`) | |
| blocos quantizados | **138**, pior erro quadrático 6.464 | |
| PROVA S (costura) | **RUIM**: 2 índices >= 512 na faixa que a Route 219 desenha (541 e 542, do `petalburg_sinnoh`) | 0 |

Três coisas, e cada uma sozinha já fecharia a questão:

1. **O tile não cabe.** Os 512 slots enchem e sobram 23 blocos de fora. Não é o
   caso de Twinleaf (273 de 512, com folga de 239).
2. **O anel come a cidade.** Sandgem tem conexão em TRÊS lados (oeste, norte e
   sul), e a faixa de `ANEL_COSTURA` = 8 dá 272 + 272 + 144 = **688 células das
   1.156**, ou seja **59,5% do mapa** seria arte NOSSA e não do autor. Em
   Twinleaf, que tem um lado só, o anel é 23% da cidade e a seção 7.3 já
   registrou isso como "o preço da regra 3.2, e ele é visível". A 60% não é mais
   uma cópia com moldura: é uma moldura com um miolo copiado dentro.
3. **A costura tem furo real pelo sul.** A Route 219 usa dois metatiles do
   `petalburg_sinnoh` (541 e 542, em 4 células da faixa que Sandgem desenharia:
   (24,5), (25,5), (26,3) e (27,3)). Com secundário próprio, essas quatro
   células viram lixo na tela de quem está parado em Sandgem.

O recorte foi medido também, e não salva: `--recorte 0,0,34,32` dá 499 tiles e
93,58%, `--recorte 0,2,34,32` dá 473 tiles e 96,80%, mas os dois CORTAM duas
linhas da planta do autor e a PROVA S continua RUIM pelo mesmo furo do sul.
Recorte é a exceção da resposta 91, e ela existe para planta que se estende ALÉM
da saída que o próprio autor desenhou; não é o caso aqui.

**O que aconteceu com as três vizinhas, para o condutor:**

- **Route 201, o que o briefing pediu para não encostar.** Ela continua com
  **ZERO metatile >= 512** no `map.bin` e no `border.bin` depois desta onda, que
  é a invariante que deixa o condutor apontar o `Route201_Layout` para o
  `gTileset_TwinleafRetroSec` de graça. Para isso a ferramenta ganhou
  `--rota-no-primario` (ver 9.5): o gêmeo de seta do lado dela foi mintado no
  `gTileset_GeneralSinnoh`, e não no secundário.
- **Route 202 NÃO foi reivindicada.** As três provas que o briefing pedia dão
  certo (Route 202 usa 0 índice >= 512; o anel SUL da Jubilife tem 0; a faixa da
  Route 202 que Sandgem desenharia tem 0), mas a reivindicação só faria sentido
  no desenho de 3.2, que caiu. Com par próprio não existe conexão nenhuma, e a
  Route 202 fica como está.
- **Route 219**: o furo dos metatiles 541 e 542 deixou de existir pelo mesmo
  motivo. A conexão sul virou warp.

### 10.2 O par próprio, medido

    python3 dev_scripts/copia_cidade_fonte.py --cidade SandgemTown \
        --par-proprio --sem-conexao \
        --depara dev_scripts/depara_sinnoh_retro_platinum.json \
        --aplicar --simbolo SandgemRetro

| medida | valor |
|---|---|
| planta | 34x34 na fonte, layout 34x32 -> **34x34**, sem recorte, `mapLayoutId` intacto |
| fidelidade do MAPA INTEIRO (sem conexão, tudo é interior) | **100,00%** (0 pixels de 295.936) |
| semente de paleta escolhida | `cor` (a `paleta` dava 99,79%, com 26 blocos quantizados) |
| tiles | 432 do primário + 152 do secundário + 80 reservados de animação = **584 de 944** |
| metatiles | **235** no primário, 1 no secundário |
| paletas | 13 de 13; 281 conjuntos de cor distintos, 117 cores no total, 265 fusões EXATAS, 3 aproximadas, pior erro de fusão 5.504 |
| blocos de 8x8 distintos | 599 |
| blocos quantizados | **0**: toda cor achou paleta exata |
| índices pinados | 0 (PROVA C sem objeto: a cidade não tem conexão) |
| PROVA DO TILE 0 | ok, slot 0 do primário novo vazio |
| PROVA DA ANIMAÇÃO | ok, faixa 432-511 byte a byte igual à do `general_sinnoh`, 0 referências novas |
| ROM | 31.589.124 B no controle (HEAD 2b057a4368) -> **31.614.212 B**, ou seja **+25.088 B** |
| md5 da ROM | `90321baeda6781367e8de48276285c7f` |

Os renders do HACK e da CÓPIA saem **byte a byte iguais** (md5
`10a1e544a01e3de1bff4b1a017d81934` nos dois), que é o que 100,00% quer dizer.

### 10.3 A ANIMAÇÃO: 4 antes, 0 no hack, 0 depois

Medido nos dois lados, não presumido:

- Sandgem de HOJE: **4 células animadas**, todas de flor (metatile 4 do
  `general_sinnoh`, faixa de VRAM 508-511), em (20,0), (20,1), (29,1) e (29,2).
  Água: 0.
- Sandgem do HACK: **0**. O `.callback` de `gTileset_OutdoorJubilife` E o de
  `gTileset_Sandgem` são `NULL` no `src/data/tilesets/headers.h` da fonte, ou
  seja o autor não anima nada nesta cidade.
- Depois da cópia: **0**.

Como o hack não anima, `--anim-fonte` não tem receita a escrever e não foi usado.
O primário novo mantém `.callback = InitTilesetAnim_General` com os 80 slots
reservados byte a byte, que é o arranjo de Jubilife e de Twinleaf-par-próprio.

### 10.4 TELHADO SÓLIDO (resposta 98): 46 células, e a régua mecânica não bastava

`--telhado` é novo, lê `dev_scripts/telhado_solido_sinnoh.json` e roda DEPOIS do
`map.bin` e ANTES do conserto de `layerType`. **46 células andáveis em cima de
prédio passaram para colisão 1**, julgadas UMA A UMA no render, com a planta de
cada prédio recortada e cada célula andável rotulada:

| prédio | células | o que são |
|---|---|---|
| Laboratório do Rowan e o galpão de madeira ao lado | 18 | (9,11) (10,11) (11,11) a viga da fachada; (9,9) a (14,9) e (9,10) a (14,10) o TELHADO; (12,11) (13,11) (14,11) a fachada do galpão |
| Centro Pokémon | 8 | (17,9) a (21,9) o telhado laranja; (18,11) (19,11) (20,11) o beiral |
| Loja | 2 | (29,11) (30,11), o beiral |
| Casa 1 | 6 | (8,21) a (11,21) o telhado; (9,23) (10,23) a empena |
| casa do rival | 12 | (19,19) a cumeeira, (17,20) a (21,20) o telhado, (18,22) a (20,22) a empena, (18,23) (19,23) (20,23) as JANELAS |

**A lição que custou uma rodada:** a primeira versão do `--telhado` conferia a
linha da tabela contra a ASSINATURA mecânica de telhado (camada de cima cheia e a
de baixo vazia), que é a mesma régua do conserto de `layerType` e da regra E3 do
`mapas_qa.py`. Com ela, Sandgem dava **13** células, e só. As outras 33 passavam
batidas porque **o autor desenha o telhado na camada de BAIXO**, com a de cima
vazia: as 15 células andáveis em cima do telhado do laboratório não têm
assinatura nenhuma, e o jogador fica de pé em cima delas do mesmo jeito. A
conferência passou a ser a COLISÃO (a célula da tabela tem de ser ANDÁVEL no
mapa novo, senão a ferramenta PARA), e a assinatura virou o que sempre foi: um
aviso, impresso à parte, de que existe arte por cima de célula andável.

O que fica ANDÁVEL de propósito, e está escrito na tabela: a moldura decorativa
de mata das bordas (177 células, que o jogador nem alcança), as linhas de mata
andáveis de (22..25,1), (28..31,7) e (0..7,17), onde a copa do autor passa por
cima do jogador (é copa de árvore, não telhado), e a escadaria de areia da praia
a leste.

**Prova de que a planta andável muda SÓ ali:** busca em largura no `map.bin`
novo, a partir da pousada do warp 0. Antes das 46, **583** células alcançadas;
depois, **537**. A diferença é 46, exatamente as células fechadas, e **5 de 5
warps, 10 de 10 objetos, 8 de 8 placas e 6 de 6 gatilhos continuam alcançáveis**.
As cinco células de porta continuam andáveis.

Com o telhado fechado antes, o conserto de `layerType` não teve mais nada para
trocar: **0 metatiles passaram para COVERED** (eram 13), e ficaram só os 3 gêmeos
COVERED da moldura de mata (8 -> 233 em 85 células, 9 -> 234 em 90, 14 -> 235 em
2). **E3 em Sandgem = 0**, antes e depois.

### 10.5 As saídas por warp, e a flag que a Route 201 exigiu

    python3 dev_scripts/saidas_por_warp.py --cidade SandgemTown \
        --offsets <json> --rota-no-primario MAP_ROUTE201 --aplicar

O autor NÃO resolve a saída de Sandgem por seta (medido: o `map.bin` dele só tem
dois comportamentos, `MB_NORMAL` em 1.151 células e `MB_NON_ANIMATED_DOOR` em 5;
**zero** `MB_*_ARROW_WARP`). Ou seja `--so-seta-do-autor`, que o briefing pedia,
daria ZERO saída e trancaria a cidade. As travessias saíram da interseção da
colisão dos dois `map.bin`, que é o modo normal da ferramenta, e a conta bate com
os corredores de hoje.

| saída | offset hoje | offset novo | conta | travessias |
|---|---|---|---|---|
| oeste, MAP_ROUTE201 | 6 | **10** | `y_rota = y_cidade - 10`; o corredor da cidade desceu de y 9..13 para y 12..17 e o da Route 201 continua em y 2..7 | **6** (warps 5 a 10, (0,12) a (0,17)) |
| sul, MAP_ROUTE219 | -2 | **2** | `x_rota = x_cidade - 2`; o corredor do hack tem 10 tiles (x 22..31) e o da rota tem 6 (x 22..27) | **6** (warps 11 a 16, (24,33) a (29,33)) |
| norte, MAP_ROUTE202 | 2 | **4** | `x_rota = x_cidade - 4`; o corredor do hack anda 2 tiles para a direita | **6** (warps 17 a 22, (26,0) a (31,0)) |

As quatro células que sobram em cada corredor de 10 batem em terreno bloqueado do
outro lado e não viraram saída: a ferramenta as lista como "rota bloqueada em".

**`--rota-no-primario` é nova, e nasceu de uma medida.** Do lado da rota o gêmeo
de seta ia sempre para o SECUNDÁRIO dela. Na Route 201 isso quebraria duas coisas
ao mesmo tempo: o gêmeo sumiria quando o condutor trocasse o secundário dela pelo
`gTileset_TwinleafRetroSec` (índice >= 512 passaria a desenhar o metatile de
OUTRO tileset), e a própria troca deixaria de ser livre, porque a Route 201 passaria
a usar índice alto. Com a flag, os 6 gêmeos dela vão para o `gTileset_GeneralSinnoh`,
que tem **111 vagas livres na árvore inteira** (medido; o comentário antigo do
script dizia "1 vaga livre só" e estava velho). Route 202 e Route 219 continuam no
`petalburg_sinnoh`, que tem 450.

**Mudança nas rotas irmãs, declarada:** 6 células em cada uma (Route 201 (63,2) a
(63,7), Route 219 (22,0) a (27,0), Route 202 (22,33) a (27,33)) trocam de índice
de metatile para o gêmeo de seta, que copia as 8 palavras do chão original. O
render das três dá **0 pixel de diferença** contra o controle.

### 10.6 O jogo

Dossiê `dev_scripts/dossies_sinnoh/SandgemTown.json` aplicado inteiro: **5 warps
nos MESMOS ids** (só a coordenada muda, delta +2/+4 nas âncoras), **10
`object_events` na MESMA ordem e nos mesmos índices**, **8 `bg_events`** e **6
`coord_events`** idem, `mapLayoutId` intacto, **nenhuma flag e nenhuma var nova**.
`guarda_save.py` diz **SAVE COMPATIVEL**. Os 18 warps de seta entraram no FIM da
lista, ids 5 a 22.

Comportamentos, em `dev_scripts/comportamentos_sinnoh_retro.json`, chave
`SandgemTown`, acrescentada no fim sem tocar nas outras cidades:

- **94, 172 e 131 viram `MB_ANIMATED_DOOR`** (o autor deixou
  `MB_NON_ANIMATED_DOOR`). O 94 é a porta do laboratório, o 172 serve ao Centro
  (19,12) E à Loja (29,12), o 131 à Casa 1 (9,24) E à casa do rival (18,24).
  Conferido antes de mexer: nenhum deles aparece em outra célula do mapa nem no
  `border.bin`.
- **33, 205, 213, 222 e 226 viram `MB_SIGNPOST`**: são os SEIS postes de placa
  que o autor desenhou, e as seis placas que casam por função foram para eles.
- **Os bg 6 (21,33) e 7 (25,3) ficam em `MB_NORMAL` bloqueante**, porque caem em
  parede de mata e não em poste, como as três de Floaroma. Medida que sustenta a
  decisão: **HOJE as OITO placas de Sandgem estão em célula ANDÁVEL de chão liso**
  (metatiles 297, 289, 281, 288 e 1 do `general_sinnoh`, colisão 0, `MB_NORMAL`),
  ou seja o jogador pisa em cima delas e nenhuma tem poste desenhado. Depois da
  cópia as oito passam a ser bloqueantes e seis ganham o poste do autor: não há
  regressão em nenhuma.

### 10.7 As portas ABREM

`dev_scripts/porta_anima_copiada.py` ganhou três receitas
(`sandgem_retro_vidro`, `sandgem_retro_madeira`, `sandgem_retro_lab`) e
`src/field_door.c` ganhou as três entradas no fim do PRIMEIRO ramo do
`#if !IS_FRLG`, todas com `DOOR_SIZE_ONE_CELL`.

| porta | metatile | células | metatile ACIMA | estilo | pior erro de quadrante |
|---|---|---|---|---|---|
| vidro (Centro e Loja) | 172 | (19,12) e (29,12) | **165 e 136, diferem** | `lados`, `DOOR_SOUND_SLIDING` | **0** |
| cortina verde (Casa 1 e casa do rival) | 131 | (9,24) e (18,24) | **124 e 216, diferem** | `cortina`, `DOOR_SOUND_NORMAL` | 21.504 |
| laboratório | 94 | (10,12) | 86 | `cortina`, `DOOR_SOUND_NORMAL` | **0** |

Os dois casos de metatile ACIMA diferente são a razão de `DOOR_SIZE_ONE_CELL`
existir (seção 8.1): com `size` 1 o Centro piscaria a parede da Loja e a Casa 1 a
da casa do rival. A quantização de 21.504 da porta de cortina é a linha de GRAMA
de baixo (a cor (56,184,80) cai em (96,152,88), 8 pixels em dois quadrantes),
mesma família do 20.992 que Twinleaf tinha antes de voltar para o secundário: o
quadrante junta a paleta da folha com a do chão e o hardware dá uma paleta por
tile.

### 10.8 Os portões técnicos

| portão | resultado |
|---|---|
| `make -j8` | VERDE, md5 `90321baeda6781367e8de48276285c7f`, ROM 31.614.212 B |
| `guarda_save.py` | **SAVE COMPATIVEL** |
| `valida_conectividade.py` | **warps quebrados: 0** |
| `valida_warp_tile.py --piso 60` | Sinnoh 98,4%, nenhuma região abaixo do piso |
| `valida_mapas_sinnoh.py` | **0 mapas com problema**, 0 linhas de Sandgem, Route 201, 202 ou 219 |
| `qa/lente_warps.py` | NENHUM ACHADO |
| `qa/lente_portas.py` | 6 travas em Sinnoh, **as mesmas 6 do controle**, diff vazio |
| `qa/mapas_qa.py` | 1.960 itens antes e 1.960 depois; **1 novo e 1 sumido, e são o MESMO achado A3 pré-existente** ("warp 4 larga o jogador em cima de OBJ_EVENT_GFX_RICH_BOY") andando de (16,21) para (18,25) junto com o mapa. E3 em Sandgem: 0 antes, 0 depois |
| render das rotas irmãs | **0 pixel de diferença** nas três (Route 201, 202 e 219) |
| prova de alcance a pé | 537 células alcançadas; 5/5 warps, 10/10 objetos, 8/8 placas e 6/6 gatilhos |
| blocos novos | **T264** (6 casos, as portas), **T265** (7 casos, as saídas nos dois sentidos), **T266** (2 casos, o NPC) — todos VERDES |
| casos antigos que passam por Sandgem | **T100 volta a 16/16**: o T100.16 e o T100.17 tiveram o roteiro REFEITO por busca em largura no `map.bin` novo (a planta e os seis gatilhos da contraparte mudaram de lugar) |

Um número que o T266.2 corrigiu: o roteiro foi publicado dizendo que o jogador
pararia em (15,14) e o harness devolveu **(16,14)**, porque ali o primeiro aperto
numa direção nova só VIRA. O caso ficou com o número MEDIDO.

### 10.9 O que ficou aberto

1. **As três saídas viram fade.** Sandgem é o entroncamento oeste de Sinnoh
   (Route 201 para Twinleaf, Route 202 para Jubilife, Route 219 para o sul), e
   agora as três travessias param a tela. É o preço do par próprio, é o mesmo de
   Floaroma, e é decisão de gosto do condutor e do Gui, não da execução.
2. **Dois arquivos que o briefing mandava não tocar foram tocados, e por
   necessidade da entrega**: `data/maps/Route201/` e `data/layouts/Route201/`
   (sem eles a saída oeste fica de mão única e Sandgem some do caminho principal)
   e `src/field_door.c` (sem as três entradas na tabela as portas não animam). Em
   Route 201 a invariante do condutor foi PRESERVADA de propósito, com
   `--rota-no-primario`: ela continua com 0 metatile >= 512. Em `field_door.c` o
   acréscimo são 12 linhas no fim de três listas, longe do `DOOR_SIZE_ONE_CELL`.
3. **As duas placas de mata** (bg 6 e bg 7) ficam sendo lidas de um tronco de
   árvore. É melhor do que hoje (onde as oito estão em chão andável, sem poste),
   e o conserto de verdade é desenhar dois postes, que é arte nova.
4. **A quantização da porta de cortina** (21.504, a linha de grama) é visível só
   durante os ~20 quadros da animação.
