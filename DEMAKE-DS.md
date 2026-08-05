# Demake de mapa de DS para GBA: o que dá para automatizar

Tudo aqui foi medido nos arquivos em 04/08/2026, não lembrado. Onde a
documentação da comunidade discorda do binário, o binário ganha e a divergência
está anotada.

**Conclusão curta:** a ideia de que mapa de DS "é modelo 3D e não converte" está
errada. As duas gerações guardam, ao lado do modelo, uma grade 2D de 32x32 tiles
com colisão e terreno. Para a gen 4 a grade está totalmente decodificada e vira
`map.bin` do pokeemerald automaticamente. Para a gen 5 a grade existe e foi lida
em 1028 dos 1065 arquivos, mas só interiores saem corretos; o exterior de Unova
ainda não fecha.

Protótipo: `dev_scripts/demake_ds.py`. Rodar sem argumento faz o autoteste e
imprime origem e resultado lado a lado.

---

## 1. Gen 4 (Platinum) — formato fechado

Fonte primária: a decomp **pokeplatinum** em
`/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokeplatinum`. É código do
próprio jogo, então não é interpretação de terceiro.

### Planta do mundo

`res/field/matrices/map_matrix_000.json`, grade de 30 de largura por 27 de
altura, com três camadas paralelas:

| campo | conteúdo |
|---|---|
| `headers[y][x]` | lugar com nome, ex. `MAP_HEADER_TWINLEAF_TOWN` |
| `maps[y][x]` | pedaço de terreno, ex. `MAP_000` -> `map_data_000.bin` |
| `altitudes[y][x]` | altura da célula |

Exemplo conferido: `MAP_HEADER_TWINLEAF_TOWN` ocupa só a célula (3, 27) e usa
`MAP_000`; `MAP_HEADER_ROUTE_201` ocupa (3,26) e (4,26) com `MAP_005` e
`MAP_006`.

### Grade de tiles

`res/field/maps/data/map_data_NNN.bin`, 666 arquivos. Constantes vindas de
`include/constants/field/map.h`:

```
TERRAIN_ATTRIBUTES_OFFSET 0x10        offset da grade dentro do arquivo
TERRAIN_ATTRIBUTES_SIZE   0x800       2048 bytes = 32*32*2
MAP_TILES_COUNT_X / _Z    32          tamanho do pedaço
colisão                   bit 15      TERRAIN_ATTRIBUTES_COLLISION_MASK 0x8000
comportamento             bits 0..7   TERRAIN_ATTRIBUTES_TILE_BEHAVIOR_MASK 0xFF
```

Carregado por `TerrainAttributes_Load` em `src/terrain_attributes.c`, que lê
`(offset 0x10, tamanho 0x800)` de cada arquivo. Os nomes dos comportamentos
estão em `include/constants/field/map_tile_behaviors.h` (enum `TileBehavior`,
270 linhas): `TILE_BEHAVIOR_TALL_GRASS` = 0x02, `WATER_SEA` = 0x15,
`CAVE_FLOOR` = 0x08, `SAND` = 0x21, `JUMP_EAST` = 0x38, e assim por diante.

Medido nos 666 arquivos (682 mil tiles):

| comportamento | ocorrências | com bit de colisão |
|---|---|---|
| 0x00 (nenhum) | 582.450 | 330.825 |
| 0x15 água do mar | 40.385 | 124 |
| 0x08 chão de caverna | 16.141 | 30 |
| 0x02 grama alta | 10.141 | 0 |
| 0x0C chão de montanha | 6.781 | 1.172 |

Consequência prática, e é por isso que a ordem das regras no conversor importa:
**água na gen 4 não tem bit de colisão**. Quem impede de andar é o
comportamento, não o bit. Logo o conversor decide pelo comportamento primeiro e
só cai no bit 15 quando o comportamento é 0.

---

## 2. Gen 5 (Black 2) — formato aberto até certo ponto

Não existe decomp de Black 2 (conferido). Tudo abaixo saiu da ROM
`pokeemerald-expansion/black.nds` (cabeçalho `POKEMON B2`, código `IREO`),
desempacotada em `/tmp/claude-501/black_fs`.

### A cadeia até um lugar com nome

```
a/0/1/2  zonedata      615 registros de 48 bytes, um por zona
   +4  u16  ->  índice da matriz em a/0/0/9
   +22 u16  ->  id da própria zona (0..614, confere com a ordem)
   +26 u8   ->  índice do nome do lugar
a/0/0/2 arquivo 109    154 nomes de lugar ("Nuvema Town", "Castelia City", ...)
a/0/0/9  matrizes      416 arquivos: u32 tipo, u16 largura, u16 altura, células
   célula = u32, 0xFFFFFFFF = vazio, senão índice em a/0/0/8
   tipo 0 (414 arquivos): uma camada de células
   tipo 1 (2 arquivos):   duas camadas; a segunda são as pontes/nível de cima
a/0/0/8  mapas         1065 arquivos, o pedaço de 32x32 em si
```

Verificação de que o campo `+4` é mesmo a matriz: só existem duas matrizes
grandes (índices 0 e 175, ambas 29x27). Pelo campo `+4`, 76 zonas apontam para
elas, e os nomes dessas zonas são exatamente Striaton City, Nacrene City,
Nimbasa City, Driftveil, Mistralton, Icirrus, Opelucid, Pinwheel Forest, Desert
Resort, Chargestone Cave, Route 5, Route 6, Route 7... ou seja, o mundo aberto.
Pelo campo `+2` nenhuma zona aponta para elas. As outras 539 zonas usam matrizes
1x1 ou 2x2, que são os interiores.

A matriz 175 tem 277 células ocupadas, referenciando 187 pedaços distintos.

### O arquivo de mapa

Cabeçalho: `u32 magia`, depois N `u32` de offset, sendo o primeiro offset o
próprio tamanho do cabeçalho (dá para descobrir N sem tabela fixa).

| magia | letras | quantos | offsets | tem grade 32x32 |
|---|---|---|---|---|
| 0x00034257 | `WB` | 961 | 4 | 960 |
| 0x00044347 | `GC` | 60 | 5 | 60 |
| 0x00034452 | `RD` | 8 | 4 | 8 |
| 0x0002474E | `NG` | 36 | — | 0 |

O modelo 3D é um `BMD0` (NSBMD) na primeira seção. A seção da grade começa com
`u16 largura = 32, u16 altura = 32` e traz 1024 registros de 8 bytes. Alguns
arquivos têm registros de 8 bytes a mais no fim da seção (0 a 208 bytes extras,
sempre múltiplo de 8), conteúdo desconhecido.

Total: **1028 dos 1065 arquivos entregam a grade de 32x32**.

### Os 8 bytes por tile: o que se sabe e o que não se sabe

São 4 `u16`. Sobre 987.136 tiles do jogo inteiro:

| palavra | o que é | evidência |
|---|---|---|
| `u16[0]` | quase sempre 0 (938.995 de 987.136); valores esparsos como 0x2c formam linhas retas | não decodificado |
| `u16[1]` | id de terreno, 581 valores distintos, forma regiões grandes e coerentes dentro do pedaço (blocos retangulares, manchas) | claramente terreno, mas sem tabela de significado |
| `u16[2]` | **bit 0 = bloqueado** | provado, ver abaixo |
| `u16[3]` | 0x80 e 0x81 em 89% dos tiles, mais 0x84, 0x88, 0x24, 0x16, 0x40 e o flag 0x8000 | acompanha o `u16[2]` mas diverge em 5,5% dos tiles |

**Prova do bit de colisão:** desenhando `u16[2] & 1` de pedaços de interior
(arquivos 827, 937, 846, achados via zonas com matriz 1x1) sai a planta baixa
exata de um prédio: uma ilha de chão livre cercada de vazio, com móveis no meio.
Não é ruído, e a polaridade fica decidida (bit ligado = bloqueado). O mesmo
desenho no arquivo 0 dá uma praça de 20x26 com quatro prédios retangulares
dentro, e esse arquivo é a célula (24, 23) da matriz 175, ou seja, canto do
mapa-múndi.

**O que não fecha:** aplicando essa mesma regra aos 187 pedaços do mapa-múndi,
só 8,7% dos tiles ficam andáveis (20,0% com a regra alternativa
`(u16[3] & 0xFF) != 0x81`). Isso é baixo demais para rua de cidade e rota. O
histograma por célula: 148 das 277 células são 100% bloqueadas (pedaços de
enchimento, principalmente os índices 104, 106 e 204), e das restantes quase
nenhuma passa de 40% andável.

Leitura mais provável, e ainda não confirmada: os 8 bytes descrevem
altura/rampa por tile (o `u16[3]` com 0x80, 0x84, 0x88, 0x24, 0x40 cheira a
código de canto/inclinação), e a redução para um bit só é fiel onde o terreno é
plano, que é o caso dos interiores. Enquanto isso não fechar, pedaço de exterior
de gen 5 sai bloqueado demais.

### Divergência com a documentação da comunidade

O [B2W2 File System da Project Pokemon](https://projectpokemon.org/home/docs/gen-5/b2w2-file-system-r8/)
descreve `a/0/0/8` como "models" e `a/0/8/4` como "map layout tiles". O binário
diz outra coisa: `a/0/0/8` tem modelo **e** grade de colisão, e `a/0/8/4` tem só
21 arquivos, o primeiro começando com `RLCN` (NCLR de trás para frente, ou seja
paleta), portanto é gráfico e não layout. As entradas `a/0/1/2` (zonedata),
`a/1/3/3`, `a/1/3/6` daquela mesma tabela conferem: `a/0/1/2` é de fato a tabela
de zonas, e `a/1/3/3` / `a/1/3/6` são tabelinhas de 40 e 8 bytes, pequenas
demais para serem matriz.

Busca por documentação mais funda de gen 5 (formato do tile de 8 bytes) não
achou nada público além de tutoriais de "abra com o SDSME/Tinke". Os repositórios
citados no pedido não foram encontrados com material de formato de mapa.

### Texto da gen 5, de quebra

Para achar os nomes dos lugares foi preciso corrigir o decodificador de texto
que existia em `/tmp/claude-501/narc.py`. A chave certa para Black 2 é
**`chave(i) = (0x7C89 + 0x2983 * i) & 0xFFFF`**, girando 3 bits à esquerda a cada
caractere, e o offset de cada linha é **relativo ao início da seção**, não
absoluto. A chave inicial `0x7C89` foi achada por força bruta nos 65536 valores
(só uma chave produzia texto imprimível) e depois validada em 543 arquivos de
`a/0/0/3`, que saem em inglês legível.

---

## 3. Tabela de tradução usada no protótipo

Os metatiles não foram escolhidos por gosto: saíram de contar o que os 292
layouts de Sinnoh que já existem no repo usam (`data/layouts/*/map.bin` com
`primary_tileset` = `gTileset_GeneralSinnoh`) e de conferir o comportamento em
`data/tilesets/primary/general_sinnoh/metatile_attributes.bin`.

| origem | metatile | colisão | elevação | por quê |
|---|---|---|---|---|
| chão andável | 1 | 0 | 3 | bloco mais usado dos mapas de Sinnoh já feitos |
| caminho de terra | 289 | 0 | 3 | 2º mais usado |
| grama alta (gen4 0x02, 0x03) | 13 | 0 | 3 | comportamento `MB_TALL_GRASS`, 9.364 usos |
| água do mar (gen4 0x15) | 368 | 0 | 1 | `MB_OCEAN_WATER`, 17.594 usos |
| água parada (gen4 0x10, 0x13, 0x16, 0x17) | 161 | 0 | 1 | `MB_POND_WATER`, 3.890 usos |
| areia (gen4 0x21) | 289 | 0 | 3 | |
| bloqueado | 470/471/478/479 | 1 | 0 | árvore 2x2, alternando por paridade de x e y |

Formato de saída, igual ao pokeemerald: um `u16` por tile, 10 bits de metatile,
2 de colisão, 4 de elevação.

## 4. O que o protótipo prova de verdade

Rodando `python3 dev_scripts/demake_ds.py`:

1. **Gen 4, Twinleaf Town** (`map_data_000.bin`, achado pela matriz): sai a
   praça com quatro casas e o lago embaixo, com a água virando metatile de água
   e o bloqueio virando árvore. Origem e resultado batem tile a tile.
2. **Gen 5, arquivo 0** (célula 24,23 da matriz 175): sai a praça com quatro
   prédios, só andável e bloqueado.
3. **Gen 5, arquivo 827** (interior da zona 1): sai a planta baixa do prédio,
   com os móveis no meio da sala. É esse desenho que prova a regra de colisão.

O autoteste no fim do arquivo falha alto se qualquer uma dessas leituras
quebrar, e escreve os `map.bin` em `/tmp/claude-501/`.

O protótipo **não** registra nada em `data/layouts/layouts.json`,
`data/maps/map_groups.json` nem `data/event_scripts.s`, e não cria mapa no jogo.

## 5. O que ainda falta

**Gen 4** (o caminho está aberto, falta encanamento):

- Costurar as células da matriz num layout retangular único por lugar. A matriz
  dá o retângulo de graça (`headers[y][x]`), mas layout do pokeemerald tem borda
  e tamanho próprios.
- Escolher tileset secundário por lugar. Hoje os mapas de Sinnoh do repo usam
  `gTileset_PetalburgSinnoh`, `gTileset_Snowpoint`, `gTileset_CaveSinnoh` etc.
  Isso é decisão de arte, não de conversão.
- Tratar os comportamentos que o GBA não tem 1 para 1: rampa, ponte, escada,
  neve funda, degrau de pulo direcional (`JUMP_EAST` e companhia viram ledge do
  pokeemerald, que existe, mas precisa do metatile certo).
- Prédio na gen 4 é modelo 3D solto, não tile. O conversor entrega o buraco
  bloqueado onde o prédio está; a fachada tem que ser desenhada à mão.

**Gen 5** (tem pesquisa antes do encanamento):

- Fechar o significado dos 8 bytes para terreno inclinado. Sem isso, exterior de
  Unova sai bloqueado demais.
- Traduzir os 581 ids de terreno do `u16[1]`. Sem isso não há grama nem água na
  gen 5, só chão e parede.
- Descobrir quais células da matriz pertencem a qual zona. A zonedata aponta a
  matriz, mas não o retângulo dentro dela; hoje não dá para dizer "estas 6
  células são Castelia City" sem olhar a olho.
- Os 60 arquivos `GC` (cabeçalho com 5 offsets, provavelmente cidade) e os 8
  `RD` já são lidos porque a grade é achada procurando a seção que começa com
  32x32, mas não foram conferidos um a um. Os 36 `NG` não têm grade nenhuma.

**Fora do escopo de mapa, mas necessário para jogar:** warp, evento, script,
encontro selvagem, treinador. Nada disso está na grade de tiles.

## 6. Estimativa honesta de esforço

Nada aqui é promessa, é ordem de grandeza com base no que foi medido.

| trabalho | esforço |
|---|---|
| Gen 4: gerar `map.bin` de qualquer pedaço | **pronto**, roda hoje |
| Gen 4: costura matriz -> layout + registro no jogo, automatizado | 1 a 2 dias |
| Gen 4: acabamento à mão de prédio e detalhe, por lugar | ~1 a 3 h por lugar |
| Gen 5: fechar altura/rampa dos 8 bytes | incerto, 2 a 5 dias de engenharia reversa, e pode não fechar |
| Gen 5: tabela dos 581 ids de terreno | 2 a 4 dias, provavelmente semiautomático cruzando com as texturas do modelo |
| Gen 5: zona -> células da matriz | 1 dia se houver campo escondido, vários se for a olho |

**Unova inteira**, contando 615 zonas (76 de mundo aberto, 539 interiores):
mesmo com tudo resolvido, a conversão automática entrega colisão e nada mais.
Traduzir isso em mapa que pareça Unova de verdade, com fachada, telhado, placa e
detalhe, é trabalho de arte por mapa, não de script. Com o ritmo de ~1 a 3 h por
mapa dá algo entre **300 e 900 horas de acabamento**, e isso *depois* de a
pesquisa da gen 5 fechar.

O caminho mais barato, e é a recomendação: **começar por Sinnoh**, onde a
decomp já entrega tudo mastigado e o protótipo já funciona, e só voltar para
Unova quando o formato de altura da gen 5 estiver resolvido.

## Fontes

- Decomp pokeplatinum, arquivos `include/constants/field/map.h`,
  `include/constants/field/map_tile_behaviors.h`, `src/terrain_attributes.c`,
  `res/field/matrices/map_matrix_000.json` (fonte primária, código do jogo).
- ROM Pokémon Black 2 (`POKEMON B2`, `IREO`), arquivos `a/0/0/2`, `a/0/0/3`,
  `a/0/0/8`, `a/0/0/9`, `a/0/1/2`, `a/0/8/4` (medição direta).
- [Project Pokemon, B2W2 File System](https://projectpokemon.org/home/docs/gen-5/b2w2-file-system-r8/)
  para o mapa de nomes dos NARC. Usado como pista, e corrigido onde o binário
  discorda.
- Repo pokeemerald-expansion deste projeto: `data/layouts/layouts.json`,
  `data/layouts/*/map.bin`, `data/tilesets/primary/general_sinnoh/metatile_attributes.bin`,
  `include/constants/metatile_behaviors.h`.
