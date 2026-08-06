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
