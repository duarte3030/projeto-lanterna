# PRD: cinco regiões, de Kanto a Unova

Documento para o Gui montar o `/goal` da noite de 05/08/2026. Tudo que está
marcado como **medido** foi verificado nesta sessão, com o comando ao lado.
O que não foi medido está marcado como **presumido**.

---

## 1. A descoberta que muda o plano

**Existe código-fonte público da Unova, em pokecrystal, e ele encaixa no
conversor que já temos.**

`github.com/AzureKeys/BW3G` — *Black and White 3: Genesis*, de Azure_Keys.
Clonado e conferido agora:

| evidência | valor | como conferi |
|---|---|---|
| formato | projeto pokecrystal | `README.md` diz "based on pokecrystal" |
| mapas | **289 arquivos `.ablk`** | `find . -name "*.ablk" \| wc -l` |
| dimensões declaradas | **293 `map_const`** | `grep -c map_const constants/map_constants.asm` |
| colisão por tileset | sim, inclui `castelia_collision.asm` | `ls data/tilesets/*_collision.asm` |
| nomes de Unova | 69 ocorrências | `grep -icE "castelia\|nimbasa\|driftveil\|humilau\|opelucid\|virbank"` |

E o teste que importa, o do formato:

```
ACCUMULA_TOWN, 15, 12  →  15 × 12 = 180  →  AccumulaTown.ablk tem 180 bytes
DRIFTVEIL_CITY, 26, 20 →  26 × 20 = 520  →  DriftveilCity.ablk tem 520 bytes
```

Casa exato. `.ablk` é 1 byte por bloco, o mesmo `.blk` que
`dev_scripts/demake_gen2.py` já converte, **provado no esconderijo de Mahogany**,
que saiu com geometria e warps exatos sem reposicionar nada.

**Consequência direta:** o `PLANO-UNOVA.md` dizia que o passo 2 era achar as
tabelas de cabeçalho dentro do `.gbc` na mão, e chamava isso de "engenharia
reversa de verdade, não uma tarde". **Esse passo morreu.** Não precisa raspar
binário: tem `.ablk` com dimensão declarada, colisão por tileset, e os `.asm` de
cada mapa com warps, objetos e texto já organizados.

O `.gbc` que o Gui baixou continua útil como conferência visual, mas não é mais
a fonte.

**Autoria:** o projeto é de Azure_Keys, com tiles de Rangi, PiaCarrot,
Bloodless, Bees, JaceDeane, Morlock e Luna, e música de Mmmmmmmmmmm,
FroggestSpirit, TriteHexagon, Regen e Azure_Keys. Mesma consideração que o Gui
já aceitou para o demake de Galar. Ver pergunta 70.

---

## 2. Estado medido hoje

> **Medição de 05/08/2026, fim da segunda noite.** A tabela original desta seção
> ficou abaixo como registro do ponto de partida; ela NÃO vale mais. Números de
> agora, todos por comando (`ESTADO.md` tem a versão completa):
>
> | medida | valor |
> |---|---|
> | ROM | 31.476.792 B = **93,81% de 32 MB** (1,98 MB livres) |
> | mapas | **1616** |
> | treinadores com time próprio | **2346** |
> | grupos de mapa que carregam | **101 de 101** |
> | flags livres no pool | **184** |
>
> Completude contra a fonte de cada região (`dev_scripts/completude.py`),
> 100% = tão completo quanto o jogo de origem:
>
> | região | mapas | objetos | warps | placas |
> |---|---|---|---|---|
> | Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
> | Johto | 63,6% | 93,9% | 100,0% | 96,0% |
> | Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
> | Sinnoh | **25,6%** | 88,0% | **61,8%** | 107,6% |
> | Unova | 94,2% | 98,5% | 98,9% | 76,9% |
>
> Hoenn é o controle: nossa Hoenn é o vanilla intocado, então tem que dar 100%.
>
> **O "aperto de ROM" que este documento anunciou não existia.** Os 93 KB de
> margem eram até uma linha de 95% inventada como aviso, não até o teto de
> 32 MB. Unova completa cabe, o resto de Sinnoh cabe.
>
> **Sinnoh é o que sobrou de grande, e é caro:** os 455 mapas que faltam existem
> só no `pokeplatinum`, em formato de DS. O `fontes-mapas/sinnoh`, que é GBA e
> seria barato, tem 133 mapas próprios de Sinnoh e **os 133 já estão na ROM**.

Build limpo, último commit de conteúdo `755f50cc7c`.

| medida | valor | comando |
|---|---|---|
| ROM | 28.270.092 B = **84,25% de 32 MB** | saída do `make` |
| EWRAM | 226.652 B = **86,46%** (29 KB livres) | idem |
| IWRAM | 28.384 B = **86,62%** (4 KB livres) | idem |
| mapas | **1327** | `map_groups.json` |
| layouts | **1332** | `layouts.json` |
| alcance a pé desde Twinleaf | **1050 de 1327** | `valida_conectividade.py` |
| warps quebrados | **0** | idem |
| vars livres | **30** | `grep -c VAR_UNUSED` |
| flags livres | **457** | `grep -c FLAG_UNUSED` |
| MAPSEC em uso | ~220 de 255 (`u8`) | `region_map_sections.h` |
| tabelas de selvagem | **522** | `wild_encounters.json` |

Mapas por região:

| região | mapas | estado |
|---|---|---|
| Kanto (FRLG) | 417 | presente e ligado por barco |
| Johto | 228 | 8 ginásios, 78 mapas com selvagem, Rocket, torres, farol |
| Hoenn | ~290 | original, intacto |
| Sinnoh | 96 | começo, 8 ginásios, Galáctica, Elite, Cynthia, Hall da Fama |
| **Unova** | **0** | não existe |

**CORREÇÃO, 05/08/2026: eram três regiões, não quatro. Kanto nunca esteve na
ROM.** Ver seção 11.

**Ligação entre regiões:** `data/maps/CanalaveCity/scripts.inc` tem o marinheiro
com três destinos, `MAP_OLIVINE_CITY_PORT_INSIDE`, `MAP_SLATEPORT_CITY_HARBOR` e
`MAP_VERMILION_CITY`. A constante existe e aponta para a pasta
`data/maps/VermilionCity_Frlg`. O que eu não conferi na hora foi se esse mapa
chega a existir dentro da ROM. Não chegava.

**Início:** `src/new_game.c:155` manda para `MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F`.
Existe um ramo em `:151` apontando para `MAP_PALLET_TOWN_PLAYERS_HOUSE_2F`.
Hoje o jogo começa em Sinnoh.

---

## 3. Duas coisas podres que achei agora

**3.1 — Kalos fantasma, 34 mapas.**
`data/maps/` tem 34 pastas de Kalos (Vaniville, Lumiose, Santalune, ginásios) e
`layouts.json` tem 36 entradas, mas **nenhuma pasta de layout existe**. É
exatamente a doença da Unova falsa que apagamos: `map.json` apontando para
layout que não existe. Está inerte só porque `gMapGroup_Kalos` **não está em
`group_order`**, então nada compila. Se alguém puser lá, quebra.

**3.2 — `gMapGroup_SinnohWest` pendurado.**
Está listado em `group_order` mas **não existe como chave** no
`map_groups.json`. Sobra da reorganização de MAPSEC. Qualquer ferramenta que
percorra `group_order` e indexe direto estoura, e três dos meus scripts
estouraram hoje nisso.

Ambos entram no bloco 0, porque são baratos e são armadilha.

---

## 4. O que o agente dos ginásios entregou (terminou agora)

7 de 8 ginásios de Sinnoh com planta real do Platinum, líder alcançável em
todos, provado por flood fill lido **dos arquivos gravados**, não da conversão
em memória.

Achados dele que valem para o resto do trabalho:

- **6 dos 8 ginásios saíam para o warp 0 da cidade**, que é a porta de outro
  prédio. O `valida_conectividade.py` não pegava porque índice 0 existe. Isso é
  uma classe de bug que o validador ainda não cobre.
- O metatile mais usado como chão em `SootopolisCity_Gym_1F` é **525 =
  `MB_THIN_ICE`**, gelo que racha e derruba o jogador num andar que não existe.
  Era a escolha óbvia por frequência, e estava errada.
- **Canalave não converteu**: é ginásio de plataformas em vários níveis, a grade
  2D sai degenerada (896 de 896 tiles andáveis, sala vazia) e o Byron cai numa
  faixa de altura sem dado. Fica com layout de Hoenn.

---

## 5. Escopo proposto, em blocos com "pronto" verificável

Cada bloco tem um teste que falha se o bloco não estiver pronto. Sem teste, o
bloco não está definido.

### Bloco 0 — Limpar o terreno
- Apagar Kalos fantasma (34 mapas, 36 layouts)
- Remover `gMapGroup_SinnohWest` de `group_order`
- Apagar os 3 mapas `_NIGHT` mortos
- Buildar com o trabalho dos ginásios

**Pronto quando:** `make` EXIT=0, `valida_conectividade.py` com 0 warps
quebrados, `valida_mapas_sinnoh.py` sem regressão, `testa_percurso.py` 6/6.

### Bloco 1 — Unova de verdade (o maior)
- Clonar BW3G, estender `demake_gen2.py` para `.ablk` e para os tilesets do BW3G
- Converter os 289 mapas, colisão exata
- Ler warps, objetos e sinais dos `.asm` de cada mapa
- Registrar em `layouts.json`, `map_groups.json`, `event_scripts.s`
- MAPSEC agrupada: `UNOVA_WEST/EAST/NORTH`, com apelido por cidade no template
  versionado (`region_map_sections.constants.json.txt`, **nunca no `.h` gerado**)
- Tabelas de selvagem
- Ligar ao barco de Canalave, ida e volta

**Pronto quando:** um percurso automatizado sai do barco, anda por Unova, entra
e sai de pelo menos 10 prédios, e volta; 0 warps quebrados; 0 sprite quebrado.

### Bloco 2 — As cinco regiões ligadas e testadas
- Conferir entrada e saída de cada região, nos dois sentidos
- Cobrir o buraco que o agente achou: **warp que aponta para índice válido mas
  errado**. Regra nova no validador: se A warpa para B, algum warp de B deve
  voltar para perto da origem em A. Sem isso, "0 quebrados" mente.

**Pronto quando:** o validador roda com a regra de ida-e-volta e passa nas 5
regiões.

### Bloco 3 — Começo em Pallet e ordem cronológica (decisão 66)
- Ligar o início em `MAP_PALLET_TOWN_PLAYERS_HOUSE_2F`
- Abertura de Kanto: Oak, escolha de inicial, rival
- Abertura de Sinnoh vira chegada de meio de jogo
- Transição Kanto → Johto: campeão de Kanto, ticket do Oak, barco em Vermilion
- Curva de nível na ordem nova

**Pronto quando:** T1 e T4 passam.

### Bloco 4 — Iniciais e encontros por região (decisão 68)
- Trio de iniciais entregue na chegada de cada região
- Selvagens coerentes por rota e cidade

**Pronto quando:** cada uma das 5 regiões entrega trio, lido da memória.

### Bloco 5 — Teste de cabo a rabo
- Leitura de memória no `gba_runner` (ver seção 10, é o item mais valioso)
- T1 a T10, um por região, não um percurso gigante
- Menu de debug já existe: R + START, `include/config/debug.h:15`

**Pronto quando:** T1 a T10 passam, cada um provando a coisa específica, nunca
só "não travou".

### Bloco 6 — Polimento
Canalave (o ginásio que não converteu), laboratório do Rowan em mapa próprio,
tela de introdução, sprites provisórios.

---

## 6. Riscos reais, não de cronograma

**O que aperta antes do cartucho é MAPSEC e RAM, não ROM.** ROM tem 3,7 MB
livres e Unova cabe. MAPSEC tem ~35 vagas de 255 e é `u8`; por isso Unova usa
MAPSEC agrupada. IWRAM tem 4 KB. **Erro de link sem motivo aparente = olhar RAM
antes de ROM.**

**O risco que já mordeu duas vezes é sinal verde falso**, não falta de tempo:
seis agentes e dois validadores passaram limpo com a ROM resetando na tela de
título. Por isso todo bloco fecha com build **e** emulador, nunca só validador.

**Vars são o recurso escasso**, 30 no jogo inteiro para cinco regiões. Flags são
baratas, 457. Toda cena nova de Unova deve usar os padrões que já provamos:
`goto_if_defeated` em flag de treinador, `setmetatile` em `ON_LOAD`, NPC parado
no único tile passável, raio de visão de treinador no lugar de `coord_event`.

**Agentes em paralelo colidem em faixa de flag.** Já aconteceu hoje. Distribuir
faixa por agente na hora de disparar.

---

## 7. Ideias que eu proponho, além do que foi pedido

1. **Menu de debug com warp por região.** Sem isso, testar Unova exige jogar
   quatro regiões antes. É a ferramenta que mais economiza tempo na noite.
2. **Regra de ida-e-volta no validador de conectividade** (bloco 2). O bug dos 6
   ginásios passou por baixo do validador atual.
3. **Percurso automatizado por região**, não um só gigante: falha localizada
   diz onde, falha global só diz que falhou.
4. **Nunca escrever mapa do zero.** Toda vez nesta sessão que a resposta foi "a
   fonte já tem", foi certo; toda vez que foi "escrevo do zero", foi errado.
5. **`.ablk` do BW3G tem os `.asm` junto**, com warp, objeto, sinal e texto. Dá
   para portar a estrutura de eventos, não só a geometria. Isso é o que separa
   "Unova existe" de "Unova é jogável".

---

## 8. Decisões do Gui, 05/08/2026

Respondidas. Não são mais perguntas, são requisito.

| # | decisão |
|---|---|
| 66 | **Começa em Pallet Town**, ordem cronológica **Kanto → Johto → Hoenn → Sinnoh → Unova** |
| 67 | **Cynthia fecha Sinnoh, Alder fecha Unova** como desafio final |
| 68 | **Cada região entrega seu trio de iniciais** quando o jogador chega nela |
| 69 | **Portar** o texto e a história do BW3G, não escrever enredo novo |
| 70 | **Só creditar** Azure_Keys e os artistas. Não contatar |

### O que a decisão 66 arrasta junto

Mudar o início de Twinleaf para Pallet não é trocar uma linha em
`src/new_game.c:155`. O ramo para `MAP_PALLET_TOWN_PLAYERS_HOUSE_2F` já existe
em `:151`, mas ligar ele deixa pendente:

- **Kanto precisa de abertura**: Oak, escolha de inicial, rival. Hoje quem tem
  abertura pronta é Sinnoh.
- **A abertura de Sinnoh vira chegada de meio de jogo.** Rowan e a escolha de
  inicial de Sinnoh passam a ser o trio da quarta região, pela decisão 68.
- **A história da Galáctica sobe de nível.** Hoje ela é conteúdo de começo.
- **A curva de nível inverte.** Sinnoh deixa de ser regiao 1 e vira a 4.
- **O barco de Canalave muda de papel**: hoje é o hub que sai de Sinnoh, passa a
  ser o trecho final Hoenn → Sinnoh → Unova.

Nada disso é impeditivo, mas é a maior mudança estrutural do plano, e deve ser
feita em bloco próprio, com teste próprio, não espalhada.

---

## 9. Regra de parada, corrigida pelo Gui

Antes estava ambíguo. A regra correta:

**Parar por dúvida ou risco de retrabalho para UMA frente de trabalho, nunca
para o trabalho todo.** Se um agente específico esbarra numa decisão que só o
Gui toma, **aquele agente para e reporta; todos os outros continuam**. O grosso
do trabalho nunca fica bloqueado por uma pendência localizada.

Na prática: a pendência vira item numerado da lista final, a frente dela fica
parada, e o resto segue. Frente parada nunca vira sessão parada.

---

## 10. Como testar, de verdade

O Gui pediu para eu bolar isto, e é a parte que decide se a noite vale.

### O problema

Não dá para jogar até a hora 20 para testar a transição Kanto → Johto. Se o
teste exigir chegar lá jogando, ele nunca roda.

### A saída, que já está pronta e provada

`include/config/debug.h:15` tem `DEBUG_OVERWORLD_MENU DISABLED_ON_RELEASE`, e a
combinação é **R + START** (`:16`, `:17`). O `gba_runner` **já aceita acorde
`R+START!`** e já abriu esse menu nesta sessão. Ou seja: dá para saltar para
qualquer mapa e acender qualquer flag sem jogar até lá.

Cada teste vira uma tripla:

```
cenário = (flags a acender, mapa de destino, roteiro de botões, o que provar)
```

### O que falta construir, e é o item mais valioso da noite

**Ler a memória do jogo em vez de adivinhar pelo pixel.** O `gba_runner` já é
linkado com `libmgba`, então ele consegue ler EWRAM direto. Com isso um teste
afirma `FLAG_X está acesa` ou `o time tem 1 Pokémon` **lendo o dado**, em vez de
inferir da tela.

Isso mata de uma vez a família de falso positivo que já mordeu duas vezes hoje:
tela que parece certa com estado errado, e quadro repetido lido como travamento.
Enquanto o teste olhar só pixel, "passou" continua sendo palpite.

### Os testes críticos, na ordem

| # | teste | prova |
|---|---|---|
| T1 | Novo jogo em Pallet: quarto, desce, sai, lab do Oak, escolhe inicial | time tem 1 Pokémon, lido da memória |
| T2 | Os 8 ginásios de Kanto: entra, chega no líder | carrega sem reset, líder alcançável |
| T3 | Victory Road, Indigo Plateau, Elite dos Quatro | os 5 mapas carregam em sequência |
| T4 | **Transição Kanto → Johto**: acende a flag de campeão de Kanto, vai ao gatilho, pega o ticket do Oak, embarca em Vermilion, desembarca em Johto | flag de ticket acende, e o mapa final é de Johto |
| T5 | Eventos de gen 2: Sprout Tower, Slowpoke Well, Burned Tower, Torre Rádio, esconderijo de Mahogany, Farol de Olivine | cada evento dispara, medido por flag |
| T6 | Johto → Hoenn de barco | mapa final é de Hoenn |
| T7 | Hoenn: liga e campeão | carrega |
| T8 | Hoenn → Sinnoh, Slateport → Canalave | mapa final é de Sinnoh |
| T9 | Sinnoh: Galáctica, Spear Pillar, Cynthia, Hall da Fama | cada um carrega, Cynthia alcançável |
| T10 | Sinnoh → Unova de barco | mapa final é de Unova |

**Critério que não vale:** "não travou". Todo teste tem que provar que a coisa
específica aconteceu. Um teste que só sabe dizer que o jogo não caiu é um teste
que passa com o jogo quebrado, e foi exatamente assim que dois crashes desta
sessão sobreviveram a seis agentes.

### T11 — a save sobrevive à atualização da ROM

Requisito do Gui, 05/08/2026: **achar um bug na hora 50 de jogo não pode custar
recomeçar.** Em pokeemerald não existe versionamento de save nem migração, o
SaveBlock é despejado cru na flash, então todo índice que a save guarda é
promessa permanente.

O jeito mais fácil de quebrar é o menos visível: **a save guarda a posição do
jogador como par de índices `(mapGroup, mapNum)`, não como nome.** Apagar ou
reordenar mapa no meio de um grupo desloca todos os seguintes, e a save volta em
outro lugar. Foi exatamente o que o bloco 0 fez ao remover os três `_Night`.
Saiu de graça só porque ainda não havia save para proteger.

Regras que passam a valer, impostas por `dev_scripts/guarda_save.py`:

| regra | por quê |
|---|---|
| mapa novo **só no fim do grupo** | inserir no meio empurra os índices seguintes |
| grupo novo **só no fim de `group_order`** | inserir no meio desloca grupos inteiros |
| flag nova **só do pool `FLAG_UNUSED_*`** | número novo cresce `flags[]`, que está em 0x1270 do SaveBlock1 |
| struct de save **só recebe append** | trocar ordem de campo reinterpreta a save inteira |

**Teto medido, e é apertado: SaveBlock1 está em 15764 bytes de 15872 (99,3% dos
setores 1 a 4). Sobram 108 bytes.** Passar disso não dá erro de compilação, dá
save corrompida.

O teste T11 fecha o assunto: joga, salva, rebuilda a ROM com mudança, recarrega
a mesma `.sav` e prova pela memória que o jogador está no mesmo mapa, com o
mesmo time e as mesmas flags. Só é possível porque a frente A está fazendo o
leitor de EWRAM.

### Paralelismo

As duas frentes correm juntas desde o começo:

- **Frente A, validação de 1 a 4:** T1 a T9 sobre o que já existe. Não depende de
  nada da Unova.
- **Frente B, Unova:** blocos 0 e 1 do escopo.
- **No fim, frente C:** T10 mais uma revisão que roda tudo junto.

A frente A acha bug no que já está pronto enquanto a B constrói o que falta.
Cada uma com faixa de flag própria e exclusiva, porque agentes em paralelo já
colidiram em faixa de flag hoje.

---

## 11. Kanto nunca esteve na ROM (achado de 05/08/2026)

O achado mais caro da sessão, e o mais mal medido antes dele.

### O sintoma

Liguei o começo do jogo em Pallet Town. O leitor de EWRAM confirmou
`mapa=38.1 pos=6,6`, exatamente o destino pedido. **A tela veio preta, com só o
sprite do jogador.** Sprite é OAM e não depende de layout; o fundo é que não
existia.

### A causa, em três camadas

| camada | o que estava fechado | efeito |
|---|---|---|
| `src/data/tilesets/graphics.h:1986` | `#if IS_FRLG` em volta dos gráficos | 0 tileset de FRLG na ROM |
| `src/data/tilesets/headers.h:1037` | `#else` de `#if !IS_FRLG` | structs `Tileset` fora |
| `src/data/tilesets/metatiles.h:268` | `#else` de `#if !IS_FRLG` | metatiles fora |
| `tools/mapjson/mapjson.cpp:783` | `layout_version != "emerald"` → `continue` | **344 layouts descartados** |
| `tools/mapjson/mapjson.cpp:743` | `region != "REGION_HOENN"` → `invalid_maps` | **421 mapas descartados** |

Os dois filtros do `mapjson` existem no upstream porque lá se builda Emerald
**ou** FireRed. Aqui a ROM é uma só, com cinco regiões de propósito, então o
filtro jogava Kanto inteira fora **sem imprimir uma linha**.

Sinnoh e Johto escapavam por acidente: têm o campo `region` vazio, que cai no
padrão `REGION_HOENN`.

### Por que nenhum validador pegou

Porque **todos eles leem o JSON, não a ROM.**

- `valida_conectividade.py` andava `map_groups.json` e jurava que Kanto era
  alcançável de barco. O warp existia, a constante existia, o mapa não.
- A contagem de 1327 mapas era de entradas no JSON. Na ROM havia 906.
- `layouts.json` tinha 1305 layouts; `layouts.inc` gerado tinha 815. **A
  diferença de 490 nunca foi olhada por ninguém.**

Isso é o mesmo erro das cinco lições do handoff, numa camada nova: eu verifiquei
na camada do dado de entrada, não na camada da afirmação. A afirmação era "Kanto
está no jogo", e a única prova válida era abrir Kanto no emulador.

**Regra que sai daqui: todo validador precisa de um par que leia o artefato
construído.** Contar linha de JSON não prova nada sobre a ROM.

### O conserto: sete camadas, não uma

Cada camada só aparecia depois de abrir a anterior. Nenhuma delas imprimia
aviso; todas simplesmente deixavam Kanto de fora.

| # | onde | o que fechava | como apareceu |
|---|---|---|---|
| 1 | `graphics.h:1986` | `#if IS_FRLG` nos gráficos de tileset | 0 símbolo de tileset FRLG na ROM |
| 2 | `headers.h:1037` | `#else` de `#if !IS_FRLG` | structs `Tileset` fora |
| 3 | `metatiles.h:268` | `#else` de `#if !IS_FRLG` | erro de compilação `gMetatiles_*_Frlg undeclared` |
| 4 | `mapjson.cpp:783` | `layout_version != "emerald"` | 344 layouts descartados calados |
| 5 | `mapjson.cpp:743` | `region != "REGION_HOENN"` | 421 mapas descartados calados |
| 6 | `flags.h:2158` a `2347` | 190 `FLAG_HIDDEN_ITEM_*` valendo `0` | montador aborta 182 vezes com "flag 0 is too small" |
| 7 | `event_scripts.s:770` | `.if IS_FRLG` nos 418 includes de script | 417 `undefined reference to *_MapScripts` |
| 8 | 4 arquivos de `object_events/` | `#if IS_FRLG` nos sprites | 124 dos 129 sprites usados por Kanto sem gráfico, em 1649 objetos |

A camada 8 é a mais perigosa das oito, porque **não dá erro de compilação**: id
de sprite sem gráfico faz o jogo reiniciar na tela de título. É exatamente o
crash que já custou duas sessões, esperando em 1649 objetos.

### O que a camada 6 obrigou a decidir

As 190 flags de item escondido de Kanto valiam `0` porque, numa build Emerald,
Kanto não existia. Para valerem, `FLAGS_COUNT` tem que crescer, e crescer
`flags[]` empurra tudo depois dele no SaveBlock1 e **invalida save**.

**Feito agora, de uma vez, e de propósito.** É a única janela em que sai de
graça: o Gui ainda não começou as 50 horas, e o requisito dele é que a save
sobreviva a partir do momento em que ele começar. A reserva de Unova (467 flags
para 334 item balls e 133 escondidos) entrou junto, no mesmo crescimento, porque
fazer duas vezes custaria a save.

```c
#define FLAG_HIDDEN_ITEMS_FRLG_START  (DAILY_FLAGS_END + 1)
#define NUM_HIDDEN_ITEMS_FRLG         0xBE   // 190, Kanto
#define FLAG_ITEMS_UNOVA_START        (FLAG_HIDDEN_ITEMS_FRLG_START + NUM_HIDDEN_ITEMS_FRLG)
#define NUM_ITEMS_UNOVA               0x1D3  // 467, Unova
```

Depois disto, `guarda_save.py --gravar` fixa a nova linha de base, e a promessa
passa a valer para sempre.
