# Fase de conteúdo de Galar: o que foi medido, o que foi feito, o que sobra

Escrito em 21/08/2026 como rascunho de executor, e **corrigido no mesmo dia pelo
executor que mediu**, depois que o bloco c3 foi executado e derrubou a premissa
central da primeira versão. A condutora aceitou a medição e mandou corrigir aqui.
O ESTADO 0.i ainda carrega o número velho e será corrigido no fechamento.

Fonte: demake fan-made Ultimate Plus v1.2.1.2 em `fontes-mapas/galar-swsh/`
(fora do repo, sem remote). Ferramentas que medem: `dev_scripts/fala_galar.py`
(baldes a e b), `dev_scripts/cenas_galar.py` (blocos c1 e c3),
`dev_scripts/fila_galar.py` (a fila reconta a verdade do dia).

## A CORREÇÃO, e ela é de constante e não de contagem

A primeira versão deste documento chamava os 144 map_scripts de tabela `(3,)` de
"ON_FRAME_TABLE puro" e desenhava a fase inteira em cima disso. Está errado. Em
`fontes-mapas/pokefirered/include/constants/map_scripts.h`:

    MAP_SCRIPT_ON_LOAD                 1
    MAP_SCRIPT_ON_FRAME_TABLE          2      <- a tabela `var, valor, script`
    MAP_SCRIPT_ON_TRANSITION           3      <- bytecode solto, os "144"
    MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE  4      <- também tabela

Os 144 são **ON_TRANSITION**, que é bytecode e não tem var nem valor. Quem pede
`map_script_2 VAR, valor, Script` são os tipos 2 e 4, e deles a fonte tem
**19 tabelas em 17 mapas**, não 144. O `--demo` do `cenas_galar.py` reprova se
esses três números mudarem calados.

Segundo achado, do mesmo dia: dos 144 ON_TRANSITION, **139 não escrevem var
nenhuma** e 77 são literalmente `setflag 0x918; setflag 0x90E; release; end`.
As quatro flags que dominam (0x90D, 0x90E, 0x918, 0x91A) estão ACIMA da
`FLAGS_COUNT` do FireRed (0x900), e a varredura crua da ROM mostra que 0x90E tem
98 `setflag`, 97 `clearflag` e **zero `checkflag`**: quem as lê é código C do
hack, que a nossa ROM não tem. Portá-las seria acender lâmpada sem fio.

## Os quatro baldes, medidos (`python3 dev_scripts/fala_galar.py`)

| balde | total | script_objeto | placa | map_script | porta_morta |
|---|---|---|---|---|---|
| a_fala (zero estado novo) | 466 | 414 | 52 | 0 | 0 |
| b_flag | 93 | 93 | 0 | 0 | 0 |
| c_var_cena | 2.311 | 1.821 | 70 | 194 | 226 |
| d_treinador | 325 | 313 | 12 | 0 | 0 |
| **TOTAL** | **3.195** | | | | |

Fila em 21/08 depois do c3: **2.630 pendentes**, 461 feitas, 104 descartadas.

## Orçamento, com o número real

**Flags: sobram 5.711** (`flags_livres.py`), 4.447 numa faixa contígua. Flag não
é gargalo de nada nesta fase. A onda 1 gastou 56; o c3 gastou **zero**.

**Vars: 150 livres medidas** (0x4100, 0x4107-0x412F, 0x417E-0x41BF,
0x41D6-0x41FF), das quais o c3 gastou **3** e restam **147**. A estimativa de
"200 a 260" da primeira versão nasceu do erro de constante acima: com uma var por
MAPA e só 17 mapas com tabela, **não há déficit nenhum**. Nada de crescer
`VARS_COUNT`, e a save fica onde está.

## Blocos, com o estado de cada um

- **c1, faixa e portão. FEITO em 21/08.** `dev_scripts/cenas_galar.py` mede a
  faixa livre pelo pré-processador (mesma máquina do `guarda_colisao_vars.py`,
  sobre uma árvore em que o próprio bloco foi retirado, senão a segunda rodada
  escolheria outras vars), declara `VAR_GALAR_<MAPA>_CENA` em bloco delimitado no
  fim de `include/constants/vars.h` como apelido de `VAR_UNUSED_*`, e o `--demo`
  planta DUAS vars de Galar na mesma vaga livre e prova que o portão REPROVA,
  com o par negativo (alocação sozinha não reprova).
- **c2, tabela vazia** (62 linhas). **FEITO em 21/08.**
- **c3, map script. FEITO em 21/08: 16 cenas em 16 mapas** (2 ON_FRAME_TABLE,
  1 ON_WARP_INTO_MAP_TABLE, 13 ON_TRANSITION, estas com corpo deduplicado porque
  os 13 mapas da Wild Area apontam para o MESMO offset da fonte). Custo: 3 vars,
  0 flags. Provado por T127, 8 casos em 4 pares: dispara na primeira entrada e
  não na segunda; a var sobrevive a salvar e recarregar a `.sav`; duas cenas em
  mapas diferentes não se atrapalham, nos dois sentidos; o NPC sai do caminho
  depois da cena.
- **c4, cena de OBJETO com estado.** É o que sobra, e agora é o grosso. Ver a
  classificação medida abaixo.

### As 301 entradas de map script que ficaram de fora do c3, por motivo

    82  cena vira no-op depois da traducao (so `release; end`)
    44  entrada de map script com ponteiro sujo (tabela lida em cima de dado)
    25  `setworldmapflag` (comando so do FRLG, sem equivalente aqui)
    24  tipo 5 (ON_RESUME) fora do bloco
    14  tipo 1 (ON_LOAD) fora do bloco
    14  id de objeto vindo de var (0x8007), nao de literal
    13  `setrespawn` (id de heal location do FR nao e o nosso)
    13  `special` (indice do FR nao e o nosso)
     8  opcode 0xFF em posicao nao provavelmente inalcancavel
    ~40 flag de motor do demake (0x320, 0x110E, 0x409, 0xAF0, 0x10A2, ...)
     3  tabela apontando para var que nao e de save
     2  segundo estado no mesmo mapa (o preco declarado de uma var por MAPA)
     2  objeto local que o G4 nao pos no mapa
     2  `specialvar`

**Sobre os 390 indecisos e a `gScriptCmdTable`:** medir a tabela de opcodes do
demake contra a do FireRed NÃO era necessário para o c3, e isso é medição e não
desistência. Em map script a única falha de decodificação encontrada foi o
opcode `0xFF`, que é byte de ENCHIMENTO de espaço livre e não comando. Os 390
indecisos são todos scripts de OBJETO, ou seja balde c4, e é lá que a medição da
`gScriptCmdTable` continua valendo a pena.

## (c4) Classificação MEDIDA das 1.891 linhas de objeto e placa

As 1.385 "comando de estado" mais os 390 "decodificação incompleta" mais os 116
de texto somam as 1.891 linhas de `script_objeto` e `placa` do balde c. Cada
linha entra no padrão do seu bloqueio MAIS PESADO, porque a linha só fica
executável quando todos os bloqueios dela caem. Ordem: opcode, `special`,
`trainerbattle`, entrega de item, var de etapa, flag de esconder, resto.

| padrão | linhas | o que trava |
|---|---|---|
| resto (movimento, fala, `fadescreen`, warp) | **1.038** | nada de estado: é porte mecânico, o mesmo tradutor do c3 serve |
| opcode indecodificável | **390** | ramo cai em opcode que o FR não tem; aqui SIM vale medir a `gScriptCmdTable` do demake |
| `special`/`specialvar` do FireRed | **282** | índice do FR não é o nosso; cada `special` precisa de decisão própria |
| só `setflag`/`checkflag` de esconder | **104** | flag do pool livre (5.711 sobrando), custo zero de save |
| `givemon`/`giveitem`/loja | **58** | espécie e item precisam do de-para que o `gente_galar` já tem |
| `setvar`/`compare` de etapa | **19** | var de cena, e é o único padrão que gasta var |
| **TOTAL** | **1.891** | |

**Quanto "uma var por MAPA" cobre, medido:** só **43 linhas** de objeto e placa
tocam var de estado salva, espalhadas por **28 mapas** e **22 vars distintas** da
fonte. Desses 28 mapas, **18 usam UMA var só** (22 linhas, cobertas inteiras pelo
desenho) e **10 usam duas ou mais** (21 linhas), sendo que três deles usam 9, 9 e
7 vars: nesses, uma var por mapa cobre a var mais usada e as outras entradas saem
com motivo, como já acontece no c3. Custo total se o c4 inteiro entrar: **28
vars**, contra 147 livres. **Var continua não sendo o gargalo desta fase; o
gargalo é `special` e opcode.**

### Sugestão de ordem para despachar o c4 (a condutora decide)

1. **c4a, os 1.038 do resto**: maior volume, zero endereço novo, e reusa o
   tradutor do `cenas_galar.py` sem uma linha de desenho nova.
2. **c4b, as 104 de flag de esconder**: barato e visível (NPC que some de vez).
3. **c4c, as 58 de item e Pokémon**: precisa do de-para de espécie e item.
4. **c4d, as 19 de var de etapa**: 28 vars no pior caso, dentro do orçamento.
5. **c4e, os 390 indecisos**: começa medindo a `gScriptCmdTable` do demake contra
   a do FR (se a tabela cresceu, os comandos novos existem e dá para dimensioná-
   los pelo ponteiro de cada entrada); o que não destravar fica de fora com
   motivo.
6. **c4f, os 282 de `special`**: o mais caro por linha, e o único que pede
   decisão caso a caso. Provavelmente nunca entra inteiro.

## (d) treinadores: medição, com o aviso na frente

**AVISO, e ele vale mais que os números abaixo: o struct de party do demake não
é o do FireRed.** Lendo `gTrainers` em 0x23EAC8 com o molde do FR (40 B por
entrada, party de 6/8/14/16 B por `partyFlags`), só **165 dos 741 times passam na
validação** de espécie e nível plausíveis. Os 576 reprovados não são treinadores
vazios, são o molde errado. Quem executar mede o stride antes de acreditar em
qualquer número daqui.

Do que passou: **278 ids de treinador citados pelos scripts de Galar** (faixa 1 a
741), 774 Pokémon, nível mínimo 18, **mediana 70**, e **276 deles exatamente no
nível 100**. A curva da fonte é de pós-jogo, não de campanha: importada crua,
Galar inteira nasce em nível 100. Isso entra na mesma decisão do Gui que congelou
a Fase F, e não se executa aqui.
