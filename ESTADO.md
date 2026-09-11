# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 09/09/2026 (madrugada), na ROM da SEGUNDA E ÚLTIMA QUEBRA DE SAVE do CARTUCHO 1,
`roms/pokemon-claude-2026-09-09-c1-save3.gba` (md5 `d2150aedff3f3c6a65527660fe6e2f15`), medida no HEAD
`0776dc0f58` (esta seção é o commit anterior; o md5 é o da build LIMPA dele). Build LIMPO verde,
`antes_de_empurrar.sh` VERDE nos onze passos, **SAVE COMPATIVEL** (impressão regravada),
**suíte 821 de 821** (820 no laço bloco a bloco mais o T11.3, que só roda com as duas ROMs),
**T11 3 de 3 com o T11.3 INVERTIDO**, e ROM em **94,03%**, com 2.002.412 B livres.
**Essa ROM NÃO tem refino de arte nenhum**, e depois da reversão de 09/09/2026 isso deixou de ser
uma pendência e virou o estado do jogo: ela é BYTE A BYTE idêntica à ROM da reversão,
`roms/pokemon-claude-2026-09-09-c1-sem-refino.gba`. Não há mais duas frentes para consolidar.

**A save do Gui NÃO ABRE MAIS, e isso é de propósito, e a quebra foram DUAS:** `SAVE_LAYOUT_REVISION`
foi de 1 para 2 em 08/09/2026 (as oito quebras pendentes juntas, seção 0.z) e de 2 para 3 na
madrugada de 09/09 (as 36 árvores de berry de Johto, seção 0.ab), esta segunda autorizada pelo Gui na
resposta 58. Nos dois casos o jogo abre em NEW GAME, com o Chapter Jump repondo o progresso. A ÚLTIMA
ROM que ainda abre a save da revisão 1 é `roms/pokemon-claude-2026-09-08-c1-consolidada.gba` (md5
`bc5f411d54ba26ade79fd7653a1f082f`), e a última que ainda abre a da revisão 2 é
`roms/pokemon-claude-2026-09-08-c1-bugs.gba` (md5 `9954be734a93fefcb0cd4180cea64cd7`). **A segunda foi
a ÚLTIMA: a regra "nunca mais" volta a valer, e árvore de berry nova sai das 8 vagas de folga que a
0.ab deixou dentro de `BERRY_TREES_COUNT`.**

**Medição mais recente (09/09/2026, noite): O REFINO DE ARTE FOI REVERTIDO INTEIRO.** O Gui olhou os
renders e recusou o resultado das ondas 2, 3, 3b e 4 ("pedras impedindo o caminho, tile nada a ver,
horroroso"), e as vinte e nove cidades dessas ondas voltaram byte a byte ao desenho de `a0e54260a2`.
Ficam Snowpoint e Canalave, da onda 1, que ele aprovou, e Mahogany em neve. A ROM é
`roms/pokemon-claude-2026-09-09-c1-sem-refino.gba` (md5 `d2150aedff3f3c6a65527660fe6e2f15`), build
LIMPO verde, `antes_de_empurrar.sh` VERDE nos onze passos, **SAVE COMPATIVEL** (a reversão NÃO
quebra save), **suíte 820 de 820** bloco a bloco em 110 blocos (placar em
`roms/c1-placar-reversao.txt`) e ROM em **94,03%**. Essa ROM é byte a byte idêntica à da segunda
quebra de save, `pokemon-claude-2026-09-09-c1-save3.gba`, que é a última desta linha SEM arte de
refino nenhuma. Detalhe na seção 0.ae. **As seções 0.ad e 0.ac descrevem arte que NÃO ESTÁ MAIS NO
JOGO: valem como registro do que foi feito e desfeito, não como estado atual.**

A seção 0.ae abaixo é a REVERSÃO do refino e a lição que ela deixa; a 0.ad é o fechamento do REFINO
de Johto e a 0.ac o do REFINO de Sinnoh, que fecharam no mesmo dia em frentes paralelas e foram
desfeitos no mesmo dia; a 0.ab é a passagem de bastão da rodada da segunda quebra de
save, a 0.aa é a fila de bugs do cartucho 1, a 0.z
a primeira quebra de save, a 0.y a consolidação que saiu antes, a 0.x a pausa de 08/09, a 0.w a da
onda 1, e a 0.v e a 0.u as da rodada 13.

**Este repositório é o CARTUCHO 1: Kanto, Johto, Hoenn e Sinnoh, e o jogo termina na Cynthia.**
Unova e Galar saíram em 07/09/2026 e vivem na branch `cartucho-2` e na tag
`pre-remocao-unova-galar`. Nenhuma das duas volta aqui.

---

## 0.ae A ARTE GERADA DO REFINO SAI: O GERADOR ESPALHAVA PEÇA PARA BATER NÚMERO, E O GUI RECUSOU, 09/09/2026 (reversão das ondas 2, 3, 3b e 4; executor Opus, uma rodada)

**Resposta em uma linha:** o Gui olhou os renders das ondas 2, 3, 3b e 4 do REFINO e
recusou o resultado, com estas palavras: "pedras impedindo o caminho, tile nada a ver,
horroroso". As vinte e nove cidades dessas ondas voltaram byte a byte ao desenho de
`a0e54260a2`, o último commit antes de a primeira delas entrar. Ficam Snowpoint e
Canalave, da onda 1, que ele aprovou, e Mahogany em neve. **Johto voltou também**,
inclusive as cidades que a onda 3 dizia ter deixado modernas: a fonte de Johto é o
HeartGold e Soul, e o Gui disse que aquilo "já é lindo" do jeito que estava.

O QUE DEU ERRADO, e não foi o código. Cada passada de refino rodou verde do começo ao
fim: build limpo, `guarda_save.py` compatível, carimbo de comportamento intacto, régua
de carimbo caindo de 60% e 70% para menos de 20%, suíte fechando. O defeito estava um
degrau acima disso. O gerador recebia um teto de carimbo (a fração do chão andável
ocupada pelo metatile mais repetido) e espalhava peça de decoração até o número passar
por baixo do teto. Ele não desenhava cidade: ele **quebrava tapete**. O resultado tem a
estatística certa e a imagem errada, e as duas coisas não se contradizem em lugar
nenhum. Pedregulho no meio da calçada derruba o carimbo tanto quanto um canteiro no
lugar certo derrubaria.

A LIÇÃO, que é a única coisa que esta rodada deixa de pé:

1. **Portão de planta não é portão de gosto.** O `portao_planta.py`, o carimbo de
   comportamento e a régua de cidades provam que a arte nova não quebrou regra de jogo,
   e provaram certo. Nenhum dos três olha a imagem, e nenhum dos três foi feito para
   isso. Ter os três verdes não é ter a cidade bonita, e tratar verde de portão como
   aprovação foi o erro desta rodada.
2. **Ninguém olhou a imagem antes do Gui.** O `prancha_antes_depois.py` existia e gerava
   a prancha de antes e depois de cada cidade, e mesmo assim as ondas 2, 3, 3b e 4
   inteiras entraram no master sem que nenhum condutor abrisse uma. A primeira pessoa a
   ver o desenho foi o dono do projeto, depois de vinte e nove cidades feitas.
3. **Daqui para a frente, nenhuma arte entra no master sem duas assinaturas de OLHO
   HUMANO na imagem**: o condutor Fable abre o render da cidade e diz que passa, e o Gui
   aprova. Portão verde autoriza a arte a ser MOSTRADA, não a ser aplicada.

COMO O REFINO VOLTA, quando voltar. Não como gerador com teto de número. O refino volta
como **cópia de cidade inteira** de uma ROM hack de referência: pega-se a cidade
desenhada por gente, inteira, com a composição que o autor fez, e traz-se ela para cá,
com o render aprovado ANTES de qualquer byte entrar no master. Peça solta espalhada por
algoritmo está proibida.

O QUE SAIU E O QUE FICOU:

| item | situação |
|---|---|
| 29 `map.bin` de cidade das ondas 2, 3 e 4 | **saiu**, volta a `a0e54260a2` |
| 23 tilesets secundários dessas cidades (`tiles.png`, `metatiles.bin`, `metatile_attributes.bin`, paletas) | **saiu**, inclusive a compactação de Dewford, Rustboro e Mossdeep |
| `src/data/tilesets/graphics.h` (`-num_tiles` de Rustboro e Dewford) | **saiu**, volta a 498 e 503 |
| 16 seções de CREDITS dessas cidades, 919 linhas | **saiu** |
| 18 `dev_scripts/*_kit.json` (a arte importada de hack de terceiro, em paleta e tile) | **saiu**: o único crédito que tinham eram as seções de CREDITS que saíram |
| 22 blocos de teste da decoração nova (T194 a T198, T200, T201, T203 a T206, T210 a T220) | **saiu** |
| Snowpoint e Canalave (onda 1, aprovadas pelo Gui) e Mahogany em neve | **ficou**, com ZERO pixel de diferença |
| fila de bugs (0.aa), inclusive o conserto E3 de tileset | **ficou** |
| as duas quebras de save (0.z e 0.ab) | **ficou**, `guarda_save.py` diz SAVE COMPATIVEL |
| ferramentas: `portao_planta.py`, `regua_cidades.py` consertada, `varia_carimbo.py`, `atlas_metatiles.py`, `compacta_tileset.py`, `prancha_antes_depois.py`, `corpos_repetidos_pokecenter.py`, `render_maps.py` | **ficou** |
| `dev_scripts/<cidade>*.py` e os `.json` de plano de cada passada | **ficou**, como registro do que foi tentado |
| a LENTE do carimbo com os 57 mapas de Hoenn que a onda 4 acrescentou | **ficou**: o buraco que ela achou era real, e tirar os 57 devolveria o buraco |

A PROVA DE QUE A REVERSÃO É REVERSÃO, e não uma arte nova por cima:

- Os 125 arquivos de arte e o CREDITS.md ficaram **byte a byte idênticos** a
  `a0e54260a2` (`git diff a0e54260a2 HEAD` sobre eles: vazio).
- `render_maps.py` das 29 cidades: 26 png idênticos ao render da mesma cidade em
  `a0e54260a2`. As outras três, FloaromaTown, PastoriaCity e SolaceonTown, só diferem no
  retângulo vermelho que o renderizador desenha em cima de `object_event`, porque
  `8a103e07f3` (a quebra de save, canteiros de berry de Sinnoh) mexeu no `map.json`
  delas DE PROPÓSITO. Levando esses três `map.json` para a árvore de `a0e54260a2` e
  renderizando de novo, os três ficam idênticos também. AzaleaTown tem o mesmo tipo de
  mudança por causa de `4bb7045480` e batia mesmo assim.
- Nenhum commit da fila de bugs tocou nenhum dos 125 arquivos revertidos: medido commit
  a commit no intervalo `a0e54260a2..083006891f`. Os consertos E3 (`b528058bcf` e
  `962d0827c2`) escrevem em `ecruteak_city_gym`, `cave_sinnoh` e `valor`, que não são
  tileset de cidade desta lista. **A reversão não devolve bug nenhum.**
- `lente_carimbo.py` acusou 56 achados em exatamente 29 mapas, as 29 cidades, e nenhuma
  rota irmã. Regravado com `--carimba`: 90 entradas antes, 90 depois, 29 mudaram,
  nenhuma entrou e nenhuma saiu. Das 29, as 18 que já estavam carimbadas em
  `a0e54260a2` voltaram ao carimbo DAQUELE commit, valor por valor.
- **A PROVA MAIS FORTE, e ela caiu de graça:** a ROM que sai desta reversão é **byte a
  byte idêntica** a `roms/pokemon-claude-2026-09-09-c1-save3.gba` (md5
  `d2150aedff3f3c6a65527660fe6e2f15`), a ROM da segunda quebra de save, medida em
  `0776dc0f58`, que é o último commit desta linha ANTES de qualquer arte de refino
  entrar na árvore. `cmp` das duas: nenhum byte diferente. E a diferença de ÁRVORE entre
  `0776dc0f58` e o HEAD desta reversão são 64 arquivos, todos eles `dev_scripts/`,
  `ESTADO.md`, `CREDITS.md` ou outro `.md`: **nenhum arquivo que entra na ROM.** Contra a
  ROM do master de antes (`a30b8f0ded4cec32e0a943cfe5606e6b`), a diferença é de
  16.568.381 bytes.

PORTÕES DESTA RODADA: build LIMPO verde (`make clean && make -j8`),
`antes_de_empurrar.sh` **VERDE nos onze passos**, `guarda_save.py` **SAVE COMPATIVEL**
(a reversão NÃO quebra save; `SAVE_LAYOUT_REVISION` continua em 3), `valida_rom.py`
verde, `roda_qa.py` com as travas iguais às do master (Kanto 5, Johto 2, Hoenn 2,
Sinnoh 6, comum 12), `lente_carimbo.py` com **0 achados** depois do `--carimba`, e a
**suíte 820 de 820** bloco a bloco em 110 blocos, 0 vermelho, em 314 s (placar em
`roms/c1-placar-reversao.txt`). ROM em **94,03%**, com 2.002.412 B livres; era 94,07%
com o refino. A ROM está em `roms/pokemon-claude-2026-09-09-c1-sem-refino.gba`, com
`.map` e `.gba.md5` ao lado.

O QUE A SUÍTE PERDEU, e por que não é regressão: 927 casos em 132 blocos viraram 820 em
110. Os 107 casos que saíram são os 22 blocos de decoração nova, e todos eles provavam
metatile que deixou de existir. Nenhum bloco que sobrou mudou de tamanho e nenhum ficou
vermelho.

---

## 0.ad JOHTO FICA MODERNA: SEIS CIDADES SAEM DO TAPETE DE CHÃO REPETIDO, E QUATRO DELAS A CUSTO ZERO, 09/09/2026 (onda 3 do REFINO; condutor Opus, duas retomadas, seis executores Opus)

**REVERTIDA EM 09/09/2026: a arte descrita nesta seção NÃO está mais no jogo.** O Gui
recusou o resultado e as cidades voltaram ao desenho de antes; ver a seção 0.ae. O que
está escrito abaixo vale como registro do que foi feito, e da medição de cada passada,
não como estado atual do repositório.

**Resposta em uma linha:** as seis cidades de Johto que tinham carimbo dominante acima
de 20% caíram todas abaixo dele, a maior de 54,5% para 16,2%, e a onda inteira custou
**2.144 B de ROM**, porque quatro das seis não importaram nem um pixel de fora.

O QUE É O CARIMBO, e por que ele é a régua desta onda. `dev_scripts/regua_cidades.py`
mede a fração das células andáveis A PÉ que estão ocupadas pelo metatile de chão mais
repetido do mapa. É a medida de "tapete": uma cidade com 54% de carimbo é uma cidade em
que mais da metade do chão que o jogador pisa é a MESMA imagem, sem junta, sem canteiro
e sem mudança de piso. O Gui pediu Johto "linda e moderna", e o teto da onda ficou em
20%.

A TABELA, cidade a cidade. "antes" e "depois" são a régua consertada (a de antes da
onda 2 cravava 512 tiles e 6 paletas e não enxergava tileset grande de Johto). "células"
é quantas células do `map.bin` a passada reescreveu, e "sólidas" quantas delas viraram
intransponíveis, que é o número que o alcance a pé tem que cair, nem mais nem menos.

| cidade | antes | depois | células | sólidas | bytes | fonte |
|---|---|---|---|---|---|---|
| CianwoodCity | 54,5% | **16,2%** | 830 de 2.257 | 51 | +1.408 | Scorched Silver (coqueiro, granito, penhasco) |
| BlackthornCity | 47,6% | **13,7%** | 395 de 3.540 | 52 | +928 | Scorched Silver (piso de cratera, com a NOSSA tinta) |
| GoldenrodCity | 26,4% | **12,9%** | 122 de 2.668 | 16 | **-224** | Scorched Silver (losango e bueiro), reindexado |
| EcruteakCity | 25,4% | **6,2%** | 331 de 4.026 | 55 | +32 | GS Chronicles (marco de pedra) + 48 móveis nossos |
| OlivineCity | 22,4% | **8,1%** | 153 de 3.744 | 32 | **0** | NADA importado: 605 peças do atlas que já estavam pagas |
| AzaleaTown | 17,7% | **11,2%** | 216 de 2.232 | 56 | **0** | NADA importado: 42 vagas mortas do próprio secundário |

`Mahoganytown` continua em 24,1% e **não se toca**: ela é a cidade de NEVE, o chão
repetido dela é neve de propósito, e mexer nisso é estragar a leitura da região. As
outras quatro de Johto (`VioletCity` 12,9%, `NewBarkTown` 11,1%, `CherrygroveCity` 7,9%
e as duas acima) já entravam abaixo do teto e ficaram como estavam por falta de tempo,
não por decisão de desenho: quem pegar a próxima onda tem material aí.

GOLDENROD DEVOLVEU 224 BYTES, e isso não é erro de medição. A metrópole foi a cidade
mais cara de resolver e a única que ENCOLHEU a ROM: o `gTileset_Goldenrod` está no TETO
dos dois lados (384 de 384 tiles e 384 de 384 metatiles) e o orçamento de TINTA dele é
ZERO, medido cor a cor (a menor união de um par de vagas em uso é 25 cores e uma vaga
cabe 15, então nenhum par cabe junto e a repactuação de paleta é impossível). A saída foi
importar o calçamento em losango e o bueiro do Scorched Silver e REINDEXAR os dois para
os quatro bege que a paleta 5 do nosso primário `gTileset_JohtoGeneral` já tinha, um dos
quais nenhum pixel da cidade usava. Como as três direções do calçamento são a MESMA peça
escrita com os bits 10 e 11 de espelho da entrada de metatile, elas custam zero tile a
mais, e o `tiles.png` resultante comprime melhor do que o antigo. Medido em build isolado:
`1e7962307e` = 31.563.220 B, `70aea067d5` = 31.562.996 B.

A LIÇÃO MAIS CARA DA ONDA, e ela invalida uma leitura ingênua da régua: **a régua conta
por ID de metatile, e ID não é imagem.** O executor de Azalea renderizou os 1.024
metatiles do par primário mais secundário e comparou pixel a pixel: o metatile 9, que a
régua apontava como carimbo com 17,7%, tem TRÊS CÓPIAS EXATAS vivas no mapa (o 8 com 42
células, o 0 com 24 e o 188 com 58). São quatro ids para uma imagem só, e existem porque
o ATRIBUTO deles difere (0x0007, 0x0000, 0x0000 e 0x1000). Ou seja, a régua lia 17,7%
onde o olho via 227 de 583 células de gramado idêntico, isto é **38,9%**. Consequência
prática, e ela vale para toda cidade daqui em diante: cada variante nova precisou ser
escrita TRÊS vezes, uma por atributo, porque a regra 3 da onda cobra (comportamento,
layerType) idêntico em toda célula que continua andável. Olivine tem o mesmo problema em
menor grau: o carimbo por id caiu para 8,1%, mas somando a trama nas duas orientações
mais o metatile 449 do primário, que é o clone dela, a conta honesta por FAMÍLIA VISUAL
vai de 26,3% para 17,0%. **Quem for medir cidade, meça também a família visual, não só o
id.**

O ATLAS DE METATILES PAGOU A ONDA. A ferramenta nasceu no meio dela (`6dc0cb4877`) a
partir de um número que muda a conta: o primário de Johto tem 640 metatiles DESENHADOS e
cada cidade usa entre 103 e 162 deles. São cerca de quinhentas peças de arte já
compiladas na ROM que ninguém escreveu no `map.bin`. Em Olivine o atlas mostrou 478 peças
livres do primário e 127 do secundário, e dentro delas estavam dois guarda-sóis inteiros,
um painel de toldo, pernas, balizas e bueiro. Em Azalea, as 42 vagas de metatile que a
grama mosqueada ocupou eram vagas MORTAS do próprio `gTileset_AzaleaTown`. É por isso que
essas duas cidades custaram ZERO byte, ZERO tile e ZERO cor: **antes de importar, garimpe
o que já está pago.**

O PORTÃO QUE SEGUROU TUDO é o `dev_scripts/portao_planta.py`, e ele mora FORA dos scripts
que desenham, de propósito: auto-teste de gerador é o gerador se olhando no espelho. Ele
compara o `map.bin` em disco com o do commit de referência e cobra sete coisas: tamanho
igual, elevação intacta em 100% das palavras, colisão 1 para 0 em ZERO células,
(behavior, layerType) idêntico em toda célula que continua andável, layerType COVERED em
toda célula solidificada, alcance a pé pelos DOIS portões (busca em largura respeitando
elevação, mais componentes conexos) e nenhum warp ou evento soterrado. As quatro cidades
desta rodada passaram contra `1e7962307e` com o alcance caindo EXATAMENTE o número de
células solidificadas: 612 para 596, 1.093 para 1.038, 938 para 906 e 563 para 507, e os
pedaços conexos intactos (13, 33, 26 e 6). Cianwood e Blackthorn, que entraram no master
antes desta retomada, foram reconferidas contra `53baeb31ab` e também saíram verdes; em
Cianwood o alcance cai 47 e não 51, porque QUATRO das células solidificadas já estavam
fora do alcance a pé antes da passada, e o portão aceita isso de propósito: ele cobra que
ninguém PERCA caminho, não que toda peça caia em chão pisado.

A PROVA DE VAZAMENTO, e por que a versão ingênua dela é vazia. Cada secundário de Johto é
compartilhado com uma ou duas rotas, e arte nova pode aparecer onde ninguém pediu. A prova
é renderizar o irmão antes e depois e contar pixel diferente, mas ela só vale se o irmão
DE FATO usar o secundário: `Route37` usa o `gTileset_EcruteakCity` e `Route34` e `Route35`
usam o `gTileset_Goldenrod`. Medido: **0 pixel** nos três, contra 39.710 e 22.420 pixels
de mudança nas duas cidades. Prova feita em irmão que não usa o tileset é verde por
construção e não prova nada.

O QUE FICOU PROVADO NO FIM, no master `eb3013fe17`, ROM
`roms/pokemon-claude-2026-09-09-refino-johto.gba` (md5 `a30b8f0ded4cec32e0a943cfe5606e6b`),
build LIMPO de 2 min 16 s, ROM em 94,07%:

- **suíte inteira 891 de 891**, bloco a bloco, 123 blocos, 1.383 s (23,1 min), saída
  inteira de cada bloco em disco. Zero vermelho. O T11.3 continua PULADO e não vermelho,
  porque só roda com `--rom2`. Placar em `roms/c1-placar-refino-johto.txt`.
- `antes_de_empurrar.sh` **VERDE nos onze passos**.
- `guarda_save.py` **SAVE COMPATIVEL**: esta onda NÃO quebra save. A promessa da 0.ab
  segue de pé.
- `lente_carimbo.py`: 39 mapas carimbados, 39 medidos, 0 achado.
- QA A/B honesto (`roda_qa.py` no master de referência contra a árvore nova): **8.280
  achados dos dois lados, 0 novo e 0 sumido**.
- blocos novos desta onda: **T200** (Cianwood, 5), **T201** (Blackthorn, 6), **T203**
  (Goldenrod, 9), **T204** (Ecruteak, 7), **T205** (Olivine, 6) e **T206** (Azalea, 7).
- renders para o Gui vetar, em `Pokemon Claude/amostras-tileset/refino/`:
  `CianwoodCity`, `BlackthornCity`, `GoldenrodCity`, `EcruteakCity`, `OlivineCity` e
  `AzaleaTown`, cada uma com `-antes-depois.png` e `-emulador.png`.

ARMADILHAS QUE ESTA ONDA PAGOU, e que a próxima não precisa pagar de novo:

- **O `gba_runner` é gitignored e envelhece calado.** Ele é a base de toda a suíte e a
  fonte dele está em `dev_scripts/gba_runner.c`. Recompile ANTES de usar, sempre:
  `cc -O2 -o dev_scripts/gba_runner dev_scripts/gba_runner.c -I/opt/homebrew/include
  -L/opt/homebrew/lib $(pkg-config --cflags --libs libpng) -lmgba`.
- **Sem o campo `hora` no caso de teste, o runner NÃO instala fonte de RTC e o cartucho lê
  o relógio do Mac.** Hora, minuto e segundo da parede entram no jogo, e duas rodadas do
  mesmo caso nascem de estados diferentes. Emulador determinístico não quer dizer teste
  determinístico.
- **A primeira tecla de uma direção NOVA só vira o boneco enquanto ele está PARADO desde o
  warp.** Depois que ele já andou, trocar de direção ANDA no mesmo aperto. Errar isso põe
  a prova uma célula fora do lugar.
- **`Image.convert("P")` numa imagem que já é "P" devolve uma CÓPIA e não converte nada.**
- **Textura de chão importada sem a borda vira retalho**: importe a peça com a junta.
- **`mapas_qa.py` ignora o argumento de mapa** e leva uns 4 minutos de qualquer jeito.
- **`pkill -f` com padrão largo atinge as outras frentes.** Nesta onda rodavam três
  condutores ao mesmo tempo (Johto, Sinnoh e Kanto/Hoenn), e um `pkill -f testa_critico.py`
  do condutor de Johto podia derrubar caso em curso das outras duas. Mate por PID ou por
  caminho de worktree, nunca por nome de script.
- **Em arquivo compartilhado (`CREDITS.md`, `dev_scripts/qa/carimbo_comportamento.json`,
  `ESTADO.md`), sempre `git merge master` antes de publicar, e mantenha OS DOIS LADOS.**
  Os conflitos desta onda foram todos aditivos: uma frente escreve a seção dela, a outra a
  dela, e resolver é apagar os três marcadores.
## 0.ac O REFINO DE SINNOH FECHA: AS QUATORZE CIDADES DA REGIÃO SAEM DO TAPETE DE CHÃO REPETIDO, 09/09/2026 (PRD-REFINO.md ondas 1 e 2; condutor Opus, um executor Opus por cidade)

**REVERTIDA EM 09/09/2026: a arte descrita nesta seção NÃO está mais no jogo.** O Gui
recusou o resultado e as cidades voltaram ao desenho de antes; ver a seção 0.ae. O que
está escrito abaixo vale como registro do que foi feito, e da medição de cada passada,
não como estado atual do repositório.

**Resposta em uma linha:** as **14 cidades e vilas de Sinnoh** foram refinadas, o carimbo dominante
(a fração de células andáveis de exterior que usam UM único metatile, a coluna `liso` da
`dev_scripts/regua_cidades.py`) caiu de uma média de 45,9% para 15,0%, **treze das quatorze fecham
abaixo dos 20% que o Gui pediu**, e planta, warps, colisão de caminho e alcance a pé saíram intactos
em todas, medidos arquivo contra arquivo pelo `dev_scripts/portao_planta.py`.

A única acima do teto é `CanalaveCity`, com 24,4%, e ela é da onda 1: não foi remexida nesta.

### As quatorze cidades, medidas

O `carimbo antes` e o `carimbo depois` são a coluna `liso` da régua. O `depois` da tabela foi
REMEDIDO nesta sessão, com a régua rodando na árvore final, e não copiado da mensagem de commit de
cada frente: as catorze bateram. As `células` são as que o `map.bin` mudou, medidas pelo
`portao_planta.py` contra o commit anterior ao refino daquela cidade. Os `bytes` são o que a arte
nova custou de verdade na ROM, ou seja o crescimento do `tiles.4bpp.lz` do tileset secundário
(o `metatiles.bin`, o `metatile_attributes.bin` e as paletas têm tamanho FIXO e não custam byte
nenhum), medido comprimindo os dois lados com o `tools/gbagfx` da própria árvore.

| # | cidade | carimbo antes | depois | células | bytes | render | fonte da arte |
|---|---|---|---|---|---|---|---|
| 1 | `SnowpointCity` | 87,9% | **19,4%** | 997 | +980 | sim | Golden Glazed |
| 2 | `CanalaveCity` | 27,3% | **24,4%** | 114 | +2.364 | sim | Golden Glazed, Scorched Silver |
| 3 | `CelesticTown` | 72,1% | **14,9%** | 311 | +616 | sim | Light Platinum |
| 4 | `SolaceonTown` | 64,3% | **17,2%** | 586 | 0 | sim | Light Platinum (kit de Celestic) |
| 5 | `OreburghCity` | 61,5% | **15,0%** | 597 | +2.160 | sim | Light Platinum |
| 6 | `EternaCity` | 30,0% | **16,1%** | 217 | 0 | sim | Light Platinum (kit de Oreburgh) |
| 7 | `TwinleafTown` | 47,3% | **8,9%** | 211 | +900 | sim | Light Platinum |
| 8 | `SandgemTown` | 37,4% | **11,4%** | 236 | 0 | sim | Light Platinum (kit de Twinleaf) |
| 9 | `JubilifeCity` | 51,4% | **16,6%** | 585 | +408 | sim | Light Platinum |
| 10 | `PastoriaCity` | 36,5% | **16,0%** | 330 | +692 | sim | Light Platinum |
| 11 | `SunyshoreCity` | 39,9% | **18,3%** | 435 | +936 | sim | Light Platinum |
| 12 | `HearthomeCity` | 26,9% | **12,1%** | 622 | +80 | sim | Light Platinum |
| 13 | `VeilstoneCity` | 29,3% | **11,0%** | 778 | +640 | sim | Light Platinum |
| 14 | `FloaromaTown` | 31,4% | **8,7%** | 513 | **0** | sim | nenhuma, arte do próprio repositório |
| | **total** | média 45,9% | **média 15,0%** | **6.532** | **+9.776** | 14 de 14 | |

Os renders antes/depois e as fotos do emulador de todas as quatorze estão em
`amostras-tileset/refino/<Cidade>-antes-depois.png` e `<Cidade>-emulador.png`, no workspace, fora do
git. Floaroma tem uma terceira, `FloaromaTown-pecas.png`, o catálogo das 51 peças da passada.
**É por esses arquivos que o Gui veta cidade a cidade.**

### O que estes números NÃO dizem

A ROM saiu de 31.552.020 B (94,03%, a da 0.ab) para **31.563.156 B (94,07%)**, ou seja
**+11.136 B**, e esse delta **não é só de Sinnoh**: entre uma medida e outra entraram também o
refino de Johto (`CianwoodCity`, `BlackthornCity`, `GoldenrodCity`, `EcruteakCity`) e o de Kanto e
Hoenn (`LittlerootTown`, `PetalburgCity`, `DewfordTown`), que rodaram em frentes próprias e ao mesmo
tempo. O que é de Sinnoh, e está medido tileset a tileset, são os 9.776 B da coluna da tabela.

### As lições que esta onda pagou

1. **Cidade irmã de tileset sai de graça.** `SolaceonTown` divide o `gTileset_Celestic` com
   `CelesticTown`, `EternaCity` divide o `gTileset_Jubilife` com `OreburghCity` e `SandgemTown`
   divide o `gTileset_PetalburgSinnoh` com `TwinleafTown`. As três custaram **zero byte**, porque a
   cidade vizinha já tinha pago o kit e elas só o usaram. Ao planejar onda de refino, agrupar as
   cidades por tileset secundário antes de distribuir as frentes: metade do custo da onda 2 estava
   nesse agrupamento, e ele saiu de graça só porque as frentes calharam de rodar na ordem certa.

2. **Dá para derrubar o carimbo sem importar um único pixel.** `FloaromaTown` foi de 31,4% para 8,7%
   com **zero byte de diferença no `tiles.png`**. A chave: os dois carimbos de flor da cidade são
   justamente as vagas de tile que `src/tileset_anims.c` reescreve a cada quadro. **Referenciar
   vaga animada é de graça e mantém a animação; GRAVAR nela é que é o defeito.** As 41 peças novas
   saíram de mistura de quadrante, espelho, metatiles mortos que o próprio tileset já tinha
   desenhados, e duas vagas de paleta livres recoloridas em 4 índices.

3. **O Light Platinum não serve para tudo, e triagem que REPROVA vale tanto quanto a que aprova.**
   A grama de exterior do hack é (136,184,80) e a nossa é (115,197,164): 87,6 de distância RGB
   contra o critério de 50 da onda. Como no hack toda flor é CHÃO desenhado sobre aquele verde, não
   havia o que importar para Floaroma, e a frente registrou o veredito em vez de forçar a peça.

4. **Ferramenta no `.gitignore` envelhece calada.** O `dev_scripts/gba_runner` no repositório era de
   07/09 às 01:43, contra um `gba_runner.c` de 08/09 às 22:31: o binário estava mais velho que a
   fonte e ninguém tinha como ver. Toda frente recompila o runner do `.c` ANTES de rodar suíte, e o
   `antes_de_empurrar.sh` já compila quando ele falta (mas não quando ele existe VELHO, que é o caso
   pior; isso continua sendo trabalho de quem conduz).

5. **`--carimba` regrava TODOS os mapas, não o seu.** A `lente_carimbo.py` acusou K1 e K2 em
   `FloaromaTown`, e a correção é o rebase do carimbo, que o próprio cabeçalho dela autoriza quando a
   mudança é deliberada. Só que `--carimba` remede os 39 mapas de uma vez: commitar o que ele escreve
   sem conferir apagaria a linha de base das outras frentes. **Conferir o JSON inteiro contra o do
   HEAD antes de `git add`, e commitar só se a diferença for do seu mapa.** Aqui a diferença ficou
   nas duas linhas de `FloaromaTown` e as outras 38 entradas saíram byte a byte iguais.

6. **Proibição no briefing vira buraco no portão.** O buraco do item 5 nasceu de mim: proibi o
   executor de Floaroma de tocar em `carimbo_comportamento.json` para proteger as outras frentes, e
   com isso ninguém regravou a linha de base dele. A suíte do emulador passou verde do mesmo jeito,
   porque quem acusa isso é a lente, não o jogo. **Quem proíbe um arquivo compartilhado herda a
   tarefa que morava nele.**

7. **`git merge master` em onda de várias frentes conflita SEMPRE no `CREDITS.md`, e sempre por
   vizinhança.** Três merges, três conflitos, todos no mesmo ponto: cada frente escreve a seção nova
   logo depois da última. A resolução é sempre a mesma (as duas seções ficam, na ordem das cidades),
   e ela é mecânica o bastante para não merecer leitura linha a linha, desde que se confira depois
   que o número de seções `###` é a soma dos dois lados.

### Portões, e o que cada um provou

- `portao_planta.py` contra o commit anterior a cada cidade: **VERDE nas 12 da onda 2**. Colisão 1
  para 0 em **zero** células nas QUATORZE (inclusive nas duas da onda 1), elevação intacta em 100%
  das palavras, `(behavior, layerType)` idêntico em toda célula que continua andável, alcance a pé
  caindo exatamente as células que a decoração ocupou, e nenhum warp, `object_event`, `bg_event` ou
  `coord_event` soterrado. O único mapa que perdeu um pedaço conexo foi `OreburghCity` (11 para 10),
  e o portão o aceitou porque o pedaço foi COBERTO INTEIRO, não partido.

  **As duas da onda 1 saem VERMELHAS, e a investigação diz que é falso positivo do portão aplicado
  para trás.** O `portao_planta.py` nasceu no meio da onda 2 (commit `15add7b3c2`), depois de
  Snowpoint e Canalave, então esta foi a primeira vez que ele olhou para elas. Ele acusa a regra 5:
  **`SnowpointCity` tem 33 células e `CanalaveCity` 24 que viraram sólidas com `layerType` `NORMAL`
  em vez de `COVERED`** (em Snowpoint, 9 das 33 têm a camada de cima VAZIA e não podem incomodar
  ninguém por construção; sobram 24 e 24 com arte em cima). Só que **esse é o idioma de fábrica**,
  e não um defeito: medido nesta sessão, `RustboroCity` tem 275 células assim e `LilycoveCity` 283,
  e nesses dois mapas o `map.bin` E os tilesets são **byte a byte idênticos ao `upstream/master`**.
  É o beiral de telhado e a copa de árvore: peça alta, sólida, cuja metade de cima desenha ACIMA do
  boneco de propósito, para o jogador passar ATRÁS e o mapa ganhar profundidade. A seção 0.u já
  tinha medido e escrito isso em 06/09 (*"ferramenta que discorda do vanilla está errada"*), e as
  peças acusadas aqui são justamente as altas: em Canalave, os metatiles 887 a 890, o bloco 2x2 do
  kit de porto, em seis cópias. **A regra 5 continua certa COMO DISCIPLINA DE ONDA** (proíbe a onda
  de criar célula nova desse tipo em decoração de chão), e errada como veredito retroativo sobre
  cenário alto. Fica na fila de bugs para um olho no emulador fechar de vez; nenhuma célula foi
  mexida nesta sessão por causa disso.
- `guarda_save.py`: **SAVE COMPATIVEL**, `SaveBlock1` em 15.432 B de 15.872 (97,2%). A janela de
  quebra continua FECHADA: esta onda não gastou um byte de save.
- `roda_qa.py` A/B: **8.280 achados dos dois lados**, diferença zero depois do carimbo regravado.
- Zero pixel nos mapas irmãos: cada frente provou que os mapas que dividem o tileset secundário com a
  cidade mexida saíram com **0 pixel** de diferença, sempre com um controle no mesmo relatório
  (a própria cidade, com o número de pixels que mudou), porque prova de zero em irmão que não usa o
  secundário é vazia por construção. Em Floaroma: `Route205_South` 0 de 786.432, `Route208` 0 de
  661.504, `ValleyWindworks` 0 de 811.008, contra `FloaromaTown` com 50.344 de 313.344 (16,07%).
- Suíte crítica inteira, bloco a bloco, contra a ROM do build LIMPO do master publicado: **902 de
  902**, em 125 blocos. Dos 125, os **110 que já existiam saíram com a contagem IDÊNTICA à do
  `c1-placar-save3.txt`**, sem uma única linha "MUDOU" na tabela, e 15 são blocos novos das três
  frentes, 81 casos (5 desta: T194, T195, T196, T197 e T198). O único vermelho do laço é o T11 2 de
  3, que é como o laço conta o T11.3 pulado por falta de `--rom2`; rodado a parte, o T11 fecha 3 de
  3. Placar em `roms/c1-placar-refino-sinnoh.txt`.
- **A ROM desta seção** é `roms/pokemon-claude-2026-09-09-refino-sinnoh.gba`, md5
  `e6c8809ae0fa8b07aeacdd9e9cefb65c`, do commit `e4574a745a`, com o `.map` do linker e o `.gba.md5`
  ao lado. Ela carrega, além do REFINO de Sinnoh, o de Johto e o de Kanto e Hoenn, que fecharam na
  mesma janela.
- `antes_de_empurrar.sh`: **VERDE**, com build limpo do HEAD em worktree isolada.

### O T11 e a save do Gui

O T11 fecha **3 de 3** contra a base que o próprio caso declara, a ROM da fila de bugs
(`pokemon-claude-2026-09-08-c1-bugs.gba`, md5 `9954be734a93fefcb0cd4180cea64cd7`, revisão 2), e o
T11.3 continua **INVERTIDO**, como a 0.ab deixou: a save de revisão 2 é RECUSADA e o jogo abre em
NEW GAME.

Além disso, e isso é medida NOVA desta onda, a save da revisão 3 foi carregada na ROM nova: gravada
na ROM da 0.ab (`pokemon-claude-2026-09-09-c1-save3.gba`, md5 `d2150aedff3f3c6a65527660fe6e2f15`) e
aberta na desta seção, ela **volta certa**, com o jogador em `MAP_SANDGEM_TOWN` e as flags como
estavam. **O refino de Sinnoh não custou a save de ninguém.**

### Riscos abertos

1. **`CanalaveCity` fica em 24,4%**, acima do teto de 20%. Ela é da onda 1 e não foi remexida nesta.
   Se o Gui quiser dentro do teto, é uma frente de uma cidade só.
2. **A vaga de paleta 10 do `gTileset_MauvilleSinnoh`.** Ela foi recolorida para a papoula vermelha
   de Floaroma. Está livre de metatile VIVO, e por isso muda zero pixel hoje (provado pelos três
   irmãos com 0 pixel), mas **20 metatiles MORTOS ainda a usam** (o prédio rosa, ids 721 a 748 e
   800/801). Quem ressuscitar aquele prédio precisa de outra vaga ou de recuperar as cores do
   histórico. A vaga 12, a outra usada, é limpa de verdade.
3. **O T198.2 discrimina por apenas 2 tiles** (a mata do sudeste fecha logo abaixo da peça). Está
   dito na cara no nome do caso, e o T198.5 cobre o mesmo eixo com 15 tiles em outro pedaço do mapa.
4. **As 48 células de `layerType` `NORMAL` da onda 1** (24 em Snowpoint, 24 em Canalave), acusadas
   pela regra 5 do `portao_planta.py`. A investigação desta sessão diz falso positivo, com o número
   do vanilla ao lado (558 células iguais em dois mapas byte a byte idênticos ao upstream), mas
   quem fecha isso de vez é um olho no emulador, andando na frente do farol de Canalave e do boneco
   de neve de Snowpoint. Entra na fila de bugs, não foi mexido.
5. **A média de 15,0% é de Sinnoh, e Sinnoh agora é a região mais bem tratada do cartucho.** Kanto e
   Hoenn ainda têm cidade de tapete liso, e a onda 4 do REFINO, que roda em frente própria, é quem
   está atacando isso.

---

## 0.ab A SEGUNDA E ÚLTIMA QUEBRA DE SAVE: AS 36 ÁRVORES DE BERRY DE JOHTO GANHAM VAGA PRÓPRIA, 08/09/2026 (madrugada de 09/09; autorizada pelo Gui na resposta 58; executor Opus)

**Resposta em uma linha:** as 36 árvores de berry mudas de Johto e do `WorldHub` ganharam id,
script e berry, `BERRY_TREES_COUNT` subiu de 178 para 222 e `SAVE_LAYOUT_REVISION` foi de 2 para 3.
**A save da revisão 2 não abre mais, e isso é de propósito.** Esta foi a **SEGUNDA e ÚLTIMA**
quebra: a partir daqui a regra "nunca mais" volta a valer, e quem precisar de árvore de berry nova
gasta uma das 8 vagas de folga que ficaram livres.

A promessa da 0.z era que a quebra tinha sido ÚNICA. Ela foi desfeita **por decisão explícita do
Gui, no mesmo dia**, e não por descuido: o item 12 da 0.aa mediu 36 árvores lendo `berryTrees[0]`,
deixou-as como estavam porque a janela tinha fechado, e a resposta 58 reabriu a janela com todas as
letras, *"pode subir o teto das IDs, não tem problema quebrar save"*.

A ÚLTIMA ROM que ainda abre a save da revisão 2 é
`roms/pokemon-claude-2026-09-08-c1-bugs.gba` (md5 `9954be734a93fefcb0cd4180cea64cd7`).
A desta onda é `roms/pokemon-claude-2026-09-09-c1-save3.gba` (md5 `d2150aedff3f3c6a65527660fe6e2f15`).

### Placar, medido nos dois lados

| medida | antes (`135b9050fa`) | depois (`0776dc0f58`) |
|---|---|---|
| ROM usada | 31.551.796 B (94,03%) | **31.552.020 B (94,03%)** |
| ROM livre | 2.002.636 B | **2.002.412 B** |
| EWRAM | 225.972 B (86,20%) | **226.324 B (86,34%)** |
| IWRAM | 29.036 B (88,61%) | **29.036 B (88,61%)** |
| SaveBlock1 | 15.080 B de 15.872 (95,0%) | **15.432 B de 15.872 (97,2%)** |
| `BERRY_TREES_COUNT` | 178 | **222** (36 árvores mais 8 de folga) |
| árvores de berry com id próprio | 176 de 212 | **212 de 212** |
| `SAVE_LAYOUT_REVISION` | 2 | **3** |
| `guarda_save.py` | SAVE COMPATIVEL | **SAVE COMPATIVEL** (impressão regravada) |
| casos na suíte | 817 | **821** |
| suíte | 817 de 817 | **821 de 821** |
| T11 | 3 de 3 | **3 de 3, com o T11.3 INVERTIDO** |

### O que entrou, passo a passo

Quatro commits, cada um buildável, cada um com a medida no corpo da mensagem.

1. **As 36 árvores ganham id, script e berry** (`dev_scripts/berries_johto.py`). Elas já estavam
   desenhadas no mapa desde a importação de Johto, mas com `trainer_sight_or_berry_tree_id` igual a
   0, `script` igual a `"0"` e `MOVEMENT_TYPE_LOOK_AROUND`. **Id 0 não é "sem id":** é a vaga
   `berryTrees[0]`, que jogo nenhum planta, então as 36 liam o mesmo estado permanentemente vazio e
   o aperto de A nem chegava no `BerryTreeScript`. Agora são os ids 178 a 213, com
   `BerryTreeScript` e `MOVEMENT_TYPE_BERRY_TREE_GROWTH`, e cada uma plantada no `new_game.inc` com
   `BERRY_STAGE_BERRIES`.
2. **`SAVE_LAYOUT_REVISION` 2 para 3**, com a base do T11 trocada no MESMO commit.
3. **O bloco T193**, quatro casos no emulador sobre uma árvore de Johto.
4. **O T187.11 remedido**, de dez apertos de A para doze. Foi o único vermelho que a suíte inteira
   devolveu, e ele não é do jogo: é a janela estreita de roteiro que o próprio caso avisava por
   escrito que teria de ser remedida.

### De onde veio a berry de cada uma, e o que NÃO veio da fonte

A fonte é `fontes-mapas/hns` (Heart n Soul), que já é a fonte dos mapas de Johto desta árvore. Ela
desenha as **MESMAS 36 árvores nas MESMAS coordenadas**, cada uma com a berry escrita no nome do id
e plantada com `BERRY_STAGE_BERRIES` no `new_game.inc` dela. A casação é por **coordenada exata**, e
árvore sem fonte seria RECUSADA em vez de receber berry escolhida no chute: **zero recusadas, 36 de
36**. Saem 16 espécies: ORAN x4; ASPEAR, CHERI, CHESTO, LEPPA, PECHA, PERSIM, RAWST e SITRUS com 3
cada; LUM com 2; e GREPA, HONDEW, KELPSY, POMEG, QUALOT e TAMATO com 1. O `WorldHub` fica com uma de
cada uma das 16, que é o jardim de berries que a fonte desenhou lá.

**O id da fonte NÃO foi reaproveitado, só a espécie**, e isso é medida e não preferência: a fonte
REPETE id entre mapas. O `WorldHub` dela usa os mesmos ids das rotas de Johto, e a Route26 dela usa
`BERRY_TREE_ROUTE_118_SITRUS_1`, que é de Hoenn. **Id repetido é o defeito que esta onda existe para
matar**: duas árvores no mesmo índice são a mesma árvore, e colher uma esvazia a outra. Cada uma das
36 tem id próprio, em append depois do 177.

### O relatório de ANTES do `guarda_save.py`, com a revisão ainda em 2

Duas linhas, e a primeira sozinha já mataria a save:

```
SAVEBLOCK1 MUDOU DE TAMANHO: 15080 B -> 15432 B. Tudo que vem depois do campo que
cresceu muda de lugar, e save antiga passa a ser lida errada.

SAVE_LAYOUT_REVISION NAO SUBIU: o layout da save mudou (1 quebra(s) acima) e a
revisao continua 2. `SECTOR_SIGNATURE` fica igual, entao a save do layout ANTIGO
continua sendo aceita e passa a ser lida DESLOCADA, em silencio, sem erro nenhum
na tela. Suba SAVE_LAYOUT_REVISION em include/save.h para 3.
```

Com a revisão em 3 a segunda linha vira **REVISÃO DE LAYOUT DA SAVE MUDOU**, que é a invalidação
DELIBERADA, e foi em cima disso que a impressão foi regravada com `--gravar`.

**O `guarda_save.py` não tem `BERRY_TREES_COUNT` na lista `MACROS_DE_TAMANHO`, e mesmo assim pegou.**
Quem pegou foi `tamanho_saveblock1()`, que lê o `sizeof` do ELF em vez de confiar na lista de macros:
352 B a mais aparecem quer a macro esteja na lista, quer não. É o mesmo raciocínio que o item 4 do
docstring dele já dizia, e a lista de macros é conveniência, não a rede.

### O bloco T193: quatro números no MESMO tile

A árvore medida é a `BERRY_TREE_JOHTO_ROUTE30_ORAN_2`, em Route30 (23,38), alcançada pelo warp 0.
Os quatro casos rodam o MESMO percurso com a MESMA hora de cartucho forçada, e **nenhum vale
sozinho**:

| caso | o que faz | ORAN BERRY na bolsa |
|---|---|---|
| T193.2 | anda até o tile, sem aperto nenhum de A | **0** |
| T193.1 | colhe | **2** |
| T193.3 | roda a colheita DUAS vezes seguidas | **2**, e não 4 |
| T193.4 | colhe e planta de volta | **1** |

O T193.3 é o que mede o conserto de verdade, o **ESTADO SALVO**: a primeira colheita chama
`ObjectEventInteractionRemoveBerryTree`, que grava `BERRY_STAGE_NO_BERRY` na vaga DELA, e a segunda
interação já acha TERRA. Enquanto as 36 estavam com id 0 não havia vaga própria para gravar nada. A
prova é `item_0x208` (`ITEM_ORAN_BERRY` = 520) lido da BOLSA dentro do SaveBlock1, com os offsets
medidos da fonte pelo probe do harness, e não do texto da caixa de fala; as telas do fim da execução,
gravadas em PNG pelo próprio harness, confirmam por um caminho independente ("It's soft, loamy soil.
Want to plant a BERRY?" no T193.3 e "One Oran Berry was planted here." no T193.4).

### Os achados desta onda

**1. O número 2 é o `minYield` da ORAN, e é determinístico.** A primeira leitura do caso esperava 1 e
veio 2, e a explicação estava no motor, não no acaso: `setberrytree` cai em `SetBerryTree`
(`src/berry.c`), que com `OW_BERRY_ALWAYS_WATERABLE` em FALSE e estágio `BERRY_STAGE_BERRIES` chama
`CalcBerryYield`; lá `min` vira `berryYield` (0 numa árvore nova) mais o `minYield` da berry, e
`CalcBerryYieldInternal` devolve `min` **sem sortear nada** quando a árvore nunca foi regada, que é o
caso de toda árvore de jogo novo. Nenhum `Random()` entra na conta, e por isso o caso pode cobrar o
número exato em vez de uma faixa.

**2. O warp do menu de debug NÃO entrega o jogador em cima do warp.** Ele entrega um tile ADIANTE: o
warp 0 de Route30 está em (26,39) e o jogador aparece em (26,40). A rota do T193 foi medida no
próprio harness antes de ser escrita, e não deduzida do `map.json`.

**3. Toque de direção com o boneco olhando para outro lado só VIRA, não anda.** Quatro toques de
LEFT valem TRÊS passos. A primeira versão da rota andava dois tiles a menos do que a conta do
`map.json` prometia, e o sintoma era "a colisão está errada".

**4. As 36 estavam com `MOVEMENT_TYPE_LOOK_AROUND`, o movimento de GENTE.** Isso não aparece em
nenhuma das contas de id: uma árvore com id certo e movimento de gente não reavalia o estágio da
planta (`MovementType_BerryTreeGrowth`, `src/event_object_movement.c:4386`). Os três campos andam
juntos, e a fonte já os tinha juntos.

**5. O único vermelho da suíte inteira foi um teste, e ele avisou que seria.** O T187.11 prova que a
música de vitória é da região, e o roteiro dele ganha a batalha com N apertos de A num ponto que o
próprio caso descrevia como janela ESTREITA, com a escada de N medida em 07/09/2026. Com esta onda a
escada andou: medido nos DOIS lados, dez apertos ficam VERDES na ROM base e VERMELHOS na desta onda,
dizendo faixa 744 (`MUS_DP_VS_WILD`, a batalha ainda correndo). A escada nova, varrida aperto por
aperto: 10 = VS_WILD, 11 a 14 = VICTORY_WILD, 15 e 16 = a música do mapa. Doze é o meio do patamar, e
o patamar de agora tem QUATRO apertos de largura contra UM na medição de 07/09, ou seja o caso ficou
mais robusto. **A causa é dedução declarada, não medida:** `EventScript_ResetAllBerries` ganhou 36
linhas, o roteiro é contado em QUADROS, e alguns quadros de deslocamento no começo mudam o estado do
gerador quando o encontro selvagem dispara. Nenhum `setberrytree` chama `Random()`; o que anda é o
relógio de quadros. **A lição é para o próximo:** caso cuja prova depende de contagem de quadros de
batalha é caso que qualquer onda pode derrubar, e o remédio é o que este já trazia, a escada escrita
no `nome`, que transformou meia hora de caça em uma varredura de sete execuções.

### O que fica aberto

- **`SaveBlock1` está em 97,2% do teto de 15.872 B**, com 440 B livres. As 8 vagas de folga de
  `berryTrees` custaram 64 B desses. Campo novo em struct de save agora é assunto de medição, não de
  hábito: 440 B são 55 vagas de berry, ou muito menos de qualquer outra coisa.
- **A janela de save fechou de novo, e desta vez sem pendência conhecida atrás dela.** Os cortes que
  a 0.z listou como "sem relação com save" (os 63 VENT e BOLLARD, os 2 canteiros de Route214)
  continuam sem relação.
- A worktree `c1-t11-consolidada` (`849e8565ee`) **pode ser apagada**: a base do T11 passou a ser a
  `c1-t11-bugs` (`135b9050fa`), com a ROM `pokemon-claude-2026-09-08-c1-bugs.gba`.
- **A ROM desta seção não tem o refino de arte de Sinnoh, e o master tem.** A frente de arte rodou em
  paralelo e entrou no master em `53baeb31ab`, depois do commit em que esta ROM foi medida. O merge
  desta frente com aquela está feito e o HEAD builda limpo com `antes_de_empurrar.sh` VERDE, mas a
  suíte de 821 casos foi rodada ANTES do merge: **quem for consolidar roda a suíte inteira no HEAD
  merged e tira a ROM de lá.** O que JÁ foi medido no HEAD merged (`a012ad7c7d`, ROM 31.557.012 B,
  94,05%, md5 `1de090bc8e7463cbbe59c17b0d0dc0f4`): `antes_de_empurrar.sh` verde nos onze passos, e os
  blocos T193 (4 de 4), T187 (11 de 11), T126 (15 de 15), T132 (42 de 42) e T11 com as duas ROMs (3
  de 3). Os outros 105 blocos não foram rodados depois do merge.

### A suíte, e como ela foi rodada

**821 de 821**, e a conta tem duas linhas que precisam ser ditas em voz alta em vez de escondidas
no total. O laço bloco a bloco (110 blocos, o placar de cada um gravado em disco a cada bloco)
devolveu **819 de 821**, com DOIS vermelhos:

- o **T11.3, que só roda com as DUAS ROMs**: sem `--rom2` ele é pulado e o laço conta como falha.
  Rodado à parte, com a ROM da fila de bugs (`pokemon-claude-2026-09-08-c1-bugs.gba`) e a árvore dela
  na worktree `c1-t11-bugs`, o **T11 fecha 3 de 3**, com o T11.3 continuando INVERTIDO: a save da
  revisão 2 é RECUSADA e o jogo abre no quarto de jogo novo;
- o **T187.11**, que é o achado 5 acima. Ele foi REMEDIDO (dez apertos de A para doze) e o bloco
  rodou de novo, fechando 11 de 11. **É esse 11 que está no `roms/c1-placar-save3.txt`**, e o
  cabeçalho do arquivo diz que ele veio de uma segunda execução, para ninguém ler o placar achando
  que o laço saiu limpo de primeira.

Com o T187 consertado o laço vale **820 de 821**, e com o T11.3 rodado à parte, **821 de 821**.

Os 4 casos novos desta onda são o bloco T193 inteiro; nenhum caso saiu da suíte.

A ROM saiu depois da meia-noite, por isso o nome dela traz **09/09** enquanto a onda inteira e a
autorização do Gui são de **08/09**.

O placar bloco a bloco está em `roms/c1-placar-save3.txt`, com a coluna "antes" tirada da coluna
"depois" do `c1-placar-bugs.txt`.

---

## 0.aa A FILA DE BUGS DO CARTUCHO 1: DOZE ITENS, E QUATRO DELES NÃO ERAM O QUE O ENUNCIADO DIZIA, 08/09/2026 (condutor Opus, cinco executores Opus)

**Resposta em uma linha:** os doze itens da fila foram fechados, e `guarda_save.py` disse
**SAVE COMPATIVEL em todos os 22 commits**, ou seja a promessa da 0.z está de pé: a quebra
de save foi ÚNICA e nenhuma frente desta rodada quebrou de novo. Quatro itens mudaram de
enunciado ao serem medidos, e um deles (o nível de encontro acima de 100) simplesmente não
era bug.

### Placar, medido nos dois lados

| medida | antes (`f33055bf27`) | depois |
|---|---|---|
| ROM usada | 31.546.508 B (94,02%) | **31.551.796 B (94,03%)** |
| ROM livre | 2.007.924 B | **2.002.636 B** |
| EWRAM | 225.972 B (86,20%) | **225.972 B (86,20%)** |
| IWRAM | 29.036 B (88,61%) | **29.036 B (88,61%)** |
| SaveBlock1 | 15.080 B de 15.872 (95,0%) | **idêntico** |
| `guarda_save.py` | SAVE COMPATIVEL | **SAVE COMPATIVEL** |
| `guarda_colisao_vars.py` | 24 colisões, **1 REPROVA (0x4083)** | **23 colisões, ZERO reprova** |
| travas do `roda_qa.py` | Kanto 5, Johto 2, Hoenn 2, Sinnoh 6, comum 12 | **idênticas** |
| achados E3 (`mapas_qa.py`) | 1.305 | **859** |
| Dex obtenível | 1.571 de 1.571 | **1.571 de 1.571** |
| espécies no MATO que são lenda | 31 | **0** |
| T11 | 3 de 3 | **3 de 3** |
| casos na suíte | 790 | **817** |
| suíte | 790 de 790 | **817 de 817** |

### Item a item

| # | item | veredito | onde |
|---|---|---|---|
| 1 | colisão `VAR_TREM_MAGNETICO` sobre `0x4083` | **FEITO**, e o estrago era dos dois lados | `2c015f808e` |
| 2 | `treinadores_faltantes_b4.py --demo` vermelho | **FEITO**, os DOIS lados do assert estavam velhos | `0bed4e26c6` |
| 3 | níveis de encontro acima de 100 | **NÃO É BUG**, medido; a ferramenta que media é que estava morrendo | `4ba597ed88` |
| 4 | corpos repetidos em interiores de Sinnoh | **FEITO**, 10 corpos em 7 mapas; o número de 06/09 não reproduz mais | `91247df72b`, `1177eef863` |
| 5 | achados E3 restantes | **FEITO**, 1.305 para 859; os 33 telhados de Sinnoh já não existiam | `b528058bcf`, `962d0827c2` |
| 6 | Safari de Johto sem script | **FEITO**, com as três saídas lendo o `dynamicWarp` | `0ba831a7d0` |
| 7 | maré baixa do Lago da Fúria | **FEITO**, e achou um defeito no `special` do Emerald | `3194d1743b` |
| 8 | prêmio de série da torre de Olivine | **FEITO**; a torre já estava aberta desde a chegada | `da2a231e92` |
| 9 | míticos de macro no mato | **FEITO**, 31 saíram do mato e viraram estático | `5502bff203`, `586b9909dc` |
| 10 | Frontier Brains com a Fase F | **FEITO**; o NÍVEL já saía certo sozinho | `ec90eb1ee7`, `880834a23d` |
| 11 | seletor de mecânica de batalha | **FEITO**; a preferência da IA não tem o que preferir | `0cbcc26b30` |
| 12 | 36 árvores de berry sem id | **FICAM**, e o motivo está escrito no `berry.h` | `2800828ada` |

### Os quatro itens que mudaram de enunciado quando foram medidos

**1. Nível de encontro acima de 100 não é bug.** `MAX_LEVEL` é **255**
(`include/constants/pokemon.h:156`) e `gExperienceTables` é `[][MAX_LEVEL + 1]`
(`include/pokemon.h:730`), ou seja o motor tem experiência definida até lá. Dos 9.974 slots
de `gWildMonHeaders`, 3.685 passam de 100, **zero** passa de 255 e o maior é 196. Isso é a
escada da Fase F que `dev_scripts/curva_selvagem.py` aplicou de propósito, com a tabela
escrita no próprio arquivo: Kanto 3-46, Johto 42-122, Hoenn 90-146, Sinnoh 140-196. Os
únicos 155 slots fora da faixa da região são **inalcançáveis**: moram nos 132 headers de
versão LEAFGREEN, e `GetCurrentMapWildMonHeaderId` (`src/wild_encounter.c:374`) devolve o
PRIMEIRO header que casa com o mapa, que nos 125 mapas com mais de um header é sempre o
EMERALD. Nada foi reescalado. O que estava quebrado era a ferramenta: `curva_selvagem.py`
morria de `IndexError` antes de imprimir a linha de Sinnoh, porque `encontros_b7.ORDEM`
ainda lista Unova e a lista de níveis dela voltava vazia.

**2. Os 33 telhados de Pokécenter de Sinnoh já não existiam.** Medido nos metatiles que o
próprio ESTADO 0.u nomeia: 7 células andáveis em `7b9a11ce64`, **zero** em `bce66c4718`, zero
no master. A rodada 13 fechou a classe na mesma madrugada em que anotou a pendência. Em vez
deles entraram 57 células de Sinnoh da classe do brejo (caverna e mato), que ninguém tinha
levantado.

**3. Os 405 de Johto não eram todos de camada.** Rodar `conserta_camada_metatile.py --regiao
Johto` grava zero, e o próprio script diz por quê: todos os alvos também aparecem em célula
sólida. Abrindo as duas camadas de cada metatile, são TRÊS defeitos: 46 de camada (o ginásio
de Morty, onde 107 dos 108 warps ficam em cima do metatile preto e fechar a célula quebraria
o quebra-cabeça), 345 de colisão em parede desenhada na camada de cima, e 312 de enchimento
preto entre as duas salas do laboratório de New Bark, que a BFS invade pelo warp 1.

**4. Os 31 corpos repetidos de 06/09 não reproduzem mais.** Com as mesmas provas, os
interiores casados têm hoje **810 objetos nossos contra 857 na fonte**: no agregado temos
MENOS gente que o Platinum. Vinte e quatro mapas têm mais objetos que a fonte, somando 43
corpos de excesso bruto, e a maior parte disso NÃO é cópia: é o povoamento de
`povoa_cidades.py` (os 210 NPCs de 07/09), que tem script próprio e por isso não passa nem
pela prova do corpo mudo nem pela de "cópia de quem fala". A contagem de 31 media excesso
BRUTO por mapa.

### Os achados que ninguém tinha previsto

**1. O trem magnético e a Selphy da Lost Cave se apagavam.** `VAR_TREM_MAGNETICO` (nosso,
nascido na onda 3) e `VAR_MAP_SCENE_FIVE_ISLAND_LOST_CAVE_ROOM10` (do FireRed) dividiam o
endereço `0x4083`, os dois usados em `data/maps`. Quem andasse de trem saía com `0x4083` em
1 e a cena da Selphy, que roda por `map_script_2 VAR_..., 0`, nunca mais disparava; quem
achasse a Selphy fazia a estação se comportar como se o jogador não tivesse descido. Quem
andou foi o lado do FireRed, para `0x41D6`, pelo mesmo remédio das 19 vars de Kanto do J6, e
o motivo é medido: `guarda_save.py` guarda a ATRIBUIÇÃO de todo apelido de `vars.h`, então
mover `VAR_TREM_MAGNETICO` seria APELIDO MOVIDO e reprovaria o portão.

**2. `UpdateShoalTideFlag` não escreve a flag sempre, e isso quase passou como verde.** Ele
exige `IsMapTypeOutdoors(GetLastUsedWarpMapType())`, ou seja olha o ÚLTIMO WARP USADO, não o
mapa em que o jogador está. Na Shoal Cave funciona, porque lá se entra por warp vindo da
rota; no Lago da Fúria o jogador entra ANDANDO por conexão com a Route 43, e o último warp
continua sendo a porta que ele usou antes, em outro canto do mundo. Com um interior ali, a
flag não era escrita e a maré congelava. **O caso de maré baixa passava por coincidência**,
porque a flag nasce apagada; foi o PAR NEGATIVO (relógio nas 0h, que a tabela diz ser maré
alta) que abriu vermelho e denunciou. Entrou `AtualizaMareDoLagoDaFuria`, com a mesma tabela
e a mesma flag, sem aquele portão.

**3. Quinze estáticos numa janela travam o jogo, e nenhuma ferramenta via.** A Viridian
Forest recebeu 15 míticos e o jogo parou em `OUT OF SPRITE SLOTS` (`src/sprite.c:452`), na
cara do jogador. O executor achou no emulador e mediu o limite por bisseção com flags de
HIDE: 9 objetos na janela travam, 8 andam. Nasceu `TETO_SPRITE_DEX = 8`.

**4. Dois executores escolheram o mesmo número de bloco de teste.** O do seletor e o do
Safari criaram, cada um por conta, o bloco 188, com ids T188.1 a T188.8 e T188.1 a T188.6.
Os arquivos não conflitam no git (nomes diferentes) mas os IDS sim. O Safari virou 189.
**Número de bloco de teste é recurso compartilhado, como faixa de flag: quem distribui o
trabalho reserva o número no briefing.** Os blocos seguintes já saíram reservados (190
míticos, 191 maré, 192 Frontier).

**5. Regra mecânica que casa com a fonte precisa de peneira contra o que a suíte já prova.**
A primeira passada do item 4 apagou 11 corpos e um deles derrubou o T113.1, escrito de
propósito na leva de povoamento para provar que aquele NPC existe e é sólido. As duas
leituras eram defensáveis (a régua manda ficar com quem FALA; o princípio do item manda
ficar com quem está na posição da FONTE), e escolher é conteúdo, não medição. O objeto
voltou e a ferramenta ganhou `PROTEGIDOS`, com o motivo escrito por mapa.

**6. Texto de script sem `$` final passa por build verde e por teste verde.** A fala nova da
torre de Olivine saiu sem o terminador e o motor emendou a fala seguinte no meio da caixa
("he BATTLE TOWER of something useful.Welco"). Quem pegou foi o PNG, não a ferramenta.

### O que fica aberto

- **As 37 células E3 que sobraram estão presas ao carimbo de comportamento.** Johto
  `GoldenrodCity` 14 e `Route26` 2 (conserto de colisão); Sinnoh `SunyshoreCity` 14,
  `VeilstoneCity` 4, `EternaCity` 2 e `Route209` 1 (conserto de camada); mais as 4 de
  `CanalaveCity` do `conserta_colisao_sinnoh.py`. Fechá-las exige regravar
  `dev_scripts/qa/carimbo_comportamento.json`, que é do REFINO, e por isso vira rodada
  própria depois que o refino fechar. **É a pergunta 48.**
- **`SinnohLeague` tem 36 achados E3 no `gTileset_EliteFour`**, que é compartilhado com
  Hoenn e vem do vanilla. Mexer ali muda Hoenn junto.
- **A preferência de mecânica por treinador para a IA não tem o que preferir hoje.** Medido:
  `tools/trainerproc/main.c:2211` emite `.shouldUseDynamax` OU `.teraType`, num `else if`, e
  a varredura de `src/data/trainers*.h` acha 6.988 mons de treinador, 54 com Dynamax, 5 com
  Tera e **zero com os dois**. Mega e Z dependem de item na mão, e segurar Mega Stone ou
  Z-Crystal já derruba Dynamax e Terastal. **É a pergunta 49.**
- **O Ouro do Brandon deixou de ser os três pássaros lendários e virou a família Regi
  completa**, o que põe Regigigas com Slow Start em campo. É escolha de desenho. **É a
  pergunta 50.**
- **`JubilifeCity_Flat2_F3` tem dois `POKEFAN_M` que são a mesma pessoa**, e a escolha de
  qual fica é de conteúdo. **É a pergunta 51.**
- **`SnowpointCity_Gym` guarda um corpo repetido no índice 8 de 20 objetos.** Ele fica: não é
  sufixo da lista, e apagar do meio desloca o índice de objeto que a save guarda.
- ~~**As 36 árvores de berry de Johto e do `WorldHub` continuam sem id.**~~ **FECHADO em 09/09/2026
  pela seção 0.ab**, com a janela de save reaberta pela resposta 58 do Gui. O texto abaixo é o que
  valia quando esta seção foi escrita.
- **As 36 árvores de berry de Johto e do `WorldHub` continuam sem id.** Há UMA vaga dentro de
  `BERRY_TREES_COUNT` (a 57, que o próprio pokeemerald já reservava), e gastá-la numa das 36
  faria uma rota de Johto ter árvore viva e as outras dezenove não. O conserto de verdade
  custa save.
- **Quatro dos 31 estáticos novos param do lado errado no roteiro de prova.** O objeto está de
  pé (provado no Genesect, com a batalha lida da EWRAM); o errado é o `para` que o planejador
  de rota escreveu na tabela.
- **`VeilstoneCityMart` não casa com nenhum header do Platinum** pela `chave()` do importador,
  então fica fora da varredura de corpo repetido.
- **A mensagem do commit `4ba597ed88` diz "11.974 slots"**; o número certo, recontado, é
  **9.974**. O resto da medição daquele commit está correto.

### A suíte, e como ela foi rodada

**817 de 817.** O laço bloco a bloco (109 blocos, o placar de cada um gravado em disco a cada
bloco, em `roms/c1-placar-bugs.txt`) fecha **816 de 817**, e o único vermelho dele é o
**T11.3, que só roda com as DUAS ROMs**: sem `--rom2` ele é pulado e o laço conta como falha.
Rodado à parte, com a ROM da consolidação (`pokemon-claude-2026-09-08-c1-consolidada.gba`) e a
árvore dela na worktree `c1-t11-consolidada`, o **T11 fecha 3 de 3**, com o T11.3 continuando
INVERTIDO: a save de layout velho é RECUSADA e o jogo abre no quarto de jogo novo.

Os 27 casos novos desta rodada: T126.14 e T126.15 (prêmio da torre de Olivine, com par
negativo), T188.1 a T188.8 (seletor de mecânica), T189.1 a T189.6 (Safari de Johto),
T190.1 a T190.4 (míticos de macro), T191.1 a T191.5 (maré do Lago da Fúria) e T192.1 e
T192.2 (Frontier Brains).

---

## 0.z A QUEBRA ÚNICA DE SAVE DO CARTUCHO 1: UMA VEZ SÓ, E NUNCA MAIS, 08/09/2026 (PRD-CARTUCHO-1.md onda 3; condutor Opus, sem executores)

> **ATUALIZAÇÃO DE 09/09/2026: o "nunca mais" desta seção durou um dia.** A seção 0.ab é uma SEGUNDA
> quebra, `SAVE_LAYOUT_REVISION` de 2 para 3, e ela foi autorizada pelo Gui na resposta 58 de
> 08/09/2026, com todas as letras: *"pode subir o teto das IDs, não tem problema quebrar save"*. Esta
> seção fica como está porque história não se recalcula; o que ela promete valeu até a 0.ab.

**Resposta em uma linha:** as oito quebras que o projeto tinha pendentes entraram numa só,
`SAVE_LAYOUT_REVISION` foi de 1 para 2, a ROM devolveu **70.172 B (68,5 KB)** e a suíte fechou
**790 de 790** (789 no laço bloco a bloco mais o T11.3, que só roda com as duas ROMs), com ZERO regressão nos 104 prefixos. **A save antiga do Gui não abre mais, de propósito**, e a promessa que vem junto é
que **nenhuma onda posterior tem licença para quebrar de novo**.

A última ROM que ainda abre a save antiga continua sendo
`roms/pokemon-claude-2026-09-08-c1-consolidada.gba` (md5 `bc5f411d54ba26ade79fd7653a1f082f`).
A desta onda é `roms/pokemon-claude-2026-09-08-c1-save2.gba` (md5 `1af8c4da0be3b4f674df5b08593b7cd6`).

### Placar, medido nos dois lados

| medida | antes (`a0e54260a2`) | depois (`5e25c183ce`) |
|---|---|---|
| ROM usada | 31.616.680 B (94,23%) | **31.546.508 B (94,02%)** |
| ROM livre | 1.937.752 B | **2.007.924 B** |
| EWRAM | 225.856 B (86,16%) | 225.972 B (86,20%) |
| IWRAM | 29.036 B (88,61%) | 29.036 B (88,61%) |
| SaveBlock1 | 14.964 B de 15.872 (94,3%) | **15.080 B de 15.872 (95,0%)** |
| mapas em `map_groups.json` | 2.406 | **1.594** |
| grupos de mapa | 129 de 255 | **103 de 255** |
| layouts na ROM | 2.055 | **1.286** |
| ids de treinador declarados | 2.875 | **2.196** |
| maior id de treinador | 3.267 | **2.046** |
| `MAX_TRAINERS_COUNT` | 4.000 | **2.200** |
| `FLAGS_COUNT` | 12.856 | **10.584** |
| `BERRY_TREES_COUNT` | 128 | **178** |
| símbolos com nome de Unova ou Galar no `.map` | 2.383 | **173** (só formas galarianas de Pokémon) |
| `guarda_save.py` | SAVE COMPATIVEL | **SAVE COMPATIVEL** (impressão regravada) |
| `SAVE_LAYOUT_REVISION` | 1 | **2** |
| warps quebrados | 0 | **0** |
| `valida_warp_tile --piso 60` | Hoenn 93,4 Kanto 79,4 Sinnoh 98,3 Johto 90,9 | **idênticos** |
| travas do `roda_qa.py` | Kanto 5, Johto 2, Hoenn 2, Sinnoh 6, comum 12 | **idênticas** |
| `lente_warps` / `lente_portas` | 0 achados / 334 | **0 achados / 334** |
| casos na suíte | 790 | **790** |
| suíte | 790 de 790 | **790 de 790** |
| T11 | 3 de 3 | **3 de 3, com o T11.3 INVERTIDO** |
| tempo da suíte | 1.135 s | 1.184 s (com a frente de arte rodando em paralelo) |

Os **70.172 B** de ROM são o líquido: os túmulos e os ids de treinador devolveram mais do que
isso, e os 88 canteiros de berry novos gastaram ~2 KB de volta. A promessa do PRD era 37,7 KB
dos túmulos mais 4,8 KB do `gTrainerIndex`, ou seja 42,5 KB; saiu **68,5 KB**.

Os **116 B a mais de EWRAM** também são líquido, e essa é a única coluna que piorou: o
`flags[]` encolheu 284 B (224 do teto de treinador, 60 da reserva de itens de Unova) e o
`berryTrees[]` cresceu 400 B. SaveBlock1 subiu de 94,3% para 95,0% do teto de 15.872 B.

### O que entrou, passo a passo

Nove commits, cada um buildável, cada um com a medida no corpo da mensagem.

1. **Os 812 túmulos saem do disco.** 729 de Unova e Galar, 70 dos cortes de Sinnoh que a
   resposta 48 do Gui deixou fora (Battle Zone, Pokétch, GTS, Union Room, Global Terminal,
   os 2F de Pokécenter) e 13 da torre de Sevii e da praça da Route 40. Com eles saíram 769
   entradas de layout, 28 pastas de geometria (as 27 próprias mais `data/layouts/TocoVago`,
   que ninguém mais usa) e 812 linhas de `.include` em `data/event_scripts.s`. Os 7 layouts
   que mapa VIVO compartilhava com túmulo ficaram.
2. **`group_order` vira bloco contíguo por região:** HOENN (grupos 0 a 29, 457 mapas), KANTO
   (30 a 69, 402), JOHTO (70 a 85, 239), SINNOH (86 a 100, 430) e COMUM (101 e 102, 66). De
   129 grupos para 103, com 152 vagas livres das 255. Os 3 mapas de Hoenn presos nos grupos
   que Galar tinha lotado foram para `gMapGroup_SpecialArea` (decisão 25 do Gui).
3. **Ids de treinador compactados:** 679 defines de Unova e Galar apagados, 2.196 nomes
   renumerados em 2.047 ids densos, 1.221 buracos fechados, `MAX_TRAINERS_COUNT` de 4.000
   para 2.200 com 153 vagas de folga.
4. **Apelidos devolvidos ao pool:** 422 (378 flags e 44 vars), mais os 9 `MAPSEC_RESERVADO_*`
   e a reserva de 467 flags que existia só para os itens de Unova.
5. **Os 88 canteiros de berry de Sinnoh plantados**, `BERRY_TREES_COUNT` de 128 para 178.
6. **Os 27 casos de teste que provam treinador pelo número** acompanham a renumeração.
7. **`SAVE_LAYOUT_REVISION` 1 para 2**, com o T11.3 invertido no MESMO commit.
8. **As 16 flags de vitória CRUAS dos casos de teste** acompanham a renumeração.

### Relatório de ANTES do `guarda_save.py`, com a revisão ainda em 1

**4.592 quebras**, e cada uma delas sozinha já mataria a save:

| tipo | quantas |
|---|---|
| MAPA MOVIDO | 1.330 |
| MAPA APAGADO | 812 |
| LAYOUT APAGADO | 769 |
| TREINADOR APAGADO | 617 |
| LAYOUT MOVIDO | 565 |
| APELIDO APAGADO | 251 |
| TREINADOR MOVIDO | 206 |
| LAYOUT INSERIDO NO MEIO | 23 |
| MAPA INSERIDO NO MEIO | 14 |
| MACRO DE TAMANHO MUDOU | 3 (`FLAGS_COUNT` 12856 → 10584, `MAX_TRAINERS_COUNT` 4000 → 2200, `SYSTEM_FLAGS` 5280 → 3480) |
| REVISÃO DE LAYOUT DA SAVE MUDOU | 1 |

### Os três achados desta onda, e nenhum deles estava previsto

**1. O letreiro de mapa buildava VERDE com a tabela velha.** A regra de
`src/data/map_popup_names.h` em `map_data_rules.mk` dependia só da LISTA de
`data/maps/*/map.json`. **Apagar mapa nunca dispara essa regra**: a lista só encolhe, nenhum
arquivo que fica é mais novo que o `.h`, e `map_groups.json` nem era dependência. A tabela é
indexada por `(grupo, número de mapa)`, então depois da reorganização ela apontava para os
grupos de ANTES, com o nome errado em centenas de mapas, sem uma linha de erro. Os quatro
primeiros passos desta onda buildaram assim. A dependência agora inclui `map_groups.json`, e
a tabela regerada caiu de 37.602 para 35.462 B. **Boa notícia é suspeita: build verde não
prova que o gerado é do commit.**

**2. A flag de vitória crua dos casos de teste era id de treinador disfarçado.** A varredura
de literais que o PRD manda fazer procura par `(grupo, mapa)` e não achou nada em código
compilado, o que estava certo. O que ela não procurava é `TRAINER_FLAGS_START + id`: o T12.3
acende `"flags": ["0xB80", "0xB7E"]` para marcar a Reli como já derrotada e deixar a Ali
aparecer na Ponte do Nugget. `0xB80` era `0x500 + 1664` (Reli) e virou outro treinador
qualquer, a Reli voltou a estar de pé e o caso reprovou dizendo **"esperado
TRAINER_LASS_ALI, obtido TRAINER_LASS_RELI"**. O sintoma é "o jogo mudou"; a causa é o número
velho no caso. Derrubou também o T94.5 e os T97.1 e T97.4. **Número cru de FLAG é índice de
save tanto quanto número cru de mapa**, e a varredura de literais tem de incluir a faixa
`0x500` a `0x500 + MAX_TRAINERS_COUNT`.

**3. O harness resolvia o nome da prova na ÁRVORE ERRADA.** `testa_critico.py` montava as
tabelas de mapa, layout, flag e treinador UMA vez, a partir de `--src`, e traduzia com elas
até a prova do caso marcado `"rom": "rom2"`, que roda na ROM NOVA. Enquanto as duas builds
tiveram os mesmos índices ninguém viu; esta é a primeira onda que os move, e o T11.3
reprovou dizendo **"esperado MAP_PALLET_TOWN_PLAYERS_HOUSE_2F (38.1), obtido grupo 31 mapa 1
(sem nome)"** — e 31.1 era exatamente o quarto de jogo novo na ordem NOVA. É o mesmo erro que
o cabeçalho de `offsets_da_fonte` já descrevia para os offsets do SaveBlock1 ("leitor com
offset chumbado não é testemunha, é adivinho"), um degrau acima. Agora cada caso resolve nome
na árvore da SUA ROM; sem `--rom2` o segundo conjunto é o mesmo objeto do primeiro, então a
suíte normal roda byte a byte como antes.

**4. O `guarda_save.py` era cego para um quarto do espaço de ids de treinador.** Ele lia só
`include/constants/opponents.h`, e os treinadores de KANTO moram em `opponents_frlg.h` com
números do MESMO espaço (1653, 1400, ...). Eram 623 ids sem guarda nenhum. Agora ele lê os
dois: 1.573 ids conferidos viraram 2.196.

### As decisões que mandaram nesta onda

- **Hoenn continua sendo o grupo 0.** `ShouldLegendaryMusicPlayAtLocation` (`src/overworld.c`)
  e `AbnormalWeatherHasExpired` (`src/field_specials.c`) comparam `mapGroup == 0` na mão.
  Nenhum compilador denunciaria a troca.
- **Johto continua CONTÍGUO**, de `gMapGroup_TownsAndRoutes_Johto` a
  `gMapGroup_SpecialArea_Johto`. `GetCurrentRegion` (`include/regions.h`) separa Johto de
  Sinnoh por intervalo de grupo, porque os 65 apelidos de MAPSEC de Johto são todos
  `MAPSEC_SINNOH_WEST` e nenhuma comparação de `sectionId` distingue as duas. Conferido por
  medida: a faixa é 70 a 85, tem 16 grupos e 239 mapas, nenhum grupo não-Johto dentro e
  nenhum grupo de Johto fora.
- **`REF_TREINADOR` do `guarda_save.py` avançou** de `e5224a3d67` para o passo 4 desta onda.
  A base mudou de propósito, e manter a referência velha deixaria o guarda reprovando 1.074
  achados para sempre. **Guarda que sempre reprova não é guarda**: vira barulho que o próximo
  leitor aprende a ignorar. Só se mexe nesse número em dia de quebra ACEITA.

O placar bloco a bloco está em `roms/c1-placar-save2.txt`, no mesmo formato do
`c1-placar-consolidada.txt` e com a coluna "antes" tirada da coluna "depois" dele. **Nenhum
caso saiu da suíte**: os 812 mapas apagados não eram citados por caso nenhum, e a contagem de
790 é a mesma dos dois lados.

### O que ficou de fora, e a razão medida de cada um

- **2 dos 90 canteiros de berry**, os dois de `Route214`: não há um único tile andável a 5
  tiles da coordenada convertida do Platinum. São déficit de verdade, não corte, e por isso o
  corte inteiro saiu de `CORTES_DO_GUI`. Objetos de Sinnoh vão de 101,6% (com os 90 fora do
  denominador) para 99,5% (com os 90 dentro e 88 plantados), que é a leitura honesta.
- **Os 63 VENT e BOLLARD continuam cortados**, e a razão está na própria 0.s: **eles nunca
  tiveram a ver com save**. Respiro de calçada e balizador são desenho com colisão, sem fala,
  sem item e sem gatilho; este motor não tem objeto decorativo sólido, e onde eles importam o
  desenho já está no tileset. Nenhuma janela de save muda isso.
- **As 39 `FLAG_HIDE_DEX_*` de Unova NÃO voltaram ao pool, e isso foi medido**: as 106
  `FLAG_HIDE_DEX_*` declaradas são as 106 usadas por mapa vivo depois da redistribuição da
  Dex da onda 2. Nenhuma sobrou para devolver. As três com "GALAR" no nome
  (`ARTICUNO`, `ZAPDOS`, `MOLTRES`) ficam porque a FORMA do pássaro é galariana e as três
  estão plantadas em mapa vivo, em Hoenn, Sinnoh e Johto.
- **A torre de treinadores de Sevii não tinha id para compactar**: os times dela vivem em
  `src/trainer_tower_sets.c`, com numeração própria. `MAP_TRAINER_TOWER_*` e
  `LAYOUT_TRAINER_TOWER_*` continuam definidos por `tools/mapjson/required_map_defines.json`
  (grupo fantasma 118 e layout `0xFFFF`), e é por isso que `src/trainer_tower.c` e
  `src/field_specials.c` seguem compilando com os mapas apagados.
- **Os pares "grupo 75, mapa 13" da 0.u ficam como estão.** Eles vivem na prosa deste
  arquivo e num comentário de `conserta_colisao_sinnoh.py`: são história, e história não se
  recalcula. Os números da ordem NOVA estão na tabela acima.

### O que fica aberto

- **`guarda_colisao_vars.py` continua REPROVANDO uma colisão**, e ela é ANTERIOR a esta onda
  (conferida no master `a0e54260a2`, idêntica): `VAR_TREM_MAGNETICO` e
  `VAR_MAP_SCENE_FIVE_ISLAND_LOST_CAVE_ROOM10` dividem o endereço `0x4083`, e os dois são
  usados. Não é assunto de save (as duas já cabem em `VARS_COUNT`), então pode ser consertada
  a qualquer momento movendo `VAR_TREM_MAGNETICO` para outra vaga do pool. Entra na fila de
  bugs.
- **Os 36 objetos `OBJ_EVENT_GFX_BERRY_TREE` de Johto com `trainer_sight_or_berry_tree_id`
  em `"0"` e `script` em `"0"`** continuam inertes: todos apontam para a vaga 0 de
  `berryTrees[]` e nenhum tem script (16 deles no `WorldHub`, o resto espalhado por 18
  rotas de Johto). Foi visto ao medir os canteiros de Sinnoh e não foi tocado, porque dar
  id a eles cabe dentro de `BERRY_TREES_COUNT` = 178 e **não** precisa de quebra de save.
  Fila de bugs.

---

## 0.y A CONSOLIDAÇÃO DO CARTUCHO 1: A SUÍTE INTEIRA FECHA VERDE E SAI A ÚLTIMA ROM COMPATÍVEL COM A SAVE ANTIGA, 08/09/2026 (condutor Opus, sem executores)

**Resposta em uma linha:** a suíte fechou **790 de 790** (789 no laço bloco a bloco mais o
T11.3, que só roda com as duas ROMs), o portão `antes_de_empurrar.sh` fechou verde nos dez
passos e a ROM `roms/pokemon-claude-2026-09-08-c1-consolidada.gba`
(md5 `bc5f411d54ba26ade79fd7653a1f082f`) é build LIMPO do HEAD `849e8565ee`, com
**SAVE COMPATIVEL**. **Esta é a última ROM que abre a save antiga do Gui antes da quebra de
save.** Esta seção é o commit seguinte e não toca a ROM.

### Placar, medido bloco a bloco

O placar completo, prefixo por prefixo, está em `roms/c1-placar-consolidada.txt`, no mesmo
formato do `c1-placar-bloco-a-bloco.txt` da onda 1 e com a coluna "antes" tirada da coluna
"depois" daquele arquivo.

| medida | antes (onda 1, `517322bedd`) | depois (`849e8565ee`) |
|---|---|---|
| casos na suíte | 747 | **790** (104 prefixos) |
| suíte | 747 de 749 | **789 de 790 no laço, 790 de 790 com o T11.3** |
| vermelhos | T176.3 | **NENHUM** |
| T11 (save da ROM anterior na nova) | 3 de 3 | **3 de 3** |
| `guarda_save.py` | SAVE COMPATIVEL | **SAVE COMPATIVEL** |
| `antes_de_empurrar.sh` | verde | **verde nos 10 passos** |
| ROM usada | 29.585.128 B (88,17%) | **31.616.680 B (94,23%)** |
| ROM livre | 3.969.304 B | **1.937.752 B** |
| EWRAM | 225.856 B (86,16%) | 225.856 B (86,16%) |
| IWRAM | 28.392 B (86,65%) | **29.036 B (88,61%)** |
| `valida_rom.py` | 2.404 mapas, 2.054 layouts | **2.406 mapas, 2.055 layouts** |
| Dex obtenível | 1.315 de 1.571 | 1.571 de 1.571 (onda 2, já no master) |

Os 2,03 MB a mais de ROM e os 644 B a mais de IWRAM não são desta encomenda: são o preço
das ondas 2 a 5 e da música original de Johto e Sinnoh, que já estavam no master e nunca
tinham sido medidas juntas. **O teto ficou em 1,94 MB livre**, e é bom lembrar disso antes
da próxima onda de conteúdo.

Os 43 casos a mais que a onda 1 são os blocos novos T185 (2), T186 (22) e T187 (11), mais o
T129 regerado para a Dex de 1.571 (de 3 casos para 11).

**O laço rodou por PREFIXO tirado de `testa_critico.py --lista`, e não por arquivo.** Isso é
obrigatório: `10_kanto.json`, `20_johto.json` e `30_hoenn_sinnoh.json` misturam prefixos, e
laço por arquivo conta errado. No fim a contagem foi conferida caso a caso contra o
`--lista`: 104 prefixos e 790 casos dos dois lados, zero divergência. A suíte inteira leva
**1.135 s (18,9 min)** nesta máquina, e não as ~2 h que a nota antiga dizia; a diferença é
que ela encolheu de 1.088 para 790 casos quando Unova e Galar saíram.

### O que estava vermelho, e o que cada um era

**T134.25 e T134.26 (Glastrier de Snowpoint): caso desatualizado, jogo intacto.** O refino
"Snowpoint sem calçada" (`ace0ac7877`) é POSTERIOR à geração do par (`4f6ba5701f`) e fechou
o tile (27, 46), que era o único degrau andável da fileira 46 entre o pouso do Pokécenter e
o bicho. A rota antiga (LEFT saturante a partir de (29, 46)) passou a travar em (28, 46),
quatro tiles antes, e o par negativo denunciou primeiro, como sempre.

Antes de mexer no caso, a pergunta certa foi respondida com medida: **o Pokémon ilha alguma
coisa?** Com o Glastrier tratado como parede, a busca em largura sobre o `map.bin` alcança
**656 dos 657 tiles alcançáveis** do mapa, ou seja o único tile que ele tira é o dele
próprio. O mapa está são; quem envelheceu foi a rota.

A rota nova saiu da MESMA máquina que gerou as originais (`escorrega` do
`lendarios_sinnoh`, com os irmãos de mapa como parede), com uma correção que o gerador
não tem e que vale como armadilha para quem for regerar caso de estático:

> **`rota_entre_vizinhos` planeja a navegação com o próprio alvo ANDÁVEL.** Ele ignora todo
> objeto de origem `distribui_dex`, inclusive o que ele está mirando, então a rota que ele
> propõe pode ATRAVESSAR o tile do Pokémon: em Snowpoint ele mandou subir a coluna 25
> passando por cima do Glastrier, e isso é impossível no jogo. A correção é tratar o alvo
> como parede em toda perna de navegação e deixar só a perna de aproximação atravessá-lo, e
> depois VALIDAR o candidato andando a rota duas vezes na grade, uma com o bicho e outra sem,
> conferindo que a primeira para em `para` e a segunda escorrega até `vazio`.

A linha do Glastrier em `dev_scripts/dex_distribuicao.json` foi atualizada junto com o caso,
para uma regeração futura não ressuscitar a rota velha.

### A causa raiz dos "instáveis": o relógio do Mac entrava no jogo

Este é o achado da noite, e ele explica a família inteira de casos que o projeto vinha
chamando de instáveis desde a rodada 13.

**Sem o campo `hora`, o `gba_runner` não instala fonte de RTC nenhuma** (`g_rtc_hora = -1`,
`dev_scripts/gba_runner.c`) **e o cartucho lê o relógio do Mac, com hora, MINUTO e SEGUNDO.**
Duas rodadas do mesmo caso, na mesma ROM e com o mesmo roteiro, nascem de estados diferentes,
e batalha é onde isso aparece. Com `hora` declarada, o runner instala um `mRTCSource` com
minuto e segundo em ZERO, e a execução vira reproduzível.

A prova não é raciocínio, é medida: o **T187.11 alternava verde e vermelho de rodada para
rodada sem uma linha de código mudar**, e passou a 4 de 4 verdes assim que a hora foi
declarada, com os mesmos dez apertos de A que o caso já dizia. O **T170.8 fazia o mesmo e
virou vermelho DETERMINÍSTICO** com a hora pregada, e foi isso que permitiu consertá-lo de
verdade: o PNG final mostrou a batalha do Silver ainda correndo, no menu de ação do Raichu,
com o tapete de A esgotado. Não era o jogo, era orçamento de apertos. O tapete dobrou de 400
para 900 e a folga foi medida em três horas do cartucho (3h, 12h e 21h), as três verdes.

**Emulador determinístico não quer dizer teste determinístico: o relógio da máquina é
entrada.** Todo caso que joga batalha, ou que depende de NPC que anda, deve declarar `hora`.
Os quatro instáveis nomeados do projeto (T170.8, T176.3, T183.1, T183.2, T187.11) passaram a
declarar `hora: 12`, e depois disso os cinco blocos rodaram **três vezes seguidas, todos
verdes nas três**.

O harness NÃO tem campo `"instavel"`, e nenhum foi inventado: nenhum caso precisou dele.

### Lições

1. **O relógio do Mac é entrada do teste.** Caso sem `hora` é caso com semente aleatória. É
   isso, e só isso, que estava por trás dos "instáveis" da rodada 13 e da sessão do cartucho 2.
2. **Instável é bug de teste até prova em contrário, e pregar o relógio é o jeito de achar a
   prova.** O T170.8 só pôde ser consertado depois de virar vermelho SEMPRE. Teste que
   oscila esconde defeito; teste que falha sempre entrega o defeito.
3. **Vermelho de rota em mapa refinado é quase sempre caso velho, mas a pergunta que separa
   "caso velho" de "jogo quebrado" é o teste de ilhamento**, e ele custa dez linhas de
   Python. Nunca reescrever roteiro sem responder isso antes.
4. **Gerador de rota de estático não trata o alvo como parede.** Quem regerar caso de
   estático tem de validar o candidato andando a rota na grade, com e sem o bicho, senão
   aceita rota que atravessa o próprio Pokémon.
5. **Laço bloco a bloco anda por PREFIXO, não por arquivo**, e a contagem final se confere
   caso a caso contra `--lista`. Três arquivos da suíte misturam prefixos.
6. O build é reprodutível: `make clean && make -j8` no `849e8565ee` devolveu o md5
   `bc5f411d54ba26ade79fd7653a1f082f`, o mesmo da árvore incremental. Leva 2 min 22 s.

### O que fica aberto

- **A quebra de save é a próxima onda**, e esta ROM é a fronteira: `SAVE_LAYOUT_REVISION`
  continua 1, e a save do Gui abre aqui. Depois dela, não abre mais. O T11.3 tem de ser
  invertido no MESMO commit que subir a revisão para 2, e a instrução está escrita dentro do
  próprio caso, em `dev_scripts/testes_criticos/40_save.json`.
- **A ROM está em 94,23%, com 1,94 MB livre.** Os 37,7 KB dos túmulos de Unova e Galar
  voltam com a quebra de save.
- A fila de bugs e os refinos das ondas 2 e 3 continuam como a 0.x deixou; nada deles foi
  tocado aqui.
- As branches `c1-fix-a`, `c1-fix-b` e `c1-fix-c` continuam por conferir e apagar, e os
  worktrees soltos de `/private/tmp/claude-501/` (`arte-baseb`, `c1-fixE`, `zring-wt`)
  continuam para apagar. O `t11-povoamento` criado aqui pode sumir junto; `t11-r13` e
  `c2-t11-antiga` ficam.

---

## 0.x PAUSA DE 08/09/2026, ~02:00: O ESTADO EXATO PARA A RETOMADA DE QUARTA, 10/09 (condutor Fable; anotado a pedido do Gui)

**Resposta em uma linha:** o master `d2fc6e9ea9` (push em dia) tem o cartucho 1 quase inteiro, mas
NÃO tem suíte completa verde nem ROM consolidada; a retomada começa por isso.

**O que está no master (tudo com push):** Unova e Galar como túmulos (0.w, onda 1; tag
`pre-remocao-unova-galar` marca o último master com elas); Dex 1.571 de 1.571 nas quatro regiões
(`c1-onda2`); cortes de Sinnoh de volta e trem magnético (`c1-onda3`); Trainer Tower e praças de
Johto como túmulo, Battle Tower de Olivine, fala final da Cynthia (`c1-onda4`); música original de
Johto e Sinnoh, partes A, B e C (`c1-onda5`, `c1-musica-b`, `c1-musica-c`: 157 faixas, dia e noite
em Sinnoh, batalha por região); Snowpoint refinado sem calçada (`refino-neve3`, decisão 56 do Gui;
a versão com calçada, `922b2771c9`, foi revertida em `f729f209b8`); povoamento (210 NPCs); time de
teste de cinco com Mega, Z, Gigantamax e Tera; os quatro aparelhos no jogo novo.

**O que NÃO está feito:**
1. Suíte completa no master. O condutor do cartucho 1 parou no meio dos consertos de teste:
   T134 tem 12 pares negativos de estático de Mt. Coronet reprovando desde antes da onda
   (A/B feito pelo executor de Snowpoint), T187.11 aberto, T129 (Dex) regerado e nunca rodado.
   As branches `c1-fix-a`, `c1-fix-b`, `c1-fix-c` parecem já estar no master como
   `dd194d148d`, `ecd200be8e`, `4f6ba5701f`: conferir por diff e apagar.
2. ROM consolidada. A última ROM jogável é `roms/pokemon-claude-2026-09-07-povoamento.gba`
   (com Unova dentro e sem música nova). A próxima, `pokemon-claude-2026-09-10-c1-consolidada`,
   é a ÚLTIMA compatível com o save antigo e só sai com suíte verde, T11 3/3 e
   `antes_de_empurrar.sh`.
3. Canalave refinada está na branch `refino-porto3` (`6427cbbf6a`): veleiro, farol e cais do
   Golden Glazed, sem guindaste (não há chão para os pés), carimbo 26,9% para 24,4%. Absorver.
4. Quebra única de save (pastas por região, `rm` dos túmulos, ids de treinador compactados,
   berries, MAPSEC/flags/vars liberadas, heal locations, `SAVE_LAYOUT_REVISION` 2, T11.3
   invertido): autorizada pelo Gui, ainda não começada.
5. Fila de bugs: Safari de Johto, maré baixa do Lago da Fúria, E3 restantes, 31 corpos
   repetidos, níveis de encontro acima de 100, seletor de mecânica de batalha (resposta 54:
   sim), Frontier de Hoenn com a Fase F, `treinadores_faltantes_b4.py`.
6. Refino ondas 2 (Sinnoh por tileset) e 3 (Johto pelo GS Chronicles e Scorched Silver).

**Worktrees em `/private/tmp/claude-501/` com resto solto, todos descartáveis:** `arte-baseb`
(`testa_critico.py` com o `.sav` local), `c1-fixE` (T134 pela metade, executor morto aos 11
minutos), `zring-wt` (`new_game.c` já commitado). Apagar na retomada; manter `t11-r13` e
`c2-t11-antiga`.

**Lições da noite:** condutor dado como encerrado pode acordar sozinho e commitar (aconteceu
com a calçada de Snowpoint); esperas de agente aparecem para o Gui como "tarefas de wait" e ele
as mata; nomeá-las `ESPERA-C1-*` e `ESPERA-REFINO-*` e usar o mínimo.

## 0.w CARTUCHO 1, ONDA 1: UNOVA E GALAR SAEM DO JOGO, E A ROM DEVOLVE 2,80 MB, 07/09/2026 (PRD-CARTUCHO-1.md; condutor Opus, dois executores Opus)

### Placar, medido nos dois lados

| medida | antes (`41f54c50ef`) | depois (`0003e88fbc`) |
|---|---|---|
| ROM usada | 32.384.728 B (96,51%) | **29.585.128 B (88,17%)** |
| ROM livre | 1.169.704 B | **3.969.304 B** |
| EWRAM | 225.856 B (86,16%) | 225.856 B (86,16%) |
| IWRAM | 28.400 B (86,67%) | 28.392 B (86,65%) |
| arquivos versionados | 39.805 | **36.082** (menos 3.723) |
| `guarda_save.py` | SAVE COMPATIVEL | **SAVE COMPATIVEL** |
| `valida_rom.py` | 2.404 mapas, 2.054 layouts | 2.404 mapas, 2.054 layouts |
| warps quebrados | 0 | **0** |
| `valida_warp_tile --piso 60` | Hoenn 93,4 Kanto 79,4 Sinnoh 98,1 Johto 91,0 | idênticos, e sem a linha de Unova |
| travas do `roda_qa.py` | Kanto 5, Johto 2, Hoenn 2, Sinnoh 8, comum 13, Unova 25, Galar 268 | **Kanto 5, Johto 2, Hoenn 2, Sinnoh 8, comum 13** |
| casos na suíte | 1.088 | 749 (747 herdados mais os dois novos do T185) |
| suíte | 1.085 de 1.088 | **747 de 749** |
| T11 (save da ROM anterior na nova) | não se aplica (é o par das duas ROMs) | **3 de 3** |
| Dex obtenível | 1.571 de 1.571 | **1.315 de 1.571** |

A ROM devolveu **2.799.600 B (2,80 MB, 2,67 MiB)**, contra os 2.405.300 B que o
`PRD-GENS-6-9.md` tinha projetado. A diferença para mais é o texto e o script dos
729 mapas, que a projeção contou símbolo a símbolo e aqui saiu inteiro.

**As duas suítes foram rodadas na mesma máquina e comparadas CASO A CASO, não por
placar**, e o placar bloco a bloco está gravado em
`roms/c1-placar-bloco-a-bloco.txt`: 341 casos sumiram (os de Unova e de Galar),
**ZERO regressão**, ou seja nenhum caso que passava antes reprova agora. Depois
dessa comparação entraram os dois casos novos do bloco T185, o par adversarial do
menu do barco, rodados à parte: 2 de 2. O único vermelho
de hoje é o **T176.3, o instável já nomeado na seção 0.u**. O antes tinha um
segundo vermelho, o T183.5, e ele era um dos casos que rodavam em mapa de Galar,
então saiu com a região.

**T11 3 de 3, e ele é a prova mais forte desta onda.** Rodado com a ROM ANTERIOR
(`41f54c50ef`, md5 `3a1703f00940222e2ded028d19a60796`) de um lado e a ROM nova do
outro: a save gravada na antiga **abre na nova em `MAP_SANDGEM_TOWN`, com o layout
de Sandgem e a flag `0x2BA` acesa**. O caso T11.3 estava INVERTIDO desde 18/08/2026
(ele exigia que a save fosse RECUSADA, que era o esperado da janela ABERTA), e o
texto dele já dizia quando voltar ao normal: "na próxima onda de janela FECHADA,
quando a ROM oficial nova virar baseline". É agora. **A onda de quebra de save tem
de inverter o T11.3 de novo, no MESMO commit que subir `SAVE_LAYOUT_REVISION` para
2**, e isso está escrito dentro do próprio caso.

### A decisão que manda nesta onda: TÚMULO, e não `rm`

**Os 729 mapas de Unova e Galar não foram apagados. Eles viraram TÚMULO**, no
molde que o projeto já usa para os 111 cortes de Sinnoh
(`dev_scripts/remove_mapas_cortados.py`, commit `721c77fb63`): o `map.json`
continua existindo com o id intacto, mas sem evento nenhum, com
`region_map_section` em `MAPSEC_NONE` e com um campo `cortado_por` que diz de onde
veio o corte; o `scripts.inc` fica só com o rótulo `<Mapa>_MapScripts:: .byte 0`,
que o `header.inc` gerado exige.

**Por quê, medido e não lembrado.** A regra dura desta onda é `guarda_save.py`
dizendo SAVE COMPATIVEL, e a save guarda ÍNDICE, não nome. Apagar as 729 entradas
mata dois índices de uma vez:

1. `SaveBlock1.location.mapGroup` / `mapNum` (0x04). O guarda acusou as 729
   quebras, uma por mapa, na primeira tentativa desta onda.
2. `SaveBlock1.mapLayoutId` (0x32), que é a POSIÇÃO do layout dentro de
   `layouts.json` contando só quem tem `border_filepath` no disco
   (`tools/mapjson/mapjson.cpp:895`). **Os 729 layouts de Unova e Galar são os
   numerados 1171 a 2026**, com 127 layouts das quatro regiões INTERCALADOS e mais
   28 de Sinnoh DEPOIS deles. Apagar a entrada deslocaria o número de 155 layouts
   vivos, e `LoadSaveblockMapHeader` (`src/overworld.c:682`) carrega a geometria
   por esse número: a save do Gui abriria no mapa certo com o desenho de outro.
   **Este é o mesmo ponto cego que o `remove_mapas_cortados.py` já tinha
   documentado**, e a resposta dele vale igual aqui.

O que SAI do túmulo é o peso: a geometria (`border.bin` e `map.bin`, que é onde
moram os 1,43 MB de blockdata), todos os eventos, as conexões, o script e o texto.
A entrada do layout continua numerada, encolhida para 1x1 e apontando para
`data/layouts/TocoVago` (8 B de borda e 2 B de bloco, compartilhados pelos 729).

**O que isso ainda custa: 38.621 B (37,7 KB)** somados no `pokeemerald.map` sobre
os 2.214 símbolos com nome de Unova ou de Galar que sobraram (cabeçalho de mapa,
struct de eventos vazia, tabela de layout). **É exatamente esse o valor que a onda
de quebra de save recupera**, quando as 729 pastas e os 23 grupos vazios puderem
sumir de verdade.

Pela mesma razão ficaram como BURACO, sem andar índice nenhum:

- **os 23 grupos de mapa** que ficaram vazios (22 de Unova e `gMapGroup_Galar`)
  continuam em `group_order`. O `mapjson` já sabe: escreve `.4byte NULL` em
  `gMapGroups` e não emite o símbolo do grupo, e o contador `group_num` anda por
  grupo DECLARADO, então os grupos 123 a 128 (Sinnoh e Johto) mantêm o número.
  Medido: os três mapas presos nos grupos que Galar ocupou
  (`Route116_TunnelersRestHouse`, `Route117_PokemonDayCare`,
  `Route121_SafariZoneEntrance`) estão todos na POSIÇÃO 0, então nenhum `mapNum`
  se moveu.
- **os 679 ids de treinador** (411 de Unova, 268 de Galar) continuam definidos em
  `opponents.h`. O que saiu foi o TIME, em `trainers.party`. A flag de vitória é
  `TRAINER_FLAGS_START + id`, então apagar o `#define` seria quebra de save; e
  `testa_critico.py --treinadores` só reprova apelido USADO por script, então 679
  ids sem time são inertes.
- **as 382 flags e as 44 vars** com nome das duas regiões continuam como estão.
  Elas já eram apelido de `FLAG_UNUSED_*` / `VAR_UNUSED_*`, custam ZERO byte de
  ROM, e apagar o apelido faz o `guarda_save.py` acusar uma quebra por nome (a
  save guarda o BIT, e o slot passaria a ter outro dono). As 39 `FLAG_HIDE_DEX_*`
  de lendário plantado em mapa de Unova também ficam, porque a onda da Dex vai
  precisar delas para replantar o bicho em outra região.
- **os 9 slots de MAPSEC** viraram `MAPSEC_RESERVADO_01` a `09` em vez de sumir.
  `regionMapSectionId` é gravado na save como local de captura do Pokémon;
  apagá-los empurraria `MAPSEC_SS_AQUA` em três e `MAPSEC_NONE` em nove. Os 112
  apelidos (`MAPSEC_UNOVA_*`, `MAPSEC_GALAR_*`) saíram do template.

### O que saiu de verdade, item por item

| item | Unova | Galar | total |
|---|---|---|---|
| mapas viraram túmulo | 291 | 438 | 729 |
| layouts encolhidos para 1x1 | 291 | 438 | 729 |
| pastas de geometria apagadas | 291 | 438 | 729 |
| pastas de tileset apagadas | 58 | 47 (45 secundários e os primários `galar_00` e `galar_11`) | 105 |
| entradas em `trainers.party` | 411 | 268 | 679 |
| chefes de Fase F | 36 | 38 | 74 (de 236 para 162) |
| heal locations | 18 | 12 | 30 (de 93 para 63) |
| tabelas de mato | 87 | 0 | 87 |
| trocas in-game | 9 | 0 | 9 (eram as últimas do enum) |
| linhas de script dedicado | 0 | 17.625 em 6 arquivos | 17.625 |
| apelidos de MAPSEC | 70 | 42 | 112 |
| casos de teste | 114 | 227 | 341 (de 1.088 para 747) |

Mais: o motor de animação de tileset de Unova e o gerado `anims_unova.h`; os 30
protótipos de `InitTilesetAnim_Unova*`; os seis `def_special` de Quest Log e Help
System do FireRed, que existiam só para o tradutor de Galar não recusar cena; as
duas entradas de `sRegioes` no seletor de capítulo e o array `sGinasiosUnova`; e
as duas faixas de `GetRegionForSectionId` em `include/regions.h`.

### O menu do barco, e por que nenhum `case` foi renumerado

Os destinos 3 (VIRBANK, Unova) e 6 (WEDGEHURST, Galar) saíram de
`data/scripts/travessia_regioes.inc` e dos quatro portos que ficam. **Os ids 3 e 6
ficaram VAGOS de propósito**: quem manda é o id que o `dynmultipush` empilha, não a
posição na lista, então `case 0`, `1`, `2`, `4` e `5` continuam valendo sem um
caractere de diferença. O tamanho máximo do `dynmultistack` caiu de 7 para 5.

**O que MUDOU foi a contagem de DOWN**, porque o menu encolheu: CANALAVE deixou de
ser o quarto item visível e passou a ser o terceiro. Três casos foram corrigidos
(T8.3, T86.2, T86.4) e quatro foram apagados porque a rota deles ATRAVESSAVA o
Porto de Virbank (T10.2, T86.10, T86.11, T86.12).

### O que NÃO foi tocado, e é decisão medida

- **`include/constants/regions.h` continua com `REGION_UNOVA` e `REGION_GALAR`.**
  Aquele enum não é a lista de regiões do hack, é a do universo Pokémon, e
  `REGION_GALAR` é infraestrutura de FORMA REGIONAL: `src/pokemon.c:6772`
  (`isGalarianForm`), a evolução de Koffing e de Mime Jr. em
  `gen_1_families.h`, `test/daycare.c:107` e o rótulo da Dex em
  `pokedex_plus_hgss.c`. Tirar de lá quebraria Pokémon, não região.
- **`charmap.txt` continua com `Ã Õ ã õ` em F1, F2, F4 e F5.** A mudança nasceu por
  causa da fonte de Galar, mas os glifos de `graphics/fonts/latin_*.png` já foram
  redesenhados e essas são letras do português. Reverter seria trabalho sem ganho.
- **Nenhuma faixa de música saiu.** Medido varrendo os 2.404 `map.json` do commit
  anterior: só **5 faixas** eram usadas exclusivamente por mapa de Unova ou Galar
  (`MUS_CABLE_CAR`, `MUS_DESERT`, `MUS_RG_CYCLING`, `MUS_RG_FOLLOW_ME`,
  `MUS_RG_VS_GYM_LEADER`), e as cinco são faixas de base do pokeemerald e do
  FireRed, com uso fora de mapa (`MUS_RG_VS_GYM_LEADER` é `GetBattleBGM`). O
  orçamento da onda de música é inteiro novo, como o PRD já dizia.
- **`WorldHub` e `WorldHub2` ficam inteiros.** Medido: um warp cada, os dois para
  `MAP_NEW_BARK_TOWN`, `region_map_section` `MAPSEC_NEW_BARK_TOWN`. São mapas de
  Johto e não apontavam para lugar nenhum das duas regiões.
- **A fala final da Cynthia continua a mesma.** Ela não cita Unova; o que ela diz é
  "Carry that with you wherever you go next", e a reescrita é a decisão 26, de uma
  onda posterior. O que esta onda precisava provar é que nada depois do Hall da
  Fama aponta para as duas regiões, e não aponta: o barco perdeu os dois destinos e
  `FLAG_SYS_GAME_CLEAR` continua abrindo o Battle Frontier de Hoenn.

### A Dex caiu, e isso é a próxima onda

`censo_dex.py` mediu **1.315 de 1.571 obteníveis**, contra os 1.314 projetados. As
**256 espécies e formas que perderam toda fonte** estão concentradas na geração 5
(**171 delas**), e são o insumo da onda de redistribuição: 39 delas nem têm sprite
de overworld, então não podem virar encontro estático sem obra de arte.

### Armadilhas achadas nesta onda, para quem vier depois

1. **`mapLayoutId` é índice de save e quase ninguém lembra dele.** Foi o achado
   caro desta onda: a primeira tentativa apagou as entradas de layout e o
   `guarda_save.py` só reclamou dos mapas, porque o lado velho do número de layout
   vem de um commit de referência e o deslocamento aparecia lá. Quem apagar layout
   sem encolher a entrada quebra a save de quem está parado em OUTRA região.
2. **Filtrar túmulo por nome de pasta não basta.** Toda ferramenta de medição
   precisa ignorar mapa com `cortado_por`, senão os 729 caem no balde padrão de
   Hoenn e envenenam a coluna de arte, que mede TODOS os mapas nossos e não só os
   casados com a fonte.
3. **Backtick em mensagem de commit é substituição de comando.** O `git commit -m`
   com a mensagem inline comeu oito nomes de arquivo e o commit saiu com buracos.
   Mensagem longa vai em arquivo, com `-F`.
4. **`treinadores_faltantes_b4.py --demo` já estava VERMELHO antes desta onda**, no
   assert de excesso de Unova. Depois da limpeza ele para no assert seguinte, que é
   outra defasagem antiga (`RIVAL_CHIKORITA_4` deixou de ser exceção de Johto e o
   assert manda revisitar a seção 9 do PRD). Nenhum portão roda esse arquivo; fica
   registrado para não ser confundido com regressão desta onda.

### O que fica aberto

- A onda de quebra de save (`SAVE_LAYOUT_REVISION` 1 para 2) é quem apaga as 729
  pastas de verdade, compacta os 23 grupos vazios e os 679 ids de treinador, e
  recupera os 37,7 KB dos túmulos. **Ela não é desta encomenda.**
- **O T11.3 tem de ser invertido de novo pela onda de quebra de save**, no mesmo
  commit que subir `SAVE_LAYOUT_REVISION` para 2. Ele hoje exige que a save da ROM
  anterior CARREGUE; naquele dia o esperado volta a ser
  `MAP_PALLET_TOWN_PLAYERS_HOUSE_2F` com a `0x2BA` apagada. A instrução está
  escrita dentro do próprio caso, em `dev_scripts/testes_criticos/40_save.json`.
- **`dev_scripts/antes_de_empurrar.sh` fechou VERDE nos nove passos** no HEAD
  `0003e88fbc`, buildando o commit numa worktree isolada, e a ROM daquele build
  tem o mesmo md5 da entrega. Pode empurrar.
- Os geradores de Unova e de Galar continuam em `dev_scripts/`
  (`importa_unova.py`, `tileset_galar.py`, `mundo_galar.py`, `galar_*.json` e
  irmãos). Eles não custam ROM, mas rodá-los ressuscitaria as regiões: quem mexer
  em tileset ou em mapa NÃO deve chamá-los. Apagá-los é decisão do Gui.

---

## 0.v O SELETOR DE CAPÍTULO DEIXA DE ENTREGAR UM PIKACHU E PASSA A ENTREGAR UM TIME DE CINCO, 07/09/2026 (pedido direto do Gui; executor Opus)

### Time de teste do seletor

Quem salta de capítulo com a party VAZIA deixou de ganhar um Pikachu nível 20 sozinho e passou a ganhar
**cinco Pokémon nível 50, um por mecânica moderna**, e o mesmo salto põe na mochila os quatro aparelhos
(Mega Ring, Z-Power Ring, Dynamax Band, Tera Orb) e acende `FLAG_B8_DYNAMAX_LIBERADO` e
`FLAG_B8_TERA_ORB_CARREGADO`. **O achado que não estava na fila e vale mais que o pedido:** `src/new_game.c`
só dava a Dynamax Band e o Mega Ring, então **o Z-Power Ring e a Tera Orb nunca existiram em save nenhuma
desta ROM**, e por isso `CanUseZMove` (`src/battle_z_move.c:121`) e `CanTerastallize`
(`src/battle_terastal.c:77`) recusavam SEMPRE, para qualquer jogador, em qualquer batalha: duas mecânicas
inteiras estavam mortas e nenhum teste pegava, porque nenhum teste abria o menu de golpes. O nível subiu de
20 para 50 porque 20 não sobrevive a chefe de capítulo tardio, que é justamente onde o seletor mais serve, e
o modo de teste LV.5 TRAINERS não rebaixa isto: ele mexe SÓ na party do TREINADOR (`src/battle_main.c:2003`).
Custo de save ZERO em tudo: itens numa mochila que já existe, flags que já existem e um time que nasce na
hora e nunca foi gravado em disco.

| slot | Pokémon (nível 50) | segura | golpes | mecânica | prova lida da EWRAM |
|---|---|---|---|---|---|
| 0 | Raichu | Raichunite Y (859) | Thunderbolt, Surf, Rock Smash, Strength | Mega Raichu Y | `especie0` = 1554 |
| 1 | Charizard, fator Gigantamax | nada | Flamethrower, Fly, Sunny Day | Gigantamax | `especie1` = 1491 e `gCurrentMove` = 903 (G-Max Wildfire) |
| 2 | Mew | Mewnium Z (378) | Psychic, Cut, Flash | Z-move | `gCurrentMove` = 871 (Genesis Supernova) |
| 3 | Incineroar, tera Dark | nada | Darkest Lariat, Flare Blitz, Bulk Up | Terastal | `FLAG_B8_TERA_ORB_CARREGADO` de 1 para 0 |
| 4 | Lucario | Lucarionite Z (864) | Aura Sphere, Close Combat | Mega Lucario Z | `especie4` = 1559 |

O Raichu é o slot 0 de propósito e carrega a suíte de HM inteira: `ScrCmd_checkfieldmove`
(`src/scrcmd.c:2307`) varre a party do índice 0 para cima e PARA no primeiro que conhece o golpe, então toda
rota de teste de Surf, Rock Smash e Strength continua valendo letra por letra.

**O que o motor impõe e o time não conserta.** `AssignUsableGimmicks` (`src/battle_gimmick.c:20`) dá UMA
mecânica por lutador, a PRIMEIRA da fila MEGA, ULTRA BURST, Z-MOVE, DYNAMAX, TERA, então Pokémon do jogador
de mãos vazias SEMPRE cai no Dynamax, e **o Terastal do jogador só fica alcançável depois de o Dynamax ter
sido gasto na mesma batalha**. Segurar Mega Stone ou Z-Crystal derruba o Dynamax, mas derruba o Terastal
junto pela MESMA linha (`src/battle_terastal.c:102`), e isso foi TENTADO com uma Darkranite inerte na mão do
Incineroar: ele ficou sem mecânica nenhuma. Não há item que resolva; é ordem de enum, e mexer nela é rodada
própria. Mega também é uma vez por batalha por treinador, então o Mega Raichu Y e o Mega Lucario Z não cabem
na mesma luta.

**Portões.** Build verde (`make -j8`, RC 0) na worktree isolada `/private/tmp/claude-501/time-teste`, HEAD
`7053780f27` mais só estes arquivos: **EWRAM 86,16%, IWRAM 86,68%, ROM 96,45% (32.364.776 B), idênticos aos
do HEAD limpo**. `guarda_save.py` **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%).
**T183 6 de 6** (bloco novo, `dev_scripts/testes_criticos/183_time_do_seletor.json`), **T11 3 de 3** contra
`roms/pokemon-claude-2026-08-18.gba` com a fonte na worktree de `cf6786b2ae`, e **25 blocos verdes**, entre
eles os treze que dependem de HM de campo ou liam o Pikachu (T90, T97, T98, T100, T101, T107, T112, T121,
T124, T129, T136, T137, T148, T152, T157, T166, T169, T170) mais a amostra T2, T4, T20, T40, T82, T92, T95,
T99, T116, T128, T143, T144, T153, T159, T176.

**Dois casos foram RECALIBRADOS, e o time não.** T101.13 cobrava `time` 1 e passou a cobrar 5. T170.8
travava em "Raichu is already in battle!", e o diagnóstico saiu do PNG final: com time de mais de um Pokémon
o estilo de batalha SHIFT (o padrão) pergunta "quer trocar de POKEMON?" toda vez que o adversário manda um
bicho novo, e o tapete de A do caso respondia SIM e caía na lista do time. O conserto é o `antes_do_warp`
passar pelo menu de OPTION e pôr BATTLE STYLE em SET antes do warp. Vale de aviso para o playtest: quem
jogava com um Pokémon só nunca via essa pergunta, e agora ela aparece em toda batalha de treinador.

**E o JOGO NOVO passa a dar os quatro aparelhos, não dois.** O achado acima era só do lado do SALTO: `src/new_game.c`
seguia dando apenas Dynamax Band e Mega Ring, e por isso Z-move e Terastal continuavam mortos para quem joga a história
do começo. Agora ele dá também ITEM_Z_POWER_RING e ITEM_TERA_ORB, custo de save ZERO. T184.1 (bloco novo) lê os quatro
com quantidade 1 na bolsa do jogo novo e fica VERMELHO na ROM de antes em `item_0x2C0` e `item_0x304`; e de jogo novo um
Wobbuffet com Firium Z disparou `gCurrentMove` 857 (Inferno Overdrive) numa selvagem. Build verde, SAVE COMPATIVEL, T11 3/3.

### Povoamento: 10 NPCs por cidade, 07/09/2026 (frente de POVOAMENTO, executor Opus)

**A lei, e ela é do Gui** (07/09/2026, pergunta 53): "cada cidade deve ter pelo menos uns 10 NPCs".
Vale para as cidades EXTERIORES do cartucho 1, ou seja Kanto, Johto, Hoenn e Sinnoh.

**A régua, e ela mede coisa diferente da lista que veio na pergunta.** NPC aqui é OBJETO QUE É
GENTE. Ficam de fora o Pokémon de cenário nas três formas em que ele aparece nesta árvore (a macro
`OBJ_EVENT_GFX_SPECIES(...)`, o gráfico velho que É nome de espécie como `OBJ_EVENT_GFX_MACHOP`, e a
forma de lendário como `GROUDON_SIDE`), a bola de item, o pé de berry e o mobiliário que anda
(caminhão, barco, pedra, placa-objeto). **E fica de fora o `OBJ_EVENT_GFX_LIGHT_SPRITE`, que é POSTE
DE LUZ**: foi ele que fez a contagem da pergunta 53 divergir da desta frente, e a diferença é grande.
VioletCity aparecia com 31 objetos e tem **6 pessoas**, porque 25 dos 31 são lampiões; Ecruteak tinha
"25" e tem 9; Olivine tinha "18" e tem 6. Régua que conta lampião como gente diz que a cidade está
povoada quando ela está vazia.

Com essa régua, **43 das 58 cidades que a lei alcança estavam abaixo do piso**, e não as 20 da
lista. As 15 que já passavam continuam intocadas. (58 e não 61 porque três das 61 TOWN/CITY do
cartucho 1 saem por corte, e estão logo abaixo.)

**O piso, medido e não escolhido a olho.** 10 é a lei. Sobe para 11 em cidade com 700 células secas
alcançáveis ou mais, e para 12 com 1.000 ou mais (`GRANDE` em `povoa_cidades.py`). É área, não gosto:
sem isso Slateport e Twinleaf teriam a mesma população.

**Quem ficou de fora, e por quê.** `FightArea`, `SurvivalArea` e `ResortArea`: são a Battle Zone, que
o Gui cortou do porte em 21/08/2026 (`completude.CORTES_DO_GUI`), e os três mapas são cotocos de
**1x1 célula**. Nenhuma outra cidade exterior do cartucho 1 ficou fora.

### O que entrou

**210 NPCs em 43 cidades**, cada um com objeto próprio no `map.json` e roteiro próprio no
`scripts.inc`: `lock` / `faceplayer` / `msgbox` / `release` / `end`, 1 a 3 páginas de inglês, sem
flag, sem var, sem item e sem batalha. Nenhum `map.bin`, tileset ou `layouts.json` foi tocado (isso é
da frente de ARTE, que rodou em paralelo).

| região | cidades | NPCs | bytes |
|---|---|---|---|
| Kanto | 16 | 90 | 8.358 |
| Johto | 9 | 42 | 3.899 |
| Hoenn | 10 | 54 | 4.996 |
| Sinnoh | 8 | 24 | 2.222 |
| **total** | **43** | **210** | **19.475** |

Os 19.475 B são a SOMA das cidades, lida do `pokeemerald.map` (cada `_EventScript_Povoa*` até o
símbolo seguinte, que é o texto dele) mais 24 B por `ObjectEventTemplate`. A ROM cresceu de
**32.364.808 B para 32.384.280 B**, ou seja **+19.472 B**, medidos build contra build no mesmo HEAD
`ac1b026f53`: os 3 B de diferença são alinhamento. O mesmo +19.472 saiu de duas medições anteriores,
sobre `7053780f27` e sobre `348e4dbd22`, o que é o esperado de dado que só cresce por conta própria. **EWRAM e IWRAM não mudaram um byte** (225.856 e
28.404), e não podiam mudar: objeto e texto moram na ROM.

### A tabela antes e depois, cidade a cidade

| região | cidade | antes | depois | novos | bytes |
|---|---|---|---|---|---|
| Kanto | CeladonCity | 10 | 12 | +2 | 185 |
| Kanto | CeruleanCity | 9 | 12 | +3 | 284 |
| Kanto | CinnabarIsland | 3 | 10 | +7 | 646 |
| Kanto | FiveIsland | 2 | 10 | +8 | 729 |
| Kanto | FourIsland | 5 | 10 | +5 | 460 |
| Kanto | FuchsiaCity | 7 | 11 | +4 | 384 |
| Kanto | IndigoPlateau_Exterior | 2 | 10 | +8 | 733 |
| Kanto | LavenderTown | 3 | 10 | +7 | 646 |
| Kanto | OneIsland | 3 | 10 | +7 | 629 |
| Kanto | PalletTown | 3 | 10 | +7 | 697 |
| Kanto | PewterCity | 6 | 11 | +5 | 470 |
| Kanto | SevenIsland | 3 | 10 | +7 | 637 |
| Kanto | SixIsland | 2 | 10 | +8 | 732 |
| Kanto | TwoIsland | 7 | 10 | +3 | 277 |
| Kanto | VermilionCity | 8 | 12 | +4 | 384 |
| Kanto | ViridianCity | 6 | 11 | +5 | 465 |
| Johto | AzaleaTown | 6 | 10 | +4 | 390 |
| Johto | BlackthornCity | 7 | 11 | +4 | 377 |
| Johto | CherrygroveCity | 6 | 10 | +4 | 377 |
| Johto | CianwoodCity | 6 | 11 | +5 | 465 |
| Johto | EcruteakCity | 9 | 12 | +3 | 268 |
| Johto | MahoganyTown | 4 | 10 | +6 | 533 |
| Johto | NewBarkTown | 3 | 10 | +7 | 659 |
| Johto | OlivineCity | 6 | 11 | +5 | 464 |
| Johto | VioletCity | 6 | 10 | +4 | 366 |
| Hoenn | DewfordTown | 4 | 10 | +6 | 544 |
| Hoenn | EverGrandeCity | 0 | 10 | +10 | 921 |
| Hoenn | FallarborTown | 3 | 10 | +7 | 651 |
| Hoenn | FortreeCity | 6 | 10 | +4 | 390 |
| Hoenn | LavaridgeTown | 9 | 10 | +1 | 86 |
| Hoenn | LittlerootTown | 6 | 10 | +4 | 382 |
| Hoenn | OldaleTown | 4 | 10 | +6 | 553 |
| Hoenn | PacifidlogTown | 3 | 10 | +7 | 641 |
| Hoenn | PetalburgCity | 7 | 10 | +3 | 269 |
| Hoenn | VerdanturfTown | 4 | 10 | +6 | 559 |
| Sinnoh | CanalaveCity | 7 | 10 | +3 | 285 |
| Sinnoh | CelesticTown | 8 | 10 | +2 | 182 |
| Sinnoh | FloaromaTown | 8 | 11 | +3 | 280 |
| Sinnoh | SandgemTown | 6 | 10 | +4 | 375 |
| Sinnoh | SnowpointCity | 8 | 11 | +3 | 265 |
| Sinnoh | SolaceonTown | 9 | 12 | +3 | 279 |
| Sinnoh | SunyshoreCity | 9 | 11 | +2 | 188 |
| Sinnoh | TwinleafTown | 6 | 10 | +4 | 368 |

`EverGrandeCity` tinha **zero** gente, e é o caso mais visível: a cidade da Liga era um portão e uma
montanha, sem uma alma na praia.

### A ferramenta, e por que a POSIÇÃO é dado congelado

`dev_scripts/povoa_cidades.py` mais `dev_scripts/povoa_cidades.json`. A tabela (cidade, gráfico,
posição, movimento, fala) mora no JSON; o script aplica, confere e tem `--demo` de 16 provas.
`--aplica` é **idempotente**: a segunda passada muda 0 arquivos. Cada objeto carrega
`"origem": "povoa_cidades"`, que é a mesma técnica que o `distribui_dex.py` usa desde 21/08/2026
(`tools/mapjson` lê o objeto por chave e ignora chave que não conhece), e é por ela que a ferramenta
reconhece e reescreve o próprio trabalho em vez de duplicá-lo.

**A posição é PROPOSTA por `--sugere` e GRAVADA no JSON, não recalculada a cada rodada.** Isso
importa porque a frente de arte redesenha cidade: posição recalculada em silêncio faria o NPC andar
sozinho pelo mapa entre duas builds, e ninguém veria. `--confere` revalida o dado congelado contra o
`map.bin` de hoje, e foi ele que pegou as sete posições que a arte invalidaria.

**Sete regras de posição, todas conferidas em `--confere` e todas verdes nos 210:**

1. célula andável (colisão 0) com comportamento de CHÃO COMUM, por **lista branca** de 8
   comportamentos (`MB_NORMAL`, `MB_SAND`, `MB_DEEP_SAND`, `MB_SHORT_GRASS`, `MB_FOOTPRINTS`,
   `MB_NO_RUNNING`, `MB_MOUNTAIN_TOP`, `MB_PUDDLE`). Lista branca e não lista negra: o enum tem 250
   nomes e quase todos são mobília, porta, escada, gelo, água ou piso de puzzle, e comportamento
   novo que apareça amanhã tem que entrar como suspeito, não como bom;
2. alcançável a pé, com a regra de elevação do motor (`IsElevationMismatchAt`);
3. não ilha ninguém: o alcance com os NPCs novos como PAREDE é o de antes menos as células deles;
4. longe de porta, placa e gatilho: nem em cima nem na vizinhança-4 de warp, `bg_event` ou
   `coord_event`, nem na FAIXA DA PORTA (os três tiles em linha reta abaixo de cada warp, que é por
   onde quem sai de uma porta desce), nunca em cima de objeto que já existe, e nunca no ANEL DE BORDA
   do mapa (célula de borda aparece dentro do mapa vizinho enquanto o jogador anda na rota);
5. espalhados: Chebyshev 3 entre NPC novo e qualquer outra gente, caindo para 2 só onde a cidade não
   tem chão para 3 (`PacifidlogTown` é passarela de troncos, `IndigoPlateau_Exterior` é trilha);
6. `movement_range` que não invade porta: a caixa inteira passa pelas regras 1 e 4, e por isso o NPC
   em beco recebe `FACE_*`/`LOOK_AROUND` de alcance 0 em vez de `WANDER_AROUND`;
7. teto de sprite: nenhuma janela de 20x17 fica com mais de 15 objetos que gastam vaga.

### As três medições que mudaram o desenho, e cada uma custou uma passada

1. **ÁGUA TEM COLISÃO 0, e busca que só olha colisão atravessa o mar.** Quem barra o jogador na água
   é a ELEVAÇÃO, e quem atravessa é o Surf. A primeira versão do alcance não sabia disso.
2. **Objeto que já existe NÃO É SEMENTE de alcance.** Pokémon de cenário mora em praia e em penhasco
   onde o jogador só chega surfando. Em `CianwoodCity`, semear a busca nos 22 objetos do mapa abria
   **868 células contra as 404 que se alcançam a pé pelas portas**, e cinco NPCs foram parar na praia
   oeste. **Quem pegou foi a lente C2 do `mapas_qa.py`** ("objeto com script inalcançável"), e ela
   estava certa: seis achados novos, cinco de Cianwood e um de Solaceon. Corrigida a semente, a
   ferramenta passou a recusar sozinha essas posições, e a lente voltou a zero achado novo.
3. **NPC é sólido, e beco de largura 1 é comum em vila.** Sem a prova de ilhamento dentro do próprio
   guloso (com a fila ORDENADA, para o segundo colocado entrar quando o primeiro fecha caminho),
   Pacifidlog perdia 9 células atrás de um NPC no meio de um tronco, Fallarbor 4, SixIsland 2 e
   FiveIsland 1.

4. **A FAIXA DA PORTA é caminho, e caminho é parede para objeto novo.** Esta saiu da SUÍTE, e é a
   quarta porque as três de cima não a pegariam. Um `WALK_UP_AND_DOWN` plantado em (31,19) de
   `AzaleaTown` alcança (31,18), que é o terceiro tile abaixo da porta do Kurt, e o **T149.7 abriu
   VERMELHO**: o roteiro descia dois tiles, o segundo DOWN esbarrava no velho, e a rota inteira saía
   um tile do lugar (o jogador parava em (35,14) em vez de (34,15), com os quatro RIGHT andando em
   vez de três, porque o esbarrão come o aperto que serviria para virar). Medido nos dois lados: o
   caso é 14/14 na árvore sem o povoamento e era 13/14 com ele, três execuções seguidas, ou seja
   determinístico e não instável. A regra que ficou é a mesma que o `distribui_dex.py` já aplica com
   `rota_dos_lendarios_sinnoh`: **tile que um roteiro PISA é parede para objeto novo**, e aqui ela
   virou geometria em vez de lista de casos. Reposicionou 15 NPCs em 5 cidades (Azalea, Cinnabar,
   Oldale, One Island e Pacifidlog), sem mudar um byte de texto.

A lição que fica das quatro: **a régua da ferramenta tem que ser pelo menos tão dura quanto a lente e
o teste que vão auditá-la.** Enquanto ela era mais frouxa, a ferramenta dava tudo verde e quem
acusava era a lente C2 e, depois dela, a suíte.

### As provas

- `povoa_cidades.py --demo`: **16 provas verdes**, entre elas a idempotência (2ª passada, 0 arquivos),
  as sete regras nos 210, rótulo único por cidade, nenhuma linha de fala acima de 34 caracteres e
  nenhum caractere fora do charmap nas 212 falas.
- `povoa_cidades.py --censo`: **faltam 0 NPCs**, nas 58 cidades que a lei alcança.
- **Build limpo verde** sobre o HEAD `ac1b026f53`, ROM 32.384.280 B (96,51% de 32 MB), EWRAM e IWRAM iguais
  aos da build sem o povoamento. A ROM desta frente é
  `roms/pokemon-claude-2026-09-07-povoamento.gba`, md5 `ecfab6695463b6a8144fef13b6ee61a2`, com o
  `.map` do linker ao lado.
- `guarda_save.py`: **SAVE COMPATIVEL**. Objeto novo entra no FIM da lista de cada mapa, que é o que
  a save exige (ela guarda ÍNDICE de objeto), e nenhuma flag nova foi gasta.
- `valida_rom.py`: 2.404 mapas e 2.054 layouts, tudo que foi declarado entrou.
- `valida_conectividade.py`: **0 warps quebrados**, alcance **1.969 de 2.293**, os MESMOS números da
  árvore sem o povoamento (medido nas duas).
- `valida_warp_tile.py --piso 60`: **5.937 de 6.893 (86,1%)**, Hoenn 93,4%, Kanto 79,4%, Sinnoh
  98,1%, Johto 91,0%, Unova 100,0%. Idêntico à árvore sem o povoamento.
- `completude.py`: nenhuma coluna caiu e a de objetos subiu nas quatro regiões: Kanto 101,2% ->
  **106,7%**, Johto 100,8% -> **102,6%**, Hoenn 100,7% -> **102,7%**, Sinnoh 99,4% -> **100,6%**.
  Unova e Galar intocadas.
- `roda_qa.py --demo`: **verde nas sete lentes**. Varredura cheia: **14.661 achados com 323 travas**
  contra **14.654 e as MESMAS 323 travas** da árvore sem o povoamento. Os 7 a mais são TODOS da lente
  de texto (`checa_texto` T07, cosmético). Do lado do MAPA a árvore final tem **ZERO achado novo**,
  conferido achado a achado contra a base (6.705 contra 6.705), e isso vale para as 15 regras de
  objeto e de alcance, `B7` (janela de sprite) e `C2` (objeto inalcançável) incluídas.
- **Suíte 1.084 de 1.084**, rodada bloco a bloco (116 blocos, o placar de cada um gravado em disco),
  ZERO reprovado, o T11 à parte. Nem o T176.3, nem o T94.1, nem o T143.9, os três instáveis da rodada
  13, abriram vermelho nesta passada. Ela rodou sobre a build de `348e4dbd22` mais esta frente; sobre
  a build final (`ac1b026f53` mais esta frente) foram refeitos o **T149 (14 de 14)**, o **T11
  (3 de 3)** e a prova no emulador (**5 de 5**), porque o que entrou entre os dois HEADs foi
  `src/new_game.c` e um bloco de teste novo, e nada de dado de mapa.
- **T11 3 de 3**, contra `roms/pokemon-claude-2026-08-18.gba` com a fonte velha na worktree de
  `cf6786b2ae`.
- A suíte foi rodada DUAS vezes inteiras: a primeira, ainda sem a regra da faixa da porta, deu
  **1.077 de 1.078 com o T149.7 vermelho**, e foi ela que achou o defeito descrito acima. Rodar a
  suíte cheia depois de mexer em 43 mapas não é zelo: era a única prova que pegava aquilo.

### A prova no emulador, e ela anda até o NPC

`dev_scripts/prova_povoamento.py`: warpa pelo menu de debug, ANDA até um NPC novo, aperta A, grava o
framebuffer e lê da EWRAM onde o jogador parou. **5 de 5 casos pararam no tile de conversa** e os
cinco PNGs foram abertos e olhados:

| cidade | região | NPC | a caixa que abriu |
|---|---|---|---|
| PalletTown | Kanto | FISHERMAN (18,15) | "The sea opens up south of town. Without SURF you stop at the sand." |
| NewBarkTown | Johto | LASS (12,14) | "Every house here knows every other house. Keep no secrets." |
| OldaleTown | Hoenn | LASS (5,11) | "The MART clerk explains POTIONS to everyone. Every single time." |
| SandgemTown | Sinnoh | WOMAN_4 (12,13) | "The MART here is small but it never runs out of POTIONS." |
| SunyshoreCity | Sinnoh | SCIENTIST_1 (47,12) | "The LIGHTHOUSE lens is solar. The whole city runs on sun." |

**O alvo de cada caso é escolhido pela ferramenta, não decorado**: o NPC mais perto da chegada de uma
porta, entre os que NÃO ANDAM (`movement_range` 0), porque NPC que passeia não está onde o plano diz
quando o roteiro chega lá (lição do T98.9). E o roteiro **se corrige sozinho**: roda, lê da EWRAM
onde parou e, se não for o tile de conversa, RECALCULA o resto do caminho dali e roda de novo. Sem
isso, Sandgem e Sunyshore paravam a um tile do alvo, porque o modelo de "trocar de direção custa um
aperto" erra onde o motor engole aperto por esbarrão.

**Medido de passagem, e vale para toda fala futura: 34 caracteres por linha CABEM na caixa.** A linha
"Without SURF you stop at the sand." tem 34 e apareceu inteira no framebuffer de Pallet Town. E a
primeira leva de PNGs foi tirada com a caixa AINDA DIGITANDO: 180 quadros de espera depois do A não
bastam para uma página de duas linhas, 600 bastam.

### O que fica aberto

- **A lente T07 do `checa_texto.py` acusa inglês em Sinnoh, Unova e Galar** como se essas regiões
  devessem estar em português. A regra contraria a decisão que vale hoje ("sem português no jogo") e
  já acusava 1.124 vezes em Sinnoh antes desta frente; os 7 novos são meus. É cosmético e não é
  trava, mas a régua está mentindo sobre a intenção e alguém vai acreditar nela um dia.
- **`IndigoPlateau_Exterior` recebeu 8 NPCs numa trilha**, com distância mínima 2 em vez de 3, e é a
  cidade mais apertada da leva. Se o Gui achar carregado, tirar é uma linha no JSON.
- **Toda fala é de sabor e de dica verdadeira**, mas nenhuma foi lida pelo Gui ainda. As 212 páginas
  estão no `povoa_cidades.json`, uma por linha, e é lá que ele muda o que não gostar.

---

## 0.u O LETREIRO DE MAPA PARA DE DIZER "SINNOH WEST" E JOHTO PARA DE TOCAR CAVERNA: O NOME DO POPUP SAI DO MAPSEC, E O DE-PARA DE MÚSICA SAI DE PETALBURG WOODS, 05-07/09/2026 (rodada 13; o playtest do Gui, um executor Opus por frente, fechador Opus)

### PLACAR DA RODADA 13, fechado em 07/09/2026

**A ROM do Gui é `roms/pokemon-claude-2026-09-07.gba`**, md5
`c0ea203b6fad9336bba410145fc0663d`, 33.554.432 B de arquivo com **32.371.748 B de conteúdo (96,48%
de 32 MB)**, com o `.map` do linker ao lado. Ela é o HEAD `ed8698166c` **mais os três consertos
pequenos da fila do fechador** (a lava de Blackthorn, a conexão duplicada da Route 43 e as duas lojas
do Pokécenter da Liga), buildada LIMPA (`make clean && make -j8`) na árvore principal com o lock.

Dezoito commits de código entraram, todos com push, mais cinco commits só de ESTADO, mais os dois do
fechador (`14646ff35b`, os três consertos pequenos e este placar; `229800c388`, o percurso de prova
de vida). `5f3a4cb403` é a recalibração dos roteiros que a colisão de `bce66c4718` moveu, então os
dois são a MESMA frente.

| # | conserto | hash |
|---|---|---|
| 1 | O letreiro de mapa passa a dizer o lugar: `map_name_popup` em 1.332 mapas, tabela gerada no build | `b7ef40f330` |
| 2 | Johto para de tocar caverna: 23 apelidos `MUS_HG_*` saem de `MUS_PETALBURG_WOODS` | `fccccc0265` |
| 3 | Trainer Hill e as três Battle Tents devolvem o jogador para o lado por onde ele entrou | `40ebe8eedd` |
| 4 | Toda porta entra: a lente `lente_portas` e o elevador da loja de Goldenrod | `bfe2b35a71` |
| 5 | O Pokécenter de Sinnoh volta a ter uma enfermeira só: 25 corpos repetidos em 15 mapas | `9d63704a3a` |
| 6 | Os portões da frente dos prédios compartilhados (só ESTADO) | `e2ea8fb537` |
| 7 | A igreja de Hearthome abre pelos dois lados, e a placa de obras fala inglês | `95759c9b4f` |
| 8 | Mahogany Town amanhece em neve, e nenhum vizinho respinga | `3711c3b036` |
| 9 | As passarelas de Sunyshore param de comer o sprite: o cruzamento vira portão | `9539325fc3` |
| 10 | Batalha de treinador chamada de gatilho ou de placa para de dar tela azul (lente C28) | `82b42f859c` |
| 11 | O ginásio de Blackthorn para de travar: a ponte deixa de ser pintada de lava | `6b3effaa92` |
| 12 | O jogador para de sumir dentro do brejo da Route 212 South (lente E3) | `7b9a11ce64` |
| 13 | O jogador para de andar por dentro do cenário de Sinnoh, e três ginásios ganham porta | `bce66c4718` + `5f3a4cb403` |
| 14 | As casas pretas de Goldenrod: a posição no array de paleta é o slot | `884c3f9516` |
| 15 | As cidades sem graça ganham enfeite temático, e Canalave ganha um porto | `8c82badf58` |
| 16 | O Contest Hall de Hearthome para de ser um posto de enfermagem | `9313e873f3` |
| 17 | Os três cães acordam na Burned Tower, e o sábio sai da porta do ginásio de Ecruteak | `6c1e43f94c` |
| 18 | Quem entra por uma porta sai por ela: a auditoria de ida e volta dos warps | `ed8698166c` |
| 19 | As cinco meias portas fora do corte: três ganham o warp gêmeo, e o Slumbering Weald não é meia porta (depois do fechamento; a ROM consolidada NÃO tem) | `cfa0d30bd4` |

**A fila do fechador, item a item.** Onze pendências foram anotadas pelos executores na madrugada de
06/09. O que aconteceu com cada uma:

| item | veredito |
|---|---|
| 1. unificar os dois specials de "sair pela porta por onde entrou" | **FEITO na própria rodada** (`ed8698166c`): sobrou só `DefinirRetornoPredioCompartilhado`, e o T171 fecha 10/10 |
| 2. lava do ginásio de Blackthorn, 429 células colisão 0 e elevação 2 | **FEITO pelo fechador**, `dev_scripts/fecha_lava_blackthorn.py` |
| 3. lente E3, Sinnoh 33 e Johto 405 restantes | **ABERTO**, e é rodada própria: 33 são colisão de telhado e 405 são camada `NORMAL` -> `COVERED` como o brejo |
| 4. Route 43 declara `up` duas vezes | **FEITO pelo fechador** |
| 5. 31 portas decorativas de Johto | **ABERTO, e é pergunta 46 ao Gui** |
| 6. `.sav` de teste em caminho absoluto compartilhado | **ABERTO**, e é dívida do `testa_critico.py` |
| 7. lock de build furado e órfão | **ABERTO como regra**, ver as lições abaixo |
| 8. ROM consolidada | **FEITA**, é esta seção |
| 9. 31 corpos repetidos em 25 interiores de Sinnoh fora de Pokécenter | **ABERTO**, e pede estender `corpos_repetidos_pokecenter.py` |
| 10. `PokemonLeagueNorthPokecenter1F`, as duas lojas com `script: "0"` | **FEITO pelo fechador** |
| 11. `importa_npcs_sinnoh.py` e `valida_mapas_sinnoh.py` sem commit | **FEITO na própria rodada** (`9313e873f3`) |

**O que ficou para o Gui, e só ele responde.**

- **Pergunta 46: as 31 portas decorativas de Johto.** A `lente_portas` acha 40 achados na classe "sem
  interior" em Johto: porta que o jogador vê, não abre, e para a qual não existe mapa de interior na
  árvore. Nove são o portão de rota desenhado dos dois lados da emenda, e não são defeito. Sobram 31,
  e fechar cada uma exige INVENTAR conteúdo (interior novo) ou apagar a porta do desenho. Nenhum
  agente decide isso.
- **Pergunta 47: o enfeite das 11 cidades.** As 388 células temáticas de `8c82badf58` são gosto, e o
  gosto é dele: manter como está, podar onde ficou carregado, ou reverter. Cianwood, a 5ª mais sem
  graça pela régua, ficou de fora de propósito e entra ou não na mesma resposta.

**As lições de infra desta rodada, e elas valem para toda rodada com muitos agentes.**

1. **Lock de build furado é pior que lock nenhum**, porque ensina a ignorar o rito. Ele foi furado e
   ficou órfão duas vezes em 06/09. A regra que ficou: **o lock envolve o `make` e nada mais**, e
   frente que precisa de build própria usa **worktree por frente** em vez de disputar a árvore.
2. **Suíte inteira num processo só é aposta.** Com várias frentes na máquina, três execuções foram
   mortas por fora no meio. O fechador rodou **bloco a bloco, com o placar gravado em disco a cada
   bloco**: quem apanha perde um bloco, não a varredura, e a contagem final se soma dos arquivos.
   Formato mantido mesmo com a máquina livre.
3. **`.sav` de teste em caminho absoluto e compartilhado é veredito sorteado.** Os caminhos vivem
   cravados nos `*.json` (`/tmp/claude-501/frenteA/...`), e duas suítes ao mesmo tempo escrevem no
   mesmo arquivo. Três frentes contornaram com um `sed` NÃO commitado; o conserto de verdade é opção
   no `testa_critico.py`, e continua aberto.
4. **Índice do git é compartilhado, e `git add` de uma frente carrega arquivo de outra.** Foi assim
   que o ESTADO de uma frente entrou de carona no commit de outra (`bfe2b35a71`). A regra: cada
   frente commita com `GIT_INDEX_FILE` próprio e lista fechada de arquivos, nunca `add -A`.
5. **Ferramenta descartável com nome genérico atropela a de outra frente.** Duas frentes escreveram
   `patch_estado.py` na mesma pasta, meia hora uma da outra. Ferramenta de uma passada mora na pasta
   da frente, com nome da frente.
6. **`open(caminho, "w")` antes do `assert` trunca o arquivo quando o `assert` cai.** Foi assim que o
   ESTADO perdeu 31 linhas e ganhou um bloco duplicado, o que custou três commits de conserto
   (`b12658fd95`, `7a6e430d8a`, `b58dcbad7f`). Escreva em temporário e renomeie, ou valide ANTES de
   abrir para escrita.
7. **Sem `--offsets`, o `gba_runner` usa os offsets padrão do cabeçalho dele**, e nesta build `vars[]`
   mora em `0x18B8`, não em `0x13E0`: escrita de var cai no lugar errado e o roteiro passa a testar
   outro mundo, calado. O fechador pagou isso montando a prova das lojas da Liga.

**A última medição desta rodada, contra a ROM `2026-09-07`.** Build limpo verde (`make clean && make
-j8`, RC 0), **EWRAM e IWRAM sem mudança**. `valida_rom.py` com os **2.400 mapas e 2.054 layouts
declarados dentro da ROM**. `guarda_save.py` **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B
(94,3%), 2.400 mapas, 2.252 ids de treinador e 1.718 apelidos: os três consertos do fechador são
dado de mapa e de layout, e nenhum deles é índice de save. `valida_conectividade.py` com **0 warps
quebrados**; o alcance caiu de 1.966 para **1.965 de 2.289** e a queda é HONESTA, é o
`LakeOfRageLowTide` saindo do grafo (ver o conserto da Route 43 abaixo). `valida_warp_tile.py --piso
60` em **5.918 de 6.874 (86,1%)**, Hoenn 93,3%, Kanto 79,4%, Sinnoh 98,1%, Johto 90,8% e Unova
100,0%, nenhuma região abaixo do piso. `roda_qa.py --demo` **verde nas SEIS varreduras**, e a
varredura cheia dá **14.663 achados com 323 travas** (Kanto 5, Johto 2, Hoenn 2, Sinnoh 8, Unova 25,
Galar 268, comum 13). `completude.py`: mapas 100% nas seis regiões; objetos Kanto 101,2%, Johto
100,8%, Hoenn 100,7%, **Sinnoh 99,4%**, Unova 102,3%, Galar 103,6%; Dex obtenível 1.571 de 1.571.

**As lentes novas desta rodada, medidas no cartucho 1** (Kanto, Johto, Hoenn e Sinnoh): **C28 zero
achados**, **E1 zero**, **E2 zero**, **E3 zero travas** (os 5.307 achados dela são todos classe
"provável"), **lente_warps zero travas nas quatro regiões** (o que sobra é Unova 38 e Galar 130) e
**lente_portas zero travas em Kanto, Johto e Hoenn**. A lente_portas **tem 8 travas em Sinnoh**, e
elas não são desta rodada nem são regressão: são as portas do corte que já estão registradas
(`JubilifeCity` 42,25; `Route208` 57,14; `Route212_North` 6,50; `Route214` 16,2; `Route221` 82,15;
`SnowpointCity` 29,20; `SpearPillar_Distorted` 16,14; `VeilstoneCity` 31,47, esta última já listada
como túmulo no retrato das 44). Quem disser "zero travas no cartucho 1" está arredondando: são zero
em três regiões de quatro.

**Suíte 1.047 de 1.048** no HEAD `ed8698166c`, rodada bloco a bloco (114 blocos, 1.048 casos, o T11 à
parte), e **T11 3 de 3** contra `roms/pokemon-claude-2026-08-18.gba` com a fonte velha na worktree de
`cf6786b2ae`. O único vermelho é o **T176.3, e ele é INSTÁVEL, não regressão**: medido pelo fechador
em seis execuções seguidas da MESMA ROM, o roteiro entra no `MAP_HEARTHOME_CITY_GYM` em cinco e para
uma célula à direita da porta na sexta, porque a perna `RIGHT*5` conta com o "primeiro toque numa
direção nova só vira" e uma vez em cada seis esse toque anda. Uma pausa entre as pernas foi tentada e
NÃO estabilizou, então o diagnóstico do roteiro ainda não está fechado e o caso fica na lista de
instáveis, ao lado do T94.1 e do T143.9. **Depois dos três consertos do fechador**, os **13 blocos
que passam pelos mapas tocados foram refeitos: 103 de 103, zero reprovado**, com o T176 fechando
**12 de 12** nessa passada, que é a contraprova da instabilidade.

### Os três consertos pequenos do fechador, 07/09/2026

**1. A lava do ginásio de Blackthorn deixa de ser andável.** Eram **429 células com colisão 0 e
elevação 2** no `data/layouts/BlackthornCity_Gym/map.bin`, herdadas do import. Ninguém pisava nelas
hoje, e não por mérito do dado: quem barrava era `IsElevationMismatchAt`, porque o jogador anda em
elevação 3. Era mina: ponte nova encostando na lava por uma célula de elevação 0
(`ELEVATION_TRANSITION`, que casa com qualquer vizinho) deixaria o jogador entrar na elevação 2 e
nunca mais sair. `porta_ginasios_johto.py` LÊ o `map.bin` e nunca o escreve, então o conserto é dado
e mora em **`dev_scripts/fecha_lava_blackthorn.py`**, idempotente e com `--demo` de cinco provas.
Ele muda **só os dois bits de colisão**: metatile e elevação saem byte a byte iguais. **Provas:** as
64 células de ponte que o roteiro abre estão em colisão 1 e elevação 0, ou seja a interseção com o
alvo é VAZIA; a BFS com a regra do motor a partir do tile de chegada do warp dá **31 antes e 31
depois** com as pontes fechadas e **338 antes e 338 depois** com as quatro abertas, e a célula ao
lado da Clair continua alcançável nos dois casos; o `T164` fecha **4 de 4** e o `T90`, que anda com
os cinco Pokémon de overworld do ginásio, **14 de 14**. Os três Pokémon de enfeite que ficam em cima
da lava (CHARIZARD 28,20 e DRAGONITE 11,15 em `WALK_IN_PLACE`, MAGCARGO 28,53 em `WANDER_AROUND` com
alcance 0) não andam, então fechar a célula não prende ninguém que se mexia.

**2. A Route 43 declarava `up` duas vezes, e a segunda era conexão morta.** `MAP_LAKE_OF_RAGE` e
`MAP_LAKE_OF_RAGE_LOW_TIDE`, as duas com `offset: -16`. **O hns tem a mesma duplicata**, e o motivo
está no `data/maps/LakeOfRage/scripts.inc` DELE: lá a maré baixa não é mapa vizinho, é **troca de
layout no próprio LakeOfRage** (`setmaplayoutindex LAYOUT_LAKE_OF_RAGE_LOW_TIDE` dentro do
`ON_TRANSITION`), e `LakeOfRageLowTide` só existe como casca do layout. Esse `ON_TRANSITION` nunca
foi importado, porque a var de enredo do hns foi cortada.

O motor trata as duas conexões de jeitos DIFERENTES, e é isso que fazia da duplicata uma armadilha:
quem ANDA usa `GetMapConnection` (`src/fieldmap.c`), que para no PRIMEIRO casamento de direção, ou
seja `LAKE_OF_RAGE`; quem DESENHA é `InitBackupMapLayoutConnections`, que preenche TODAS e deixa a
ÚLTIMA por cima, ou seja `LAKE_OF_RAGE_LOW_TIDE`. Medido antes de tocar: nas 7 linhas de baixo do
lago, que são a faixa que a Route 43 desenha, os dois layouts são **idênticos célula a célula**,
então a divergência era invisível hoje e ia deixar de ser no dia em que alguém editasse um dos dois.
Ficou **uma conexão**, a `MAP_LAKE_OF_RAGE`. **Provas:** o Lago da Fúria continua alcançável a pé
(`valida_conectividade.py` com 0 warps quebrados, e o lago dentro do grafo); o alcance caiu de 1.966
para 1.965 porque o `LakeOfRageLowTide` saiu, que é a ferramenta parando de mentir; a nota da
`lente_portas` sobre as duas casas do lago de maré baixa foi reescrita para dizer o mecanismo certo,
senão o comentário viraria mentira no primeiro leitor.

**3. As duas lojas do Pokécenter norte da Liga estavam mudas.** `MART_EMPLOYEE` em (12,1) e `CLERK`
em (12,3) tinham `script: "0"` enquanto `PokemonLeagueNorthPokecenter1F_EventScript_Loja1` e
`_Loja2` já existiam no `scripts.inc`, escritos por `mudos_sinnoh.py --lojas-aplica` numa rodada
anterior. O de-para saiu da FONTE e não de chute: em
`res/field/scripts/scripts_pokemon_league_north_pokecenter_1f.s` do Platinum, a entrada 2 é
`VendorCommon` e a 3 é `VendorSpecial`; no `events_*.json`, `LOCALID_LEAGUE_NORTH_CASHIER_F` tem
`script: 2` e `CASHIER_M` tem `script: 3`; e no de-para de `valida_mapas_sinnoh.py`, `CASHIER_F` vira
`MART_EMPLOYEE` e `CASHIER_M` vira `CLERK`. Logo `MART_EMPLOYEE` -> `Loja1` (lista comum) e `CLERK`
-> `Loja2` (`MART_SPECIALTIES_ID_POKEMON_LEAGUE`). O gerador não conseguia refazer isso sozinho: com
os dois corpos repetidos apagados por `corpos_repetidos_pokecenter.py`, o casamento com a fonte
passou a dar `sem_casamento`, e a guarda `tem_loja` do próprio gerador pula o balconista comum em
mapa que já tem `pokemart` escrito. **Prova no emulador:** o menu **BUY / SELL / QUIT** abre nos
DOIS, com a saudação "Welcome! Take a look around, we've got everything a TRAINER needs.", e os PNGs
foram abertos e olhados. A rota usa pernas saturantes de 20 apertos e desarma antes os três
`coord_event` do rival gravando `VAR_SINNOH_RIVAL_VENCEU_SUNYSHORE`; o `T104`, que é o caso do rival
deste mesmo mapa, continua **9 de 9**.

### O quarto conserto, que não estava na fila: o portão de push estava vermelho para todo mundo

`bash dev_scripts/antes_de_empurrar.sh` no HEAD commitado reprovava no passo **"percurso no
emulador"**, e o jogo estava certo. O percurso `fala com tudo em volta` de
`dev_scripts/testa_percurso.py` aperta A oito vezes em cada direção dentro do quarto inicial, e uma
dessas falas é a do NES: ele terminava com a caixa **"RED played with the NES."** ABERTA, e o `START`
que serve de prova de vida não faz nada com caixa aberta. O teste lia "NAO RESPONDE" com o jogo
respondendo.

**Medido, e não deduzido:** a MESMA falha aparece rodando o percurso contra
`roms/pokemon-claude-2026-08-23d.gba` (a ROM da rodada 12, que o Gui jogou) e contra
`roms/pokemon-claude-2026-09-05.gba`, ou seja é antiga e não é regressão desta rodada. O conserto são
**seis `B` antes do `START`**: com eles, a ROM velha e a nova passam, e três execuções seguidas dão
"nenhum problema em 6 percursos". Depois disso o portão fecha **VERDE nos nove passos**. É a lição
4.3 outra vez: portão que não pode ficar verde ensina todo mundo a ignorar a saída, e este estava
assim havia pelo menos duas rodadas.

### A fumaça da ROM consolidada, catorze itens, PNG por item aberto e olhado

| item | o que apareceu na tela |
|---|---|
| letreiro de Sunyshore | "SUNYSHORE CITY" no alto, no lugar de "SINNOH EAST" |
| letreiro de Azalea | "AZALEA TOWN" no alto, no lugar de "SINNOH WEST" |
| música de Goldenrod | `prova_musica_johto.py` **11 de 11**: header e driver leem 521 (`MUS_RG_CELADON`), e o controle de Hoenn continua em 362 |
| praça de Johto -> Trainer Hill -> praça | volta em `TrainerHill_Courtyard` (95.13) em (12,11), na frente da porta por onde entrou |
| Veilstone -> loja -> Veilstone | `prova_portas_compartilhadas.py` **11 de 11**: sai em `VeilstoneCity` (75.9) em (25,31), e não em Lilycove |
| emboscada do Lentimas Gym | caixa "You are challenged by HEX MANIAC SYLVIA!", oponente 2456, sem tela azul |
| ponte do ginásio de Blackthorn | passarela AZUL sobre a lava vermelha, com o jogador em cima dela em (20,48) |
| Mahogany em neve | cidade branca, telhado com cume, e o letreiro "MAHOGANY TOWN" na mesma tela |
| Route 43, controle do vizinho | rocha marrom e grama verde, nenhum floco: o respingo não existiu |
| passarela de Sunyshore | cinco DOWN param em (25,31), o corpo aparece inteiro e o corrimão barra |
| porta da Radio Tower de Goldenrod | `prova_paletas_goldenrod.py` OK: **1,1% de preto** contra o teto de 12%, e o controle das Ruínas em 0,2% |
| Hearthome, árvore e casa | o jogador para em (19,20) na banca, e a POFFIN HOUSE (123.31) entra pela porta |
| Contest Hall | recepcionistas de uniforme e ninguém de touca de enfermeira no salão |
| Ecruteak, o sábio | sem a flag o jogador fica em (20,50), na rua; com `FLAG_JOHTO_CAES_LIBERTOS` ele entra no `EcruteakCity_Gym` (90.8) |
| Route 212 South, o brejo | o jogador continua VISÍVEL em cima do brejo, em (71,20) |

O Gui jogou a ROM `23d` e trouxe o primeiro defeito do playtest: o letreiro que aparece ao entrar num
mapa dizia **"SINNOH WEST", "SINNOH EAST", "SINNOH NORTH", "UNOVA EAST", "GALAR NORTH"** em centenas de
mapas de quatro regiões. Não era dado errado, era o desenho: `MAPSEC` é `u8` e divide o espaço de
valores com `METLOC_SPECIAL_EGG` (0xFD), então Johto, Sinnoh, Unova e Galar **não têm uma seção por
cidade**, e cada lugar é APELIDO de um MAPSEC de GRUPO
(`src/data/region_map/region_map_sections.constants.json.txt`). Como `GetPopUpMapName` copiava
`gRegionMapEntries[mapsec].name`, o letreiro só sabia dizer o nome do grupo. Medido antes de tocar:
**398 mapas de Sinnoh carregavam o MAPSEC de grupo cru** no `region_map_section` e **172 mapas de Galar
estavam em `MAPSEC_GALAR_POSTWICK`**, que era o valor padrão errado de interiores de outras cidades
(Turffield, Wyndon, Wild Area, Isle of Armor).

### O mecanismo novo: o nome do letreiro deixa de ser o MAPSEC

MAPSEC continua `u8` e os apelidos continuam onde estavam. O "met location" do sumário do Pokémon
segue por GRUPO, e isso é aceito. O que mudou é só o letreiro, em quatro peças:

1. **Campo opcional `"map_name_popup"` no `map.json`**, com a string já no formato exibido
   ("SUNYSHORE CITY"). `tools/mapjson` lê o `map.json` por CHAVE (`generate_map_header_text`) e
   **ignora campo que não conhece**: conferido antes de escrever, e por isso o header do mapa não
   mudou um byte.
2. **`dev_scripts/nomes_popup.py`**, o gerador. Deriva o nome nesta ordem: (a) NOME DA PASTA por
   dicionário de radicais, que é a única fonte que sobrou em Sinnoh e em Galar; (b) o APELIDO do
   `region_map_section` transformado (`MAPSEC_UNOVA_R_11` -> "ROUTE 11", `MAPSEC_GALAR_ROUTE01` ->
   "ROUTE 1"), que é a fonte boa em Johto e Unova, onde o demake carregou o apelido certo em cada
   mapa; (c) o que sobra vai para `dev_scripts/qa/nomes_popup_revisao.csv` e **não recebe campo**,
   caindo no comportamento antigo. Interior herda o lugar da cidade, mapa TÚMULO (`MAPSEC_NONE`) fica
   fora, e Kanto e Hoenn ficam fora porque têm MAPSEC próprio. Ele é **idempotente** (rodar duas vezes
   dá 0 arquivos alterados na segunda) e tem `--demo` com 25 casos.
3. **`src/data/map_popup_names.h`, GERADO no build**, não versionado, como
   `region_map_entries.h` já é: um passo em `map_data_rules.mk` com todos os `map.json` como
   pré-requisito o refaz sozinho, e `$(C_BUILDDIR)/map_name_popup.o` depende dele. Um literal por nome
   distinto (**224** no total, compartilhados entre regiões: "ROUTE 5" e "VICTORY ROAD" servem Unova e
   Galar ao mesmo tempo), um array de ponteiros por grupo de mapa que tem nome (**55** grupos) e a tabela de grupos com o tamanho de cada um.
4. **`GetPopUpMapName` ganhou `mapGroup`/`mapNum`** e consulta a tabela antes de cair no MAPSEC. O
   par vem de `gSaveBlock1Ptr->location`, que é exatamente de onde `gMapHeader` é carregado
   (`src/overworld.c:674`), porque `struct MapHeader` não guarda grupo nem número. Celadon Dept.,
   andar e Battle Pyramid continuam como estavam, e o teste "Map names fit in popup" de `test/text.c`
   passou a medir também os nomes novos, agora que recebe o par.

### O que entrou, e o que ficou de fora

| região | mapas com nome | sem nome | nomes distintos |
|---|---|---|---|
| Johto | 220 | 0 | 54 |
| Sinnoh | 394 | 4 | 70 |
| Unova | 280 | 2 | 68 |
| Galar | 438 | 0 | 44 |

Dos 1.332, **317 mostram o letreiro hoje** (`show_map_name` verdadeiro): 66 em Johto, 56 em Sinnoh, 70
em Unova e 125 em Galar. Os outros 1.015 são interiores que hoje não mostram nada, e ganharam o campo
assim mesmo, para que ligar o letreiro num deles amanhã não precise passar por aqui de novo.

**1.332 mapas ganharam o campo** e o CSV de revisão tem **147 linhas**: 6 são "não resolveu" de
verdade (`Cafe`, `Restaurant`, `ForeignBuilding` e `UnusedGateBetweenEternaCityRoute206` em Sinnoh,
`Unova_MobileBattleRoom` e `Unova_MobileTradeRoom`, que são salas de link sem lugar no mundo) e as
outras 141 são **aviso de divergência**, onde a PASTA mandou e o apelido dizia outra coisa: são os
interiores de Galar presos no `MAPSEC_GALAR_POSTWICK`. O aviso fica no CSV de propósito, porque a
divergência é o retrato do defeito do `region_map_section` de Galar, que continua aberto.

### A régua de largura entrou no gerador

O teste `Map names fit in popup` cobra 80 px na `FONT_NARROWER`, e o buffer do letreiro tem 20
caracteres. O gerador mede o nome **mais o sufixo de andar** com a tabela real
(`gFontNarrowerLatinGlyphWidths` de `src/fonts.c` e o `charmap.txt`), e nome que não couber vai para o
CSV em vez de entrar. Medido: o mais largo é **"OLIVINE LIGHTHOUSE", 71 px de 80**, e nenhum dos mapas
nomeados tem andar. Foi essa régua que encurtou "POKEMON WORLD TOURNAMENT" (94 px) para
"WORLD TOURNAMENT".

### A prova está no framebuffer, e é um par antes/depois

Cinco warps pelo menu de debug, PNG por passo, abertos e olhados. Na ROM `23d`, o MESMO warp e a
MESMA rota: `SunyshoreCity` (grupo 75, mapa 13) escrevia **"SINNOH EAST"** e `Galar_Wyndon01`
(grupo 127, mapa 11) escrevia **"GALAR NORTH"**. Na build desta rodada os mesmos dois escrevem
**"SUNYSHORE CITY"** e **"WYNDON"**, e mais: `AzaleaTown` (84, 3) escreve "AZALEA TOWN" no lugar de
"SINNOH WEST", `Unova_NimbasaCity` (107, 0) escreve "NIMBASA CITY" no lugar de "UNOVA EAST", e
`PetalburgCity` (0, 0), que é o controle de Hoenn e não tem campo nenhum, continua escrevendo
"PETALBURG CITY".

### O que fica aberto no letreiro de mapa

- **Porymap não conhece o campo.** `tools/mapjson` ignora chave desconhecida, mas um editor gráfico que
  reserialize o `map.json` inteiro pode deixar `map_name_popup` para trás. Se algum mapa perder o
  campo, `python3 dev_scripts/nomes_popup.py` o repõe sozinho, e o `make` refaz a tabela.
- **Os 172 mapas de Galar em `MAPSEC_GALAR_POSTWICK` continuam lá.** O letreiro deles já está certo,
  mas o `region_map_section` não, e é ele que o sumário do Pokémon e o mapa da região leem. As 141
  linhas de aviso do CSV são a lista exata do conserto, e ele é obra de dados de Galar, não deste
  mecanismo.
- **Seis mapas seguem sem nome próprio** e caem no comportamento antigo: quatro de Sinnoh
  (`Cafe`, `Restaurant`, `ForeignBuilding`, `UnusedGateBetweenEternaCityRoute206`) e as duas salas de
  link de Unova. Precisam de decisão de conteúdo, não de código.

### O segundo defeito do playtest: a música de Johto, 06/09/2026

O Gui trouxe "toda cidade de Johto toca música de caverna". Não era mapa e não era arte de som: era
**de-para de apelido**. Em `include/constants/songs.h`, **23 apelidos `MUS_HG_*`** apontavam para
`MUS_PETALBURG_WOODS`, que nesta build também era o destino de `MUS_CAVE`, `MUS_ROCK_TUNNEL` e
`MUS_SHOAL_CAVE`. Medido antes de tocar: **159 dos 236 mapas dos grupos `*_Johto`** resolviam na mesma
faixa 366, cidade, rota, ginásio, loja e caverna no mesmo som. Nenhuma outra região tinha o problema.

O conserto é troca de constante, **zero arte de som e zero byte de ROM** (32.360.228 B antes e
depois): as faixas de destino já estavam todas na ROM. Cada apelido passou a apontar para uma faixa
com **número próprio** em `songs.h` e `.s` em `sound/songs/midi/`, conferido um a um, porque
`MUS_RG_*` nem sempre entra em build baseada em Emerald.

| apelido | faixa | por quê |
|---|---|---|
| `MUS_HG_NEW_BARK` | `MUS_LITTLEROOT` | vila natal pequena |
| `MUS_HG_CHERRYGROVE` | `MUS_OLDALE` | vilarejo vizinho calmo |
| `MUS_HG_VIOLET` | `MUS_RG_FUCHSIA` | cidade tradicional serena |
| `MUS_HG_AZALEA` | `MUS_VERDANTURF` | vila tranquila |
| `MUS_HG_GOLDENROD` | `MUS_RG_CELADON` | metrópole com loja |
| `MUS_HG_ECRUTEAK` | `MUS_SOOTOPOLIS` | cidade mística tradicional |
| `MUS_HG_OLIVINE` (novo) | `MUS_RG_VERMILLION` | cidade portuária |
| `MUS_HG_CIANWOOD` | `MUS_DEWFORD` | ilha litorânea isolada |
| `MUS_HG_MAHOGANY` (novo) | `MUS_FALLARBOR` | vila serrana pequena |
| `MUS_HG_BLACKTHORN` (novo) | `MUS_EVER_GRANDE` | cidade de montanha |
| `MUS_HG_ROUTE29` | `MUS_ROUTE101` | primeira rota campestre |
| `MUS_HG_ROUTE30` | `MUS_RG_ROUTE1` | rota inicial arborizada |
| `MUS_HG_ROUTE34` | `MUS_ROUTE104` | rota larga litorânea |
| `MUS_HG_ROUTE26` | `MUS_ROUTE120` | rota final úmida |
| `MUS_HG_ROUTE42` | `MUS_ROUTE113` | rota de montanha |
| `MUS_HG_GYM` | `MUS_GYM` | ginásio, direto |
| `MUS_HG_POKE_MART` | `MUS_POKE_MART` | loja, direto |
| `MUS_HG_GAME_CORNER` | `MUS_GAME_CORNER` | cassino, direto |
| `MUS_HG_ELM_LAB` | `MUS_RG_OAK_LAB` | laboratório de professor |
| `MUS_HG_ROCKET_TAKEOVER` | `MUS_RG_ROCKET_HIDEOUT` | ocupação da Rocket |
| `MUS_HG_DANCE_THEATER` | `MUS_CONTEST_LOBBY` | casa de espetáculo |
| `MUS_HG_NATIONAL_PARK` | `MUS_SAFARI_ZONE` | parque natural |
| `MUS_HG_ICE_PATH` | `MUS_RG_MT_MOON` | caverna fria |
| `MUS_HG_DRAGONS_DEN` | `MUS_CAVE_OF_ORIGIN` | caverna mística |
| `MUS_HG_UNION_CAVE` | `MUS_RG_SEVII_CAVE` | caverna comum |
| `MUS_HG_ROCK_TUNNEL` | `MUS_RG_SEVII_DUNGEON` | túnel subterrâneo |

**As dez cidades de Johto têm dez faixas distintas**, conferido por contagem, e caverna só nas quatro
masmorras, cada uma com a sua. Os três apelidos mortos que criavam a armadilha (`MUS_CAVE`,
`MUS_ROCK_TUNNEL`, `MUS_SHOAL_CAVE`, **zero uso** em `map.json` e em código) saíram de Petalburg
Woods também, para que o próximo que os usar não recrie o defeito.

**Catorze `map.json` corrigidos**, que é a herança tosca do import: `OlivineCity` tocava a faixa de
Violet e as seis dependências dela a de Cherrygrove; `Mahoganytown` e `MahoganyTown_House1` tocavam a
de Cherrygrove; as quatro de `BlackthornCity` tocavam a de Azalea; e `MahoganyTown_Shop`, que é loja,
tocava a de Azalea e virou `MUS_HG_POKE_MART`.

**A prova é do emulador, e tem par antes/depois.** `dev_scripts/prova_musica_johto.py` warpa por
debug e lê DUAS camadas: `gMapHeader.music` (o header que o motor carregou) e
`gMPlayInfo_BGM.songHeader` (o ponteiro que o driver de som está tocando naquele quadro), este último
traduzido de volta para o número da faixa procurando o ponteiro em `gSongTable` dentro do binário. Os
dois endereços saem do `pokeemerald.map`. Na ROM `2026-09-05`, que é a que o Gui jogou, Goldenrod, New
Bark, Olivine, Blackthorn, a Rota 29, o ginásio de Violet, a loja de Cherrygrove e o Ice Path leem
**366 nos dois**, ou seja Petalburg Woods; nesta build leem **521, 405, 525, 422, 359, 364, 404 e
500**, cada um a sua. `PetalburgCity` é o controle de Hoenn e lê **362 nas duas ROMs**. O `gba_runner`
ganhou `--mem16` e `--mem32`, leitura crua de endereço, porque nenhuma das duas provas passa por
SaveBlock1.

### Os portões das duas primeiras frentes: o letreiro e a música de Johto

**Suíte 1.002 de 1.003**, com o T11.3 contado à parte, e **T11 3/3** contra a ROM
`roms/pokemon-claude-2026-08-18.gba`, que é a última ANTES do `SAVE_LAYOUT_REVISION` de 19/08 (a fonte
dela é a worktree de `cf6786b2ae` em `/private/tmp/claude-501/t11-r13`). Build verde com o lock,
**ROM 96,44% de 32 MB** (32.360.228 B, **1.194.204 B livres**, 9.632 B a mais
que a 0.t, que é o custo inteiro da tabela e das strings), **EWRAM 86,16% e IWRAM 86,68%**, idênticos
aos da 0.t. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas, 2.252 ids de
treinador e 1.716 apelidos conferidos: não há mudança de struct, de índice nem de flag nesta rodada, e
o campo novo mora no `map.json`, que não entra na save. `valida_rom.py` com os 2.400 mapas declarados
dentro da ROM. `dev_scripts/qa/roda_qa.py --demo` verde nas quatro varreduras, e
`dev_scripts/nomes_popup.py --demo` com 25 casos.

**Os portões foram REFEITOS INTEIROS depois do conserto da música de Johto (06/09/2026), e deram os
MESMOS números**, o que é a prova de que a troca de constante não custou nada: build verde com o lock,
**ROM 32.360.228 B, byte a byte o mesmo tamanho**, EWRAM 86,16% e IWRAM 86,68% iguais, **suíte 1.002 de
1.003** com o T11.3 à parte, **T11 3/3** contra a mesma `roms/pokemon-claude-2026-08-18.gba`,
**SAVE COMPATIVEL** (música não mora na save), `valida_rom.py` com os 2.400 mapas dentro da ROM,
`roda_qa.py --demo` verde nas quatro varreduras e `prova_musica_johto.py` com **9 de 9** mapas certos
no header e no driver de som, contra **1 de 9** na ROM `2026-09-05`.

### O terceiro defeito do playtest: batalha de treinador chamada de gatilho ou de placa dava tela azul, 06/09/2026

O Gui pisou na emboscada da Hex Maniac no `Unova_LentimasGym` (capítulo "before Shauntal") e a ROM
parou em azul com
`SRC/BATTLE_SETUP.C:1258: TRAINER SCRIPT THAT NEEDS TO BE USED FROM AN OBJECT EVENT WAS CALLED FROM
PLAYER`. Não é dado errado, é desenho: **os moldes de `trainerbattle` COM fala de abertura exigem um
objeto de evento selecionado, e gatilho de chão, placa e script de mapa não têm um.**

O caminho, medido no motor e não deduzido: `trainerbattle_single` e irmãos vão a
`EventScript_TryDoNormalTrainerBattle` (`data/scripts/trainer_battle.inc:19`), que chama
`special SetTrainerFacingDirection`; esse special (`src/battle_setup.c:1258`) abre com
`assertf(gSelectedObjectEvent != gPlayerAvatar.objectEventId, ...)`. Quem preencheria
`gSelectedObjectEvent` seria `SetMapVarsToTrainerA`, e ela só reatribui quando o comando traz local
id, mas **todos os macros passam `LOCALID_NONE`**. E `ProcessPlayerFieldInput` zera
`gSelectedObjectEvent` a cada quadro em que o jogador tem controle
(`src/field_control_avatar.c:169`): só o caminho de OBJETO (linha 420) e o avistamento de treinador
(`src/trainer_see.c:484`) o reatribuem. Gatilho, placa e script de mapa não passam por nenhum dos
dois, então `gSelectedObjectEvent` é o jogador e o assert dispara **em qualquer região**.

### A varredura, e ela é curta

`dev_scripts/qa/checa_scripts.py` ganhou a checagem **C28**, que entra em `roda_qa.py` com as outras e
é classe **trava**: ela caminha da entrada SEM objeto (todo `coord_event`, todo `bg_event` e todo
alvo de `<Mapa>_MapScripts`, incluindo os de dentro das tabelas `ON_FRAME_TABLE` e
`ON_WARP_INTO_MAP_TABLE`) e reprova qualquer `trainerbattle` dos oito modos que passam pelo special
(`TRAINER_BATTLE_SINGLE`, `DOUBLE`, os quatro `CONTINUE_SCRIPT*`, `REMATCH` e `REMATCH_DOUBLE`),
achado por `goto`/`call` transitivo. Na árvore de antes do conserto ela achou **18**, e o retrato é
este:

| região | gatilho (`coord_event`) | placa (`bg_event`) | script de mapa | total |
|---|---|---|---|---|
| Kanto | 0 | 0 | 0 | 0 |
| Johto | 0 | 0 | 0 | 0 |
| Hoenn | 0 | 0 | 0 | 0 |
| Sinnoh | 0 | 0 | 0 | 0 |
| Unova | 6 | 0 | 0 | **6** |
| Galar | 0 | 12 | 0 | **12** |
| total | 6 | 12 | 0 | **18** |

Os 6 de Unova são as emboscadas dos dois ginásios do B5 (quatro Hex Maniac no `Unova_LentimasGym`,
uma Youngster e uma Lass no `Unova_AspertiaGym`), o defeito que o Gui viu. Os **12 de Galar** são
todos no `Galar_Circhester03` e ninguém tinha visto: são treinadores que a fonte guardava como
BACKGROUND EVENT, e `treinadores_galar.py` os colocou como `bg_event` de tipo `sign`
(`aplica`, ramo `tipo == "placa"`). Placa cai em `GetInteractedBackgroundEventScript`, que não toca
em `gSelectedObjectEvent`: mesma tela azul, só que ao FALAR em vez de ao pisar. **Nenhum caso
legitimamente diferente apareceu**, porque não existe comando de script que preencha
`gSelectedObjectEvent`: `setvar VAR_LAST_TALKED` escreve `gSpecialVar_LastTalked`, que é outra coisa.

### A regra, e ela já era do FireRed

**Batalha de treinador que não vem de objeto usa o caminho SEM intro**, e o molde é este, igual ao de
`Route24_EventScript_BattleRocket` do FireRed vanilla:

```
	lock
	goto_if_defeated TRAINER_X, <fim>
	applymovement <LOCALID da NPC>, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement <LOCALID da NPC>, Common_Movement_Face<lado do jogador>
	waitmovement 0
	msgbox <texto de abertura>, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, <LOCALID da NPC>
	trainerbattle_no_intro TRAINER_X, <texto de derrota>
	release
	end
```

Três detalhes que não são enfeite. **(1) O `goto_if_defeated` deixa de ser conforto e vira
obrigação**: `trainerbattle_no_intro` cai em `EventScript_DoNoIntroTrainerBattle`, que vai DIRETO ao
`dotrainerbattle` sem o `specialvar GetTrainerFlag` que o caminho com intro tem na linha 16, então
sem ele o gatilho rebate para sempre depois da vitória. **(2) O `setvar VAR_LAST_TALKED`** existe
porque `EventScript_DoNoIntroTrainerBattle` faz `applymovement VAR_LAST_TALKED,
Movement_RevealTrainer` sem perguntar, e numa entrada sem objeto essa var vale `LOCALID_NONE`, que não
é local id de ninguém: `GetObjectEventIdByLocalId` devolve `OBJECT_EVENTS_COUNT` e o `applymovement`
escreve um elemento depois do fim de `gObjectEvents`. Onde não há NPC (as 12 placas de Galar) vale
`LOCALID_PLAYER`, porque `reveal_trainer` em objeto que não é BURIED nem disfarce é no-op
(`src/event_object_movement.c:8769`). **(3) O `release` no fim continua sendo quem solta o jogador**:
o pós-batalha volta pelo `gotopostbattlescript`, que é a linha seguinte ao comando.

O texto de derrota **não sai por `msgbox`**: ele é impresso DENTRO da batalha, do `defeatTextA` que o
`trainerbattle_no_intro` carrega, e é por isso que ele não some ao trocar de molde.

**As quatro NPCs disfarçadas do Lentimas e as duas do Aspertia ganharam `local_id` com nome** no
`map.json` (`LOCALID_UNOVA_LENTIMAS_GYM_HEX1..4`, `LOCALID_UNOVA_ASPERTIA_GYM_YOUNGSTER` e `_LASS`),
que é só um `#define` gerado em `include/constants/map_event_ids.h`: **o header do mapa não muda um
byte** e a save não sente nada, porque `local_id` sem nome já era a posição mais um e continua sendo.

**O gerador de Galar foi consertado junto**, e não só o arquivo que ele escreve:
`dev_scripts/treinadores_galar.py` passa a emitir o molde sem intro para toda linha de `tipo ==
"placa"`, e RECUSA em voz alta placa com batalha dupla, que é o único caso para o qual não existe
molde sem intro.

### O que a lente NÃO cobra, e por que

`EventScript_DoNoIntroTrainerBattle` faz aquele `applymovement VAR_LAST_TALKED` em **196 lugares da
árvore** que caem em entrada sem objeto, e a maioria é **vanilla intocado**
(`EverGrandeCity_ChampionsRoom`, `FiveIsland_LostCave_Room10`, `EcruteakCity_Theater`): as três linhas
de `applymovement` de `trainer_battle.inc` são acréscimo da própria pokeemerald-expansion, para o
seguidor, e o jogo roda com elas há anos. Cobrar isso seria 196 travas de falso positivo calibrado,
pela lição 4.10, então ficou escrito dentro do C28 e não virou checagem. O conserto de hoje escreve o
`setvar` mesmo assim, porque custa uma linha.

Junto veio uma trinca no portão: `roda_qa.py --demo` chamava `mod.demo()` e olhava **só a exceção**,
mas as quatro `demo()` DEVOLVEM 1 quando a mutação plantada não é mordida. Um `return 1` imprimia
"DEMO VERDE" e o portão passava com a lente cega. Agora o código de saída conta.

### A prova está no framebuffer, e são cinco rotas

Todas com o `gba_runner`, warp pelo menu de debug, PNG por passo, abertos e olhados. As rotas saem da
grade de colisão de cada mapa, nunca de chute.

1. **`Unova_LentimasGym`, emboscada 1.** Do warp 0 (7,19) sobem-se 4 tiles até (7,15), porque (7,14)
   é parede; anda-se para a esquerda até (2,15), porque (1,15) é parede; sobe-se até (2,13), porque
   (2,12) é parede; um passo à esquerda para (1,13); e sobe-se a coluna 1 até **(1,8)**, o terceiro
   tile do gatilho. **PNG: a NPC do alto da coluna faz o "!" e a caixa abre com "Eh he he… We have
   trained with the spirits."**; depois dos A, a tela é a de batalha, com a sprite de HEX MANIAC e
   **"You are challenged by HEX MANIAC SYLVIA!"**. Sem tela azul. `oponente=2456`, mapa
   `MAP_UNOVA_LENTIMAS_GYM`, posição (1,8).
2. **O mesmo, com a flag de vitória do motor acesa** (`0x500 + 2456 = 0xE98`): nenhuma batalha
   (`oponente=0`) e o jogador **atravessa os três tiles do gatilho** e para em **(1,6)**, onde a
   própria NPC de (1,5) o bloqueia. É esta que prova que o gatilho não rebate depois da vitória.
3. **`Unova_AspertiaGym`.** Do warp 0 (4,21) sobe-se a coluna 4 até (4,17). **PNG: "You are challenged
   by YOUNGSTER LAMAR!"**, `oponente=2449`.
4. **O mesmo com `0xE91` acesa**: `oponente=0` e o jogador continua subindo.
5. **`Galar_Circhester03`, a placa.** Do warp 2 (26,23) a coluna 26 é corredor limpo até (26,10), onde
   a linha 9 é parede maciça e segura o excedente; três DOWN descem para (26,12), que é a linha SEM o
   NPC de (25,11); os LEFT param em (22,12) porque x21 é parede; dois UP sobem para (22,11) e o
   terceiro só vira, porque (22,10) é a própria placa. **PNG: "You are challenged by BEAUTY Talia!"**,
   `oponente=3069`.

E a prova do texto de derrota é de memória, na camada da afirmação: com a batalha aberta,
`gTrainerBattleParameter` lido cru pelo `--mem32` do runner diz **`defeatTextA = 0x0842E2BD`**, que é
exatamente o endereço de `Unova_LentimasGym_Text_Hex1Beaten` no `pokeemerald.map`, **`introTextA =
0x00000000`** (o motor não tem fala de abertura, ela saiu pelo `msgbox`) e o byte de modo em
`0x02000928` vale **52**, cujo nibble alto é **3 = `TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT`**.

### Mahogany em neve, o primeiro pedido de GOSTO do playtest, 06/09/2026

O Gui perguntou "tem como colocar neve na cidade do ginásio de neve em Johto?" e emendou "ela TODA
em neve seria tão fofo". Mahogany Town é o ginásio de gelo do Pryce, e agora é a única cidade nevada
de Johto: chão branco, rocha nevada, árvore virada em bolo de neve, telhado com cume branco e
**neve caindo** (`"weather": "WEATHER_SNOW"` no `map.json`, o mesmo de Snowpoint).

**A trava, medida antes de tocar em nada:** o secundário `gTileset_MahoganyTown` é de SEIS layouts
(`ROUTE42`, `ROUTE43`, `MAHOGANYTOWN`, `MT_SILVER_OUTSIDE`, `LAKE_OF_RAGE` e `LAKE_OF_RAGE_LOW_TIDE`),
e o primário `gTileset_JohtoNorthEast` é de Johto inteira. Nada de neve podia entrar em nenhum dos
dois. Por isso a cidade ganhou um secundário PRÓPRIO, `gTileset_MahoganyTownNeve`, cópia do outro,
apontado só por `LAYOUT_MAHOGANYTOWN`. Os outros cinco mapas continuam byte a byte como estavam
(`data/tilesets/secondary/mahogany_town/` não mudou um bit).

**O mecanismo é TROCA DE PALETA, não arte nova.** Layout `"johto"` é `bigPrimary`: o primário tem 640
tiles, 640 metatiles e 7 paletas, e ao secundário sobram 384/384 e as paletas 7 a 12. O mapa
(44x28, 1.232 blocos mais 4 de borda) desenha **170 metatiles distintos**, 137 do primário e 33 do
secundário, e as paletas que ele realmente usa são a 0, 1, 2, 3 e 5 do primário e a 8, 10, 11 e 12 do
secundário. Sobravam a **7** e a **9**; a **8** foi liberada convertendo os dois únicos metatiles que
a usavam (880 e 881, a árvore de frutinha). Com três slots na mão:

| slot do secundário de neve | vira a versão nevada de | o que isso pinta |
|---|---|---|
| 7 | paleta 1 do primário | a rocha e o paredão da montanha |
| 8 | paleta 5 do primário | o caminho de areia |
| 9 | paleta 0 do primário (e a 8 do secundário, que é quase igual) | grama, arbusto e árvore |

Cada cor nova é a cor velha projetada numa **rampa de neve de nove âncoras**, todas múltiplas de 8
(que é o passo real de cor do GBA), copiadas da paleta 7 do `mt_silver_snow`, que é a neve que Johto
já usava no Mt. Silver. O metatile nevado é o metatile de origem com os MESMOS tiles, os MESMOS
espelhamentos e a MESMA ordem de camada: só o índice de paleta do quadrante muda. **158 metatiles de
neve** entraram nos slots que o mapa não usava (o mapa ocupava 33 dos 384), e o `map.bin` trocou
**1.219 dos 1.236 blocos**. Os 12 metatiles que ficaram de fora (99, 116, 155, 156, 202, 317, 326,
347, 652, 685, 687 e 829) são parede e telhado puros, sem um quadrante de terreno.

**A única arte desenhada é o cume dos telhados**, e ela é um algoritmo de três linhas: para cada
coluna do tile, acha o primeiro pixel opaco de cima para baixo e pinta os 3 ou 4 seguintes com o
branco da própria paleta do telhado (a 11 tinha os índices 10 a 15 livres e recebeu `E8E8F0` e
`C8D8F0`; a do Centro Pokémon é a 2 do primário, que já tinha `F6F6FF`). São **11 tiles**: 8 do
secundário (118 a 122 e 359 a 361, o cume das casas) e 3 COPIADOS do primário para slots livres do
secundário (192, 193 e 194, o cume do Centro Pokémon), porque o primário é de Johto inteira e não
pode ser tocado.

**Colisão, elevação e comportamento, provados byte a byte** contra o `map.bin` do HEAD: **0 blocos com
colisão ou elevação diferente** e **0 metatiles com atributo diferente** (o atributo do metatile de
neve é copiado do de origem, então grama de encontro continua grama de encontro e porta continua
porta). `valida_warp_tile.py --regiao Johto` fecha em **721 de 795 (90,7%)** e Mahogany não aparece na
lista de quebrados.

O gerador é `dev_scripts/mahogany_neve.py`, **idempotente** (a segunda passada não muda um byte,
porque nenhum slot de destino é origem de outra troca) e com `--demo` de 5 checagens.

**A prova é um par de PNG mais o framebuffer.** `dev_scripts/render_maps.py` antes e depois em
`Pokemon Claude/amostras-tileset/mahogany-neve-antes-depois.png`, e o warp de debug para
`MAP_MAHOGANYTOWN` (grupo 84, mapa 9) mostra a cidade branca **com os flocos caindo**; o mesmo warp
para `MAP_ROUTE43` (grupo 84, mapa 25) mostra rocha marrom, grama verde e nenhum floco, que é a prova
de que o respingo não existiu.

**Conserto de raspão no `render_maps.py`:** ele cortava primário e secundário em **512 metatiles e 6
paletas**, que é o número do Emerald. Layout `"johto"` e `"frlg"` têm 640 e 7 (`GetNumMetatilesInPrimary`
e `GetNumPalsInPrimary` em `src/fieldmap.c`), então TODO mapa de Johto vinha renderizado com o
metatile e a paleta errados, sem uma linha de erro. Agora o corte sai do `layout_version`.

**O que fica aberto:**
- **A transição de bioma na borda é de propósito.** Route 42, Route 43 e o Lago da Fúria chegam sem
  neve, como Snowpoint faz com a Route 216. Se um dia isso incomodar, o caminho é o mesmo: secundário
  próprio para a rota, nunca mexer no compartilhado.
- **O tileset de neve é uma CÓPIA congelada.** Quem editar `mahogany_town` tem que rodar
  `python3 dev_scripts/mahogany_neve.py` de novo para a cópia acompanhar.
- **Porta de Johto não anima, e continua não animando.** `sDoorAnimGraphicsTable` (`src/field_door.c`)
  não tem uma linha de Johto, então nenhuma porta da região tem animação hoje; a troca de id não
  piorou nada, mas quem for ligar isso amanhã tem que usar os ids NOVOS e o tileset novo.

### As cidades sem graça ganham tema, e a régua que as escolheu, 06/09/2026

O Gui, no playtest: "a cidade está muito feia, é assim mesmo?" sobre `CanalaveCity`, e "as cidades sem
graça do ROM hack você podia dar uma enfeitada temática". Onze cidades e vilas foram enfeitadas,
**388 células no total** (386 delas mudam byte de verdade; duas repintam o mesmo
metatile), e Canalave ganhou um porto que não existia em tileset nenhum de Sinnoh.

**PODADO em 07/09/2026: as 333 células do gerador viraram 80**, e com as 55 do porto, que não foram
tocadas, o total sai de 388 para **135**. É a resposta do Gui à pergunta 47 ("manter e podar").
Duas mudanças, as duas no gerador e nenhuma à mão: o teto por carimbo caiu de 6 para **2** e passou a
contar pela ASSINATURA do desenho, porque contar por `id(e)` não segurava nada quando o mesmo carimbo
chegava pelas duas chamadas de `catalogo()` (Celestic tinha 9 placas iguais, Solaceon 11 e Oreburgh 12,
e foi isso que o Gui viu); e o RETALHO DE CHÃO, o quadrado de areia com borda de grama (metatiles 280 a
298 do `gTileset_GeneralSinnoh` e 254 a 263 do `gTileset_JohtoNorthEast`), entrou em `RECUSADOS`, porque
ele não desenha objeto nenhum e só troca o piso: ou vira remendo de outra cor (a areia na calçada de
Eterna e no gramado de Solaceon), ou vira moldura de nada no meio da areia. Por cidade, de 333 para 80:
Canalave 10→6, Celestic 21→6, Snowpoint 18→6, Solaceon 72→6, Oreburgh 51→12, Jubilife 30→10, Twinleaf
14→8, Sandgem 21→10, Blackthorn 30→2, Eterna 36→6, Floaroma 30→8. O plano continua idempotente (três
rodadas seguidas dão `map.bin`, tileset e os dois planos byte idênticos), e o T175.4 e o T175.5 foram
recalibrados por busca, porque mediam cópias que a poda tirou.

#### A régua: `dev_scripts/regua_cidades.py`

A régua de arte que já existia (`completude.py`, `PISO_ARTE = 10`) conta metatiles DISTINTOS por mapa,
e essa conta **não enxerga o defeito que o Gui viu**: Canalave tem 201 metatiles distintos, muito acima
do piso, e mesmo assim a praça dela é um tapete cinza liso. Vocabulário grande com repetição grande
continua sendo mapa sem graça. A régua nova mede três coisas nas **58 cidades e vilas** de Kanto,
Johto, Hoenn e Sinnoh (Unova e Galar são do cartucho 2 e ficam fora):

| coluna | o que é | por que |
|---|---|---|
| `liso` | % das células andáveis com o metatile MAIS COMUM | é a coluna que casa com o olho: o tapete de chão repetido |
| `liso3` | o mesmo somando os TRÊS mais comuns | separa o mapa de um chão só do de chão mais duas costuras, que é o caso do demake |
| `d/100` | metatiles distintos por 100 células andáveis | densidade, não contagem: 250 distintos num mapa 70x64 é mais pobre que 100 numa vila 20x20 |

**Duas armadilhas medidas, e as duas mudavam a lista.** (1) `map_type` sozinho não serve: o conversor
do demake carimbou TOWN em `Route220`, `LakeValor`, `EternaForest` e `ValleyWindworks`, e os três
cotocos 1x1 da Battle Zone entram como cidade. Saem por nome e por piso de células, e a lista de fora
é impressa junto. (2) **A ÁGUA tem colisão 0** no Emerald (quem barra é a elevação, quem atravessa é o
Surf), então contá-la como "andável" fazia o metatile mais comum de Canalave ser o RIO, com 477 das
1.342 células: a régua lia 35,5% de chão liso que era canal. Com a água fora, Canalave marca 27,3% e
**Snowpoint sobe para 87,5%**, que é o retrato certo.

`--pobres` ainda separa NOSSO de VANILLA comparando o `map.bin` byte a byte com a fonte da região
(pokefirered em Kanto, pokeemerald em Hoenn). A primeira versão perguntava ao `git log --follow`, e
**errava**: `LittlerootTown/map.bin` só tem dois commits e o segundo é `89d35e82a2 Move 'map
attributes' into 'layouts'`, que não está em nenhuma lista de assunto de upstream que dê para escrever
sem chutar. Com ela, quatro mapas vanilla de Hoenn entravam na lista de intervenção.

**As 10 mais pobres, medidas antes de tocar** (só as NOSSAS; Hoenn e Kanto vanilla ficam de fora):

| # | mapa | liso | liso3 | d/100 | tema | feito |
|---|---|---|---|---|---|---|
| 1 | `SnowpointCity` | 87,5% | 97,8% | 15,9 | neve | sim |
| 2 | `CelesticTown` | 71,8% | 80,1% | 26,1 | ruínas | sim |
| 3 | `SolaceonTown` | 64,2% | 77,6% | 11,1 | rural | sim |
| 4 | `OreburghCity` | 57,5% | 69,8% | 19,1 | mina | sim |
| 5 | `CianwoodCity` | 54,5% | 83,0% | 18,1 | porto de pedra | **não**, ver abaixo |
| 6 | `JubilifeCity` | 51,6% | 69,2% | 15,2 | cidade grande | sim |
| 7 | `TwinleafTown` | 48,1% | 71,4% | 14,9 | vila natal | sim |
| 8 | `BlackthornCity` | 47,7% | 70,2% | 22,9 | dragões | sim |
| 9 | `SunyshoreCity` | 37,6% | 76,0% | 26,4 | orla | **não**: outro agente editando |
| 10 | `VeilstoneCity` | 37,5% | 61,8% | 14,4 | meteorito | não, fila |

Mais quatro entraram por decisão: **`CanalaveCity`** (27,3% de `liso`, `liso3` 51,6%; é a reclamação
do Gui, e ela cai fora do top 10 justamente porque metade da área dela é canal), **`SandgemTown`**
(37,5%), **`EternaCity`** (29,8%) e **`FloaromaTown`** (31,8%), que vêm logo depois e as duas últimas
têm tema nomeado pelo Gui. Total: **11 cidades enfeitadas, 388 células escritas**.

#### O gerador: `dev_scripts/enfeita_cidades.py`

Nada de arte nova pixel a pixel e nada de metatile inventado: o catálogo de enfeites é EXTRAÍDO,
medindo, de mapas NOSSOS que já são ricos e carregam **o mesmo PAR de tilesets** do alvo (as rotas em
volta de cada cidade). Enfeite é grupo 4-conexo de metatiles raros naquele doador, retângulo cheio de
até 3x3, longe de evento e da borda, com o anel de 8 em volta quase todo andável. São dois tipos, e
eles pagam portões diferentes:

- **Canteiro** (carimbo ANDÁVEL: flor, mato baixo, areia). Escreve só os 10 bits de baixo,
  `(antigo & 0xFC00) | novo`, e só troca metatile por metatile de comportamento IDÊNTICO. Colisão,
  elevação e andabilidade saem byte a byte iguais.
- **Objeto** (carimbo SÓLIDO: árvore, pedra, cerca, placa). Esse MUDA colisão, e por isso só cai em
  célula que é chão liso, **encosta em algo sólido de verdade** (por isso "enfeite de beira": ele fica
  junto do prédio, do muro do canal ou da árvore, nunca plantado no meio da praça), não é evento nem
  vizinha de um, está a 2 células da borda, e **não ilha ninguém**. Isso não é promessa: `alcance()`
  faz busca em largura a partir de todos os warps e NPCs respeitando elevação, e roda **a cada
  carimbo**, exigindo `depois == antes - células_solidificadas`. Carimbo que fecha um beco é desfeito e
  o gerador segue (aconteceu em `CelesticTown`); um portão só no fim saberia dizer "recusado" e mais
  nada.

**Quatro travas que só entraram depois de o desenho sair errado, e todas foram vistas no PNG:**

1. **Espalhar variante de piso, DESCARTADO.** A primeira ideia era trocar parte do chão liso por
   metatiles de comportamento igual e luminância parecida. Em `SolaceonTown` o filtro deixou entrar os
   metatiles de LAVOURA do `gTileset_Celestic`, e o resultado foram centenas de retalhos laranja
   jogados no gramado inteiro: a régua melhorou de 64,2% para 33,6% de chão liso e o mapa ficou PIOR.
   Número de régua melhor com desenho pior é exatamente o que a régua não vê.
2. **Doador tem que ser do mesmo PAR, não só do mesmo primário.** Aprender pelo primário punha arbusto
   de GRAMA verde na neve de Snowpoint, porque a camada de baixo do metatile 486 é grama.
3. **Solidão e isenção.** O metatile tem que cair, na maioria das vezes, em mancha sólida de até 9
   células, senão entram as lascas de PENHASCO (104, 106, 114, 116, 120, 128, 130, 136), que passam no
   anel quando a ponta do penhasco cai na areia mas soltas no meio da praça viram mancha marrom.
   Árvore, arbusto e cerca são isentos com motivo: no demake eles formam a MOLDURA de todo mapa, então
   a mancha deles tem centenas de células.
4. **Atalho de cobertura, com trava de COR.** Enfeite que troca 90% dos pixels do chão pode ir para um
   chão diferente do do doador (é o que solta a pedra na terra de Oreburgh), **mas só se a cor bater**.
   Medido: arbusto verde na neve de Snowpoint dá 253 de distância de cor, contra 29 da pedra na terra
   de Oreburgh e 82 da árvore na grama de Celestic. O limite é 150.

Também há **teto de 6 cópias do mesmo carimbo por cidade**: sem ele Snowpoint ganhava dez placas
iguais, porque o catálogo de neve tem poucos objetos e o rodízio voltava sempre nele.

**Idempotência precisa de arquivo, e é a diferença para o `arte_mapas_pobres.py`.** Lá as escolhas
dependem só de colisão e comportamento, que o gerador não muda; aqui elas dependem do METATILE, que é
justamente o que muda. Por isso o plano guarda o valor ANTIGO de cada célula em
`dev_scripts/enfeita_cidades.json`: na rodada seguinte o script desfaz o próprio desenho em memória,
replaneja sobre a base e escreve de novo. O mesmo arquivo é o **desfazer manual** (`--desfazer`) se o
Gui não gostar de alguma.

**E desfazer só no mapa ALVO não bastava, porque o DOADOR também é cidade enfeitada.** A primeira
versão desta seção afirmava que rodar duas vezes dava byte idêntico, e a prova de dentro concordava,
porque o caso 5 do `--demo` só olha o mapa alvo. Medido em 06/09/2026, sobre a MESMA base: três
rodadas seguidas deram Oreburgh com **45, depois 51, depois 57 células**, e Eterna com 45 e depois 54,
sempre crescendo. A causa é o catálogo: `EternaCity` aprende com `OreburghCity` pelo caminho de mesmo
PRIMÁRIO, e `CanalaveCity` é doadora das outras sete de Sinnoh. Lido do disco já desenhado, o doador
devolve o enfeite da rodada anterior como se fosse arte original, e o vocabulário engorda sozinho.
Duas peças consertaram, e as duas são necessárias:

- **`grade_base()`**, por onde passa TODA leitura de doador, desfaz pelos DOIS planos em disco (o do
  gerador e o do porto). Ela vale só para DOADOR: usá-la também no mapa alvo apagava o porto de
  Canalave, porque o `roda` grava a grade inteira e o porto teria sido desfeito junto. Isso custou um
  render, com a cidade saindo sem um barco.
- **`registra_desenho()`**, que faz o plano crescer EM MEMÓRIA durante a rodada. Sem ela a segunda
  cidade da mesma rodada aprende com a primeira, que o `roda` acabou de gravar em disco.

O `porto_canalave.py` pagou o mesmo preço do outro lado: ele planejava sobre um mapa que já tinha os
enfeites do gerador, e na segunda rodada um poste de luz saía de (9,18) para (9,20). Hoje ele
**planeja sobre a base limpa** (sem enfeite nenhum, nem o dele) e **escreve por cima do disco**,
preservando o desenho do outro script; se algum dia uma peça do porto cair em cima de um enfeite, ele
avisa em voz alta em vez de calar.

Hoje **três rodadas seguidas dão `map.bin`, tileset e os dois planos byte idênticos**, e quem cobra
isso para sempre é o **caso 9 do `--demo`**: nenhuma célula de enfeite de doador nenhum pode chegar ao
catálogo. Ele foi atacado de propósito, quebrando o `grade_base`, e abriu VERMELHO com quatro achados
(Celestic aprendendo de Solaceon e de Jubilife, Solaceon aprendendo de Celestic e de Jubilife).

**A base é o HEAD, e é dela que sai a conta de 388.** O plano da primeira tentativa foi feito numa
árvore compartilhada que tinha, SEM COMMIT, o trabalho de colisão de Sinnoh de outra frente: 136
células só em Oreburgh, 70 em Jubilife e 45 em Solaceon. Isso deu 413, um número que não dava para
commitar sem levar junto o trabalho alheio. O desenho foi refeito sobre o HEAD `7b9a11ce64` e, quando
aquela frente commitou (`bce66c4718`, 401 células só de colisão), **refeito de novo sobre
`884c3f9516`**. As duas vezes o custo foi um comando: `porto_canalave.py` e depois
`enfeita_cidades.py`, que replanejam sobre a base nova sem escrever uma célula fora do plano. É para
isso que a idempotência serve, e é a prova de que ela é real.

#### O porto de Canalave: `dev_scripts/porto_canalave.py`

Canalave é cidade PORTUÁRIA no Diamante/Perola, e o demake trouxe a geometria (o canal, as duas
margens, as duas pontes) **sem uma peça de porto**. Conferido metatile a metatile no atlas: o
`gTileset_Canalave` inteiro é calçada, telhado e água, e Canalave é o ÚNICO layout que o usa, então
não há mapa irmão de quem aprender. Quem tem porto desenhado nesta ROM é HOENN: o `gTileset_Slateport`
guarda o bote, o poste de luz da orla e os tambores do cais.

O script IMPORTA essas peças **sem desenhar um pixel**. Metatile do Emerald tem duas camadas de quatro
tiles, e nesses objetos a de BAIXO é o chão de Slateport e a de CIMA é o objeto com fundo transparente.
Então a camada de cima vem inteira da fonte (só trocando o índice do tile e o número da paleta) e a de
**baixo é substituída pela de Canalave**: a calçada (metatile 521) nas peças de terra e a ÁGUA do
`gTileset_GeneralSinnoh` (metatile 368) nos botes. Como a água é desenhada por tiles do PRIMÁRIO, que
tem animação própria, **o bote flutua em água que se mexe de graça**. O comportamento do metatile novo
é o do CHÃO que entrou embaixo, não o da fonte: a célula do canal continua sendo água para o motor, só
que agora com colisão.

Orçamento, medido antes de escrever: **33 tiles novos** (vagas 384 a 416 das 512 de um secundário; o
`tiles.png` cresce de 128x192 para 128x256, o máximo), **3 paletas** (7, 8 e 9 de Slateport para as
vagas livres 9, 10 e 11 de Canalave, que usava só até a 8) e **15 metatiles** nos locais 160 a 174
(ids 672 a 686). "Vaga em branco" não serve como teste: as vagas livres do `metatiles.bin` de Canalave
não são zero, são o padrão de enchimento do dumper (as oito entradas iguais a 1, ou a 2). O que vale é
o mapa não usar o id, e o script recusa gravar se usar.

No mapa entraram **25 peças, 55 células**: 6 botes atracados no muro do canal, 10 postes de luz e 9
tambores no cais. O canal tem 6 células de largura e o bote tem 3, então sempre sobram 3 para quem
surfa, e isso não é olhômetro: além do portão de alcance A PÉ, roda um portão de alcance DA ÁGUA
(busca em largura pela água do canal) a cada peça.

**Ordem de rodar:** `porto_canalave.py` ANTES de `enfeita_cidades.py`. O porto cria metatiles que não
entram no "chão liso", então o outro nunca os escolhe; o inverso não vale.

#### O que muda em cada célula, lido bit a bit

O plano tem 388 células, e elas se dividem em duas contas, medidas e não afirmadas:

| o que | quantas | o que muda |
|---|---|---|
| canteiro | **145** | só os 10 bits de baixo. Colisão e elevação saem IDÊNTICAS |
| objeto sólido | **241** | colisão 0 -> 1 em todas as 241, e elevação para 0 (172 vinham de 3, 36 de 1, que é a água do canal, e 33 de 4) |
| repinta o mesmo valor | 2 | nada |

Elevação 0 em célula sólida é a convenção do Emerald para obstáculo, e ela é inofensiva porque a
célula deixou de ser pisável; quem prova isso não é a convenção, é o portão de `alcance()`, que roda a
cada carimbo. **Fora dessas 388 células, nenhum bit de nenhum dos onze `map.bin` mudou**: conferido
comparando com o `git show HEAD:` de cada arquivo, 386 células diferentes e ZERO fora do plano. Nenhum
`map.json` foi aberto para escrita, então warp, `bg_event`, `coord_event`, NPC e item estão onde
estavam.

#### Os portões da frente das cidades enfeitadas

Build verde numa worktree ISOLADA (`/private/tmp/claude-501/arte-r13b`, HEAD `884c3f9516` mais só esta
frente), porque a árvore compartilhada tem outras frentes no meio da obra. **ROM 32.371.336 B, 96,47%
de 32 MB**, contra **32.370.248 B** do MESMO HEAD sem esta frente, buildado ao lado em
`/private/tmp/claude-501/arte-baseb`: **+1.088 B**, e esse é o custo inteiro do kit do porto (33
tiles, 15 metatiles e 3 paletas), porque `map.bin` tem tamanho fixo e decoração não ocupa um byte a
mais. **EWRAM 86,16% e IWRAM 86,68%**, idênticos ao HEAD limpo.

**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas, 2.252 ids de treinador e
1.717 apelidos: nenhuma flag, var, item, mapa ou índice novo, porque a frente inteira é dado de mapa e
de tileset. **T11 3 de 3** contra `roms/pokemon-claude-2026-08-18.gba`, com a fonte velha em
`/private/tmp/claude-501/t11-r13` (`cf6786b2ae`). `valida_rom.py` com os 2.400 mapas declarados dentro
da ROM. `valida_warp_tile.py --piso 60` em **5.918 de 6.875 (86,1%)**, com Hoenn 93,2%, Kanto 79,4%,
Sinnoh **98,1%**, Johto 90,7% e Unova 100%: os três warps a mais em Sinnoh são das portas que a frente
de colisão consertou no `bce66c4718`, e não desta; era o que tinha que acontecer, já que nenhum tile de
warp foi tocado aqui. `dev_scripts/qa/roda_qa.py --demo` verde.

**A suíte completa deu 1.034 de 1.040**, com **5 vermelhos e 1 pulado**, e nenhum dos cinco era de
dado: todos eram de ROTA desatualizada. Quatro (T101.7, T101.8, T134.25 e T134.26) foram medidos
TAMBÉM na build do HEAD limpo, com a MESMA posição errada e a MESMA var: vieram do `bce66c4718`, a
frente de colisão de Sinnoh, e não desta. Com as rotas que ela recalibrou em `5f3a4cb403` os quatro
voltam ao verde COM a decoração aplicada (**T101 14 de 14, T125 12 de 12 e T134 26 de 26**, rodados
aqui). O quinto era desta frente, o T175.5, que media uma árvore que a base nova mudou de lugar; a
rota foi refeita pela busca e o bloco fecha em **7 de 7**. O pulado é o T11.3, que exige `--rom2` e
foi rodado à parte, 3 de 3.
**A lente E3 do `mapas_qa.py` deu ZERO novos**, e isso foi medido dos dois lados: a varredura completa
roda na worktree do HEAD limpo e na desta frente, e os dois lados dão os **mesmos 5.307 achados**, sem
um a mais nem um a menos. É a prova de que nenhum enfeite tapa o jogador, que é o risco de trocar
metatile sem olhar o tipo de camada.

#### O caso que a suíte pegou, e o portão novo que nasceu dele

O `corredores_de_teste()` simulava as pernas saturantes **a partir do tile do warp**, e só dele. Isso
está errado para metade dos casos, porque o warp de depuração não promete em que tile o jogador pousa:
o warp 2 de `CelesticTown` é a PORTA de uma casa, em (2,15), e dali não se dá um passo. Simulando só
daquele tile, o corredor da cidade tinha **23 células** e o resto da praça ficava livre para enfeitar.
Na ROM o jogador pousa em **(2,16)** e atravessa a cidade até (16,10), que é o tile de onde ele fala
com o grunt da Galáctica; um carimbo novo o parou em **(6,15)**, e o **T94.1 abriu VERMELHO** com
"a batalha começou contra o id 0". Nada tinha ficado inalcançável, de novo: o caminho só encurtou.

Duas coisas mudaram. A varredura passou a simular **as DUAS hipóteses de pouso** (o tile do warp e o
de baixo dele) vezes as quatro direções iniciais, e o corredor de Celestic saltou de 23 para **46
células**. E entrou o **caso 10 do `--demo`**, que é o cobrador de SAÍDA e não de entrada: para as ONZE
cidades, todo caso da suíte que entra pelo warp tem que TERMINAR NO MESMO TILE antes e depois do
desenho. Ele é conta de grade, não custa emulador, e foi atacado desfazendo o conserto: acusa
`CelesticTown: o caso T94.1 parava em (16, 10) e passou a parar em (6, 15) (pouso (2, 16))`, que é
exatamente a frase que o emulador levou meia hora para dizer.

**O bloco novo é o `dev_scripts/testes_criticos/175_cidades_enfeitadas.json`, 7 de 7 no emulador**, e
ele anda de verdade em TRÊS cidades, com porta atravessada em cada uma:

| caso | o que mede |
|---|---|
| T175.1 | Canalave: o porto PARA o jogador em (17,43); sem ele iria a (16,43) |
| T175.2 | Canalave, a outra margem: para em (27,46) contra (27,44) sem o porto |
| T175.3 | Canalave: a porta do Pokécenter continua abrindo, pisada de verdade |
| T175.4 | Oreburgh: a pedra de (31,28) para o jogador em (30,28); sem ela ele iria a (32,28) |
| T175.5 | Eterna: a árvore de (24,39) para o jogador em (25,39); sem ela ele iria a (23,39) |
| T175.6 | Oreburgh: a porta do ginásio continua abrindo |
| T175.7 | Eterna: a porta do condomínio continua abrindo |

Os cinco primeiros nasceram contra o desenho de 413 células e **abriram VERMELHO em Oreburgh e em
Eterna** a cada troca de base, porque as peças que eles mediam mudaram de lugar. As rotas novas não
foram chutadas: saíram de uma busca que simula as pernas saturantes sobre a grade de ANTES e a de
DEPOIS, para as DUAS hipóteses de pouso do warp de depuração e as QUATRO direções iniciais de olhar, e
só entra a rota que dá uma posição única em todas elas e diferente entre as duas grades. **A lição é
que caso de decoração é caso FRÁGIL por natureza**: ele mede uma peça, e a peça se move quando a base
se move. Quem mexer na base tem que rodar este bloco de novo, e a busca está no repositório para isso
não custar meia hora de emulador.

Os onze pares antes/depois estão em
`Pokemon Claude/amostras-tileset/cidades-enfeitadas/<Cidade>-antes-depois.png`, renderizados dos DOIS
lados (o "antes" sai da worktree do HEAD limpo). Eles foram abertos e olhados: em Canalave os barcos
estão atracados no muro do canal e os postes ficam na calçada, e o par de ANTES não tinha peça de
porto nenhuma, o que denuncia que o render da primeira tentativa mentia.

#### O portão que nenhum portão pega: `RECUSADOS`

Uma peça pode passar em TODOS os portões (colisão, alcance, rota, cor, pureza do anel) e ainda assim
estar errada no olho, porque ela não é enfeite: é peça de LIGAÇÃO, e só faz sentido presa ao que liga.
Os metatiles **175 e 207** são o DEGRAU branco de três células do `gTileset_GeneralSinnoh`. Eles
passam na pureza do anel justamente porque o anel deles é grama pura, e o resultado, visto no render e
não deduzido, era uma **escada flutuando no meio do gramado**: 3 peças em OreburghCity, 3 em
EternaCity e 2 em FloaromaTown, 24 células ao todo. A lista `RECUSADOS` é curta, escrita à mão e com o motivo ao
lado, porque isto é julgamento de desenho e não regra que dê para medir; quem crescer a lista tem que
abrir o PNG antes.

**Risco aberto, e ele é de gosto, não de defeito:** o teto de 6 cópias por carimbo ainda deixa a mesma
placa aparecer seis vezes em Snowpoint e em Celestic, e as vagas que os degraus deixaram foram
preenchidas por retalhos de chão de outra cor (areia sobre a calçada de Eterna, terra sobre o gramado
de Solaceon) que leem como canteiro para uns e como mancha para outros. Nada disso quebra jogo; é
candidato a poda na próxima rodada, com a mão do Gui dizendo quais peças ficam.

#### Cianwood ficou de fora, e o motivo está medido

`CianwoodCity` é a 5ª mais sem graça e **não foi servida**. Os quatro irmãos de par dela (Route47,
Route41, Route44, Route48) não guardam UM objeto solto, e o chão dela (metatile 113, a areia de praia
de Johto) não aparece embaixo de nenhum enfeite dos mapas de mesmo primário: dos 31 carimbos que o
catálogo achou, nenhum passa em `chão`/`cobertura` sem ficar com borda de grama ou de terra na areia.
Servir Cianwood exige importar peça de outro tileset, como o `porto_canalave.py` fez, e isso é obra de
outra rodada. Está escrito em `NAO_SERVIDAS`, dentro do gerador, para ninguém "consertar" achando que
esqueceram.

### O ginásio de Blackthorn para de travar: a ponte era pintada de LAVA, 06/09/2026

O Gui trouxe "está até bonito, mas está travando para andar, do nada trava na lava". A ponte existia,
andava e levava até a Clair; o que não existia era o DESENHO dela. As quatro pontes eram pintadas com
o metatile **889, que é lava vermelha lisa**, o mesmo desenho que a célula já tinha antes de acender:
**46 dos 76 `setmetatile` repintavam o metatile idêntico**, então acender uma ponte não mudava um
pixel. O jogador via o lago de lava inteiro, sem faixa nenhuma, e tinha que adivinhar por onde passar.

A culpa é de uma linha do gerador: `piso_mais_comum()` de `dev_scripts/porta_ginasios_johto.py`
escolhia o metatile mais frequente entre as células de COLISÃO ZERO. Neste mapa isso não é o chão. A
lava de Blackthorn tem colisão zero no `map.bin` (**429 células**) e só não é pisada porque está em
**elevação 2** enquanto o chão está em **3**, e `IsElevationMismatchAt`
(`src/event_object_movement.c:10014`) recusa o passo entre elevações diferentes. Com a lava contando
como piso, a votação deu **889 com 194 ocorrências contra 809, o chão de verdade, com 168**.

**A suspeita de origem era outra, e foi refutada com número.** A hipótese que abriu a rodada era
metatile fora do teto do tileset: `blackthorn_gym` tem 330 metatiles e 889 - 512 = 377 estouraria a
tabela de atributos. Só que `LAYOUT_BLACKTHORN_CITY_GYM` é `layout_version: johto`, ou seja
`bigPrimary` (`include/global.fieldmap.h:128`), e aí `GetNumMetatilesInPrimary` devolve **640**. O
primário `johto_building` define 640 metatiles (10.240 B / 16) com 640 atributos (1.280 B / 2) e o
secundário define 330 (5.280 B / 16) com 330 atributos (660 B / 2): a faixa válida é **640 a 969**. O
maior id do `map.bin` é **948** e o do script é **889**. Nada fora do teto. A elevação 0 das pontes
contra 3 do piso também não é defeito: 0 é `ELEVATION_TRANSITION` e é justamente o que junta dois
pisos, e `setmetatile` nem poderia mudá-la, porque `MapGridSetMetatileIdAt` (`src/fieldmap.c:474`)
preserva os bits de elevação de propósito.

#### O conserto, no gerador

`piso_mais_comum` virou **`piso_da_ponte`**, e a conta certa não é "andável", é "andável NA ELEVAÇÃO
EM QUE O JOGADOR ANDA". A elevação sai do tile de chegada do warp, que é onde ele nasce; a lava está
noutra elevação e some da contagem sozinha. Resultado: **809**, o piso azul de ladrilho.

Cada linha passou a ser conferida contra o `map.bin` antes de virar `setmetatile`:

- célula que o script ABRE e que já está andável **não vira linha nenhuma** (são as 9 pedras azuis
  das pontas das pontes, metatile 857, que o desenho de lava vinha cobrindo);
- célula que o script FECHA e já está bloqueada **sai fora**, era `setmetatile` sem efeito;
- célula que ele fecha e está aberta mantém o próprio desenho e muda só a colisão;
- e ABRIR pintando o metatile que a célula já tem passou a **abortar o gerador com erro**, porque
  essa é a ponte invisível e ela não pode voltar calada.

De **76 linhas** sobraram **64**, todas com o metatile 809. O `map.json` não mudou um byte.

#### Duas lentes novas em `dev_scripts/qa/mapas_qa.py`

| regra | classe | o que mede | achados |
|---|---|---|---|
| `E1` | trava | metatile fora do teto do tileset (o motor lê atributo fora do buffer) | **0** nos 2.400 mapas |
| `E2` | provável | `setmetatile` que ABRE a célula pintando o metatile que ela já tem | **46**, todos em `BlackthornCity_Gym`, e **0** depois do conserto |

O teto do `E1` sai do TAMANHO dos dois `.bin` e o corte sai da versão do layout, nunca de 512
cravado, senão a lente acusaria Johto e Kanto inteiros. O `E2` só conta quando o script ABRE: fechar
repintando o mesmo desenho é idioma legítimo. As duas têm mutação plantada no `mapas_qa.py --demo`.

#### A prova é do emulador, e tem par antes/depois

`gba_runner` com `--mem16` lendo `sBackupMapData`, que é a grade que o motor está usando no quadro,
mais a posição do jogador e `VAR_BLACKTHORN_GYM_STATE`. O mesmo roteiro nas duas ROMs: entrar pelo
warp em (20,58), acender as quatro pontes nos gatilhos de (19..21,55), (17..19,41), (25,26..28) e
(19..21,16) e parar em (19,5), ao lado da Clair, com a var em **4**. Nas duas ROMs a travessia
completa, e é por isso que o defeito não era de colisão. O que muda é o DESENHO: na ROM
`2026-09-05`, que é a que o Gui jogou, as células (20,50), (20,26) e (20,13) leem **metatile 889 com
colisão 0**, ou seja lava andável; nesta build leem **809**. O PNG do mesmo passo, com o jogador
parado em (20,48) no meio da ponte 1, mostra a diferença sem precisar de número: antes, lava por
baixo e por todos os lados; depois, uma passarela azul.

A Clair responde e a batalha começa ("You are challenged by LEADER Clair!"), e a **persistência foi
medida**: com a var em 4, sair para `MAP_BLACKTHORN_CITY`, voltar pelo warp e andar oito tiles ao
norte deixa o jogador de novo em (20,50), com as quatro pontes redesenhadas pelo ON_LOAD (metatile
809, colisão 0, nas linhas 50, 37, 26 e 13).

#### Os portões desta frente, e as três armadilhas que ela pagou

Build verde (`MAKE RC=0`) em **worktree isolada** sobre o HEAD `40ebe8eedd` mais estes três arquivos.
**ROM 96,44% de 32 MB** (32.360.196 B), **EWRAM 86,16%**, **IWRAM 86,68%**. **Suíte 1.012 de 1.013**,
com o T11.3 pulado. `guarda_save.py` = **SAVE COMPATIVEL** (SaveBlock1 em 14.964 de 15.872 B, 2.400
mapas, 1.716 apelidos conferidos; esta rodada não mexe em struct, índice nem flag).
`valida_rom.py` com os 2.400 mapas declarados dentro da ROM. `valida_warp_tile.py` sem nenhuma linha
de `BlackthornCity_Gym`. `roda_qa.py --demo` verde nas quatro varreduras.

1. **`.gba` e `.map` da árvore compartilhada podem ser de links DIFERENTES.** Às 02:53 o
   `pokeemerald.gba` era de 02:30 e o `pokeemerald.map` de 02:44. Ler endereço de símbolo num `.map`
   que não é do binário é prova falsa, e por isso este bloco buildou em worktree própria.
2. **Zero de 1013 é sempre verificação quebrada, nunca notícia.** A primeira passada da suíte na
   worktree deu 0/1013: o `dev_scripts/gba_runner` é binário compilado e NÃO é versionado, então
   `git archive HEAD` não o levou e o `testa_critico` caiu no caminho antigo. Com o runner copiado
   para dentro, a suíte voltou ao normal.
3. **Os 17 reprovados da primeira contagem eram CONTENÇÃO, e a prova é a repetição isolada.** Todos
   os 17 (T11.1, T11.2, T120.9, T120.10, T123.21, T123.22, T127.3, T127.4, T127.9, T127.10, T136.1,
   T136.2, T136.5, T136.6, T139.3, T139.4, T160.4) são pares de save, e o caminho do `.sav` é
   ABSOLUTO e igual para todo mundo (`/tmp/claude-501/frenteA/`). Com sete suítes de agentes
   diferentes gravando no mesmo arquivo, um par sempre perde. Repetidos com `.sav` em pasta própria:
   T11 2/3 (o terceiro é o PULA), T120 10/10, T123 25/25, T127 10/10, T136 10/10, T139 6/6,
   T160 8/8, **zero falha**.

#### O que fica aberto no ginásio de Blackthorn

- **A lava continua andável no `map.bin`: 429 células de colisão 0 em elevação 2.** Hoje ninguém
  chega nelas (a BFS com a regra do motor alcança 335 de 785 células andáveis a partir do warp, e
  nenhuma em elevação 2), e nenhuma célula de ponte encosta nelas, então não há armadilha. Mas é
  mina: ponte nova ao lado da lava deixaria o jogador entrar por uma célula de elevação 0 e nunca
  mais sair, porque de elevação 2 não se volta para 3. Consertar é pôr colisão 1 nessas células, e
  isso é obra de layout, não deste gerador.
- **`porta_ginasios_johto.py` reescreve o `scripts.inc` do zero e apaga o que outros geradores
  escreveram depois dele.** Nesta rodada uma regeneração levou junto a Jasmine escondida de Olivine,
  as cinco pedras de Cianwood e os 16 Pokémon de enfeite, com build verde. O gerador agora **nomeia
  o bloco que apagou** ("AVISO: <mapa>: bloco de OUTRO gerador apagado, rode-o de novo"), e o
  `setflag FLAG_REGIAO_HOENN_LIBERADA` da Clair, que estava escrito à mão dentro do arquivo gerado
  contra o aviso do cabeçalho, mudou de casa para `DEPOIS_DA_INSIGNIA`, dentro do gerador.
- **Caminho de `.sav` de teste é absoluto e compartilhado.** Enquanto vários agentes rodarem a suíte
  ao mesmo tempo, todo par de save vai piscar vermelho sem defeito nenhum. Consertar é derivar a
  pasta do `.sav` do processo, e é conserto do `testa_critico`, não desta frente.

### As passarelas de Sunyshore param de comer o sprite: o cruzamento vira portão, 06/09/2026

Terceiro defeito do playtest, capítulo "before Volkner": o Gui **subia nas passarelas elevadas direto
do chão, sem escada**, e ao andar por elas **o corpo sumia atrás do piso cinza**. Medido em
`data/layouts/SunyshoreCity/map.bin` (70x64): **68 células com elevação 15** (`ELEVATION_MULTI_LEVEL`),
o idioma de PONTE do Emerald, em que `IsElevationMismatchAt` (`src/event_object_movement.c:10014`)
devolve FALSE e o andarilho de elevação 3 pisa nos MESMOS tiles do de elevação 4. **O erro não era a
elevação, era a MISTURA:** 35 das 68 usam metatile de corrimão, de camada de cima cheia e `layer_type`
NORMAL, que `DrawMetatile` (`src/field_camera.c:287`) manda para o **BG1 de prioridade 1**, à frente de
quem tem `sElevationToPriority[3] == 2`; as outras 33 são o piso liso 562, em que o mesmo jogador
aparece inteiro. A passarela nunca foi invadida, e as três subidas legítimas são as ilhas de elevação 0
da arte: o "subir sem escada" era subir no CRUZAMENTO.

O conserto está no gerador `dev_scripts/conserta_passarelas_sinnoh.py` (`--demo`/`--aplica`,
idempotente, com a medição inteira no topo do arquivo): por região conexa de elevação 15, acha o PORTÃO
(colunas em que chão encosta na região dos dois lados, mais toda coluna com `object_event`), fora dele
o piso vira elevação 4 e o corrimão vira parede, dentro dele mantém 15 e troca o corrimão pelo piso
liso. Nenhuma coordenada cravada. **58 células mudaram** (25 viraram parede, 23 viraram elevação 4, 10
trocaram de metatile), nenhum tileset foi tocado e a ROM tem o mesmo tamanho. Selar o cruzamento
INTEIRO foi medido e recusado: cortaria o Pokécenter, a criadora e a Jasmine. A varredura de alcance
semeada nos 12 warps dá o MESMO conjunto antes e depois, **2.801 tiles e nenhum warp fora**.

**Par antes/depois no framebuffer**, mesma rota (warp 4, que entrega em (25,31)), PNG por passo aberto:
na ROM `2026-09-05` cinco DOWN atravessavam o corrimão e paravam em (25,33), em cima da passarela, e em
(27,10) e (27,13) só a ponta do boné aparecia; nesta build os mesmos DOWN param em **(25,31)**, o
jogador aparece **inteiro** em (28,13) e (28,10) e sai em (28,8), quatro UP em (29,14) não sobem, o
marinheiro de (25,17) fica visível de corpo inteiro, e a escada de (42..45, 20..23) leva de (42,24) a
(43,19), já em cima da passarela. **Lição:** a primeira regra selou (26,10), onde mora
`LOCALID_SUNYSHORE_RIVAL`, e o deixaria de pé em cima de uma parede; hoje toda coluna com objeto entra
no portão e o `--demo` recusa gravar se algum objeto acabar em tile impassável.

### Duas lições

1. **Pasta de `.sav` em `/tmp` é veredito falso esperando acontecer.** Seis casos de prova de save
   (T123.21, T123.22, T127.3, T127.4, T127.9, T127.10) abriram VERMELHOS na primeira passada, e o
   motivo não era o jogo: `/tmp/claude-501/fechador` e `/tmp/claude-501/frenteGalar` tinham sido
   limpos pelo sistema desde a rodada 12, e o `gba_runner` respondia "nao consegui abrir sav". O
   conserto ficou em `dev_scripts/testa_critico.py`, na função `roda`, que agora cria a pasta do
   `.sav` antes de chamar o runner; com ela, os dois blocos voltaram 25/25 e 10/10 sem tocar em mais
   nada.
2. **Campo de `map.json` que o `mapjson` não conhece é grátis, e a tabela tem que sair DELE, não da
   derivação.** A primeira versão do gerador montava o `.h` a partir do dicionário de radicais, e não do
   campo que ele mesmo tinha acabado de escrever: quem editasse `map_name_popup` à mão veria o
   `map.json` mudar e o letreiro continuar igual, sem uma linha de erro. Hoje `--tabela` lê SÓ o
   campo, e é esse passo que o `make` chama. Provado trocando o campo de `SunyshoreCity` por
   "PROVA DO CAMPO" e vendo o `.h` mudar sozinho.

### O Pokécenter de Sinnoh tinha três enfermeiras, e a fonte tem uma, 06/09/2026

Defeito do playtest na foto do `SunyshoreCityPokecenter1F` ("before Volkner"). O Gui
apontou duas coisas na mesma tela, e **só uma era defeito**.

**O piso NÃO é defeito, e a prova é o controle de Hoenn.** O "triângulo de bolinhas laranja e
brancas" entre o balcão e o tapete é a **Poké Ball desenhada no chão do Pokécenter**, arte do
Emerald original: um bloco de 4x4 metatiles (620-623, 560-563, 568-571, 576-579) em (5,4)-(8,7),
metade de cima laranja e metade de baixo branca, com a faixa do meio deixada no piso xadrez. Ela
aparece igual no `PetalburgCity_PokemonCenter_1F`, que foi o controle fotografado. Medido, e não
deduzido: `data/layouts/OreburghCity_PokemonCenter_1F/map.bin` difere do
`data/layouts/PokemonCenter_1F/map.bin` em **um único bloco**, o (13,6), que é a escada do B1F; e
`data/tilesets/primary/building/` e `data/tilesets/secondary/pokemon_center/` são **byte a byte
idênticos** ao `fontes-mapas/pokeemerald` (21 e 18 arquivos, md5 a md5). Layout igual mais tileset
igual quer dizer que o que a ROM desenha ali é o que o Emerald desenha. Nada mudou no piso.

**A gente é que estava repetida.** Contado nas 18 fontes de Pokécenter 1F do Platinum
(`fontes-mapas/pokeplatinum/res/field/events/events_*_pokecenter_1f.json`): **cada uma tem
exatamente UMA** `OBJ_EVENT_GFX_POKECENTER_NURSE`, sempre em (8,4) da grade de lá, sempre com
script. Não existem as atendentes de Wi-Fi/Union/GTS que a suspeita inicial levantava, e não havia
sprite errado: `OBJ_EVENT_GFX_NINJA_BOY` é byte a byte o `ninja_boy.png` do Emerald, e o menino do
Emerald **tem cabelo rosa mesmo**. O que havia eram **corpos repetidos da mesma pessoa**, por duas
portas distintas:

1. **`fecha_portas_sinnoh.py`, na criação do mapa.** O arquétipo `pc1` copia o NPC funcional do
   índice 0 de `OreburghCity_PokemonCenter_1F` (a enfermeira com o `Common_EventScript_PkmnCenterNurse`)
   e o insere na posição 0, enquanto `conteudo_do_mapa` já tinha importado a enfermeira DA FONTE
   como um objeto qualquer. Duas mulheres, a mesma pessoa: a importada ficou muda, de pé na frente
   do balcão. É a enfermeira de (8,4) de onze mapas.
2. **`importa_npcs_sinnoh.py`, nas rodadas de completude de 22 e 23/08.** A guarda de idempotência
   dele reconhece "já importado" por VIZINHANÇA de até um tile. Nesses mapas a planta é
   REAPROVEITADA do repo, então a coordenada da fonte não diz nada: a régua de escala mudou entre
   rodadas, a mesma pessoa caiu em (8,4) numa passada e em (10,2) na seguinte, e nenhuma reclamou a
   outra. Foi assim que nasceram a terceira enfermeira de Sunyshore e de Hearthome, o segundo
   menino de cabelo rosa de Sunyshore, a segunda LASS de Canalave e de Snowpoint, a segunda WOMAN_3
   de Eterna e as demais.

As duas portas foram fechadas nos geradores: `fecha_portas_sinnoh.py` não importa mais o corpo mudo
que tem o mesmo gráfico do NPC funcional, e `importa_npcs_sinnoh.reclama` passa a reclamar por
IDENTIDADE (mesmo `graphics_id`, em qualquer lugar do mapa) quando o `map.json` diz
`planta reaproveitada`. O que já estava escrito saiu por
**`dev_scripts/corpos_repetidos_pokecenter.py`**, idempotente e com `--demo` de nove provas:
**25 corpos em 15 mapas**, e cada um passou por cinco portões: mapa com fonte no Platinum; objeto
MUDO e anônimo (script "0", flag "0", sem `local_id`, sem treinador); marca `pokeplatinum`; a
pessoa continua no mapa e COM a fala dela (existe outro objeto do mesmo gráfico que tem script); e
a fonte tem menos corpos daquele gráfico do que nós.

| mapa | corpos apagados |
|---|---|
| SunyshoreCityPokecenter1F | 3 (NURSE 8,4; NINJA_BOY 13,4; NURSE 10,2) |
| EternaCityPokecenter1F | 3 (NURSE 8,4; SCHOOL_KID_M 1,6; WOMAN_3 13,3) |
| CanalaveCityPokecenter1F | 2 (NURSE 8,4; LASS 9,8) |
| CelesticTownPokecenter1F | 2 (NURSE 8,4; EXPERT_F 13,4) |
| HearthomeCityPokecenter1F | 2 (NURSE 8,4; NURSE 10,2) |
| PokemonLeagueNorthPokecenter1F | 2 (NURSE 3,2; NURSE 0,2) |
| SnowpointCityPokecenter1F | 2 (NURSE 8,4; LASS 0,2) |
| SolaceonTownPokecenter1F | 2 (NURSE 8,4; OLD_MAN 13,3) |
| Floaroma, Jubilife, Oreburgh, Pastoria, LeagueSouth, Sandgem, Veilstone | 1 cada (a enfermeira muda) |

**A armadilha do apagar, desarmada antes e não depois.** Apagar objeto desloca o id de todos os
seguintes do mesmo mapa (`tools/mapjson` gera `#define <local_id> <posição + 1>`). Os
`LOCALID_*_PC_NURSE` destes 15 mapas apontam todos para a posição 0, que nunca sai, e os `#define`
escritos à mão em `include/constants/sinnoh/*.h` para eles valem todos 1. O caso perigoso era um só
e estava medido: `PokemonLeagueNorthPokecenter1F` chamava o rival por **`addobject 7`** cru, e as
duas enfermeiras a apagar estavam ANTES dele. A ferramenta batiza o objeto antes de apagar qualquer
coisa (`LOCALID_LEAGUE_NORTH_PC_RIVAL` no `map.json`, a constante no lugar do número no
`scripts.inc`) e RECUSA o mapa inteiro se sobrar id cru sem batismo.

**Três enfermeiras mudas continuam no repo, e é de propósito**: as de `FloaromaTown`,
`JubilifeCity` e `OreburghCity` em (3,2) já estão atrás de `FLAG_SINNOH_NPC_DUPLICADO`, ou seja
invisíveis em jogo novo desde a leva de 12/08. Corpo com flag não passa no portão 2 desta
ferramenta, e mexer nelas seria refazer uma decisão já tomada.

**Duas lições desta frente.**

1. **Defeito relatado por foto pede CONTROLE antes de conserto.** O piso "errado" era arte do
   Emerald, e bastou fotografar um Pokécenter de Hoenn no mesmo emulador para ver a mesma Poké Ball.
   Sem esse par, o conserto teria sido reescrever um `map.bin` que está certo desde 2004.
2. **Sprite estranho não é sprite errado.** As "figuras de cabelo rosa que parecem enfermeira" eram
   o `OBJ_EVENT_GFX_NINJA_BOY` do Emerald, cujo `ninja_boy.png` é idêntico ao do upstream. O defeito
   não estava no de-para, estava na CONTAGEM: eram dois meninos onde a fonte tem um.

**Os portões desta frente.** Build verde com o lock (ROM 96,47% de 32 MB, 32.369.368 B; EWRAM
86,16%, IWRAM 86,68%). `guarda_save.py` **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B,
2.400 mapas: apagar objeto NÃO é índice de save, o que a save guarda de mapa é `(mapGroup, mapNum)`,
e nenhum deles andou. `valida_rom.py` com os 2.400 mapas declarados dentro da ROM.
`valida_conectividade.py` com 0 warps quebrados, `valida_mapas_sinnoh.py` com `'sprite': 0` e 0 mapas
com problema, `valida_warp_tile.py --piso 60` sem região abaixo do piso, `completude.py` com Sinnoh
em 100,3% de objetos. **T11 3/3** contra `roms/pokemon-claude-2026-08-18.gba` (fonte na worktree de
`cf6786b2ae`). Suíte **1.008 de 1.015** com o T11.3 à parte; os seis vermelhos são de obra ALHEIA em
curso na mesma árvore, e isso foi medido, não suposto: T140.1/3/4 andam pelo `ContestHallLobby`, cujo
`map.json` e `scripts.inc` outra frente está reescrevendo neste momento; T151.3/4 andam pela sala de
treinador do ginásio D/P de Hearthome, cujo `map.bin` outra frente está redecorando; T170.4 é da
frente de Johto. Contra a ROM entregue `2026-09-05`, com o `--src` casado numa worktree de
`b7ef40f330`, esses cinco passavam e outros três (T140.7, T140.8, T140.11) falhavam, ou seja a linha
de base da árvore compartilhada se move sozinha enquanto várias frentes escrevem nela.

**FECHADO PELO FECHADOR, 07/09/2026:** era mesmo obra alheia em curso. Na build limpa do HEAD `ed8698166c`, com a árvore parada, os seis passam e a suíte fecha em 1.047 de 1.048 (ver o placar no topo desta seção).

**O mesmo defeito tem 31 irmãos fora do Pokécenter, e eles ficam abertos.** Passando as MESMAS cinco
provas em todo interior de Sinnoh de planta reaproveitada, sobram **31 corpos mudos repetidos em 25
mapas** (`VeilstoneStore2F` a `5F`, os seis Marts, `CanalaveLibrary1F/2F/3F`, `MiningMuseum`,
`PoffinHouse`, `Route222WestHouse`, `SunyshoreCityWestHouse`, `CycleShop`, e mais). Não entraram
porque o `PARES` desta ferramenta é de Pokécenter, escrito à mão; estendê-lo pede o mesmo casamento
mapa-a-fonte que `importa_npcs_sinnoh.headers_do_platinum()` já faz, e é rodada própria.

### O Contest Hall tinha sete enfermeiras, e a fonte tem três recepcionistas, 06/09/2026

Defeito do playtest, dito assim: **"que tanto de enfermeira é essa?"**, na casona do Contest Hall de
Hearthome, na ROM `2026-08-23d`. Medido no `map.json` antes de tocar em nada: `ContestHallLobby`
tinha **7 objetos `OBJ_EVENT_GFX_NURSE` num salão de 11**, e a fonte
(`fontes-mapas/pokeplatinum/res/field/events/events_contest_hall_lobby.json`) tem **3** atendentes de
balcão, que lá são as recepcionistas do concurso.

São **duas causas somadas**, e nenhuma delas é o Contest Hall.

#### Causa 1: o de-para de sprite não olhava o MAPA

`OBJ_EVENT_GFX_POKECENTER_NURSE` não quer dizer "enfermeira" no Platinum: quer dizer **atendente de
balcão com aquele uniforme**. Em Pokécenter ela é a enfermeira mesmo; no lobby do Contest Hall ela é
a recepcionista. A linha fixa da `TROCA_SPRITE` mandava as duas para `OBJ_EVENT_GFX_NURSE`.

Medido nos 497 mapas de Sinnoh casados com a fonte, antes do conserto: dos **21 objetos** com esse
gráfico, **18 estão num `events_*_pokecenter_1f`** e **3 estão em `events_contest_hall_lobby`**. Por
isso o conserto é um PAR, e não uma troca de linha: `valida_mapas_sinnoh.TROCA_SPRITE_POR_BALCAO`
guarda `("OBJ_EVENT_GFX_NURSE", "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST")`, e
`V.troca_de_sprite(gfx, pokecenter)` escolhe pelo contexto do mapa. A chave continua na
`TROCA_SPRITE` com o destino de MAIORIA de propósito, porque quem consulta a tabela sem contexto
(e `corpos_repetidos_pokecenter.py` consulta) tem que continuar recebendo a resposta certa para 18
dos 21.

**Quem responde "este balcão é de Pokécenter?" são três testemunhas, nesta ordem, e nenhuma delas é o
nome da nossa pasta**, que é justamente o que envelhece calado: (1) o arquivo de eventos DA FONTE;
(2) o motor, porque mapa que é `respawn_map` de uma heal location tem enfermeira por definição, senão
ninguém cura o jogador; (3) o script, porque objeto cujo rótulo se apresenta como enfermeira é
enfermeira (a régua da rodada 10, "o de-para por nome olha o script").

**O inverso do de-para NÃO é função, e reaplicá-lo nos dois sentidos plantaria defeito novo.** Isto
quase custou caro: `OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST` é destino de **cinco** gráficos da fonte
(`RECEPTIONIST`, `WIFI_PLAZA_ATTENDANT_F` e os três `FRONTIER_*_ATTENDANT`), então ler "recepcionista
num Pokécenter" como "enfermeira fora do lugar" poria **quinze enfermeiras** nos porões de Union Room
dos Pokécenters de Sinnoh, onde a fonte tem a atendente de Wi-Fi. `OBJ_EVENT_GFX_NURSE`, ao
contrário, tem UMA origem só em todo o de-para, e é por isso que só ele volta atrás. O `--demo` de
`de_para_sprites_sinnoh.py` cobra as duas metades desta frase CONTRA a tabela, e não como texto.

#### Causa 2: em planta emprestada, a coordenada não é testemunha, e a vizinhança também não

197 mapas de Sinnoh nasceram com a planta REAPROVEITADA de outro mapa do repo
(`fecha_portas_sinnoh.py` grava isso no próprio `map.json`). Neles a régua de escala mudou entre
rodadas, a mesma pessoa caiu em (8,4) numa passada e em (10,2) na seguinte, e a guarda de
idempotência do importador, que reconhecia "já importado" por VIZINHANÇA de um tile, não reconhecia
as duas como a mesma. Foi assim que os Pokécenters chegaram a três enfermeiras (subseção acima) e o
Contest Hall a sete.

O conserto tem **duas metades, e a segunda só apareceu depois de a primeira entrar**:

1. Onde a planta é emprestada, quem reclama é a **IDENTIDADE**: se o mapa já tem um corpo com aquele
   mesmo `graphics_id`, a pessoa já está lá, em qualquer lugar do mapa. Junto veio um conserto que
   parece de detalhe e é a raiz: o `graphics_id` que chega no `reclama` passou a ser o **NOSSO**, e
   não o da FONTE. Até aqui o de-para só era aplicado depois dos tetos, então
   `OBJ_EVENT_GFX_POKECENTER_NURSE` nunca casava com o `OBJ_EVENT_GFX_NURSE` que o mapa já tinha, e a
   mesma mulher entrava de novo a cada rodada.
2. **A vizinhança precisou SAIR junto.** Enquanto o `perto` valia em OU com a identidade, a PRIMEIRA
   pessoa da fonte reclamava para si qualquer corpo importado a um tile de onde ela caiu, fosse ela
   ou não. Medido em `HearthomeCityNortheastHouse1F`: a `POKEFAN_F` da fonte tomou o corpo da `TWIN`,
   a `TWIN` não achou mais o dela e entrou de novo, e o mapa ficou com **duas TWIN e nenhuma
   POKEFAN_F**. Contagem certa, elenco errado, e um **pingue-pongue eterno** com o corte de
   `de_para_sprites_sinnoh.py`, que via a TWIN sobrando e a apagava toda rodada. Com a vizinhança
   fora, os dois passam a concordar por construção, e a idempotência é MEDIDA: importador aplicado,
   depois o de-para, e o de-para diz `mapas tocados: 0`.

#### A ferramenta: `dev_scripts/de_para_sprites_sinnoh.py`

Conserto de raiz é no gerador; o que já está escrito sai por esta ferramenta, idempotente e com
`--demo` de nove provas. Ela **repinta** (o gráfico que o contexto do mapa desmente) e **corta** (o
corpo repetido que a fonte não tem), e o corte passa por quatro portões: marca `pokeplatinum`, objeto
MUDO (`script: "0"`), sem flag e sem `local_id`. **O corte sai sempre dos ÚLTIMOS corpos daquele
gráfico**, e nunca de quem fala: em todos os 27 mapas a pessoa continua no mapa e continua com a fala
dela.

Ela **não escreve `map.json` de Pokécenter** de propósito (trava de escrita; aqueles são da frente
dos Pokécenters, na subseção acima) e **não devolve fala a NPC mudo**, que é a outra metade do
estrago e precisa do índice de script da fonte.

#### A conta, mapa a mapa

**27 interiores de Sinnoh, 144 objetos antes e 126 depois: 7 repinturas, 38 corpos mudos cortados e
20 pessoas de verdade que entraram no lugar.** As 20 entraram porque o corte abriu vaga sob o teto da
fonte, e são gente que o Platinum tem e nós não tínhamos: no Contest Hall, **FANTINA**, uma beauty e
uma picnicker no lugar de quatro enfermeiras a mais.

| mapa | antes | depois | o que mudou |
|---|---|---|---|
| `ContestHallLobby` | 11 | 9 | as 7 NURSE viram recepcionistas, 5 corpos saem (4 recepcionistas a mais que a fonte e um rich boy), FANTINA + beauty + picnicker entram |
| `VeilstoneStore2F/3F` | 7 / 6 | 7 / 6 | 2 cortes e 2 entradas em cada |
| `MiningMuseum`, `ForeignBuilding`, `HearthomeCityPokemonFanClub` | 8 / 9 / 6 | 8 / 9 / 6 | 2 cortes e 2 entradas em cada |
| `CanalaveLibrary1F/2F/3F` | 3 / 2 / 5 | 2 / 1 / 3 | 4 corpos repetidos, sem vaga a repor |
| 6 Marts de Sinnoh | 5 cada | 4 cada | o `MART_EMPLOYEE` mudo de (3,2), que era cópia do caixa |
| `PoffinHouse`, `VeilstoneStore4F/5F/B1F`, `CycleShop`, `PokemonDayCare`, `EternaCityCondominiums1F`, `EternaCityMart`, `JubilifeTv2FGallery`, `JubilifeTv3FGroupRankingRoom`, `HearthomeCityNortheastHouse1F`, `SunyshoreCityGymRoom2` | | | 1 ou 2 cortes, 0 ou 1 entrada |

**Índice de objeto ANDOU em 12 desses mapas, e isso foi medido antes de gravar, não depois:** nenhum
`scripts.inc` dos 27 usa `addobject`, `removeobject`, `applymovement` com número cru nem `LOCALID_`,
então não há script mirando outra pessoa. O que a save guarda de mapa é `(mapGroup, mapNum)`, e
`guarda_save.py` diz **SAVE COMPATIVEL**.

#### O corredor de teste entrou no importador, e ele pegou dois casos

**Corpo novo em cima de roteiro de suíte é caso vermelho.** O `sem_tranca` prova que nada fica
inalcançável, e isso NÃO basta: objeto é sólido, e a perna de um roteiro não para onde o autor
escreveu, e sim no primeiro obstáculo. A lição é emprestada de `enfeita_cidades.corredores_de_teste()`
desta mesma rodada, que perdeu sete casos de balsa para um poste de luz.

`importa_npcs_sinnoh.corredores_de_teste()` varre `dev_scripts/testes_criticos/*.json`, simula as
pernas de DIREÇÃO de cada caso que entra no mapa por `warp` a partir do pouso, SEM olhar parede, e
congela toda célula pisada. É aproximação POR EXCESSO: caso que entra no meio por `WARP=` não é
simulado. Ela barrou **dois** corpos: a `MOM` que a fonte quer em (4,5) do `ContestHallLobby`, que é
a quarta célula da subida do T140.1 e do T140.3, e o `SINNOH_RILEY` de (21,10) do `IronIsland`, que o
`sem_tranca` já vinha barrando pelo T124.2.

#### A prova é do emulador, e o par é de PALETA, não de olho

`OBJ_EVENT_GFX_NURSE` usa `OBJ_EVENT_PAL_TAG_NPC_1` e `OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST` usa
`OBJ_EVENT_PAL_TAG_NPC_WHITE`: **são palettes diferentes**, então dá para provar a troca lendo a PLTT
OBJ, e não descrevendo o que se vê. A cor é `0x32B9` = (205,172,98) de `npc_white.pal`, a mesma que o
T96.1 já usa. Três casos novos em `dev_scripts/testes_criticos/180_elenco_sinnoh.json`:

| caso | mapa | ROM `2026-08-23d` | esta build |
|---|---|---|---|
| T180.1 | `ContestHallLobby` | `npc_white` **ausente** | `npc_white` **presente** |
| T180.2 | `VeilstoneStore2F` (controle) | presente | presente |
| T180.3 | `ContestHallLobby`, sobe da porta até a porta fechada do palco | (caso novo) | para em (6,1) |

**O T180.2 é o que impede o T180.1 de ser um relógio parado**: ele lê a MESMA cor num interior de
Sinnoh que esta frente não repintou, e ela já estava lá na ROM que o Gui jogou. Sem ele, `0x32B9`
estaria medindo "build nova", e não "recepcionista no lugar da enfermeira".

Os PNGs foram abertos e olhados, nas duas ROMs: no `ContestHallLobby` da `23d` o salão é uma fileira
de mulheres de cabelo rosa e touca branca; nesta build não há nenhuma, e no lugar delas estão as
recepcionistas de uniforme verde e a FANTINA de cabelo lilás. No `VeilstoneStore2F` da `23d` havia
DUAS mulheres idênticas no canto de baixo; nesta build há uma.

#### Os portões da frente do Contest Hall

Build verde numa worktree ISOLADA (`/private/tmp/claude-501/sprites-r13`, HEAD `7b9a11ce64` mais só
esta frente), porque a árvore compartilhada tem outras cinco frentes no meio da obra. **A ROM
entregue é desse HEAD**: enquanto esta frente estava no emulador, outras três commitaram e o HEAD
compartilhado andou para `8c82badf58`, que a `06s` não contém. **ROM
32.369.672 B, 96,47% de 32 MB; EWRAM 86,16% e IWRAM 86,68%**, os mesmos das outras frentes desta
rodada. `guarda_save.py` **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas:
nenhuma flag, var, item ou mapa novo, e apagar ou acrescentar objeto no fim da lista não é índice de
save. `valida_rom.py` com os 2.400 mapas declarados dentro da ROM. `valida_conectividade.py` com
**0 warps quebrados** e os mesmos **1.966 de 2.289** do HEAD. `valida_mapas_sinnoh.py` com
`'sprite': 0` e **0 mapas com problema**. `valida_warp_tile.py --piso 60` em **5.915 de 6.875
(86,0%)**, com Sinnoh em 97,7%, idêntico ao HEAD. `de_para_sprites_sinnoh.py --demo` com os nove
casos verdes, e o relatório dele na árvore final em **`mapas tocados: 0`**, que é a idempotência
medida. `dev_scripts/qa/roda_qa.py --demo` verde nas SEIS varreduras, rodado na árvore compartilhada.
Suíte **1.024 de 1.024, nenhum pulado e nenhum reprovado**, com os três casos novos dentro, e
**T11 3 de 3** na mesma passada (`--rom2 roms/pokemon-claude-2026-08-18.gba`, `--src2` na worktree
de `cf6786b2ae`): a save da build de 18/08 continua se comportando como a régua manda.

**Duas armadilhas de convivência custaram duas passadas inteiras da suíte, e ficam escritas.**
(1) Os caminhos de `.sav` dos casos são CRAVADOS no JSON e COMPARTILHADOS entre frentes
(`/tmp/claude-501/frenteA/...`), então quatro suítes rodando ao mesmo tempo escrevem no mesmo
arquivo e o veredito vira sorteio. A suíta desta frente rodou com a pasta própria
(`SAV_BASE=/tmp/claude-501/sprites-sav`, e a mesma ideia para os PNG com `SAIDA_TESTES`), num
ajuste LOCAL da worktree que NÃO foi commitado; transformar isso em opção de verdade do
`testa_critico.py` é dívida aberta. (2) Sob contenção pesada de CPU o T94.1 abriu VERMELHO uma
vez e passou sozinho na sequência: roteiro de dezoito apertos com menu de sim/não não sobrevive a
quatro emuladores disputando a máquina.

**A completude de objetos de Sinnoh CAIU, de 100,3% para 99,4%, e isso é o conserto aparecendo na
régua, não uma perda.** A régua divide pelo que a fonte tem: os 38 corpos que saíram eram cópias que
a fonte NÃO tem, e estavam inflando o número acima de 100%. Entraram 20 pessoas de verdade no lugar,
e o que falta para fechar são **21 objetos em 11 mapas, nenhum deles desta frente**: dez em
Pokécenters (frente vizinha), três na rua de Eterna, dois no `Restaurant`, e um em cada de
`IronIsland`, `PastoriaCity`, `VeilstoneStore1F`, `OreburghCity_PokemonCenter_1F` e no próprio
`ContestHallLobby`. No HEAD desta rodada o mesmo importador já queria **25 objetos em 14 mapas**, ou
seja a fila encolheu; ela é de rodada de completude, e não desta.

#### O que fica aberto no elenco de Sinnoh

1. **Os 21 objetos acima.** `importa_npcs_sinnoh.py --aplicar` escreve `map.json` de Pokécenter, e
   isso PRECISA ser combinado com a frente dos Pokécenters antes de rodar: parte do que ele quer pôr
   lá são `OBJ_EVENT_GFX_VAR_A` e `VAR_B`, que são sprite de espaço reservado.
2. **A fala.** Os corpos que entraram são MUDOS, e o `ContestHallLobby` tem três
   `ContestHallLobby_EventScript_Npc1/2/3` órfãos, sem objeto que aponte para eles. São parte das 94
   falas órfãs de Sinnoh em 45 mapas, e casá-las pede o índice de script da fonte.
3. **A trava de escrita de Pokécenter em `de_para_sprites_sinnoh.py` é temporária**, e existe só
   porque duas frentes escreviam nos mesmos arquivos nesta rodada. Quem retomar pode tirá-la e rodar
   a ferramenta em Sinnoh inteira de uma vez.

### O defeito dos prédios que Hoenn e Johto dividem: entrar por Johto e sair na Rota 111, 06/09/2026

Relato do Gui: "entrei em Trainer Hill por Olivine City (Johto) e quando fui sair, saí na Rota 111, em
Hoenn". Medido antes de tocar: a praça `TrainerHill_Courtyard`, que é a praça de instalações que o
demake de HGSS põe ao norte da Route 40 (ligada a ela pela conexão e pelo
`MAP_GATE_ROUTE40_TRAINER_HILL_COURTYARD`) e que o item **F5 da 0.j** completou com a porta para a
Battle Frontier, tem cinco warps, e **quatro deles
entram em prédios COMPARTILHADOS com Hoenn**: `MAP_TRAINER_HILL_ENTRANCE` em (12,10) e os três lobbies
de Battle Tent, `FALLARBOR` em (27,19), `VERDANTURF` em (20,28) e `SLATEPORT` em (34,28). A saída dos
quatro era warp FIXO de Hoenn (`TrainerHill_Entrance` (9,16) e (10,16) para `MAP_ROUTE111` warp 4, e
cada lobby para a sua cidade), então **o mesmo defeito acontecia quatro vezes, e não uma**. O quinto
warp, (24,29) para o `BattleFrontier_OutsideWest` warp 11, foi conferido e está CERTO: os dois lados
são recíprocos e a volta é a seta ao sul, que o T126.3 já mede desde 21/08.

#### O mecanismo: o retorno é o `dynamicWarp`, e quem o grava é o motor

Nenhum mapa foi copiado e nenhum bit de save foi gasto. A saída dos quatro prédios virou
`MAP_DYNAMIC` / `WARP_ID_DYNAMIC`, que é o mesmo idioma dos elevadores e do `InsideOfTruck`, e quem
preenche o destino é o próprio motor: em `SetupWarp`
(`src/field_control_avatar.c:1131`), quando o warp em que o jogador vai POUSAR é dinâmico, ele chama
`SetDynamicWarp` com o mapa e o ÍNDICE do warp de onde o jogador veio. Ou seja, entrar já grava por
onde sair, com a mesma animação de porta e o mesmo tile de chegada de antes, porque o retorno guarda
`warpId` e não coordenada crua. `dynamicWarp` já existe no `SaveBlock1` desde o Emerald: **custo de
save ZERO**.

O que o motor NÃO faz é repor esse retorno depois que outra coisa reescreve o `dynamicWarp`, e dentro
das tendas isso acontece sempre: `InitFallarborTentChallenge` e as duas irmãs (`src/battle_tent.c:115,
178, 234`) apontam o `dynamicWarp` para o PRÓPRIO lobby, porque é dele que `SaveGameFrontier`
(`src/frontier_util.c:2534`) tira o ponto de "Continuar" de quem salva no meio do desafio. Sem
reposição, ao voltar da sala de batalha a porta do lobby devolveria o jogador para dentro do lobby, e
ele não sairia nunca mais. Por isso os quatro mapas de entrada ganharam `MAP_SCRIPT_ON_TRANSITION`
chamando o special novo `DefinirRetornoPredioCompartilhado` (`src/field_specials.c`), que **repõe o
retorno a partir do `escapeWarp`** quando ele aponta para mapa fechado. O `escapeWarp` é o registro
que o próprio motor faz da última entrada de mapa aberto para mapa fechado (`UpdateEscapeWarp`,
`src/overworld.c:774`): ele guarda o mapa de fora e o tile uma linha abaixo da porta, e nenhum passo
dado dentro do prédio o altera, porque lobby, corredor e sala de batalha são todos fechados.

Conferido e sem volta fixa para Hoenn em lugar nenhum: as saídas por elevador, derrota e desistência
do Trainer Hill (`data/scripts/trainer_hill.inc:40,52` e `TrainerHill_Elevator/scripts.inc:37`) voltam
todas ao `Entrance`, cuja porta é a dinâmica; as salas de batalha das três tendas voltam ao LOBBY, não
à cidade; e nenhum `HEAL_LOCATION` nem `setrespawn` aponta para esses prédios (a enfermeira do Trainer
Hill cura e não marca respawn).

#### A prova é do emulador, e o par negativo é a outra porta

`dev_scripts/testes_criticos/171_predios_compartilhados.json`, **10 casos, 10 verdes**, todos lendo
mapa e posição do `SaveBlock1`. **T171.1**: entra no Trainer Hill pela praça de Johto e sai em
`MAP_TRAINER_HILL_COURTYARD` (12,11). **T171.2**, o par negativo, é o MESMO prédio com o MESMO
roteiro entrando pela Route 111: sai em `MAP_ROUTE111` (31,114), que é a regressão zero de Hoenn.
**T171.3**: entra por Johto, vai ao `TRAINER_HILL_1F`, volta ao `Entrance` e só então sai; cai na
praça, o que prova que o retorno atravessa os andares de dentro. **T171.4**: o mesmo caminho menos os
últimos passos, o jogador entra e FICA no capacho (9,16), o que separa "a porta funciona" de
"qualquer tile devolve para a praça". **T171.5 a T171.8** fecham as três tendas: Verdanturf pela
praça (20,29) e por Verdanturf Town (3,8), Fallarbor pela praça (27,20) e Slateport pela praça
(34,29).

E os PNGs foram abertos, porque memória não desenha tela. No último quadro do T171.1 o jogador está de
pé embaixo do portal escuro do Trainer Hill, entre os dois postes acesos da praça, com o mato fechado
à esquerda e o paredão à direita; no do T171.2, o MESMO prédio, o cenário é a rocha roxa da Route 111,
sem poste nenhum. O T171.3 termina com o quadro idêntico ao do T171.1. No T171.5 o jogador está
embaixo da cúpula da Battle Tent com a fileira de postes e a grade d'água da praça atrás; no T171.6, a
MESMA cúpula, mas cercada pelo capim e pela cerca de Verdanturf Town, com dois NPCs da cidade. Dois
mapas diferentes, o mesmo prédio, a mesma porta.

O par **T171.9 e T171.10** é o adversarial, e existe porque os oito primeiros exercitam só o
automático do motor: se o special fosse um `return` vazio, os oito passariam igual. Quem suja o
`dynamicWarp` no jogo é o desafio da tenda, que este harness não joga até o fim, então o par usa um
sujador equivalente e alcançável, o **elevador da loja de Lilycove**, cujo
`setdynamicwarp MAP_LILYCOVE_CITY_DEPARTMENT_STORE_5F, 2, 1`
(`LilycoveCity_DepartmentStoreElevator/scripts.inc:98`) aponta o retorno para um mapa FECHADO do outro
lado do mundo. O **T171.9** é o controle: depois do elevador, sair pela porta dele cai mesmo em
`MAP_LILYCOVE_CITY_DEPARTMENT_STORE_5F` (2,2), ou seja o retorno está sujo de verdade. O **T171.10**
carrega esse mesmo estado para dentro do lobby da tenda e sai pela porta: cai na praça de Johto em
(20,29), e não na loja. Sem a reposição, ele cairia na loja.

#### O que fica aberto nos prédios compartilhados

- **Duas funções com a MESMA regra nasceram na mesma rodada, e viraram UMA no mesmo dia.** A frente
  das lojas compartilhadas de Sinnoh (Veilstone e Oreburgh, que reaproveitam a loja e o museu de
  Lilycove) tinha escrito `DefinirSaidaPelaPortaDeEntrada` em `src/retorno_dinamico.c`, com este corpo
  byte a byte. Ficou o `DefinirRetornoPredioCompartilhado` daqui, a loja e o museu passaram a chamar
  ele, e o arquivo duplicado foi apagado; a dívida está FECHADA, e a prova é este T171 continuar
  **10 de 10** com os seis prédios servidos pela mesma função (subseção da auditoria de warps).
- **O "Continuar" de quem salva no meio de um desafio de tenda muda de tile.** Depois que o
  `ON_TRANSITION` repõe o retorno, um `tent_save` feito DENTRO do lobby grava o ponto de continuação
  fora da tenda, e não no lobby como no Emerald original. O jogador reaparece na praça (ou na cidade)
  em frente à porta, com o desafio ainda pausado, e retoma entrando de novo. É diferença de tile, não
  de estado: nada trava e nada se perde.
- **O letreiro e o mapa da região continuam dizendo Hoenn dentro desses quatro prédios**, porque o
  `region_map_section` deles é o de Hoenn e é ele que essas telas leem. Quem entra pela praça de Johto
  vê "FALLARBOR TOWN" no lobby da tenda da esquerda. É dado de mapa, não deste mecanismo.

#### Os portões da frente dos prédios compartilhados

Build verde numa worktree ISOLADA (`/private/tmp/claude-501/predios`, HEAD `fccccc0265` mais só este
conserto), porque a árvore compartilhada estava com outra frente no meio de uma obra e não linkava.
**ROM 32.360.292 B, 96,44% de 32 MB**, ou seja **+64 B** sobre os 32.360.228 B que a frente da música
mediu neste mesmo HEAD, e é esse o custo inteiro do conserto; **EWRAM 86,16% e IWRAM 86,68%**,
idênticos aos da 0.t e da 0.u. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400
mapas, 2.252 ids de treinador e 1.716 apelidos conferidos: nenhuma flag, var, item, mapa ou índice
novo. `valida_rom.py` com os 2.400 mapas declarados dentro da ROM. `valida_conectividade.py` com **0
warps quebrados** e os mesmos 4 / 12 / 1.966 de 2.289 que a MESMA ferramenta dá na árvore SEM o
conserto (medido numa worktree de `b7ef40f330`, o HEAD de antes da rodada): o campo
`destinos_dinamicos` dos quatro `map.json` mantém o grafo de alcance honesto, já que a ferramenta pula
`MAP_DYNAMIC` de propósito. `valida_warp_tile.py --piso 60` em 5.915 de 6.875 (86,0%), idêntico à
0.t. `guarda_colisao_vars` com 23 colisões herdadas, 0 novas e 0 stub. `dev_scripts/qa/roda_qa.py
--demo` verde nas quatro varreduras. **Suíte 1.010 de 1.011, ZERO reprovado**, com o T11.3 pulado na
varredura, e **T11 3/3 à parte** contra `roms/pokemon-claude-2026-08-18.gba` (worktree de `cf6786b2ae`
em `/private/tmp/claude-501/t11-r13`), a mesma dupla que a 0.u usou.

### A meia porta da igreja de Hearthome, e o retrato das 44 portas fechadas do corte, 06/09/2026

O Gui trouxe do capítulo "before Fantina": **"não está entrando no castelo bonito na esquerda, um
building"**. É a igreja de Hearthome, o `ForeignBuilding`, e o mapa dela **nunca foi cortado**: tem 9
objetos, as 9 falas do Platinum já em inglês e dois warps de volta. O que estava quebrado era
**metade da porta**.

`LAYOUT_HEARTHOME_CITY` desenha a porta da igreja em DUAS células, (8,6) e (9,6), as duas com o mesmo
metatile 484 e `MB_NORTH_ARROW_WARP`, e na fonte cada metade levava a um lugar DIFERENTE: (9,6) ao
`ForeignBuilding`, vivo, e (8,6) ao portão oeste da Amity Square, que o Gui cortou. O corte de
22/08/2026 (`721c77fb63`) fechou só a metade cortada, e sobrou meia porta: quem encostasse pela
coluna da esquerda apertava para cima e **nada acontecia**, e ainda lia uma placa de obras **em
português** pregada na porta da igreja. A porta da NORTHEAST HOUSE, em (50,6)/(51,6) do outro lado da
mesma cidade, tinha exatamente o mesmo defeito. **São as duas únicas do jogo**, e a varredura abaixo
é o que prova isso.

### O retrato das 44: são 22 mapas, 26 portas e 24 túmulos

`grep -rl EventScript_PortaFechada data/maps/` dá **44 ARQUIVOS**, que são **22 mapas** (`map.json` e
`scripts.inc` de cada um) e **22 placas**. As portas fechadas são **26**: 24 lápides (a entrada de
warp fica no índice, repete a coordenada do doador e guarda a porta velha em `porta_original`) e 2
warps apagados nas duas salas de link de Unova, que não têm doador. Destino por destino, com o
`region_map_section`, a contagem de eventos e a lista `CORTES_DO_GUI` na mão:

| mapa vivo | warp | célula da porta | destino | veredito |
|---|---|---|---|---|
| HearthomeCity | 7 | (8,6) | FOREIGN_BUILDING (era WEST_GATE_TO_AMITY_SQUARE) | **REABERTA, gêmea viva** |
| HearthomeCity | 8 | (51,6) | HEARTHOME_CITY_NORTHEAST_HOUSE_1F (era EAST_GATE_TO_AMITY_SQUARE) | **REABERTA, gêmea viva** |
| CanalaveCityPokecenter1F | 2 | (1,6) | CANALAVE_CITY_POKECENTER_2F | túmulo, fica fechada |
| CelesticTownPokecenter1F | 2 | (1,6) | CELESTIC_TOWN_POKECENTER_2F | túmulo, fica fechada |
| EternaCityPokecenter1F | 2 | (1,6) | ETERNA_CITY_POKECENTER_2F | túmulo, fica fechada |
| HearthomeCityPokecenter1F | 2 | (1,6) | HEARTHOME_CITY_POKECENTER_2F | túmulo, fica fechada |
| PastoriaCityPokecenter1F | 2 | (1,6) | PASTORIA_CITY_POKECENTER_2F | túmulo, fica fechada |
| PokemonLeagueNorthPokecenter1F | 2 | (1,6) | POKEMON_LEAGUE_NORTH_POKECENTER_2F | túmulo, fica fechada |
| PokemonLeagueSouthPokecenter1F | 2 | (1,6) | POKEMON_LEAGUE_SOUTH_POKECENTER_2F | túmulo, fica fechada |
| SnowpointCityPokecenter1F | 2 | (1,6) | SNOWPOINT_CITY_POKECENTER_2F | túmulo, fica fechada |
| SolaceonTownPokecenter1F | 2 | (1,6) | SOLACEON_TOWN_POKECENTER_2F | túmulo, fica fechada |
| SunyshoreCityPokecenter1F | 2 | (1,6) | SUNYSHORE_CITY_POKECENTER_2F | túmulo, fica fechada |
| VeilstoneCityPokecenter1F | 2 | (1,6) | VEILSTONE_CITY_POKECENTER_2F | túmulo, fica fechada |
| PokemonLeagueNorthPokecenter1F | 4 | (12,1) | POKEMON_LEAGUE_ELEVATOR_TO_AARON_ROOM | túmulo, fica fechada |
| ContestHallLobby | 2 | (6,1) | CONTEST_HALL_STAGE_NO_CONTEST | túmulo, fica fechada |
| JubilifeCity | 6 | (20,13) | JUBILIFE_CITY_POKETCH_COMPANY_F1 | túmulo, fica fechada |
| JubilifeCity | 7 | (17,13) | JUBILIFE_CITY_POKETCH_COMPANY_F1 | túmulo, fica fechada |
| JubilifeCity | 10 | (42,25) | GLOBAL_TERMINAL_1F | túmulo, fica fechada |
| PastoriaCityObservatoryGate1F | 2 | (2,1) | GREAT_MARSH_6 | túmulo, fica fechada |
| Route212_North | 2 | (6,50) | POKEMON_MANSION | túmulo, fica fechada |
| Route214 | 5 | (16,2) | SENDOFF_SPRING | túmulo, fica fechada |
| Route221 | 1 | (82,15) | PAL_PARK_LOBBY | túmulo, fica fechada |
| VeilstoneCity | 10 | (31,47) | GAME_CORNER | túmulo, fica fechada |
| Unova_CasteliaCitySouth | 9 | (12,7) | UNOVA_CASTELIA_PLAZA_LOBBY | túmulo, fica fechada |
| Unova_MobileTradeRoom | apagado | (4,7) | UNOVA_POKECENTER_2F | túmulo, fica fechada |
| Unova_MobileBattleRoom | apagado | (4,7) | UNOVA_POKECENTER_2F | túmulo, fica fechada |

**Os 24 destinos de lápide são túmulo de verdade**, os 24: `MAPSEC_NONE`, 0 objetos, 0 warps, 0
`bg_events`, 0 `.string` no `scripts.inc`, e os 24 estão em `CORTES_DO_GUI` no modo `deficit`.
**Nenhum aponta para mapa vivo**, e o `ForeignBuilding` nunca esteve entre eles: a placa que o Gui leu
na porta dele era a do portão da Amity Square, plantada na célula (8,5) porque o gerador procura a
parede vizinha da porta que fechou e a parede vizinha, ali, é o desenho da porta da igreja.

### O conserto é regra no gerador, e não remendo nos dois mapas

`dev_scripts/remove_mapas_cortados.py` ganhou `gemea_viva()`: antes de virar lápide, o warp pergunta
se a célula VIZINHA (quatro direções) tem o MESMO metatile e um warp VIVO em cima. Se tem, as duas
são metades da mesma porta, e a metade cortada **adota o destino da gêmea** em vez de fechar. Mapa em
que todas as portas foram adotadas não recebe placa nenhuma. Rodar o gerador de novo dá **0 portas a
fechar**, e o `--demo` ganhou o caso 7, que replanta em HearthomeCity o warp cortado de (8,6) e cobra
que `gemea_viva` ache o vizinho, mais a contraprova de que porta solta não casa com ninguém.

**A placa passou a falar inglês, e é UMA SÓ.** As 22 cópias de `"Fechado. Área em obras."` (a única
fala em português que sobrava no jogo, e o Gui a encontrou justamente na porta da igreja) viraram
`Common_Text_PortaFechada` em `data/scripts/portas_fechadas.inc`, incluído no `data/event_scripts.s`
logo depois do `sinnoh_placas.inc`: **"Closed for renovations."**, 123 px dos 208 da caixa, medidos com
`gFontNormalLatinGlyphWidths`. O rótulo de cada mapa continua onde estava, só apontando para lá, e por
isso nenhum `map.json` de Pokécenter precisou ser tocado. O `--demo` do gerador cobra as três coisas:
que o arquivo compartilhado tem exatamente o texto da constante, que o texto é ASCII, e que nenhum
mapa guardou cópia própria. A ROM ENCOLHEU 524 B com isso.

### A prova está no framebuffer, e tem contraprova de ROM

Cinco casos novos no bloco que já era o dono do assunto, `140_portas_fechadas.json` (T140.7 a
T140.11), todos com PNG aberto e olhado: o jogador nasce EM CIMA de (8,6), a metade esquerda, sobe e
**entra na igreja**; o par negativo desce em vez de subir e continua em Hearthome, em (8,9), porque
`MB_NORTH_ARROW_WARP` só dispara olhando para o norte; a metade direita (warp 12) continua abrindo o
mesmo prédio; dentro da igreja o NINJA BOY de (2,8) fala ("When people and Pokémon join hands,
everyone's happy.") e a saída devolve o jogador em (9,6), **na frente da porta**; e o warp 8 abre a
NORTHEAST HOUSE. A placa em inglês é lida no T140.3, e o PNG mostra a caixa escrita
`Closed for renovations.`.

**A contraprova é de graça e é exata:** os MESMOS 11 casos rodados contra
`roms/pokemon-claude-2026-09-06.gba` dão **8 de 11**, e os três que caem são exatamente os três que
tocam os warps 7 e 8 (T140.7, T140.8 e T140.11). O T140.7 lá para em `MAP_HEARTHOME_CITY`, que é o
defeito do Gui reproduzido em laboratório.

### Os portões, e o que a régua fez

Build verde, **ROM 32.359.704 B (96,44% de 32 MB), 524 B a MENOS que a `0.u`**, EWRAM 86,16% e IWRAM
86,68%, idênticos. **SAVE COMPATIVEL** (nada aqui é índice: as duas entradas de warp ficaram no mesmo
lugar da lista e só trocaram de destino), `valida_rom.py` com os 2.400 mapas declarados dentro da ROM,
`valida_conectividade` com **0 warps quebrados**, `valida_warp_tile --piso 60` em 5.915 de 6.875
(86,0%), `roda_qa.py --demo` verde nas quatro varreduras e `remove_mapas_cortados.py --demo` verde.

Na régua, **uma coluna anda e é para baixo**: Sinnoh em placas vai de 103,5% para **103,4%**, porque a
placa de obras de HearthomeCity saiu e ela nunca existiu na fonte. As outras cinco colunas de Sinnoh e
as cinco regiões restantes ficam idênticas.

**Esta build foi feita em worktree isolada** (`/private/tmp/claude-501/portas-q`, HEAD `fccccc0265`
mais só os arquivos desta frente), e não na árvore principal, porque às 02:37 a árvore principal
**não linkava**: `data/maps/GoldenrodCity_DepartmentStoreElevator/scripts.inc`, trabalho não commitado
de outra frente, cita `Common_Movement_WalkUp1` e `Common_Movement_WalkDown1`, que não existem. O lock
de build foi tomado, o defeito foi medido e o lock foi devolvido em seguida, para não prender a frente
que precisa consertá-lo.

### O fechamento da frente, reconferido no HEAD de encerramento, 06/09/2026

Continuação depois de o executor anterior morrer por cota às 06h40, com a bateria de provas pela
metade. **Zero linha de código nova aqui:** o conserto já estava commitado em `95759c9b4f`, e o texto
acima entrou no repositório de carona no `bfe2b35a71`, de OUTRA frente, que passou um `git add` por
cima da árvore compartilhada. O que faltava era reconferir o veredito sem acreditar na mensagem de
commit, rodar a bateria no HEAD de encerramento e gravar a ROM.

O veredito das 26 portas foi refeito do zero, e fecha, por três varreduras que não dependem uma da
outra:

1. **Nenhum warp de mapa vivo leva a túmulo, no jogo inteiro.** Varredura dos 2.404 `map.json`:
   **111 túmulos** (0 objeto, 0 warp, 0 placa e `MAPSEC_NONE`) e **0 warps** apontando para eles a
   partir dos mapas vivos. É a prova de completude que a tabela sozinha não dá: porta fechada que
   sobrou no lugar errado, ou porta aberta para o vazio, apareceria aqui, e não aparece.
2. **Os 24 warps que o corte alterou são exatamente as 24 lápides da tabela.** Cada `map.json` foi
   comparado entrada por entrada com a versão de `721c77fb63^`, e cada destino ORIGINAL foi relido:
   os 21 destinos distintos têm 0 evento e `MAPSEC_NONE`, e os 21 estão em `CORTES_DO_GUI` no modo
   `deficit`. Nenhum interior vivo ficou atrás de placa.
3. **O caso que PARECIA contraexemplo, e não é.** O warp 4 de `PokemonLeagueNorthPokecenter1F` fechou
   a porta do `POKEMON_LEAGUE_ELEVATOR_TO_AARON_ROOM`, e a Elite dos Quatro de Sinnoh está VIVA:
   `SinnohLeague_AaronsRoom` e as cinco irmãs, com 10 objetos e os warps entre elas. Interior vivo
   atrás de porta fechada é exatamente o critério de REABRIR, então ele foi aberto e medido. Não é o
   caso, por dois motivos: o mapa do elevador tinha UM warp só ANTES do corte, e ele voltava para o
   próprio Pokécenter, ou seja o elevador nunca levou a lugar nenhum; e a entrada da Elite não é
   `warp_event` nenhum, é `warp MAP_SINNOH_LEAGUE_AARONS_ROOM, 0` de SCRIPT
   (`data/maps/SinnohLeague_Entrance/scripts.inc:61`), que varredura de warp não enxerga. Reabrir
   teria criado um atalho que a fonte não tem. Ela fica fechada, e a lição vira regra: **mapa sem
   `warp_event` de entrada não é mapa órfão até o `grep` no `scripts.inc` dizer que é.**

Bateria buildada na worktree isolada `/private/tmp/claude-501/portas-q`, no HEAD `7b9a11ce64`, e não
na árvore principal, que tem seis frentes escrevendo ao mesmo tempo. **ROM 32.370.104 B, 96,47% de
32 MB**, EWRAM 86,16% e IWRAM 86,68%. Os 10.400 B a mais sobre os 32.359.704 B medidos por esta
frente vêm das outras cinco que entraram no HEAD depois dela, e não daqui: esta continuação não tocou
uma linha de código. Os três commits que entraram DEPOIS de `7b9a11ce64` enquanto a bateria rodava
(`7a6e430d8a`, `b58dcbad7f` e `5f3a4cb403`) mexem só no `ESTADO.md` e em três `.json` de caso de
teste, nada que o compilador leia, então a ROM gravada continua sendo a do topo.

**Suíte 1.021 de 1.021**, rodada BLOCO A BLOCO, com o placar em disco, porque o processo único de uma
hora foi MORTO duas vezes por volta dos 40 minutos, com sinal 15, enquanto seis frentes rodavam suíte
na mesma máquina; retomar de onde parou custou nada, e o driver é descartável, fora do repositório. O
único caso que não fica verde na varredura por bloco é o **T11.3**, que sem `--rom2` é PULADO por
desenho e nunca contado como passou; rodado à parte com as duas ROMs, **T11 fecha 3 de 3** contra
`roms/pokemon-claude-2026-08-18.gba`, com a fonte velha em `/private/tmp/claude-501/t11-r13`, e a save
de layout velho continua sendo RECUSADA de propósito pela ROM nova, que é o que a janela de save
fechada manda.

**O bloco desta frente é o `140_portas_fechadas.json`, e ele fecha 11 de 11 nesta build.** A porta
fechada não warpa (T140.1) e o vizinho vivo do MESMO mapa continua warpando índice por índice (T140.2,
T140.5 e T140.6); a placa se lê, e a caixa que aparece no framebuffer diz `Closed for renovations.`
(T140.3), com o par negativo que percorre a mesma rota sem apertar o A (T140.4); e as portas reabertas
ENTRAM, com TRÊS travessias de verdade: T140.7 na metade esquerda da igreja, T140.9 na metade direita
que sempre funcionou, e T140.11 na porta da NORTHEAST HOUSE. O par negativo de direção é o T140.8
(`MB_NORTH_ARROW_WARP` só dispara olhando para o norte) e a volta inteira é o T140.10, em que o NINJA
BOY fala dentro da igreja e a saída devolve o jogador em (9,6), na frente da porta. Vale dizer com
todas as letras: **portas REABERTAS por esta frente existem DUAS no jogo inteiro, e não três**, porque
só duas tinham interior vivo. A terceira travessia é a gêmea que já funcionava, e ela está no roteiro
justamente para provar que a reabertura não roubou a porta boa.

`guarda_save.py`: **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas, 2.252
ids de treinador e 1.717 apelidos. `valida_rom.py`: os 2.400 mapas declarados entraram na ROM.
`valida_conectividade.py`: **0 warps quebrados**, 1.966 de 2.289 mapas vivos alcançados, com os 111
túmulos fora da conta. `valida_warp_tile.py`: **5.915 de 6.875 (86,0%)**, idêntico. `roda_qa.py
--demo` verde nas cinco varreduras do HEAD, e `remove_mapas_cortados.py --demo` verde.
`completude.py`: as seis regiões com **100,0% de mapas e de warps**, Sinnoh em 103,4% de placas,
nenhuma coluna caiu.

ROM em `roms/pokemon-claude-2026-09-06q.gba`, com o `.map` ao lado, md5
`6db3c8c539941362030ed4d2b9fa5966`.

#### Uma correção na tabela acima, e um resto que fica

As duas linhas de Unova estavam imprecisas, e foram corrigidas. `Unova_MobileTradeRoom` e
`Unova_MobileBattleRoom` não são o túmulo: o túmulo é o destino delas, `UNOVA_POKECENTER_2F`, e por
não haver doador de coordenada o gerador APAGOU os dois warps de cada uma em vez de virá-los lápide.
Elas próprias são mapas cortados que **nenhum caminho alcança** (o `valida_conectividade.py` as lista
entre os inalcançáveis), e são os ÚNICOS dois dos 113 cortados que não viraram túmulo: o
`esvazia_mapa()` limpou as duas, e a passada de fechar portas, que roda depois, replantou uma placa
dentro delas. É placa que ninguém pode ler, dentro de mapa em que ninguém pode entrar, a 0,3 KB cada.
Não foi mexido porque mexer é escrever em mapa cortado por ganho zero de jogo; a regra para o gerador,
se alguém voltar aqui, é **não plantar placa em mapa que está na lista de cortados**.

#### Uma lição de convivência, e ela custou um susto

Script auxiliar de sessão NÃO vai para `/private/tmp/claude-501/` com nome genérico. Esta frente
escreveu `patch_estado.py` ali, e meia hora depois OUTRA frente escreveu um `patch_estado.py` dela por
cima, com assinatura de argumentos diferente. A chamada morreu com `File name too long` em vez de
aplicar a edição errada no `ESTADO.md`, e foi sorte, não desenho: o mesmo acidente com scripts de
assinatura parecida edita o arquivo de outra frente sem avisar. Ferramenta descartável mora na pasta
de scratchpad da sessão, que já é única por definição.

### O que fica aberto nas 44 portas fechadas

- **Cinco meias portas do MESMO tipo, fora do corte**, achadas pela varredura de célula gêmea com
  comportamento de porta e sem warp: `FloaromaTown` (4,2)/(5,2), `MtSilver_2F` (25,36)/(26,36),
  `Galar_WarmUpTunnel01` (40,37)/(39,37) e `Galar_SlumberingWeald02` em (17,13) e (17,14). Não são
  obra do corte, são da importação de cada fonte. **FECHADAS em `cfa0d30bd4`, depois do fechamento da
  rodada**: três ganharam o warp gêmeo e a do Weald não era meia porta; ver a seção seguinte. As outras
  8 que a varredura levanta são falso positivo conhecido (o chão furado do ginásio de Ecruteak,
  `MB_MT_PYRE_HOLE`, e duas pontes `MB_BRIDGE_OVER_OCEAN`).
- **Galar ainda fala português em 310 textos de jogo** (mais 58 sem acento), medido por
  `dev_scripts/qa/checa_texto.py`. Nada disso é placa de porta fechada, e nada disso entrou nesta
  frente: é dado de Galar, e o censo de idioma da ferramenta ainda diz o contrário do que o projeto
  decidiu (ela classifica texto em inglês em Sinnoh, Unova e Galar como achado).

### As cinco meias portas fora do corte: três ganham o warp gêmeo, e o Slumbering Weald não é meia porta, 06/09/2026 (depois do fechamento da rodada 13)

Frente única, executada depois do placar acima, e por isso **a ROM consolidada
`roms/pokemon-claude-2026-09-07.gba` NÃO tem este conserto**: quem consolidar a próxima leva junto.
Mesma classe do defeito da igreja de Hearthome: célula gêmea com o mesmo metatile e o mesmo
comportamento de porta do vizinho que tem warp, e sem warp nenhum em cima. As cinco vieram assim da
importação de cada fonte, e nenhuma passou pelo `remove_mapas_cortados.py`.

**Medido no blockdata antes de tocar**, célula a célula, com a tabela de atributos do
`valida_warp_tile.py` (metatile, colisão e comportamento da célula viva, da gêmea e das quatro vizinhas):

| mapa | viva | gêmea | metatile | comportamento | o que cerca a gêmea | veredito |
|---|---|---|---|---|---|---|
| `FloaromaTown` | (4,2), warp 5 | (5,2) | 539 | `MB_NORTH_ARROW_WARP` | parede em (3,2), (6,2) e (5,1) | **meia porta, warp 6 acrescentado** |
| `MtSilver_2F` | (25,36), warp 0 | (26,36) | 647 | `MB_SOUTH_ARROW_WARP` | parede em (27,36) e (26,37), chão em (24,36) | **meia porta, warp 7 acrescentado** |
| `Galar_WarmUpTunnel01` | (40,37), warp 1 | (39,37) | 647 | `MB_SOUTH_ARROW_WARP` | chão dos dois lados, (39,38) sólido | **meia porta, warp 2 acrescentado** |
| `Galar_SlumberingWeald02` | (17,13) e (17,14), warps 1 e 2 | (18,13) e (18,14) | 799 | `MB_WEST_ARROW_WARP` | faixa de TRÊS colunas, (17..19, 13..14) | **não é meia porta, fica como está** |

**O Weald é falso positivo da varredura, e o motivo é geometria.** Nas outras quatro (e nas duas de
Hearthome) a gêmea fica lado a lado, PERPENDICULAR à seta: quem está nela aperta a direção da seta
contra parede e fica. No Weald a seta aponta para oeste, AO LONGO da faixa: quem está em (18,y) ou
(19,y) e aperta para a esquerda simplesmente anda até (17,y), onde o warp existe, e o aperto seguinte
dispara (`TryArrowWarp` só olha a célula do jogador). A varredura de célula gêmea não distingue os
dois casos; quem a rodar de novo vai ver o Weald outra vez, e a resposta é esta.

**O conserto é um warp a mais no FIM de `warp_events`** de cada um dos três mapas (append, nunca
inserção, porque `dest_warp_id` é índice e a save do Gui está congelada), repetindo destino e
`dest_warp_id` do gêmeo vivo e marcado com a chave `gemea`, como em Hearthome. Nenhum índice se move:
`guarda_save.py` diz **SAVE COMPATIVEL**. `valida_warp_tile.py` vai de 6.874 para **6.877** warps
conferidos e de 5.918 para **5.921** que disparam, medido no HEAD limpo em worktree e na árvore
alterada: exatamente os três.

**A prova está no framebuffer, e a contraprova é exata.** Bloco novo
`dev_scripts/testes_criticos/181_meias_portas.json`, **12 casos, 12 verdes** na ROM nova, PNG do quadro
final aberto e olhado (o mato do Meadow, a sala da cachoeira do Mt. Silver, a grama da Isle of Armor).
Para cada porta: o jogador nasce no warp vivo, dá um passo lateral para a gêmea e aperta a seta
(T181.1, T181.4, T181.7); o par negativo aperta o sentido contrário e a POSIÇÃO final prova que o passo
lateral aconteceu (T181.2, T181.5, T181.8); e a metade viva continua abrindo o mesmo lugar (T181.3,
T181.6, T181.9). No Weald, T181.10 anda até o fundo da faixa e para em (19,13), e T181.11 e T181.12
atravessam a faixa inteira de volta e saem pelo warp de sempre. Os mesmos 12 casos contra a ROM
consolidada (`c0ea203b`) dão **9 de 12, e os três que caem são exatamente as três portas consertadas**,
parando no mapa de origem.

**A regra de roteiro que o par negativo ensinou, e que fica escrita nos casos.** A primeira versão dos
roteiros supunha que um toque de 20 quadros é um passo. O par negativo caiu na ROM anterior e denunciou:
o positivo estava passando SEM sair da célula viva. Medido: quem nasce num warp de seta olha CONTRA a
seta (`GetAdjustedInitialDirection`: seta norte, olha sul; seta sul, olha norte; seta oeste, olha
leste); um toque de 20 quadros só VIRA o jogador quando ele não olha naquela direção, e o seguinte é
que anda; e a seta dispara pelo dpad, sem depender de para onde ele olha. Por isso os roteiros têm dois
toques laterais (vira, anda), e o do Warm-Up Tunnel tem exatamente dois, porque (38,37) é chão e um
terceiro passaria da porta.

**Os portões.** Build verde com o lock envolvendo só o `make` (ROM md5 `496c4a8edb`), `T140` **11 de
11** (a classe inteira, Hearthome incluída), `valida_rom.py` com os 2.400 mapas na ROM,
`valida_conectividade.py` com **0 warps quebrados**, `valida_warp_tile --piso 60` verde (Sinnoh 98,1%,
Unova 100,0%), `roda_qa.py --demo` verde nas seis varreduras, `remove_mapas_cortados.py --demo` verde,
e `lente_warps --lista` e `lente_portas --lista` sem achado novo nos três mapas (os P2 que aparecem ali
são os de antes, calibrados). **A suíte inteira, bloco a bloco com placar em disco: 1.062 de 1.063,
com o T11.3 pulado** (precisa de `--rom2`) e **zero vermelho**, medida contando caso a caso contra os
`*.json` (1.063 casos nos arquivos, 1.063 rodados). Armadilha do laço bloco a bloco, para quem repetir:
`10_kanto.json`, `20_johto.json` e `30_hoenn_sinnoh.json` misturam prefixos (T2, T3, T5, T7, T8, T9),
e um laço que tira o prefixo do PRIMEIRO caso do arquivo pula 59 casos calado; a conferência caso a
caso é que pegou.

### As 31 portas de Johto ganham interior: quatro casas novas, quatro ligações que já estavam desenhadas dos dois lados, e 18 placas, 07/09/2026 (pergunta 46, depois do fechamento da rodada 13)

Frente única, executada depois do placar acima e depois das cinco meias portas, e por isso **a ROM
consolidada `roms/pokemon-claude-2026-09-07.gba` NÃO tem este conserto**. A ROM desta frente é
`roms/pokemon-claude-2026-09-07c.gba`, md5 `d8068a6489cabf67bacdf5e5223ae7c2`, com o `.map` do linker
ao lado, buildada LIMPA no commit `cb7dcb7505`, que é este conserto rebaseado em cima da poda das
cidades enfeitadas (`eefed261ca`).

A decisão do Gui foi: "as 31 ganham interior onde alguma fonte tiver; o que não tem em fonte nenhuma
ganha placa `closed` em inglês". Para responder isso foi preciso MEDIR cinco fontes de Johto, e o
resultado desmonta a premissa em dois pontos. **Três das 31 nunca foram porta morta**, e **as três
que o Gui deu como certas não são as três que a fonte tem**: a casa da trilha do sino tem fonte
(FireGold), a MooMoo Farm da fonte está na Route 39 e já está aberta aqui há tempo (a fazenda da
Route 38 é desenho NOSSO), e as bocas do Monte Prata em fonte nenhuma passam de UMA por lado.

**As cinco fontes, e o que cada uma respondeu.** `fontes-mapas/hns` (Pokémon Heart & Soul, que é a
fonte da nossa Johto), o decomp público do **GS Chronicles** (`G0LD/GS-Chronicles-Decomp`, clonado em
`fontes-mapas/romhacks/gs-chronicles/decomp/`, e que absorve os mapas do HnS: os `map.json` dele
chamam-se `*_hns` e batem com os nossos warp a warp), e as ROMs **Liquid Crystal**, **FireGold** e
**Scorched Silver**, lidas com o `gbamap.py`. Crédito no `CREDITS.md`. Duas descobertas de método que
valem para a próxima leitura de ROM: `liquid-crystal/` e `liquid-crystal-beta-3.3/` são o MESMO
arquivo (md5 `3e72e2d767ed9e689c48692f2f00de7a`), e o `enumera()` do `gbamap.py` SUBCONTA mapas (424
na Liquid Crystal contra 762 reais), porque a heurística de fim de banco e os filtros de clima e de
número de eventos derrubam header válido.

**A tabela das 31**, e a coluna "fonte" diz quem abre aquela porta lá:

| # | porta | família | o que ficou | fonte |
|---|---|---|---|---|
| 1 | `MtSilver_MountainSide` (27,18) | já entrava | nada muda; foi para a lista branca da lente | a nossa, medida |
| 2 | `MtSilver_MountainSide` (34,31) | já entrava | idem | a nossa, medida |
| 3 | `MtSilver_MountainSide` (41,40) | já entrava | idem | a nossa, medida |
| 4 | `Route34` (33,31) | ligação | warp 5 <-> `Route34_DayCare` warp 1, em (3,9) | Liquid Crystal, FireGold e Scorched Silver abrem as DUAS portas da creche |
| 5 | `Route45` (45,6) | ligação | warp 1 <-> `DarkCave_NorthSide` warp 2, em (35,3) | as duas pontas já desenhadas na nossa árvore |
| 6 | `Route46` (25,33) | ligação | warp 3 <-> `DarkCave_SouthSide` warp 3, em (64,4) | idem |
| 7 | `MtSilver_Outside` (34,7) | ligação | warp 2 <-> `MtSilver_1F_WaterfallRoom` warp 7, em (50,5) | idem |
| 8 | `BellchimeTrail` (54,58) | interior novo | `BellchimeTrail_House`, planta de `EcruteakCity_House1` | **FireGold 44.105**, a casinha do sábio na Bellchime Trail (9x8, 6 objetos); Liquid Crystal 2.46 tem o mesmo prédio ao lado da Tin Tower |
| 9 | `Route38` (34,41) | interior novo | `Route38_FarmHouse`, planta de `Route39_FarmHouse` | a casa da fazenda existe nas CINCO (hns/GSC `Route39_FarmHouse` 13x10, LC 1.28 13x10, FG 44.109 11x9, SS 17.0 12x9), sempre na Route 39 |
| 10 | `Route34` (23,50) | interior novo | `Route34_House1`, planta de `Route26_House1` | a casa de telhado azul existe no LC (4.7 e 4.9, 13x10) e na FG (45.56 e 45.57), nas duas na Route 26 |
| 11 | `EcruteakCity` (57,25) | interior novo | `EcruteakCity_House3`, planta de `EcruteakCity_House2` | a casa de Ecruteak 13x10 é do hns; a TERCEIRA é desenho nosso |
| 12 | `LakeOfRageLowTide` (15,4) | inalcançável | nada; o mapa inteiro está fora do grafo, e isso é da fonte | hns |
| 13 | `LakeOfRageLowTide` (39,41) | inalcançável | idem | hns |
| 14-19 | `OlivineCity` (2,15) (6,15) (10,15) (27,15) (31,15) (35,15) | placa | os seis galpões do porto | **nenhuma**: nas cinco o porto é cais mais terminal, e a fileira de galpões não tem warp |
| 20 | `EcruteakCity` (8,54) | placa | boca no penhasco sudoeste | **nenhuma** |
| 21 | `BlackthornCity` (39,18) | placa | boca no penhasco leste | **nenhuma** (no LC o penhasco leste tem duas bocas, mas as duas são Ice Path, que aqui já está ligada) |
| 22 | `BlackthornCity` (5,33) | placa | boca no penhasco oeste | **nenhuma**: as cinco têm zero boca no oeste |
| 23 | `IlexForest` (77,39) | placa | boca da floresta | **nenhuma** |
| 24 | `Route26` (2,20) | placa | boca da Route 26 | **nenhuma** (Tohjo Falls é da Route 27) |
| 25 | `Route26North` (21,8) | placa | boca da Route 26 norte | **nenhuma** |
| 26 | `Route34` (53,53) | placa | boca da Route 34 | **nenhuma** |
| 27 | `Route45` (1,7) | placa | boca oeste | **nenhuma**: as cinco têm UMA boca por rota, e ela é a Dark Cave |
| 28 | `Route45` (39,53) | placa | boca sul | **nenhuma** |
| 29 | `MtSilver_Outside` (14,3) | placa | boca norte | **nenhuma**: LC e FG têm UMA boca externa no Monte Prata |
| 30 | `MtSilver_Outside` (7,16) | placa | boca oeste | **nenhuma** |
| 31 | `MtSilver_MountainSide` (44,9) | placa | boca da encosta | **nenhuma** |

**As três que já entravam, e por que a lente as via.** A boca da encosta do Monte Prata é
`MB_NON_ANIMATED_DOOR` sólido, e a célula colada à direita é `MB_WEST_ARROW_WARP` com colisão 0 e COM
warp: (27,18) tem o warp 0 em (28,18), (34,31) o 1 em (35,31) e (41,40) o 2 em (42,40), os três para
`MT_SILVER_1F_WATERFALL_ROOM`. O jogador pisa na seta, aperta para oeste e o `TryArrowWarp`
(`src/field_control_avatar.c`) dispara. A lente não juntava as duas células no mesmo bloco porque o
comportamento delas é diferente, e `blocos()` só junta comportamento IGUAL: é o limite conhecido dela,
não defeito do jogo. As três entraram na `LISTA_BRANCA` com a medida, e o **T182.17** prova que se
entra e o **T182.18** prova que só para oeste.

**A armadilha que custou a primeira versão: ligar não bastava.** Escrito o primeiro par de warps, dos
8 novos só 2 disparavam, e o `valida_warp_tile` CAIU em vez de subir. A conta é do motor:
`MB_ANIMATED_DOOR` é a única família de porta que dispara SENDO SÓLIDA, porque o motor abre a porta de
prédio e atravessa; a boca de caverna, `MB_NON_ANIMATED_DOOR`, dispara quando o jogador PISA nela, e
com colisão 1 ele nunca pisa. O censo fecha o diagnóstico: das 93 células de `MB_NON_ANIMATED_DOOR`
com warp em Johto, as **87 que já existiam têm TODAS colisão 0**, e só as 6 recém-escritas tinham 1.
Então a boca decorativa é ABERTA no `map.bin`, e só nos dois campos que o motor lê: colisão 0 e
elevação 0. **O metatile não muda**, para o desenho continuar o mesmo (fora, o mesmo 169 da boca que
funciona; dentro, o mesmo 660 do arco). Elevação 0 é `ELEVATION_TRANSITION`, e
`IsElevationMismatchAt` (`src/event_object_movement.c`) devolve FALSE para ela sempre, o que resolve o
caso real das três bocas de fora, que recebem o jogador vindo de elevação 5 (Route 45), 4 (Monte
Prata) e 3 (Route 46). Seis palavras mudaram, e estão nomeadas no relatório do script:
`0x04A9 -> 0x00A9` nas três de fora e `0x0694 -> 0x0294` nas três de dentro.

**A ferramenta é `dev_scripts/abre_portas_johto.py`**, com tabela declarativa (uma linha por porta),
`--aplicar` e conferência que roda sempre: célula fora da grade, comportamento que não dispara, warp
duplicado no mesmo tile, falta de chão andável colado, e o par comportamento+colisão que nasceria
morto. Mapa novo entra em `gMapGroup_JohtoPortas`, grupo NOVO no fim de `group_order`, e todo warp
novo entra no FIM da lista do mapa que já existe: nenhum índice antigo anda, e o `guarda_save.py`
continua dizendo **SAVE COMPATIVEL**.

**Os quatro interiores novos não gastam blockdata.** O layout é REAPROVEITADO de interior de Johto que
já está na árvore, do jeito que o `fecha_portas_sinnoh.py` fez em Sinnoh. O que é nosso é o NPC e a
fala, dois por casa, os oito em inglês. Custo total da frente: **1.740 B de ROM** (32.371.772 para
32.373.512), sendo zero de layout.

**As 18 placas.** `bg_event` do tipo `sign` na célula da porta, apontando para um de dois scripts
comuns de `data/scripts/portas_fechadas.inc`: o galpão de porto usa o `Common_EventScript_PortaFechada`
que já existia ("Closed for renovations."), e a boca de caverna ganhou o
`Common_EventScript_BocaFechada`, com frase própria ("The cave mouth is blocked by fallen rocks."),
porque escrever "em obras" na frente de um buraco de pedra mentiria o mapa. A `lente_portas.py`
aprendeu a regra por MEDIDA e não por lista: célula com `bg_event` apontando para uma das duas placas
sai das três regras e é contada à parte.

**O que a lente diz agora.** Em Johto, "sem interior" caiu de **40 para 11**, e os 11 são os 9 portões
de rota desenhados dos dois lados da emenda mais as 2 casas do Lago da Fúria em maré baixa, ou seja o
que não é defeito. `lente_portas` com **0 travas em Kanto, Johto e Hoenn** (Sinnoh continua com as 8
do corte, que são de antes), lista branca de 18 para 21, e 18 portas na conta nova de placa.
`lente_warps` com **zero achado em Johto**.

**A prova está no framebuffer, e são 18 casos.** `dev_scripts/testes_criticos/182_johto_portas_31.json`,
**18 de 18**, com entrada e saída de cada interior novo, entrada e saída de cada ligação, e o par
positivo/negativo da seta do Monte Prata. O T182.16 mais o T182.15 são o percurso que o Gui pediu:
entra pela boca (34,7) do Monte Prata, atravessa o 1F e sai pela (50,5). O T182.10 é o que separa
"entrou pela fachada" de "saiu pelo lado": a saída da fachada da creche devolve para o warp 5 e não
para o 4. Armadilha de roteiro medida aqui e que vale para o próximo: **o motor entrega o jogador UM
TILE ABAIXO da boca** ao sair do warp de debug, e um toque de 20 quadros nem sempre completa o passo,
então boca de caverna se prova com `20:UP*4` e não com descer e subir; com o roteiro errado quatro
casos reprovavam com o jogo inteiro certo.

**O que fica aberto.** As 18 placas NÃO foram provadas no emulador. As 18 ficam em porta que o jogador
alcança pela BORDA do mapa, vindo da rota vizinha, e não a partir de nenhum warp do próprio mapa
(medido com busca em largura a partir de cada saída de warp: nenhuma das 18 é alcançável por dentro),
então prová-las custaria atravessar mapas inteiros com botão. O que está provado delas é o dado (o
`bg_event` no `map.json`), o script (o build liga, e o `checa_scripts` do `roda_qa` confere o rótulo)
e a leitura da lente. Segundo item aberto: a `Route45` (39,53) é a única das 18 cuja célula de porta
tem colisão 0, ou seja o jogador PASSA por cima dela em vez de encostar; a placa dela só é lida por
quem chegar de frente, e por isso ela é a mais fraca das 18.

**A última medição desta frente**, contra a ROM `2026-09-07c`. Build limpo verde, EWRAM e IWRAM sem
mudança, ROM 32.373.512 B (96,48% de 32 MB). `guarda_save.py` **SAVE COMPATIVEL**, SaveBlock1 em
14.964 de 15.872 B, **2.404 mapas** (2.400 mais os quatro interiores novos). `valida_rom.py` com os
2.404 mapas dentro da ROM. `valida_conectividade.py` com **0 warps quebrados**, e o alcance sobe de
1.965 para **1.969 de 2.293**, que são exatamente os quatro mapas novos. `valida_warp_tile --piso 60`
em **5.937 de 6.893 (86,1%)**, com Johto subindo de 90,8% para **91,0%** e nenhuma região abaixo do
piso; os 16 warps novos disparam TODOS. `completude.py` de Johto: mapas 100,0%, objetos 100,8%,
warps 100,1% para **101,7%**, placas 100,4% para **104,0%**. `roda_qa.py --demo` verde nas seis
varreduras, e a varredura cheia dá **14.654 achados com as MESMAS 323 travas** (Kanto 5, Johto 2,
Hoenn 2, Sinnoh 8, Unova 25, Galar 268, comum 13). `testa_percurso.py` sem problema nos 6 percursos.
`prova_portas_compartilhadas.py` **11 de 11**. Suíte: **os 22 blocos que passam pelos mapas tocados,
237 de 237**, mais o **T11 3 de 3** contra `roms/pokemon-claude-2026-08-18.gba` com a fonte velha da
worktree `cf6786b2ae`.

### O bloco preto de Pastoria: não era Pastoria, era CAMADA DE DESENHO na Route 212 South, 06/09/2026

O Gui trouxe do playtest, no capítulo "before Crasher Wake", à noite e chovendo, "um retângulo de
tiles pretos (azul-escuro sólido, ~6x4) encostado nas árvores, e o jogador entra embaixo dele: anda
por dentro do bloco preto, que desenha por cima dele". A hipótese de entrada era o portão do Great
Marsh, cortado em 21/08/2026, com metatile indefinido e sem colisão.

**As duas partes da hipótese estavam erradas, e medir isso foi metade do trabalho.**

1. **Não é Pastoria.** `PastoriaCity` tem **zero** célula preta: `render_maps.py` não pinta um pixel
   de cor de fundo no mapa inteiro (o backdrop do `gTileset_GeneralSinnoh` é `(24,41,82)`, o
   azul-escuro exato que a foto mostra, e ele não aparece em nenhum dos 4.080 blocos), os 182
   metatiles distintos cabem todos nos tilesets (512 no primário, 392 no `LilycoveSinnoh`), e quatro
   varreduras no emulador (os dez warps mais 115 passos de caminhada) não acharam nada escuro. O
   corte do Great Marsh está LIMPO: `PastoriaCityObservatoryGate1F` tem placa
   `PortaFechada` e nenhum warp para o `GreatMarsh6`, que é TÚMULO sem warp de entrada.
2. **Não é metatile indefinido, e não é corte.** O mapa é a **Route 212 South**, a vizinha de
   Pastoria e a ÚNICA das quatro que tem `"weather": "WEATHER_RAIN"` (Pastoria é `WEATHER_NONE`, e a
   chuva da foto é que a denuncia). O que engole o jogador é o **brejo**, e o defeito é a CAMADA em
   que a arte foi parar.

### O mecanismo: `DrawMetatile` só tem três casos, e dois deles põem arte ACIMA do sprite

Cada metatile tem duas camadas de quatro tiles, e o tipo de camada
(`metatile_attributes.bin`, bits 12-15 no formato Emerald e 29-30 no de FRLG) decide em qual BG cada
uma cai (`src/fieldmap.c`):

| tipo | camada de baixo | camada de cima |
|---|---|---|
| `NORMAL` | BG2, **abaixo** do sprite | BG1, **acima** de todo sprite |
| `COVERED` | BG3 | BG2, **abaixo** do sprite |
| `SPLIT` | BG3 | BG1, **acima** do sprite |

Os 13 metatiles do brejo (`gTileset_LilycoveSinnoh` locais 179, 180, 184-188, 192-194 e 200-202,
ids 691, 692, 696-700, 704-706 e 712-714) trazem a arte inteira na camada de **cima**, 100% opaca,
com tipo `NORMAL`. E o `map.bin` marca colisão 0 nas 405 células em que eles aparecem. Ou seja: o
jogador entra, e o BG1 desenha o brejo inteiro por cima dele. À noite, com chuva, a cor média
`(48,88,104)` fica quase preta, que foi como a foto mostrou.

**Prova no framebuffer, antes e depois, o mesmo warp e a mesma rota:** warp 0 da `Route212_South`
(grupo 75, mapa 30), 25 passos para a direita e 8 para baixo, `--dump-estado` confirmando o jogador
em **(77,21)**, que é o metatile 705. Na ROM `2026-09-06` a tela mostra o retângulo escuro e
**nenhum jogador**. Nesta build o mesmo passo mostra o jogador em pé sobre o brejo.

### O conserto: 13 metatiles passam para `COVERED`, e nada mais muda

`dev_scripts/conserta_camada_metatile.py` (novo, com `--demo`, `--regiao`, `--tileset` e `--aplica`)
levanta os alvos pela lente E3 e reescreve o tipo de camada. Não muda um pixel de arte, não toca em
`map.bin`, não toca em `map.json`, não mexe em mapa nenhum: são **dois bytes por metatile** no
`metatile_attributes.bin`, e a mesma arte passa a ser desenhada no BG2, abaixo do sprite. Idempotente
(a segunda passada com `--aplica` dá 0).

Ele tem **duas travas**, e as duas nasceram de erro medido nesta rodada:

- **Tileset que Hoenn ou Kanto usam não é tocado.** A mesma lente acusa **546 células em Hoenn** e as
  MESMAS 546 na árvore do `pokeemerald` intocado, e as de Kanto têm atributo idêntico ao do
  `pokefirered` (conferido byte a byte no `power_plant`: `metatiles.bin` e `tiles.png` iguais, e os
  metatiles 673-677 com `0x01000008` nos dois). Lá é idioma do jogo original, não defeito nosso.
- **Metatile que aparece em célula SÓLIDA não é tocado.** A lente acusa dois defeitos com a mesma
  cara e que se consertam em lugares opostos. O do brejo é CAMADA (405 usos, nenhum sólido). O outro
  é COLISÃO: os metatiles 12, 80-82, 89, 131 e 139 do `gTileset_GeneralSinnoh` são o telhado
  vermelho e a fachada do Centro Pokémon, com **12 usos sólidos contra 1 andável**, e passá-los para
  `COVERED` só trocaria "o jogador sumiu" por "o jogador andando por cima do telhado". Ali o
  conserto é a colisão da célula, no mapa, e fica registrado abaixo.

### A lente permanente: `E3` em `dev_scripts/qa/mapas_qa.py`

"Bloco preto andável": célula **alcançável** (a BFS de `mapas_qa`, semeada por warp, heal location e
conexão, com a regra de elevação do motor) cujo metatile **tapa o jogador por inteiro**: tipo
`NORMAL` ou `SPLIT`, camada de cima 100% opaca, e camada de baixo VAZIA ou repetindo a de cima em
**metade dos quadrantes**.

Três decisões de régua, todas medidas:

- **O alcance é o que separa defeito de enchimento.** Sem ele a regra acusava 4.581 células só no
  grupo de Goldenrod: mapa importado tem centenas de células de metatile 0 (preto, colisão 0) FORA da
  sala, atrás da parede, onde ninguém pisa.
- **"Metade dos quadrantes", e não "as duas camadas iguais".** Os cantos do brejo (691 e 700)
  repetem o miolo em 3 de 4 quadrantes e trocam um só; com a régua de "os quatro iguais" eles
  escapavam e o conserto saía pela metade, com o miolo aparecendo e as bordas ainda engolindo o
  jogador.
- **Passagem por baixo de verdade não compartilha quadrante nenhum**, e por isso não é acusada: o
  metatile 669 do `gTileset_Facility` (Aqua Hideout, vanilla) tem 0 de 4, com o chão na camada de
  baixo e a máquina na de cima.

`--vanilla` roda a mesma régua no `pokeemerald` intocado e dá **546 em Hoenn**, exatamente o que a
nossa árvore dá: Hoenn está calibrado em zero acima do vanilla.

### O que a lente achou, por região

| região | antes | depois | veredito |
|---|---|---|---|
| Kanto | 240 | 240 | herdado do `pokefirered` (PowerPlant 141, salas da Elite dos Quatro, Saffron) |
| Johto | 405 | 405 | **aberto**, ver abaixo |
| Hoenn | 546 | 546 | **falso positivo calibrado**: o vanilla dá os mesmos 546 |
| Sinnoh | 587 | **113** | os 405 da Route 212 South consertados |
| Unova | 215 | 215 | outro cartucho, só listado |
| Galar | 3.787 | 3.787 | outro cartucho, só listado |

**Johto (405), aberto e NÃO consertado nesta frente**, porque não é o mesmo defeito e porque os mapas
estão na mão de outros executores nesta rodada (Ecruteak, Goldenrod, Blackthorn, Mahogany):

- `NewBarkTown_Lab` **312**, e é outra classe: o laboratório é 40x14 e só as 13 primeiras colunas são
  sala; o resto é metatile 0 (preto) com colisão 0, e a BFS ENTRA nele a partir da linha 12. A sala
  não está vedada, e o conserto é colisão no `map.bin`, não camada.
- `EcruteakCity_Gym` 46 (metatile 811), `OlivineCity_Lighthouse` 20, `GoldenrodCity` 14, `Route26` 2,
  `Route34` 2: assinatura de camada, do mesmo tipo do brejo, e cada um pede o mesmo conserto de dois
  bytes.

**Sinnoh, os 113 que sobraram** (nenhum é o defeito relatado, e nenhum passa pelas duas travas do
conserto): 36 nas quatro salas da Liga (`gTileset_EliteFour` locais 7 e 8, tileset COMPARTILHADO com
Hoenn, mesma célula e mesmo atributo do vanilla); `MtCoronet_1F_South` 26, `Route214` 19,
`SunyshoreCity` 14 e o resto pingado em Veilstone, Eterna, os lagos e as torres, tudo de 1 a 3
células. Os de telhado (Oreburgh, Eterna, Hearthome, Floaroma) são conserto de COLISÃO no mapa e
estão nomeados acima.

### Os portões desta frente

Build verde com o lock, **ROM 32.371.048 B, 96,47% de 32 MB**. O conserto custa **zero byte**: o
`metatile_attributes.bin` tem tamanho fixo e só 13 entradas de dois bytes mudaram, com os bits de
comportamento intactos (`0x0000` -> `0x1000`, conferido byte a byte contra o `git show HEAD:`). O
render de `Route212_South` sai **byte a byte idêntico** antes e depois (mesmo md5), que é a prova de
que nenhum pixel de arte mudou: quem mudou foi o BG em que ele é desenhado.

`valida_rom.py` com os **2.400 mapas declarados dentro da ROM**, `guarda_save.py` **SAVE COMPATIVEL**
(SaveBlock1 em 14.964 de 15.872 B), **T11 3/3** contra a `roms/pokemon-claude-2026-08-18.gba`,
`valida_warp_tile.py` em 6.875 warps conferidos, `roda_qa.py --demo` verde nas seis varreduras
(as quatro antigas mais `lente_warps` e `lente_portas`) e `mapas_qa.py --demo` verde com o autoteste
novo da E3. ROM entregue: `pokemon-claude-2026-09-06p.gba`, md5 `b9decf96a4bf93b0254983e2fe100f49`.

**A suíte fechou 1.004 de 1.028 nesta árvore, e as 23 reprovações NÃO são desta frente**, o que está
medido e não suposto: `gTileset_LilycoveSinnoh` é usado por **três mapas apenas**
(`PastoriaCity`, `Route212_North` e `Route212_South`, conferido no `layouts.json`; o
`metatile_attributes.bin` entra por `INCBIN_U16` direto, sem `ASSET_ALIAS`), e nenhum dos 23 casos
passa por eles. Os sete casos de barco (T8.5, T10.1, T86.8 a T86.12) **passam 12 de 12 na ROM
`2026-09-06`** e reprovam nesta build, ou seja o que os quebrou entrou entre `fccccc0265` e agora:
esta rodada tem vários executores mexendo em Sinnoh ao mesmo tempo (Sunyshore, Pokécenters,
auditoria de warps, Mahogany), e as outras reprovações são exatamente nos mapas deles (T125.9/10
Sunyshore, T140.x portas fechadas, T151.x interiores pobres, T100/T101 Twinleaf, Hearthome e
Solaceon). Fica registrado para o fechador da rodada juntar as pontas.

**PONTA JUNTADA PELO FECHADOR, 07/09/2026:** eram mesmo obra alheia em curso. Na build limpa do HEAD
`ed8698166c`, com a árvore parada e uma frente só na máquina, a suíte fecha sem nenhuma dessas
reprovações (o placar completo está no fim desta seção).

### Toda porta entra: a lente de porta sem warp, e o elevador de Goldenrod volta a funcionar, 06/09/2026

O Gui pediu no playtest: *"reveja se dá para entrar em TODAS as casas da ROM"*. O
`valida_warp_tile.py` só respondia metade da pergunta, porque ele parte do WARP e pergunta se o tile
embaixo dispara. A outra metade, partir do TILE e perguntar se existe warp em cima, nunca teve régua,
e porta desenhada sem warp é justamente a casa em que o jogador anda até a porta e nada acontece.

A lente nova é `dev_scripts/qa/lente_portas.py`, entra em `roda_qa.py` com as outras e tem três
regras: **P1** porta ao ar livre sem warp, **P2** porta em mapa fechado sem warp e **P3** warp fora
da célula da porta. A unidade é o BLOCO de células vizinhas de mesmo comportamento, porque porta de
prédio no FRLG tem três tiles de largura e portão de Johto tem quatro, e só um deles carrega o warp.
Porta que o roteiro abre sai da conta, e isso é LIDO do script: `setmetatile` (a escada escondida da
loja de Mahogany) e `opendoor` (todo elevador de loja de departamento), seguindo o rótulo por um
índice da árvore inteira, porque o `opendoor` do elevador mora no `.inc` de outro mapa.

**A calibração é de identidade, rodando a MESMA lente nas fontes intocadas:** Hoenn dá 1 em 202
mapas ao ar livre aqui e 1 em 202 no `pokeemerald`, Kanto dá 11 em 168 aqui e 11 em 168 no
`pokefirered`, mapa a mapa e célula a célula. Não há o que consertar nas duas, e os 12 casos entram
na lista branca um a um. Em Johto, todo `map.bin` e todo warp são byte a byte iguais aos do `hns`.

**O único conserto é o elevador da loja de departamento de Goldenrod.** Os seis andares e o subsolo
tinham a porta desenhada em (9,4), e em (10,6) no subsolo, e o warp uma célula ACIMA dela, em parede
com colisão 1: warp em tile sólido nunca dispara e porta sem warp nunca abre, então a porta não fazia
nada em nenhum andar. O mecanismo certo estava na fonte e não tinha sido importado, e ele não usa o
mapa do elevador: um `coord_event` na frente da porta chama a cena, a cena abre a porta, entra com
`applymovement`, mostra o menu de sete andares e usa `warp` de script. O warp de (9,3) **não foi
movido**, porque índice de warp é promessa permanente de save e mover a célula não consertaria nada.
Custo em save: **zero**. `coord_event` não entra na save e `VAR_ELEVADOR_GOLDENROD` é apelido de
`VAR_UNUSED_0x4114`, então `VARS_COUNT` não muda.

**Sobram 40 achados em Johto na classe "sem interior"**, que são decisão do Gui e não do agente:
porta que o jogador vê, não abre, e para a qual não existe mapa de interior na árvore. Medido: Johto
não tem um só mapa órfão, então não há interior cortado esperando ser religado, e consertar exigiria
inventar conteúdo. Nove dos 40 nem são defeito, são o portão de rota desenhado dos dois lados da
emenda. Os 31 restantes são a **pergunta 46** ao Gui.

#### Os portões da frente do elevador de Goldenrod

Build verde com o lock, **ROM 96,47% de 32 MB** (32.371.048 B), **EWRAM 86,16% e
IWRAM 86,68%**. `valida_rom.py` com os **2.400 mapas** declarados dentro da ROM.
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), sem mudança de
struct, de índice de mapa, de índice de warp nem de objeto; a var nova é apelido
de `VAR_UNUSED_0x4114` e `guarda_colisao_vars.py` diz 0 colisões novas.
`valida_warp_tile --piso 60` com Hoenn 93,2%, Kanto 79,4%, Sinnoh 98,1%, Johto
90,7% e Unova 100,0%, nenhuma região abaixo do piso. `roda_qa.py --demo` verde
nas SEIS varreduras, com a `lente_portas` entre elas, e a lente nova dá **0
travas em Kanto, Johto e Hoenn**.

A prova do conserto é o **T172, 3 de 3 no emulador**, e ela é o par entrar e
sair, duas portas: o T172.1 entra pela porta da rua do primeiro andar, anda até
o gatilho de (9,5), pega o menu com o cursor em 6F e termina **no sexto andar em
(9,6)**; o T172.2 faz o mesmo no sexto andar e desce até o **subsolo, em
(10,8)**, que é o andar cuja porta fica em (10,6). O T172.3 é o par negativo: sem
pisar no gatilho o jogador continua no primeiro andar. No framebuffer do T172.1
aparece a cabine ABERTA com o painel marcando "1F" e o menu de sete andares mais
"EXIT"; no do T172.2 o mesmo painel marca "6F" com o cursor em "B1F"; e os dois
quadros finais mostram o jogador embaixo da porta FECHADA do andar em que
desembarcou.

**A suíte fechou em 1.008 de 1.015**, com o T11.3 contado à parte, e os **seis
reprovados NÃO são desta frente**: T140.1, T140.3 e T140.4 caem no
`ContestHallLobby`, T151.3 e T151.4 na sala de treinador do ginásio de Hearthome,
e o T170.4 na cena dos três cães do Burned Tower. Os três mapas estão com edição
NÃO commitada de outras frentes desta mesma rodada (as 44 portas fechadas, o
gerador de Sinnoh e o arco de Ecruteak), e nenhum arquivo desta frente encosta
neles: o conserto daqui é a loja de departamento de Goldenrod, mais um apelido no
fim de `vars.h` e uma entrada no FIM do enum de `script_menu.h`, que não desloca
id de ninguém.

**FECHADO PELO FECHADOR, 07/09/2026:** era mesmo obra alheia em curso. Na build limpa do HEAD `ed8698166c`, com a árvore parada, os seis passam e a suíte fecha em 1.047 de 1.048 (ver o placar no topo desta seção).

### A auditoria de ida e volta dos warps: quem entra por uma porta tem que sair por ela, 06/09/2026

Mais um defeito do playtest, e o pedido que veio junto: *"em Sinnoh fui para Veilstone, entrei no
prédio da esquerda, e saí, e aí saí em Lilycove City"*, seguido de **"revisa todas essas entradas e
saídas, se os links estão certos! TODAS!!!"**. A loja de Veilstone É a loja de Lilycove
REAPROVEITADA, e a saída dela era fixa para Hoenn. O `valida_conectividade.py` dava verde no warp,
porque ele confere se o ÍNDICE de destino existe, e existia: a camada que faltava era a VOLTA.

#### A lente nova, e o recorte que a faz valer alguma coisa

`dev_scripts/qa/lente_warps.py`, quinta varredura do `roda_qa.py`. Para cada warp A(x,y) -> B[k] ela
olha o warp k de B, que é o tile em que o jogador POUSA, e cobra que ele devolva para A, na porta que
o jogador usou.

| regra | o que cobra |
|---|---|
| **P1** | destino inexistente: mapa ou id de warp que não existe |
| **P2** | porta que não devolve: ao ar livre <-> fechado, e a volta cai em OUTRO mapa |
| **P3** | volta para lugar errado: cai no mapa certo, mas fora da porta usada |
| **P4** | escada interna que não devolve: mesmo prédio, e só em tile de escada ou porta |

**A versão ampla dessa regra já tinha sido medida e REPROVADA** em 23/08/2026 (comentário no
`valida_conectividade.py`): "todo warp tem que voltar" dava 427 casos aqui contra a MESMA taxa por 100
mapas no pret/pokeemerald intocado. O que separa bug de idioma do motor é a **travessia de camada**,
mais três recortes, cada um com a medida que o justifica:

1. **Warp fora da grade do layout não tem ida e volta**, porque ninguém pisa nele. São 2 no cartucho
   1, `TinTower_8F` warp 4 em **(-1,10)** e `Route26` warp 0 em **(12,-24)**, lixo do importador do
   demake.
2. **Warp cujo tile NUNCA DISPARA também não**, e essa camada já tem dono, o `valida_warp_tile.py`.
   São **960 dos 6.875**. Sem este recorte a lente acusava `EcruteakCity` warps 4, 5 e 14 e
   `NewBarkTown` warps 4 a 7, todos `MB_NORMAL` com colisão 1, ou seja portas que o motor nunca abre.
3. **Porta larga é UMA porta.** Warps de A que apontam para o MESMO (mapa, warp) e ficam colados são
   a mesma porta, e a volta pousar em qualquer um deles está certo. É o idioma dos portões de Johto
   (4 tiles em `Route34` e no Parque Nacional) e das saídas de prédio de Kanto (3 tiles).

O P4 só olha tile de **mão dupla** (escada, porta, escada rolante, escada diagonal), porque buraco do
Mt. Pyre, redemoinho do esconderijo Aqua, chão falso dos ginásios de Lavaridge e Mossdeep e saída de
sala de batalha são de mão única DE PROPÓSITO, e quem os separa é o COMPORTAMENTO DO METATILE, lido
do enum do repo e não de número copiado.

**A calibração é o vanilla**, como manda a lição 4.2: rodada antes de qualquer conserto, a lente dava
**0 em Hoenn e 0 em Kanto** fora da lista branca. Os 14 casos de Hoenn e Kanto que ela levanta foram
abertos um a um e comparados com `../fontes-mapas/pokeemerald` e `../fontes-mapas/pokefirered`:
**`warp_events` IGUAL byte a byte nos 14**, então entram na lista branca com o motivo escrito, nunca
"para baixar o número".

#### O retrato, antes e depois

| regra | Kanto | Johto | Hoenn | Sinnoh | Unova | Galar | total |
|---|---|---|---|---|---|---|---|
| P1 destino inexistente | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| P2 porta que não devolve | 0 | 6 -> **0** | 0 | 3 -> **0** | 0 | 47 | 56 -> **47** |
| P3 volta para lugar errado | 0 | 0 | 0 | 0 | 3 | 0 | **3** |
| P4 escada que não devolve | 0 | 2 -> **0** | 0 | 0 | 35 | 83 | 120 -> **118** |
| total | 0 | 8 -> **0** | 0 | 3 -> **0** | 38 | 130 | 179 -> **168** |

**6.874 warps em 2.289 mapas vivos** (111 túmulos fora da conta; eram 6.875 antes de o warp morto do
Battle Tower de Ecruteak sair), dos quais **4.321 passam por porta de prédio ou escada interna**, que
é o denominador da regra, e **956 nunca disparam**, camada do `valida_warp_tile.py`. Esse censo é da
ÁRVORE COMPARTILHADA, com as seis frentes da rodada 13 juntas; na worktree isolada desta frente ele dá
959 e 4.318, porque as outras frentes consertaram metatile de porta e três warps passaram a disparar.
O que NÃO muda entre as duas árvores é o que importa: **0 achados em Kanto, Johto, Hoenn e Sinnoh**,
medido nas duas. **O cartucho 1 fecha em ZERO**, e é isso
que o `--demo` da lente cobra: ele reprova se Kanto, Johto, Hoenn ou Sinnoh voltarem a ter achado.
Dos 11 do cartucho 1, **4 eram do Trainer Hill e das três Battle Tents** e já são da frente dos
prédios que Hoenn e Johto dividem, desta mesma rodada; os **7** desta frente estão na tabela de
consertos.

#### O mecanismo: `MAP_DYNAMIC` mais um special, e ZERO custo de save

O interior de Hoenn que Sinnoh reaproveita **não foi copiado**. A porta de saída dele virou
`MAP_DYNAMIC`, e o próprio motor grava de onde o jogador veio: em `SetupWarp`
(`src/field_control_avatar.c:1131`), quando o warp em que o jogador vai POUSAR é dinâmico, ele chama
`SetDynamicWarp` com o mapa e o índice do warp de origem, e com o `warpId` gravado a saída mantém a
animação de porta e o tile de sempre. `dynamicWarp` já existe no SaveBlock1 desde o Emerald: **custo
de save zero**.

O que o motor NÃO faz é repor esse retorno depois que outra coisa reescreve o `dynamicWarp`, e dentro
da loja de Lilycove isso acontece sempre, porque o **ELEVADOR** faz
`setdynamicwarp MAP_LILYCOVE_CITY_DEPARTMENT_STORE_3F, 2, 1` a cada andar escolhido
(`data/maps/LilycoveCity_DepartmentStoreElevator/scripts.inc:80`). Sem reposição, quem subisse de
elevador e descesse a escada até o térreo sairia pela porta da rua e reapareceria no terceiro andar,
para sempre.

O conserto é o special `DefinirRetornoPredioCompartilhado` (`src/field_specials.c`), chamado no
`ON_TRANSITION` do andar de ENTRADA. **A guarda é a pergunta certa, e não "quem escreveu por
último"**: a porta da rua do térreo TEM que levar para fora, então se o retorno gravado aponta para um
mapa que **não é ao ar livre** (`IsMapTypeOutdoors`), ele está velho e é reposto pelo `escapeWarp`,
que é o registro que o motor faz da última entrada de mapa aberto para mapa fechado
(`UpdateEscapeWarp`, `src/overworld.c:774`) e guarda o tile uma linha abaixo da porta. Quando o
jogador entrou pela rua, o retorno aponta para a cidade, a guarda não toca em nada, e a saída fica
idêntica ao original.

**Nasceram DOIS specials com esse papel na mesma rodada**, este e o
`DefinirRetornoPredioCompartilhado` da frente dos quatro prédios que Hoenn e Johto dividem (Trainer
Hill mais os três lobbies de Battle Tent), escritos em paralelo por duas frentes que não se viam. Os
CORPOS eram iguais byte a byte, e a guarda cobre os dois casos: "o retorno aponta para o próprio
mapa", a assinatura das Battle Tents, é um caso particular de "o retorno não aponta para fora".
**Viraram UM em 06/09/2026**, e ficou o do `src/field_specials.c`, porque ele já estava no HEAD
(`40ebe8eedd`): a loja e o museu de Lilycove passaram a chamar `DefinirRetornoPredioCompartilhado`,
`src/retorno_dinamico.c` foi APAGADO e o `def_special` sobrando saiu do `data/specials.inc`. A prova
não é "compilou": os **10 casos do T171**, que são das tendas e do Trainer Hill, foram rodados de novo
nesta build e deram **10 de 10**, e a `prova_portas_compartilhadas.py` deu **11 de 11** com os dois
prédios de Sinnoh chamando a função do outro. Um special, seis prédios.

#### Os oito consertos do cartucho 1

| # | região | onde | o que era | o que ficou |
|---|---|---|---|---|
| 1 | Sinnoh | `VeilstoneCity` (25,30) -> loja de Lilycove | a saída da loja era fixa para `LilycoveCity` | os dois tiles de porta da `LilycoveCity_DepartmentStore_1F` viraram `MAP_DYNAMIC`, mais o special no `ON_TRANSITION` |
| 2 | Sinnoh | `OreburghCity` (54,14) -> museu de Lilycove | a saída do museu era fixa para `LilycoveCity` | as duas portas da `LilycoveCity_LilycoveMuseum_1F` viraram `MAP_DYNAMIC`, mais o special |
| 3 | Sinnoh | `Route218` (59,24), seta leste | levava a `MAP_ROUTE211_EAST` warp 0, do outro lado do mapa, perto do Mt. Coronet | `MAP_ROUTE218_EAST` warp 1, que é a porta oeste do portão, e o par fecha |
| 4 | Johto | `ReceptionGate` (11,1) e (10,1), porta norte | `VICTORY_ROAD_1F` warp **0**, que é a ESCADA do 2F | warp **1**, que é a boca sul da Victory Road, e esse warp virou `MAP_DYNAMIC` |
| 5 | Johto | `ReceptionGate` (20,9), porta leste | `MAP_ROUTE22` warp 0, que é o tile da PORTA do portão de Kanto: o jogador era cuspido em cima dela | `MAP_ROUTE22_NORTH_ENTRANCE` warp 0, que virou `MAP_DYNAMIC` |
| 6 | Johto | `SafariZoneGate_SafariZoneEntrance` (9,1) | o Safari de Johto É o de Hoenn, e sair dele levava à Rota 121 | `SafariZone_South` warp 0 virou `MAP_DYNAMIC` |
| 7 | Johto | `EcruteakCity` (39,46), warp 14 | `BattleFrontier_BattleTowerLobby` warp 0, ou seja Hoenn | o warp SAIU do mapa. Decisão do Gui: Olivine ganha depois a Battle Tower simples do Crystal, e até lá nenhum warp de Johto pode mandar para a Battle Frontier de Hoenn |
| 8 | Kanto/Hoenn | os lados originais de 1 a 6 | (nada, é o controle) | conferidos no emulador como REGRESSÃO, um par por conserto |

Os warps 4 e 5 do `ReceptionGate` eram herança do importador do demake: no `../fontes-mapas/hns` eles
apontam para `MAP_VICTORY_ROAD_KANTO_B2F` e para o `MAP_ROUTE22` **do próprio hns**, e nenhum dos dois
foi importado; nesta ROM as duas constantes resolvem para mapas do FireRed, e o portão passou a
desembocar na escada e em cima de outra porta.

#### O que a auditoria achou e NÃO consertou, com o motivo

- **Unova 38 e Galar 130**, listados pela lente e deixados de fora por escopo: as duas regiões vão
  para OUTRO cartucho (memória `pokemon-claude-gens-6-9-escopo`). O grosso de Galar são os prédios
  compartilhados de Hammerlocke, Circhester e Ballonlea, com a mesma assinatura do caso de Veilstone,
  e o mesmo mecanismo resolve quando a frente de Galar abrir.
- **`EcruteakCity` warps 4 e 5 são WARP MORTO**, não link errado: os dois estão sobre `MB_NORMAL` com
  colisão 1, medido no blockdata (comportamento 0, `dispara=False`), e abrir essas portas é mexer no
  metatile do mapa, que é obra da frente de Ecruteak. O warp **14 era o terceiro morto**, e ele era o
  do Battle Tower: mesmo sem disparar, o link mandava para `BattleFrontier_BattleTowerLobby`, do outro
  lado do mundo, e a saída do lobby é fixa para `BattleFrontier_OutsideEast`. O Gui decidiu que Olivine
  vai ganhar a Battle Tower simples do Crystal mais para a frente, então o warp foi REMOVIDO em vez de
  reapontado: ele era o ÚLTIMO da lista do mapa, ninguém apontava para o índice 14 (varridos os 2.400
  `map.json`), e por isso a remoção não desloca índice de warp nenhum, que é promessa permanente de
  save. Quando a Battle Tower de Olivine existir, ela entra como warp novo no fim da lista, com o
  retorno dinâmico deste mesmo mecanismo.
- **`NewBarkTown` warps 4 a 7 também são warp morto**, e é por isso que os dois `WorldHub` aparecem
  inalcançáveis: nenhuma das quatro portas dispara.
- **O Safari de Johto não tem script de entrada nenhum**: não cobra taxa, não acende
  `VAR_SAFARI_ZONE_STATE`, não dá bolas nem contador de passos. Quem entra por Johto entra sem modo
  Safari, e sai andando pela porta, que agora devolve para o portão certo. A saída POR DIÁLOGO com o
  atendente continua com `warp MAP_ROUTE121_SAFARI_ZONE_ENTRANCE, 2, 5` cravado em
  `data/scripts/safari_zone.inc:25`, e cai em Hoenn: é conteúdo do Safari de Johto, não link de warp.

#### A prova é do emulador, e cada conserto vem com o seu par negativo

`dev_scripts/prova_portas_compartilhadas.py`, **11 de 11**. Ela warpa pela porta pelo menu de debug,
ENTRA andando, SAI andando, e lê da EWRAM o `(grupo, num)` e o `(x, y)` em que o jogador parou. Cada
conserto tem ao lado o LADO ORIGINAL do mesmo interior, porque sem o par um conserto que quebra o
original passa verde.

| caso | região | rota medida |
|---|---|---|
| `veilstone` | Sinnoh | Veilstone (25,31) -> porta (25,30) -> loja (8,7) -> **Veilstone (25,30) -> (25,31)** |
| `lilycove_loja` | Hoenn | Lilycove (27,7) -> (27,6) -> loja (8,7) -> **Lilycove (27,7)** |
| `oreburgh` | Sinnoh | Oreburgh (54,15) -> (54,14) -> museu (9,13) -> **Oreburgh (54,14) -> (54,15)** |
| `lilycove_museu` | Hoenn | Lilycove (11,6) -> (11,5) -> museu (9,13) -> **Lilycove (11,5) -> (11,6)** |
| `safari_johto` | Johto | portão (9,2) -> (9,1) -> Safari (32,34) -> **portão (9,1) -> (9,2)** |
| `safari_hoenn` | Hoenn | Rota 121 (2,5) -> Safari (32,33) -> **Rota 121 (2,5)** |
| `portao_victory` | Johto | portão (11,2) -> (11,1) -> Victory Road (11,20) -> **portão (11,1) -> (11,2)** |
| `portao_rota22` | Johto | portão (20,9) -> portão de Kanto (7,2) -> (7,1) -> **portão (20,9)** |
| `route218` | Sinnoh | Rota 218 (59,24) -> portão (1,5) -> (2,5) -> (1,5) -> **Rota 218 (59,24)** |
| `victory_kanto` | Kanto | Rota 23 (5,29) -> (5,28) -> Victory Road (11,20) -> **Rota 23 (5,28) -> (5,29)** |
| `elevador` | Sinnoh | ADVERSARIAL, abaixo |

**O caso `elevador` é o adversarial, e sem ele os outros dez passariam com o special QUEBRADO**,
porque o caminho curto (entra, sai) nunca chega a sujar o `dynamicWarp`. Ele entra na loja por
Veilstone, ANDA ATÉ O ELEVADOR e entra nele, o que faz o próprio motor gravar
`dynamicWarp = (loja 1F, warp 3)`, um mapa FECHADO; volta ao térreo sem escolher andar, atravessa a
loja e sai pela porta da rua. Medido no traço passo a passo: Veilstone (25,31) -> loja (8,7) ->
(2,5) -> **elevador** -> loja (2,2) -> (17,5) -> (4,6) -> (4,7) -> (13,7) -> porta (8,7) ->
**Veilstone (25,31)**, o tile em frente à porta (25,30). Sem a reposição ele sairia em cima da porta
do elevador, dentro da própria loja.

**Segunda armadilha medida, e ela custou o dobro do que parecia:** dentro da loja NÃO se conta tile
em corredor que uma NPC de andar alcança. São duas `MOVEMENT_TYPE_WANDER_AROUND` de alcance 1, em
(4,4) e em (14,5), e a de (4,4) guarda justamente a única passagem para o lado oeste do salão, que é
onde fica a porta do elevador. Um roteiro que contava tiles ali deu **11 de 11 numa rodada e 0 de 1
na seguinte, com a MESMA ROM**: a NPC barrava a ida e o jogador subia a coluna 5 até (5,2), sem
chegar ao elevador. O roteiro passou a andar de ÂNCORA em ÂNCORA, sempre com apertos de sobra, e as
âncoras são de dois tipos, os dois imóveis: **parede** (oeste em (2,5) da linha 5, leste em (17,5),
sul em (17,6), a borda do mapa) e **NPC PARADA** (as duas `LOOK_AROUND` de (2,6) e (3,6), que ancoram
em (2,5) e em (4,6)). Só a última perna conta tiles, e ela mira uma **porta LARGA**: (8,7) e (9,7)
são os dois tiles da mesma saída, então 5 ou 6 apertos acertam do mesmo jeito. Medido **4 vezes
seguidas com o mesmo resultado**, e a suíte inteira duas vezes com 11 de 11.

**Terceira armadilha, medida aqui e válida para qualquer roteiro futuro do harness: ESBARRAR
DESREGULA A CADÊNCIA.** Cada aperto do roteiro são 20 quadros segurando mais 60 de folga, o que basta
para UM PASSO, mas a animação de esbarrão é mais longa, então a perna seguinte começa no meio dela e
perde apertos. Foi assim que uma versão já ancorada deu 11 de 11 numa rodada e 10 de 11 na outra: o
jogador parou em (6,6) em vez de (8,6) porque três apertos foram engolidos pelo esbarrão anterior. O
conserto é `espera` (240 quadros, de graça) DEPOIS de toda perna que termina esbarrando, porque ela
devolve o jogador parado e virado, que é o único estado de onde contar tile vale.

**Quarta armadilha, do mesmo tronco: TROCAR DE DIREÇÃO CUSTA UM APERTO.** Medido quadro a quadro: o
jogador parado em (0,2) virado para cima recebeu RIGHT duas vezes e andou UM tile só; andar na
direção que já se encara não cobra nada (UP,3 na coluna 8 andou os três). Por isso cada perna contada
leva "um a mais", e a que termina em cima da porta leva 1 mais os tiles.

Os PNGs foram abertos e olhados: no caso `veilstone`, o quadro da ida é a rua de Veilstone com o
prédio de emblema de Poké Bola, o do meio é o salão de piso laranja da loja, e o da volta é a MESMA
rua de Veilstone, com o jogador em frente à porta. No `lilycove_loja`, o quadro da volta traz o
letreiro **"LILYCOVE CITY"** e a rua de Lilycove: o lado original não mexeu.

**Armadilha medida no caminho, e ela vale para qualquer roteiro futuro:** seta de rota
(`MB_*_ARROW_WARP`) só dispara com a direção SEGURADA e o jogador já VIRADO para ela
(`input->heldDirection && input->dpadDirection == playerDirection`), então o primeiro aperto depois
da meia-volta é gasto virando. Andar N tiles para dentro e N de volta gasta todos os apertos chegando
na seta e nenhum a acionando, e o caso da Rota 218 abriu VERMELHO três vezes por isso, com o jogo
certo. Porta não tem esse problema, porque dispara ao ser PISADA.

#### Os portões da frente da auditoria de warps

Build verde numa worktree ISOLADA (`/private/tmp/claude-501/warps-r13`, HEAD `7b9a11ce64` mais só os
arquivos desta frente), porque a árvore compartilhada tem outras cinco frentes no meio da obra.
**ROM 32.370.128 B, 96,47% de 32 MB**, **EWRAM 86,16% e IWRAM 86,68%**, idênticos aos da 0.t e da 0.u.
O tamanho NÃO é comparável com os 32.360.292 B que a primeira volta desta frente mediu: aquela era
sobre `fccccc0265`, e entre um HEAD e o outro entraram os consertos de outras frentes; o custo desta
frente em si é **negativo em código**, porque ela APAGOU um special duplicado, e o que sobra é
`map.json` e comentário.

**O HEAD andou dez commits entre a build e o commit desta frente** (de `7b9a11ce64` para
`6c1e43f94c`), e a build NÃO foi refeita em cima. Isso é declarado e medido, não presumido:
`git diff 7b9a11ce64..6c1e43f94c` sobre os quinze arquivos desta frente volta VAZIO, ou seja nenhuma
das outras frentes encostou em nada que esta frente mudou. O que os dez commits mudaram em Ecruteak
foi o `scripts.inc` (o sábio da porta do ginásio), e o que esta frente mudou lá foi o `map.json` (o
warp morto do Battle Tower): arquivos diferentes do mesmo mapa.

**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas, 2.252 ids de treinador e
1.717 apelidos: nenhuma flag, var, item, mapa ou índice novo, e `dynamicWarp` já existe no SaveBlock1
desde o Emerald. O único índice que esta frente mexeu é o warp 14 de `EcruteakCity`, que era o ÚLTIMO
da lista e não é destino de ninguém, então remover não desloca índice nenhum.

**Suíte 1.020 de 1.021, ZERO reprovado**, com o T11.3 pulado na varredura (ele só prova algo com duas
ROMs) e **T11 3 de 3 à parte** contra `roms/pokemon-claude-2026-08-18.gba`, cuja fonte velha está em
`/private/tmp/claude-501/t11-r13` (`cf6786b2ae`). **T171 10 de 10** com o special unificado, que é a
prova de que a consolidação não quebrou a frente dos prédios de Johto.

**Como a suíte foi rodada, e por que isso vira lição:** em GRUPO, um `testa_critico.py T<n>` por vez,
com o resultado de cada grupo gravado em disco antes do próximo, porque com seis frentes na máquina a
varredura inteira num processo só foi MORTA por SIGTERM duas vezes no meio (a segunda aos 408 casos,
com zero reprovado até ali). Rodar em grupo é RETOMÁVEL: quem apanha perde um grupo, não a varredura,
e a contagem final se soma dos 110 arquivos de resultado. **Treze grupos abriram vermelho no lote**
(T108, T139, T144, T145, T146, T147, T153, T156, T157, T159, T160, T161 e T162), e os 24 casos deles
são TODOS de par de save, a contenção que a 0.t já tinha medido: o `testa_critico.py` crava o caminho
do `.sav` em `/tmp/claude-501/frenteA/`, e com cinco outras suítes gravando no mesmo arquivo um par
sempre perde. Repetidos com o `.sav` em pasta própria (`/tmp/claude-501/warps-sav/`, uma linha de
`sed` na worktree isolada, NÃO commitada), os treze deram verde: 10/10, 6/6, 9/9, 10/10, 10/10,
12/12, 21/21, 10/10, 11/11, 14/14, 8/8, 7/7 e 3/3. O T171.10, o T169.7 e o T169.8 caíram pelo mesmo
motivo e passaram na repetição isolada. **A dívida continua sendo do `testa_critico.py`** e não desta
frente: enquanto o caminho do `.sav` for absoluto e compartilhado, toda rodada paralela vai piscar
vermelho sem defeito nenhum.
`dev_scripts/prova_portas_compartilhadas.py` **11 de 11, duas rodadas seguidas**, e o caso adversarial
do elevador **4 rodadas seguidas** com o mesmo resultado. `valida_rom.py` com os 2.400 mapas
declarados dentro da ROM. `valida_warp_tile.py --piso 60` em **5.915 de 6.874 (86,0%)**, com Hoenn
93,3%, Kanto 79,4%, Sinnoh 97,7%, Johto 90,8% e Unova 100% (o denominador caiu 1 e as duas
porcentagens subiram 0,1 ponto porque o warp que saiu era MORTO). `valida_conectividade.py` com
**0 warps quebrados** e os mesmos **1.966 de 2.289** mapas alcançáveis do HEAD: os cinco
`destinos_dinamicos` novos mantêm o grafo honesto, já que a ferramenta pula `MAP_DYNAMIC` de
propósito. `dev_scripts/qa/roda_qa.py --demo` verde nas SEIS varreduras (as quatro antigas, a
`lente_portas` da frente das casas e a `lente_warps` desta).

**A lente roda em 0 nas quatro regiões do cartucho 1 na árvore compartilhada E na worktree isolada.**
Na primeira volta desta frente havia um aviso aqui, porque a worktree isolada de então não tinha o
conserto do Trainer Hill e das três Battle Tents e a lente acusava 4 achados em Johto; esse conserto
entrou no HEAD em `40ebe8eedd`, então o aviso morreu: as duas árvores fecham em **0 / 0 / 0 / 0**, e
o que sobra é **Unova 38 e Galar 130**, de outro cartucho.

**ROM de entrega:** `roms/pokemon-claude-2026-09-06n.gba`, md5
`1247141d12eee1548ba2a3cf93ace3e3`, com o `.map` do linker ao lado.

---

### O quarto defeito do playtest: o jogador andava por dentro do cenário, e três ginásios de Sinnoh não tinham porta, 06/09/2026

O Gui, jogando Hearthome: "está zoado o limite dos tiles, estou entrando debaixo
das árvores", "o sprite aparece cortado pela metade em frente à casa", "nem
nessa casa entra". E em Snowpoint: "estou entrando 50% dentro dos lugares".

São DOIS defeitos diferentes com a mesma cara, e por isso duas ferramentas.

#### 1. A célula que apaga o jogador: `dev_scripts/conserta_colisao_sinnoh.py`

O mecanismo é de duas camadas, e está no motor, não no mapa. `DrawMetatile`
(`src/field_camera.c`) manda as entradas 4..7 do metatile para o **Bg1**, e o
comentário do próprio motor diz que essa camada "covers object event sprites".
Só o layer type `METATILE_LAYER_TYPE_COVERED` desvia essa metade para o Bg2. A
colisão, por outro lado, são os 2 bits do `map.bin` e não têm nada a ver com o
tileset. Metatile que desenha coisa sólida por cima do sprite E vem com colisão
0 é o pior dos dois mundos, e é exatamente o que ele viu.

**A régua NÃO é "desenha por cima"**, e isso foi medido antes de escrever
qualquer byte: em `LittlerootTown`, `PetalburgCity` e `RustboroCity` de fábrica
existem dezenas de células andáveis com pixel opaco no Bg1, e todas são
legítimas (beiral de telhado e copa de árvore existem para o jogador passar
ATRÁS, e é isso que dá profundidade ao mapa). Ferramenta que discorda do vanilla
está errada.

A régua que sobrou tem NOVE portões, e o mais caro deles nasceu de um erro:

1. não é célula de EVENTO (warp, placa, item escondido, gatilho, objeto). O item
   escondido de `VeilstoneCity` em (26,24) mora num tile de `MB_NORMAL` que cobre
   o sprite, e a primeira versão fechou o tile DELE e três vizinhos, deixando o
   item impossível de pegar;
2. colisão 0 e 3. comportamento `MB_NORMAL` (isso congela sozinho grama, água,
   porta, seta, escada, gelo, ponte e areia: nada que o motor leia por
   comportamento é tocado);
4. elevação 3, o chão comum. Elevação 15 é o IDIOMA DE PONTE do Emerald, onde a
   passarela cobre o sprite de propósito: sem esta trava a régua queria fechar
   as três pontes da Route 216;
5. é PEÇA e não TERRENO (no máximo 12 células abertas do mesmo metatile no
   layout). A lama do brejo da Route 212 South cobre as duas camadas inteiras e
   aparece em 191 células em fila: fechá-la emparedaria o brejo;
6. a célula é ALCANÇÁVEL, e 7. o layout é EXCLUSIVO da região (sem isso a
   ferramenta vazava para o Hoenn de fábrica: os cinco quartos da Elite dos
   Quatro de Sinnoh vestem os layouts `LAYOUT_EVER_GRANDE_CITY_*_ROOM`);
8. **as DUAS FAIXAS de cobertura**, e 9. o **VETO DO VANILLA**. Os dois abaixo.

**As duas faixas.** Um corte só de pixels NÃO ordena os casos, e isto é o número
que decidiu a ferramenta: o vaso de planta dos portões de Sinnoh
(`gTileset_Pasos` 520 e 538) cobre **138** px de 256 e é decoração legítima, por
onde se passa atrás; a base do muro do templo de Snowpoint (`gTileset_Snowpoint`
568, 569 e 573) cobre **128, 128 e 132** e é defeito de verdade. O legítimo cobre
MAIS que o defeito. Então:

- de **140** px para cima a peça entra sozinha (o arbusto de Hearthome cobre 152,
  o balcão da banca 248, o tronco da Route 209 232): esse tanto apaga o jogador
  esteja ele onde estiver;
- entre **128** e 140 ela só entra se for **BASE DE PAREDE**, isto é, se a célula
  logo ACIMA já for bloqueada. É o que separa a neve encostada no muro (acima
  está o muro) do vaso de planta (acima está o chão da sala).

O 128 não é número redondo escolhido a dedo: o Bg1 é 16x16 px e o sprite é 16x32
com os pés no tile, então 128 de 256 é **exatamente a metade do sprite**, que é a
frase que o Gui usou. E o contra-exemplo continua de fora: o alto do muro da
banca de Hearthome (640) cobre 118.

**O veto do vanilla.** Quando existe prova EXTERNA de que a peça é chão, ela ganha
do corte, e a prova externa mais forte que este repo tem é o Hoenn de fábrica.
Medido em 06/09/2026: os ginásios de Veilstone e de Sunyshore vestem
`gTileset_DewfordGym` e `gTileset_MauvilleGym`, e a faixa de baixo queria fechar
**39 células** deles; os mesmos metatiles (530, 531, 533, 534, 536, 546, 547...)
aparecem ANDÁVEIS no ginásio de Dewford e no de Mauville de fábrica, dezenas de
vezes. O veto derrubou os 39, e com eles as 23 células de interior que a régua
anterior (corte único de 140, sem veto) tinha escrito em salas de ginásio e de
condomínio. Tileset que só Sinnoh usa (Snowpoint, Hearthome, Jubilife, Canalave)
não tem prova externa nenhuma, e aí quem decide é a cobertura.

**A guarda.** Depois de cada bloqueio o conjunto alcançável tem que perder
EXATAMENTE as células corrigidas, nem uma a mais; a que cortar corredor é
devolvida. Medido depois de aplicar, nos 26 mapas mudados: **0 células perdidas
por tabela e 0 eventos (warp, objeto, placa, gatilho) que tenham ficado
inalcançáveis**. `completude.py --detalhe sinnoh` fecha em 100,0% mapas / 100,3%
objetos / 103,7% warps / 103,4% placas, igual a antes.

A ferramenta escreve SÓ os 2 bits de colisão, `(antigo & ~0x0C00) | 0x0400`.
Metatile e elevação saem byte a byte idênticos, o que o `--demo` confere célula a
célula, e ela é idempotente (a segunda execução dá 0).

**401 células em 26 `map.bin`**, todas de Sinnoh:

| mapa | células |
|---|---|
| `OreburghCity` | 93 |
| `HearthomeCity` | 40 |
| `OreburghMine_B1F` | 38 |
| `VeilstoneCity` | 36 |
| `Route212_South` | 30 |
| `SunyshoreCity` | 28 |
| `Route209` | 26 |
| `EternaCity` | 24 |
| `Route206` | 18 |
| `HotelGrandLake` | 12 |
| `FloaromaTown` | 9 |
| `SnowpointCity` | 7 |
| `SolaceonTown` | 4 |
| `CelesticTown` | 4 |
| `PastoriaCity` | 4 |
| `CanalaveCity` | 4 |
| `MtCoronet_1F_South` | 4 |
| `Route210_South` | 3 |
| `Route212_North` | 3 |
| `ValleyWindworks` | 3 |
| `JubilifeCity` | 2 |
| `Route210_North` | 2 |
| `Route214` | 2 |
| `Route218` | 2 |
| `Route206_North` | 2 |
| `Route206_South` | 1 |

#### 2. O warp que não estava em cima da porta: `dev_scripts/conserta_portas_sinnoh.py`

`valida_warp_tile.py` já listava 18 warps mortos em Sinnoh, e ninguém tinha lido a
lista pelo nome do DESTINO: **cinco eram a porta de um GINÁSIO** (Hearthome,
Pastoria, Canalave, Snowpoint e Sunyshore). Ginásio com warp morto é ginásio
inalcançável, e o capítulo que o Gui está jogando é o "before Fantina", cujo
ginásio é o de Hearthome.

A regra é "mover o warp, não a porta", e o ÍNDICE do warp nunca muda (outro mapa
aponta para ele por `dest_warp_id`), só o par x,y. Um warp morto só é consertado
quando o próprio mapa responde onde a porta está, por um de dois caminhos:

| mapa | warp | de | para | como |
|---|---|---|---|---|
| `HearthomeCity` | 4 | (29,26), chão de praça | (10,31) | boca única: o metatile 636 de `gTileset_Hearthome` aparece UMA vez no repo inteiro, é o arco de pedra da fachada que escreve GYM, e o atributo dele virou `MB_NON_ANIMATED_DOOR` |
| `PastoriaCity` | 1 | (34,30), grama | (27,34) | porta livre a 7 de distância, a do prédio da esquerda (o da direita já era do warp 7) |
| `SnowpointCity` | 0 | (17,34), `MB_SAND` | (17,33) | porta livre a 1 de distância, o clássico erro de um tile |

A boca de Hearthome **não é automática**, e está escrito no código por quê: a
régua de "boca única" sozinha achou TRÊS candidatos em Sinnoh
(`gTileset_Hearthome` 636, `gTileset_Sunnyshore` 657 e `gTileset_CaveSinnoh` 931),
todos com metatile de uso único no mundo, e os PNG foram abertos e olhados: só o
primeiro é porta, os outros dois são fenda de rocha e parede de caverna. A tabela
`BOCAS_MEDIDAS` guarda o julgamento e o código só CONFERE que ele continua
valendo; se o mapa mudar, a conferência falha em vez de escrever no lugar errado.

Os outros **15 warps mortos de Sinnoh ficaram de fora de propósito** e estão
listados pelo relatório: Canalave 1 e Sunyshore 1 (warp sobre `MB_OCEAN_WATER`,
sem porta livre; qual porta é do ginásio ali é decisão de conteúdo, não medida),
os dez da Elite dos Quatro (warp em tile sólido é o IDIOMA da Elite, ESTADO 0.t) e
os de caverna e floresta, onde não existe porta desenhada para achar.

#### A prova, e ela é no emulador

`dev_scripts/testes_criticos/176_colisao_sinnoh.json`, **12 casos, 12 verdes**,
todos com `gba_runner` e leitura da EWRAM, nunca de pixel:

| caso | o que prova |
|---|---|
| T176.1 | Hearthome: RIGHT saturante na linha 20 para em (19,20), ao lado do balcão da banca. Antes parava em (20,20), DENTRO dele |
| T176.2 | Hearthome: LEFT saturante na linha 16 encosta em (18,16). Antes terminava em (17,16), dentro do arbusto |
| T176.3 | Hearthome: pisar no arco de (10,31) leva ao ginásio da Fantina |
| T176.4 a .6 | três casas de Hearthome (Poffin, noroeste e sudeste) entram E saem, voltando no mesmo tile |
| T176.7 a .9 | os três portões (Route 208, 209 e 212) levam |
| T176.10 | Snowpoint: o UP em (13,8) não sobe mais para dentro do muro do templo |
| T176.11 | Snowpoint: a fachada do ginásio fecha, e o jogador para em (14,33) |
| T176.12 | Snowpoint: (17,33) leva ao ginásio |

Fato do motor que custou seis casos e fica registrado: **o primeiro toque numa
direção NOVA só VIRA o jogador, não anda**. Por isso toda perna contada tem um
toque a mais que a distância, e as pernas de 20 são saturantes para não depender
disso. E os portões de cidade são `MB_WEST/EAST/SOUTH_ARROW_WARP`: seta só
dispara quando o jogador ANDA NA DIREÇÃO DELA (`TryArrowWarp`), então nascer em
cima dela pelo menu de debug não warpa nada.

#### O que foi rodado, e o que ficou pela metade

- **Build verde** na worktree `/private/tmp/claude-501/colisao-r13b`, ROM em
  `roms/pokemon-claude-2026-09-06r.gba` com `.map` ao lado, md5
  `87f59f2912844fd05ff906ef605e6927`, 33.554.432 B.
- `valida_rom.py`: **2.400 mapas e 2.054 layouts, tudo que foi declarado entrou**.
- `guarda_save.py`: **SAVE COMPATIVEL**, `SaveBlock1` em 14.964 B de 15.872
  (94,3%), inalterado (esta frente não encostou em nenhum `.c` nem `.h`).
- `qa/roda_qa.py --demo`: **verde nas cinco varreduras** desta árvore.
- `completude.py --detalhe sinnoh`: **100,0% mapas / 100,3% objetos / 103,7%
  warps / 103,4% placas**, igual a antes do conserto.
- **T11 completo 3/3**, contra a baseline certa: `--rom
  roms/pokemon-claude-2026-08-15c.gba --src` uma worktree em `d6b8c9e898` com
  `make generated` rodado e os binários de `tools/` copiados, mais `--abertura
  intro_carvalho`. **Armadilha medida hoje**: o `.sav` do caso mora no `TMPDIR`, e
  rodar o T11 duas vezes com `TMPDIR` sujo faz o T11.3 ler a save da execução
  ANTERIOR e reprovar com a mensagem errada (aqui deu "obtido MAP_SANDGEM_TOWN"
  com a flag acesa, que é o retrato de uma save que carregou). Apagar o `TMPDIR`
  antes é parte do procedimento, não zelo.
- **`dev_scripts/testes_criticos/176_colisao_sinnoh.json`, 12 de 12**.
- **A suíte inteira NÃO fechou nesta sessão, e isso fica dito.** A máquina estava
  com SEIS frentes rodando emulador ao mesmo tempo e o ritmo caiu de 5,4 para 1,6
  casos por minuto; três execuções do `testa_critico.py` inteiro foram mortas por
  fora (código 144) antes do fim, a mais longa em **135 casos, 0 reprovados**.
  Ficou montado um jeito de retomar sem perder o andado, e ele é o que a próxima
  sessão deve usar: `python3 -u /tmp/claude-501/suite_resumivel.py >>
  /tmp/claude-501/suite-colisao.log`, que lê o log, pula todo caso que já tem
  linha `[OK   ]` ou `[FALHA]` e roda só o resto; num laço, ele fecha a suíte em
  quantas retomadas forem precisas. Até o ponto em que esta linha foi escrita:
  **0 reprovados**.

#### O que fica aberto na colisão de Sinnoh

- **A comparação com a fonte DPPt foi feita e não achou quase nada.** Os 62
  layouts de Sinnoh que existem em `fontes-mapas/sinnoh/` com o mesmo tamanho e o
  mesmo metatile têm **11 células** em que a fonte bloqueia e nós não (6 em
  `RavagedPath`, 2 em `SnowpointCity`, 1 em `FloaromaTown`, 1 em
  `MtCoronet_1F_North_Room1`, 1 em `Route204`), e **nenhuma** no sentido
  contrário. Ou seja: a colisão do demake está fiel à fonte, e o defeito que o
  Gui viu **também está na fonte**. Comparar com o demake não teria achado nada;
  quem achou foi a régua de cobertura. As 11 não foram tocadas nesta rodada
  (`SnowpointCity` (16,7) e (17,7) são as portas animadas das duas casas do
  norte, que em Hoenn seriam sólidas de propósito).
- **`fontes-mapas/pokeplatinum` não foi usada.** Lá o mapa é 3D (NSBMD mais bytes
  de permissão), a grade não é 1:1 com a do demake 2D, e decodificar isso é obra
  própria.
- **Nove `map.bin` são compartilhados com a frente de ARTE das cidades.** O commit
  desta frente leva a versão SÓ de colisão (regerada do HEAD), e a árvore de
  trabalho ficou com a mescla (decoração da arte + os bits de colisão daqui), para
  que a frente de arte não perca o que ainda não commitou. Conferido: nas 8 que a
  arte mexeu, nenhuma célula minha caiu em metatile que ela trocou.
  **FECHADO em 07/09/2026:** a frente de arte commitou em `8c82badf58` e a árvore
  está limpa; a mescla que estava fora do controle de versão entrou inteira.
- **`Route206_North` (0,5)**: é o mesmo vaso de planta de (0,2), e fica ANDÁVEL
  porque acima dele há chão. A régua recusa onde não consegue provar, e isso é de
  propósito.

### As casas pretas de Goldenrod: a POSIÇÃO no array de paleta É o slot, 06/09/2026

O Gui mandou a foto de uma cena noturna em Goldenrod City com um prédio de topo branco e corpo
inteiro PRETO, só as janelas aparecendo, com os vizinhos normais. Não era arte, não era o DNS e não
era o `metatiles.bin`: era a **ORDEM do array de paleta**. `LoadTilesetPalette`
(`src/fieldmap.c:1035`) copia `tileset->palettes[numPalsInPrimary]` **em bloco**, então a POSIÇÃO da
linha dentro de `gTilesetPalettes_X` É o slot de paleta que o jogo carrega. E
`dev_scripts/importa_tilesets_johto.py` montava esse array com `sorted(os.listdir(...))`, emitindo
também os `.pal` que NÃO são slot: a camada de luz noturna do hns (`08_over.pal`, `09_over.pal`,
`10_over.pal`, `12_over.pal`) e o `bellchime_12.pal`.

Em `gTileset_Goldenrod` o array tinha **20 linhas em vez de 16**, e `08_over.pal` caía na posição 9.
Johto é `layout_version: "johto"`, ou seja `bigPrimary`, com 7 paletas no primário, então o
secundário ocupa os slots 7 a 12. O que o motor carregava, medido linha a linha:

| slot do jogo | arquivo que entrava | arquivo certo |
|---|---|---|
| 7 | `07.pal` | `07.pal` |
| 8 | `08.pal` | `08.pal` |
| **9** | **`08_over.pal`** (12 das 16 cores são `0 0 0`) | `09.pal` |
| 10 | `09.pal` | `10.pal` |
| **11** | **`09_over.pal`** (13 das 16 cores são `0 0 0`) | `11.pal` |
| 12 | `10.pal` | `12.pal` |

Preto é preto com qualquer tingimento, então o defeito **não depende da hora**: a foto do Gui é de
noite porque ele jogou de noite. Medido no `LAYOUT_GOLDENROD_CITY` (58x46): **151 blocos de 2.668, em
84 metatiles distintos, usam os slots 9 ou 11** e saíam pretos, e outros **1.061 blocos usam o slot
12**, que saía com a cor do `10.pal`, errada mas não preta (é o toldo que estava branco em vez de
amarelo). `Route34` e `Route35` compartilham o tileset e não colocam nenhum metatile dos slots
pretos, e por isso ninguém tinha reclamado deles. Elas não saíram ilesas: contado bloco a bloco,
`Route34` tem **389 de 5.400 blocos no slot 12 e 1 no slot 10**, ou seja cor trocada e não preto, e
`Route35` usa o secundário em **1 bloco só**, nenhum dos slots deslocados. São esses três mapas, e
mais nenhum, que mudam de cor com este conserto: `LAYOUT_GOLDENROD_CITY`, `LAYOUT_ROUTE34` e
`LAYOUT_ROUTE35` são os únicos layouts do repo com `gTileset_Goldenrod` como secundário, e
`LAYOUT_RUINS_OF_ALPH_OUTSIDE` é o único com `gTileset_RuinsOfAlphOutside`.

**A varredura do repo inteiro achou quatro arrays desalinhados, e só um era defeito visível.**
`Goldenrod` e `RuinsOfAlphOutside` divergem a partir da posição 9; `Route32` e `VioletCity` têm
`bellchime_12.pal` na posição 13, que é além do `NUM_PALS_TOTAL` de 13 e por isso o motor nunca lê.
`RuinsOfAlphOutside` estava desalinhado e mesmo assim correto na tela: **0 de 2.208 blocos** do mapa
dele usam os slots pretos, e é por isso que ele virou o CONTROLE da prova, e não um segundo conserto.
Os outros dois geradores de tileset (`tileset_gen2.py` e `tileset_galar.py`) emitem
`palettes/{i:02d}.pal` com `range(16)` e nunca podiam cair nisso.

**O conserto é na raiz, no gerador.** `importa_tilesets_johto.py` passou a aceitar só `NN.pal`,
ordenar por NÚMERO e cobrar que a sequência comece em 00 e não tenha buraco, tanto na hora de copiar
do hns quanto na hora de emitir o `INCGFX`. O `--demo` dele ganhou a invariante que faltava, e ela é
sobre o `graphics.h` INTEIRO e não só sobre o bloco que o script escreve: posição tem que ser igual
ao número do arquivo, nenhum array pode ter menos de 13 slots, e ela recusa rodar se examinar menos
de 280 arrays. Calibrada dos dois lados: no `graphics.h` de `7b9a11ce64` ela para no primeiro,
`gTilesetPalettes_Goldenrod: a posicao nao e o slot; posicao 9 carrega '08_over.pal'`, e na árvore
desta rodada passa. As 8
linhas de `.pal` que não são slot saíram do `graphics.h` e os 8 arquivos saíram do disco (todos
reprodutíveis a partir do hns em `fontes-mapas/hns`), para que o disco e a tabela digam a mesma coisa
e nenhuma outra ferramenta tropece neles de novo. Custo de ROM medido no `.map`, e não deduzido:
`gTilesetPalettes_Goldenrod` cai de `0x280` para `0x200` bytes (20 paletas para 16), e as 8 linhas
das quatro tabelas somam **256 B a menos**.

**A lente que parecia óbvia foi tentada, medida e RECUSADA**, e a medida está escrita dentro do
`prova_paletas_goldenrod.py` para ninguém refazer o caminho: "procurar metatile colocado num mapa cujo
slot de paleta sai TODO preto" **não pega este defeito**. Rodada com o `graphics.h` de `7b9a11ce64`
nos **2.053 layouts** que têm blockdata em disco, ela não acusa Goldenrod, porque `08_over.pal` tem
12 cores pretas e **4 amarelas**, que são as janelas acesas, e portanto não é "toda preta". De quebra
ela acusa **56 layouts de Kanto, Hoenn e Galar com tileset VANILLA**, que precisariam de calibração
contra o `pret/pokeemerald` intocado antes de virarem cobrança. Duas razões para não existir: não
acha o que esta rodada consertou, e acenderia vermelho permanente. Quem pega o defeito é a invariante
de ORDEM, e ela examina os **288 arrays** de `graphics.h` mais `graphics.c`, nas três formas em uso
(com e sem `ALIGNED(4)`, com o arquivo em `.pal` ou já em `.gbapal`); uma regex mais estreita
examinaria 70 dos 288 e daria verde por não ter olhado. Contado nesta rodada: **70 declarações
levam `ALIGNED(4)` e 227 não levam**, e **9 arrays entram por `INCBIN_U16` contra 279 por
`INCGFX_U16`**, que são exatamente as três formas que a regex larga precisa cobrir.

**A prova é do emulador, com par antes/depois e um controle**
(`dev_scripts/prova_paletas_goldenrod.py`). Cor não mora em EWRAM que se leia por símbolo, então a
prova é o PNG, medido e não olhado: o roteiro warpa por debug e a ferramenta conta quanto da metade
de cima da tela é PRETO PURO. Na ROM `2026-09-05`, que é a que o Gui jogou, a porta da Radio Tower
(warp 7) dá **38,5% de preto** e o Game Corner (warp 10) dá **13,0%**; nesta build dão **0,9%** e
**0,3%**. `RuinsOfAlphOutside` mede **0,2% nas duas**, que é o controle. As quatro medidas saíram
com minutos de diferença e portanto na mesma faixa de hora do DNS, que é o que fecha a comparação;
o `gba_runner` não tem opção de relógio, então a hora é a da máquina, e **o defeito aparece de dia
também**, porque preto continua preto depois de qualquer tingimento. Aviso para quem repetir: as
frações variam cerca de **0,1 ponto** entre rodadas em horas diferentes, justamente por causa do
tingimento, e por isso o teto do caso é 12% e não um valor colado na medida.

**E tem uma terceira camada, lida do BINÁRIO e não da tela.** `gTilesetPalettes_Goldenrod` está em
`0x08f18a98` na ROM `2026-09-05` e em `0x08f1b298` nesta, os dois endereços tirados do `.map`. Lendo
32 bytes por slot: na ROM velha o **slot 9 tem 12 das 16 cores em `0x0000`** e o **slot 11 tem 13**;
nesta, os slots 9, 11 e 12 têm **zero** cor preta. É a mesma afirmação medida em três lugares
diferentes, arquivo de dados, binário e framebuffer.

**Efeito colateral, achado no caminho: `render_maps.py` nunca tinha conseguido desenhar Goldenrod.**
Ele lia o nome do `.pal` com `int()` cru e morria com `invalid literal for int() with base 10:
'12_over'`. Agora ele filtra por `^\d{2}\.pal$`, que é a mesma regra do gerador. Medido dos dois
lados, com os quatro `_over.pal` de volta no disco só para a medida: o script de `7b9a11ce64` morre
com essa mensagem e desenha **0 mapas**, e o desta rodada desenha `GoldenrodCity` inteiro. O render
de disco de `GoldenrodCity` tem **0,00% de preto puro** em 928x736 px, e é ele que separa as duas
hipóteses do diagnóstico: a arte no disco sempre esteve certa, e quem errava era a tabela. O render
lê a paleta pelo NÚMERO do arquivo e o jogo lê pela POSIÇÃO no array, e é a invariante de ORDEM que
passou a garantir que as duas leituras digam a mesma coisa; enquanto ela estiver verde, render e ROM
não podem mais divergir.

**Os portões desta frente.** Build verde numa worktree própria (`/private/tmp/claude-501/goldenrod-wt/tree`,
HEAD `7b9a11ce64` com só os arquivos desta frente por cima), **ROM 96,47% de 32 MB, EWRAM 86,16%,
IWRAM 86,68%**. **Suíte 1.020 de 1.021**, com o T11.3 pulado na rodada normal e **T11 3/3 rodado à
parte** contra `roms/pokemon-claude-2026-08-18.gba` (fonte na worktree de `cf6786b2ae`, em
`/private/tmp/claude-501/t11-r13`). `guarda_save.py` **SAVE COMPATIVEL** (SaveBlock1 em 14.964 de
15.872 B, 2.400 mapas), `valida_rom.py` com os **2.400 mapas declarados dentro da ROM**,
`roda_qa.py --demo` verde nas cinco varreduras, `importa_tilesets_johto.py --demo` e
`prova_paletas_goldenrod.py --demo` verdes. ROM entregue:
`roms/pokemon-claude-2026-09-06v.gba`, md5 `19e10798c6e0029a86a4f0264c20f72c`, com o `.map` ao lado.
A letra é `v` e não `k` porque `k` já era de outra frente da mesma rodada; confira a lista de `roms/`
antes de escolher a sua.

**O que fica aberto.** A cobrança desta classe é ESTÁTICA (a invariante de ordem no `--demo`) mais
uma ferramenta de emulador rodada à mão (`prova_paletas_goldenrod.py`); ela **não** entrou na suíte
crítica, porque `testa_critico.py` só afirma fato lido da EWRAM e cor de tileset mora na PLTT de BG
(`0x05000000` a `0x050001FF`). O caminho pronto para fechar isso é o mesmo que fechou os NPCs verdes
de Kanto em 12/08/2026: o `gba_runner` ganhou `--palobj` para a PLTT de OBJ e uma prova
`palobj_presentes`; falta o gêmeo de BG. Enquanto ele não existir, paleta de tileset trocada em mapa
que ninguém fotografar continua passando pela suíte inteira.

### Ecruteak e Burned Tower: o sábio que trancava o ginásio, e a cena dos três cães que nunca existiu, 06/09/2026

O Gui, no playtest: "em Ecruteak City não achei o evento que dispara os cães lendários, não achei o
rival, não tem nada para fazer lá, e aí o ginásio fica travado". As três queixas são **um defeito só**,
e ele é de FLAG, não de mapa.

**A trava, medida antes de tocar.** O objeto 1 de `data/maps/EcruteakCity/map.json` é um
`OBJ_EVENT_GFX_MR_FUJI` em **(20,49)** com `FLAG_HIDE_ECRUTEAK_CITY_SAGE` no campo `flag`. A porta do
ginásio é **(20,48)**, e a linha 48 do `map.bin` de `LAYOUT_ECRUTEAK_CITY` é parede de x=19 a x=22:
**(20,49) é o único tile de onde se entra**. E `FLAG_HIDE_ECRUTEAK_CITY_SAGE` **não era acesa nem
apagada por nenhum script do repositório**: o único uso dela em `data/`, `src/` e `include/` era o
campo `flag` do próprio objeto. Objeto é sólido, então o sábio nascia sempre e o ginásio do Morty
ficava trancado **para sempre**.

**Por que a corrente inteira estava rompida.** No hns o mesmo sábio sai do caminho em
`BurnedTower_B1F/scripts.inc:123` (`setflag FLAG_HIDE_ECRUTEAK_CITY_SAGE`), no fim da cena em que os
três cães acordam, e essa cena era `ON_FRAME_TABLE` em `VAR_ECRUTEAK_CITY_STATE`. Essa var foi CORTADA
no import ("ponytail: o enredo de var do hns foi cortado", cabeçalho de `EcruteakCity_Gym/scripts.inc`),
e com ela foram a cena, a flag e o destravamento. Sobraram no B1F três objetos de decoração parados
(`ENTEI` em (18,8), `RAIKOU` em (14,8), `SUICUNE` em (16,9), as mesmas coordenadas do hns) com
`script: 0` e `flag: 0`, dentro de uma **câmara selada** de paredes (x de 14 a 18, linhas 8 e 9).

#### O conserto: UMA flag, e ela é o arco inteiro

`FLAG_JOHTO_CAES_LIBERTOS` (`FLAG_UNUSED_0x4DB`, apelido novo em append; o bloco 0x270-0x28F do SILVER
já estava cheio). **Zero var**, e a mesma flag faz três coisas: é o campo `flag` dos três objetos do
trio no B1F (acesa, eles não nascem); é o que `EcruteakCity_OnTransition` lê para **RECALCULAR**
`FLAG_HIDE_ECRUTEAK_CITY_SAGE` a cada entrada no mapa (técnica 2 do `SINNOH-PADRAO.md`, a mesma do
SILVER que já morava duas linhas abaixo no arquivo); e é o que o seletor de capítulo acende ao pular
para "Before MORTY".

O fluxo, em cinco elos, e só o quarto é novo:

1. **Ecruteak**: o sábio na porta manda o jogador à BURNED TOWER (fala do hns, já estava lá).
2. **Burned Tower 1F**: o `ON_TRANSITION` já mostrava o SILVER entre a vitória de Azalea
   (`TRAINER_JOHTO_RIVAL_SILVER_2`, 1359) e a daqui (`SILVER_3`, 1360). O objeto fica em (15,19)
   virado para baixo com raio 3 e o warp de entrada larga o jogador em (15,22): três tiles dentro do
   cone, o duelo dispara sozinho, sem roteiro de movimento.
3. **O chão cede** depois do duelo: `ShakeCamera`, `SE_FALL` e `warp MAP_BURNED_TOWER_B1F, 16, 12`.
   Por que `warp` de coordenada fixa e não `warphole`: MEDIDO em `src/scrcmd.c`, `warphole` com mapa
   explícito leva o jogador para a coordenada em que ELE está, e depois da abordagem do SILVER ele
   está por volta de (15,20); o B1F tem altura 19, então "a mesma coordenada" cairia FORA do mapa.
4. **B1F**: `ON_FRAME_TABLE` em `VAR_TEMP_0 = 0` roda a cena na chegada; os três acordam, gritam,
   fogem e somem, com os movimentos do hns. Dez `coord_event` em `VAR_TEMP_1 = 0` nas lajes de frente
   para a câmara (x de 14 a 18, linhas 11 e 12) são a rede de segurança de quem chegar pela ESCADA de
   (26,7) em vez de pela queda. **Zero var de save nas duas**, técnica do `SINNOH-PADRAO.md`.
5. **De volta a Ecruteak**: o sábio não nasce, (20,49) fica livre, o ginásio abre.

**O seletor de capítulo ganhou `flagEnredo`** (`src/chapter_jump.c`), um campo no FIM da
`struct GinasioDoHack`, então as outras 39 linhas não mudaram uma vírgula e ficam com 0 por omissão. O
laço novo usa `i < capitulo`, e não `i + 1 < capitulo`, porque a cena que abre a porta do ginásio `i` é
pré-requisito DELE: "Before MORTY" já precisa dela acesa. Ele também **APAGA** a flag nos capítulos
anteriores, senão pular de uma save adiantada para "Before FALKNER" deixaria Ecruteak sem o sábio que
ainda deveria estar lá.

**A armadilha do `ON_FRAME_TABLE`, que vale para a próxima rodada:** `TryRunOnFrameMapScript` é chamado
A CADA QUADRO por `ProcessPlayerFieldInput` (`src/field_control_avatar.c:195`) e devolve `TRUE`, que
congela o jogador. Roteiro de `ON_FRAME` que não mata a própria condição **na primeira instrução**
trava o jogo. Por isso `setvar VAR_TEMP_0, 1` é a primeira linha do roteiro do porão.

**Zero regressão no Raikou e no Entei de Dex do B1F**: são objetos DIFERENTES, em (26,12) e (24,4), com
`FLAG_HIDE_DEX_*` própria, e continuam sendo batalha de lendário. E fica um **registro medido que
desmente um comentário antigo** do `BurnedTower_1F/scripts.inc`: o buraco do hns existe nesta build
(o offset do tileset secundário aqui é **640**, e não 512, então `0x37E` é o índice **254** de
`gTileset_BurnedTower`, atributo `MB_MT_PYRE_HOLE`). Não foi usado porque `MB_MT_PYRE_HOLE` não passa
pelo `warp_event` do mapa: ele chama `EventScript_FallDownHoleMtPyre`, que usa o warp de buraco FIXO
(`setholewarp`), outro mecanismo. O `warp_event` de (16,12) do 1F continua inerte (metatile 0x280,
`MB_CAVE`), e trocá-lo fica como polimento.

#### A música do farol

`MUS_HG_LIGHTHOUSE` apontava para `MUS_SLATEPORT`: o farol de OLIVINE tocava música de CIDADE DE PRAIA
por dentro. Passou a `MUS_RG_POKE_TOWER` (518, faixa com número e `.s` próprios), interior de torre
alta. **Uma linha.** O apelido também serve os **oito mapas de MT SILVER**, que pela mesma troca saem
de música de cidade para música de torre.

#### A prova é do emulador, e o par negativo está em quatro dos oito casos

`prova_musica_johto.py` ganhou dois casos e fecha **11 de 11**: nesta build o `OlivineCity_Lighthouse`
e o `MtSilver_2F` leem **518** no `gMapHeader.music` E no `gMPlayInfo_BGM.songHeader`, contra os **433**
(Slateport) que a ROM `pokemon-claude-2026-09-06` lia, a que o Gui jogou. Os outros nove leem igual nas
duas, `PetalburgCity` incluso, que é o controle de Hoenn.

Os oito casos novos são `dev_scripts/testes_criticos/170_ecruteak_burned_tower.json`, **8 de 8**. O
**T170.8 é o primeiro caso deste projeto que JOGA UMA BATALHA ATÉ O FIM**, o que o ESTADO 0.c
registrava como limite do harness: o seletor entrega o PIKACHU nível 20 a quem salta com party vazia, a
opção de teste **LV.5 TRAINERS** (byte 36 em `opcoes`) põe os cinco Pokémon do SILVER_3 em nível 5, e um
tapete de apertos de A joga a luta inteira. Ele prova o fluxo de ponta a ponta num roteiro só: vitória,
chão cedendo, queda em (16,12), cena dos cães, e `FLAG_JOHTO_CAES_LIBERTOS` acesa com o mapa final
sendo o porão. O T170.1 mede a trava com o jogador parando em **(20,50)**, um tile abaixo do sábio, e o
T170.2 muda UMA coisa (a flag) e o mesmo roteiro entra no ginásio.

## 0.t A CAÇA A BUGS ANTES DO PLAYTEST: A RÉGUA PARA DE MEDIR PORCENTAGEM E PASSA A MEDIR DEFEITO, 23/08/2026 (rodada 12; condutor Opus, quatro executores Opus, fechador Opus)

Build verde, uma build só, e a primeira rodada em que **nenhuma coluna de completude era o alvo**: o
que a régua não mede é jogo travando, cena abrindo na pessoa errada, texto cortado e mapa alcançável
no papel e intransitável no cartucho. **A varredura de QA caiu de 39 travas para 22 e de 2.244
prováveis para 1.972**, e as quedas são obra e medição, não recalibragem de conveniência.

**ROM 96,41% de 32 MB** (32.350.596 B, **1.203.836 B livres**, 10.120 B a mais que a 0.s), **EWRAM
86,16% e IWRAM 86,68%**, idênticos aos da 0.s, **Dex obtenível 1.571 de 1.571 e ZERO inobtenível**.
**Suíte 1.002 de 1.003, ZERO reprovado**, com o T11.3 pulado na varredura (ele só prova algo com duas
ROMs); a varredura inteira foi REFEITA pelo fechador sobre a ROM `23d` e deu o mesmo 1.002/1.003, com
**T143.9 verde**, que antes já tinha sido rodado sozinho CINCO vezes e passado nas cinco. **T11 3/3**
contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`). Blocos novos: **T163 4/4, T164 4/4, T165 10/10, T166 4/4, T167 5/5, T168 5/5** (dois do
Deoxys) e **T169 8/8**, o adversarial. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%),
**2.054 layouts e 2.400 mapas**, os 2.400 dentro da ROM, 2.252 ids de treinador e 1.716 apelidos
conferidos; `guarda_colisao_vars` com 23 colisões herdadas, **0 novas** e 0 stub;
`valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em 5.915 de 6.875
(86,0%), nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com `'sprite': 0` e 0 mapas
com problema; os quinze `--demo` de ferramenta tocada verdes, mais `dev_scripts/qa/roda_qa.py --demo`
nas quatro varreduras. ROM oficial **`roms/pokemon-claude-2026-08-23d.gba`**
(md5 `b6cdb072b9fd904215c21a544df389d8`), com o `.map`, e o MESMO binário em
`roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | 101,5% | 103,7% | 103,5% | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 103,6% | 100% | 70,3% | 59,2% | 48 (32) | 0 |

### Três lentes, e a tabela de QA antes e depois

**(1) A varredura estática** (`dev_scripts/qa/`, quatro ferramentas, 8.746 achados no começo) lê a
árvore e acha CANDIDATO em escala. **(2) O emulador** (`testa_critico.py`) roda o jogo e lê a EWRAM, e
PROVA o fato. **(3) O olho no framebuffer**, o PNG que o `gba_runner` grava, aberto e olhado, a única
que responde "a caixa está desenhada e a linha cabe". Nenhuma substitui a próxima. Abaixo,
`roda_qa.py`, a MESMA ferramenta, em `010cc1dd67` e na árvore desta rodada:

| classe | Kanto | Johto | Hoenn | Sinnoh | Unova | Galar | comum | total |
|---|---|---|---|---|---|---|---|---|
| trava, antes | 5 | **19** | 2 | 0 | 0 | 0 | 13 | **39** |
| trava, depois | 5 | **2** | 2 | 0 | 0 | 0 | 13 | **22** |
| provável, antes | 373 | 108 | 811 | 130 | 141 | **264** | 417 | **2.244** |
| provável, depois | 359 | 104 | 759 | 121 | 137 | **76** | 416 | **1.972** |
| cosmético, antes | 718 | 449 | 1.538 | 2.085 | 1.154 | 475 | 42 | 6.461 |
| cosmético, depois | 718 | 444 | 1.538 | 1.929 | 1.154 | 474 | 42 | 6.299 |
| falso positivo | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| falso positivo, depois | 11 | 0 | 48 | 0 | 0 | 0 | 2 | **61** |

As duas linhas que mais andaram dizem onde a obra foi: **Johto perdeu 17 das 19 travas** e **Galar
perdeu 188 prováveis**.

### As quatro frentes

**Galar.** Os 127 blocos `nointro` (`lock`/`faceplayer`/`goto_if_set`/`trainerbattle_no_intro`/`end`)
viraram `trainerbattle_single` + `msgbox GalarTrn_Depois_*` + `release`. **108 objetos dividiam id de
treinador** e por isso nasciam vencidos junto com o gêmeo; a numeração passou a ser por OBJETO, ids
publicados intactos e **60 ids novos em append, 3208 a 3267**. Alocadores de flag e var viraram
append-only com os 16 endereços repostos nos da 22f, e `guarda_save.py` ganhou guarda de apelido.

**Johto.** Sete travas de verdade na raiz, `release` e `waitstate` fora de ordem. Ho-Oh, Lugia e
Deoxys tinham UMA flag de esconder pendurando dois ou três objetos em regiões diferentes; cada mapa
ganhou apelido na faixa 0x1BB4, custo zero de var. Unown invisível em tile sólido, e três espécies da
Dex realocadas para mapa vivo.

**Sinnoh.** **203 textos requebrados por pixel**, contra a caixa de 208 px e não por contagem de
caractere. O rival do Pokecenter da Liga voltou **na posição 7 da lista**, e não no fim, porque
`local_id` sem nome é a POSIÇÃO mais um: com ele fora, o `addobject 7` da cena mirava a PICNICKER do
canto, que fazia o "!", andava até o jogador, lutava como BARRY e sumia do mapa para sempre. Três
NPCs ligados por `ON_TRANSITION`, `VerityLakefront` com `warp`/`waitstate`/`releaseall` na ordem
canônica, `GalacticHQ_Hall` de 34 para 15 objetos na janela e `Restaurant` de 19 para 15, e 69
túmulos repovoados limpos.

**Resto.** O seletor de capítulo passou a acender **FLAG_BADGE01..08_GET por ÍNDICE**: os oito golpes
de campo perguntam por elas e mais nada (`src/field_move.c`), e a coluna `flagInsignia` do seletor só
É a insígnia do motor em KANTO, então quem pulava para "Before CANDICE" ganhava um Pikachu com Surf,
Rock Smash e Strength que o motor RECUSAVA em cinco das seis regiões. Capítulo 0 continua sem insígnia
(T99 2/2). Twist Mountain portada no gerador, Driftveil por `ON_TRANSITION`, três `dual_connection` de
Unova consertadas (15 órfãos para 3), e a QA promovida para `dev_scripts/qa/`.

### Os falsos positivos PROVADOS (a régua não via o mecanismo)

**Azalea e Blackthorn**: quem tira o jogador dali é `applymovement`/`setmetatile`, e a régua procurava
`release`. **E4 de Kanto** (Lorelei, Bruno, Agatha): o warp 0 pousa em tile sólido, blockdata IDÊNTICO
ao `pokefirered`, e quem tira o jogador é o `ON_FRAME` com `Common_Movement_WalkUp5`, porque
`applymovement` de script não consulta colisão. **Sevii, 162 mapas fora do grafo de warp**: portão de
ENREDO intacto, a balsa é `special DoSeagallopFerryScene` e a corrente Blaine -> Bill -> TRI PASS está
inteira. **Hearthome e ThreeIsland**: o mapa TROCA DE LAYOUT no `ON_TRANSITION`, e não é
`setmetatile`, que foi o que a auditoria procurou e não achou.

### O Deoxys ganha caminho, e a porta é a que a ROM já tinha

`FLAG_HIDE_DEOXYS` nunca ser apagada é **falso positivo**: é idioma vanilla, o Deoxys entra por
`addobject` quando o triângulo é resolvido. A outra metade era verdade: o menu da balsa de Lilycove
cobra **BOLSA E FLAG** (`src/script_menu.c:853`), o Seagallop de Vermilion cobra o mesmo par, e o
único `giveitem ITEM_AURORA_TICKET` do repo mora **dentro do Mystery Gift, que este cartucho não
tem**: as duas Birth Island eram alcançáveis no grafo de warp e sem porta no jogo. O conserto segue a
regra que a pesquisa de lendários já tinha escrito ("não copiar o gate por Mystery Gift") e usa o
guarda-chuva que a ROM já usa para item-chave que ninguém entrega: o Aurora Ticket virou a **décima
linha de `chaves`** e sai pelo MESMO NPC do laboratório, com `setflag
FLAG_ENABLE_SHIP_BIRTH_ISLAND` colado no `additem`. **Nenhum mapa novo, nenhum estático movido, custo
ZERO de save**, e o portão de ENREDO fica de pé: a atendente só atende com `FLAG_SYS_GAME_CLEAR`,
então Deoxys continua pós-Liga. **T168.4 e T168.5.**

### Os cinco casos adversariais (T169, 8 casos)

1. **Galar, vencer e falar de novo.** Dito por inteiro: vencer de verdade no harness NÃO dá, o time
   de Galar é `Level: 255` e o Pikachu 20 do seletor não ganha; plantar a flag do id é o MESMO estado
   de save. O que este caso tem a mais que o T163.3 é a camada da afirmação: **o PNG foi aberto e a
   caixa de pós-batalha está desenhada, com texto dentro**, e depois dela o jogador anda.
2. **Johto, capítulo alto, Surf e Strength.** Liga de Johto, oito insígnias. Surf em
   `OlivineCity_PortOutside`, escolhido por varredura dos 236 mapas atrás de "warp cuja linha reta
   bate em água funda com corredor limpo e água terminando em PAREDE": a Route41, candidata óbvia,
   tem oito TILES DE WARP em fila na linha de caminhada. Strength no ginásio de Cianwood, o único
   lugar de Johto com bloco de Strength e script próprio. **Os dois com par negativo em "Start of
   region"**, que prova que quem destrava é o capítulo, e não o Pikachu.
3. **Sinnoh, o texto no framebuffer.** Das 433 linhas acrescentadas, a mais larga em mapa alcançável
   por rota curta tem **200 px de 208** e está em `VeilstoneCityNortheastHouse`. **PNG aberto: as duas
   linhas cabem, sem letra cortada e sem terceira linha.**
4. **Accumula, T143.9, cinco vezes seguidas: 5/5.**
5. **O gêmeo atravessa o desligamento.** T169.7 planta a flag do gêmeo PUBLICADO (0x10BE, id 3006) e
   SALVA sem falar com ninguém; T169.8 abre em CONTINUAR **sem acender flag à mão** e a batalha que
   abre é `TRAINER_GALAR_ISADORA_22_3`, id 3250.

### O que a caça achou DENTRO do próprio ferramental

Cinco vermelhos que ninguém via porque um `assert` anterior sempre caía primeiro. (a) **Três espécies
da Dex moradas em DOIS lugares**: a realocação de Johto pôs cópia nos mapas novos e deixou as
originais na órfã Diglett's Cave, e como `encontros_base()` desfaz a escrita pela coluna
`substituido`, o censo-base voltava a vê-las e o plano as dava por obtidas; os três slots voltaram a
`SPECIES_DIGLETT`. (b) **Um COMENTÁRIO entregava um item**: `RotomsRoom/scripts.inc:44` cita
`ITEM_ROTOM_CATALOG` dentro de um `@`, e a varredura era regex no texto cru, então o NPC parava de
dar o item e **as cinco formas do Rotom voltavam a inobteníveis sem uma linha de erro**. (c)
**`plano_congelado` cobrava o irreproduzível**: exigia o mesmo par espécie -> casa de cada estático, e
`decide_estaticos` escolhe casa por cota e por lotação, que leem a árvore; passou a cobrar o CONJUNTO
de linhas por balde, e foi essa cobrança que pegou o item (a). (d) **Tabela de encontro VAZIA não é
conteúdo**. (e) **O Masquerain tem estático próprio** desde 22/08 e a régua só aceitava evolução ou
mato: cobrava o caminho em vez do resultado.

E seis casos ficaram vermelhos pela troca de idioma de Galar, **sem defeito de jogo** (T153.1 a
T153.4, T154.5, T154.6): `trainerbattle_single` escreve `gTrainerBattleParameter` no SETUP, ANTES de o
`GetTrainerFlag` desviar para `gotopostbattlescript`, então **`oponente_faixa [0,0]` deixou de
significar "nenhuma batalha começou"** e quem responde isso agora é o time do adversário, carregado só
quando ela começa. E o caminho de quem ainda não venceu ganhou uma caixa: o `nointro` batia direto, o
`single` mostra o texto de entrada e espera botão, então a rota precisa de UM A a mais.

### Lições

1. **`UnlockPlayerFieldControls` é solta no FIM do script, e não pelo `release`.** O `frozen` que o
   `lock` põe é do OBJETO, não do jogador. Ler `lock` sem `release` e gritar "trava" errou 127 vezes
   numa rodada só; o que o `end` seco custava era outro, NPC congelado e zero fala.
2. **Alocador de flag e de var é APPEND-ONLY, sempre.** Reordenar endereço publicado invalida save em
   silêncio, e save inválida é o único defeito desta obra sem conserto.
3. **Túmulo fora do denominador.** Mapa sem warp, sem conexão e com `MAPSEC_NONE` não entra em alcance
   nem em completude; contá-lo faz a régua mentir dos dois lados.
4. **QA mora em `dev_scripts/qa/`**, com uma contagem só, um `--demo` só e os vereditos de calibração
   escritos DENTRO da ferramenta: auditoria fora do repo envelhece sem ninguém ver. E **falso positivo
   que volta todo mês custa mais que o bug**: os 61 reclassificados foram medidos contra o
   `pret/pokeemerald` intocado ou contra o mecanismo real, com arquivo e linha por escrito.

### O que fica aberto

- **Galar: 246 mapas órfãos**, e o retrato NÃO é o que se supunha. Medido nesta rodada: 58 interiores
  de Turffield, 49 da Isle of Armor, 27 de Postwick, 22 interiores de Wyndon, 20 da Crown Tundra, 13
  da Wild Area, 13 da Lost Cave e o resto pulverizado. O grosso é **interior sem porta**, e não DLC:
  86 dos 246 são de DLC. É o maior item da região, e é obra de warp, não de escopo.
- **22 travas e ~1.970 prováveis** ainda na varredura. Não é fila de conserto, é fila de VEREDITO, e
  cada um passa por medir, como os 61 desta rodada. Hoenn concentra 759 prováveis.
- **A fala de Galar é em PORTUGUÊS** (intro e pós-batalha, 308 textos), porque o demake de origem é
  brasileiro; as outras cinco regiões são em inglês. Decisão herdada, não regressão, mas o Gui vai ver
  a troca de idioma ao atravessar.
- **Galar** segue com 70 estáticos dos 1.088, 25 placas, 514 NPCs mudos e `fila_galar.json` em 1.198
  de 3.195; a **pergunta 18** segue sem resposta; **gens 6, 7 e 9** paradas por escopo. Os **90
  canteiros de berry**, as **8 bolas de neve** e os **141 objetos em 49 mapas** de Sinnoh continuam
  onde a 0.s os deixou.
- **Playthrough por região é a PRÓXIMA rodada.** Esta caçou defeito por lente; falta percorrer o
  enredo de ponta a ponta, uma região por vez, que é a única lente que pega ordem de cena e ritmo.

### A ROM `23d` é a candidata ao playtest do Gui

`roms/pokemon-claude-2026-08-23d.gba`, md5 `b6cdb072b9fd904215c21a544df389d8`, com o `.map` ao lado, e
o mesmo binário em `roms/pokemon-claude-teste-2026-08-16.gba`, que é o arquivo que o emulador dele já
aponta. Save antiga continua valendo: `SAVE_LAYOUT_REVISION` segue em 1 e `guarda_save.py` fechou
COMPATIVEL.

---

## 0.s SINNOH FECHA: O ENREDO ENTRA POR FLAG RECALCULADA, O GELO GANHA BATENTE, E A PORCENTAGEM PASSA A MEDIR O QUE VAI FICAR, 23/08/2026 (rodada 11; condutor Opus, três executores Opus, fechador Opus)

Build verde, uma build só, e a rodada em que **Sinnoh passa de 100% nas quatro colunas**: mapas 100%,
**objetos 93,3 → 101,6%**, warps 103,7% e **placas 98,1 → 103,4%**. **ROM 96,38% de 32 MB**
(32.340.476 B, **1.213.956 B livres**, 3.932 B a mais que a 0.r), **EWRAM 86,16% e IWRAM 86,68%**,
os dois idênticos aos da 0.r, Dex obtenível em 1.571 de 1.571. **Suíte 961 de 963**, com o T11.3
pulado na varredura porque ele só prova algo com duas ROMs e **um reprovado que é o T143.9, o
instável conhecido**: ele mora na Accumula Town, que tem quatro NPCs `MOVEMENT_TYPE_WANDER_AROUND`
no caminho da rota, e ele mesmo diz isso no par negativo T143.10. Foi **rodado sozinho três vezes
depois da varredura e passou nas três**; Unova não foi tocada nesta rodada. O bloco novo **T162 em
3/3**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, 2.192 ids de treinador conferidos e os 38 chefes de Galar da Fase F
conferidos um a um; `guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags, **0 novas
nos dois perfis** e 0 stub; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile
--piso 60` em **5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh
--so-sinnoh` com `'sprite': 0` e 0 mapas com problema; os nove `--demo` rodados, oito deles TOCADOS nesta rodada (`completude`,
`bolas_neve_sinnoh`, `cenas_sinnoh_b3`, `porta_morta`, `texto_placas_sinnoh`, `importa_npcs_sinnoh`,
`treinadores_galar`, `guarda_party`, `guarda_save`) verdes. ROM oficial
`roms/pokemon-claude-2026-08-23c.gba` (md5 `1924d5cf6d7c38c2310d1445382e648f`), com o `.map` ao lado, e o MESMO binário em
`roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | **101,6%** | 103,7% | **103,4%** | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 103,6% | 100% | 70,3% | 59,2% | 48 (32) | 0 |

### O enredo de Sinnoh entra por flag RECALCULADA, e não por estado inicial

`dev_scripts/cenas_sinnoh_b3.py` trouxe **30 objetos de cena** do Platinum para 18 mapas: 13 que
estão sempre visíveis, 13 de polaridade **"aparece"** e 4 de polaridade **"some"**. Custo de save:
**6 apelidos de flag e ZERO var**. O idioma é o que importa, e ele foi escolhido contra a alternativa
óbvia: pôr `setflag` em `EventScript_ResetAllMapFlags` só roda em JOGO NOVO, e save antiga veria o
ancião de Celestic plantado desde o primeiro dia. Aqui não há estado inicial nenhum para acertar,
porque o `MAP_SCRIPT_ON_TRANSITION` de cada mapa **reescreve a flag toda vez que o mapa carrega**:
acende sempre, e só apaga se o marco já caiu. Save velha e save nova se comportam igual, e nada
entrou em `new_game.inc`.

`dev_scripts/porta_morta.py` mediu mapa a mapa quem tem warp em cima de metatile de porta e achou
**um só em Sinnoh**: a **caverna de Celestic**, onde o pouso do warp alcançava UM tile de 108
andáveis, porque o primeiro passo ao norte pisava na porta e devolvia o jogador à cidade. A porta
virou chão, o tile de pouso virou `MB_SOUTH_ARROW_WARP` (0x208, o metatile que 86 bocas de Sinnoh do
mesmo par de tilesets já usam) e o warp desceu para (10,21). `texto_placas_sinnoh` liberou **39
placas** (7 com texto do próprio banco do Platinum; 3 ficaram de fora por não haver tile de leitura),
e o conserto de `teto_bg` no importador é o que deixou a coluna `placas` sair de 98,1% para 103,4%.
**T161 em 7/7.**

### O gelo: a bola de neve é BATENTE, e o teto real é o de SPRITE

A primeira tentativa trouxe as bolas como bloco de Strength, e a medida derrubou a ideia: o chão do
ginásio é `MB_ICE`, e em tile de gelo o motor entra em movimento forçado ANTES de chegar em
`TryPushBoulder`. Então elas entraram pelo que são: objeto sólido, sem script e sem flag, na
coordenada da fonte. `desliza()` foi **calibrada contra o emulador com 197 sondas** lidas da EWRAM, e
as duas regras que faltavam estão escritas no topo do arquivo. Das 19 bolas do Platinum, **11
entraram e 8 ficaram de fora**: 7 pelo teto de sprite e 1 por acesso. **T115 7/7, T125 12/12 e T157
11/11**, este último em duas passadas.

### A ordem de rodar virou GUARDA, e a guarda foi provada na árvore de verdade

A 0.r deixou escrito que `treinadores_galar.py --aplicar` APAGA a Fase F se rodado sozinho, e que
isso era "disciplina de quem roda". Deixou de ser: `bloco_party` passou a **preservar o AI e os
Pokémon dos 38 chefes** que moram dentro do bloco de Galar, e `dev_scripts/guarda_party.py`, chamado
por `guarda_save.py`, reprova chefe cru. A prova não é só de laboratório: `--aplicar` foi rodado
**na árvore real desta rodada, duas vezes**, e o `git diff` inteiro ficou com o MESMO md5
(`f4a8c6ad0f211bc8c02b5ea5642c15de`) antes e depois, com `opponents.h` e `trainers.party` byte a
byte iguais. Nada precisou de `git checkout`.

### O corte honesto: a régua contava MAPA, e o que faltava era REGISTRO

Ordem do Gui: "vamos completar Sinnoh" e "normalizar a porcentagem com base no que realmente vai
ficar". `CORTES_DO_GUI` tinha dois modos, e os dois eram de MAPA: `mapa_fonte` tira o que a fonte tem
e nós não, `deficit` zera o buraco de um mapa inteiro. Nenhum dos dois enxerga **um tipo de registro
dentro de mapa que fica**, e era exatamente aí que Sinnoh sangrava. Nasceu o terceiro modo,
**`objeto_fonte`**: regex contra o `graphics_id` de cada objeto da fonte, e quem casa sai do
denominador da coluna `objetos` na região inteira.

Os dois grupos, ambos datados de 23/08/2026 e impressos por `--detalhe Sinnoh`:

| grupo | registros | motivo |
|---|---|---|
| Mobiliário sem mecânica | **63** (55 `VENT` em 14 mapas, 8 `BOLLARD` em 3) | desenho com colisão, sem fala, sem item e sem gatilho; este motor não tem objeto decorativo sólido, e NPC de pé em cima de respiro de calçada faz o mapa mentir |
| Canteiros de berry | **90** `BERRY_SOIL` em 23 mapas | o canteiro é ESTADO, e o id da árvore mora na save; corte **com prazo**, cai na primeira janela de save aberta de propósito |

**A trava que torna isso honesto, e ela é medida, não jurada:** o gráfico cortado tem que ter ZERO
ocorrências nos NOSSOS `map.json` da região. Cortar do denominador o que nós usamos seria descontar
de um lado e contar do outro, e a coluna subiria sem obra nenhuma. `confere_cortes` cobra isso, e o
`--demo` tem a mutação plantada: cortar `OBJ_EVENT_GFX_ITEM_BALL`, que Sinnoh usa 167 vezes, reprova.

O **"teto da fonte"** foi MEDIDO e NÃO virou corte, de propósito: mapa em que já pusemos tanto objeto
quanto o Platinum tem déficit ZERO, então o registro dele já não pesa no denominador. A régua já o
tratava; inventar um corte para ele seria maquiagem.

Resultado: objetos de Sinnoh de **2.181 sobre 2.300 (94,8%)** para **2.181 sobre 2.147 (101,6%)**.
O excedente acima de 100 é o mesmo fenômeno de `warps` e `placas`: NPC e cena nossos que a fonte não
tem.

### O que AINDA falta em Sinnoh, nomeado

Depois do corte, **49 mapas ainda têm menos objeto que a fonte, 141 no total**, e `--detalhe Sinnoh`
imprime a lista mapa a mapa. Atribuindo o buraco de cada mapa aos gráficos da fonte que ele não tem
(heurística, e é declarada como tal), o retrato é: **71 obstáculos de HM** (34 `ROCK_SMASH`, 26
`STRENGTH_BOULDER`, 11 `CUT_TREE`), quase todos recusados pelo portão de TRANCA ou de BOLSO, que é o
portão provando que ninguém fica preso; **23 item balls**; **7 bolas de neve**, as recusadas por teto
de sprite; **6 portas animadas** de Elite e do QG, que aqui são warp e não objeto; e **34 pessoas**,
o balde de nome próprio sem sprite mais os 24 objetos de marco sem equivalente nesta ROM. Os piores
mapas são `SinnohVictoryRoad2F` (14 de 32) e `RavagedPath` (13 de 31), os dois de pedra quebrável.

### Lições

1. **O teto real de objeto por sala não é o do mapa, é o de SPRITE.** `gObjectEvents` tem 16 vagas e
   a 0 é do jogador, então sobram 15, e `TrySpawnObjectEvents` simplesmente NÃO acorda o resto quando
   elas acabam: sem erro, sem aviso. Objeto que não acordou não é sólido, e bola de neve que não é
   sólida não para escorregão nenhum. O ginásio de Snowpoint é a janela mais apertada de Sinnoh (20
   objetos: 11 bolas e 9 corpos, com câmera que enxerga as 15 vagas cheias), e o `--demo` agora liga
   o `VAGAS_DE_SPRITE` ao `OBJECT_EVENTS_COUNT` lido do `.h`: quem mexer no motor quebra ali.
2. **Os tiles 192 e 193 PARAM o deslize, e bloqueiam também a SAÍDA.** `MetatileBehavior_IsIce_2` só
   aceita `MB_ICE`, e `IsMetatileDirectionallyImpassable` olha o tile de ORIGEM e o de DESTINO. Sem a
   primeira regra são 12 divergências em 161 medidas; sem a segunda, 6.
3. **Porta de beco: warp em cima de metatile de porta come o primeiro passo.** O mapa fica alcançável
   pelo validador estático e intransitável no jogo. A busca vale a pena e é barata: `porta_morta.py`
   varreu Sinnoh inteira e achou um único caso.
4. **Censo que não reconhece o próprio trabalho mente para baixo.** Os "166 objetos de enredo" que a
   0.r listava eram 169, dos quais **12 já estavam no mapa**, 97 moravam em mapa já no teto da fonte
   e 122 eram mobiliário. Régua e fila envelhecem juntas, e remedir custa minutos.

### O que fica aberto

- **9 divergências residuais** do simulador de gelo contra o motor (o deslize foi encerrado a 7
  tiles, não fechado) e as **8 bolas** que ficaram de fora, 7 delas por teto de sprite: subir isso
  pede reduzir corpo no salão, não calibrar melhor.
- **141 objetos em 49 mapas de Sinnoh**, no retrato da seção acima, mais os **24 objetos de marco sem
  equivalente nesta ROM**, que só andam com a máquina de cenas de Sinnoh avançando.
- **Os 90 canteiros de berry** voltam ao denominador na primeira janela de save aberta de propósito,
  e quem a abrir sobe `SAVE_LAYOUT_REVISION` junto.
- **8 das 10 constantes `OBJ_EVENT_GFX_SINNOH_*` sem uso** continuam sem uso (BUCK, CHARON, CHERYL,
  CRASHER_WAKE, LOOKER, MARS, MAYLENE, PALMER); a leva b3 gastou BYRON e RILEY, uma vez cada.
- **Galar** com 70 estáticos dos 1.088, 25 placas, 514 NPCs mudos por motivo e `fila_galar.json` em
  1.198 de 3.195; **T143.9 continua instável**; a **pergunta 18** (sprites dos 26) segue sem resposta;
  e **gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.
- **FECHADO nesta rodada**, e a 0.r o listava aqui: `treinadores_galar.py --aplicar` não apaga mais a
  Fase F. Virou guarda, não disciplina, e a prova foi rodada na árvore de verdade.

### A próxima rodada é CAÇA A BUGS, antes de o Gui jogar

As seis regiões estão em cem por cento ou acima nas colunas que a régua mede, e a régua agora só
conta o que vai ficar. O que ela **não** mede é jogo travando, cena abrindo duas vezes, texto
cortado, NPC que fala pela pessoa errada, warp que leva ao lugar certo pelo lado errado. A rodada 12
é de **caça a bugs**, com a ROM na mão, antes do playtest do Gui: procurar defeito, não porcentagem.

---

## 0.r TRÊS CONSERTOS DE IDENTIDADE: O TIL DE GALAR, O ID DE TREINADOR E O SPRITE QUE FALAVA POR OUTRA PESSOA, 23/08/2026 (rodada 10; condutor Opus, um executor Opus, fechador Opus)

Build verde, uma build só, e uma rodada que **não custou um byte**: **ROM 96,37% de 32 MB**
(32.336.544 B, **1.217.888 B livres**), **EWRAM 86,16% e IWRAM 86,68%**, os três idênticos aos da
0.q, e a **régua de completude da 0.q intocada linha por linha**, Dex obtenível em 1.571 de 1.571.
Os três consertos são de NOME e de ÍNDICE, não de conteúdo. **Suíte 949 de 950**, ZERO reprovados,
com o T11.3 pulado na varredura porque ele só prova algo com duas ROMs, e o bloco novo **T160 em
8/8**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, e agora também **2.192 ids de treinador conferidos** contra o `e5224a3d67`;
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags, **0 novas nos dois perfis** e
0 stub; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em **5.915 de
6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com `'sprite': 0` e
0 mapas com problema; os seis `--demo` tocados (`fala_galar`, `glifo_til`, `treinadores_galar`,
`guarda_save`, `importa_npcs_sinnoh`, `sprites_sinnoh`) verdes. ROM oficial
`roms/pokemon-claude-2026-08-23b.gba` (md5 `ec560cb869964788a5a4f1880179c325`), com o `.map` ao lado,
e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

### O til: byte certo com glifo errado engana a ida e volta

A 0.q fechou dizendo que os `ä` de Galar eram "obra de fonte, não de script, porque o gerador tem ida
e volta byte a byte pelo charmap, então os BYTES estão certos". Estava certa pela metade. A fonte (o
demake `ultimate-plus-v1.2.1.2`, base FireRed) escreve "não" como `E2 F4 E3`, medido byte a byte em
`0x818376`, e REDESENHOU como til o glifo do `F4`, que no FireRed é o trema alemão `ä`. O nosso
`charmap.txt` ainda chamava `F4` de `ä`, então o tradutor decodificava `ä` e o assembler reencodava
`ä` no mesmo `F4`: **a ida e volta fechava, e o defeito nunca virou erro de build**, com o jogador
lendo "N-trema-o" em 315 lugares. A verificação media o BYTE; o errado era a LETRA.

O `charmap.txt` passou a chamar `F1 F2 F4 F5` de `Ã Õ ã õ`, e `dev_scripts/glifo_til.py` redesenhou
os quatro glifos nos **nove** `graphics/fonts/latin_*.png` sem inventar pixel: o til vem do `Ñ` e do
`ñ` do MESMO arquivo, sobreposto ao `A O a o` do MESMO arquivo, e tinta da letra nunca é apagada.
**`Ü` (`F3`) e `ü` (`F6`) continuam trema**, os únicos tremas vivos do repo, por causa do "JÜRGEN" de
`src/data/battle_frontier/apprentice.h`: conferido no fechamento, célula por célula nos nove PNG, que
**só `F1 F2 F4 F5` mudaram de desenho**. Varridos `data/`, `src/`, `include/` e `tools/` em UTF-8 e
em latin-1 atrás de trema fora de Galar, **nenhuma ocorrência**: nenhum texto de Kanto, Johto, Hoenn,
Sinnoh ou Unova usava `F4` como `ä` de verdade. Os quatro `.inc` regerados dão **0 trema, 317 til**,
e o `fala_galar --demo` ganhou quatro casos que medem a letra, com mutação plantada.

### O id de treinador é APPEND-ONLY, como o de mapa e o de layout

A 0.q registrou que `TRAINER_GALAR_LEON_736` e `_739` tinham ido de 3204/3205 para 3206/3207 com o
`guarda_save.py` dizendo SAVE COMPATIVEL, "certo pela régua dele e mudo sobre a vitória que mudava de
dono". A flag de "já venci este treinador" é `TRAINER_FLAGS_START + id` e mora na save: **id de
treinador é índice de save**, e vale a regra dos mapas e dos layouts, quem existe não se move e quem
entra entra no fim. O `numera()` de `treinadores_galar.py` passou a ler o de-para do próprio
`opponents.h` e só dá vaga nova a quem ainda não tem, os dois Leon voltaram a 3204/3205, e o
`guarda_save.py` ganhou `ids_de_treinador`, que compara o header de hoje com o do `e5224a3d67` (o da
ROM publicada) e reprova quem moveu, quem sumiu e quem entrou no meio, com a mutação real plantada no
`--demo`.

### O de-para por nome precisa olhar o SCRIPT

O de-para de sprite próprio casa pelo nome do objeto da fonte, e a fonte rotula como MARS o objeto de
CENA da comandante em `ValleyWindworksBuilding`: ela aparece, fala e some, e quem fica no mapa é o
pai da família, cujo script começa com "Papa:". O casamento com o objeto NOSSO era por vizinhança
pura, então a cara da Mars foi parar em quem fala como o pai, que é o mapa mentindo. `pode_vestir()`
virou o portão único dos DOIS pontos de `importa_npcs_sinnoh.py` que repintam objeto nosso: sprite
próprio só entra em objeto MUDO ou em objeto cujo script fala como a pessoa, seguindo os saltos de
rótulo, que é como a Candice de Snowpoint continua passando (o rótulo dela não diz o nome, o corpo
tem `TRAINER_SINNOH_LEADER_CANDICE`). A Mars saiu, o objeto voltou ao `OBJ_EVENT_GFX_SCIENTIST_1` que
já tinha, e ficam **20 colocações em 20 mapas, com 16 constantes**.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/160_fechador_r10.json`, **8 casos, 8 verdes**, seis em PAR; o texto
inteiro de cada um está no JSON.

- **T160.1, T160.2 e T160.3, o id do Leon pelos dois lados.** O 3204 abre a batalha dele com o time
  da tabela; a flag `0x1184` (`0x500 + 3204`) plantada faz o `goto_if_set` disparar e a batalha não
  começa; e a `0x1186`, o id que ele TINHA fora do lugar e que hoje é da Wanda, **não** o segura. O
  terceiro mede o estrago: uma save de ontem acenderia a vitória da Wanda e mandaria brigar de novo
  com o Leon.
- **T160.4, a vitória gravada de verdade.** O Tammy de `Galar_RoseTower03` (id 3166) é DERROTADO e a
  flag `0x115E` acende com as duas VIZINHAS apagadas. O truque é o `10:HP=0=1` na janela medida entre
  a criação do time em `gParties` e a cópia dele para `gBattleMons`, seis passos de dez quadros:
  antes dela a escrita é desfeita, depois dela o HP volta a 21 no primeiro golpe.
- **T160.5 e T160.6, a Gardenia trava POR FALA.** O T158.7 já provava que ela é sólida, o que
  qualquer `graphics_id` daria; aqui o A roda a fala dela até o `trainerbattle_no_intro` e quem abre
  é `TRAINER_SINNOH_LEADER_GARDENIA`. O par sem o A não abre batalha nenhuma.
- **T160.7 e T160.8, o til lido na TELA.** O diário de `Galar_Route0803` é o único letreiro de Galar
  com til, e o tile dele é ANDÁVEL: o caso usa um toque de quatro quadros, que vira sem andar, porque
  a primeira versão usou dezesseis e atravessou o letreiro sem lê-lo. A medida de tela saiu do MESMO
  roteiro nas DUAS ROMs: os framebuffers finais diferem em **NOVE pixels**, todos no retângulo
  (116,124) a (121,125), o acento do único "a" com til da tela, dois pontos na velha e til na de
  hoje. **Nenhum outro pixel mudou.**

### O que fica aberto

- **13 bolas de neve** de Snowpoint, até o simulador de gelo ser calibrado contra o motor ao sul da
  linha 8 do ginásio; **Sinnoh em 93,3% de objetos**, que são 166 objetos de enredo do Platinum mais
  48 canteiros de berry cujo id mora na SAVE; e **Galar** com 70 estáticos dos 1.088, 25 placas, 514
  NPCs mudos por motivo e `fila_galar.json` em 1.198 de 3.195.
- **10 constantes `OBJ_EVENT_GFX_SINNOH_*` sem uso em mapa nenhum** (BUCK, BYRON, CHARON, CHERYL,
  CRASHER_WAKE, LOOKER, MARS, MAYLENE, PALMER, RILEY). Custam ROM e não aparecem; quem for usá-las
  passa pelo `pode_vestir()`.
- **`treinadores_galar.py --aplicar` APAGA a Fase F se rodado sozinho**, porque reescreve o
  `galar_treinadores.inc` inteiro e os chefes só voltam com `fase_f_chefes.py --aplicar` depois. Hoje
  é disciplina de quem roda, e não guarda: **vale um guarda**.
- **T143.9 continua instável** pelo motivo escrito na 0.q, o conserto da 0.p segue medido e refutado,
  a **pergunta 18** (sprites dos 26) segue sem resposta com a arte crua, e **gens 6, 7 e 9** seguem
  paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.

---

## 0.q GALAR VOLTA A FALAR E OS ANTROS DE RAIDE VIRAM ENCONTRO, SINNOH ABRE OS TRÊS LAGOS E GANHA 26 SPRITES PRÓPRIOS, 23/08/2026 (rodada 9; condutor Opus, três executores Opus, fechador Opus)

Build verde, uma build só. **ROM 96,37% de 32 MB** (32.336.544 B, **1.217.888 B livres**, 1,16 MB;
era 96,06% e 1.320.436 B livres na 0.p, então a rodada gastou 102.548 B), **EWRAM 86,16% e IWRAM
86,68%, idênticos aos da 0.p e aos da 0.o**: nada desta rodada encostou em RAM. **Suíte 939 de 940**, ZERO reprovados,
com o T11.3 pulado na varredura porque ele só prova algo com duas ROMs, e os quatro blocos novos **T156 em 10/10, T157 em 8/8, T158 em 6/6 e T159 em
14/14**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, **nenhum grupo novo** (128 de 255, nenhum acima de 128 mapas);
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois perfis**,
0 stub nos dois; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em
**5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com
`'sprite': 0` e 0 mapas com problema. ROM oficial `roms/pokemon-claude-2026-08-23.gba` (md5 6e3c177cbe61c5eabdd7759b3de3cfee),
com o `.map` ao lado, e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | **93,3%** | 103,7% | 98,1% | -- | **39 (18)** | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | **103,6%** | 100% | **70,3%** | **59,2%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada.

### Galar: seis specials nulos destravam 274 linhas, e as mesas de raide saem da recusa

O demake chama Quest Log e Help System do FireRed o tempo todo, 236 vezes em 178 linhas de script, e
enquanto o NOME não existisse aqui o tradutor recusava a CENA INTEIRA por um comando que não muda
nada observável. `src/field_specials.c` e `data/specials.inc` ganharam os seis com corpo NULO, e a
semântica nula é FIEL: `GetQuestLogState` devolve 0, que no FireRed quer dizer "não estou gravando
nem reproduzindo", e nesta ROM isso é sempre verdade. Resultado: **274 linhas destravadas e 168
frases novas**.

As **mesas de raide** eram, na 0.p, 200 linhas fora por "sorteio de N espécies no script".
`estaticos_galar.resolve_mesas` passou a escolher UM encontro por antro com regra determinística:
lendário pela regra 1, com **um lendário por antro e sem repetição**, e o resto por rotação no índice
do antro na fila, vetando espécie que já saiu em antro a até três mapas de distância. Medido na
árvore de hoje: **196 antros, 111 espécies distintas, 20 lendários em 20 antros, zero lendário
repetido em qualquer outro antro**. Em **três pares** de mapas vizinhos a espécie de raide ainda
repete (CrownTundra08/12, CrownTundra11/13, IsleOfArmor08/12), e isso é o SEGUNDO degrau da regra
funcionando como escrito: quando não há candidato que respeite vizinhança e lendário ao mesmo tempo,
a vizinhança cede, porque ela é a restrição mole.

Com o reposicionamento de 42 encontros a menos de três tiles, os estáticos vão de **795 para 1.018
dos 1.088** que a fonte oferece. Objetos 93,5 → **103,6%**, placas 65,8 → **70,3%**, script 55,6 →
**59,2%**, fila de 1.476 para **1.198**. Quatro defeitos de gerador consertados na raiz, e um deles ia
longe: o pool de flag escolhia por apelido e teria escrito por cima da Jasmine de Johto.

**A régua de Galar é HONESTA, e foi conferida aqui e não aceita de palavra.** O denominador de
`objetos` soma os 1.111 registros que o filtro G4 aprovou MAIS os **1.088 encontros estáticos que a
FONTE oferece** (`dev_scripts/galar_estaticos.json`); o numerador conta os `object_events` do
`map.json` de hoje, estáticos inclusive. O `da_fonte` NÃO se mexeu nesta rodada, só o `aceitos`
(795 → 1.018), e as recusas fecham a conta exata: 1.018 + 1 + 1 + 2 + 4 + 37 + 25 = 1.088. Os dois
lados contam os estáticos, e passar de 100% é o mesmo de Kanto (101,2%) e Unova (102,3%).

### Sinnoh: os três lagos abrem a pé, as bolas de neve são batente, e os objetos vão a 93,3%

Os três lagos drenados eram prisão: `LakeVerityLowWater`, `LakeAcuityLowWater` e `LakeValorDrained`
tinham a boca na elevação 3 e os ~800 tiles em volta na elevação 1, e `IsElevationMismatchAt`
recusava cada passo. A causa não era o mapa da fonte, era a REGRA de conversão, escrita para caverna
de pedra: `0x00` sem colisão virava rocha e `PUDDLE`/`SHALLOW_WATER` viravam água.
`dev_scripts/lagos_sinnoh.py` converte os três com a regra do lago, e `WATER_SEA` continua água de
propósito, porque no Platinum também é Surf que atravessa.

As **19 bolas de neve** do ginásio de Snowpoint entraram como OBJETO SÓLIDO, e não como bloco de
Strength, e isso foi MEDIDO e não escolhido: o chão do ginásio é `MB_ICE` inteiro, e em gelo o motor
entra em movimento forçado (`sForcedMovementFuncs`, `src/field_player_avatar.c:164`) ANTES de chegar
em `TryPushBoulder`, então o empurrão nunca acontece. **6 das 19 passaram** no portão, que exige que
todo NPC com script do ginásio continue alcançável pelo simulador de escorregão; as outras 13 ficam
ao sul da linha 8, onde o modelo ainda não bate com o motor.

Também entraram: os sub-baldes b1/b2/b3 do importador de NPC (b1 tem cena equivalente aqui e entra com
a NOSSA flag; b2 é sorteio diário da fonte e entra visível; b3 é flag MORTA na fonte), o corredor de
conversa reservado, as pedras com empurrão de até três tiles, a `RotomsRoom` com as sete formas como
cenário, e o `MOVE_STRENGTH` no `src/chapter_jump.c`. Objetos **87,0 → 93,3%**, **81 Pokémon no
overworld**, **19 NPCs com sprite próprio**. Três defeitos de idempotência consertados, que juntos
tinham deixado **284 cópias** de objeto no mapa.

### Sprites: 26 personagens de Sinnoh com desenho próprio, e nenhuma paleta nova

`dev_scripts/sprites_sinnoh.py` desenha 26 PNG de **144 por 32**, que são os nove quadros de 16 por 32
da tabela de animação padrão, lidos por `overworld_ascending_frames` (uma entrada só na pic table, com
`relativeFrames`). **Zero paleta nova**: os 26 reaproveitam `OBJ_EVENT_PAL_TAG_NPC_1` a `NPC_4`, porque
paleta de overworld é VRAM e estourar a janela de sprite de um mapa faz NPC sumir sem erro nenhum
aparecer. O preço é arte crua, e foi escolha. As constantes entram no FIM do enum de
`include/constants/event_objects.h`, única posição que não desloca id de sprite já gravado.

**Correção de número em relação ao que foi relatado:** as colocações são **21 objetos em 21 mapas,
com 17 constantes distintas**, e não 16; nove constantes (LOOKER, BUCK, MAYLENE, CRASHER_WAKE, CHARON,
BYRON, RILEY, PALMER, CHERYL) ainda não foram usadas em mapa nenhum.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/159_fechador_r9.json`, **14 casos, 14 verdes**, sete deles em PAR, autor
de caso diferente do autor de cena em todos. O texto inteiro de cada um está no JSON; aqui vai o que
cada par mede.

- **T159.1 e T159.2, dois antros de raide VIZINHOS.** `Galar_WildArea05` dá `SPECIES_MIME_JR` (439) e
  `Galar_WildArea06`, vizinho direto no grafo de warps, dá `SPECIES_DARUMAKA_GALAR` (989), lidos de
  `gParties`. O par é a prova: um caso sozinho só diria que ALGUM bicho apareceu.
- **T159.3, T159.4 e T159.5, o Quest Log depois de SAVE E RECARGA.** O T159.3 salva dentro de
  `Galar_Hulbury06`; o T159.4 CONTINUA daquela save, fala com o mercador que chama
  `special GetQuestLogState` e fica TRAVADO pela caixa em (25,45); o T159.5, com um aperto a menos,
  anda até (20,45). Special que a tabela não registrasse derrubaria o script.
- **T159.6, o lago esvaziado atravessado de ponta a ponta E DE VOLTA.** 181 passos em 52 pernas dentro
  do leito do `LakeValorDrained`, parando no VIZINHO da boca, porque pisar nela provaria warp e não
  leito.
- **T159.7 e T159.8, a bola de neve contra o escorregão.** Do MESMO tile (12,3): para baixo o
  escorregão para em (12,7), quatro tiles, porque a bola de (12,8) segura; para a esquerda, na linha
  sem bola, ele corre ONZE tiles até (1,7).
- **T159.9 e T159.10, o sprite próprio lido no motor.** `graphics_id` que não resolve NÃO dá erro de
  build: dá objeto que não carrega, e objeto que não carrega deixa de ser sólido e de rodar script. A
  Mars trava o jogador em (9,4) com o A; sem o A ele desce até (9,7).
- **T159.11 e T159.12, o objeto b1 some depois da cena nossa.** Com `FLAG_GALACTICA_WINDWORKS` acesa o
  objeto de (3,7) some e o jogador anda até (3,6); com ela apagada ele não sai de (3,8).
- **T159.13 e T159.14, a cena do c3 acende a flag que o mapa REALMENTE lê.** É o caso do defeito
  achado no fechamento: o jogador joga a cena inteira, SAI E VOLTA pelo mesmo warp, e só então anda.
  Recarregar o mapa é o ponto, porque `removeobject` sozinho passaria num caso da mesma sessão.
- **O rodízio do Restaurante NÃO EXISTE, e a sonda é a resposta.** `data/maps/Restaurant/map.json` tem
  19 objetos, todos com `flag: "0"`, `Restaurant_MapScripts:: .byte 0`, e `GetDayOfWeek` não tem
  chamador nenhum no repo. A decisão está em `importa_npcs_sinnoh.py:250-278`: na fonte o critério é
  `GetRandom`, não dia da semana, e o balde b2 põe os NPCs visíveis de propósito. Não há caso a
  escrever.

### O que o fechador consertou

- **A cena nova do c3 acendia uma flag que NINGUÉM lê, e foi por pouco que ninguém viu.** O bloco c3
  (`cenas_galar.py`) alocava a PRÓPRIA flag de esconder por (mapa, flag da fonte),
  `FLAG_GALAR_ESCONDE_G09M11_230` na vaga 0x1C89, enquanto os objetos 1 e 2 do `Galar_Hammerlocke05`
  escondem por `FLAG_GALAR_ESCONDE_230`, vaga 0x1C81, que é a que o bloco c4b (`objetos_galar.py`)
  batizou para a MESMA flag da fonte e escreveu no `map.json`. A cena chamava `setflag` numa e
  `removeobject` nos objetos da outra: o sumiço valia só a sessão de mapa e os dois NPCs voltavam ao
  reentrar. O c3 passou a REUSAR o nome do c4b quando ele já existe no header, e o T159.13/T159.14 é a
  prova. Efeito colateral MEDIDO e querido: a flag do c4b é por FLAG DA FONTE e não por mapa, e a
  0x230 pendura seis objetos em três mapas de Hammerlocke, então a cena passa a sumir com os seis, que
  é o que a fonte faz.
- **`objetos_galar.py --demo` ficou VERMELHO nesta árvore, e a causa é a mesma família.** Ele planta
  duas flags na mesma vaga e cobra que o portão reprove; a vaga escolhida já tinha dono, o grupo
  acusado vinha com TRÊS nomes e a mutação reprovava por si mesma. Raiz: o filtro por PREFIXO. O c4b
  tirava da conta tudo que começasse com `FLAG_GALAR_ESCONDE_`, e o c3 usa o MESMO prefixo mais o nome
  do mapa. Não chegou a colidir por sorte de ordem, e teria colidido na próxima flag pedida. O
  reconhecimento passou a ser por FORMATO EXATO do nome, numa função só (`flags_com_dono`).
- **T141.5 e T141.6 ficaram VERMELHOS, e a culpa não era do jogo.** A partir desta rodada o
  `Galar_Hammerlocke05` tem cena de `ON_FRAME` própria, longa, que dispara ao entrar e come os apertos
  do roteiro em caixa de texto. Com `VAR_GALAR_G09M11_CENA` valendo 1 o mapa se comporta tile a tile
  como na ROM da 0.p, medido nos dois binários, então não há travamento: há cena nova. Os dois casos
  ganharam a var e voltaram a medir o que foram escritos para medir. **Custou meia hora acreditar que
  era trava**, e o que desfez a suspeita foi rodar a MESMA sonda contra a ROM `2026-08-22f`.
- **Semântica de aperto, medida e não suposta:** pressão de 16 quadros contígua anda um tile, mas a
  PRIMEIRA pressão do roteiro é engolida, e um `NADA` no meio faz a pressão seguinte virar só a
  virada. Quatro rotas do T159 nasceram erradas por isso, e foram medidas até baterem tile a tile.

### O que fica aberto

- **A cena longa nova de `Galar_Hammerlocke05`** tem três caixas com muitas páginas e roda ao ENTRAR
  no mapa. Ela é fiel à fonte, mas é a primeira cena de Galar que um jogador encontra sem pedir, e o
  Gui pode querer olhar o texto dela (ver o item do "ä" abaixo).
- **T143.9 continua INSTÁVEL, e o conserto que a 0.p propunha foi MEDIDO e REFUTADO.** Ele passou
  verde nas duas varreduras completas desta rodada, e rodado sozinho deu 2 de 3 numa vez e 1 de 3 na
  outra, na mesma ROM. A 0.p dizia que o conserto era dar um Pokémon ao jogador pelo `antes_do_warp`,
  como o T144.5 faz; isso foi feito e medido, e o caso passou a 1 de 3, ou seja PIOROU. Duas medidas
  do mesmo remédio com o resultado errado querem dizer que o diagnóstico está errado, então o
  `antes_do_warp` foi desfeito e o caso ficou como estava, com a medida nova escrita no próprio texto
  dele. Quem for mexer: meça POR QUE a batalha se fecha, em vez de supor que é falta de time.
- **13 bolas de neve** de Snowpoint até o simulador de gelo ser calibrado contra o motor ao sul da
  linha 8 do ginásio.
- **Sinnoh, objetos em 93,3%**: 166 objetos de enredo do Platinum e 48 canteiros de berry cujo id mora
  na SAVE.
- **Galar, 70 estáticos** dos 1.088 (mesa sem espécie com nome aqui e geometria recusada), **25
  placas**, **514 NPCs mudos** por motivo, `fila_galar.json` com 1.198 de 3.195.
- **Texto de Galar sem "ã".** Os arquivos de fala trazem **191 ocorrências de "ä" e ZERO de "ã"**
  ("Näo", "irmä"). Não é regressão desta rodada, veio com a onda de 20/08, e o gerador tem ida e volta
  byte a byte pelo charmap, então os BYTES estão certos: o que falta é o glifo. Conserto é obra de
  fonte, não de script.
- **`opponents.h` deslocou dois ids** (`TRAINER_GALAR_LEON_736` e `_739` foram de 3204/3205 para
  3206/3207) e `vars.h` remanejou seis apelidos de var de Galar. O `guarda_save.py` diz SAVE
  COMPATIVEL e está certo, porque ele mede TAMANHO (`FLAGS_COUNT`, `MAX_TRAINERS_COUNT`) e não
  atribuição; mas a flag de "já derrotei" de um treinador é indexada pelo id, então esses dois trocaram
  de vaga. Não morde hoje, porque Galar não tem treinador jogável, e é a última hora em que isso é de
  graça.
- **A Mars de `ValleyWindworksBuilding` fala como o pai da família.** O objeto 0 trocou de
  `OBJ_EVENT_GFX_SCIENTIST_1` para `OBJ_EVENT_GFX_SINNOH_MARS`, e o script dele
  (`ValleyWindworksBuilding_EventScript_Npc1`) é a fala portada que começa com "Papa:". Ou o sprite
  está errado, ou o script; não foi mexido de propósito, porque os sprites estão na pergunta 18, sem
  resposta do Gui.
- **Pergunta 18 (sprites dos 26 personagens) segue sem resposta.**
- **Gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.

---

## 0.p O B10 DERRUBA A ROM DE 99,28% PARA 96,06%, E O DISTORTION WORLD FICA SIMÉTRICO, 22/08/2026 (rodada 8; condutor Opus, dois executores Opus, fechador Opus)

Build verde, um build só. **ROM 96,06% de 32 MB** (32.233.996 B, **1.320.436 B livres**, 1,26 MB;
era 99,28% e 241.172 B livres na 0.o), **EWRAM 86,16% e IWRAM 86,68%, idênticos aos da 0.o**: o B10
é obra de ROM e não encostou em RAM. **Suíte 900 de 902**, com o T11.3 pulado e UM vermelho de
tempo no T143.9 (ver "o que fica aberto"), e o bloco novo **T155 em 6/6**; **T11 3/3** contra a
build `cf6786b2ae` (worktree em
`/private/tmp/claude-501/t11-antiga`). **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B,
**2.054 layouts sem nenhum movido** e **2.400 mapas**, os 2.400 declarados dentro da ROM;
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois
perfis**; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em
**5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh` com 0 mapas com
problema; os três `--demo` tocados verdes, um deles depois de conserto. ROM oficial
`roms/pokemon-claude-2026-08-22f.gba` (md5 `fb239ede296088906761daece2e7d6d5`), com o `.map` ao
lado, e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

**A régua de completude não se mexeu**, e isso é o critério de aceitação do B10, não um detalhe:

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | 87,0% | 103,7% | 98,1% | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 93,5% | 100% | 65,8% | 55,6% | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada.

### O B10, fatia por fatia

| fatia | onde | B de volta |
|---|---|---|
| tabelas de fala de treinador, VAZIAS desde sempre | `src/trainer_slide.c` | **498.400** (448.056 + 50.400 viraram 56) |
| dificuldade colapsada: EASY e HARD de `gTrainers` | `include/constants/difficulty.h` | **277.160** |
| blockdata repetido virando referência, 2.373 de 4.108 blobs | `dev_scripts/dedupe_blockdata.py`, chamado pelo `map_data_rules.mk` | **264.080** |
| 20 famílias novas de asset, criadas pela entrada de Galar | `dev_scripts/dedupe_assets.json` | **38.700** |

Somadas dão 1.078.340 B previstos contra **1.079.264 B medidos no link**; a diferença é alinhamento
de seção, e vale o medido. `B_VAR_DIFFICULTY == 0` faz `GetCurrentDifficultyLevel()` devolver
`DIFFICULTY_NORMAL` sempre, então EASY e HARD eram zeros inalcançáveis e `[DIFFICULTY_NORMAL]` virou
`[0]` sozinho (dar um var a `B_VAR_DIFFICULTY` devolve as três na hora, e `TESTING` segue com as
três); as duas tabelas de fala nunca tiveram uma fala cadastrada; e o dedupe de layout só troca o
`.incbin` do repetido pelo símbolo do primeiro de conteúdo igual, sem tocar em `map.bin`, em
`layouts.json` nem no motor.

**Descartado, com número e não no olho:** a **indireção de tabela de treinador** renderia ~52 KB
líquidos, caro demais para o tamanho, e os **ícones já estão em `.smol` desde a Fase D**.

### Distortion World, a corrente ficou simétrica

O `cria_mapas_sinnoh.py` ganhou `simetriza`, e ele mora ali, e não numa ferramenta à parte, porque
o `--aplicar` não recria mapa que já existe: sem esse passo o defeito ficaria congelado para sempre.
Ele corrigiu **9 `dest_warp_id` em 8 `map.json`**, e o `pares` é simétrico POR CONSTRUÇÃO (o mesmo
`zip` produz A→B e B→A), o que o `--demo` cobra com mutação plantada. **Uma assimetria FICA, e é
honesta**: o warp 0 do `DistortionWorld1F` leva ao `MtCoronet6F`, que não tem escada de volta, então
essa porta é de mão única; está no T153.14, e é falta de degrau, não fiação errada.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/155_fechador_r8.json`, **6 casos, 6 verdes**, autor de caso diferente
do autor de cena em todos.

- **T155.1, dificuldade no CHEFE.** O time de `TRAINER_SINNOH_LEADER_CANDICE` lido de `gParties`:
  seis espécies diferentes, seis níveis em escada (178 a 182) e o item do ace (`ITEM_ABOMASITE`). O
  "antes" foi RODADO, não argumentado: o mesmo caso passou verde contra a ROM da rodada anterior
  (`pokemon-claude-2026-08-22e.gba`), com os mesmos doze campos.
- **T155.2 e T155.3, blockdata aliasado com PLACA.** O `CanalaveLibrary2F` (layout aliasado) é
  cruzado de ponta a ponta e uma placa é lida; a prova é a posição, porque a caixa aberta ENGOLE a
  perna seguinte. O par negativo tira só o A e termina em (0,7) em vez de (13,7).
- **T155.4, Galar com o tileset inteiro aliasado.** No `gTileset_Galar19` metatiles, ATRIBUTOS e
  paletas viraram alias; o único mapa que o usa entra, SAI para o vizinho e VOLTA, para medir a
  segunda carga e não só a primeira.
- **T155.5, trainer slide no pior id.** `TRAINER_GALAR_LEON_739` é o id **3205**, o maior de
  `opponents.h` e o que ocupava a última linha da tabela que saiu; a batalha abre e entrega as seis
  espécies. Medido no caminho: batalha de Frontier **não** é desviada por `IsSpecialTrainer`
  (`include/data.h:275`), ela chega em `GetTrainerSlideArray`.
- **T155.6, o Distortion World inteiro.** Nove andares a pé numa sequência só, 27 pernas e ~345
  tiles, terminando no Spear Pillar em (14,12). É o único jeito de medir simetria: par torto põe o
  jogador no tile errado e a rota do andar seguinte quebra na hora.

### O que o fechador consertou

- **`dedupe_blockdata.py --demo` era verde VAZIO.** Ele lia o `layouts.inc` do DISCO, que já passou
  pelo próprio passo dentro do `make`, e imprimia "0 repetidos, 0 B de volta" com exit 0. Passou a
  rodar o `mapjson` num diretório temporário e medir A LINHA DE BASE: **4.108 blobs, 2.373 repetidos,
  264.080 B**, com `assert` que reprova se o número der zero. É a mesma armadilha dos dois `--demo`
  consertados na 0.o: autoteste tem de saber que o gerador já rodou.
- **`valida_warp_tile.py` ia CEGO em tileset aliasado.** A varredura de pastas só enxergava
  `INCBIN`, e o `dedupe_assets.py` troca o `INCBIN` do repetido por `ASSET_ALIAS`:
  `Galar_Motostoke03` e `GoldenrodCity_BikeShop` caíam em "sem pasta" e saíam da conta sem virar
  vermelho. Ele passou a seguir o alias até o canônico, e o total subiu de **6.873 para 6.875
  conferidos, com 5.915 vivos**; os dois escondidos são VIVOS. O defeito é anterior a esta rodada (o
  BikeShop já estava cego) e cresce a cada família nova de alias.
- **A primeira versão do T155.2 era prova vazia**: as duas histórias, com placa e sem placa,
  terminavam no MESMO tile. Foi redesenhada até o par discriminar, e só então o negativo entrou.

### O que fica aberto

- **Próximas fatias de ROM, não executadas:** **blockdata cru ~1,5 a 2 MB**, o maior prêmio que
  sobra, mas é obra de MOTOR (comprimir `map.bin` e descomprimir na carga do mapa) e não de script;
  **metatiles crus ~600 KB**, mesma natureza; **glifos japoneses 130 KB**, barato e sem risco, e é
  por onde começar se a próxima rodada precisar de pouco. Com 1,26 MB livres, nada é urgente.
- **Lagos `LakeVerityLowWater` e `LakeAcuityLowWater`** seguem na fila: a trava é de ELEVAÇÃO (boca
  em 3, os 799 tiles em volta em 1), e o conserto honesto é converter o leito drenado do Platinum.
- **Sinnoh, objetos em 87,0%**, e nenhum balde é ferramenta parada: 128 nomes próprios sem sprite,
  ~100 com `hidden_flag` que esta ROM não tem, 115 bolas e 59 obstáculos recusados por tile fora de
  alcance, 90 canteiros de berry (id mora na SAVE) e 63 VENT e BOLLARD.
- **Galar, objetos em 93,5% e `script` em 55,6%**, com os 200 encontros de raide fora por decisão e
  89 recusados por geometria. `fila_b6.json` com 157 pendentes, `fila_galar.json` com 1.476 de 3.195.
- **Gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.
- **T143.9 é INSTÁVEL, e isso não é regressão desta rodada.** Ele reprovou na varredura de fechamento
  e passou **3 de 3 rodado sozinho**, na MESMA ROM (md5 `fb239ede296088906761daece2e7d6d5`), e tinha
  passado na varredura anterior do mesmo binário. A causa está escrita no próprio caso: a janela de
  apertos dele é de UM aperto (com 10 A o diálogo ainda rola, com 12 A o jogador já perdeu), e o
  jogador de teste entra sem time, então o instante em que a batalha fica aberta depende de RNG.
  Quem for mexer: o conserto não é aumentar a cauda, é dar um Pokémon ao jogador pelo
  `antes_do_warp`, como o T144.5 faz, para a batalha parar de se resolver sozinha.

---

## 0.o AS SEIS REGIÕES FECHAM O QUE DAVA PARA FECHAR, E A ROM ENCOSTA NO TETO, 22/08/2026 (rodada 7; condutor Opus, sete executores Opus, fechador Opus)

Build verde. **ROM 99,28% de 32 MB** (33.313.260 B, **241.172 B livres**, 235,5 KB; era 98,50% na
0.n), EWRAM 86,16% e IWRAM 86,68%. **Suíte 886 de 887**: a varredura normal deu 865/866 com só o
T11.3 pulado, e o bloco novo T153 deu **21/21**. **T11 3 de 3** contra a build `cf6786b2ae`
(worktree em `/private/tmp/claude-501/t11-antiga`), que é o primeiro 3/3 desde que o T11.1 foi
calibrado. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts numerados sem
nenhum movido** e **2.400 mapas** (eram 2.377); `valida_rom.py` com os 2.400 declarados dentro da
ROM; `guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois
perfis**; `valida_conectividade` com **0 warps quebrados** e nenhum mapa de Sinnoh ou Johto
inalcançável; `valida_warp_tile --piso 60` em 5.914 de 6.874 (86,0%, era 85,9%), nenhuma região
abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com **0 mapas com problema**. Os **26 `--demo`
de gerador tocados** rodaram verdes, dois deles depois de conserto (abaixo). ROM oficial
`roms/pokemon-claude-2026-08-22e.gba` (md5 `bba1d16835302015348c7bc374b66127`), com o `.map` ao
lado, e o MESMO binário na ROM de teste de nome fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | **100%** | **100,8%** | **100,1%** | **100,4%** | -- | **55 (0)** | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | **100%** | **87,0%** | 103,7% | **98,1%** | -- | **39 (18)** | 267 |
| Unova | **100%** | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 93,5% | 100% | **65,8%** | **55,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

### As decisões, e quem as tomou

Do **Gui**: "completa até ficar 100 em tudo", "agentes para melhorar as artes pobres das 5
primeiras regiões", **Galar travada em nível 255** e **seis regiões**, teto de pé.

Do **condutor**: **Galar fecha `objetos` em 93,5%** e os registros de "gráfico é cenário" ficam
sendo cenário, sem virar objeto; **a GS Ball sai** (não existe item nem cena que a use); o **trem
magnético de Saffron é corte declarado** (`SaffronMagnetTrainStation` entrou em `CORTES_DO_GUI`);
o **PWT é autorizado**; e os **nove andares novos do Distortion World FICAM**, com forma honesta e
arte chapada, com a decoração adiada para outra rodada.

### As sete frentes, com número

1. **Harness (T11).** O T11.1 contava o menu de START **de cima** e caía na tela de CARTÃO na ROM
   velha, porque `BuildNormalStartMenu` (`src/start_menu.c:332`) monta o TOPO conforme o estado do
   jogo e só o RABO é fixo: PLAYER, SAVE, OPTION, EXIT. Passou a contar **de baixo**, três UP a
   partir da linha 0, que `Menu_MoveCursor` (`src/menu.c:704`) faz dar a volta; junto veio
   `prova.sav_gravada`, que abre o `.sav` e cobra um slot inteiro escrito. T11 **3/3**.
2. **Galar, treinadores e placas.** `treinadores_galar.py`, `galar_fase_f.py` e `placas_galar.py`:
   **266 batalhas em 148 mapas** a nível 255, **38 chefes** com 17 lendários, 31 Mega e 7 Z, zero
   Dynamax e zero Tera; **206 times novos** em `trainers.party` (ids 3000 a 3205); placas de 44,1%
   para **65,8%** e `script` de 35,6% para **55,6%**; a fila de Galar caiu de 1.775 para **1.476
   de 3.195**. T147 **12/12**. Conserto de motor: **`trainerbattle_no_intro` NÃO consulta a flag de
   vitória**, então o gerador emite `goto_if_set TRAINER_FLAGS_START + id` antes dela, senão o
   treinador rebrigaria para sempre.
3. **Sinnoh, os 100% de mapa.** `converte_interiores_sinnoh.py`, `cria_mapas_sinnoh.py`,
   `corredores_sinnoh.py`, `bolas_sinnoh.py`, `pedras_sinnoh.py` e `importa_npcs_sinnoh.py`:
   **23 mapas novos** (90 KB), entre eles os 9 andares do Distortion World; mapas de 95,4% para
   **100%**; RavagedPath saiu de 133 tiles ilhados para **0**; objetos de 76,3% para **87,0%**;
   placas de 86,8% para **98,1%**; **166 bolas**, **51 obstáculos** e 30 clones removidos.
   T148 **9/9**.
4. **Johto e Unova, os 100%.** `completa_objetos_johto.py`, `completa_placas_johto.py`,
   `bolas_faltantes_johto.py`, `arco_farol_johto.py`, `cenas_pwt_unova.py` e
   `completa_placas_unova.py`, mais o **quebra-cabeça deslizante** como motor novo
   (`src/sliding_puzzle.c` e 13.476 B de arte comprimida), usado pelas quatro placas do
   `RuinsOfAlph_PuzzleAndRewardChambers`. Johto **100 / 100,8 / 100,1 / 100,4** e Unova
   **100 / 102,3 / 100 / 100,2**, com **2 vars novas** do PWT. T149 **14/14**.
5, 6 e 7. **Arte.** `arte_cavernas_sinnoh.py` em **70 mapas** (mediana de 8 para 21 metatiles
   distintos, T150 **6/6**), `arte_exteriores_sinnoh.py` em **11 salas** do ginásio D/P de
   Hearthome e na casa da Iron Island (de 12 para 27, T151 **6/6**) e `arte_mapas_pobres.py` em
   **4 mapas** de Johto e Unova (T152 **4/4**). Os **21 pobres de Hoenn são vanilla e ficam**, e o
   elevador de Virbank foi descartado no olho.

Nas três frentes de arte a regra é a mesma e está provada célula a célula no `--demo`: o gerador
escreve só os **10 bits de baixo** de cada célula do `map.bin`, então colisão, elevação e
comportamento saem byte a byte idênticos ao `git show HEAD:`.

### O que o fechador consertou

- **Os 12 casos que apertam SAVE** pelo menu do START passaram a contar **de baixo** (três UP) e
  ganharam `prova.sav_gravada`: T11.1, T120.9, T123.21, T127.3, T127.9, T136.1, T136.5, T139.3,
  T144.1, T145.3, T145.7 e T146.3. Dois apertavam três DOWN e dez apertavam dois, e a diferença era
  administrada à mão conforme o jogador tivesse ou não Pokémon.
- **Dois `--demo` vermelhos, os dois da mesma família: autoteste que não sabe que o gerador já
  rodou.** O `arte_exteriores_sinnoh.py` comparava a arte de DEPOIS com o DISCO (que já estava
  decorado) em vez do HEAD do git, e reprovava um gerador idempotente e correto; passou a usar
  `base`, como o `arte_mapas_pobres.py` já fazia. O `placas_galar.py` montava o plano só com o que
  ainda está `pendente`, e depois do `--aplicar` o plano fica VAZIO: ganhou `plano(incluir_feitas)`
  para o autoteste e um portão que soma o que já está no mapa.
- **Os lagos `LakeVerityLowWater` e `LakeAcuityLowWater` foram para a fila, com motivo**, e não
  consertados. Medido: o jogador chega pela boca e alcança **um tile, ele mesmo**, e a causa é
  ELEVAÇÃO, não colisão (a boca é elevação 3 e os 799 tiles em volta são elevação 1, água;
  `IsElevationMismatchAt`, `src/event_object_movement.c:10014`, barra 3 contra 1). Não é trava
  dura: a seta do warp devolve o jogador, e quem tem Surf entra na água. Corredor não resolve,
  porque as ilhas de chão de verdade são o metatile 0x201, preto puro de enchimento de caverna, e
  a passagem levaria ao vazio: o conserto honesto é **converter o leito do lago**, drenado no
  Platinum, e isso é obra de conversão.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/153_fechador_r7.json`, **21 casos, 21 verdes**, autor de caso
diferente do autor de cena em todos.

- **T153.1 a T153.4, Galar.** O treinador comum vencido não rebriga depois de **sair do mapa e
  voltar** (`WARP=` no roteiro) nem depois de **salvar e recarregar**, e o par negativo prova que
  sem a flag a batalha começa (`TRAINER_GALAR_RUAN_POKE_372`, flag 0x500+3137 = 0x1141).
- **T153.5 a T153.10, arte.** Um mapa decorado de cada gerador, com rota longa e leitura de NPC:
  MtCoronet2F (o Looker fala e solta o jogador), Mahogany B2F (o Lance cura e solta) e a segunda
  sala de elevador de Hearthome, onde não existe NPC com script nos 11 mapas daquele gerador e o
  que se prova é o corpo no mesmo tile do HEAD.
- **T153.11 a T153.15, Sinnoh.** O corredor novo do RavagedPath é atravessado em **16 pernas e 69
  tiles**, dos quais **nove eram parede no HEAD**, até uma item ball nova, pega **uma vez**; e os
  **três warps** do andar novo `DistortionWorld1F` disparam, um caso cada.
- **T153.16 a T153.18, Johto.** O quebra-cabeça deslizante **abre e toma o controle** (seis DOWN
  são engolidos), **fecha com B e devolve o jogador** (a perna seguinte anda quatro tiles), e o par
  negativo prova que sem abrir nada os mesmos apertos andam.
- **T153.19 a T153.21, Unova.** A cena do PWT dispara **uma vez**, com **save no meio**, e o
  recepcionista volta ao posto de (7,3) no fim da coreografia.

### Lições desta rodada

- **Aperto de direção que o jogador NÃO está encarando só VIRA, não anda.** Passo solto pede dois
  apertos quando muda de direção. Quatro casos do T153 reprovaram exatamente por isso.
- **Porta empurra um tile ao sul na chegada.** Quem entra por `MB_NON_ANIMATED_DOOR` não nasce na
  coordenada do warp. O primeiro T153.7 andava de (3,14), pisava de novo no próprio warp no meio da
  perna e caía no B1F.
- **O menu de START se conta de baixo**, porque o topo depende do que o jogo já liberou, e
  **`trainerbattle_no_intro` não consulta a flag de vitória**: quem desvia é o `goto_if_set`.
- **Stride do CFRU é 8/16 B** nos times da fonte de Galar, e **`planta_provisoria` está morta
  desde os túmulos**: nenhum mapa de Sinnoh veste mais o molde.
- **Autoteste tem de saber que o gerador já rodou.** Linha de base é o `git show HEAD:`, nunca o
  disco.

### O que impede 100% onde não chegou

- **Sinnoh, objetos em 87,0%**, e nenhum dos baldes é trabalho de ferramenta parado: **128** são
  nome próprio sem sprite aqui (Cynthia, Cyrus, os oito líderes, os lendários), **~100** têm
  `hidden_flag` do Platinum que esta ROM não tem, **115 bolas e 59 obstáculos** foram recusados por
  tile fora de alcance, **90** são canteiros de berry (id de árvore de berry MORA NA SAVE, então é
  obra de janela), e **63** são VENT e BOLLARD, cenário sem mecânica nativa.
- **Galar, objetos em 93,5% e `script` em 55,6%.** Faltam os 200 encontros de raide (o script da
  fonte sorteia até 59 espécies, e escolher uma seria inventar) e 89 recusados por geometria; a
  coluna `script` conta só NPC, e o que falta lá é fala, não colocação. Galar segue com **Dex 0**
  na régua, porque estático não conta como entrada de Dex de região.
- **Fila:** `fila_b6.json` com **157 pendentes** (150 de Sinnoh, 6 de Unova, 1 de Johto) e
  `fila_galar.json` com **1.476 de 3.195**.
- **Assimetria medida e CONSERTADA na 0.p** (quando esta seção foi escrita ela ainda estava de pé,
  e a frase original dizia "não consertada"): os **17 warps dos 9 andares novos do Distortion World**
  subiam sempre para o índice 0 do andar de cima, que é o warp de subida DELE e não o par
  correspondente; ninguém ficava preso, mas o jogador reaparecia no tile errado. O `simetriza` do
  `cria_mapas_sinnoh.py` corrigiu **9 `dest_warp_id` em 8 `map.json`** em 22/08/2026, e o T155.6
  desce a corrente inteira de uma vez.
- **O ramo de SUCESSO do quebra-cabeça deslizante não virou caso de suíte**: `CheckForSolution`
  (`src/sliding_puzzle.c:972`) exige as 24 casas na ordem e em `ORIENTATION_0`, o que não sai de
  martelada de botão; é pendência de FERRAMENTA, como a vitória do estático único da 0.n.

### O teto de ROM, e o que ele custa a partir de agora

**A ROM está em 99,28% de 32 MB, com 241.172 B livres**, e esta rodada gastou 261.332 B: nesse
ritmo resta menos de uma rodada. **A próxima obra grande exige o B10** (compressão de ícones mais
indireção de tabela de treinador, ~1,1 MB estimados) **ou um corte novo declarado pelo Gui**; a
economia mais óbvia continua sendo tirar da ROM os mapas que o `PLANO-ESCOPO.md` já cortou e que
hoje ainda compilam.

**Para o Gui olhar**: as três folhas de contato da arte nova estão em
`scratchpad/arte/sinnoh-cavernas/CONTATO.png`, `scratchpad/arte/sinnoh-exteriores/CONTATO.png` e
`scratchpad/arte/johto-unova-hoenn/CONTATO.png`, e são a única coisa desta rodada que depende de
gosto e não de medida.

---

## 0.n GALAR GANHA OS 795 POKÉMON DO OVERWORLD, E A RÉGUA VOLTA A FECHAR, 22/08/2026 (rodada 6; condutor Opus, um executor Opus, fechador Opus)

Build verde. **ROM 98,50% de 32 MB** (33.051.928 B, 490,7 KB livres; era 98,43% na 0.m), EWRAM
86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 814/815** (só o T11.3 pulado na rodada
normal), **T146 10/10** e o **T11 em 2 de 3** contra a build `cf6786b2ae`
(`/private/tmp/claude-501/t11-antiga`), com esse vermelho explicado no fim desta seção. **SAVE
COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B e 2.032 layouts sem nenhum movido;
`valida_rom.py` com os 2.378 mapas declarados dentro da ROM; `guarda_colisao_vars.py` com 23
colisões herdadas e **0 novas nos dois perfis**; `valida_conectividade` com **0 warps
quebrados**; `valida_warp_tile --piso 60` em 5.869 de 6.829 (85,9%, igual à 0.m); `--demo`
tocados verdes. ROM oficial `roms/pokemon-claude-2026-08-22d.gba` (md5
`17e5f891bfb0862e8443644ff73a3e74`), com o `.map` ao lado, e o MESMO binário na ROM de teste de
nome fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | 76,3% | 100,9% | 86,8% | -- | 39 (76) | 267 |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | **93,5%** | 100% | 44,1% | 35,6% | 48 (32) | 0 |

### O bloco c5: 795 Pokémon parados no mapa, como em Sword/Shield

Decisão do Gui: **o teto de seis regiões fica de pé, Galar fica, e o conteúdo próprio dela
entra.** Caiu com ela o descarte de 18/08 ("gráfico de Pokémon mentiria a espécie"), verdade
naquele dia e não mais: `OBJ_EVENT_GFX_SPECIES` existe nesta build e o `distribui_dex.py` já
punha 106 estáticos com ela. `dev_scripts/estaticos_galar.py`: **795 encontros em 68 mapas**
(791 comuns e 4 únicos), 79 espécies, 145 cenas no `.inc` e **4 flags** (0x1D0A a 0x1D0D,
apelidos de `FLAG_UNUSED`, save intocada); a fila de Galar caiu de 2.570 para **1.775 de
3.195**. A espécie sai da `gSpeciesNames` da PRÓPRIA ROM da fonte, achada por âncora, **por NOME
e nunca por id** (o 331 do demake é `Sharpedo`); nome repetido é forma e só entra com decisão
escrita uma a uma.

**Comum e único são medidos, não arbitrados.** Único é aquele cujo script da fonte acende a
própria flag de esconder: gasta flag e a acende só em vitória ou captura. Comum não gasta flag
NENHUMA, e é isso que o faz renascer quando o mapa recarrega. **De fora ficaram 293 linhas com
motivo contado**: 200 de raide (o script sorteia até 59 espécies, e escolher uma seria
inventar), 89 de geometria, 3 de forma e 1 de id fora da tabela da fonte; nenhuma caiu por teto
nem por janela.

**O 859 do plano era 1.092.** Remedido sobre a MESMA fonte: 1.092 linhas de `script_objeto`
carregam `setwildbattle`, e 1.088 são de objeto que o G4 não pôs no mapa. Nenhuma definição
testada devolve 859: cita-se 1.092, e a régua divide por 1.088, que é o recorte de objeto.

### Os dois defeitos de motor, que viram lição

1. **`VAR_LAST_TALKED` não guarda id entre a batalha e o fim do script**, porque
   `ProcessPlayerFieldInput` regrava essa var a cada quadro em que o jogador tem controle:
   `removeobject VAR_LAST_TALKED` depois de `dowildbattle` é aposta na ordem dos quadros. O
   gerador guarda o id em `VAR_TEMP_1` ANTES da batalha, e o **T146.7** martela LEFT na saída da
   batalha: passou **5 de 5 execuções seguidas**.
2. **Remover o objeto ANTES da batalha congela o jogador**: a ordem é a da fonte. E
   **`FLAG_SYS_CTRL_OBJ_DELETE` não é lida por ninguém neste fork**: fica no script do único
   porque é o idioma do vanilla, não porque faça efeito.

### A régua contava o mesmo objeto duas vezes, e o `--demo` dela dizia

Vermelho real da rodada. A primeira versão somava os **795 que NÓS gravamos** nos dois lados da
coluna `objetos` E mantinha esses mesmos 795 dentro de `obj_impossiveis`: as partes deixavam de
somar o todo (1.906 + 3.051 = 4.957 contra 4.162 da fonte) e o `completude.py --demo`
**reprovava**. Pior que a soma: denominador feito da própria resposta lê 100% para sempre, e os
293 que a fonte tem e nós não pusemos sumiam; o `--detalhe` ainda imprimia "sobram 1.111
colocáveis" com o divisor já em 1.906.

Conserto: o denominador sai do **lado da fonte**, por um censo que o próprio gerador escreve
(`dev_scripts/galar_estaticos.json`, `da_fonte: 1088`), e os 1.088 saem dos impossíveis e entram
nos colocáveis. Galar `objetos` vai a **93,5%** (2.055 de 2.199) no lugar dos 107,8% de antes, e
1.963 + 2.199 = 4.162 fecha. A coluna `script` conta **só NPC** (448 de 1.260, 35,6%): estático
já nasce com script, e misturá-lo levaria a coluna a 60,5% sem uma linha de fala nova.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/146_fechador_r6.json`, 10 casos, 10 verdes.

- **T146.1 e T146.2, o comum renasce sem passar pelo save.** Numa execução só: batalha, fuga, o
  Skwovet some, o jogador SAI para o `Galar_WildArea05` e VOLTA, e o corredor volta a barrar em
  (19,17); o par sem a ida e volta anda os 41 tiles até (7,17) e é quem isola a carga de mapa.
  Pediu ferramenta nova: `WARP=MAP_X[:id]` no roteiro (`expande_warps` em `testa_critico.py`),
  com o mapa resolvido pela tabela.
- **T146.3 e T146.4, o único que NÃO se apaga.** O T145.7 acende a flag na mão e passa nos dois
  mundos; aqui a batalha termina em FUGA, e a flag tem de seguir apagada e o Slowpoke sólido,
  inclusive depois do save.
- **T146.5, T146.8, T146.9 e T146.10: os cinco warps do mapa mais cheio.** O
  `Galar_CrownTundra08` tem 43 objetos de 64 (15 herdados, 28 do c5); somados ao T145.9, os
  cinco ficam provados com o mapa cheio. **T146.6**: no mesmo mapa o NPC de cena de (22,54)
  continua acordando, prova de que o herdado não perdeu a vez na janela de sprite, com os
  encontros no FIM da lista de templates.
- **A prova de que o recusado NÃO está no mapa é de SCRIPT**, porque tile não andável, ocupado e
  inalcançável são onde o jogador não chega, e andar por cima não separa "o objeto não existe"
  de "não consigo chegar lá". Virou o portão 9 do `--demo` do gerador: chave recusada não
  aparece em `map.json` nenhum, chave aceita aparece uma vez, e não há objeto nosso com chave
  que a fonte não tenha.

### O que fica aberto para o Gui

- **A curva de Galar (pergunta 16)**: o nível é o da fonte, cru, e a fonte é de pós-jogo, então
  Galar ainda nasce em nível alto. **Os 200 de raide e os 89 de geometria** seguem na fila. E
  **Galar continua com Dex 0 na régua**: estático não conta como entrada de Dex de região, e
  ligar isso é escopo.
- **Vencer o estático único não virou caso de suíte.** A vitória FOI medida à mão (a flag foi de
  0 para 1 e o objeto saiu do mapa), mas o Pokémon do menu de debug chega à batalha DORMINDO em
  parte das execuções, sem que o inimigo tenha golpe de sono: flaky por construção, e pendência
  de FERRAMENTA.
- **`lendarios_sinnoh.comportamento` não julga warp morto**: responde MB_NORMAL para os warps 1,
  3 e 4 do `Galar_CrownTundra08` e os três disparam. **T108.2 é flaky**: reprovou por "não andou"
  numa varredura, passou na outra e 3 de 3 isolado.
- **O T11 está 2 de 3, e o verde do T11.3 NÃO vale hoje.** O T11.1 passa, mas o menu de SAVE
  dele para na TELA DE CARTÃO na ROM velha (medido no framebuffer): a save nunca é escrita, e o
  T11.2, que é o controle, cai num menu principal SEM "CONTINUE". Com save inválida, o T11.3
  ("a ROM nova RECUSA a save velha") passa por não ter o que carregar: verde falso. Reprova
  igual com o `testa_critico.py` do HEAD, ou seja não é desta rodada; é calibração do roteiro
  do T11.1 contra a ROM velha.
- **Gens 6, 7 e 9 andaram FORA do repo**, em `fontes-mapas/`: scripts de XY extraídos, Alola com
  268 treinadores com lugar por guia e Paldea com 23 interiores. E seguem abertos os cinco itens
  da 0.m, do `valida_warp_tile` sem linha de base às duas salas do Mt. Coronet.

---

## 0.m O WARP DE OBJETO DE GALAR ANDA, E O ELENCO QUE FALTAVA ENTRA, 22/08/2026 (rodada 5; condutor Opus, dois executores Opus, fechador Opus)

Build verde. **ROM 98,43% de 32 MB** (33.026.864 B, 515,2 KB livres; era 98,38%
na 0.l), EWRAM 86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 794/795**
(só o T11.3 pulado na rodada normal), **T11 3/3** à parte contra a build
`cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`), **SAVE
COMPATIVEL** com SaveBlock1 em 14.964 de 15.872 B e 2.032 layouts numerados sem
nenhum movido, `valida_rom.py` com os 2.378 mapas declarados dentro da ROM,
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0
novas nos dois perfis**, `valida_conectividade` com **0 warps quebrados e nenhum
órfão novo**, `valida_warp_tile --piso 60` com 5.869 de 6.829 warps disparando
(85,9%, igual à 0.l) e os cinco `--demo` de gerador tocados verdes. ROM oficial:
`roms/pokemon-claude-2026-08-22c.gba` (md5 `462fef1424fc2ae5b467346df11f518a`), com o `.map` ao
lado, e o MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | 76,3% | 100,9% | 86,8% | -- | 39 (76) | 267 |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | 113,4% | 100% | **44,1%** | **35,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.
### As decisões desta rodada

Do Gui: **"pode continuar isso aí tudo"**, que autorizou as duas frentes de uma
vez; **Primal para Maxie e Archie**; **importar o que a fonte tiver**, sem
inventar batalha nenhuma; e o **teto de seis regiões fica de pé**.

Do condutor: **no chefe de equipe vilã a lore vence** (herança da 0.l, e é ela
que põe o orbe na mão do vilão e não do herói). **Kalos, Alola e Paldea não entram no repo**: material e julgamento ficam em
`fontes-mapas/` (`PLANO-OBRAS-KALOS/ALOLA/PALDEA.md`,
`AUDITORIA-PRONTIDAO-2026-08-22.md`, `INFRA-GENS-6-9.md`).

### Frente 1: Galar, blocos c4e e c4f, e o warp que sempre esteve certo

`objetos_galar.py` e `cenas_galar.py`: **58 cenas de objeto em 34 mapas** (eram
31 em 15 na 0.l), com **7 flags de esconder** na faixa 0x1C80 (apelidos de
`FLAG_UNUSED`, save intocada), **5 vars de etapa do c4d** e as 5 do c3 reusadas.
A fila de Galar caiu de 2.597 para **2.570 de 3.195**, a coluna `script` subiu de
33,6% para **35,6%** e a de placas de 43,1% para **44,1%**. T142 4/4 e T130 10/10.

**O `warp` de objeto nunca esteve quebrado.** A 0.l deixou como pré-requisito do
c4e um "aviso grave" dizendo que `warp` de script de objeto traduz mas não troca
de mapa, e que `warp` seguido de `waitstate` prende o jogador para sempre. Está
errado, e a receita boa é justamente a proibida: **`warp` mais `waitstate`**. O
que estava quebrado era a SONDA: ela entrou pelo warp de debug num mapa SEM warp
nenhum (`Galar_StowOnSide02`, `Galar_Wedgehurst09`), pedindo um índice de warp
que não existe, e isso deixa o estado de warp do jogador sujo. A cena rodava e a
troca de mapa não acontecia, e o defeito era do banco de provas. O parágrafo
velho do `PLANO-CONTEUDO-GALAR.md` ficou marcado como vencido, para lembrar que
conclusão tirada de sonda montada errado custou uma rodada de bloco caro.

**O de-para de opcode: 214 contra 214.** A `gScriptCmdTable` do demake tem o
mesmo tamanho da do FireRed, ou seja **nenhum opcode novo**, e o c4e não pedia
motor. O buraco era do nosso lado: o parser de `fala_galar.py` só guardava o
PRIMEIRO ramo das macros de dois ramos (`.ifb \map`), e `applymovement_at` (0x50),
`waitmovement_at` (0x52), `removeobject_at` (0x54) e `addobject_at` (0x56) caíam
no balde de "opcode indecodificável". Conferido pelo fechador: a tabela responde
213 opcodes com tamanho, com os quatro `_at` dentro. E o bloco c4f resolve
`special` por NOME e não por índice (o do FireRed não é o nosso, e por número a
função errada entraria calada): **192 nomes em comum** (444 na tabela do FireRed
contra 623 na nossa, conferido pelo fechador), e de fora ficam **64 chamadas de
`GetQuestLogState`**, motor de Quest Log que não existe aqui.

### Frente 2: Fase F, o Primal, e as batalhas que a fonte tinha

**Primal em Maxie e Archie, sem gastar o gimmick.** O motor foi medido ANTES de a
tabela mudar: a Primal Reversion **não está no `enum Gimmick`**
(`include/battle_gimmick.h:4`), roda sozinha na entrada em campo
(`src/battle_switch_in.c:276`) e não passa por escolha de gimmick nenhuma. Ou
seja o Red Orb no Groudon do Maxie e o Blue Orb no Kyogre do Archie **convivem**
com a Mega Camerupt e a Mega Sharpedo dos aces, e a regra "um gimmick por chefe"
segue de pé. O guarda do gerador aprendeu orbe (`--demo` 10/10, com a mutação de
orbe em espécie sem Primal reprovando).

**Seis batalhas que a fonte tinha e este repo não**, mais oito de uma segunda
leva, todas importadas e nenhuma inventada: SILVER 5, 6 e 7 (ids 2523 a 2525,
fechando as sete batalhas de rival do HGSS), `RYOKU1` (2526), **N** (2527),
HUGH_TEPIG (2528), BIANCA (2529), CHEREN_2 (2530) e as **seis variantes de
Nate/Rosa** (2531 a 2536, gênero vezes inicial, times idênticos mon a mon como na
fonte). A Fase F fecha em **198 batalhas e 1.054 Pokémon**, com Dynamax em 5 (teto
5) e Terastal em 6 (teto 6), as cotas do Gui gastas e não estouradas. T143 22/22.

**O N mudou de tile de propósito**: ficou em (0,4) do `Unova_NsRoom`, o ÚNICO
tile de porta do mapa; quem sai da sala é quem venceu, e o `setflag
FLAG_HIDE_UNOVA_N` mais `removeobject` do fim da batalha é o que devolve a porta.

**Quem NÃO existe na fonte, e por isso não entrou**: Ghetsis, o Shadow Triad,
Courtney e Charon. Dos dois primeiros o BW3G tem texto e nome de música, e nem
constante nem time. Isso sai da fila como inexistente, não como pendência.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/144_fechador_r5.json`, 9 casos, 9 verdes.

- **T144.1 a T144.4, o warp de objeto com SAVE no meio.** O T130 prova a receita
  dentro de UMA execução, e execução única não responde se o `warp` de script
  grava `SaveBlock1.location` do jeito que o SAVE espera. Aqui o T144.1 dá
  `ITEM_GO_GOGGLES` pelo menu de debug, sai de `Galar_Underwater01` pelo objeto
  de (32,9) e SALVA já do outro lado; o **T144.2 carrega ESSA save** e faz a
  volta, que passa por `checkitem`, ou seja também prova que a bolsa sobreviveu.
  O T144.4 é o portão: sem os óculos a volta cai no texto de recusa e o jogador
  fica parado. De quebra ficou medido que a `Galar_WildArea17` tem `warp_events`
  VAZIO e o `warp` de script funciona nela do mesmo jeito.
- **T144.5 e T144.6, e eles pediram ferramenta nova**: a suíte sabia dizer QUAL
  Pokémon estava no slot e em que nível, e não sabia dizer se ele estava
  machucado, então cena de enfermeira e cena que só imprime texto eram
  indistinguíveis. O `gba_runner` ganhou **`--hp`** (hp0..hp5 e hpmax0..hpmax5,
  com os offsets medidos pelo probe, porque hp e maxHP ficam FORA do bloco
  cifrado) e o passo de roteiro **`HP=slot=valor`**, que existe porque não há
  caminho de jogo determinístico que machuque um time. Com o Bulbasaur em 1 de
  HP, a enfermeira de `Galar_Wedgehurst03` devolve o HP cheio; o par negativo
  refaz tudo sem apertar A e o HP fica em 1 cravado. **Achado do caso**: o
  `Party… > Set Party` do menu de debug NÃO serve para isto, porque
  `DebugAction_Party_SetParty` não atualiza `gPartiesCount` e `HealPlayerParty`
  itera até ele; com Set Party o time existe na memória e a cura não toca nele.
- **T144.7**: o N sai da porta. O T143.11 prova que a batalha abre e o T143.12
  que o jogador esbarra nele; nenhum dos dois chega ao DEPOIS. Com a
  `FLAG_HIDE_UNOVA_N` acesa (o estado de quem venceu), os MESMOS dois passos do
  T143.12 pisam em (0,4) e o jogador SAI da sala. NPC parado em cima da única
  porta é sala sem saída enquanto ele estiver lá, e agora isso tem caso.
- **T144.8**: o ramo de GÊNERO do Nate/Rosa. O T143.19, o T143.21 e o T143.22
  varrem os três valores do inicial e param todos do MESMO lado do primeiro teste,
  porque a abertura da suíte grava gênero masculino: as três ROSA eram código
  morto para a suíte. Com o `Player… > Toggle gender` do debug e mais nada
  mudando, o oponente passa a ser `TRAINER_UNOVA_ROSA_OSHAWOTT`.
- **T144.9**: os portões dos três Silvers novos não são apelidos um do outro.
  0xEDB e 0xEDC são vizinhas, e trocá-las daria um jogo em que vencer o Silver 5
  faz aparecer o Silver 7, sem erro de build e sem vermelho. Com só a 0xEDB
  acesa, o Centro Pokémon do Indigo Plateau tem que ficar vazio.

### O vermelho que o fechador achou, e o conserto é de uma função

`cenas_galar.py --demo` **nasceu vermelho** nesta árvore: "segunda passada ainda
mexeria em vars.h". Nenhuma letra de conteúdo mudava, só a ORDEM: `poe_bloco`
apagava o bloco marcado e colava o novo no FIM do arquivo, então dois geradores
que escrevem no MESMO header (o bloco c1 daqui e o c4d do `objetos_galar.py`, que
chama esta mesma função) ficavam trocando de última posição a cada rodada. Agora
o bloco é trocado NO LUGAR e o fim do arquivo só é usado quando o bloco é novo.
Os dois `--demo` ficaram verdes e o conteúdo dos headers não mudou uma linha.

### O que fica aberto para o Gui

- **Galar, o que sobrou do c4**: **340 chamadas de `special`** que dependem do
  Quest Log do FireRed, **1.398 linhas de objeto que não estão no mapa** (descarte
  do condutor de 21/08) e **859 encontros estáticos** da fonte medidos e parados,
  esperando decisão de sprite. Galar segue com **zero linha de encontro** e Dex 0.
- **A curva de Galar**: a fonte é de pós-jogo (mediana 70, 276 times no nível
  100). Importada crua, Galar inteira nasce em nível 100.
- **Fase F**: a moldura de torneio da Bianca **não foi portada** de propósito (na
  fonte ela é `scene_script` com `priorityjump`, `setmapscene` e `warpcheck` do
  PWT); só a batalha entrou.
- **Gens 6, 7 e 9**: assets e planos em `fontes-mapas/`, fora do repo, como acima.
- Seguem abertos, da 0.l: `valida_warp_tile` sem linha de base, as 19 bolas de
  neve de Snowpoint, as 31 pedras de Sinnoh, a alcançabilidade de `RavagedPath` e
  de duas salas do Mt. Coronet.

---

## 0.l A DEX FECHA EM 1.571, OS VILÕES ENTRAM E OS CORTADOS SAEM DA ROM, 22/08/2026 (rodada 4; condutor Opus, quatro executores Opus, fechador Opus)

Build verde. **ROM 98,38% de 32 MB** (33.011.952 B, 529,8 KB livres; era 98,85%
na 0.k, ou seja meio ponto e cerca de 150 KB devolvidos), EWRAM 86,16% e IWRAM
86,66% (iguais às de ontem), **suíte 757/758** (só o T11.3 pulado na
rodada normal), **T11 3/3** à parte contra a build `cf6786b2ae` (worktree em
`/private/tmp/claude-501/t11-antiga`), **SAVE COMPATIVEL** com SaveBlock1 em
14.964 de 15.872 B e agora com o **`mapLayoutId` coberto**, `valida_rom.py` com
os 2.378 mapas declarados dentro da ROM, `guarda_colisao_vars.py` com 23
colisões herdadas em vars e 5 em flags e **0 novas nos dois perfis**,
`valida_conectividade` com **0 warps quebrados e nenhum órfão novo**,
`valida_warp_tile --piso 60` com 5.869 de 6.829 warps disparando (85,9%), e os
oito `--demo` de gerador tocados verdes. ROM oficial:
`roms/pokemon-claude-2026-08-22b.gba` (md5 `470666cf982cec334a950db80987a4ea`), com o `.map` ao lado, e o
MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,0% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | **76,3%** | 100,9% | 86,8% | -- | 39 (**76**) | **267** |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | 113,4% | 100% | 43,1% | **33,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%.** Os três números de Sinnoh que CAÍRAM
(objetos 82,7 → 76,3, arte pobre 102 → 76, Dex 295 → 267) não são regressão de
obra: são honestidade. Os 111 mapas cortados viraram túmulo e pararam de
emprestar objeto, arte e encontro a uma coluna que os contava.

### As decisões desta rodada

Do Gui: **"completa a dex, falta 5; pode continuar"**; os **ginásios ficam** como
estão (pergunta 3); e o **Giovanni de Tohjo Falls mantém os níveis 111 a 114**
(pergunta 6), com a palavra dele, *"a curva pode ter outliers coerentes"*.

Do condutor: **no chefe de equipe vilã a lore vence, e o herói é quem cede**
(Maxie fica com Groudon e Archie com Kyogre; Brendan cede para Latios e Wallace
para Palkia); a **`RockPeakRuins` entra no corte da Battle Zone**; e importar
Ghetsis, N e o Shadow Triad **depende de a fonte tê-los**, o que ninguém mediu
ainda, então segue hipótese e não promessa.

### Frente 1: a Dex fecha em 1.571, e o buraco era do CENSO

A 0.k dizia 1.566 e culpava mecânica de troca de forma. Estava errada, e o
conserto é de UMA função: `censo_dex.censo()` fechava um passo só de forma, e as
cinco que faltavam saem de correntes de DOIS e TRÊS passos (Deoxys-Defesa e
Deoxys-Velocidade vêm do Deoxys-Ataque, que vem do Normal; as três formas de
Zygarde saem umas das outras pelo Cube). Com o fecho em cadeia o repositório
responde sozinho, e nenhum estático novo foi preciso. A obra acrescentou os **nove
itens de troca de forma**, entregues pelo NPC do laboratório do Birch com
`checkitem` de guarda antes de cada `additem`. T137 2/2, mais sonda.

**O que o fechador consertou**: a remoção física apagou a tabela de mato da
`Route229`, **única casa de Surskit e Masquerain no jogo inteiro**, e o censo
voltou a 1.569. O conserto é pelo gerador, com a régua nomeada: nasceu
`REPOE_NA_REGIAO` em `distribui_dex.py`, a **única exceção à regra 3** (gen 1 a 5
vai para a região da geração), porque isto é REPOSIÇÃO de um lar que obra nossa
destruiu. O Surskit voltou para `MAP_CANALAVE_CITY`, `fishing_mons`, slot
duplicado 1, em Sinnoh; o **Masquerain não ganha linha e não precisa**, porque é
Bug/Flying, a regra 6 proíbe água para quem não é `TYPE_WATER`, e ele sai do
Surskit por `EVO_LEVEL`.

**O defeito que esse conserto revelou vale mais do que ele**: o `decide_selvagem`
não era estável contra árvore já mexida. Espécie nova no meio da lista empurrava
a escolha de todas as seguintes um slot adiante, e o `aplica_selvagem` deixava
ÓRFÃ a linha antiga que a tabela nova não mencionava mais. Medido: o
replanejamento mexia em NOVE linhas que ninguém pediu, uma delas deixando a
`SeafloorCavernRoom1` com um Salazzle-Totem no lugar do Zubat **para sempre**.
Agora quem já tem escolha gravada e ainda válida FICA ONDE ESTÁ, e o
replanejamento tocou **duas** linhas. Conferido contra o `git`: o
`wild_encounters.json` de hoje difere do de `852be4632a` em **2 slots**, zero
níveis e zero tabelas redimensionadas.

O `diff_do_mato` (T129.13) também estava vermelho e ninguém tinha rodado: exigia
o CONJUNTO de tabelas idêntico ao de `0cb8724099`, e 26 saíram legitimamente com
os cortados. Agora sumir só vale para mapa cortado e **nascer nunca vale**.

### Frente 2: os 40 chefes de equipe vilã

`fase_f_chefes.json` com `papel: "vilao"`, o mesmo gerador idempotente: **40
batalhas, 228 Pokémon, 18 lendários distintos, 39 Mega e 1 Z, e ZERO Dynamax e
Tera novos** (as cotas do Gui, 5 e 6, seguem gastas nos 144 chefes da primeira
leva). A Fase F vai a **184 batalhas e 970 Pokémon**, com a curva de nível
intocada. As quatro trocas de Hoenn foram feitas pelo gerador e não à mão, e **nem
Groudon nem Kyogre ganharam orbe de Primal**, de propósito: Primal entraria POR
CIMA da Mega Camerupt e da Mega Sharpedo e quebraria o "um gimmick por chefe" sem
que o guarda visse, porque ele só conhece pedra de Mega e cristal Z. Tabela e
razão de cada lendário em `PLANO-FASE-F.md`. T138 2/2.

### Frente 3: Galar, blocos c4b a c4d

`objetos_galar.py`: **31 cenas de objeto em 15 mapas e 30 cenas de mapa**, com **5
flags de esconder** (`FLAG_GALAR_ESCONDE_*`, 0x1C80 a 0x1C84, apelido de
`FLAG_UNUSED`, save intocada) em **10 objetos** e **5 vars de etapa**. A fila de
Galar caiu de 2.622 para **2.597** e a coluna `script` subiu de 31,7% para 33,6%.
T139 6/6.

**Diagnóstico pendente, e pré-requisito do c4e**: `warp` dentro de script de
OBJETO traduz e a cena roda, mas **não troca de mapa**; e `warp` seguido de
`waitstate` **prende o jogador para sempre**. Até isso ser entendido, nenhuma
cena portada pode usar `warp`.

### Frente 4: os 111 mapas cortados saíram da ROM, e nenhum id andou

`dev_scripts/remove_mapas_cortados.py`. **111 mapas viraram túmulo** (110 da
primeira medição mais a `RockPeakRuins`, acrescentada pelo fechador por decisão do
condutor: o único warp dela ia para a `Route228` e sem ela o mapa ficava sem
caminho nenhum; as irmãs `IronRuins` e `IcebergRuins` NÃO entram, e foi medido,
porque saem da `IronIslandB3F` e do `MtCoronet_1F_North_Room2`, dois mapas vivos).
**45 layouts exclusivos encolhidos para 1x1**, **26 tabelas de mato fora**, **29
portas fechadas em 23 mapas vivos** com **22 placas** (a 23ª foi embora com a
`RockPeakRuins`), e **24 casos de suíte** que morriam nos cortados removidos.

**Por que a entrada da tabela NÃO é apagada**, e este é o parágrafo que salva a
próxima pessoa: a save guarda **índices**, e são dois.
`SaveBlock1.location.mapGroup`/`mapNum` (0x04) é a POSIÇÃO do mapa dentro do
grupo, e os 111 cortados estão espalhados NO MEIO de nove grupos (o
`gMapGroup_IndoorSinnohPortas` perde 38 de 128, do índice 1 ao 123), então apagar
a entrada desloca todo mapa vivo que vem depois. E `SaveBlock1.mapLayoutId` (0x32)
é o ordinal do layout, e por isso o layout **encolhe** para 1x1 em vez de ser
apagado. Pelo mesmo motivo o warp que ia para túmulo vira **lápide**: a entrada
fica no MESMO índice e passa a repetir as coordenadas do warp vivo de menor índice
do mapa, porque `dest_warp_id` também é índice e a `HearthomeCity` sozinha
perderia os índices 7 e 8 de 16 e desalinharia 14 ponteiros de terceiros. Duas
entradas no mesmo tile: `GetWarpEventAtPosition` devolve a PRIMEIRA, então o
doador ganha e a lápide nunca dispara.

### A guarda nova: `mapLayoutId`, o ponto cego que a própria remoção denunciou

`guarda_save.py` agora cobre o `mapLayoutId`, e a régua **replica o gerador**
(`tools/mapjson/mapjson.cpp:895`) em vez de contar posições no JSON: o número do
layout é a posição contando SÓ os layouts cujo `border_filepath` existe no disco.
Medido: **2.167 entradas no `layouts.json` e 2.032 numeradas**, conferido contra o
`layouts.h` gerado, divergência zero. A consequência é a que assusta: **apagar um
`border.bin` desloca o id de todo layout seguinte**, sem mudar uma letra de
arquivo nenhum e sem erro de compilação, e a save parada lá carrega a geometria de
outro mapa. É por isso que a remoção encolhe o `border.bin` em vez de apagá-lo. O
lado velho vem de `852be4632a` por `git ls-tree` enquanto a impressão gravada não
tiver a chave. Rodado hoje: **2.032 layouts, nenhum movido**.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/141_fechador_r4.json`, 8 casos, 8 verdes, cada um
com o par negativo.

- **T141.1 e T141.2**: o T138 provou o Cyrus de Sinnoh e **nenhum caso chegava a
  um Maxie**, que é justamente onde a troca do Groudon foi feita. Agora o caso
  entra pelo warp 1 do `MagmaHideout_4F`, anda três tiles, abre a cena do
  despertar do Groudon e lê `gParties` decifrado: Groudon no slot 4 e Camerupt no
  ace com `ITEM_CAMERUPTITE`. Os números vieram do pré-processador (Groudon 383,
  Cameruptite 323) e não da saída do runner, senão a prova seria circular.
- **T141.3 e T141.4, e este NASCEU VERMELHO**: a suíte só sabia ler o TIME, e item
  de troca de forma não entra em `gPlayerParty` nenhum, ou seja os nove `additem`
  poderiam estar vazios sem um caso reclamar. O `gba_runner` ganhou `--bolsa` +
  `--item`, que varre a bolsa e DECIFRA a quantidade com os 16 bits baixos de
  `encryptionKey` (`src/item.c`), com os offsets medidos pelo probe e nunca
  chumbados. **O achado é do caso**: dos nove itens só CINCO são
  `POCKET_KEY_ITEMS`, e os quatro néctares de Alola são `POCKET_ITEMS`, ao
  contrário do que o comentário do gerador dizia. Por isso a varredura é do
  `struct Bag` inteiro.
- **T141.5 e T141.6**: o T139 prova a mecânica de esconder no `CrownTundra08`, que
  tem UM objeto com flag nova. O `Galar_Hammerlocke05` tem DOIS, e é nele que
  trocar as duas passaria calado; pior, a cena faz `removeobject 4` e
  `removeobject 5`, que são LOCAL IDs de base 1, ou seja os objetos de ÍNDICE 3 e
  4 do `map.json`, e errar a base por um apagaria o vizinho. Com a `BA7` acesa o
  jogador atravessa (16,10) e sai do mapa; com a `BA8`, a do outro NPC, para em
  (16,11).
- **T141.7 e T141.8**: a lápide no caso mais apertado que existe. No
  `CanalaveCityPokecenter1F` a escada do 2F virou uma SEGUNDA entrada em (6,8), o
  mesmo tile do warp 0 que sai para a cidade; pisar ali sai em `MAP_CANALAVE_CITY`
  (28,23), sem travar. Medido de quebra: (1,6), o tile da escada velha, é colisão
  sólida, então aquele warp **nunca disparava nem antes**.
- **T129.18, fora do emulador**: nenhuma das 234 linhas de mato aponta para tabela
  morta (o Burmy-Planta apontava, e o `--selvagem` morria com `SystemExit`), e o
  Surskit está em água de Sinnoh e deixou de ser inobtenível.
- **Passo 5 do `remove_mapas_cortados --demo`**: a pergunta do condutor, "dá para
  entrar num túmulo pelo seletor de capítulo?", foi respondida por medição. **Não,
  e nenhum capítulo precisou sair**: o seletor (`src/chapter_jump.c`) só oferece
  `HEAL_LOCATION` de cidade de ginásio e de Liga. O que faltava era a trava,
  porque o Chapter Jump é o único caminho do jogo que ignora warp: cortar uma
  cidade de ginásio um dia daria um capítulo que larga o jogador num mapa vazio
  SEM SAÍDA, e nem o build nem a suíte diriam nada.

### O que fica aberto para o Gui

- **`warp` em script de objeto de Galar**, o diagnóstico acima, e os blocos **c4e
  (390 indecisos)** e **c4f (282 de `special`)**, os dois caros.
- **A Dex de Galar**: 859 encontros estáticos da fonte medidos e parados,
  esperando decisão de sprite. Galar segue com zero linha de encontro.
- **Importar as batalhas que não existem**: as três de Silver, a `RYOKU1`, os
  rivais do BW3G e, do lado vilão, Ghetsis, N, o Shadow Triad, Courtney e Charon.
  **Ninguém mediu a fonte ainda**, e o BW3G pode não trazê-los, como não trouxe
  rival nenhum.
- **Primal para Maxie e Archie**, se o Gui quiser: custa trocar o gimmick deles.
- **`valida_warp_tile` sem linha de base**: os 85,9% de hoje não têm com o que ser
  comparados, e o portão só cobra piso de 60% por região.
- Seguem abertos, da 0.k e da 0.j: as 19 bolas de neve de Snowpoint, as 31 pedras
  de Sinnoh, a alcançabilidade de `RavagedPath` e de duas salas do Mt. Coronet, e
  a curva de Galar.

**Dívida quitada**: o `T93.6` e o `T85.1`, que desde a 0.i fixavam o molde do
`SendoffSpring` (cortado do escopo e portanto nunca convertido), foram embora com
os outros 22 casos de mapa cortado. A bomba plantada em 0.i saiu do mapa.

---
## 0.k A DEX COMPLETA NAS CINCO REGIÕES, 21-22/08/2026 (rodada 3; condutor Opus, executores Opus, fechador Opus)

Build verde. **ROM 98,85% de 32 MB** (+16 KB sobre a 0.j, 375 KB livres), EWRAM
86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 757/758** (só o T11.3
pulado na rodada normal), **T11 3/3** à parte contra a build `cf6786b2ae`
(worktree em `/private/tmp/claude-501/t11-antiga`), **SAVE COMPATIVEL** com
SaveBlock1 em 14.964 de 15.872 B, `valida_rom.py` com os 2.378 mapas declarados
dentro da ROM, `guarda_colisao_vars.py` com as 23 colisões herdadas e **0 novas**,
e os sete `--demo` de gerador tocados (`distribui_dex`, `objetos_galar`,
`cenas_galar`, `fala_galar`, `fila_galar`, `arte_ginasios_sinnoh`,
`lendarios_sinnoh`) verdes. ROM oficial: `roms/pokemon-claude-2026-08-22.gba`
(md5 `3cd78228b0803ff6ef3ed67100c24fb9`), com o `.map` ao lado, e o MESMO binário na ROM de teste de nome
fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | **101,0%** | 100% | 100% | -- | 52 (0) | **290** |
| Johto | 100% | **96,1%** | 100,1% | 96,2% | -- | 55 (3) | **305** |
| Hoenn | 100% | **100,7%** | 100,1% | 100% | -- | 39 (21) | **297** |
| Sinnoh | 95,4% | **82,7%** | 100,7% | 86,3% | -- | 39 (102) | **295** |
| Unova | 99,0% | **102,3%** | 100% | 99,6% | -- | 30 (3) | **315** |
| Galar | 100% | 113,4% | 100% | **43,1%** | **31,7%** | 48 (32) | 0 |

**Dex obtenível: 1.096 → 1.566 de 1.571 (69,8% → 99,7%).** É a obra que a 0.j
deixou planejada, feita em duas ondas.

### O censo, a régua e a pesquisa

O pedido supunha 1.200 a 1.300 entradas. O censo (`dev_scripts/censo_dex.py`,
importável, com `--demo`) mediu **1.571 entradas distintas de `gSpeciesInfo`**:
1.668 ids do enum menos 97 apelidos, 1.025 bases e 546 formas, porque mega,
gmax, regional, padrão de Vivillon, letra de Unown, sabor de Alcremie e prato de
Arceus são entrada própria. **Armadilha de 243 entradas**: o
`catalogo_especies.py` só enxerga `[SPECIES_X] = { ... }`, e dez famílias são
escritas por MACRO; `censo_dex.entradas_macro()` existe só para isso. **Achado
que vale por si: os iniciais de Hoenn não existiam neste jogo**, o
`SPECIES_TREECKO` só aparecia em `debug.inc` e o Birch entregava os de Johto; os
outros buracos de espécie comum são exatamente os exclusivos de versão, porque
quem importou pegou um lado só.

A decisão mora em `dev_scripts/dex_distribuicao.json`, uma linha por entrada
inobtenível; o executor é `dev_scripts/distribui_dex.py` e não decide nada. As
regras que mudam o resultado: **nível não se toca** (a linha nova herda o nível
do slot, o estático herda o da fonte); **"slot vazio" tem definição medida**, e
não é slot vazio nenhum, são os **5.622 slots duplicados** (48% dos 11.732) em
que a mesma espécie ocupa duas linhas da MESMA tabela, e a nova entra na segunda
ocorrência, de modo que nenhuma espécie da fonte sai e nenhum mapa nem tabela
nova foi preciso; **gen 1 a 5 vai para a região da geração**, sem exceção, e as
gens 6 a 9 vão por bioma tirado do PERFIL DE TIPOS da própria tabela, com empate
resolvido por cota; **água é água**; **lenda nunca vai para o mato**, é sempre
estático; e **nada de trava de pós-jogo**.

A pesquisa de lendários (`dev_scripts/lendarios_referencia.csv`, 117 linhas) leu
o que vanilla e sete rom hacks (Radical Red, Unbound, Renegade Platinum, Sacred
Gold, Blaze Black 2 Redux, Elite Redux, Liquid Crystal) fizeram com cada lenda
fora da região de origem, e decidiu: **lar canônico quando o mapa existe neste
repo, bioma quando não existe**. N's Castle, Abundant Shrine e Liberty Garden
NÃO existem aqui, e nesses casos vale o vizinho mais próximo. A régua sozinha põe
Xerneas em floresta de Johto, Yveltal em torre de Unova, Zacian e Zamazenta nas
Ruins of Alph, Koraidon e Miraidon no Mt. Coronet e Glastrier na neve de
Snowpoint.

### O que entrou, por caminho

| caminho | linhas | onde |
|---|---:|---|
| mato (slot duplicado) | **233** | Kanto 47, Johto 41, Hoenn 47, Sinnoh 54, Unova 44 |
| estático novo | **106** | Kanto 15, Johto 22, Hoenn 16, Sinnoh 14, Unova 39, em 29 mapas |
| presente por NPC | **22** | 3 iniciais de Hoenn por `dynmultichoice`, 19 sem sprite por `givemon` |
| evolução em cascata | **114** | sai de graça quando a base ou a forma entra |
| `EVO_ITEM` novo | **2** | Karrablast e Shelmet, com `ITEM_LINKING_CORD` (id 796, já existia) |

O motor ganhou 29 linhas em `include/regions.h`: **Johto sai por GRUPO DE MAPA**
(84 a 98) e não por mapsec, porque os 65 apelidos de MAPSEC de Johto são todos
`#define ... MAPSEC_SINNOH_WEST` e nenhuma comparação de `sectionId` separa as
duas; Sinnoh, Unova e Galar saem por faixa de mapsec. **Custo de save zero**: é
leitura de `location.mapGroup`, que o motor já gravava. As 106
`FLAG_HIDE_DEX_*` (0x31A0 a 0x3209) mais duas de presente (0x319E, 0x319F) são
apelido de `FLAG_UNUSED`, então `FLAGS_COUNT` não muda.

**Os 5 que faltam, e por quê**: `DEOXYS_DEFENSE`, `DEOXYS_SPEED`,
`ZYGARDE_10_POWER_CONSTRUCT`, `ZYGARDE_COMPLETE` e `ZYGARDE_MEGA`. Nenhum é
questão de lugar: os cinco dependem de **mecânica de troca de forma** que este
jogo não tem ligada (o meteorito das torres para o Deoxys, as células e o Cube
para o Zygarde). Pôr como estático seria mentir a forma.

### Os seis defeitos de gerador que a onda B achou

Todos vieram de rodar o gerador contra a árvore JÁ MEXIDA, que a onda A nunca
exercitou, e todos são de posicionamento silencioso: nenhum dá erro de compilação.

1. **Estático em cima de objeto que já existia**: a busca ignorava os objetos do
   `lendarios_sinnoh` e três caíram sobre o Shaymin, o Heatran e o Regigigas. A
   marca a ignorar virou parâmetro; as dos outros valem como parede.
2. **Estático em cima da CAMINHADA de um caso gerado** (T123.9, T123.10, T123.13,
   T123.14). Não ilhar tile nenhum não basta: caso de emulador é rota exata.
3. **A mesma coisa com caso escrito À MÃO** (T124.11, T124.13, T124.14, no
   Distortion World): nasceu o `corredor_de_casos`, que relê o roteiro de todo
   caso e refaz a caminhada sobre a grade de colisão.
4. **Estático órfão**: mudar um lendário de mapa deixava o objeto velho no mapa
   velho para sempre (SnowpointTempleB5F guardou um em (5,3)).
5. **Rota atravessando linha de visão de treinador** (MtPyre_Summit, quatorze
   tiles antes do lendário). O raio vai nas QUATRO direções, porque NPC anda.
6. **Parede não segura seta**: a perna de zerar escolheu DOWN sobre um
   `MB_SOUTH_ARROW_WARP` na Viridian Forest, o motor decide o warp ANTES da
   colisão, e o jogador foi parar na guarita, dois mapas adiante.

### A janela de 15 sprites, o defeito que não dá sintoma

`OBJECT_EVENTS_COUNT` é 16 e um slot é sempre o jogador, então sobram **15**.
`TrySpawnObjectEvents` acorda todo template dentro de uma janela em volta do
jogador que, refeita a partir de `MAP_OFFSET` 7, é de **20 por 17 tiles**
(`pos.x - 9 <= tile.x <= pos.x + 10`, `pos.y - 7 <= tile.y <= pos.y + 9`). Do 16º
em diante o motor desiste CALADO: o lendário existe no mapa, tem script, tem
flag, e não aparece. Distância de 5 tiles não basta (4 por 4 de 5 em 5 já são
16), e por isso o gerador tem portão de lotação por janela.

**Folga medida pelo fechador em 22/08, e que não estava escrita**: template de
`OBJ_EVENT_GFX_LIGHT_SPRITE` **não gasta slot de ObjectEvent** (o motor o manda
para `SpawnLightSprite`, no ramo de cima do `if`). O `lotacao()` conta as luzes,
então a régua é PESSIMISTA: no `RuinsOfAlph_Outside`, o mapa no teto (15 numa
janela só, ancorada em (8,8), ou seja jogador em (17,14) ou (17,15)), cinco
daqueles 15 são luz e o motor vê 10. **Não afrouxe a conta sem medir de novo**:
errar para esse lado custa um reposicionamento, para o outro custa um lendário
invisível.

**Os 17 quadros por toque não garantem o passo.** Os 202 casos da onda B usam
`17:` e não `16:` para o aperto não empatar com o passo do jogador, que dura 16
quadros; medido em 22/08 no ginásio de Eterna, uma subida reta de 23 tiles com
`17:UP*25` (24 de folga, contando o toque que só vira o boneco) para em (11,10),
treze tiles antes do alvo, e só fecha com `17:UP*40`. Regra: **perna longa e reta
usa contagem SATURANTE com folga larga**, nunca a exata.

### Eterna e Canalave, e o Galar c4a

A pergunta 14 da 0.j foi respondida com obra: os dois ginásios que o corte não
pegou ganharam tileset secundário próprio (`gTileset_FortreeGym` em Eterna,
`gTileset_Lab` em Canalave) pelo `arte_ginasios_sinnoh.py`, que subiu de 6 para 8
ginásios decorados. **Custo de ROM zero** (tilesets que já existiam) e **colisão
idêntica**, conferida byte a byte. T125 em 12/12.

Em Galar, `dev_scripts/objetos_galar.py` portou **8 cenas de objeto em 6 mapas**
(6 NPCs mudos e 2 placas que não existiam), a custo de 0 var e 0 flag; a fila caiu
de 2.630 para **2.622**. O que muda o plano é o tamanho: das 1.891 linhas de
objeto e placa, **1.398 são de objetos que o G4 não pôs no mapa**, então o teto
real do c4a é **79** e não 1.038. Dentro daquelas 1.398 estão os **859 scripts de
encontro estático de Galar**, insumo de uma Pokédex de Galar futura.
**AVISO GRAVE**: `warp` de script de objeto traduz e a cena roda, mas **não troca
de mapa**; e `warp` seguido de `waitstate` **prende o jogador para sempre**.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

- **T136.1 e T136.2**: os 212 casos das ondas A e B acendem a `FLAG_HIDE_DEX_*`
  na EWRAM e leem o efeito no MESMO boot, o que prova o motor e não prova ONDE a
  flag mora; e a faixa nova (0x31A0) é OUTRA que a do `lendarios_sinnoh.py`
  (0x3220), a única provada em 21/08. Agora o jogo salva pelo menu, recarrega do
  zero e o tile do Ting-Lu continua vazio.
- **T136.3 e T136.4**: o T129.5 lê UMA espécie do time, então o NPC podia
  entregar seis vezes a mesma forma e passar. Agora os SEIS slots são lidos de
  `gPlayerParty` e cobrados contra a ordem dos `givemon` (1020, 1011, 1009, 1016,
  1019, 1014, que não é crescente nem contígua), com o par negativo que faltava.
- **T136.5 e T136.6**: a cena do c4a agora roda inteira depois de salvar e
  recarregar do zero, e o `release` devolve o jogador a (4,7).
- **T136.7 a T136.10**: Eterna e Canalave não tinham caso NENHUM, nem de chegada.
  Agora a Gardenia e o Byron abrem batalha de verdade, com par negativo cada. O de
  Canalave custou sete flags de derrotado, e a razão está medida: os sete
  treinadores do ginásio são `MOVEMENT_TYPE_LOOK_AROUND` e **não existe caminho do
  warp até o Byron sem atravessar linha de visão**.
- **T129.13, fora do emulador**: o mato conferido contra o GIT
  (`git show 0cb8724099:src/data/wild_encounters.json`), tabela a tabela e slot a
  slot. **1.005 tabelas intactas em número e tamanho, 233 slots trocados, ZERO
  espécies perdidas e ZERO níveis alterados.** O T129.2 comparava o arquivo de
  hoje com ele mesmo desfeito pela coluna `substituido`: se a tabela mentisse, os
  dois lados mentiriam junto.
- **T129.14 e T129.15, por sonda**, porque `GetCurrentRegion` não aparece na
  EWRAM e o teto de sprite não tem sintoma: os `_Static_assert` agora afirmam que
  a **Ilex Forest**, onde mora o Okidogi, cairia em `REGION_SINNOH` pelo mapsec e
  só o ramo do GRUPO a devolve como `REGION_JOHTO`, com `IF_REGION` vivo; e o
  `--demo` refaz `TETO_SPRITE` e `JANELA_SPRITE` a partir de
  `OBJECT_EVENTS_COUNT` e de `MAP_OFFSET` em vez de confiar no número escrito à
  mão. Mutação plantada reprovada nos dois.

**A circularidade do `--demo`**: ele reprovava, e não era defeito de dado. O
`corredor_de_casos` lia os arquivos 129 e 131 a 135, que são ESCRITOS a partir da
tabela depois de ela existir; na segunda rodada o `plano()` reservava corredores
que ele mesmo criara e mudava de decisão (Kanto de 15 estáticos para 16, Johto de
22 para 30), e o autoteste comparava a tabela gravada com um plano que nunca
poderia bater. Conserto: **arquivo derivado desta tabela não entra na conta dos
corredores**, e o `--demo` passa a provar a TABELA GRAVADA contra os mapas, com
um plano refeito do zero cobrando espécie para região e mapa, e não tile, porque
Great Tusk e Scream Tail tiveram o tile movido à mão por linha de visão.

### O que fica aberto para o Gui

- **A Dex de Galar**: 859 encontros estáticos da fonte medidos e parados,
  esperando decisão de sprite. Galar hoje tem zero linha de encontro.
- **Zygarde e Deoxys**: os 5 que faltam pedem mecânica de forma, não lugar.
- **Os chefes de equipe vilã** (Rocket, Magma/Aqua, Galáctica, Plasma) seguem
  fora da Fase F.
- **Galar c4b a c4f**, com o teto real medido e o aviso do `warp` escrito.
- **Remoção física dos mapas cortados**: nada foi apagado, e com a ROM em 98,85%
  de 32 MB é a economia mais óbvia que existe.
- Seguem abertos, da 0.j e da 0.i: as três batalhas de Silver e os rivais do BW3G
  a importar, as 19 bolas de neve de Snowpoint, as 31 pedras de Sinnoh, a
  alcançabilidade de `RavagedPath` e de duas salas do Mt. Coronet, e a curva de
  Galar.

**Dívida que continua plantada**: o `T93.6` e o `T85.1` seguem fixando o molde do
`SendoffSpring`, cortado do escopo e portanto nunca convertido.

---

## 0.j ESCOPO DECIDIDO, LENDÁRIOS, DISTORTION WORLD E FASE F DESTRAVADA, 21/08/2026 (rodada 2; condutor Opus, sete executores Opus, fechador Opus)

Build verde. **ROM 98,80% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%, **suíte
524/525** (só o T11.3 pulado na rodada normal), **T11 3/3** à parte contra a
build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`; `vars` em
0x1678 e 8248 flags do lado velho contra 0x18B8 e 12856 do novo), **SAVE
COMPATIVEL**, `valida_rom.py` dizendo que os 2.378 mapas declarados entraram, e
`guarda_colisao_vars.py` com 23 colisões herdadas e **0 novas**. ROM oficial:
`roms/pokemon-claude-2026-08-21b.gba` (md5
`8c01c21bdaad23f79e93f3b70f852471`), com o `.map` ao lado, e o MESMO binário
na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte (mediana, pobres) |
|---|---|---|---|---|---|---|
| Kanto | 100% | 100,1% | 100% | 100% | -- | 52 (0) |
| Johto | 100% | 95,2% | 100,1% | 96,2% | -- | 55 (3) |
| Hoenn | 100% | 100,1% | 100,1% | 100% | -- | 39 (21) |
| Sinnoh | **95,4%** | **82,2%** | **100,7%** | **86,3%** | -- | 39 (**102**) |
| Unova | **99,0%** | 99,5% | **100%** | **99,6%** | -- | 30 (3) |
| Galar | 100% | 113,4% | 100% | 42,1% | 31,3% | 48 (32) |

Kanto, Johto e Hoenn subiram para 100% **no commit `e905a87d3d`, de ontem**, por
conserto de régua e não por obra: quem quiser o antes/depois lê a mensagem dele.
O que esta rodada mexeu é Sinnoh e Unova, e por DUAS causas separadas: os cortes
de escopo (mapas, warps e placas) e obra de verdade (os objetos de Sinnoh saíram
de 81,9% para 82,2% com os 10 lendários, e a arte pobre caiu de 105 para 102 com
os ginásios decorados).

### As decisões do Gui, que é o que esta seção existe para gravar

- **Sai do porte**, em Sinnoh: Battle Zone inteira (três Areas, rotas 225 a 230,
  Stark Mountain, Villa, o Frontier de gen 4 e as cinco instalações), Pokémon
  Mansion e Trophy Garden, Turnback Cave / Sendoff Spring / Spring Path, Great
  Marsh, Amity Square, Pal Park, Underground, GTS, Pokétch Company, 2º andar dos
  Pokécenters, Union Room / Wi-Fi / Record Mixing, elevadores da Liga, mapas de
  Mystery Gift, palco de Contest e o Game Corner de Veilstone. Em Unova: Battle
  Tower do BW3G, Cable Club, caça-níquel de Castelia e o 2F do Pokécenter.
- **Fica**: o **Distortion World** (com gravidade normal), os 8 ginásios de
  Sinnoh, o Bug Contest de Johto, o Snowpoint Temple, o trem-bala de Unova e o
  `Restaurant`, que é o Seven Stars do Valor Lakefront com 9 duplas e não fachada
  de Game Corner como o inventário dizia.
- **Uma battle facility só na ROM**, a de Hoenn, alcançável a pé de Johto.
- **Lendário nunca é cortado**: o lar sai, o Pokémon fica, em lugar fácil.
- **A Fase F foi DESTRAVADA**, com regra própria: times no espírito do Radical Red
  modo insano em líder, rival, Elite Four e campeão; **nível da curva intocado**,
  porque quem rebaixa é o modo lv5; lendário em todo chefe de ace acima de 40;
  Mega e Z à vontade, **pouco Dynamax**, **pouco Tera**.
- **Planejada, executa na próxima onda**: Dex completa nas 5 regiões, censo em
  `scratchpad/dex/`.

A régua é `CORTES_DO_GUI` em `dev_scripts/completude.py` (`--detalhe <região>` diz
o que cada grupo tirou) e a cobrança é o status `cortada` de `fila_b6.json`. Texto
em `PLANO-ESCOPO.md`; se ele e a tabela discordarem, a **tabela** está certa.

### O que cada frente fez

- **F1, régua e fila**: 24 grupos de corte na `completude.py`, em dois modos
  (`mapa_fonte` para o que só a fonte tem, `deficit` para o que existe na ROM e
  ninguém vai terminar), com `--demo` cobrindo alvo inexistente e grupo repetido.
  Fila do B6 de **193 para 165 pendentes**, com **28 cortadas**.
- **F2, lendários de Sinnoh**: **10 encontros estáticos** (Uxie, Azelf e Mesprit
  nas cavernas dos lagos, Rotom no Old Chateau, Regigigas no B5F do Snowpoint
  Temple **sem trava de pós-jogo**, Heatran no `MtCoronet_B1F`, Shaymin em
  Floaroma, Darkrai e Cresselia no porto de Canalave, Arceus no Spear Pillar
  atrás de Dialga **e** Palkia), flags 0x3220-0x322A, apelido de `FLAG_UNUSED`.
- **F3, moldes, Distortion World e portas**: os **4 moldes de portão** do escopo
  viraram mapa (`IronIsland`, `MtCoronetOutsideNorth` e `South`, `Route204North`);
  o **Distortion World** nasceu com UM andar 32x32, o Giratina no fundo e portal
  novo no Spear Pillar; `porta_morta.py` mais um `valida_warp_tile.py` que agora
  olha COLISÃO destravaram **9 portas**.
- **F4, arte de ginásio**: 8 `map.bin` de Sinnoh redesenhados. Conferido pelo
  fechador byte a byte contra o HEAD: **colisão e elevação idênticas nos oito, e
  nenhum tile mudou de comportamento de metatile** (a primeira medição do
  fechador acusou 362 mudanças e estava ERRADA: cortava primário/secundário pelo
  tamanho do arquivo, a quarta armadilha do `valida_warp_tile.py`).
- **F5, Frontier por Johto**: porta em `TrainerHill_Courtyard` (24,29) para o cais
  do `BattleFrontier_OutsideWest` (20,68), volta por seta ao sul, UM metatile
  mudado no cais de Hoenn (2 bytes).
- **F6, cenas de Galar**: 16 cenas de map script e 3 `VAR_GALAR_*`; a fila de lá
  foi de 445 para **461 feitas** (3.195 linhas, 2.630 pendentes).
- **Fase F**: **144 batalhas, 742 Pokémon, 61 lendários distintos, 80 Mega, 9 Z,
  5 Dynamax e 6 Terastal**, escritas em `trainers.party` por gerador idempotente
  que só toca bloco de chefe.

### As premissas que a rodada derrubou

1. **Os 144 map_scripts de Galar NÃO são `ON_FRAME_TABLE`** (a 0.i diz isso e
   está errada). No FireRed, que é a fonte do demake, o tipo **3 é
   `ON_TRANSITION`** e o **2 é `ON_FRAME_TABLE`**: os 144 são bytecode solto, sem
   var e sem valor, e tabela de cena a fonte tem **19, em 17 mapas**. Ainda por
   cima **139 dos 144 não escrevem var nenhuma**, e 77 são só dois `setflag` de
   flags que nenhum script LÊ (0x90E tem 98 `setflag` e zero `checkflag`): quem
   as lia era código C do hack, que aqui não existe.
2. **O Distortion World não tem chão na fonte.** Os dez headers do Platinum
   juntos têm no máximo dez tiles andáveis, porque a geometria mora no modelo 3D
   de gravidade variável. O andar que entrou é **invenção declarada**.
3. **Nenhum lendário de Sinnoh existia na ROM**: zero em `wild_encounters.json`,
   zero batalha estática. Havia o que colocar, não o que realocar, e por isso o
   status `realocar` da fila segue em zero linhas (medido de novo hoje: nenhuma
   linha do B6 casa a tabela `LENDARIO_NO_ID`, porque a fila é de `hidden_flag` e
   de gatilho). O pedido do F2 ao dono da fila era, portanto, **um no-op**, e a
   cobrança da realocação mora no `PLANO-ESCOPO.md`.
4. **Vars de Galar: 3 bastaram, não 200.** A conta de 200 a 260 da 0.i vinha da
   premissa 1; com 19 tabelas na fonte, a fase cabe nos **147 que ainda sobram**.
5. **Porta sólida nunca dispara.** O `valida_warp_tile.py` julgava warp só pelo
   comportamento do metatile e dava por boas portas em tile de colisão 1, onde o
   jogador nunca pisa. Passou a olhar os dois.

### O bug que o caso adversarial achou: o Arceus infinito

O portão do Arceus rodava no `ON_TRANSITION` e, a cada entrada no Spear Pillar,
acendia `FLAG_HIDE_ARCEUS_SINNOH` e a apagava se `FLAG_CAUGHT_DIALGA` e
`FLAG_CAUGHT_PALKIA` estivessem acesas. Só que **capturar o Arceus acende essa
MESMA flag**: quem o pegava (o que exige os dois marcos) e saía da sala tinha a
flag apagada na volta, e o lendário nascia de novo, **quantas vezes quisesse**.
Uma flag não distingue "escondido porque o portão está fechado" de "escondido
porque o bicho já foi". Medido no emulador antes do conserto: (13,15), barrado
pelo Arceus, com a HIDE em 0. O conserto é na raiz, em
`dev_scripts/lendarios_sinnoh.py`: nasceu `FLAG_ARCEUS_SINNOH_RESOLVIDO`
(0x322A, apelido de `FLAG_UNUSED`), acesa na vitória e na captura, e ela é a
PRIMEIRA linha do portão. Caso **T123.25**.

### Os outros casos adversariais (autor de caso ≠ autor de cena)

- **T123.21 e T123.22**: os vinte casos do F2 acendem a HIDE na EWRAM e leem o
  efeito no MESMO boot, o que prova o motor e não prova ONDE a flag mora. Agora o
  jogo salva pelo menu e recarrega do zero, e o tile do Uxie continua vazio.
- **T123.23 e T123.24**: o portão do Arceus com UMA flag só. Com um
  `goto_if_unset` a menos os casos do F2 passariam e o Arceus nasceria só com o
  Dialga; as três combinações que fecham o portão agora estão medidas.
- **T124.19**: entrada e saída do Distortion World eram dois casos de mão única,
  cada um do seu warp de debug. O circuito ida-volta-ida corre numa sequência só.
- **T125.11 e T125.12**: a lição da 0.i aplicada. O T115.3 provava só que o
  jogador CHEGA em (11,3); agora ele aperta A e a batalha da Candice abre, no
  ginásio de gelo, o mais arriscado dos oito.
- **T126.9 e T126.10**: a razão escrita da porta nova é que largar o jogador na
  praça o deixaria sem o Frontier Pass PARA SEMPRE, e ninguém tinha medido que a
  cena do Scott dispara para quem vem de Johto: agora uma corrida só vai do warp
  10 da Route 40 até `FLAG_SYS_FRONTIER_PASS` acesa, e outra faz a volta inteira
  até `MAP_ROUTE40` (11,14). Medido e dito: dali até a Olivine City o caminho
  EXISTE (a varredura de colisão alcança a borda leste em (33,13) a (33,18)), mas
  este harness não o estabilizou, e o caso para no chão de Johto em vez de fingir
  que chega na cidade.
- **T127.9 e T127.10**: o T127.4 recarrega a save mas acorda DENTRO do mapa e
  nunca o recarrega, e é o carregamento que roda a tabela de cenas. Agora o
  jogador salva, o jogo recarrega do zero e ele ENTRA de novo: a cena não repete.
- **T128.5**: com LV.5 ligado os seis níveis viram 5, e a partir daí um time da
  Fase F é indistinguível de qualquer outro; pior, quem carrega o Mega é o ACE,
  que é o ÚLTIMO slot e nunca o ativo, e a Mega é um ITEM. O `gba_runner` ganhou
  `--timeinimigo`, que decifra o substruct 0 de `gParties` como `src/pokemon.c`
  faz, e imprime `especie0..5`, `item0..5` e `tera0..5`. As seis espécies do
  Byron e a `ITEM_HEATRANITE` no ace batem com o `fase_f_chefes.json`.

### O elenco de rival: nada ficou de fora, o buraco é do IMPORT

A tabela da Fase F chama a atenção com **4 batalhas de rival em Johto e ZERO em
Unova**. Medido contra `trainers.party` e `opponents.h`, e não contra a memória
das fontes: existem exatamente **quatro** Silver com time próprio
(`TRAINER_JOHTO_RIVAL_SILVER_1` a `_4`) e **os quatro estão na Fase F**; o HGSS
enfrenta o Silver sete vezes, e as outras três nunca foram importadas. Em Unova,
as 403 constantes de `TRAINER_UNOVA_*` **não têm rival nenhum**: os
`TRAINER_BIANCA`, `TRAINER_HUGH` e `TRAINER_NATE` que existem são NPCs de HOENN
(Route 111, Route 119 e o ginásio de Mossdeep), homônimos. Varredura fechada:
**zero** treinadores com `RIVAL` no nome e time próprio ficaram fora da tabela.
O item de fila é **importar** as três batalhas de Silver e os rivais do BW3G;
dar time a eles é depois, com o mesmo gerador.

### O que fica aberto para o Gui

- **A obra da Dex completa nas 5 regiões**, planejada aqui e por executar.
- **Os chefes de equipe vilã** (Rocket, Magma/Aqua, Galáctica, Plasma) não
  entraram na Fase F, por decisão do condutor; são o próximo alvo natural.
- **O bloco c4 de Galar por padrão**: 2.630 linhas pendentes e vars de sobra.
- **Remoção física dos mapas cortados**: nada foi apagado, e os mapas fora do
  escopo continuam compilando, ocupando ROM e alcançáveis por warp. Com a ROM em
  98,80% de 32 MB é a economia mais óbvia que existe; mexe em `data/`, em
  `map_groups.json` e nos warps de lá, então pede build e suíte.
- **Pergunta 14, ainda de pé**: o `BattleFrontier` de Sinnoh vira a praça do
  Platinum ou fica ligado ao Frontier de Hoenn que já existe? E os ginásios de
  **Eterna** e **Canalave**, cujos moldes o corte não pegou, ficam como estão?
- Seguem abertos, da 0.i: as 19 bolas de neve de Snowpoint, as 31 pedras de
  Sinnoh, a alcançabilidade de `RavagedPath` e de duas salas de Mt. Coronet, e a
  curva de Galar (mediana 70, 276 bichos no nível 100, e o struct de party do
  demake que NÃO é o do FireRed).

**Dívida que continua plantada**: o `T93.6` e o `T85.1` seguem fixando o molde
do `SendoffSpring`, que agora está **cortado do escopo** e portanto nunca será
convertido. A dívida da 0.i virou letra morta em vez de bomba, mas os dois casos
continuam medindo um mapa que o Gui decidiu não terminar; quem apagar os mapas
cortados reescreve os dois.

---

## 0.i CONTEÚDO DE GALAR, MOLDES DE SINNOH E PEDRAS, 21/08/2026 (condutor Opus, três executores Opus, fechador Opus)

Build verde. **ROM 98,69% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%, **suíte
443/444** (só o T11.3 pulado na rodada normal, que é o caso de duas ROMs), **T11
3/3** à parte contra a build do commit `cf6786b2ae` (worktree próprio; `vars` em
0x1678 e 8248 flags do lado velho contra 0x18B8 e 12856 do novo), **SAVE
COMPATIVEL**, `valida_rom.py` dizendo que tudo que foi declarado entrou, e
`valida_mapas_sinnoh.py --so-sinnoh` fechando com `bloqueado: 0`. ROM oficial:
`roms/pokemon-claude-2026-08-21.gba` (md5 `c4452153949d42b8aef2f57a65c7678a`),
com o `.map` ao lado, e o MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | arte (mediana, pobres) |
|---|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100% | 100% | 52 (0) |
| Johto | 95,9% | 95,2% | 100% | 96% | 55 (3) |
| Hoenn | 100% | 100,1% | 100% | 100% | 39 (22) |
| Sinnoh | 80,1% | **75,9%** (era 75,8) | 97,7% | 81,3% | 39 (**105**, era 104) |
| Unova | 94,2% | 99,5% | 99,3% | 98% | 30 (3) |
| Galar | 100% | 26,7% | 100% | 15,4% | 48 (32) |

**A linha de Galar não se mexeu e isso é defeito de régua, não da onda.** O
`completude.py` lê Galar de censos congelados (`galar_gente.json`,
`objetos_gravados: 1204`, `itens_gravados: 33`) e a onda não os regerou. Medido
hoje no `map.json`: **1.260 objetos**, **394 com script** (era 1) e **85 bg
events** (eram 33). Regerar o censo é item de fila; até lá a linha de Galar diz o
mundo de anteontem.

### O que a rodada fez

- **Galar, onda 1 da fase de conteúdo** (`fala_galar.py`, novo): 337 NPCs mudos
  ganharam a fala da fonte, 52 placas passaram a existir (Galar não tinha
  nenhuma) e 56 bolas de item entraram com **flag própria por bola**, em
  0x1C21-0x1C58, todas apelido de `FLAG_UNUSED` e portanto a **custo zero de
  save**. A fila caiu de 3.257 para 3.195 linhas: 445 feitas, 104 descartadas com
  motivo, 2.646 pendentes.
- **Sinnoh, o 13º molde virou mapa** (`converte_moldes_sinnoh.py`, novo): o
  `OreburghGateB1F` deixou de vestir o molde de portão 13x9 e virou a caverna
  64x32 da grade 2D do Platinum, com 2 NPCs e 3 pedras. Os outros 12 seguem
  parados por decisão do Gui, com o `--dry-run` pronto.
- **Sinnoh, as pedras**: o validador passou a julgar por COMPORTAMENTO de
  metatile e por ALCANÇABILIDADE, não por colisão crua, e o seletor de capítulo
  passou a dar `MOVE_ROCK_SMASH` ao Pikachu (uma linha em `chapter_jump.c`, custo
  zero de save), o que destravou a primeira prova de SMASH da suíte.

### As três premissas que a medição derrubou

1. **As 31 pedras de Sinnoh NÃO são dívida da conversão.** A 0.g dizia que "a
   conversão do Platinum marca o tile da pedra como bloqueado". Errado: o nosso
   `map.bin` é **byte a byte** o do demake 2D em `OreburghGate_1F`,
   `MtCoronet_1F_South` e `MtCoronet_B1F`, e em `RavagedPath` difere em UM tile
   do mapa inteiro, a 20 tiles da pedra mais próxima. Quem não desenhou a
   passagem foi a FONTE. 28 das 31 caem em tile com ZERO vizinho alcançável.
   Deslocamento não salva: varrendo (dx,dz) de -20 a 20, o melhor põe 18 das 27
   pedras de RavagedPath em tile andável e casa ZERO warp. Pôr essas pedras é
   DESENHAR corredor, ou seja decisão de fase e não conversão.
2. **Eram 13 mapas de molde, não 12.** Há DOIS moldes no repo,
   `LAYOUT_ROUTE226_ACCESS` e `LAYOUT_ROUTE208_ACCESS`, e `planta_provisoria`
   sempre pegou os dois. Quem enxergava só 12 era a **lista escrita à mão** da
   fila, que escondia o `OreburghGateB1F`. A fila passou a tirar a lista da
   medição.
3. **O pool de flags é 5.711 e não 1.375.** O 1.375 da 0.h era o que o harness
   conseguia NOMEAR, não o que existe. Medido por `flags_livres.py`: **5.711
   livres**, 4.447 numa faixa contígua. Flag não é gargalo nesta fase.

### Vars de Galar: sobram 150, e a saída é uma var por MAPA

Dos 512 endereços 0x4000-0x41FF, 16 são `TEMP_VARS`, 346 têm dono declarado (318
citados de verdade, 28 recuperáveis um a um) e **150 estão livres**
(0x417E-0x41BF, 0x41D6-0x41FF, 0x4107-0x412F, 0x4100). A fase de conteúdo estima
200 a 260, ou seja **déficit de 50 a 110**, e crescer `VARS_COUNT` quebra a save.
**A saída recomendada é uma var por MAPA com o valor codificando a etapa**, que é
o que o FireRed faz com `VAR_MAP_SCENE_*`: cabe folgado, não abre janela de save,
e o preço é não ter duas cenas independentes no mesmo mapa. O bloco c3 (144
linhas de `ON_FRAME_TABLE` puro) é o teste dessa escolha: fazer 12 e MEDIR antes
de comprometer a faixa. **ERRADO, e corrigido na 0.j:** no FireRed o tipo 3 é
`ON_TRANSITION`, não `ON_FRAME_TABLE`; os 144 são bytecode solto, e tabela de
cena a fonte tem 19, em 17 mapas. Por isso 3 vars bastaram, e não 200. Rascunho em `PLANO-CONTEUDO-GALAR.md` (é rascunho de
executor, não decisão).

### O achado da rodada: dois Pokécenters de Sinnoh não curavam

`JubilifeCity_PokemonCenter_1F` e `SandgemTown_PokemonCenter_1F` tinham
enfermeira com sprite, script de cura e movimento certo, e mesmo assim **não
havia de onde falar com ela**. Medido no emulador contra a ROM de 19/08, com par
positivo e negativo: em Jubilife o jogador terminava em (3,4) COM e SEM o A; a
MESMA rota em Oreburgh travava em (7,4) com o A e andava até (5,4) sem ele.

**O conserto que a fila mandava fazer estava errado, e o número mostra por quê.**
Ela pedia `MB_COUNTER` no metatile de balcão, que é o 545 do
`gTileset_PokemonCenter`; ele aparece TRÊS vezes na linha do balcão de TODOS os
20 Pokécenters desse tileset, Hoenn incluída, então dar `MB_COUNTER` a ele
abriria conversa através da parede em 20 mapas para consertar 2. O defeito era a
COORDENADA: varridos os 67 mapas com enfermeira com script, **65 põem a moça em
cima da coluna que tem `MB_COUNTER`** (517 em Hoenn e no resto de Sinnoh, 664 em
Johto e no Mt. Silver, 577 em Unova, 774 no Trainer Hill) e só estes 2 caíam
fora. As duas foram para (7,2). Casos T122.1 a T122.4.

**Lição, de régua e não de mapa: "o NPC está lá" não é "dá para falar com ele".**
Entre o objeto e a conversa há um atributo de metatile, e nenhuma medida de
completude enxerga isso.

### Os casos adversariais (autor de caso ≠ autor de cena)

- **T120.9 e T120.10 (Galar)**: a bola é pega, o jogo SALVA pelo menu e a save é
  recarregada do zero. Os casos que já existiam acendiam a flag à mão na EWRAM, o
  que prova o motor e não prova ONDE a flag mora: se as 56 tivessem caído na
  faixa temporária ou acima de `SPECIAL_FLAGS_START`, todos passariam e o jogador
  ganharia o item de novo a cada boot. Passou: a flag sobrevive.
- **T112.5 (pedras)**: o par NEGATIVO do de cima. O jogador quebra a pedra, sai
  pelo B1F, volta e ela está lá, porque a memória do smash é `FLAG_TEMP_2` e
  `ClearTempFieldEventData` zera a faixa a cada carregamento de mapa. Era o que a
  0.g afirmava sem medir, e é dele que depende o custo zero de save das 478
  pedras.
- **T121.6 (Oreburgh)**: o T121.2 provava que a escada dispara e que o mapa é o
  certo, e parava aí; mapa certo não é tile certo. Agora a chegada é medida:
  subindo pela escada de verdade o jogador para no MESMO (7,5) em que o T112.2
  para saindo do mesmo tile por warp de debug.
- **T121.4 nasceu FLAKY e foi reescrito pelo fechador**: terminava um tile abaixo
  do ciclista `WANDER_AROUND` de (37,12), que o próprio T121.3 já tinha
  descartado como alvo. Três rodadas isoladas: OK, OK, FALHA. A perna final virou
  DOWN, saturando em (50,14), longe de tudo que se mexe. **Mesma família do
  T98.9 e do T108.2.**

### O que fica aberto para o Gui

- **Os 12 mapas de molde de Sinnoh**: a ferramenta não trava mais nada, falta
  gosto. A troca entrega forma honesta e desenho chapado: a arte cai de 46-48
  metatiles distintos para 5-9 e Sinnoh vai de 105 para 116 mapas abaixo do piso.
  O prêmio contado na fonte são 91 objetos e 36 placas, sendo 30 e 20 só no
  `BattleFrontier`. **Pergunta separada: o `BattleFrontier` de Sinnoh vira a
  praça do Platinum (a fonte) ou fica ligado ao Battle Frontier de Hoenn que já
  existe na ROM?**
- **A curva de Galar**: 278 ids de treinador citados pelos scripts, 774 Pokémon,
  **mediana 70 e 276 exatamente no nível 100**. A fonte é pós-jogo, não campanha;
  importada crua, Galar inteira nasce em 100. É a mesma decisão que congelou a
  Fase F. **Aviso: o struct de party do demake NÃO é o do FireRed** (só 165 dos
  741 times passam com o molde do FR); medir o stride antes de acreditar.
- **A Fase F continua congelada** por decisão dele de 19/08 (carta de trabalho na
  0.h). Seguem abertos as 19 bolas de neve de Snowpoint, os 8 ginásios de Sinnoh
  sem arte, as 31 pedras (agora com o motivo certo), a alcançabilidade de
  `RavagedPath` e de duas salas de Mt. Coronet (257, 652 e 153 tiles ilhados) e o
  censo de Galar por regerar.

### Dívida plantada: dois casos fixam um molde que vai morrer

**`T93.6` e `T85.1` VÃO QUEBRAR no dia em que o `SendoffSpring` for convertido, e
quem converter reescreve os dois na MESMA rodada.** O T93.6 prova
`layout: LAYOUT_SENDOFFSPRING`, o molde 13x9, e o id muda com a planta nova; o
T85.1 anda `16:RIGHT*11` dentro de um mapa de 13 colunas para chegar ao
`MAP_TURNBACK_CAVE_ENTRANCE`, e no 64x64 essa rota não chega a lugar nenhum.

**Régua para quem escrever rota**: andabilidade se mede por COLISÃO **e
ELEVAÇÃO** (o lago do `OreburghGateB1F` tem colisão zero e elevação 1); warp só
dispara sobre metatile com comportamento de porta ou escada (a primeira conversão
do B1F nasceu de mão única sobre chão comum); a primeira tecla de uma direção
nova só VIRA o boneco; e **aperto mandado durante a animação de escada é
COMIDO**, então perna logo depois de warp precisa de espera antes.

---

## 0.h ENCERRAMENTO DO PRD-GOAL, 19/08/2026 (condutor Opus, executores Opus)

**O goal `PRD-GOAL.md` está CUMPRIDO no escopo que ele define, com UMA fase
congelada por decisão do Gui.** Handoff da próxima sessão:
`/tmp/handoff-pokemon-claude-2026-08-19.md`; auditoria item a item:
`/tmp/fechamento-prd-2026-08-19.md`.

Build verde, **ROM 98,58%**, EWRAM 86,16%, IWRAM 86,66%. **Suíte 413/414**
(só T11.3 pulado na rodada normal, que é o caso de duas ROMs), **T11 3/3**
à parte, **SAVE COMPATIVEL**, `valida_rom.py` dizendo que tudo que foi
declarado entrou. ROM oficial: `roms/pokemon-claude-2026-08-19b.gba`
(md5 `8f90f12f1279e557dd0f41899fa7d057`), com o `.map` ao lado, e a mesma
build na ROM de teste de nome fixo, também com o `.map` casado.

### Critério do PRD, item a item

| critério | veredito |
|---|---|
| suíte verde completa | **cumprido** (413/414, zero vermelho) |
| T11 3/3 contra a ROM congelada | **cumprido**, com o T11.3 provando a RECUSA da save velha |
| fila sem pendente executável | **cumprido**: de 15 para **0**; os 192 que sobram têm bloqueio medido |
| Galar jogável | **cumprido no escopo da obra** (ver decisão abaixo) |
| ROM oficial + ROM de teste | cumprido, com `.map` ao lado das duas |
| ESTADO com seção de fechamento | esta seção |
| memória apontando o estado final | cumprido |
| handoff de encerramento | cumprido |

### Duas decisões de condução que ficam escritas, para ninguém reabrir

1. **"Galar jogável" vale pelo critério final, não pelo "Pronto quando" da
   Fase E.** O texto da Fase E pedia insígnias e Liga, mas a decisão 1 do
   próprio `PLANO-OBRAS-GALAR.md` mandou cena, treinador e ginásio para uma
   fase de conteúdo separada, e foi assim que a obra rodou. Galar hoje é a
   região inteira andável (149 mapas a pé pelo barco, com volta, provado
   nos casos T108.4 a T108.6), com 26,7% de objeto, zero cena e fila
   própria de 3.257 linhas. **A Liga de Galar é fase futura nomeada**, não
   pendência escondida deste goal.
2. **A Fase F está CONGELADA pelo Gui**, não esquecida: "nao quero mexer em
   times de lideres ainda nem curva de nivel, deixa todos lv 5, pra eu
   poder testar o rom" (19/08/2026). A medição dela foi feita e está na
   carta de trabalho abaixo, para quando ele destravar.

### O que a Fase F mediu antes de congelar (carta de trabalho)

- **7 chefes SEM GIMMICK NENHUM, e isso é defeito, não desenho**: os três
  campeões de Unova (`GENESIS`, `JUNIPER_*`) e os E4 `COLRESS`, `ELESA`,
  `MARSHAL`. Nasceram no B6, depois do B8, e o `gens69_treinadores.py`
  nunca rodou de novo. É o clímax do jogo sem mecânica.
- **26 blocos com Dynamax sem lenda** (eram 22 no B8; Sinnoh e Unova
  ganharam chefes depois). Dar lenda exige trocar o mais fraco do time, o
  que contraria "a fonte entra primeiro": decisão do Gui.
- **Curva: quatro regiões de cinco estão certas.** Johto tem 76 mons acima
  do teto, e **24 deles são a S.S. Aqua** (níveis 120 a 128, teto 100),
  importada depois da rodada de curva e nunca reescalada. O 25º é o RED do
  Mt. Silver, com 149, provavelmente proposital.
- **Os 41 grupos de Pokécenter**: 28 são executáveis (o motor tem
  `ClearDailyFlags`, sobram 52 flags no bloco diário e a faixa de id
  2523-3999 está livre); os 13 do Mart são Mystery Gift, que não existe
  neste motor, e devem sair do escopo.
- **Armadilha para quem executar**: `gens69_treinadores.py --aplicar` NÃO é
  idempotente. Rodar de novo hoje acrescentaria 580 Pokémon e 44 lendas,
  porque ele só olha "tem vaga". Consertar isso é parte do trabalho.

### O que a leva de encerramento consertou

- **Johto parou de mostrar bola de item onde não há bola**: 1171 objetos
  restaurados pelo que a fonte diz (775 Pokémon de overworld, 219 efeitos
  de luz, 49 pedras, 33 canteiros, 13 árvores de Cut). Custo zero de ROM
  nos Pokémon, porque o desenho vem de `gSpeciesInfo`. **61 tiles andáveis
  abriram**: efeito de luz é tratado antes de virar object event.
- **A fila passou a CALCULAR bloqueio** lendo `vars.h` e `flags.h`, em vez
  de confiar no campo escrito à mão. Bloqueio some sozinho quando a var
  nascer.
- Duas armadilhas silenciosas de ferramenta: o validador de Sinnoh
  contava Pokémon de overworld como sprite inexistente e, com
  `--corrigir`, trocaria 781 deles por boneco genérico; e o harness não
  conseguia nomear nenhuma das 1375 flags do pool novo, porque o regex
  exigia hexadecimal maiúsculo.

### O que fica aberto, dito

Fase F inteira (congelada), os 8 ginásios de Sinnoh sem arte (decisão de
desenho do Gui, com amostra pronta em `.../scratchpad/AMOSTRA_oreburgh_4_
caminhos.png`), as 19 bolas de neve de Snowpoint (mecânica), os 12 mapas
de Sinnoh que são molde de portão, as 31 pedras dentro de parede, a fase
de conteúdo de Galar (3.257 linhas) e as gens 6-9 paradas por decisão de
17/08. **ROM em 98,58%, com cerca de 460 KB livres.**

---

## 0.g ONDA DE JANELA ABERTA E A RODADA DE COMPLETUDE, 18-19/08/2026 (condutor Fable até o G5, depois Opus; executores Opus)

Build verde (**ROM 98,58% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%), **suíte 399/400** na hora em que a seção foi escrita (hoje são 414 casos,
413/414; ver 0.h),
**T11 completo 3/3**, e **SAVE COMPATIVEL** depois da regravação da
impressão. ROM oficial: `roms/pokemon-claude-2026-08-19.gba`, com o
`.map` gravado ao lado (faltava, e o T11 precisa dele), e a mesma build na
ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada. Commits: `f23c4e4ab2`, `c68e11fc55`,
`3f922f893d`, `01b1874b83`, `fe8668803c`, `001ea8e056`.

### A JANELA DE SAVE ABRIU E FECHOU DE NOVO. A save antiga NÃO carrega mais

Decisão do Gui em 18/08/2026: pode quebrar a save, porque o Chapter Jump
repõe o progresso em minutos. A onda fez o que a janela fechada proibia e
**a janela está FECHADA outra vez** desde a regravação da impressão.

O pool de flags cresceu (`FLAGS_COUNT` 8248 para 12856, SaveBlock1 em
94,3% com 431 B de folga até o teto de 97%), as item balls de Johto
ganharam flag própria uma a uma, e 19 vars de cena de Kanto saíram de
cima do estado de Hoenn.

**O defeito que o adversarial achou é a lição da rodada: a save velha não
era recusada, era lida errada em silêncio.** O checksum batia por acidente
(o setor é zerado antes de gravar, e os bytes a mais somam zero), então
`GetSaveValidStatus` devolvia OK e o jogo carregava com todas as vars
deslocadas 288 posições, Pokédex embaralhada, creche com Pokémon de
espécie inválida e até 153 item balls nascendo como já pegas. **Carregar
lixo calado é pior do que perder a save.** `SAVE_LAYOUT_REVISION` entrou
na assinatura de setor: o menu agora abre só com NEW GAME (medido em
print, não deduzido), e o T11.3 foi reescrito para provar o comportamento
NOVO, ou seja a recusa.

Três camadas de trava, e a terceira nasceu porque as duas primeiras
dependiam de memória humana: o guarda detecta o deslocamento; a
amarração reprova deslocamento sem subida de revisão; e o `--gravar`, que
era escape hatch mudo, passa a RECUSAR gravação com quebra e revisão
parada (`--forcar` existe e exige decisão escrita).

### Portão de colisão: o que o pré-processador resolve, não o que o texto diz

Ferramenta nova, `dev_scripts/guarda_colisao_vars.py` (faz vars e flags,
`--flags`), lendo o valor que o `cpp` devolve. Achou o que ninguém sabia:

- **38 endereços de var com dois donos vivos**, sendo **19 a doença real**
  (cena de FRLG gravando sobre estado de Hoenn; medido: o `setvar` da
  Pallet Town escrevia em `VAR_LITTLEROOT_TOWN_STATE`). Os 19 foram para
  0x41C3-0x41D5. As outras 19 são utilitárias e ficam declaradas.
- **Duas flags de Johto em 0x4000 e 0x4001**, que são flags especiais do
  motor. Nasceram de um `#ifndef` de import que inventava endereço quando
  não achava o nome. O portão passou a reprovar `#ifndef` nesses headers:
  **mata a classe, não só o caso**.

Calibração medida: em vars, apelido é regra larga; em flags, tem que ser
a forma exata, senão faixa gerada por base mais deslocamento fica
invisível justo para o portão que existe para vigiá-la. E a ordem dos
headers segue a ordem do include, senão o portão grava o corpo de um
arquivo e o valor de outro (foi o falso positivo de 0x20).

### A régua enxerga arte, e Galar entrou na tabela

`completude.py` contava presença e nunca abria o desenho. Era por isso que
Unova aparecia com 94% sendo máscara de colisão em duas cores, e **o erro
só caiu porque o Gui olhou o jogo e desconfiou**. Coluna de arte nova
(mediana de metatile por mapa, piso 10), e Galar como sexta linha, pelos
censos e nunca por nome de grupo.

Dois documentos meus estavam mentindo e foram corrigidos com data: a arte
de Unova já tinha sido feita em 12/08 (mediana 30, não 3; 2 mapas abaixo
do piso, não 155), e a queda de objetos de Sinnoh não era regressão, era
denominador maior mais 270 NPCs inventados apagados de propósito.

### Sinnoh: o buraco era pedra, e a arte de ginásio não existe

- **Completude de objetos de Sinnoh: 60,2% para 75,8%.** Dos 594 objetos
  que faltavam, **447 eram pedra de Rock Smash**, não gente. Entraram 478
  em 28 mapas, **a custo ZERO de save**: o motor pede flag por pedra, mas
  da faixa temporária, então pedra quebrada volta ao sair e entrar, que é
  o comportamento do jogo original.
- **O portão de tranca recusou 14 pedras** que fechavam caminho, provado
  por BFS sem Rock Smash na mochila, nos dois estados. Ele foi consertado
  no meio: a primeira versão reprovava pedra por defeito que já existia
  (seis mapas de Sinnoh nascem com warp fora do alcance a pé, porque a
  fonte pede Surf ou Strength ali).
- **A fonte de Sinnoh não tem arte de ginásio.** O Platinum guarda esses
  mapas como modelo 3D; o 2D carrega só colisão e comportamento, de 2 a 6
  valores. Já emitíamos mais do que a fonte sabe dizer. Conferido na
  segunda fonte: o "Oreburgh Gym" do demake gen 3 é byte a byte o ginásio
  da Roxanne. **A prova pixel a pixel que vale para Unova é indefinida
  para Sinnoh**; a camada certa aqui é o comportamento.
- **`MB_ICE` é atributo, não arte**: 5 metatiles em append (92 B)
  devolveram os 497 tiles de gelo de Snowpoint e as passagens direcionais
  de Oreburgh. Hoenn não mudou um pixel (bytes antigos são prefixo exato
  dos novos).

### Lições novas

- **Com gelo, colisão livre não significa que dá para parar ali.**
  Snowpoint tem 531 tiles andáveis e 84 paradas. Régua de treinador tem
  que separar quem precisa de conversa (parada colada) de quem batalha por
  vista (basta pisar).
- **Em mapa de gelo, os apertos seguintes são comidos enquanto o jogador
  desliza.** Caso de suíte ali precisa de ~240 quadros entre pernas, não
  60.
- **Coordenada errada só aparece quando alguém tropeça.** Os NPCs dos oito
  ginásios de Sinnoh estavam 1 tile abaixo porque ginásio tem UM warp e a
  régua de translação não podia provar nada, então a identidade assumiu,
  cega ao recorte. Não é epidemia: medido nos 353 mapas com NPC
  importado, o desvio é só dos ginásios.
- **Pareamento por nome nosso esconde duplicata**; por evento da FONTE,
  não. Oreburgh tinha a mesma pessoa duas vezes, invisível enquanto as
  duas estavam desalinhadas.
- **`pgrep -f <script>` dentro de um laço que contém esse nome se
  enxerga.** Espera de processo casa por PID guardado. Um `pkill` por
  padrão de texto matou vigias de outra onda nesta rodada.
- **Flaky conhecidos, não regressão**: T98.9 (Unova, VirbankCity) e
  T108.2 (Galar, Circhester06), os dois por NPC que passeia sobre tile de
  gatilho. Rodar isolado 3 vezes antes de acusar.

### O que fica pendente, dito

- **Os 1211 objetos de Johto com sprite de item ball sem serem item
  ball** (a fonte diz efeito de luz, pedra, canteiro, NPC). É o maior
  defeito visível do repo hoje, está na fila com critério de aceite.
- **12 mapas de Sinnoh são o molde de portão 13x9, não mapa** (o Battle
  Frontier é o maior prêmio parado ali: 24 NPCs e 25 placas). Critério de
  detecção é medido, comparação de blockdata contra o molde, nunca nome.
- **31 pedras de Sinnoh caem dentro de parede**, porque a conversão do
  Platinum marca o tile da pedra como bloqueado. Dívida de geometria.
- **As 19 bolas de neve de Snowpoint** com a pergunta de mecânica em
  aberto (empurrável no GBA é bloco de Strength; o Platinum empurra sem
  HM). Enquanto não entrarem, **NÃO realinhar os 3 treinadores** que
  estão 1 tile fora de propósito.
- **Os 8 ginásios de Sinnoh continuam abaixo do piso de arte** e só saem
  de lá inventando desenho, que é decisão do Gui, ainda em aberto.
- `valida_warp_tile.py` não mede Galar (o filtro é por nome de grupo e o
  alocador espalhou 344 dos 438 mapas em grupos alheios).

---

## 0.f FECHAMENTO DA FASE E, GALAR ENTRA COMO SEXTA REGIÃO, 18/08/2026 (condutor Fable até o G5, depois Opus; executores Opus)

Build verde (**ROM 98,55% de 32 MB**, EWRAM 85,94%, IWRAM 86,66%), **suíte
372/373** (só T11.3 pulado, que é o caso de duas ROMs), **T11 completo 3/3 à
parte** contra `roms/pokemon-claude-2026-08-15c.gba`, e **SAVE COMPATIVEL**
(SaveBlock1 em 14388 B de 15872, 90,7%; os 438 mapas de Galar entraram todos
em append). ROM oficial: `roms/pokemon-claude-2026-08-18b.gba`, e a mesma
build sobrescreveu `roms/pokemon-claude-teste-2026-08-16.gba` (md5
`ac8ed5419ab69cacece45ad6479e6063` nas três).

Commits do dia, em ordem: `b61e3fbc12` (G4, gente e itens), `b25f786253`
(miúdas), `4c0368bea0` (Route 222), `3d867acdfc` (arte de Johto),
`2c82216fc0` (pendências de Sinnoh e Johto), `86deaf89c0` (G5),
`ebd8cb29a2` (plano da janela aberta).

### O que Galar é hoje, e o que ela não é

É **geometria inteira e conteúdo nenhum**: 438 mapas com tilesets provados
pixel a pixel, 1.473 warps, 1.203 NPCs mudos, 33 itens escondidos, 12 heal
locations e música traduzida por medição (id da fonte mais 212). Não tem
cena, treinador, encontro, ginásio nem Liga: isso está na fila gerada
`dev_scripts/fila_galar.json`, com **3.257 linhas** chaveadas pela FONTE e
não pelo nosso nome, porque o G3 renomeou 140 mapas.

O Gui entra em Galar pelo barco, em qualquer um dos cinco portos, atrás de
`FLAG_GALAR_QA_ANDAR` (apelido de UNUSED), com marinheiro de volta em
Wedgehurst: **149 mapas a pé, volta de 147**. O Chapter Jump ganhou Galar
como sexta região, e com ela a regra de que heal location zero significa
região sem Liga, senão o seletor ofereceria capítulo que não leva a lugar
nenhum.

### As duas premissas que a medição derrubou nesta fase

1. **Os "455 warps mortos de Galar" não eram herança do desvio MB_NORMAL do
   G1.** São 477 em 211 mapas, e **435 têm comportamento MB_NORMAL na
   própria fonte**: o demake também não dispara. Só 13 vinham do G1. Quem
   deriva "o comportamento certo a partir do contexto" recebe de volta
   `MB_NORMAL`, porque é o que a fonte diz. O resgate que entrou é estreito
   de propósito, aceita só byte baixo que dá PORTA, e ressuscitou 11 warps
   de Circhester. Lição: **hipótese de causa escrita num plano não é
   medição**, e o executor que mede tem o dever de contradizer o plano.
2. **A Route 222 não estava partida onde o plano dizia.** A coluna 91 não é
   a estrada, a entrega em Sunyshore é por warp de portão e sempre
   funcionou. O partido era a entrada norte vinda de Valor, um bolso de 4
   tiles onde elevação 3 contra 4 barrava o passo **sem aparecer na
   colisão**. Três tiles viraram `ELEVATION_TRANSITION`, diff de 3 palavras.

### O defeito de família que apareceu de graça

As 3 placas ilegíveis da Route 222 não eram defeito de mapa: o
`importa_npcs_sinnoh.py` converte coordenada **por escala** da caixa da
matriz do Platinum sobre o nosso layout, e a escala engolia até 4 tiles
onde o layout é redesenho 1 para 1. Duas das três placas não tinham nenhum
tile andável na frente, ou seja o jogador nunca poderia lê-las. O conserto
mora no gerador (`deslocamento_de_warp`, translação provada por dois warps,
mais a lista autorizada `REDESENHO_1PARA1`). **Outros 7 mapas de Sinnoh
seguem na conversão por escala, com 15 placas já gravadas**, e estão na
fila: mover placa já gravada é conteúdo, se mede uma a uma.

### Lições novas, para quem escrever caso ou esperar processo

- **`pgrep -f <nome do script>` dentro de um laço que contém esse nome se
  enxerga.** Um `pkill` disparado por esse padrão matou os vigias de outra
  onda (sem perder dado, porque a suíte dela já tinha terminado). Espera de
  processo casa por **PID guardado**, nunca por padrão de texto.
- **T98.9 (Unova, VirbankCity) é flaky conhecido, não regressão.** O objeto
  12 daquele mapa passeia numa caixa 2x2 que cobre os três tiles de gatilho
  do caso, então a semente do relógio às vezes fecha o caminho. Verde em 4
  de 4 rodadas isoladas. Conserto honesto é pinar RNG ou mexer no NPC, que
  é conteúdo de Unova.
- **O procedimento do T11 ficou mais caro do que estava registrado.** A
  worktree da ROM antiga agora precisa de `make generated` inteiro (não só
  `map_groups.h`: também `layouts.h`, `region_map_sections.h`,
  `heal_locations.h` e os `trainers.h`), com os binários de `tools/` da
  árvore principal copiados para lá.
- **A fala de 5 páginas custou 16 apertos de A, não 11.** Com 11 o `msgbox`
  ficava aberto na última página e o `setvar` nunca rodava: o caso
  reprovava por motivo que não era o gatilho.
- **`OBJECT_EVENTS_COUNT` 16 é teto de objetos SIMULTÂNEOS**, não de
  templates: a save guarda 64. Mapa com 17 objetos não é defeito (o máximo
  simultâneo medido no Lago da Fúria é 6).

### O que fica pendente, dito

- **A janela de save está autorizada a abrir** (decisão do Gui de
  18/08/2026, porque o Chapter Jump repõe o progresso). Nada do que foi
  commitado hoje abriu: a árvore ainda é SAVE COMPATIVEL. A onda tem plano
  próprio, `PLANO-JANELA-ABERTA.md`, e roda antes da Fase F.
- **A faixa de flag de Johto acabou** (192 de 192) e ganhou o transbordo
  `0x1D00`-`0x1D3F`, 62 vagas. **`P_FLAG_FORCE_SHINY` agora aponta para
  `FLAG_TEMP_7`**: acender essa flag em qualquer outro lugar faz todo
  selvagem nascer shiny.
- **`valida_warp_tile.py` não enxerga Galar de verdade**: o filtro é por
  nome de grupo e o alocador espalhou 344 dos 438 mapas em append dentro de
  grupos alheios, então `--regiao Galar` aferiria 283 de 1.473. Não entrou
  em `REGIOES` de propósito (lição 4.3). Quem mede Galar hoje é o censo do
  `mundo_galar`.
- **218 mapas de Galar seguem fora do grafo alcançável** (226 warps sem
  destino representável, 188 apontando para mapa vanilla do FireRed) e
  **4 portas de mão única**, as quatro sujeira da fonte. Estão na fila.
- **ROM em 98,55%, sobram cerca de 470 KB.** A fase de conteúdo de Galar não
  cabe nessa folga sem orçamento. Corte por espaço continua sendo portão da
  condutora com o Gui, nunca decisão de executor.
- Herdadas e sem mexida: mecânica de parceiro (desenho), Amity Square e
  Stark Mountain medidos e parados na fila (a saída da Stark é decisão
  pendente, a fonte não tem porta de volta), corrente da bomba de Pastoria
  nunca jogada de ponta a ponta por humano.

---

## 0.e FECHAMENTO DA OBRA DE SINNOH, 18/08/2026 (condutor Fable, executor Opus)

Build verde (ROM 97,68% de 32 MB, EWRAM 85,94%, IWRAM 86,66%), **suíte
322/323** (só T11.3 pulado, porque ele é o caso de duas ROMs), **T11 completo
3/3 à parte** (a save da `roms/pokemon-claude-2026-08-15c.gba` carrega na build
nova) e **SAVE COMPATIVEL** (a obra não criou item nenhum; SaveBlock1 em
14388 B de 15872, 90,7%). ROM: `roms/pokemon-claude-2026-08-18.gba`, e a mesma
build sobrescreveu `roms/pokemon-claude-teste-2026-08-16.gba` (md5 conferido,
`16426067c02ccb74e51275ad141e021d` nas três).

### O que a obra de Sinnoh foi, do começo ao fim

Cinco ondas mais a leva final, todas desenhadas por `PLANO-OBRAS-SINNOH.md` e
executadas contra `dev_scripts/maquina_sinnoh.json`, o censo que a máquina do
bloco S1 gera:

- **Onda 1 (S1+S2)**: a máquina de vars, flags e gatilhos. 49 alias de var no
  gap `0x4130`-`0x415F` (+`0x41C2`), 157 flags novas em `0x1B00`-`0x1B9C`, e os
  esqueletos de cena plantados nos `scripts.inc`; mais os 8 grupos de
  `hidden_flag` que já estavam sem bloqueio.
- **Onda 2 (S3)**: arco de abertura (Twinleaf, casa do jogador, Verity, Sandgem,
  Route 202).
- **Onda 3 (S4/S5)**: Jubilife/Oreburgh/Eterna e Hearthome/Veilstone/Pastoria.
- **Onda 4 (S6)**: arco da Galáctica, rivais de Pastoria e do portão 209,
  treinadores 2508-2513.
- **Onda 5 (S7)**: pós-liga, Cyrus do 4F (2514) e o fim das cenas por arco.
- **Leva final (S8)**: a bomba de Pastoria inteira, o Croagunk da placa, o rival
  do Pokécenter da Liga (2515-2517), e a FIAÇÃO que sobrou das ondas.

Casos de suíte da obra: **T100 a T104**, e os nove **T104** são desta leva.
Faixa de treinador de Sinnoh: 2500-2517 gastos, 2518-2519 livres.

### A fiação que a leva final fechou, e por que ela existia

Três correntes estavam escritas e **inalcançáveis**, cada uma porque o escritor
da var morava num arquivo que a onda dona da cena não tinha escopo para tocar.
As três foram ligadas aqui, com o desvio da fonte documentado valor a valor:

1. **Partida da corrente de Pastoria.** O único `SetVar VAR_PASTORIA_CITY_STATE,
   1` da fonte inteira mora na cutscene do armazém da Galáctica de Veilstone
   (`scripts_veilstone_city_galactic_warehouse.s:89`), cutscene que esta casa
   descartou ao redesenhar o armazém. O `setvar` entrou no ponto equivalente do
   fluxo NOSSO, colado na mesma fala (`..._Text_WeDidntLearnMuch`), com
   `call_if_eq ... 0` na frente para a corrente nunca ANDAR PARA TRÁS.
2. **Fecho pós-vitória do ginásio de Pastoria.** A fonte escreve 3 no ginásio e
   só chega a 4 na cutscene `PastoriaCity_OnFrame_ExitGym`, que não foi portada.
   O ginásio passou a escrever **4 direto** (o 3 é invisível: nada neste
   repositório o lê), mais os dois `setflag` que a fonte põe na mesma linha
   (esconder o Grunt_M, bloquear o evento do Croagunk).
3. **Atores da cena da bomba.** O S7 escreveu a coreografia supondo um fecho
   pós-ginásio que revelaria Crasher Wake e Rival; esse fecho não existia, e os
   `applymovement` mirariam objetos ausentes. A própria cena passou a revelá-los
   (`clearflag` + `setobjectxyperm` + `setobjectmovementtype` + `addobject`, o
   molde que o `RivalBattle` do mesmo arquivo já usava), nas coordenadas
   convertidas da fonte: Wake em (37,9) e Rival em (34,13). E o fecho ganhou o
   `setflag` que faltava antes do `removeobject` do Wake: sem ele a cutscene
   inteira ficava replayável pelo clique nele.

Entrou também o `ON_TRANSITION` de PastoriaCity, porte do
`PastoriaCity_OnTransition` da fonte. Ele zera `VAR_SINNOH_PASTORIA_CROAGUNK_CENA`
a cada entrada no mapa (sem isso o sorteio de 10% da placa acontece UMA vez na
vida do save, porque a própria cena escreve 1) e reposiciona o rival depois da
explosão (sem isso ele volta ao tile que o `setobjectxyperm` da batalha gravou
no SAVE, do outro lado da cidade).

### As duas ferramentas, consertadas na causa

- **`dev_scripts/maquina_sinnoh.py`**: o `--demo` era vermelho num ponto só, o
  `coord_event` do Buck da Route 227 gravado em (30,19), tile que uma rodada
  ANTERIOR escolheu e que hoje é ruim (o objeto do próprio Buck nasceu em cima
  dele). A realocação só sabia casar pela posição ORIGINAL da fonte, e a posição
  velha não batia com nada. Nasceu `plano_de_reparo`, que também casa por
  SCRIPT o que está gravado e ruim sem explicação, e o manda para o tile que o
  censo de hoje escolheu. Corrigido para (29,19), `--demo` verde, `--gravar`
  idempotente.
- **A idempotência custou uma tabela nova, e ela é a lição.** O primeiro
  `--gravar` verde **ressuscitou 8 `coord_events` que levas anteriores tinham
  APAGADO de propósito**: os três falso-gatilhos da onda 4 (CanalaveCity,
  GalacticHQ_Hall e MtCoronet_1F_South, todos com cena equivalente já existente)
  e o span do Collector do Valor, que a onda 5 escolheu tile a tile no
  `map.bin`. **Gerador que não sabe o que a mão decidiu desfaz a decisão
  calado.** `LEVA_DONA` lista os quatro, com commit e motivo, e a máquina não
  planta, não move e não apaga nenhum deles.
- **E a fila mexeu embaixo da máquina, que é o achado mais perigoso do dia.**
  `maquina_sinnoh.py` escolhia o que portar filtrando `status == "pendente"` no
  `fila_b6.json`, e a alocação de flag saía dessa mesma lista. Quando a fila
  aprendeu `feita`/`descartada`/`adiada`, o conjunto de entrada encolheu de 164
  para 56 e de 247 para 126: um `--gravar` inocente teria **reescrito o bloco de
  flags de Sinnoh com endereços diferentes**, embaixo das dezenas de cenas que
  já citam esses apelidos por nome. Duas travas entraram: a seleção passou a ser
  por REGIÃO e TIPO, sem olhar status (`entradas_da_fila`), e **endereço de flag
  já gravado virou HISTÓRIA** (`alias_ja_gravados` lê o bloco do `flags.h` e
  devolve nome e endereço; alocação nova só existe para nome que nunca saiu, e
  entra em append depois do maior endereço já apelidado da faixa, contando
  também os que a condutora autorizou à mão fora do bloco). Consumo depois
  disso: **158 flags** (as 157 de antes mais
  `FLAG_SINNOH_ESCONDE_VEILSTONE_CITY_GRUNT_M_STORAGE_KEY` em `0x1BA1`, que é a
  calibração do falso "feita" virando endereço reservado para quem escrever a
  cena). Conferido: a ROM recompilada depois dessa linha tem o MESMO md5, porque
  apelido que ninguém cita não muda binário.
- **`dev_scripts/fila_b6.py`**: aprendeu que **esqueleto não é cena**. Gatilho
  cujo rótulo só tem `@ TODO` + `end` deixou de contar como feito
  (`rotulos_com_cena`), e isso desmascarou **38 gatilhos** que a fila dava por
  prontos. E aprendeu as decisões DATADAS da obra: dois status novos,
  `descartada` e `adiada`, com o motivo escrito em cada linha.

### O placar da fila, antes e depois (`python3 dev_scripts/fila_b6.py`)

| tipo | antes: pend. / feitas | depois: pend. / feitas / descart. / adiadas |
|---|---|---|
| sinnoh `coord_event` | 73 / 91 | 56 / 51 / 39 / 18 |
| sinnoh `hidden_flag` | 206 / 70 | 126 / 69 / 35 / 46 |
| **pendentes do B6 inteiro** | **312** | **215** |

O que saiu de "pendente" por DECISÃO, e não por trabalho: os 34 clones (o campo
`hidden_flag` da fonte guardando `MAP_HEADER_*`), os 27 do Amity e os 5 de
mecânica inexistente (decisões 3 e 4), os 41 de Pokécenter/Mart (decisão 6), os
17 de acompanhante (decisão 5), os visitantes da Villa, e Amity e Stark exterior
como **descartados-por-mapa-provisório**. Mais três calibrações registradas: o
grunt da Storage Key de Veilstone, que era falso "feita"; os trainers do
`MtCoronet1FTunnelRoom`, que moram DE PROPÓSITO em outros mapas; e os
`coord_events` decorativos dos portões de molde 13x9.

### As lições de harness, consolidadas

Valem para quem escrever caso novo. Todas medidas, nenhuma deduzida:

1. **N+1 apertos por perna.** O runner segura o botão 6 quadros, e isso só VIRA
   o jogador quando a direção é nova e ele está parado: perna de N tiles em
   direção nova custa N+1 apertos.
2. **Depois de uma perna que SATURA contra parede, a direção nova não custa o
   aperto de virar.** Medido nesta leva, com traço de EWRAM: um `RIGHT` de dois
   apertos contado como um tile andou DOIS e pôs o caso na coluna errada. As
   duas regras juntas são o motivo de a régua boa ser "não conte tile".
3. **~2 apertos de A por página de `msgbox`.** Espera é de graça, aperto de A
   não é: A que sobra pode escolher coisa em menu.
4. **Porta de casa só desce**, e **porta é WARP mesmo com colisão 1**: subir
   para dentro dela tira o jogador do mapa. Foi assim que o par negativo da
   bomba terminou dentro do portão do observatório enquanto o positivo passava
   (a cena trancava o jogador antes de ele chegar na porta).
5. **Tapete de saída é seta sul**: precisa de pausa e de um aperto a mais.
6. **Elevação barra sem aparecer na colisão** (`IsElevationMismatchAt`); o bit
   de colisão do `map.bin` não mostra isso.
7. **Colisão não barra warp de seta**: a borda de conexão atravessa.
8. **Rota se mede no `map.bin`, e se confere no traço de EWRAM.** Sempre que
   der, use perna que SATURA: perna saturada não tem ambiguidade de um tile. Se
   nenhuma perna saturar no eixo que interessa, faça a rota SERPENTINA entre
   duas paredes, e **deixe o gatilho no MEIO da perna, não na ponta** (o
   `coord_event` dispara ao ENTRAR no tile).

### O que fica pendente, dito

- **Mecânica de parceiro que anda junto** (decisão 5): as 6 vars dos cinco stat
  trainers e do rival esperam desenho de mecânica.
- ~~**`MAP_ROUTE222` está partida no meio**: nenhuma entrada do lado de Valor
  alcança a borda de Sunyshore. Pendência de MAPA, não de cena.~~
  **RESOLVIDA EM 18/08/2026, e o diagnóstico acima estava mirando a costura
  errada.** A coluna x=91 nunca foi a estrada: a Route 222 entrega em Sunyshore
  por WARP, pelo portão `(89,23)` -> `Route222_Access` -> `(11,5)` ->
  `SunyshoreCity (4,48)`, e a coluna x=0 de `SunyshoreCity` é água ou parede em
  todas as linhas, então abrir a borda direita não levaria a lugar nenhum. O
  que estava partido era a ENTRADA NORTE de Valor, e era pior: com a estrada
  sul trancada de propósito pelo Collector (sem escritor para
  `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE` neste porte), a norte era a única, e
  ela caía num bolso de 4 tiles, `(0,3)` a `(3,3)`, porque a linha 3 estava em
  elevação 3 com a região grande em elevação 4 logo abaixo (lição 6 desta
  mesma seção: elevação barra sem aparecer na colisão). Sunyshore era
  inalcançável a pé vindo de Valor. Conserto em
  `dev_scripts/conserta_route222.py` (3 tiles viram `ELEVATION_TRANSITION`,
  metatile e colisão intactos, arquivo do mesmo tamanho), prova em **T107.1**
  (`dev_scripts/testes_criticos/107_pendencias.json`), que fica vermelho se os
  três tiles voltarem para elevação 3. Detalhe medido em
  `PLANO-OBRAS-SINNOH.md`, seção "CORREÇÃO DE ROUTE 222, 18/08/2026".
- **Amity Square e Stark Mountain exterior são provisórios**: as cenas existem e
  estão corretas, e voltam a existir quando os mapas reais do Platinum forem
  importados. **Medidos em 18/08/2026 e PARADOS por decisão da condutora**: vão
  para a fila de conteúdo, não para uma onda. Os dois são viáveis sem tileset
  nem tile novo (Amity 64x64 com matriz própria e coordenadas de evento já
  locais; Stark 32x32 com offset exato de (736,224)), e a Stark tem uma decisão
  pendente da condutora com o Gui antes de qualquer execução: a fonte não tem
  porta de volta para a Route 227, então ou se inventa a saída ou o mapa vira
  de mão única. Números, custos e a armadilha inteira em
  `PLANO-OBRAS-SINNOH.md`, seção "AMITY SQUARE E STARK MOUNTAIN OUTSIDE".
- **Visitantes da Villa**: a máquina de `VAR_RESORT_VILLA_VISITOR` não existe
  neste motor.
- **Pokécenter/Mart** (41 grupos): batalha diária e Mystery Gift, polimento de
  fim de projeto.
- **Biblioteca de Canalave**: continua sem escopo escrito (herdado do ESTADO 0).
- **Dialga/Palkia do Spear Pillar** e o clímax da explosão dos lagos: fora desta
  obra.
- **`Route210_North`**: mapa não importado.
- Da própria corrente de Pastoria: o valor 6, que a fonte põe em
  `scripts_valor_lakefront.s:364`, continua sem escritor aqui, de propósito.

---

## 0.d CONSOLIDAÇÃO DE 17/08/2026 (condutor Fable, executor Opus)

Build verde (ROM 97,60% de 32 MB, EWRAM 85,94%, IWRAM 86,66%), **suíte 255/256**
(só T11.3 pulado) mais os **2 casos novos T99** no mesmo binário, **T11 completo
3/3 à parte** (a save da 2026-08-15c carrega) e **SAVE COMPATIVEL** com a
impressão regravada por causa dos itens 877 a 879 (append puro, nada movido).
ROM: `roms/pokemon-claude-2026-08-17.gba`, e a mesma build sobrescreveu
`roms/pokemon-claude-teste-2026-08-16.gba`.

O que entrou: consertos de removeobject em quatro mapas de Unova (ON_LOAD roda
antes de os objetos nascerem; virou ON_TRANSITION com FLAG_UNOVA_CENA_JUNIPER,
contrato agora com oito mapas); validador de IS_FRLG de Sinnoh; modo de teste
com seis opções no menu de opções; itens INFINITE_CANDY, INFINITE_REPEL e
CHAPTER_JUMP; o seletor de capítulo, que substitui a introdução do professor
no jogo novo (nome RED, rival GREEN, masculino); e as 426 flags de Kanto que
valiam o literal 0 ganhando número (a cadeia Bill, S.S. Ticket e policial de
Cerulean religada; 178 item balls de Kanto com flag real).

**Dois defeitos reais achados pela consolidação, os dois medidos no emulador:**

1. **O seletor de capítulo travava o jogo, sempre.** `waitstate` depois de
   `dynmultistack` para o contexto uma SEGUNDA vez (o próprio comando já chama
   `ScriptContext_Stop`), e quem religa é a tarefa do menu, que já religou.
   New Game abria o seletor, o menu fechava na escolha e o jogador ficava sem
   andar, sem menu e sem R+START. Regra que fica: **`dynmultistack` NÃO leva
   `waitstate` atrás**; o modelo certo é `data/scripts/travessia_regioes.inc`.
2. **AUTO RUN muda a gramática de andar.** Correndo, mudar de direção LOGO
   DEPOIS de um passo gasta um aperto só para virar, e parado não gasta.
   Medido nas duas ROMs com o mesmo roteiro (T80.1): na build de 15/08 o
   `16:RIGHT` depois de dois `16:UP` anda; com AUTO RUN ligado ele só vira.
   Reprovou 15 casos de percurso. AUTO RUN passou a nascer DESLIGADO em
   `src/new_game.c`; a opção continua no menu, a um toque. TURBO A/B ficou
   ligado (dispara com 20 quadros de botão segurado, o gba_runner segura 6).

**Abertura da suíte remedida** (`ABERTURA` em `dev_scripts/testa_critico.py`):
4 A exatos até NEW GAME, esperas generosas, `20:DOWN*5` até START FROM
BEGINNING e 2 B de rede; caiu de ~10.700 para ~2.100 quadros. Regra nova:
**espera é de graça, aperto de A não é**, porque depois que o seletor abre
dois A escolhem região e capítulo e o caso acorda em outra região. A abertura
velha virou `intro_carvalho`, escolhida por `--abertura`, e é ela que o T11.1
usa contra a ROM antiga (que ainda tem a intro do Carvalho). Quatro roteiros
do quarto até a rua foram remedidos no framebuffer (o jogo novo nasce em
(6,6) no quarto; a porta do 1F em (4,8) só dispara descendo).

Casos novos: **T99.1 e T99.2** (`99_chapter_jump.json`), com par negativo,
provando o seletor por fato de memória (Planalto Índigo com as oito insígnias
acesas; Pallet Town com as oito apagadas).

Riscos abertos: LV.5 TRAINERS, batalha opcional e animação pós-KO sem prova
direta de suíte (nenhum caso joga batalha até o fim); T90.5 segue calibrado
sobre o defeito conhecido do Kiyo; a impressão do guarda usa espaço de índice
próprio em `dados/items` (itens novos aparecem como 920-922 lá; o id real é
877-879), anotado para não assustar auditoria futura.

## 0.c RODADA 3 DE 15/08/2026: AS DUAS OBRAS DE UNOVA (Fable condutor)

Build verde, **suíte 255/256** (T11.3 pulado na rodada normal) e **T11 completo
3/3 à parte** (save da 2026-08-15b carrega). ROM a 97,64% (+43 KB, na conta do
desenho). SAVE COMPATIVEL direto (zero item/contador novo nesta rodada).

**Obra 2 (changeblock) COMPLETA**: os 12 mapas de planta dupla de Unova
funcionam (7 de troca de nível, 3 de pedra de Strength, 2 de interruptor).
Pedra cai em buraco de verdade (MB_MT_PYRE_HOLE por atributo de metatile
exclusivo, censo-trava em `pedra_buraco_unova.py`; motor:
`HandleBoulderFallThroughHole` roda o coord_event do tile). Elevador do
Virbank Complex RELIGADO (warps em append, nada renumerado). O B2F dos 4
interruptores virou renderizador de estado provado nas 16 combinações
(`prova_b2f_interruptores.py`). Armadilha registrada: a marca `agua` do
gerador é relativa ao map.bin, então o caminho de VOLTA também precisa de
`setmetatileinrange` com elevação explícita (12 quadrantes na Victory Road
incluem 4 de borda que a marca não pega).

**Obra 1 (setscene) COMPLETA**: 71 gatilhos + 59 cenas nos 23 mapas (A2
gerador, A4 sem batalha, A5 arco INFER com 19 batalhas ids 2148-2168, A6
abertura/portões). Ramo por starter é INVERTIDO de propósito (o rótulo da
fonte nomeia o Pokémon DELA). Dois setmapscene remotos por setvar. NPCs de
cena escondidos por FLAG_TEMP_11/12 recalculadas no ON_TRANSITION (zero bit
de save; contrato documentado nos arquivos). Abertura da casa da mãe
protegida (barco desembarca em VIRBANK, casa fica em HUMILAU; cena roda uma
vez e nunca prende). PLANO-OBRAS-UNOVA.md agora carrega a tabela de
conversão e a decisão 7 (relógio do gen 2 descartado).

**Fila recalibrada: 444 pendentes** (era 633): Unova 29, Sinnoh 411, Johto 4.
Três consertos de régua: asserts de invariante (nunca fotografia), regra
"flag citada inexistente = bloqueado" (FightArea voltou a bloqueado), e
identidade por flag dispensa raio de posição (Sinnoh 84 objetos casados).

**Casos novos: 19 (T98.1-19, `98_unova_obras.json`)**, todos verdes, com o
par negativo onde a prova positiva passaria com o mundo quebrado. Limite de
harness documentado: nenhum caso joga batalha até o fim, então consequência
pós-vitória (ex.: var remota do porão de Nimbasa) fica sem prova direta.

Pendências vivas: cena do MARLON em Undella (priorityjump, fora do gerador
de gatilhos; chip de task criado); LIFT_KEY não portada (ninguém a entrega
em Unova; elevador ficou destrancado de propósito); Rt23East Lower/Upper
são changeblock FORA da fila dos 12 (stub documentado); os 29 pendentes de
Unova são portáveis-com-bloqueio residual + 2 changeblock + 2 batalhas + 1
setscene, ver fila_b6.json.

## 0.b RODADA 2 DE 15/08/2026 (Fable condutor, agentes executores)

Build verde, **suíte 236/237** (T11.3 pulado na rodada normal) e **T11 completo
3/3 rodado à parte** (save da ROM 2026-08-15 carrega na build nova, que criou
itens). ROM a 97,51%. **Impressão de save REGRAVADA** (`guarda_save.py
--gravar`): a varredura antiga contava 8 constantes que nunca foram item de
save (`ITEM_USE_*`, `ITEM_FIELD_ARROW`); a corrigida prova zero item real
movido e os 2 sinos no FIM. Regra: item novo é append no fim, e a impressão
se rebendiz depois, com a leitura de fantasma zero conferida.

O que entrou: **Johto leva 2** (ITEM_CLEAR_BELL 875 e ITEM_TIDAL_BELL 876;
arco dos sinos completo: Baoba na Route 39 com escolha GOLD/SILVER, cameo do
rival, 5 Kimono no teatro ids 2464-2466/2468-2469, Ho-Oh e Lugia nível 100;
RED no Mt. Silver id 2467 com OBJ_EVENT_GFX_RED_2 e palette própria 0x1134,
decisão 3; Lugia pousa na BEIRA (29,15) porque a metade norte da câmara é
água legítima da fonte); **Sinnoh leva 3** (9 grupos de hidden_flag da rota
principal: Spear Pillar, Mt. Coronet, Eterna 4F, Veilstone, QG 1F, Lago Valor,
Floaroma, Route 205; 1 flag nova FLAG_SINNOH_LAGO_VALOR_ESVAZIADO, 4
reusadas); **fundação de Unova** (PLANO-OBRAS-UNOVA.md com as 6 decisões de
15/08; 27 vars e 41 flags aliasadas; dev_scripts/changeblock_gen2.py com
--demo que reconstrói 39 mapas byte a byte e os 5 números do desenho
fechando exatos; macro changeblock_gen2 em asm/macros/event.inc); **17 casos
de teste novos** (T90.14, T91.7-11, T97.1-11). Consertos de raspão: cena do
KIYO batalhava o Kiyo VANILLA (regressão de gerador, consertada NO GERADOR;
já era a 2ª vez que um conserto manual era comido por --aplica); queda de
rótulo com portão novo no porta_cenas_johto.py.

Gasto da rodada: 2 itens, 5 flags (4 Johto + 1 Sinnoh), 3 vars de Johto,
27 vars e 41 flags de Unova (fundação, ainda sem consumidor), 6 ids.

Próximo da fila de Unova: executores B3/B4 (changeblock dos 12 mapas, a
ferramenta está pronta) e A2-A6 (setscene; A3 treinadores agora está livre
porque Johto devolveu opponents.h/trainers.party).

## 0.a LEVA DE 15/08/2026 (Fable condutor, agentes executores)

Build verde, **suíte 219/220** (só T11.3 pulado na rodada normal) e **T11
completo rodado à parte: 3/3, a save da ROM 2026-08-12b carrega na ROM nova**
(worktree do commit antigo + `--rom2`; os headers gerados do worktree vieram
copiados da árvore principal porque nenhum mapa novo entrou). ROM entregue:
`pokemon-claude-2026-08-15.gba` no workspace, 97,48% de 32 MB.

O que entrou: **B10/overworld** (220,8 KB de volta; 152 sprites `.smol`;
estouro de VRAM no Battle Dome achado por prova de emulador e desfeito ali;
ferramenta `comprime_overworld.py`); **B6 Johto** (duelos GIOVANNI e
EUSINE/SUICUNE, 4º duelo do rival no subterrâneo, choro da WHITNEY com a
insígnia via BRIDGET, raio de visão devolvido a 17 treinadores de torre/farol
que já existiam com ids 1340-1357; o "grunt do subterrâneo" da fila era
fantasma; OLIVINE adiada de propósito, gatilho da fonte inalcançável);
**B6 Sinnoh** (21 objetos em 2 levas nos mapas da Galáctica + LakeVerity +
FightArea conferido; os 20 grunts do Hall somem com FLAG_GALACTICA_QG_TOMADO
na queda do Saturn); **casos T90.8-13** (autor ≠ executor da cena); fila
`fila_b6.json` calibrada três vezes (conteúdo em vez de proxy, raio 4,
fallthrough). Gasto de recursos da leva inteira: 3 flags, 2 vars, 2 ids.

Pendências novas ou vivas: decisão do Gui sobre o sprite do RED_2 (duelo do
Mt. Silver); arco dos sinos bloqueado por ITEM_TIDAL_BELL/ITEM_CLEAR_BELL
inexistentes (criar item no fim da lista não quebra save, mas ninguém criou
ainda); as duas obras grandes de Unova (máquina de setscene, 59 cenas;
tradutor de changeblock, 108 cenas) precisam de desenho antes de executor;
B10 restante (ícones ~673 KB, indireção de treinador ~485 KB, ambos pedem
mudança de engine); `porta_ginasios_johto.py` continua com a landmine de
reescrever map.json inteiro (rodar `porta_cenas_johto.py --pokemon --aplica`
depois dele); os itens de FightArea na fila são falso "sem bloqueio" (flag
inexistente, corrigir na próxima regeneração).

## 0. PASSAGEM DE BASTÃO da sessão de 12/08/2026 (Fable condutor)

### Conserto da noite de 12/08: NPCs verdes de Kanto (palettes FRLG nunca registradas)

O Gui jogou a ROM de entrega e viu os NPCs do laboratório do Oak com as cores
estragadas (verdes). O defeito existia desde pelo menos 05/08 e passou por toda
a suíte porque a suíte só lia EWRAM. Causa: quando os gráficos FRLG foram
destravados para a build Emerald (guardas `#if IS_FRLG` removidas de
`object_event_graphics.h` e `object_event_graphics_info.h`), a TERCEIRA guarda
ficou: a tabela `sObjectEventSpritePalettes` em `src/event_object_movement.c`.
Os tags 0x1129 a 0x1133 (NPC_BLUE/PINK/GREEN/WHITE, METEORITE, SS_ANNE,
SEAGALLOP e os dois do player FRLG) existiam na ROM mas nunca eram registrados;
`LoadObjectEventPalette` devolvia 0xFF e o sprite desenhava com a palette de
outro dono. Conserto: guarda removida com o mesmo comentário `(antes: ...)` dos
outros dois arquivos. Lição: destravou gráfico condicionado, procure TODAS as
ocorrências da condição, `grep -rn IS_FRLG src/ include/`.

Para essa classe nunca mais passar: o `gba_runner` ganhou `--palobj 0xXXXX`
(diz se a cor de 15 bits está na PLTT OBJ, 0x05000200-0x050003FF, fato de
memória e não pixel), o `testa_critico.py` ganhou a prova `palobj_presentes`,
e o caso novo `T96.1` (`16_kanto_palettes.json`) warpa ao laboratório e cobra
uma cor de `npc_white.pal` e uma de `npc_green.pal`. Calibrado nos dois lados:
FALHA na ROM de entrega de 12/08 (0x0227 ausente; 0x32B9 sozinho não
discrimina, coincide com palette já carregada) e OK na build consertada.
`guarda_save.py` depois do conserto: SAVE COMPATIVEL, 1939 mapas, SaveBlock1
14388 B.

**Efeito colateral esperado: o T93.3 quebrou, e foi reescrito.** O roteiro
antigo entrava pela porta da entrada e decorava o caminho de UMA sala sorteada
(a 81); o sorteio (`random` do motor de script) muda com qualquer mudança de
consumo de RNG da build, e o conserto das palettes mudou. O caso novo parte da
SALA DO PILAR por warp de debug (determinístico), margeia a parede pela linha
y=2 e coluna x=3 (livres em todas as plantas, conferido em `mapas-png`) e sai
pela porta oeste (2,11); a prova continua sendo o contador somando na sala
seguinte. Regra que fica: **roteiro de suíte não pode decorar resultado de
sorteio.**

**RISCO FECHADO em 15/08/2026, medido nas duas ROMs: não existe regressão.**
Entrar numa sala do Turnback por porta custa 58 quadros de input travado em
`0e4571bfd5` E em `25f3976336` (N=3 cada, variância zero, lido de
`sLockFieldControls` na EWRAM); porta não animada de Unova, 60 nas duas. O
">480 engolidos" era o jogador contra a parede: todo warp dinâmico chega em
(11,1), a coluna x=11 é bloqueada em y=8 nas plantas PILLAR_ROOM e ROOM_5 e
livre em ROOM_1/ROOM_3, e a sala é sorteada com semente de relógio
(`SeedRngAndSetTrainerId`, `src/main.c:215`, timers de hardware amostrados na
confirmação do nome). Regra que fica: caso de suíte que entra por porta no
Turnback PINA o sorteio com `"vars": {"0x41C0": 3}` ou `{"0x41C1": 29}`, como
T93.4/T93.5. Colaterais registrados: as "portas" do Turnback são metatile de
comportamento 97 (`MB_LADDER`), não 96 (`MB_NON_ANIMATED_DOOR`), então a
guarda de `Task_ExitNonAnimDoor` é inerte lá; e
`testa_critico.offsets_da_fonte()` grava `probe.c/probe.o` em caminho cravado
(`/tmp/claude-501/frenteA/offsets`), colisão esperando duas sessões paralelas.

### B8 FEITO em 12/08/2026, DEPOIS da janela de save fechar (leia isto primeiro)

A janela de save estava FECHADA quando este bloco rodou, e ele terminou com
`guarda_save.py` dizendo **SAVE COMPATIVEL**. Nada aqui mexeu em `FLAGS_COUNT`,
`VARS_COUNT`, `MAX_TRAINERS_COUNT`, tamanho de struct ou id de mapa; as duas
flags que a mecânica nova consome saíram do pool de `FLAG_UNUSED` que já existe.

| medida | antes | depois |
|---|---|---|
| ROM | 98,07% de 32 MB | **98,14%** (+23 KB, 601 KB livres) |
| EWRAM / IWRAM | 85,94% / 86,65% | **85,94% / 86,65%** (iguais) |
| SaveBlock1 | 14388 B | **14388 B** (igual) |
| mediana do selvagem, K/J/H/S/U | 25 / 20 / 27 / 27 / 30 | **20 / 65 / 122 / 166 / 217** |
| espécies de gen 6-9 no jogo | **0** | **365 de 365** |
| espécies-base alcançáveis | 745 | **927 de 1010** |

**O teto de 255 é viável, e a auditoria achou TRÊS defeitos reais que ele mesmo
criou** (detalhe e prova em `PRD-ROM-COMPLETA.md`, bloco B8): `u8 nextLevel` que
virava 0 e gravava **nível 0** no Pokémon do teto (`src/pokemon.c`); `s16
moveDamage` que enrolava para negativo acima de 32767 e **curava o alvo**
(`include/battle.h`), porque o termo de nível do dano sai de 42 para 104; e três
leituras `gExperienceTables[...][level + 1]` fora do array. **Nível não está em
save**: `struct BoxPokemon` não tem campo de nível, ele é derivado de
`experience:26` (folga de 21% no nível 255) e o `u8 level` de `struct Pokemon` é
cache, com 255 sendo exatamente o máximo do tipo.

**Defeito de flag que estava escondido há tempo**: `B_FLAG_DYNAMAX_BATTLE` e
`B_FLAG_TERA_ORB_CHARGED` apontavam para `FLAG_UNUSED_0x020` e `0x021`, que
neste repo são **apelido de `FLAG_HIDE_ARTICUNO` e `FLAG_HIDE_BILL_CLEFAIRY`**.
Começar o jogo escondia os dois NPCs de Kanto, e entrar nos mapas deles
desligava as duas mecânicas para sempre. Lição: **antes de usar qualquer
`FLAG_UNUSED_*` que o upstream sugere, rode `dev_scripts/flags_livres.py`**:
ele já separava "definidas" de "realmente livres" e as duas estavam na coluna
das 359 OCUPADAS.

### Build de fechamento de 12/08/2026: VERDE, suíte 210/211, ROM a 98,07%

A sessão de fechamento pegou a build verde de 197/211 e foi atrás dos 13
vermelhos. **Nenhum deles era falha de roteiro sozinha e nenhum era o que o
relatório anterior dizia que era**; os três defeitos abaixo estão medidos no
emulador, com a coordenada lida da EWRAM, e consertados.

| medida | valor |
|---|---|
| ROM | **98,07% de 32 MB** (32.136,4 KB mapeados de 32.768; **631 KB livres**) |
| EWRAM / IWRAM | 85,94% / 86,65% |
| SaveBlock1 | 14388 de 15872 B (**90,7%**) |
| mapas na ROM | 1939 |

Toolchain `~/toolchains/arm-gnu-toolchain-15.2*` passada em `DEVKITARM=`; o gcc
do brew continua sem buildar.

**ROM de entrega**: `roms/pokemon-claude-2026-08-12.gba`, com o `.map` do linker
ao lado (é dele que o `testa_critico.py` tira os símbolos). **A janela de save
foi FECHADA**: `guarda_save.py --gravar` rodou sobre essa ROM depois de a suíte
fechar, e antes disso a rodada sem `--gravar` acusou exatamente as 3 quebras
esperadas e nenhuma a mais (vars `0x40FF`→`0x41FF`, SaveBlock1 13432→14388 B,
impressão anterior aos macros).

### Defeito 1: a porta de Unova, e o que ela era DE VERDADE

**A causa registrada pelas duas sessões anteriores estava errada nas duas
direções, e as duas erravam por um.** O relatório disse
`MB_NON_ANIMATED_DOOR` com o número `0x5F`; a conferência do condutor corrigiu o
número para `0x60` e trocou o nome para `MB_LADDER`. Neste repo,
**`0x60` é `MB_NON_ANIMATED_DOOR`** e `MB_LADDER` é `0x61` (o próprio
`valida_warp_tile.py` já avisava disso no comentário da tabela `NOME`). Ou seja:
o nome do primeiro relatório estava certo, o número do segundo estava certo, e
a conclusão dos dois estava errada. **A varredura de 1060 warps de Unova é
`MB_NON_ANIMATED_DOOR` em 1000 e `MB_LADDER` em 60**, e não o contrário.

**Medição no emulador, T20.4, `Unova_NuvemaLab` (12x12, warps em (2,11) e
(3,11), última linha):** o jogador entra, e a EWRAM mostra ele em **(2,12)**,
fora da grade. Ali ele não anda para lado nenhum; o primeiro UP o devolve a
(2,11), que é a própria porta, e o warp dispara de novo: **ele é cuspido para a
rua toda vez que tenta entrar.** O motor separa isso exatamente onde a história
do empurrão precisava: `SetUpWarpExitTask` (`src/field_screen_effect.c`) manda
`MB_NON_ANIMATED_DOOR` para `Task_ExitNonAnimDoor`, que dá um passo para o sul
com **movimento segurado**, que ignora colisão e limite de mapa.

**Conserto, no motor e não no dado** (`src/field_screen_effect.c`): a porta não
animada só usa a saída com empurrão quando o tile de baixo dá para pisar. Fora
da grade o bloco vale `MAPGRID_UNDEFINED` e `MapGridGetCollisionAt` devolve
verdadeiro, então o mesmo teste cobre os dois casos. Varredura do repo inteiro
antes de escrever: **265 warps em 137 mapas** caíam fora da grade e outros
**187** caíam dentro de parede, todos de Unova menos 9 interiores de Sinnoh;
os **1106** warps sadios têm colisão 0 embaixo, então a guarda é inerte para
tudo que já funcionava. Isso é o oposto de reconverter 57 tilesets, que era o
conserto proposto.

**Um pedaço do defeito é de DADO mesmo, e esse foi cirúrgico.** Porta não
animada dispara ao ser PISADA, então quando ela é a única ligação entre a sala
de chegada e o resto do mapa, atravessá-la é sair do prédio. Foi o que o T92.6
provou na `Unova_PkmnLeagueMain`: (13,19) e (14,19) são o único caminho entre a
sala de chegada e o salão da Elite, e **depois de ganhar a Liga o salão ficava
inalcançável**, porque a cena de entrada que carrega o jogador para dentro é
pulada quando `FLAG_UNOVA_LIGA_VENCIDA` está acesa. Os dois metatiles viraram
`MB_SOUTH_ARROW_WARP` (`dev_scripts/porta_de_saida_unova.py`), e o
`applymovement` da cena caiu de seis para cinco passos, porque a seta não
empurra e a partida subiu um tile.

**O tamanho do resto está medido e escrito, para a próxima leva não remedir**
(`porta_de_saida_unova.py --censo`): de 470 metatiles de porta usados por warp
no repo, **196 (558 warps)** têm o tile do norte andável em TODOS os seus usos,
que é a assinatura de "porta por onde se sai andando para o sul" e são
candidatos legítimos a seta sul; os outros **274 (1000 warps)** têm pelo menos
um uso com o norte bloqueado, ou seja são porta de ENTRADA, e seta sul
quebraria a entrada deles. Os dois papéis convivem no MESMO tileset: em
`gTileset_UnovaPkmnLeague`, 683 são as quatro salas da Elite (entrada) e 786/788
são a escada de volta (saída). Virar os 196 de uma vez é trabalho de leva com
rebuild e suíte inteira em cima, não de fechamento.

### Defeito 2: o Lago Acuity não era soft-lock, era um par de mapas ILHADO

O relatório anterior dizia que quem entra pela frente cai na água e alcança 1
tile. A parte da água é verdade; a conclusão não. Medido no disco:
**ninguém chegava lá.** O warp do outro lado, `AcuityLakefront` (32,40), está
sobre `MB_SAND`, e `IsWarpMetatileBehavior` não dispara em areia. A fiação
inteira, antes:

    AcuityLakefront (32,40) MB_SAND         -> LakeAcuity warp 0     MORTO
    AcuityLakefront (32,39) porta           -> LakeAcuityLowWater    vivo
    LakeAcuity      (24,24) MB_POND_WATER   -> AcuityLakefront       MORTO
    LakeAcuity      (23,29) porta           -> AcuityCavern          vivo
    AcuityCavern    (16,21) seta sul        -> LakeAcuity warp 1     vivo

`{LakeAcuity, AcuityCavern}` era uma **ilha do grafo de mapas**, alcançável só
pelo menu de debug, que é o que o T94.5 usa. Conserto em
`dev_scripts/conserta_lago_acuity.py`, copiando o padrão do Lago Verity, que
funciona: (32,40) vira `MB_NORTH_ARROW_WARP` e o `warp 0` do lago sai da água e
vai para (24,31), na plataforma da boca da caverna, com `MB_SOUTH_ARROW_WARP`.
Não é (23,31) porque ali mora o template do RIVAL e em (22,31) o da JUPITER.

**E o conserto acordou um defeito de verdade, que é o melhor argumento de que
ele estava certo.** Com o mapa alcançável, o T94.6 (par negativo) reprovou:
`LakeAcuity_EventScript_Jupiter` só olhava `FLAG_GALACTICA_ACUITY_VISTO` e não
o marco da Mars, então quem chegasse na boca da caverna antes da hora via as
seis caixas de texto **com ninguém na tela** e ainda queimava a flag, trancando
a cena de verdade para sempre. Ganhou um `goto_if_not_defeated` no começo.
Enquanto o warp largava o jogador dentro do lago, esse caso passava por não
conseguir chegar no gatilho: passar por impossibilidade é o mesmo que não ter
teste.

**O que fica aberto no Acuity, de propósito**: a geometria. Medido contra
`fontes-mapas/pokeplatinum/res/field/events/events_lake_acuity.json`, a fonte
entra por quatro tiles no bordo sul, e na nossa conversão a praia sul (42 tiles)
não se liga à plataforma da caverna (25 tiles), porque virou água um caminho que
na fonte é terra. Consertar é reconverter o `blockdata` a partir da grade de
permissão do pokeplatinum. Enquanto isso a entrada cai direto na boca da
caverna: ninguém fica preso, e a cena roda. Efeito colateral aceito e medido:
`LakeAcuityLowWater` perde a única entrada a pé, e aquele mapa tem ZERO objetos,
ZERO coord_events, ZERO bg_events e um `scripts.inc` de duas linhas.

### Defeito 3: onze roteiros escritos contra um mapa que não existia mais

Os casos de Unova foram escritos antes de o B12 trocar os tilesets, quando a
última linha dos interiores era chão comum. Com a porta funcionando, os onze
tiveram que ser re-derivados por busca em largura no `map.bin`. As regras que
saíram disso valem para todo caso novo e **foram medidas, não deduzidas**:

- **O jogador chega VIRADO PARA O SUL** em porta não animada
  (`GetAdjustedInitialDirection`), então a primeira tecla de qualquer outra
  direção só VIRA. Contagem de passo sem contar a virada erra por um.
- **Depois de um warp de PORTA, os primeiros apertos se perdem.** Com 300
  quadros de espera o jogador ficava parado o roteiro inteiro no ginásio de
  Aspertia; com 600 ele anda. Warp do menu de debug não precisa disso.
- **Pausa entre pernas do caminho não é enfeite**: sem `90:NADA` entre elas, os
  apertos da perna seguinte se perdem e o jogador para no meio (T92.6).
- **Caixa de texto aberta come tecla de direção.** O T89.1 ficava parado em
  (13,14) porque a cena de entrada termina com uma mensagem; os A vêm ANTES do
  movimento agora. Isso só apareceu olhando o framebuffer.
- **Número de A é TETO, não piso** (T92.7): com 70 a cena termina na sala do
  Campeão, com 75 o duelo já começa, e com 90 o jogador perde de time vazio e
  acorda em Pallet Town.
- **A prova `andou` precisa de duas posições amostradas DENTRO do mapa final.**
  Cena que move o jogador inteira dentro de um passo do roteiro dá uma amostra
  só, e o caso reprova dizendo que o jogo não respondeu (T92.4).
- **Andar de lado de uma porta para a porta vizinha sai do prédio**, enquanto o
  tile for porta não animada. Todo caminho novo desvia da linha da porta.

### Consertos de integração além dos dois da build

- `2e03d4b561`: o Karate King do Mt. Mortar chamava `TRAINER_KIYO` (181), que é
  o Kiyo da Rota 132 de Hoenn: os dois dividiam a flag de derrotado, e o
  `TRAINER_JOHTO_KIYO` (2461) criado no mesmo dia não era citado por script
  nenhum. Varri a faixa 2460 a 2530: era o único órfão.
- `7593233e5a`: a tabela de treinadores do `testa_critico.py` lia
  `^#define TRAINER_... (\d+)\s*$` e não enxergava as **12** constantes com
  comentário no fim da linha (os quatro duelos do Silver e os oito líderes de
  Unova). O sintoma era o caso reprovar dizendo "treinador da prova não existe",
  que é mentira de validador (lição 4.3).

### Armadilhas de roteiro MEDIDAS (para quem escrever caso novo)

- **Virar custa UM aperto**, e a exceção que estava escrita aqui NÃO EXISTE
  mais. A anotação dizia que virar não custava no primeiro movimento depois do
  warp de debug; medido em 12/08/2026, custa: o jogador chega virado para a
  direção que `GetAdjustedInitialDirection` escolhe pelo comportamento do tile
  (sul em porta não animada, norte em seta sul), e qualquer outra direção gasta
  um aperto para virar. Perna que termina em PAREDE (ou no próprio NPC, que é
  sólido) não depende disso, e continua sendo a forma robusta de escrever.
- `N:BOTAO*K` **anda K tiles**: cada repetição é um aperto separado, com o botão
  solto entre elas. A anotação antiga que dizia o contrário está errada.
- ~~**Warp de debug para interior cuja porta está na última linha não serve**~~:
  serve desde 12/08/2026. O jogador nascia fora da grade porque a porta não
  animada empurrava ele um tile para o sul; a guarda em `SetUpWarpExitTask`
  acabou com isso e ele nasce no próprio tile do warp. Entrar pela cidade, com
  `warp_id` na porta, continua sendo o caminho mais fiel, e cobra ~600 quadros
  de espera antes do primeiro aperto.
- **Cena longa cobra muito mais A do que parece**: o rival de Canalave precisou
  de 10 apertos e a cena do teatro de 20. Seis não bastavam, e o sintoma era
  `oponente=0`, igual ao de roteiro que nem chegou no NPC.
- **Falha que não repete não é defeito**: o T85.3 reprovou na primeira rodada e
  passa sozinho, porque NPC anda por conta própria e pode fechar o corredor.
  Rode o caso duas vezes antes de acusar o jogo.

---

**A sessão de 12/08 executou quase o PRD inteiro por agentes, em 6 commits
(`98685da1d6` a `5127978487`), e PAROU AQUI por crédito. Os números abaixo
desta seção estão VELHOS (são de 11/08); o que vale é isto:**

**FEITO em 12/08** (detalhe em `PRD-ROM-COMPLETA.md`, que registra cada bloco):
B0 inventário; B3 (270 NPCs apagados); B7 (542 mapas com encontro: Kanto
estava 100% fora da build por sufixo `_FireRed`); B4 e B5 nas 5 regiões
(insígnias de Hoenn separadas de Kanto); B12 completo (57 tilesets do BW3G,
mediana de Unova 3→30, animações, ledges com paridade 40/40, +369 KB);
B1 a+b+c (44 mapas, Sinnoh 80,1%, Battle Frontier aberto, Turnback via
MAP_DYNAMIC); B2 (mudos encontráveis 192→63, 21 lojas da fonte, 109 Wi-Fi
escondidos); B6 parcial (espinha da Galáctica de ponta a ponta, Teatro de
Ecruteak, fim de Unova com Juniper campeã, 18 heal locations de Unova).
Infra na janela de save: +2048 flags, +256 vars, teto de treinador 4000,
teto de grupos 128→255, s16 em coordenada de warp.

**NÃO FEITO, na ordem para a próxima sessão:**
1. ~~**BUILD DO CONDUTOR NUNCA RODOU depois da leva.**~~ **FEITO**, e o
   resultado está na seção "Build de 12/08/2026" logo acima: build verde depois
   de dois consertos mecânicos, suíte em 197 de 211, e os 13 vermelhos são os
   três defeitos reais descritos lá (porta de Unova, Liga de Unova, elevação em
   Sinnoh), nenhum deles falha de roteiro.
2. ~~**A JANELA DE SAVE ESTÁ ABERTA E NÃO FOI FECHADA.**~~ **FECHADA** em
   12/08/2026 pela sessão de fechamento: `guarda_save.py --gravar` rodou sobre
   a ROM de entrega depois da suíte, e antes disso a rodada sem `--gravar`
   acusou só as 3 quebras esperadas. A impressão gravada agora inclui o campo
   `macros`, que é o que fechava o buraco de `FLAGS_COUNT`. Save feita nesta
   ROM vale daqui para a frente; save de build anterior a ela não vale.
3. ~~**B8 NÃO COMEÇOU**~~ **B8 FEITO** em 12/08/2026, e o placar está no
   primeiro bloco desta seção. Sobra dele uma decisão do Gui: 22 blocos de
   líder/E4/campeão com time cheio (6 Pokémon) ficaram só com Dynamax e sem
   lenda, e entre eles estão a Cynthia de Sinnoh e os campeões de Unova.
4. **B6 restante, REMEDIDO em 15/08/2026. A fila canônica é
   `dev_scripts/fila_b6.json`, regenerável por `dev_scripts/fila_b6.py`; os
   números antigos desta linha (193/104/348/176) estavam errados e a
   explicação de cada erro está no cabeçalho do script.** São **652 cenas
   pendentes**: Unova 209 (107 de changeblock em **12 mapas**, 1226 chamadas;
   47 setscene; os "16 callasm" são 16 coord_events de UM mapa,
   IcirrusCitySouth, sobre 4 callasm literais; 15 batalhas; 31 portáveis com
   bloqueio; 6 portáveis; 3 special), Sinnoh 430 (276 cenas de hidden_flag
   cobrindo 371 objetos; 164 gatilhos de coord_event, 177 no total; nenhuma
   var do Platinum existe aqui ainda; mais a biblioteca de Canalave, sem
   escopo escrito), Johto 13 (arco dos sinos BLOQUEADO por ITEM_TIDAL_BELL e
   ITEM_CLEAR_BELL inexistentes; 4 duelos de cena; 4º duelo do rival com
   slot pronto; RED_2 esperando decisão de arte do Gui). **Os 18 treinadores
   de torre/farol de Johto estão DESBLOQUEADOS**: a seção 4.1 do
   `PENDENCIAS-JOHTO.md` ficou velha, a faixa 2462-2499 (38 ids) está livre
   e o teto 4000 aguenta sem tocar em save.
5. **B10/corte**: ROM estava a ~97,8% ANTES da leva final de B6; a build
   da próxima sessão diz o número real. Economias mapeadas na seção 11 do
   PRD (ícones 673 KB, indireção de treinador 485 KB, overworld 330 KB).
6. Caso de emulador do guarda da Liga de Hoenn (pendência do B5, opção c).

**Regiões novas (gens 6-9)**: 4 sessões separadas rodando com escopo "tudo"
(dados + demake). Staging em `../fontes-mapas/<gen>/` (que virou repo git
LOCAL, com datamine sem licença: NUNCA ganhar remote público). A integração
ao hack é da sessão condutora, em levas. Teto de grupos já aguenta (255).

**Lições novas de 12/08 (valem regra):** quem escreveu não pode ser quem
confere (escrita silenciosamente falhada só apareceu em grep de processo
separado); agente NUNCA restaura a árvore inteira de snapshot (reverte só os
próprios arquivos; custou reverts de trabalho alheio); faixa exclusiva de
flag/var/id por agente paralelo funciona (0x1840/0x1900/0x1A00, vars 0x41xx,
ids 2460+/2500+/2520+, vagas anotadas em `opponents.h`).

---

## 1. O que o hack é

Cinco regiões num cartucho de GBA, em ordem cronológica:

**Kanto → Johto → Hoenn → Sinnoh → Unova**

Base: `pokeemerald-expansion`. Nada de mapa foi desenhado do zero; tudo veio de
fonte, convertido. As fontes ficam em `../fontes-mapas/`.

| região | fonte |
|---|---|
| Kanto | `pret/pokefirered` |
| Johto | `hns` (hack de pokeemerald) |
| Hoenn | `pret/pokeemerald`, intocado |
| Sinnoh | `fontes-mapas/sinnoh` (geometria), `pokeplatinum` (NPCs) |
| Unova | `AzureKeys/BW3G` (pokecrystal, gen 2) |

---

## 2. Números de agora

| medida | valor |
|---|---|
| ROM | **95,23% de 32 MB** (1,53 MB livres), medido na build de 11/08/2026. Era 94,67% de manhã: cresceu com os 50 itens escondidos, as 9 trocas de Unova, os 790 textos de Sinnoh e os 150 treinadores |
| EWRAM / IWRAM | 85,57% / 86,62% |
| SaveBlock1 | **13432 de 15872 B (84,6%)** |
| flags livres no pool | **40** (medido por `flags_livres.py` em 11/08/2026, depois de a última flag da faixa de itens escondidos ir para o PP UP da Rota 222: estava em 88, 46 foram para os itens escondidos de Sinnoh (`itens_escondidos_sinnoh.py`) e 1 para `FLAG_SINNOH_NPC_DUPLICADO`, que esconde o clone perdedor dos 382 pares de NPC repetido) |
| mapas | **1878** |
| treinadores com time próprio | **2346** |
| grupos de mapa | **126** (teto duro de **128** grupos e **128 mapas por grupo**: `s8` em `struct WarpData`; passar disso mata o mapa) |
| suíte de testes | **162 de 163** em 11/08/2026, rodada em worktree isolada sobre o HEAD mais a leva de tradução dos portos, dos itens escondidos e da escada de MtCoronet2F (eram 161 de 162 antes do caso T88, que prova essa escada). O único pulado é o T11.3, que precisa de duas builds. Uma rodada intermediária desta mesma leva deu **154 de 163, e os 9 reprovados eram exatamente os 9 casos que atravessam porto**: é a lição 4.13, `\l` cobrando aperto de botão que o verificador não contava. Os "2 reprovados de Unova" que esta linha já anunciou foram consertados em `44cae4fa02` uma hora depois de a linha ser escrita, e ninguém a corrigiu por seis dias |
| teto de treinador | `MAX_TRAINERS_COUNT_EMERALD` = **4000**, subido em 12/08/2026 dentro da janela de save aberta daquele dia (era 2500, e este documento chegou a dizer 3000). Maior id declarado: **2440**. Livres: **2441 a 3999, ou seja 1559**. Custou **~486 KB de ROM**, porque `gTrainers` e `sTrainerSlides` sao dimensionados pelo teto e nao pelo uso: ~324 bytes por vaga VAZIA. So da para mexer neste numero com a janela aberta |

### Completude contra a fonte de cada região

100% = tão completo quanto o jogo de onde a região veio. Rode
`python3 dev_scripts/completude.py`.

**Medição de 18/08/2026** (a tabela anterior, de 11/08, está logo abaixo marcada
como SUPERADA; nada foi apagado, porque duas investigações já foram reabertas
por causa de número velho lido como número de hoje):

| região | mapas | objetos | warps | placas | arte |
|---|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% | 52 (0) |
| Johto | 95,9% | 95,2% | 100,0% | 96,0% | 55 (3) |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% | 39 (22) |
| Sinnoh | **80,1%** | **60,2%** | 97,7% | 77,4% | 39 (**104**) |
| Unova | 94,2% | 99,5% | 99,3% | 98,0% | **30** (3) |
| **Galar** | 100,0% | 26,7% | 100,0% | 15,4% | 48 (32) |

A coluna **arte** é nova (18/08/2026) e não é completude contra a fonte: é a
mediana de metatiles distintos por mapa, e entre parênteses quantos mapas ficam
abaixo de 10. Ela existe porque a régua velha deixou uma região inteira passar
por "94% completa" durante seis dias; ver "A régua não enxergava arte" adiante.

| SUPERADA em 18/08/2026, medição de 11/08 | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
| Johto | 95,9% | 94,0% | 100,0% | 96,0% |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
| Sinnoh | 72,7% | 77,2% | 99,2% | 81,2% |
| Unova | 94,2% | 98,5% | 98,9% | 98,0% |

**A linha de Sinnoh mudou muito e NADA disso é regressão.** Mapas subiram de
72,7% para 80,1% porque o bloco B1 pôs 44 mapas de Sinnoh na ROM. Os mesmos 44
mapas derrubaram a coluna de objetos, e é aritmética de denominador: eles
trazem 564 objetos da fonte contra 63 nossos, o que sozinho custa cerca de 12
pontos. A outra metade da queda é deliberada: o B3 apagou 270 NPCs inventados
(censo em `dev_scripts/limpa_clones_sinnoh.py`). Medido no MESMO conjunto de 432
mapas dos dois lados, a queda honesta é de 77,2% para 71,1% (1963 para 1808 de
2542), e o resto é o denominador novo. A obra de 17-18/08 só SUBIU o número
(57,7% para 60,2%), e entre `d9dbdea770` e o HEAD **zero** mapas de Sinnoh
perderam objeto, medido mapa a mapa nos 476 casados. O buraco de verdade são
**1235 objetos que a fonte tem em mapas que entraram vazios** (`BattleFrontier`
0 de 25, `StarkMountainRoom1` 0 de 17, `AmitySquare` 0 de 16, as sete salas de
`TurnbackCave*`, `Route204North`, `MtCoronetOutside*`, `RotomsRoom`,
`LakeVerityLowWater`): eles nunca tiveram gente, não perderam. **Uma frente de
povoamento está mexendo nesses mapas AGORA**, então a coluna de objetos de
Sinnoh vai subir de novo e este número é datado de 18/08/2026. O
`completude.py` foi auditado nesta data e **não** tem defeito de régua aqui.

#### A régua não enxergava arte, e por isso Unova passou seis dias mentindo

`completude.py` contava PRESENÇA de mapa, objeto, warp e placa e **nunca abria o
`blockdata`**, então caixa vazia com as portas e os NPCs certos passava com 98%.
O Gui olhou o jogo e desconfiou em 12/08/2026; a medição deu razão a ele. Desde
18/08/2026 a régua abre o `blockdata`: é a coluna **arte** da tabela acima, e o
conserto de régua é o que faltava para este erro não se repetir em outra região.

Metatiles distintos por mapa, **medição de 18/08/2026**:

| região | mediana | máximo | mapas abaixo de 10 |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Johto | 55 | 437 | 3 |
| Hoenn | 39 | 545 | 22 |
| Sinnoh | 39 | 303 | **104** |
| Unova | **30** | **283** | **3** |
| Galar | 48 | 401 | 32 |

| SUPERADA em 18/08/2026, medição de 12/08 | mediana | máximo | mapas com 3 ou menos |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Hoenn | 39 | 545 | 11 |
| Sinnoh | 39 | 303 | 0 |
| Unova | 3 | 5 | 155 de 291 |

**O parágrafo abaixo é a descrição do defeito, e ele está CONSERTADO. SUPERADO
em 18/08/2026, mantido porque explica a causa:** "Máximo 5 em 291 mapas: Unova é
máscara de colisão em duas cores, chão e parede mais o metatile de porta. E não
tem um tileset próprio sequer: os 291 mapas usam tileset de Hoenn e de Sinnoh
(138 em `Building + GenericBuilding`, 75 exteriores em `GeneralSinnoh +
PetalburgSinnoh`, 32 em `CaveSinnoh`). A conversão leu o `.ablk` certo
(`AspertiaCity.ablk`, 308 bytes = 14x22 blocos de gen 2 = os 28x44 metatiles do
nosso layout) e parou na tradução de bloco para metatile."

**O que Unova é HOJE, medido em 18/08/2026:** 291 mapas, **todos** com tileset
secundário próprio de Unova (46 tilesets do BW3G convertidos, registrados em
`include/tilesets.h` e todos com mapa; os outros 11 do BW3G são de Johto, de
Kanto e das salas de palavra das Ruins of Alph, que nenhum mapa nosso usa). O
primário continua sendo `Building` (184 mapas) ou `GeneralSinnoh` (107), e isso
é **de projeto**: o tileset do BW3G cabe inteiro no slot SECUNDÁRIO do GBA, e
gastar o primário seria pagar duas vezes pelo mesmo desenho. Mediana 30,
máximo 283 (`Unova_VillageBridge`), mínimo 4, **zero** mapas com 3 ou menos. Os
3 mapas abaixo de 10 são **fiéis à fonte**, conferido byte a byte:
`CasteliaPlazaElevator` e `VirbankComplexElevator` (4 metatiles; os dois
compartilham `DeptStoreElevator.ablk`, que tem 4 bytes e 4 blocos distintos) e
`FloccesyRanchBarn` (9; `Route39Barn.ablk`, 16 bytes e 8 blocos). Quem entrou:
o commit **`72820a01db`** (12/08/2026), pelos geradores
`dev_scripts/tileset_gen2.py` (tileset) e `dev_scripts/blockdata_unova.py`
(blockdata), os dois com `--demo` verde em 18/08/2026 e prova de fidelidade
pixel a pixel com mutação plantada. Rodar `blockdata_unova.py --arte-propria`
sem `--gravar` hoje devolve "antes" idêntico a "depois" nas quatro métricas: a
conversão é idempotente e a arte da árvore é a que o gerador produz.

O que **está** pronto em Unova, e é por isso que a região não é lixo: 1396 NPCs,
1060 warps, 497 placas, 6234 linhas de texto de verdade do BW3G, 360 treinadores
únicos todos com time, 87 mapas com encontro selvagem, e as dimensões exatas da
fonte. **Superado em 18/08: a frase "conteúdo cheio com arte zerada, o inverso
de Sinnoh" valeu até 12/08 e hoje está errada.** Unova é a região mais completa
depois de Kanto e Hoenn; o que sobra dela é conteúdo (as 209 cenas da fila
`fila_b6.json` e os 67 NPCs em tile bloqueado, medidos por
`blockdata_unova.py --medir`, item (d)), não arte.

**A coluna de arte já achou serviço nas outras regiões, e isso é o ponto dela:**
Sinnoh tem **104** mapas abaixo de 10, entre eles SETE ginásios (o de Hearthome
com 4 metatiles, e Canalave, Eterna, Pastoria, Snowpoint, Sunyshore e Veilstone
com 5), que são caixa vazia com piso e parede; Galar tem 32, sendo **11 com UM
único metatile** (`Galar_Postwick23`, `Galar_WildArea16` e irmãos). Nenhum dos
dois foi investigado nesta rodada: ficam anotados aqui como fila.

Detalhe de régua, para o número bater quando alguém repetir a medição: a linha de
Sinnoh é medida sobre os 477 mapas de `nossos_mapas_sinnoh()` (a mesma lista que
o resto da linha dela usa), e as outras regiões sobre a lista de grupo. Galar não
tem lista de grupo que preste e sai do censo `galar_mundo.json`; ver o comentário
em `REGIOES` do `completude.py`.

**As placas de Sinnoh caíram de 94,4% para 82,3% em 11/08/2026, e isso NÃO é
regressão.** Medido antes e depois com `completude.py`, na mesma árvore. As 146
bg_events que sumiram nunca foram placa: eram item escondido do Platinum que o
importador copiou como placa (ver o item 3 da seção 8). Cinquenta viraram item
escondido de verdade e 96 foram apagadas. Quem contar placa vai achar que
perdemos conteúdo; o que perdemos foi mentira, e a régua é que continua contando
item escondido da fonte como se fosse placa.

**Sinnoh subiu de 72,4% para 72,7% dos mapas em 11/08/2026 sem um mapa novo, e
isso é régua outra vez.** `importa_npcs_sinnoh.NAO_TOCAR` é uma trava de
ESCRITA ("mapa que outro agente está editando"), e ela estava sendo descontada
dentro de `nossos_mapas_sinnoh()`, que é a régua do `completude.py`:
`CanalaveCity_Gym` e `SandgemTown_House1` estão na ROM e no `map_groups.json` e
mesmo assim contavam como ausentes. É o mesmo defeito de medida que segurava as
seis salas da Elite dos Quatro por causa do nome, e a diferença é que aqui não
era o nome, era a lista de quem não pode ser escrito. As duas coisas foram
separadas: `nossos_mapas_sinnoh()` mede e `mapas_editaveis_sinnoh()` escreve,
e os cinco chamadores foram divididos entre as duas conforme o que cada um faz.
`SandgemTown_House1` ganhou apelido (`MAP_HEADER_SANDGEM_TOWN_HOUSE`) porque o
`1` no fim do nosso nome não casa sozinho, e as duas entradas que só existiam
para tapar o buraco saíram de `fecha_portas_sinnoh.JA_TEMOS`.

**A escada de `MtCoronet2F` em (7,23) apontava para si mesma, e o preço era o
3F inteiro.** Consertado em 11/08/2026. No Platinum ela é metade de um par
(warps 2 e 3 de `mt_coronet_2f`); a conversão trouxe só um lado, e o outro,
(7,12), ficou como chão comum. Medido na grade: as linhas 13 a 22 do mapa são
parede maciça de ponta a ponta, então esse par é o **único** caminho entre a
sala do sul, que vem do 1F, e a metade norte, onde fica a escada para o 3F. Com
o warp morto, `MtCoronet3F` era inalcançável a pé. **Nada foi renumerado**,
porque a save do Gui já está congelada: o degrau que faltava entrou como warp 3,
no FIM da lista, o warp 1 passou a apontar para ele, e o tile (7,12) recebeu a
palavra 0x323F **copiada do próprio (7,23) deste mapa** (metatile 575,
`MB_LADDER`), em cima de chão andável que já existia. Prova no emulador em
`T88.1`, e a contraprova é de graça: o mesmo caso rodado na ROM anterior ao
conserto para em `MAP_MT_CORONET_2F`.

Mudou em 06/08/2026, na sétima leva do dia: **Sinnoh foi de 69,5% para 72,1%
dos mapas**, com 15 mapas novos, e desta vez **nada é régua**: são 12 masmorras
com a geometria CONVERTIDA de verdade e 3 exteriores de planta REAPROVEITADA.
Objetos e placas caíram em porcentagem porque o denominador cresceu: os mapas
novos entram contando os NPCs e as placas que o Platinum tem neles.

A fila de `converte_cavernas_sinnoh.py` dava **zero** e não era falta de
masmorra: Turnback Cave, Iron Island e Stark Mountain já convertiam, e o que
faltava era o mapa **DE FORA** por onde se entra em cada uma, porque o conversor
só cria masmorra que é destino de warp de um mapa que já está na ROM. Exterior
de gen 4 tem cenário DESENHADO que a grade 2D não guarda, e convertê-lo com o
motor de caverna encheria a rua de parede de pedra; então os três exteriores
saíram por `dev_scripts/abre_exteriores_sinnoh.py`, com a planta da antecâmara
`Route226_Access` que o repo já tem (13x9). Cada `map.json` grava isso no campo
`origem`, com a palavra "passagem provisoria".

- **Convertido de verdade (12):** Turnback Cave Entrance; Iron Island 1F, B1F
  Left, B1F Right, B2F Left, B2F Right, B3F, Iron Island Iron Ruins e Iron
  Ruins (o Platinum tem os dois headers, matrizes 283 e 284, e o B3F leva aos
  dois); Stark Mountain Room 1, 2 e 3.
- **Reaproveitado (3):** Sendoff Spring (entra por Route214), Iron Island (por
  CanalaveCity) e Stark Mountain Outside (por Route227). Sem NPC, sem placa e
  sem texto de propósito: coordenada de exterior no Platinum é GLOBAL da matriz
  de Sinnoh e não há offset que alinhe, então NPC importado cairia em qualquer
  lugar dentro de uma sala de 13x9.
- **Régua: nada.** Nenhuma medida mudou nesta leva.

**As 21 salas de pilar da Turnback Cave não vêm, e isso não é defeito de
ferramenta.** Medido na fonte: no Platinum toda sala de pilar aponta só de volta
para a Entrance, e a Entrance aponta para si mesma. Qual sala se entra é
escolhido por SCRIPT, não por warp, então não há warp estático que crie nenhuma
delas. Elas custam o script de sorteio de sala, não conversão de mapa.

**O bug que este bloco quase repetiu, e a prova que o pegou:** a primeira versão
do `abre_exteriores_sinnoh.py` cravou a volta ao mundo em (6,4), que é onde a
`Route226_Access` original tem o warp dela. Medido depois de aplicar: aquele
tile é `MB_NORMAL`, warp MORTO que nunca disparou (a saída de lá é scriptada
pelo marinheiro). Os três exteriores nasceram com entrada boa e **sem saída**,
com validador estático verde: dava para entrar na masmorra e não dava para
voltar ao mundo, que é a lição 4.1 outra vez. Agora a volta sai de
`fecha_portas_sinnoh.portas_livres`, que lê o comportamento do tile no `map.bin`,
e o `--demo` exige duas portas na planta: uma para voltar, pelo menos uma para a
masmorra. Casos `T85.1` a `T85.8` provam no emulador as três idas, duas voltas
de masmorra e as três voltas ao mundo.

Armadilha de roteiro de teste medida aqui: `16:DOWN*3` **não** é o mesmo que
`16:DOWN,16:DOWN,16:DOWN`. O `*N` do `gba_runner` repete os quadros dentro do
mesmo passo, e a seta de warp (`TryArrowWarp`) só dispara com
`input->heldDirection` e o jogador já virado para o lado
(`src/field_control_avatar.c:204`). Roteiro que só soma tecla falha calado.

Nenhuma flag foi gasta (a faixa 0x8EA a 0x8FF continua intacta) e **nenhum grupo
novo foi criado**: seguem 126 dos 128.

Mudou em 06/08/2026, na sexta leva do dia: **Sinnoh foi de 66,7% para 69,5% dos
mapas e a taxa de warp que dispara de verdade foi de 95,8% para 97,0%**, com
oito mapas novos e, de novo, NENHUMA ferramenta nova. Pela terceira leva
seguida, o que travava era **regua errada dentro da ferramenta certa**.

- `converte_cavernas_sinnoh.chao_de_caverna` contava so
  `TILE_BEHAVIOR_CAVE_FLOOR` (0x08). Vizinhos dele no MESMO enum do pokeplatinum
  (`include/constants/field/map_tile_behaviors.h`) sao `OLD_CHATEAU_FLOOR`
  (0x0B) e `MOUNTAIN_FLOOR` (0x0C). Por isso os cinco andares da **Lost Tower da
  Route 209** (84 a 123 tiles de 0x0B cada) e a quinta sala do fundo do **Old
  Chateau** eram reprovados como "nao e caverna de verdade", com a planta
  inteira desenhada na grade do Platinum. O filtro por `mapType` errava dos dois
  lados no mesmo lugar: FLOAROMA_MEADOW esta marcado CAVE e e um prado, a Lost
  Tower esta marcada INDOORS e e masmorra. Quem decide agora e o chao na grade;
  so `MAP_TYPE_OUTDOORS` fica de fora, por decisao. Casa, ginasio de Hearthome,
  Vista Lighthouse, Celestic Cave e a sala de ranking da Jubilife TV continuam
  fora, todos com ZERO chao de masmorra, e sao eles que provam que abrir para
  INDOORS nao abriu a porteira.
- **Achado maior que a propria leva:** o conversor cravava `dest_warp_id` "0" em
  toda escada, porque no laco que escreve o mapa do outro lado ainda nao existe.
  So que o warp 0 de uma masmorra e a SAIDA dela: **descer um andar cuspia o
  jogador para fora do dungeon inteiro**, e eram **69 escadas assim**, incluindo
  a Victory Road de Sinnoh, que jogava o jogador na porta da Liga. Isso passou
  pela leva anterior com validador estatico verde: warp que existe, dispara, e
  leva ao lugar errado (licao 4.1 por inteiro). `casa_voltas()` aponta cada uma
  para o degrau que devolve, e o caso `T84.3` guarda a prova.
- Nove mapas que **ja estavam na ROM** sairam da lista de ausentes so por
  apelido de nome (`importa_npcs_sinnoh.APELIDOS`), entre eles as **seis salas
  da Elite dos Quatro de Sinnoh**, que aqui se chamam `SinnohLeague_*` e la
  `POKEMON_LEAGUE_*`. Isso e correcao de MEDIDA, nao mapa novo, e esta separado
  de proposito: dos 2,8 pontos da leva, 1,5 e regua e 1,3 e mapa.

O que a regua nova alcancou e **nao entrou**: as quatro salas de elevador da
Liga. Abri-las fura a parede das cinco salas da Elite dos Quatro para um quarto
que devolve o jogador de onde ele veio, e a Elite ja se liga sala a sala com o
bloqueio de vitoria. `abre_portas_extras_sinnoh.NAO_FURAR` registra o motivo.

Tres `--demo` guardavam copia de um fato e envelheceram calados, todos
reprovando o proprio conserto da leva anterior (licao 4.11): "CanalaveCity tem 4
predios sem porta" (as quatro portas foram abertas), "os 15 mapas do layout de
centro Pokemon" (sao 14) e "o predio da Galactica divide layout" (foi clonado).
Passaram a testar a forma, nao a contagem. **O portao nao roda `--demo` de
ferramenta**, e foi por isso que os tres ficaram vermelhos sem ninguem ver.

Armadilha de roteiro medida escrevendo o `T84.2`, que contradiz a da leva
anterior e vale mais que ela: **depois de um warp pelo menu de debug o jogador
NAO gasta tecla para virar**, cada toque anda um tile. "Virar custa uma tecla"
vale para quem ja estava andando no mapa.

Mudou em 06/08/2026, na quarta e na quinta leva do dia: **Sinnoh foi de 59,3%
para 66,7% dos mapas e de 96,9% para 99,0% dos warps**, com 44 mapas novos e
NENHUMA ferramenta nova. As duas levas cairam pelo mesmo motivo, e ele nao era
falta de ferramenta: era **regua errada dentro da ferramenta certa**.

- 30 salas de predio (estudios da Jubilife TV, salas dos ginasios de Hearthome e
  de Sunyshore, andares da loja de Veilstone, biblioteca de Canalave 2F e 3F,
  Global Terminal 2F e 3F, elevadores, o restaurante do Lago Valor) eram destino
  de warp de mapa que ja estava na ROM, e `fecha_portas_sinnoh.arquetipo_do_header`
  devolvia `None` para todas elas. So a tabela `NOMEADOS` cresceu, e a cadeia
  inteira veio junto, rodada em laco ate parar de render.
- 14 mapas de geometria CONVERTIDA: a Victory Road de Sinnoh (1F, 2F e B1F) e as
  11 salas sem saida das Solaceon Ruins. A Victory Road ficava de fora so por
  colisao de nome, porque `MAP_VICTORY_ROAD_1F` e `LAYOUT_VICTORY_ROAD_1F` ja sao
  de HOENN; entrou com prefixo de regiao e o par vai em `I.APELIDOS`. As 11 salas
  eram reprovadas por "menos de 30 tiles andaveis nao e caverna", regra que mede
  o TAMANHO da sala: sao camaras de 10 a 13 tiles de verdade. A regra agora conta
  `TILE_BEHAVIOR_CAVE_FLOOR`, e Floaroma Meadow (zero) continua de fora.

Dois warps mortos apareceram no caminho e foram consertados: `fecha_portas_sinnoh`
escrevia direto num grupo que ja estava com os 128 do teto (o mapa 129 nasceria
morto, o defeito que matou 26 mapas), e os dois guardas de insignia da entrada da
Liga estavam parados EXATAMENTE nos dois tiles por onde se entra nas duas portas
do norte, o que deixava a porta do centro Pokemon norte fechada desde sempre.
Prova a pe no emulador em `T80.1` a `T80.5` e `T81.1` a `T81.4`.

Duas armadilhas de roteiro de teste, medidas escrevendo esses casos: **virar
custa uma tecla** (roteiro com a distancia exata erra um tile a cada troca de
direcao) e **porta `MB_ANIMATED_DOOR` so dispara com o jogador vindo de BAIXO**.

**A Elite dos Quatro de Sinnoh e a Cynthia já estavam na ROM** desde `20ac2eaac4`
(04/08/2026), e o que faltava era prova de combate: os casos `T9.9` a `T9.14`
provavam que as sete salas carregam, e nenhum provava que a batalha começa contra
quem devia. Fechado em 06/08/2026 com `T82.1` a `T82.5`, um por membro, todos por
**faixa** de id (1258 a 1262) e nunca pelo nome da constante. Os cinco blocos de
`trainers.party` são times do Platinum, dentro da curva de Sinnoh: Aaron 188-192,
Bertha 188-194, Flint 190-196, Lucian 192-198, Cynthia 196-200. Sprite de
overworld dos cinco é **provisório**, emprestado de classe parecida
(Aaron `BUG_CATCHER`, Bertha `EXPERT_F`, Flint `MANIAC`, Lucian `PSYCHIC_M`,
Cynthia `BEAUTY`); nenhum é sprite próprio de Sinnoh, e todos existem em
`object_event_graphics_info_pointers.h`.

Mudou em 06/08/2026, mais tarde no mesmo dia: **grupo de mapa tem teto de 128**,
e 26 mapas de Sinnoh estavam MORTOS por causa dele. `struct WarpData` guarda
`s8 mapGroup` e `s8 mapNum` (`include/global.h`): o mapa de indice 128 vira -128
no warp e o jogo reseta ao entrar. Medido no emulador, indice a indice. O grupo
de portas foi partido em dois, `fecha_portas_sinnoh.grupo_com_vaga` passa a
escolher o grupo sozinha e `antes_de_empurrar.sh` recusa grupo estourado. **Sobram
2 grupos dos 128**: regiao nova precisa caber neles. Com o teto respeitado
entraram as 36 cavernas com boca desenhada (`abre_bocas_cavernas_sinnoh.py`) e as
11 portas teimosas (`abre_portas_teimosas_sinnoh.py`, com clone de layout onde a
planta e compartilhada), e **Sinnoh foi de 51,0% para 59,3% dos mapas**. Detalhe
nas secoes 11 e 12 de `PENDENCIAS-NPC-SINNOH.md`.

Mudou em 06/08/2026: **Sinnoh saiu de 25,6% para 51,0% dos mapas e de 61,8%
para 95,4% dos warps**, em tres levas. A primeira reaproveitou planta de
interior do repo e fechou 112 portas de cidade; a segunda desenhou a porta que
faltava, copiando a palavra de 16 bits de um warp do proprio mapa, e abriu mais
28 interiores, entre eles os 18 `POKECENTER_B1F`; a terceira converteu a
geometria DE VERDADE de 10 cavernas a partir da grade 2D do Platinum
(`converte_cavernas_sinnoh.py`), incluindo Wayward Cave 1F inteira em 96x64. A
taxa de warp de Sinnoh que dispara de verdade foi de 86,0% para **95,8%**.
Detalhe nas secoes 8, 9 e 10 de `PENDENCIAS-NPC-SINNOH.md`.

Mudou em 05/08/2026, mais tarde no mesmo dia: o **S.S. Aqua entrou na ROM**, os
11 mapas do navio importados do `hns` com texto, NPC e os 23 treinadores de
bordo, e Johto foi de 91,4% para 95,9% de mapas. A travessia Olivine ↔ Vermilion
deixou de ser teleporte e passa **por dentro do navio** nos dois sentidos (T4.2 e
T10.3), com a caminhada e as cabines provadas no T10.4.

Mudou em 05/08/2026: as placas de Johto saíram de 6,8% para 96,0% (448 placas
importadas do `hns` com script e texto), e Unova saiu de 85,4% para 94,2% de
mapas **sem um byte novo**, porque o buraco era o normalizador de nome: no BW3G
a rota é `R5NimbasaGate` e aqui ela entrou como `Rt5NimbasaGate`.

Hoenn dando exatamente 100% é o **controle**: nossa Hoenn é o vanilla intocado,
então tem que dar 100. Se der outra coisa, a ferramenta está errada.

Sinnoh caiu de "100% / fonte 0" para estes números em 05/08/2026, e **isso é
bom**: a régua mudou, não o jogo. Antes era medida contra `fontes-mapas/sinnoh`,
que tem os mapas mas ZERO NPC de Sinnoh. Agora é contra o `pokeplatinum`, que
cobre muito mais mapa do que importamos. Os objetos foram de 528 para **1119**
de verdade; o 25,6% de 05/08 é a medida honesta aparecendo pela primeira vez, e
o 51,0% de hoje é ela subindo com mapa novo, não com régua nova.

### Warps que disparam de verdade

`python3 dev_scripts/valida_warp_tile.py --piso 60`

| Hoenn | Johto | Sinnoh | Unova | Kanto |
|---|---|---|---|---|
| 93,2% | 91,2% | 97,1% | 78,6% | 79,4% |

**Nunca chega a 100%, e não deve.** Warp só dispara se o tile embaixo tiver
comportamento de porta; muita porta é trocada por `setmetatile` em tempo de
execução, e muito warp é usado só por barco ou cutscene. Hoenn é a régua.

Kanto subiu de 69,9% para 79,4% em 05/08/2026 **sem tocar em mapa nenhum**: a
ferramenta é que não conhecia as quatro escadas diagonais (`MB_UP_LEFT_STAIR_WARP`
e irmãs, 235 a 238), que ligam os andares do esconderijo Rocket, do Silph Co e da
Mansão de Cinnabar. Elas não passam por `IsWarpMetatileBehavior`: disparam por
`TryArrowWarp` (`src/field_control_avatar.c:955`). O caso T15.3 prova no emulador
que a escada funciona, então a régua nova é o jogo, não a minha leitura dele.

Os 20,6% que sobram em Kanto **não são defeito, e não devem ser consertados**:
saída de prédio no FireRed tem três tiles de largura, e só o do meio carrega
`MB_SOUTH_ARROW_WARP`; os dois das pontas são entrada de warp redundante em cima
de `MB_NORMAL`. Medido em `PewterCity_Museum_1F` (warps 0, 1 e 2 em (13,9),
(14,9) e (15,9)), em `PowerPlant` e em `PokemonMansion_1F`. Quem "consertar" isso
está mexendo no vanilla.

---

## 3. Decisões já tomadas pelo Gui

Não relitigar. Números são das perguntas numeradas da sessão.

| # | decisão |
|---|---|
| 66 | Começa em **Pallet Town**, ordem cronológica Kanto, Johto, Hoenn, Sinnoh, Unova |
| 67 | **Cynthia fecha Sinnoh, Alder fecha Unova** |
| 68 | **Cada região entrega seu trio de iniciais** ao chegar |
| 69 | **Portar** o texto do BW3G, não escrever enredo novo |
| 70 | **Só creditar** Azure_Keys e os artistas, não contatar |
| 71 | **Nível vai até 255**, não 100. O trabalho de expansão já existia |
| 73 | Importar os treinadores de rota de Johto do `hns` |
| 13 | ~~As 152 "placas" de Sinnoh que na verdade são item escondido **ficam como estão**~~. **Revogada em 11/08/2026 pelo Gui**: as 146 (contagem certa) foram resolvidas. 50 viraram item escondido de verdade, custando 46 flags, e 96 foram apagadas |
| 14 | **Primeiro a ROM na mão do Gui**, ele joga a primeira hora; só depois atacar os 455 mapas de Sinnoh que faltam |
| 2 (15/08/2026) | **Polir times de líder/E4/campeão fica pro FIM do desenvolvimento**, quando todos os assets estiverem validados. Os 22 blocos de time cheio que o B8 deixou sem lenda ficam como estão até lá; nenhuma sessão deve "melhorar" time de líder antes dessa etapa |
| 3 (15/08/2026) | **RED do Mt. Silver REUSA a arte do jogador RED com palette própria** (novo OBJ_EVENT_GFX, sem esperar sprite dedicado). Destrava o duelo RED_2 de Johto |

**A janela de quebrar save FECHOU em 05/08/2026**, com a entrega de
`roms/pokemon-claude-2026-08-05.gba` (commit `d9e5e7581e`). A partir daqui existe
partida do Gui para proteger: mapa novo só no fim do grupo, grupo novo só no fim
de `group_order`, objeto novo só no fim da lista do mapa, flag nova só do pool
que já cabe em `FLAGS_COUNT`, struct de save só recebe append. O `T11.3` foi
provado nessa build: save feita na ROM anterior carrega na recompilada.

**Curva de nível aplicada**, remapeamento linear preservando a forma de cada jogo:

| Kanto | Johto | Hoenn | Sinnoh | Unova |
|---|---|---|---|---|
| 3-50 | 45-100 | 95-150 | 145-200 | 195-255 |

~~**Galar fica fora desta ROM.**~~ **SUPERADO em 18/08/2026**: Galar entrou como
sexta região (seção 0.f), com 438 mapas de geometria e conteúdo nenhum. Ela
ainda **não tem faixa de nível**, porque não tem encontro nem treinador; quando
tiver, a faixa entra nesta tabela. Ver `RECURSOS-REGIOES.md`.

---

## 4. As lições que custaram caro

Todas foram pagas com sessão perdida. Não repetir.

### 4.1 Verificar na camada da afirmação

O fio que liga quase todo bug grave desta sessão. Em cada caso a ferramenta
dizia verde:

- **Kanto tinha 421 mapas no JSON e zero na ROM.** Oito camadas a descartavam em
  silêncio, e a pior gravava `.4byte NULL` na posição do layout, mantendo os
  índices alinhados.
- **Johto tinha 771 warps com índice válido e 12 que disparavam.**
- **Kanto tinha 624 nomes de treinador e 623 sem time**, caindo em cima de
  treinadores de Hoenn. O ginásio de Pewter entregava um montanhista.

"O mapa está no JSON" não é "o mapa está na ROM". "O warp existe" não é "o warp
funciona". "Carrega" não é "funciona".

### 4.2 Ferramenta que discorda do vanilla está errada

Três validadores meus acusaram mapas **originais do Emerald** antes de acertar.
Quando a medida diverge do jogo original, o suspeito é a medida.

### 4.3 Falso positivo é pior que validador nenhum

Portão que não pode ficar verde ensina todo mundo a ignorar a saída. Antes de
pôr regra no portão, meça o vanilla e calibre pelo excesso sobre ele.

Exemplo: a regra "todo warp tem que voltar" acusou 427 casos aqui e o vanilla
tem a mesma taxa (25,3 por 100 mapas contra 26,4). A regra útil é a estreita:
**interior com uma porta só tem que devolver para si mesmo**, que dá zero nos
dois lados e teria pego o bug dos 6 ginásios.

### 4.4 Medir antes de racionar

Eu mandei três frentes racionarem treinador porque "só havia 24 bytes de save".
Medindo o SaveBlock1 campo a campo, `secretBases[20]` ocupava **3200 bytes**
para uma feature de troca por link. Cortada para 4: 2560 bytes, 20.480 flags.

Ainda sobram `berryTrees` (1024 B) e os campos de concurso (736 B).

### 4.5 Constante existir não é o jogo desenhar

Sprite, flag e treinador têm a mesma armadilha: a constante existe, o dado não.

- **Sprite** sem gráfico **reinicia o jogo na tela de título**, sem erro de
  compilação. A lista do que a build desenha sai de
  `object_event_graphics_info_pointers.h`, não de `event_objects.h`.
- **Flag** ocupada continua existindo como `FLAG_UNUSED_0x030`; o que muda é
  alguém apelidar ela. `grep -c FLAG_UNUSED` conta o pool, não o dono. Use
  `dev_scripts/flags_livres.py`.
- **Treinador** sem bloco `=== TRAINER_X ===` cai em cima de quem já ocupa o id.

### 4.6 Prova por identidade não vale quando o apelido devolve a si mesmo

"O oponente é `TRAINER_CAMPER_LIAM`" era verdade com o jogo quebrado. A prova
correta é por **faixa** de id.

### 4.7 Dado corrompido varia, endereço errado não

`mapLayoutId` saindo 26651 **igual em todos** os 41 grupos de Kanto foi a pista
que entregou o caso. Valor absurdo idêntico em todo lugar aponta para busca no
endereço errado, não para dado ruim.

### 4.8 `git add -A` numa árvore com agentes escrevendo captura um instante

Quebrei o `master` duas vezes assim. Buildar antes de commitar não basta: o
build é de outro instante. Rode `dev_scripts/antes_de_empurrar.sh`, que builda o
HEAD numa **worktree isolada**.

A primeira versão desse script usava `git stash`, e **destruiu trabalho de
agente**: o stash de um levou os arquivos de outro.

### 4.9 Substring casa onde você não quer

Comparar `"VENT"` contra o nome inteiro do gráfico casa com
`OBJ_EVENT_GFX_ACE_TRAINER_F`, porque tem *e-VENT-o* dentro. Isso jogou **806
NPCs fora sem erro nenhum**, e só apareceu porque o total deu zero. Tire o
prefixo antes de comparar classe.

### 4.10 Régua tirada da cabeça reprova o jogo original

Levantei que 30 placas em cima de warp eram defeito. Medi: o vanilla tem 2,64%
e nós temos 1,26%, ou seja, **o dobro da nossa taxa**. Se eu tivesse mandado
consertar, teria tirado placa boa. Antes de chamar de bug, meça a fonte.

### 4.11 Teste que guarda cópia de um fato envelhece calado

Três casos desta sessão: teste com número de flag cravado (o número andou quando
o teto de treinador subiu), testador com cópia própria do roteiro de abertura
(o começo mudou de Twinleaf para Pallet), e teste dependendo de NPC que anda.
Leia o fato da fonte; não copie.

### 4.12 Existir não é ser único, e gerador de rótulo tem que ler o arquivo

11/08/2026: o `texto_sinnoh.py` escreveu 790 rótulos e a conferência disse que
todos existiam no `scripts.inc` do próprio mapa. **O assembler reprovou 134
deles em 50 mapas**, porque existência e unicidade são checagens diferentes:
rótulo duplicado existe duas vezes e passa na primeira.

A causa não foi colisão interna. Foi colisão com o que **já estava no arquivo**
de sessões anteriores: o gerador começava com o conjunto `usados` vazio em cada
mapa e renumerava do 1, reescrevendo o `Placa4` que o `texto_placas_sinnoh.py`
tinha escrito antes. Gerador de nome tem que semear `usados` lendo o arquivo.

A checagem certa é na **unidade de montagem**, não por arquivo: os 2018
`scripts.inc` entram num único `data/event_scripts.s`, então o nome precisa ser
único no conjunto inteiro (35.747 rótulos), e a checagem por arquivo deixaria
passar colisão entre mapas. Está em `texto_sinnoh.py --demo`, e ela ignora
`.if/.else` de propósito, senão o vanilla a reprova pelo motivo errado (4.3).

**Landmine registrado:** `fecha_portas_sinnoh.py`, `importa_unova.py` e
`importa_trocas_unova.py` usam o mesmo esquema `<Mapa>_EventScript_Npc<N>` e
**nenhum semeia `usados`**. Hoje não há duplicata, conferida nos 35.747. Quem
rodar um deles num mapa que já tem `Npc1` repete este build quebrado.

### 4.13 `\l` também cobra aperto de botão, e o verificador que só olhou `\p` deu verde

11/08/2026, traduzindo os cinco portos. O número de `A` de 24 roteiros de teste
está embutido no número de páginas de cada caixa, então antes de buildar foi
escrito um verificador que comparava, rótulo a rótulo contra o `HEAD`, quantos
`\p` cada `.string` tinha. Ele deu **zero divergência**, e a suíte reprovou
**9 casos**, todos de barco.

`\l` é `CHAR_PROMPT_SCROLL` e `\p` é `CHAR_PROMPT_CLEAR`. **Os dois são
PROMPT**: param e esperam o jogador apertar A. Só `\n` passa direto. Um texto de
três linhas com `\l` no meio cobra um aperto a mais que o de duas linhas que ele
substituiu, e cada roteiro parou um `A` antes, ainda no porto de origem.

A lição não é "lembre do `\l`". É a 4.4 outra vez, num lugar novo: **o
verificador foi escrito a partir da minha lembrança de como o motor trata `\l`,
em vez de do charmap.** Medir a coisa errada com precisão dá verde, e verde de
verificador quebrado é pior que verificador nenhum (4.3). O que salvou foi a
suíte, e o que fechou o diagnóstico foi o conjunto das falhas ser EXATAMENTE o
conjunto dos casos que atravessam porto, sem um caso de outro assunto sobrando.

---

## 5. Regras de trabalho

- **Nunca escrever mapa, time ou texto do zero quando a fonte tem.** Toda vez
  que alguém escreveu conteúdo nesta sessão, foi o caminho errado.
- **Nunca ler exit code atrás de pipe.** `make -j8 > /tmp/x.log 2>&1; echo $?`.
- **Empurrar só com `antes_de_empurrar.sh` VERDE.** Commitar pode sempre.
- **Agente paralelo recebe faixa de flag e de id exclusiva**, tirada do
  `flags_livres.py`. Já colidiram.
- **Vars são escassas** (30 no jogo inteiro), flags são baratas. Antes de gastar
  var, leia `SINNOH-PADRAO.md`, que tem três técnicas que dispensam.
- Build: `export DEVKITARM="$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi"`.
- Commit como o Gui: `git -c user.name="Guilherme Duarte" -c user.email="gduarte3030@gmail.com" commit`.
  Português acentuado, sem em dash, sem trailer de IA.

### Compatibilidade de save

A save guarda **índices**: `(mapGroup, mapNum)`, índice de objeto, número de
flag. Todo índice é promessa permanente, e não há migração em pokeemerald.

- mapa novo só no **fim** do grupo
- grupo novo só no **fim** de `group_order`
- objeto novo só no **fim** da lista do mapa
- flag nova só do pool que já está dentro de `FLAGS_COUNT`

### Teto de 128, e a política de grupo (decidida em 05/08/2026)

`struct WarpData` guarda `s8 mapGroup` e `s8 mapNum` (`include/global.h:668`).
O mapa de índice **128** de um grupo vira -128 dentro do warp e **o jogo reseta
ao entrar nele**. Medido no emulador índice a índice: 127 entra, 128 derruba. O
mesmo teto vale para a quantidade de grupos. Custou 26 mapas mortos no grupo de
portas de Sinnoh, todos com warp que o validador estático dava por bom.

Estado medido: **126 dos 128 grupos em uso, e 14.302 vagas livres DENTRO dos
grupos existentes.** O que é escasso é grupo, não vaga.

**Política: não criar grupo novo.** Mapa novo entra no fim de um grupo que já
existe e tem vaga (`fecha_portas_sinnoh.grupo_com_vaga` escolhe sozinha). Criar
grupo só com autorização explícita do Gui, porque só restam 2 e não há como
devolver. O `antes_de_empurrar.sh` recusa grupo acima de 128.

`python3 dev_scripts/guarda_save.py` tem que dizer SAVE COMPATIVEL.

**A janela de quebrar save foi REABERTA pelo Gui em 12/08/2026, só para a
revisão deste dia.** Palavra dele: a save atual pode ser descartada; é da
**próxima** save em diante que precisa aguentar edição futura. Enquanto a janela
estiver aberta valem `MAX_TRAINERS_COUNT` maior, `FLAGS_COUNT` maior, mapa
inserido no meio de grupo, objeto no meio de mapa e apagar conteúdo inventado em
vez de escondê-lo atrás de flag.

**Quem fecha a janela é a entrega:** a última ação antes de mandar a ROM nova é
`python3 dev_scripts/guarda_save.py --gravar` sobre ela, congelando a impressão
nova. Da ROM seguinte em diante, tudo abaixo volta a valer como estava.

**Faça o alargamento de teto cedo.** Bloco que descobre tarde que precisa de mais
id não reabre a janela sozinho.

(Ela tinha FECHADO em 05/08/2026, com a decisão 14 da seção 3. Este parágrafo já
disse por seis dias que ela "fecha quando o Gui receber a primeira build", no
presente, depois de ela já ter fechado.)

Linha de base gravada em 11/08/2026 sobre a build `296474325a`
(`roms/pokemon-claude-2026-08-11.gba`, md5 `457f3b5211b75175a0af5b95e04616c7`),
que é a ROM que o Gui vai jogar. `dev_scripts/save_impressao.json` é a impressão
dela. Daqui em diante, quebra de save não é "aceitável se registrada": é
vermelho no portão, e desfazer é a resposta padrão.

**Cuidado que o guarda NÃO pega, porque não é quebra de save:** flag que só é
acesa em jogo novo (`EventScript_ResetAllMapFlags`) nasce apagada em save
antiga. É o caso de `FLAG_SINNOH_NPC_DUPLICADO` e das três `FLAG_REGIAO_*`: a
save de 05/08 carrega e funciona, mas com os 382 clones visíveis e os portos
fechados. Consertar isso exige `MAP_SCRIPT_ON_TRANSITION`, e é decisão do Gui.

---

## 6. Faixas de id de treinador em uso

**Medido em 11/09/2026, lendo `include/constants/opponents.h` e
`include/constants/opponents_frlg.h`.** A tabela por dono que ficava aqui era de
11/08/2026 e ENVELHECEU: ela prometia a faixa 2441-3999 com teto de 4000, e listava
Kanto em 2200-2273 e Johto em 2274-2440. Nada disso vale mais, porque a onda 1 de
07/09/2026 tirou Unova e Galar do cartucho, os ids foram recompactados e o teto
voltou para o do Emerald. Quem usasse a faixa prometida quebraria save.

| o que | valor | onde está escrito |
|---|---|---|
| teto | **2.200** | `MAX_TRAINERS_COUNT_EMERALD`, `opponents.h:1847` |
| ids definidos hoje | 2.047 | censo dos dois `opponents*.h` |
| maior id definido | **2046** | `TRAINER_JOHTO_RIVAL_SILVER_7` |
| **livre** | **2047 a 2199, 153 ids, e é tudo o que existe** | o único buraco contíguo abaixo do teto |

**Id acima de 2.200 quebra save, e não é opinião.** A flag de "já venci este
treinador" é `TRAINER_FLAGS_START + id`, com `TRAINER_FLAGS_START = 0x500`,
`TRAINER_FLAGS_END = 0x500 + MAX_TRAINERS_COUNT - 1 = 0xD97` e
`SYSTEM_FLAGS = 0xD98` (`include/constants/flags.h:1355-1360`). Um treinador com id
2441 acenderia `0xE49`, **em cima das flags de sistema**.

Quem distribuir faixa a agente recomputa ANTES de prometer, com este censo:

    python3 - <<'FIM'
    import re
    ids=set()
    for p in ('include/constants/opponents.h','include/constants/opponents_frlg.h'):
        ids |= {int(m.group(1)) for m in re.finditer(r'#define\s+TRAINER_[A-Z0-9_]+\s+(\d+)\b', open(p).read())}
    teto=2200
    livres=[i for i in range(1,teto) if i not in ids]
    print('definidos',len(ids),'maior',max(ids),'livres',len(livres),'topo',livres[-5:])
    FIM

Já gasto desta faixa: **2199, 2198 e 2197**, pelos três treinadores do Temple of
Rock (frente D, 11/09/2026). Sobram 2047 a 2196.

**A lição, que é a mesma de 11/08/2026 e por isso dói mais:** tabela errada em
documento é faixa errada em agente. Da primeira vez, duas frentes receberam faixa
inventada a partir desta tabela e as duas descobriram antes de gastar id. Desta vez
quem descobriu foi o executor do Temple of Rock, que foi usar a faixa prometida e
mediu antes de escrever. **Confira aqui, e depois confira a fonte, antes de prometer
faixa a alguém.**

---

## 7. Ferramentas

Todas em `dev_scripts/`. Cada uma tem `--demo` ou `--autoteste` e o motivo de
existir escrito no topo.

| ferramenta | o que faz |
|---|---|
| `antes_de_empurrar.sh` | Portão. Builda o HEAD em worktree isolada e roda tudo |
| `completude.py` | Quanto de cada região está pronto, contra a fonte dela |
| `valida_rom.py` | Compara o declarado com o que o build **emitiu** |
| `valida_warp_tile.py` | Warp que existe e nunca dispara |
| `valida_conectividade.py` | Warp quebrado, alcance, porta única que não devolve |
| `valida_mapas_sinnoh.py` | Sprite sem gráfico, objeto fora do mapa |
| `guarda_save.py` | Impede mudança que invalida save |
| `flags_livres.py` | Quais flags estão **realmente** livres |
| `curva_de_nivel.py` | Mede e remapeia nível do TREINADOR por região |
| `curva_selvagem.py` | Mede e remapeia nível do SELVAGEM, e põe gen 6-9 em slot duplicado |
| `gens69_treinadores.py` | Gen 6-9 nos times, lenda em líder e E4, Dynamax no ace |
| `catalogo_especies.py` | Tipo, stat, geração e lenda de cada espécie, lidos do `species_info` (o enum de `species.h` mistura base e forma, e classificar por faixa de id põe mega de gen 1 na gen 9) |
| `testa_critico.py` | Casos T1 a T30, prova lida da **EWRAM** |
| `gba_runner.c` | Emulador headless que lê memória do jogo (`--mem16`/`--mem32` leem endereço cru) |
| `prova_musica_johto.py` | Qual faixa cada mapa TOCA, lida do header e do driver de som |
| `demake_gen2.py` / `demake_ds.py` | Converte mapa de gen 2 e gen 4 |
| `regua_cidades.py` | Mede quanto CHÃO LISO cada cidade tem, e escolhe as mais sem graça |
| `enfeita_cidades.py` | Enfeita com tema, aprendendo o carimbo de mapa doador do mesmo par de tilesets; idempotente pelo plano em JSON |
| `porto_canalave.py` | Importa bote, poste e tambor do `gTileset_Slateport` para o secundário de Canalave, sem desenhar um pixel |
| `fecha_portas_sinnoh.py` | Interior de cidade de Sinnoh com planta reaproveitada do repo |
| `de_para_sprites_sinnoh.py` | Reaplica o de-para de sprite nos `map.json` de Sinnoh que já foram escritos: repinta o gráfico que o contexto do mapa desmente (a enfermeira do Contest Hall é recepcionista) e corta o corpo mudo repetido que a fonte não tem |
| `abre_portas_extras_sinnoh.py` | Desenha a porta que falta, copiando um warp do proprio mapa |
| `converte_cavernas_sinnoh.py` | Caverna de Sinnoh com a planta CONVERTIDA da grade 2D do DS |
| `importa_placas_johto.py` | Traz placa do `hns` com script e texto, e recusa a que não funciona aqui |
| `texto_placas_sinnoh.py` | Segue índice → `ScriptEntry` → banco de texto do Platinum |
| `itens_escondidos_sinnoh.py` | Desfaz a placa falsa: converte em item escondido o que vale, apaga o resto |
| `liga_flags_kanto.py` | Tira do stub só a flag que algum script mexe |

As cinco fontes ficam em `../fontes-mapas/`: `pokeemerald`, `pokefirered`,
`hns` (Johto), `sinnoh` e `pokeplatinum` (Sinnoh), `bw3g` (Unova). O BW3G morava
em `/tmp` e foi movido em 05/08/2026, porque `/tmp` é limpo pelo sistema e seis
scripts liam de lá.

---

## 8. O que falta, em ordem de tamanho

1. **Sinnoh, mapas em 72,4%, e a fila barata acabou** (medido em 11/08/2026).
   As 12 cavernas de geometria convertida e os 11 interiores teimosos que este
   item listava **já entraram** nas levas de 06/08: hoje
   `abre_bocas_cavernas_sinnoh.py` dá 0 pendências e os outros dois abridores só
   apontam para pai que não é mapa de rua. Faltam **164 mapas**, e nenhum deles
   sai com a técnica atual:

   | quanto | o quê | motivo medido |
   |---|---|---|
   | 46 | Turnback Cave e os `UNKNOWN_533` a `557`, que são as mesmas salas duplicadas | **zero pais** no grafo de warp da fonte: a sala é sorteada por script, não há warp estático que a crie |
   | 10 | Distortion World | zero pais, e a grade dá de 0 a 31 tiles de chão, abaixo do piso de 8 em quase todos |
   | ~40 | Battle Frontier/Tower, salas do ginásio DP de Hearthome, elevadores da Liga, Vista Lighthouse | **zero chão de masmorra na grade**: interiores com mobília desenhada, o caso em que a grade 2D não basta |
   | ~15 | Amity Square, Trophy Garden, Great Marsh 1 a 6, Pal Park, Spring Path, Route 204 North, Fullmoon/Newmoon, Fuego, Hall of Origin | `MAP_TYPE_OUTDOORS`. **Deixados de fora de propósito:** são folhas do grafo e não destravam masmorra nenhuma, então virariam 15 salas vazias de 13x9 com nome de área, ou seja +2,5 pontos de régua e zero mapa (lição 4.10) |

   Passar disso exige converter mobília, não geometria de chão. Decisão do Gui.
   O `fontes-mapas/sinnoh`, que é GBA e seria barato, só tem 133 mapas próprios
   de Sinnoh e **todos os 133 já estão na ROM**: dessa fonte não sobra nada.
2. **Sinnoh, o resto dos NPCs.** Em 11/08/2026, **561 NPCs deixaram de ser mudos
   e 229 placas ganharam texto próprio**, todo o texto portado do pokeplatinum
   por `dev_scripts/texto_sinnoh.py` (o `texto_placas_sinnoh.py` dava 0 porque
   seguia só o comando `Message`, e a fonte usa também `NPCMessage`, 656 vezes,
   mais `EventMessage`, `ShowMapSign` e outros seis). Sobram **559 mudos**, e a
   divisão é medida na fonte: **344 são treinador do Platinum** (o `script` deles
   é constante `TRAINER_*`, não índice de texto: precisa de time e id, é outra
   frente), 108 apontam para Wi-Fi e Union Room, que **não existem nesta ROM**,
   68 são balconista/enfermeira/vendedor cujo rótulo não tem comando de texto,
   19 têm buffer ou caractere fora do charmap, 8 estão em mapa reprovado pelo
   alinhamento.

   **Os 230 `hidden_flag` e os 84 `coord_events` continuam de fora, e não é falta
   de flag.** Medido em `src/event_object_movement.c:2882`: o objeto nasce quando
   `!FlagGet(flagId)`, então flag nova que nenhum script acende deixa o objeto
   sempre visível, ou seja, idêntico a trazê-lo com `flag: "0"`, e ainda planta o
   bloqueio permanente das 39 pedras de Strength de Unova. A flag só vale junto
   com a cena que a acende. Faltam também 71 sem sprite honesto (Cynthia, Cyrus,
   Looker, os lendários de lago). Ver `PENDENCIAS-NPC-SINNOH.md`.
3. ~~146 "placas" de Sinnoh não são placa~~. **FEITO em 11/08/2026** por
   `dev_scripts/itens_escondidos_sinnoh.py`. A causa era o importador:
   `dev_scripts/importa_npcs_sinnoh.py:385` lê `fonte["bg_events"]` cru do
   Platinum, onde placa e item escondido moram no MESMO array e só se distinguem
   pela faixa do `script` (< 2500 = placa, 7000+ = item visível, **8000 a 8799 =
   item escondido**, `include/script_manager.h:90-98` da fonte). O jogador
   parava em cima de um item invisível e lia "the lettering has faded".

   **50 viraram item escondido de verdade** (`bg_events` do tipo `hidden_item`,
   a mesma mecânica de Hoenn: `mapjson` emite `bg_hidden_item_event` e o motor lê
   item, quantidade e flag do próprio evento, sem tabela para manter), em 34
   mapas, **custando 46 flags** da faixa `0x8F0` a `0x91D`. **96 foram
   apagadas**, 95 por serem lixo de rota (Stardust, Pearl, Shard, Poké Ball,
   poção comum) e uma porque `ITEM_SUITE_KEY` não existe nesta ROM.

   **46 flags para 50 itens**, e a diferença não é economia torta: quatro itens
   aparecem em DOIS mapas vizinhos com a MESMA flag do Platinum (Moon Stone em
   EternaCity e Route211_West, Thunderstone em Route229 e ResortArea, Zinc em
   Route219 e Route220, Rare Candy em Route226 e Route227). É costura de mapa da
   fonte, e no Platinum pegar de um lado apaga o do outro; dar uma flag nossa aos
   dois reproduz o jogo original.

   **Apagar `bg_event` não quebra save, e isso foi conferido, não presumido:**
   nada em SaveBlock1/2/3 guarda posição dentro de `bg_events` (o que a save
   guarda de evento é índice de `object_event`, em `objectEvents[]` e
   `objectEventTemplates[]`). Todo acesso do motor varre o array por COORDENADA
   dentro do mapa carregado: `src/field_control_avatar.c:1203`,
   `src/item_use.c:453` e `:483`, `src/secret_base.c:385`. A única identidade de
   item escondido que atravessa o save é a FLAG, e ela viaja dentro do próprio
   dado (`hiddenItemId + FLAG_HIDDEN_ITEMS_START`).

   **Armadilha medida, que continua valendo:** `script - 8000` **não** é a
   posição na tabela `gHiddenItems`, é a posição da flag dentro de
   `HIDDEN_ITEM_FLAGS_START` (`src/script_manager.c:534` da fonte); ler pela
   tabela resolve só 139 dos 146. Quem faz essa conta certo é
   `texto_sinnoh.tabela_de_itens()`, reusada em vez de reescrita.

   **FECHADO em 11/08/2026, mais tarde no mesmo dia.** O que este item chamava
   de "até 13 itens escondidos nos 8 mapas que o alinhamento reprova" eram
   **9, em 3 mapas**, e a estimativa velha errava por contar item escondido da
   fonte em mapa que **nunca importou item escondido nenhum**:
   `fecha_portas_sinnoh.py` e `converte_cavernas_sinnoh.py` já pulam
   `script >= 8000` na origem, então os interiores criados por eles
   (`ContestHallLobby`, `GalacticHq4F`, `GalacticHQ_Laboratory`,
   `PokemonMansionMaidsRoom`, `SandgemTown_RowanLab`) não tinham nada a
   consertar. Sobrava mesmo: 7 na Route222, 1 em GalacticHQ_2F e 1 em
   SinnohLeague_Entrance. Dois viraram item escondido (SKY PLATE e PP UP,
   custando **1 flag nova**, porque a do SKY PLATE já existia) e 7 foram
   apagados como lixo de rota.

   **Sobra exatamente UM, e ele fica**: o `script` 8075 de `GalacticHQ_2F` cai
   em (13,1) junto com outro evento da fonte depois da conversão de coordenada,
   e dois candidatos no mesmo tile não se distinguem. Escolher um seria o chute
   que esta ferramenta existe para evitar.

   **O alinhamento deixou de ser por ORDEM e passou a ser por COORDENADA**, e a
   troca não é gosto: a própria passada das 146 quebrou a régua velha. Apagar 96
   `bg_events` encurtou os nossos arrays e a contagem parou de bater em 40 mapas
   **já resolvidos**, ou seja, a ferramenta ficaria incapaz de rodar de novo.
   Coordenada sobrevive: `importa_npcs_sinnoh.conversor_de_coordenada()`
   (extraída do próprio importador, não reescrita) diz onde cada evento da fonte
   foi parar, e a conta é refeita em vez de adivinhada. Duas guardas seguram o
   chute: **um `bg_event` nosso em coordenada que a fonte não tem reprova o mapa
   inteiro**, e **coordenada com mais de um candidato fica de fora**.

   **Contraprova rodada antes de escrever qualquer coisa:** o alinhamento novo
   reproduz os **50 de 50** itens que a passada ordinal já tinha convertido, com
   o mesmo item e a mesma flag do Platinum, zero divergência. E a regra do órfão
   separa sozinha os 96 mapas de `importa_npcs_sinnoh.py` dos 38 dos outros dois
   conversores: ela concorda com o campo `origem` do `map.json` nos 134, sem
   nenhuma exceção.

   **Numeração de flag passou a ser append-only** no mesmo dia, e isso era
   quebra de save esperando acontecer: `flags_em_uso()` reatribuía a faixa
   inteira por ordem alfabética a cada passada, então um nome novo no meio do
   alfabeto empurraria os 46 apelidos que já estão na ROM do Gui uma casa cada.
   Agora quem já tem número fica com ele e o nome novo só ocupa vaga livre.
4. **Unova.** Este item também estava velho: as 117 placas entraram em
   `febde977c3` e 33 NPCs em `0508831d27`. Em 11/08/2026 entraram as **9 trocas
   de Pokémon** (`dev_scripts/importa_trocas_unova.py`; `trade NPC_TRADE_X` lê
   tabela, não script, e por isso o importador de NPC recusava essas casas):
   objetos mudos 114 → 106, custo de 9 flags, zero var.

   O que sobra são as **209 cenas de enredo**, classificadas uma a uma: 107 são
   `changeblock` (1225 chamadas, exigem traduzir id de bloco de gen 2 para
   metatile), 47 usam `setscene`, 27 abrem batalha, 21 `special`, 16 `callasm`
   (a máquina de estados da Plasma). Das 32 mecanicamente portáveis, **17 são
   bloqueio** que o enredo apaga na fonte e aqui nunca apagaria, virando parede
   permanente (a armadilha das 39 pedras de Strength). Ver `PLANO-UNOVA.md`.
5. **426 flags de Kanto seguem em `0`**, e isso está certo: elas não são mexidas
   por script nenhum, então dar número a elas não mudaria nada em jogo. As 104
   que importavam saíram do stub em 05/08/2026
   (`dev_scripts/liga_flags_kanto.py`).
6. **As 20 rotas dirigidas de barco estão provadas em ROM** (T4, T6, T8, T10 e
   T86.1 a T86.12, prova lida da EWRAM, com mutante para cada caso). O texto de
   jogo dos cinco portos **saiu do português em 11/08/2026** e está em inglês,
   como o resto do jogo; junto foram as quatro falas do assistente do PROF. OAK
   em Vermilion, o item "Sair" do menu do marinheiro (agora "EXIT") e a balsa
   interna de Sinnoh entre Snowpoint e a Battle Zone, que ninguém tinha visto e
   falava português pelo mesmo motivo. **Nenhuma caixa de texto mudou de número
   de páginas**: os `\p` foram conferidos rótulo a rótulo contra o HEAD antes de
   buildar, zero divergência, e por isso nenhum dos 24 roteiros de botão que
   atravessam porto precisou ser reescrito. Re-rodado na build seguinte. As três
   `FLAG_REGIAO_*_LIBERADA` **foram ligadas em 11/08/2026**: o menu do marinheiro
   passou a ser montado em `data/scripts/travessia_regioes.inc` e esconde o
   destino da região ainda não liberada (Kanto sempre aberto; Johto pelo campeão
   de Kanto; Hoenn pela 8ª insígnia de Johto, porque esta ROM não tem Elite dos
   Quatro de Johto; Sinnoh pelo Wallace; Unova por `FLAG_ELITE_SINNOH_VENCIDA`,
   que a Cynthia já acendia). Zero flag nova, zero var, e nenhum `case` de porto
   mudou, porque `dynmultipush` devolve o **id empilhado** e não a linha. **O
   portão está provado na ROM** pelos casos T87.1 a T87.5, e a prova tem
   contraprova: numa ROM mutante, com os `call_if_set` do menu virando `call`,
   os cinco falham no ponto que a mutação prevê. Ver `PENDENCIAS-TRAVESSIA.md`.
7. **Ninguém jogou do começo ao fim.** Tudo aqui é build, dado estático e
   emulador em ponto específico.

**O aperto de ROM que este documento anunciava não existia.** Os "93 KB de
margem" eram a distância até uma linha de 95% que eu mesmo inventei como aviso,
não até o teto de 32 MB. Livres na build de 11/08/2026: **1,56 MB** (a ROM está
em 95,11%). Unova completa cabe, o resto de Sinnoh cabe, as placas de Johto
couberam.

---

## 9. Onde está o resto

| documento | assunto |
|---|---|
| `PRD-ROM-COMPLETA.md` | **O plano para acabar o hack**, em blocos B0 a B11, com os limites medidos e os portões que exigem o Gui |
| `PRD-CINCO-REGIOES.md` | Plano por blocos, decisões, desenho dos testes |
| `HANDOFF-2026-08-05.md` | O caso Kanto em detalhe, as oito camadas |
| `PLANO-UNOVA.md` | Unova: o que entrou, o que falta, e por quê |
| `PENDENCIAS-TRAVESSIA.md` | Barco entre regiões, o que foi provado e o que não |
| `PENDENCIAS-JOHTO.md`, `PENDENCIAS-INTRO.md`, `PENDENCIAS-GALACTICA.md` | Pendências por frente |
| `SINNOH-PADRAO.md` | Padrões de script que economizam var |
| `RECURSOS-REGIOES.md` | Fontes avaliadas, com o veredito medido de cada |
| `DEMAKE-DS.md` | Formato de mapa de gen 4 e gen 5 |
