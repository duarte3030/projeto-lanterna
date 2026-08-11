# O que a importação de NPC de Sinnoh deixou para trás

Gerado a partir de `python3 dev_scripts/importa_npcs_sinnoh.py` (só relata) na
madrugada de 05/08/2026. Números conferem com o `resumo:` que o script imprime.

## O que entrou

| medida | valor |
|---|---|
| mapas de Sinnoh nossos | 162 |
| casados com um `MAP_HEADER` do Platinum | 152 |
| mapas que receberam evento novo | 142 |
| **NPC novos** | **591** |
| **placas novas** | **425** |
| sprites trocados por equivalente | 284 |

Antes disso Sinnoh inteira tinha 528 objetos. `dev_scripts/completude.py`
passou a medir Sinnoh contra o pokeplatinum em vez de `fontes-mapas/sinnoh`,
que tinha zero NPC de Sinnoh e por isso imprimia "fonte 0".

## 0. Os 382 NPCs que nasceram duas vezes (11/08/2026)

Aqueles 528 objetos que Sinnoh já tinha **não eram outra gente**: eram a MESMA
gente do Platinum, escrita à mão por sessões anteriores a partir da lista de
eventos da fonte. O importador trouxe todos de novo, e desde a leva de texto de
11/08 os dois pares falam. Medido: **382 pares**, em 90 mapas.

A prova de que os dois são a mesma pessoa não é distância no mapa (para mapa de
rua a coordenada importada é PROPORCIONAL, então dois NPCs iguais podem ficar a
50 tiles um do outro e ainda ser o mesmo sujeito). São três canais de NOME, cada
par por exatamente um deles:

| pares | prova |
|---|---|
| 186 | **nome de treinador**. O nativo tem `trainerbattle TRAINER_SINNOH_X` e o objeto importado corresponde, POR ORDEM, ao objeto do Platinum cujo `script` é `TRAINER_X`. Casamento de nome próprio, não de aparência |
| 127 | **nome de LOCALID**. O `local_id` nativo termina no LOCALID do Platinum (`LOCALID_ROUTE222_SAILOR_LUTHER` contra `LOCALID_SAILOR_LUTHER`): quem escreveu à mão copiou o nome da fonte |
| 69 | **sprite único dos dois lados**, depois de os dois canais acima consumirem todo o resto do mapa: sobrou exatamente um nativo e exatamente um importado daquele gráfico |

O casamento importado → objeto do Platinum é por **ordem**: o importador percorre
`object_events` da fonte na ordem e só filtra, então o k-ésimo importado é o
k-ésimo sobrevivente do filtro. Conferido em 309 mapas, **307 alinham gráfico a
gráfico**; os 2 que não alinham (`OreburghMine_B2F` e `Route205_North`) ficaram
inteiros de fora.

**Quem perde o par**, e por quê (o critério é CONTEÚDO, não origem):

- 215 vezes o importado é **mudo** (`script: "0"`) e o nativo fala ou luta: some
  o importado. É aqui que caem os 186 treinadores, porque treinador do Platinum
  entra com `script: "0"` e `TRAINER_TYPE_NONE` (o `script` dele na fonte é a
  constante `TRAINER_*`, que não é índice de texto). **Esconder o nativo neles
  apagaria 186 batalhas e deixaria 186 bonecos mudos no lugar.**
- 165 vezes o nativo é só um `msgbox` de fala inventada e o importado carrega o
  texto de verdade do Platinum: some o nativo.
- 2 vezes o nativo tem MENU e o importado tem texto, e aí o nativo fica: o
  marinheiro Eldritch de Canalave (é a balsa entre regiões: T8.3, T8.5, T10.1,
  T10.2 e cinco casos de T86 passam por ele) e o marinheiro de Snowpoint (é o
  único acesso à Battle Zone, atrás de `FLAG_ELITE_SINNOH_VENCIDA`).

**Os dois marinheiros quase foram escondidos, e o que os salvou merece registro
(lição 4.1).** O detector de "script que faz mais do que falar" usava
`re.search(..., re.S)` com um lookahead `^\S.*::`, e com `re.S` o `.` casa quebra
de linha: o corpo do script terminava na primeira linha de comentário `@` no
começo da coluna, ou seja, em `lock` + `faceplayer`, e os dois marinheiros
passaram por "só fala". O delimitador certo é o rótulo inteiro
(`^[A-Za-z_][A-Za-z0-9_]*::?$`), porque rótulo de TEXTO tem UM dois-pontos e
rótulo de script tem dois. Depois disso, uma segunda varredura independente (por
lista de comandos de risco) confirmou zero entre os 165 escondidos.

Custo: **uma flag para os 382**, `FLAG_SINNOH_NPC_DUPLICADO`, no campo `flag` do
perdedor. **Zero índice movido, zero objeto apagado** (a save guarda índice de
objeto). Acesa uma vez em `EventScript_ResetAllMapFlags`
(`data/scripts/new_game.inc`). Reversível: apagar a flag traz os 382 de volta.

**31 pares suspeitos ficaram de pé**, todos em mapa onde sobrou mais de um NPC do
mesmo gráfico dos dois lados (2 nativos e 3 importados de PICNICKER, por
exemplo). Sem canal de nome não dá para dizer QUAL é qual, e a lição 4.10 vale:
na dúvida, os dois ficam. Os maiores são `OreburghCity` (MAN_4, 1 contra 4),
`HearthomeCity` (POKEFAN_M e POKEFAN_F, 1 contra 3 cada) e
`JubilifeCity_PokemonCenter_2F` (TEALA, 3 contra 3).

**Nenhum dos 165 nativos escondidos tem comando de risco no script.** Conferido
com dois passes independentes: nenhum é treinador, nenhum `local_id` é citado por
script de outro lugar (varredura em 8103 arquivos de `data/` e `src/`), e nenhum
corpo tem `goto`, `call`, `warp`, `setflag`, `applymovement`, `special` ou coisa
parecida. Esconder objeto só LIBERA passagem, nunca fecha, então não há risco de
trancar caminho; o que pode mudar é roteiro de teste que contava com um NPC
BLOQUEANDO o passo. Os casos que atravessam Canalave a pé (T8.3, T8.5, T10.1,
T10.2, T86.8 a T86.12) precisam ser re-rodados na próxima build.

## 1. Todo NPC importado é mudo, e toda placa diz a mesma coisa

No Platinum o campo `script` é um índice numérico dentro do arquivo de scripts
do mapa, e o texto mora num banco de mensagens separado. Nenhum dos dois
atravessa para o formato de rótulo do pokeemerald. Então:

- os 591 NPC entram com `script: "0"`: dá para esbarrar neles, não para
  conversar. `trainer_type` foi forçado para `TRAINER_TYPE_NONE`, senão a
  batalha começaria contra um time vazio.
- as 425 placas apontam todas para `Sinnoh_EventScript_PlacaImportada`
  (`data/scripts/sinnoh_placas.inc`), que responde "The lettering has faded with
  age."

**Para fechar:** portar os bancos de texto de Sinnoh, ou escrever falas próprias
mapa a mapa. Cidade com gente muda é melhor que cidade vazia, mas não é o fim.

## 2. 71 personagens ficaram de fora por não ter sprite

Sprite de líder, de Galáctica com nome e de Pokémon não existe nesta build, e
trocar por genérico faria o mapa mentir (Byron com cara de nadador). Ficaram de
fora, por contagem:

```
 8 LOOKER      5 CYNTHIA     5 PACHIRISU   4 GARDENIA    4 CYRUS
 4 BUNEARY     4 JUPITER     4 CRASHER_WAKE 3 BUCK       3 MARS
 3 ROARK       3 MAYLENE     2 FLINT       2 SATURN      2 MESPRIT
 2 JASMINE     2 CANDICE     1 CHERYL      1 VOLKNER     1 PALMER
 1 AZELF       1 UXIE        1 CHARON      1 CROAGUNK    1 BYRON
 1 SHAYMIN     1 MARLEY      1 DRIFLOON
```

**Bloqueado por arte.** A lista viva é `NOMES_PROPRIOS` em
`dev_scripts/importa_npcs_sinnoh.py`; assim que existir sprite, tirar de lá e
rodar de novo.

## 3. 230 objetos com `hidden_flag` não vieram

Os `FLAG_HIDE_*` do Platinum não existem aqui, e objeto com flag inexistente
nasce sempre. Quem nasce escondido é NPC de história: grunt da Galáctica
trancando estrada, lendário de lago, Barry aparecendo depois de um gatilho.
Trazer isso sem a flag põe **bloqueio permanente** no caminho do jogador, então
a política é não trazer.

**A faixa `0x294`-`0x2AB` (24 flags, de `dev_scripts/flags_livres.py`) fica
RESERVADA e intacta.** Decisão confirmada em 05/08/2026: gastar flag agora não
resolve nada, porque o que remove o NPC da estrada é a CENA, não a flag. Trazer o
grunt da Galáctica de volta com uma flag que nada acende tranca a estrada para
sempre, que é exatamente o que as 39 pedras de Strength fizeram com uma caverna
de Unova.

**Para fechar:** a flag só se gasta junto com o script que a acende. Portar a
cena, acender a flag no fim dela, e só então trazer o objeto.

## 4. 84 `coord_events` (gatilhos) não vieram

Gatilho do Platinum é `{script, var, value}`, e tanto o script quanto a var
(`VAR_JUBILIFE_CITY_STATE` e afins) não existem aqui. Importar o gatilho sem
eles daria erro de compilação, e importar com var inventada daria gatilho que
nunca dispara. Ficaram de fora inteiros.

## 5. Posição é aproximada nos mapas de rua

Mapa de rua no Platinum usa coordenada GLOBAL da matriz de Sinnoh (Jubilife
começa em x=140, z=743), e os nossos layouts de Sinnoh **não são** os do
Platinum. Medido: o delta entre o mesmo NPC nos dois lados varia de (89,724) a
(164,732) dentro do mesmo mapa, ou seja, não existe offset que alinhe.

O importador coloca o NPC de rua por **proporção** da caixa da matriz sobre o
nosso layout e depois empurra para o tile livre mais próximo. A posição relativa
se mantém (quem estava no centro fica no centro); a exata, não. Interior entra
com a coordenada igual, porque lá ela já é local.

## 6. 10 mapas nossos sem par no Platinum

```
FloaromaTown_FlowerShop        SinnohLeague_AaronsRoom
JubilifeCity_Flat1_F3          SinnohLeague_BerthasRoom
JubilifeCity_Flat2_F3          SinnohLeague_ChampionsRoom
JubilifeCity_Flat3_F3          SinnohLeague_FlintsRoom
                               SinnohLeague_HallOfFame
                               SinnohLeague_LuciansRoom
```

As salas da Liga têm par (`MAP_HEADER_POKEMON_LEAGUE_AARON_ROOM` etc), mas foram
deixadas de fora de propósito: quem mora nelas é a Elite dos Quatro, que
`dev_scripts/porta_ginasios_sinnoh.py` já colocou. Os andares `_F3` e a floricultura
não têm equivalente no Platinum.

## 7. Falta o resto do mapa de Sinnoh

`completude.py --detalhe Sinnoh` mostra 25,6% dos mapas. O que falta não é NPC:
são os próprios mapas (Great Marsh, Turnback Cave, Battle Frontier, Distortion
World, as lojas de Veilstone, os andares de hotel). Enquanto o mapa não existir
aqui, os NPC dele não têm onde entrar.

## Como refazer

O importador é idempotente: cada evento que ele grava leva `"origem":
"pokeplatinum"`, e mapa que já tem a marca é pulado inteiro. Rodar `--aplicar`
duas vezes não dobra a população.

```
python3 dev_scripts/importa_npcs_sinnoh.py              # relata, não escreve
python3 dev_scripts/importa_npcs_sinnoh.py --aplicar
python3 dev_scripts/valida_mapas_sinnoh.py --so-sinnoh  # sprite: 0 e fora: 0
python3 dev_scripts/testa_critico.py T50                # prova na ROM
```

---

## 8. As portas de cidade, 06/08/2026

`dev_scripts/fecha_portas_sinnoh.py` fechou 98 portas de cidade mais 14 andares
de cima: **112 interiores novos**. Sinnoh saiu de 25,8% para **44,6%** dos
mapas e de 61,4% para **90,8%** dos warps.

**O que é convertido de verdade e o que é reaproveitado.** Do pokeplatinum
vieram 368 NPCs, 98 placas e 101 textos (de placa e de NPC), pela corrente
índice, `ScriptEntry`, banco de texto que o `texto_placas_sinnoh.py` já
percorria. A **planta** de cada interior é reaproveitada de interior que o repo
já tem: `OreburghCity_House1`, `OreburghCity_Mart`,
`OreburghCity_PokemonCenter_1F` e `_2F`, `OreburghCity_Flat1_F2`,
`Route208_Access`. Cada `map.json` novo diz qual, no campo `origem`.

O motivo de não converter a planta: `demake_ds.py` lê do DS só colisão e
comportamento de tile, não o desenho. Interior convertido por ele sai como sala
de chão liso cercada de árvore, sem parede, sem balcão e sem porta.

**O warp não sai da coordenada deles.** Coordenada de warp de rua no Platinum é
global da matriz de Sinnoh e não existe offset contra os nossos layouts (mesma
armadilha da decisão 1 do importador de NPC). O warp novo vai em cima de um tile
que **já é porta aqui**, achado lendo `metatile_attributes.bin` com a mesma
lista de comportamentos que o motor usa. Resultado medido: os 217 warps novos
disparam **100%**.

### O que ficou de fora, e por quê

| quanto | o quê | por quê |
|---|---|---|
| 18 | casa de Canalave, Celestic, Solaceon, Sunyshore, Jubilife | a cidade tem menos tile de porta órfã do que o Platinum tem prédio. Abrir mais exige **desenhar porta no `map.bin` da cidade**, e escolher o metatile errado põe porta em cima de parede ou de telhado |
| 18 | `POKECENTER_B1F` | é a sala de troca subterrânea da gen 4 (Wi-Fi/Union). O arquétipo de centro Pokémon do repo tem **uma** escada, e ela foi para o 2F |
| 51 | caverna, ruína, Victory Road, andares de Mt. Coronet, Lost Tower, Old Chateau, lago | não é interior de cidade. Reaproveitar casa de 8x9 aqui mentiria o mapa; estes precisam de geometria de verdade |
| 5 | andares de mapa `UNUSED_*` | o andar de baixo também não tem escada sobrando |

Nenhuma flag da faixa 0x8E5 a 0x920 foi gasta: NPC importado nasce sem flag.

## 9. As portas que faltavam desenhar, 06/08/2026

`dev_scripts/abre_portas_extras_sinnoh.py` fechou **28 dos 39** destinos que a
leva anterior deixou sem porta: os 18 `POKECENTER_B1F` e 10 prédios de cidade.
Sinnoh foi de 44,6% para **49,3%** dos mapas e de 90,8% para **95,4%** dos
warps; a taxa de warp que dispara de verdade em Sinnoh subiu de 86,0% para
**95,6%**.

**O que mudou de método.** A leva anterior só usava porta que já estava
desenhada no `map.bin`. Esta desenha a porta que falta, e a regra que a torna
segura é uma só: **o tile novo é a palavra de 16 bits copiada de outro warp do
mesmo mapa**. Nada de metatile escolhido de cabeça. Assim o desenho, a colisão,
a elevação e o comportamento já são os de uma porta que o motor aceita, e a
porta nasce disparando.

- **Centro Pokémon:** os quatro layouts de centro do repo têm a mesma planta, com
  a escada do 2F em (1,6) colada na parede oeste. A escada do B1F entra em
  (13,6), o espelho dela na parede leste. Isso só é legítimo porque
  `LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F` é usado por 15 mapas e **os 15 querem
  um B1F**: nenhum deles fica com escada morta. O autoteste do script trava se
  essa conta mudar.
- **Cidade:** a porta só entra no rodapé de um bloco conexo de tiles bloqueados
  que não encosta na borda (senão é o paredão que cerca a cidade), tem área >= 6
  (senão é árvore 2x2), preenche 60% da própria caixa (senão é penhasco ou
  cerca) e tem fachada de 3 tiles seguidos com chão logo abaixo. Sem essas
  contas a coluna x=20 de Canalave, que é uma cerca, ganhava porta.

### Os 11 que continuam de fora

| quanto | o quê | por quê |
|---|---|---|
| 3 | casas de Celestic | a cidade é uma cratera: os blocos bloqueados dela são parede de pedra, nenhum passa no teste de prédio |
| 2 | casas de Solaceon | só um prédio sem porta na cidade, e ele foi para o Pokémon News Press |
| 1 | `SUNYSHORE_CITY_EAST_HOUSE` | idem, nenhum bloco passa no teste |
| 1 | `RESORT_AREA_RIBBON_SYNDICATE_1F` | idem |
| 4 | `ETERNA_CITY_CONDOMINIUMS_2F`, dois `UNUSED_*_3F`, `ROTOMS_ROOM` | precisam de escada dentro de um layout COMPARTILHADO com mapa que não sobe (a planta de casa é usada por 64 mapas; a do `TeamGalacticEternaBuilding_1F` é a do Weather Institute, de HOENN). Fechar exige clonar o layout, não desenhar tile |

## 10. As cavernas, geometria convertida de verdade, 06/08/2026

`dev_scripts/converte_cavernas_sinnoh.py` trouxe **10 cavernas com a planta
convertida do DS**, não reaproveitada: Wayward Cave 1F (96x64), Mt. Coronet 2F,
Mt. Coronet 1F Tunnel Room, Lake Valor Drained, as cavernas de Verity, Valor e
Acuity, Ruin Maniac Cave, Snowpoint Temple 1F e Victory Road 1F Room 3. Sinnoh
foi de 49,3% para **51,0%** dos mapas.

**Aqui o `demake_ds.py` funciona, e o motivo importa.** Para casa ele falha
porque parede, balcão e porta são desenho de tileset e não estão na grade. Para
caverna não falha, porque **a geometria de uma caverna É a colisão dela**: o
labirinto de Wayward Cave sai inteiro, com os corredores e as câmaras no lugar.
Conferido tile a tile contra a fonte.

Três leituras que o script precisou fazer e que não estavam no `demake_ds.py`:

- **`0x00` sem bit de colisão é VAZIO, não chão.** São 15 mil tiles nos mapas
  desta leva: a área que o modelo 3D da gen 4 nem desenha. Traduzir como chão
  encheria a caverna de salão. Vira rocha.
- **A rocha tem duas faces.** Metatile 753 é a pedra vista de cima e 761 é a
  face que aparece quando há chão logo abaixo (752/754 e 760/762 são as pontas).
  Os números saíram medidos de `MtCoronet_1F_South` e `MtCoronet_B1F`, que já
  estavam no repo, não de tabela de tileset lida de cabeça.
- **A boca da caverna da gen 4 é um bolsão solto na grade.** Nas três cavernas
  de lago o tile de warp da fonte tem os QUATRO vizinhos de pedra: a passagem
  até a câmara é desenhada no modelo 3D e a grade 2D não a liga. O script
  calcula a maior mancha andável conexa e, se o warp cair fora dela, empurra
  para o tile mais próximo que esteja dentro. Sem isso, quatro dos dez mapas
  entregavam o jogador preso numa fresta.

### O que ficou de fora, e por quê

| quanto | o quê | por quê |
|---|---|---|
| 12 | Old Chateau, Solaceon Ruins, Rock Peak Ruins, Maniac Tunnel, Iceberg Ruins, Mt. Coronet 6F, Lake Verity/Acuity Low Water | **a geometria está convertida e confere**, mas o mapa pai não tem tile de porta órfã para a entrada, e desenhar boca de caverna em Eterna Forest ou nas margens de lago cairia em cima de árvore. Caverna sem entrada é peso morto na ROM, então não entra |
| 1 | `FLOAROMA_MEADOW` | está marcado `MAP_TYPE_CAVE` no Platinum mas é o prado das colmeias: a grade dá 4 tiles andáveis em 4096. Seria caverna falsa |
| 1 | `VICTORY_ROAD_1F` | `MAP_VICTORY_ROAD_1F` já existe: é a Victory Road de HOENN. Precisa de outro nome de constante |
| 27 | elevador, sala de ginásio, andar de loja, estúdio da Jubilife TV, Great Marsh, Amity Square, Pal Park, Battle Frontier | não são caverna: têm mobília e piso desenhados, exatamente o caso em que a grade 2D não basta |

## 11. As bocas de caverna, 06/08/2026

`dev_scripts/abre_bocas_cavernas_sinnoh.py` abriu a entrada que faltava e
`converte_cavernas_sinnoh.py` criou **36 cavernas** com a planta convertida do
DS. Sinnoh foi de 51,0% para **57,1%** dos mapas. O script não cria mapa nenhum:
ele só desenha o tile de entrada no mapa pai, e quem cria continua sendo o
conversor.

**A boca nasce de dois jeitos, e a diferença sai do dado.**

- **Pai também convertido da grade 2D do Platinum** (Mt. Coronet 2F, Wayward
  Cave 1F, Snowpoint Temple 1F, Victory Road 1F Room 3): os dois lados são a
  mesma grade, então a coordenada da fonte vale aqui **tile a tile**. A escada
  entra na coordenada exata do warp deles, conferida andável.
- **Pai de outra geometria** (rota, cidade, floresta, margem de lago):
  coordenada de rua no Platinum é global da matriz de Sinnoh e não tem offset
  que alinhe. A posição sai por **âncora**: o mesmo mapa já tem warp para um
  destino que o Platinum também tem (Route214 → Ruin Maniac Cave Short,
  Solaceon → a creche), e o delta entre os dois pares dá a translação local.

O tile só vira boca se, medido no nosso `map.bin`, estiver **bloqueado hoje**,
tiver **chão andável logo abaixo** e tiver os vizinhos de cima, esquerda e
direita **também bloqueados**: é o meio de uma parede, não a quina de uma árvore
solta. Mancha com `MB_MOUNTAIN_TOP` ganha das outras, que é penhasco.

A palavra de 16 bits é a **porta de caverna do próprio mapa**, nunca a seta de
portaria: em Route214 a seta era a porta mais comum e a boca saía com desenho de
escada de prédio. `--redesenha` refaz essa escolha nas bocas já abertas, e não
encosta em caverna nem em pai convertido, onde o 519 do tileset de caverna já é
a boca certa.

`SpearPillar` divide layout com o Sky Pillar de HOENN: o layout foi **clonado** e
só a cópia foi furada.

**Abrir uma boca revela a próxima.** Foram sete voltas de boca mais conversão:
os sete quartos das Solaceon Ruins, os cinco andares do Snowpoint Temple, as
sete salas do Old Chateau, Mt. Coronet 3F a 6F, as duas salas de Victory Road.
Os 75 warps das 46 cavernas do grupo disparam todos.

## 12. O teto de 128 mapas por grupo, 06/08/2026

Achado provando as portas no emulador, e é a coisa mais importante deste
documento: **`struct WarpData` guarda `s8 mapGroup` e `s8 mapNum`**
(`include/global.h`). Mapa de índice 128 dentro de um grupo vira -128 no warp, o
jogo carrega lixo e **reseta**.

Medido tile a tile: o índice 127 de `gMapGroup_IndoorSinnohPortas` entra, o 128
derruba o jogo. Uma cópia byte a byte de uma casa que funciona também derruba se
entrar acima de 127, o que descarta conteúdo do mapa como causa. O grupo tinha
153 mapas, então **26 estavam mortos**, 14 deles da leva anterior, todos com
warp que `valida_warp_tile.py` dava por bom: comportamento de porta é condição
necessária, não suficiente.

- o grupo foi partido em `gMapGroup_IndoorSinnohPortas` (128) e
  `gMapGroup_IndoorSinnohPortas2`, no fim de `group_order`. Nenhum índice
  alcançável andou, e a save continua compatível;
- `fecha_portas_sinnoh.grupo_com_vaga` escolhe o grupo daqui em diante, e abre o
  próximo sozinho quando o atual enche. Os três scripts que criam mapa usam ela;
- `antes_de_empurrar.sh` recusa grupo acima de 128 e mais de 128 grupos, que é o
  mesmo campo. **Hoje são 126 grupos: sobram 2.** Região nova precisa caber
  neles ou reaproveitar grupo existente.

### As 11 portas teimosas, no mesmo dia

`dev_scripts/abre_portas_teimosas_sinnoh.py` fechou os 11 destinos que sobravam:
3 casas de Celestic, 2 de Solaceon, a casa leste de Sunyshore e o Ribbon
Syndicate pelo **teste de parede** (Celestic é uma cratera, nenhum bloco dela
passa no teste de prédio), e `ETERNA_CITY_CONDOMINIUMS_2F`, os dois `UNUSED_*_3F`
e `ROTOMS_ROOM` **clonando o layout** antes de desenhar a escada, porque a planta
de casa serve 74 mapas e a do `TeamGalacticEternaBuilding_1F` é a do Weather
Institute, de HOENN. Mais duas voltas trouxeram o 3F e o 4F dos condomínios.

A palavra de porta passou a ser procurada pelo **par de tilesets** quando o
próprio mapa não tem nenhuma para copiar: casa comum só tem o capacho de saída,
que é seta e não dispara por cima.

Sinnoh: 57,1% para **59,3%** dos mapas.

### Terceiro bug de ferramenta

`DebugAction_Util_Warp_SelectWarp` (src/debug.c) **não trata LEFT nem RIGHT**: o
campo do warp fica sempre na unidade e é clampado em 10. `testa_critico.py`
mandava LEFT e RIGHT achando que era campo de três dígitos, então pedir o warp
10 entrava o warp 1, e a casa leste de Sunyshore reprovava com a porta certa.
`digita_warp` conserta, e o T55.6 guarda contra a volta.

---

## 13. Os treinadores de masmorra, prédio e ginásio, 11/08/2026

`dev_scripts/treinadores_masmorra_sinnoh.py` ligou **105 objetos (103
treinadores) em 22 mapas** de Sinnoh que não são rota. Fecha a metade
não-rota do buraco descrito na seção 1: o campo `script` do Platinum é um
índice de texto **ou** a constante `TRAINER_*`, e `importa_npcs_sinnoh.py` só
sabia ler a primeira, então todo treinador entrou aqui mudo, com
`TRAINER_TYPE_NONE`.

**Os oito ginásios de Sinnoh tinham só o líder.** Medido antes de acrescentar:
os oito têm `trainerbattle` do líder e a insígnia (`FLAG_INSIGNIA_SINNOH_*`)
desde a leva de `porta_ginasios_sinnoh.py`, e os treinadores de dentro estavam
todos com `script: "0"`. Nenhuma batalha de líder foi refeita.

**Zero id novo, zero constante nova, zero flag, zero var, zero objeto.** A faixa
de id 2550-2749 que esta frente recebeu **continua livre**, e o motivo é medida,
não economia: os **425 `TRAINER_SINNOH_*` já estavam declarados** (855 a 1315) e
os 425 **já tinham bloco em `src/data/trainers.party`**. Criar id novo para eles
duplicaria time e texto na ROM e daria duas flags de "já venci" para a mesma
pessoa. `trainers.party` e `opponents.h` não foram tocados. A flag de derrotado
é derivada de `TRAINER_FLAGS_START` pelo próprio motor.

**Reusa o boneco mudo em vez de criar objeto.** A save guarda índice de objeto,
então objeto novo só entraria no fim da lista e o mudo continuaria de pé ao lado
do treinador, em dobro. `guarda_save.py` diz SAVE COMPATIVEL e os 1895 mapas
seguem 1895.

De onde sai cada campo, medido na fonte:

| campo | fonte |
|---|---|
| quem é treinador | `events_<mapa>.json`, objeto cujo `script` é `str` e começa com `TRAINER_` |
| raio de visão | `data[0]` do mesmo objeto. Sem `data` o raio é 0, e o Platinum tem 7 assim: lutam quando falam com eles |
| direção | `movement_type` da fonte, `LOOK_SOUTH/NORTH/WEST/EAST` -> `FACE_DOWN/UP/LEFT/RIGHT` |
| fala de antes, de derrota e de depois | `res/trainers/data/<slug>.json`, `messages`, tipos `TRMSG_PRE_BATTLE`, `TRMSG_DEFEAT`, `TRMSG_POST_BATTLE`. **Não é o banco de texto do mapa**: em gen 4 o motor cuida do treinador sozinho e a fala mora junto com o time dele |

**Direção só se porta quando a coordenada bate.** Medido: 90 dos 103 estão no
`x`/`z` exato da fonte (caverna de geometria convertida e ginásio de planta
própria). Nos 13 de planta REAPROVEITADA (sala de treinador do ginásio de
Hearthome, salas de Sunyshore, Oreburgh Gate, Café) o importador teve que
reposicionar, e ali "virado para oeste" aponta para outra parede: esses 27
objetos ficam com o `LOOK_AROUND` que o importador deixou, que enxerga girando.

**Batalha dupla: os dois bonecos apontam para o MESMO `EventScript`.** No
Platinum o par (`TRAINER_DOUBLE_TEAM_AL_AND_KAY` na Victory Road 2F e
`..._JO_AND_PAT` na B1F) é dois objetos com a MESMA constante. Aqui os dois
apontam para o mesmo `trainerbattle_double`, então encostar em qualquer um dos
dois começa a mesma batalha e, depois dela, os dois falam o texto de depois.
Dar id próprio ao parceiro criaria uma batalha que a fonte não tem; deixá-lo
mudo deixaria um boneco calado colado no treinador.

### O que ficou de fora, e o motivo medido

| quanto | o quê | por quê |
|---|---|---|
| 242 | os treinadores das 37 rotas de Sinnoh | outra frente, rodando em paralelo |
| 13 | 8 de `EternaForest` | o objeto importado está escondido por `FLAG_SINNOH_NPC_DUPLICADO` e quem luta é o nativo, que já tem a batalha. **Recusar aqui é o certo**: ligar o clone poria dois do mesmo treinador no mapa |
| 10 | `GalacticHQ_1F`/`_2F`, `MtCoronet3F`/`4F`/`5F`/`6F`, `TeamGalacticEternaBuilding_3F` | o objeto nem chegou a ser importado: `hidden_flag` do Platinum, sprite proibido ou nome próprio sem arte (seções 2 e 3) |
| 3 | `OreburghMine_B2F` (2) e `StarkMountainOutside` (1) | alinhamento. São exatamente os dois casos que a seção 0 já registrava: `OreburghMine_B2F` é um dos 2 mapas em 309 que não alinham gráfico a gráfico, e `StarkMountainOutside` é exterior de "passagem provisoria", que entrou sem NPC de propósito |
| 3 | grunts de `LakeValorDrained`, `MtCoronet1FTunnelRoom`, `ValleyWindworksBuilding`, `TeamGalacticEternaBuilding_1F` | a constante **já está em uso** noutro mapa: a frente da Galáctica pôs esses grunts no mapa de fora. Reusar a mesma constante daria duas pessoas com a mesma flag de derrotado |

**Custo de ROM: 25,7 KB** (21.620 B de `.string` mais 4.738 B de script, com
`trainerbattle` a 40 B, `msgbox` a 5 e `end` a 1), contra 1,56 MB livres.

`completude.py` não se move com esta leva, e isso está certo: ela conta mapa,
objeto, warp e placa, e nenhum objeto novo foi criado. O número que mudou é
outro: as constantes de treinador de Sinnoh que algum `trainerbattle` cita
foram de **249 para 352**.
