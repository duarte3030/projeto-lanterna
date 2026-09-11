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
