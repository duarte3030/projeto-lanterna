# Pendências da história de Johto

Escrito em 05/08/2026 pela sessão que portou do `fontes-mapas/hns` o arco da
Equipe Rocket no Slowpoke Well e o arco da Torre Rádio de Goldenrod. Tudo aqui é
coisa que **não** entrou, e o motivo. Quem orquestra decide o que vale a pena.

## 0. Flags: nenhuma pendente

As três flags que as cenas usam **já existiam** em `include/constants/flags.h`
quando esta sessão foi conferir (linhas 2505 a 2507), com exatamente estes nomes:

| Flag | Valor | O que faz |
|---|---|---|
| `FLAG_HIDE_AZALEA_TOWN_ROCKETS` | `FLAG_UNUSED_0x03D` | some com os dois Rockets de Azalea e com os quatro do poço depois que o PROTON cai |
| `FLAG_HIDE_GOLDENROD_ROCKETS` | `FLAG_UNUSED_0x03E` | some com todo Rocket do 2F ao 5F da Torre depois que o ARCHER cai |
| `FLAG_HIDE_GOLDENROD_RADIO_TOWER_1F_ROCKET` | `FLAG_UNUSED_0x03F` | some com o grunt que fica **em cima da escada** do 1F, depois que ele perde |

Nenhuma flag nova foi pedida e nenhuma var foi usada. Toda pergunta de
"isso já aconteceu?" que não precisava esconder objeto virou
`goto_if_defeated` na flag de treinador, que o motor grava sozinho.

**06/08/2026, o rival e o resto do esconderijo pediram 36 flags novas e ZERO
var**, todas aliadas em `include/constants/flags.h` na faixa `0x270`-`0x293`:
`FLAG_SILVER_NEW_BARK_DONE`, `FLAG_SILVER_HIDEOUT_DONE`, seis
`FLAG_HIDE_SILVER_*` (New Bark, Cherrygrove, Azalea, Burned Tower, Goldenrod,
Hideout B3F), `FLAG_MAHOGANY_TRAP_1..22` e `FLAG_MAHOGANY_ELECTRODE_1..6`.
Quem for aliar nome novo: a faixa `0x264`-`0x293` já tem dono, comece em
`0x294` e confira com
`grep -n "FLAG_UNUSED_0x29" include/constants/flags.h` antes.

## 1. Vagas de treinador: sobram 33 (era UMA quando isto foi escrito)

(Desatualizado. Em 05/08/2026 o teto subiu para **1400**; em 06/08/2026 o
contador está em **1367**, ou seja, sobram **33 vagas**. O número que importa é
o TETO `MAX_TRAINERS_COUNT_EMERALD`, não o contador em uso. Os 7 Rockets da
Torre Rádio listados abaixo cabem hoje, é só criar.)

`MAX_TRAINERS_COUNT_EMERALD` era 1330 e `TRAINERS_COUNT_EMERALD` foi de 1316 para
**1329**. Os 13 treinadores criados estão em `include/constants/opponents.h`, com
time em `src/data/trainers.party` (acervo em `src/data/trainers_johto.party`).

Consequência direta: **o hns tem 16 Rockets só na Torre Rádio, e couberam 9.**
Ficaram de fora, por falta de vaga e não por falta de texto:

- Torre 2F: dois grunts (`TRAINER_GRUNT_4`, `TRAINER_GRUNT_26` no hns).
- Torre 3F: um grunt (`TRAINER_GRUNT_8`) e o cientista `TRAINER_MARC`.
- Torre 4F: dois grunts (`TRAINER_GRUNT_9`, `TRAINER_GRUNT_28`) e o cientista
  `TRAINER_RICH`.

Para porta-los, subir `MAX_TRAINERS_COUNT_EMERALD` primeiro. **Subir o MAX mexe
no tamanho do saveblock**, então é decisão de quem orquestra, não de agente.

## 2. Arco de Mahogany: FEITO em 05/08/2026

Os três andares existem agora: `MahoganyHideout_B1F`, `_B2F` e `_B3F`. A planta
**não** veio do hns (que não tem o mapa) nem de layout emprestado de Hoenn: veio
do disassembly `pret/pokecrystal`, `maps/TeamRocketBaseB1F.blk` e irmãos,
convertida por `dev_scripts/demake_gen2.py`. São 15x9 blocos de gen 2 = 30x18
metatiles de gen 3, e as coordenadas de warp e de NPC do gen 2 caem 1 para 1 nos
metatiles de gen 3.

**A constante `MAP_ROCKET_HIDEOUT_B1F` já estava ocupada** pelo esconderijo de
Celadon (`data/maps/RocketHideout_B1F_Frlg/map.json` declara esse id). Por isso
os mapas novos se chamam `MAP_MAHOGANY_HIDEOUT_B1F/_B2F/_B3F`. De quebra, o warp
que a loja de Mahogany tinha para `MAP_ROCKET_HIDEOUT_B1F` estava em (8,4), que é
**parede**: nunca disparou, e apontava para Kanto. Agora aponta para (7,4) e para
o esconderijo certo.

**06/08/2026: entrou tudo o que faltava, com zero var.** As 22 armadilhas de
piso do B1F (coord_event com gatilho `VAR_TEMP_0` = 0, uma
`FLAG_MAHOGANY_TRAP_n` por armadilha para não renascer, nas mesmas 22
coordenadas do pokecrystal), os 6 ELECTRODE do B2F (mesma técnica,
`FLAG_MAHOGANY_ELECTRODE_1..6`, nos mesmos 6 tiles) e o encontro com o rival no
B3F (cameo sem batalha, igual ao original). As 5 câmeras viraram 5 guardas com
**raio de visão**, um por câmera, porque no original as cinco reaproveitam os
mesmos dois `GRUNTM` e `trainerbattle_single` não rebate treinador já derrotado;
as câmeras continuam na parede como placa, com o texto do original.

Ainda fora do B2F: a cena grande da ARIANA com o LANCE e o DRAGONITE, e o
`verbosegiveitem HM_WHIRLPOOL` que o LANCE dá quando os ELECTRODE caem. Derrubar
os seis ELECTRODE hoje não abre nada; quem abre a porta do transmissor continua
sendo o `setmetatile` do ON_LOAD com as duas senhas do B3F.

Efeito colateral aceito: a fala da ARIANA no 5F cita a derrota dela "no
esconderijo de MAHOGANY", que o jogador nunca viu. O texto é do hns e ficou como
está, de propósito, para não inventar diálogo.

## 3. Rival de Johto (SILVER): PORTADO em 06/08/2026, com duas simplificações

Cinco dos seis encontros entraram, **com zero var** e com o texto do
`pret/pokecrystal`, não inventado.

| Encontro | Mapa | Batalha | `TRAINER_` | Fonte do texto |
|---|---|---|---|---|
| 1. o esbarrão na porta do laboratório do ELM | `NewBarkTown` | não | — | `maps/NewBarkTown.asm` |
| 2. primeira batalha | `CherrygroveCity` | sim | `TRAINER_JOHTO_RIVAL_SILVER_1` | `maps/CherrygroveCity.asm` |
| 3. depois do Slowpoke Well | `AzaleaTown` | sim | `TRAINER_JOHTO_RIVAL_SILVER_2` | `maps/AzaleaTown.asm` |
| 4. atrás dos lendários | `BurnedTower_1F` | sim | `TRAINER_JOHTO_RIVAL_SILVER_3` | `maps/BurnedTower1F.asm` |
| 5. a emboscada de Goldenrod | `GoldenrodCity` | sim | `TRAINER_JOHTO_RIVAL_SILVER_4` | `maps/GoldenrodUndergroundSwitchRoomEntrances.asm` |
| 6. o desabafo sobre o homem de capa | `MahoganyHideout_B3F` | não | — | `maps/TeamRocketBaseB3F.asm` |

**Sprite: `OBJ_EVENT_GFX_RED`.** Esta build desenha esse sprite fora de qualquer
`#if IS_FRLG` (linha do `OBJ_EVENT_GFX_RED` em
`src/data/object_events/object_event_graphics_info_pointers.h`, sem `#if` em
volta), e **nenhum outro mapa do repo usava**, então o rival de Johto não se
confunde com ninguém. `OBJ_EVENT_GFX_SILVER` continua proibido (só existe dentro
de `#if IS_FRLG`), e `OBJ_EVENT_GFX_RICH_BOY` ficou de fora de propósito porque
já é o BARRY de Sinnoh. Em batalha: `TRAINER_PIC_RIVAL_EARLY_FRLG` nas três
primeiras e `TRAINER_PIC_RIVAL_LATE_FRLG` na quarta, os dois compilam fora de
`#if` (`src/data/graphics/trainers.h` não tem `#if` nenhum).

**Como sai sem var** (detalhe em `SINNOH-PADRAO.md`): a ordem dos encontros vem
de um `MAP_SCRIPT_ON_TRANSITION` por mapa, que esconde o SILVER por padrão e só
o mostra se o encontro anterior já caiu e este ainda não. O motor roda
ON_TRANSITION antes de nascerem os objetos. As quatro batalhas são treinador com
**raio de visão**, não `coord_event`.

### As duas simplificações, ditas na cara

1. **Time FIXO, sem triângulo de tipos.** No original o time do SILVER responde
   ao inicial do jogador: três `TRAINER_` por batalha, escolhidos por
   `VAR_STARTER_MON`. Aqui o inicial vem do laboratório do ROWAN, em Sinnoh, e
   `data/maps/SandgemTown_House1/scripts.inc` **não escreve `VAR_STARTER_MON`**
   (só dá o Pokémon e liga `FLAG_SYS_POKEMON_GET`). Ler a var daria sempre o
   mesmo galho, ou seja, o triângulo seria mentira. Então o SILVER roubou a
   linha do TOTODILE e pronto: TOTODILE 5 / CROCONAW 16 / CROCONAW 22 /
   FERALIGATR 32, o resto do time igual ao `RIVAL1` do pokecrystal (Gastly,
   Zubat, Magnemite, Haunter, Golbat, Sneasel).
   **Para ter o triângulo de volta**: acrescentar `setvar VAR_STARTER_MON, 0/1/2`
   nos três galhos de `SandgemTown_House1` e criar mais 8 `TRAINER_` (há 33
   vagas livres). Zero var nova. Não fiz porque aquele arquivo é da sessão da
   abertura, não desta.
2. **Sem galho de derrota.** O original usa `BATTLETYPE_CANLOSE` nas batalhas do
   rival: perder continua a história. Em gen 3, perder é apagar. Os textos
   `CherrygroveRivalText_YouLost` e companhia não têm onde entrar e ficaram fora.

### O que continua faltando do rival

- **Victory Road.** Não existe Victory Road de Johto neste repo: `VictoryRoad_1F`
  e `_B1F` são de Hoenn (`MAPSEC_VICTORY_ROAD`, `LAYOUT_VICTORY_ROAD_1F`),
  `VictoryRoad_*_Frlg` é de Kanto e `VictoryRoad_Kalos` é a Petalburg renomeada.
  Não dá para pôr o rival de Johto num deles, e criar mapa exigiria
  `layouts.json` e `map_groups.json`, que não são desta tarefa.
  Fica documentado: quando existir mapa, é a batalha `RIVAL1 (15)` do
  pokecrystal (Sneasel 34, Golbat 36, Magneton 34, Haunter 35, Kadabra 35,
  Feraligatr 38), texto em `maps/VictoryRoad.asm`.
- **Coreografia.** Ninguém anda: no original o SILVER caminha até você, empurra
  e sai. Aqui só o de New Bark anda (três passos para a direita e some); os
  outros aparecem, batalham e somem. Isso foi escolha de risco, não de var:
  `applymovement` com rota chutada em mapa convertido trava o jogador se o
  caminho estiver bloqueado.
- ~~**Goldenrod mudou de lugar.**~~ **DESFEITO em 15/08/2026**: o 4º duelo
  voltou para o subterrâneo, que é onde a fonte o põe. O SILVER está agora em
  `GoldenrodCity_UndergroundSwitches`, em (34,3), um tile ao sul do warp de
  (34,2) por onde o jogador desce do túnel, de frente para o norte e com raio
  3. A vaga usada é o objeto de índice 6, que já existia como item ball muda;
  ele saiu de (35,2) porque aquele tile é PAREDE (a fonte o usa só de
  bastidor, com `addobject`). O objeto da cidade continua na lista, no índice
  40, com script e tipo zerados e escondido para sempre por
  `FLAG_HIDE_SILVER_GOLDENROD` — a save guarda índice, então nada foi apagado.
  Zero flag e zero var novas: a MESMA flag serve aos dois objetos, porque a
  cidade e o subterrâneo nunca estão carregados ao mesmo tempo.

## 4. Torres e farol (prioridade 4): RESOLVIDO em 15/08/2026

Escrito em 05/08/2026 pela sessão que portou Sprout Tower, Burned Tower e o
Farol de Olivine. A nota antiga desta seção subestimava o custo (falava em "3
sábios"); o hns tem 7 batalhas só na Sprout Tower. Os mapas e scripts estão
prontos e passam em `valida_mapas_sinnoh.py` e `valida_conectividade.py`
(`warps quebrados: 0`).

### 4.1 Os 18 treinadores: JÁ EXISTEM (esta seção estava velha)

**Medido em 15/08/2026, e o texto anterior estava errado de duas maneiras.**
Ele dizia "zero vaga sobrando em `opponents.h`" e "isso também precisa subir
`MAX_TRAINERS_COUNT_EMERALD`". Nenhuma das duas frases vale mais:

- O teto é **4000** desde 12/08/2026 (`include/constants/opponents.h`), e o
  maior id em uso é **2522**. Não falta vaga e **não se mexe no saveblock**.
- Os 18 `TRAINER_` **já foram criados**, nos ids **1340 a 1357**, provavelmente
  pela mesma leva de 05-06/08 que escreveu o rival; a seção 4.1 nunca foi
  atualizada. Conferido nas três camadas em 15/08/2026:
  `#define` em `include/constants/opponents.h` (18 de 18), bloco
  `=== TRAINER_X ===` em `src/data/trainers.party` (18 de 18) e no acervo
  `src/data/trainers_johto.party` (18 de 18). Zero id duplicado no arquivo
  inteiro (conferido varrendo todos os `#define TRAINER_* <n>`).

| `TRAINER_` | id | Mapa | Fonte no hns |
|---|---|---|---|
| `TRAINER_SAGE_CHOW` | 1340 | SproutTower_1F | `TRAINER_CHOW` |
| `TRAINER_SAGE_NICO` | 1341 | SproutTower_2F | `TRAINER_NICO` |
| `TRAINER_SAGE_EDMOND` | 1342 | SproutTower_2F | `TRAINER_EDMOND` |
| `TRAINER_SAGE_JIN` | 1343 | SproutTower_3F | `TRAINER_JIN` |
| `TRAINER_SAGE_NEAL` | 1344 | SproutTower_3F | `TRAINER_NEAL` |
| `TRAINER_SAGE_TROY` | 1345 | SproutTower_3F | `TRAINER_TROY` |
| `TRAINER_SAGE_LI` | 1346 | SproutTower_3F | `TRAINER_LI` |
| `TRAINER_FIREBREATHER_NARD` | 1347 | BurnedTower_1F | `TRAINER_NARD` |
| `TRAINER_BURGLAR_RICHARDO` | 1348 | BurnedTower_1F | `TRAINER_RICHARDO` |
| `TRAINER_SAILOR_HUEY` | 1349 | OlivineCity_Lighthouse | `TRAINER_HUEY` |
| `TRAINER_GENTLEMAN_ALFRED` | 1350 | OlivineCity_Lighthouse | `TRAINER_ALFRED` |
| `TRAINER_BIRD_KEEPER_THEO` | 1351 | OlivineCity_Lighthouse | `TRAINER_THEO` |
| `TRAINER_SAILOR_TERRELL` | 1352 | OlivineCity_Lighthouse | `TRAINER_TERRELL` |
| `TRAINER_GENTLEMAN_PRESTON` | 1353 | OlivineCity_Lighthouse | `TRAINER_PRESTON` |
| `TRAINER_SAILOR_KENT` | 1354 | OlivineCity_Lighthouse | `TRAINER_KENT` |
| `TRAINER_LASS_CONNIE` | 1355 | OlivineCity_Lighthouse | `TRAINER_CONNIE` |
| `TRAINER_SAILOR_ERNEST` | 1356 | OlivineCity_Lighthouse | `TRAINER_ERNEST` |
| `TRAINER_BIRD_KEEPER_DENIS` | 1357 | OlivineCity_Lighthouse | `TRAINER_DENIS` |

Os níveis já estão na curva de Johto desta ROM (45 a 100 nominal, 45 a 128 no
que a fórmula de `curva_de_nivel.py` de fato produziu para a região): CHOW sai
com três Pokémon de nível 95 e HUEY, no farol, com três de 107 a 109. Ninguém
foi tocado nesta leva, por decisão do Gui de 15/08 (nada de polimento de time).

**O que FALTAVA de verdade, e foi consertado em 15/08/2026:** os 17 objetos
desses treinadores tinham vindo do import com `trainer_type:
TRAINER_TYPE_NONE` e raio 0, isto é, só batalhavam se o jogador falasse com
eles. Na fonte eles têm **raio de visão** (1 na Sprout 1F, 4 e 10 nos andares
de cima, 4 e 5 no farol e na Burned Tower). O raio foi devolvido campo a
campo, casando por COORDENADA com o objeto da fonte, nunca por índice. O
`SAGE_LI` ficou de fora **de propósito**: na fonte ele também é
`TRAINER_TYPE_NONE`, porque é o ancião que entrega o `ITEM_HM_FLASH` e a
batalha vem depois da conversa.

### 4.2 Flags cruas usadas (`flags.h` está com outro agente, então nada foi
### aliado, só consumido por número)

Doze `FLAG_UNUSED_0x264` a `0x26F`, uma por item (todas via
`Common_EventScript_FindItem`, padrão vanilla, sem script próprio por item):

| Flag crua | Mapa / item |
|---|---|
| `FLAG_UNUSED_0x264` | SproutTower_1F, Paralyze Heal |
| `FLAG_UNUSED_0x265` | SproutTower_2F, X Defense |
| `FLAG_UNUSED_0x266` | SproutTower_3F, Potion |
| `FLAG_UNUSED_0x267` | SproutTower_3F, Escape Rope |
| `FLAG_UNUSED_0x268` | BurnedTower_1F, HP Up |
| `FLAG_UNUSED_0x269` | BurnedTower_1F, Ether |
| `FLAG_UNUSED_0x26A` | BurnedTower_B1F, Ultra Ball |
| `FLAG_UNUSED_0x26B` | BurnedTower_B1F, TM Taunt |
| `FLAG_UNUSED_0x26C` | OlivineCity_Lighthouse, Protein |
| `FLAG_UNUSED_0x26D` | OlivineCity_Lighthouse, Hyper Potion |
| `FLAG_UNUSED_0x26E` | OlivineCity_Lighthouse, Rare Candy |
| `FLAG_UNUSED_0x26F` | OlivineCity_Lighthouse, Ether |

**Cuidado de concorrência já pego nesta sessão**: a primeira escolha foi
`0x041`-`0x04C`, sequência logo depois do `FLAG_ENABLE_RADIO`. No meio do
trabalho, outro agente aliou `0x041`-`0x044` para o esconderijo de Mahogany
(`FLAG_MAHOGANY_HIDEOUT_*`), o que teria colidido de verdade (mesmo bit
servindo pra abrir porta E marcar item pego). Troquei pra `0x264`-`0x26F`,
faixa isolada, e conferi de novo antes de fechar. Se outro agente aliar
qualquer coisa nessa faixa antes de `flags.h` ser liberado, os dois lados
colidem de novo: quem for aliar nomes amigáveis deveria conferir
`grep -n "FLAG_UNUSED_0x26" include/constants/flags.h` primeiro.
A `FLAG_RECEIVED_HM_FLASH` (SAGE_LI, HM Flash) e a `FLAG_TEMP_11` (pedra de
força do B1F, mesma flag que `FieryPath` já usa) já existiam, não são novas.

### 4.3 Sprout Tower — jogável hoje

1F: Teacher, Sage1, Sage2, Granny (falas, sem treinador) e o item Paralyze
Heal já funcionam. 2F e 3F: item X Defense, Potion, Escape Rope, e as duas
estátuas + pintura (bg_event) funcionam. As 7 batalhas (Chow, Nico, Edmond,
Jin, Neal, Troy, Li) estão escritas mas **não compilam** até os `TRAINER_`
existirem (seção 4.1). SAGE_LI dá `ITEM_HM_FLASH` e seta
`FLAG_RECEIVED_HM_FLASH`, que já existia.

Cortado por falta de recurso (não é decisão de gosto):
- **Cena do rival (SILVER) no 3F**: já documentada na seção 3 (sem sprite,
  sem vaga, usa `VAR_SPROUT_TOWER` que é proibida). Nada mudou aqui.
- **Tremor do pilar**: o hns usa `MOVEMENT_TYPE_TOWER_BEAM` com
  `OBJ_EVENT_GFX_RAYQUAZA` de paleta própria — é feature de engine do hns
  (`MovementType_TowerBeam` em `event_object_movement.c`), não existe neste
  repo. Ficou só o texto do Teacher/Granny descrevendo o tremor.
- **BELLSPROUT/GASTLY/RATTATA de decoração**: usam
  `OBJ_EVENT_GFX_MON_BASE+SPECIES_x`, que aqui cai no fallback
  `OBJ_EVENT_GFX_POKE_BALL` (índice lixo), mesmo problema já visto no arco
  anterior.

### 4.4 Burned Tower — jogável até onde dava sem sprite

1F: Nard e Richardo (batalhas, não compilam ainda), item HP Up e Ether.
B1F: pedra de força (funcional, `EventScript_StrengthBoulder` +
`FLAG_TEMP_11`), item Ultra Ball e TM Taunt, e **os três cães lendários**
como três `bg_event` (RAIKOU, ENTEI, SUICUNE): o jogador interage com o local
onde cada um estaria e ouve o grito (`playmoncry`) com um texto de "viu de
relance e sumiu". `OBJ_EVENT_GFX_RAIKOU/ENTEI/SUICUNE` existem no enum mas só
têm entrada em `object_event_graphics_info_pointers.h` dentro de
`#if IS_FRLG`; usar teria reiniciado o jogo na tela de título, então virou
`bg_event` igual foi feito com Dialga/Palkia no Spear Pillar. Conferido contra
o `pokecrystal` original (`maps/BurnedTowerB1F.asm`): lá também é uma cutscene
de "aparece, grita e some", não um NPC parado, então a adaptação não perde a
essência da cena.

Cortado por falta de recurso:
- **EUSINE, MORTY (como NPC de corredor) e o rival SILVER no 1F**: nenhuma
  das constantes de sprite existe nesta build (nem dentro de `#if IS_FRLG`,
  simplesmente não tem `OBJ_EVENT_GFX_EUSINE`/`MORTY`/`SILVER` no enum). O
  MORTY treinador de ginásio já existe em outro lugar (`EcruteakCity_Gym`);
  este seria um segundo objeto, de corredor, puramente de flavor.
- **Cameo do EUSINE no B1F**: mesma falta de sprite.
- **O buraco pro B1F**: no hns só abre depois da batalha do SILVER
  (`setmetatile 16, 12, 0x37E`). Sem essa cena, virou passagem sempre aberta;
  o warp de BurnedTower_1F pro B1F em `(16,12)` já existia no map.json antes
  desta sessão (não fui eu que criei) e passa em `valida_conectividade.py`.
  Não editei metatile nenhum: o ID `0x37E` do hns é de outro tileset
  (`gTileset_Building`/`GeneralSinnoh` aqui vs. o do hns), chutar o número
  certo sem abrir o tileset era risco desnecessário para um efeito puramente
  visual.
- **RATICATE/ZUBAT/KOFFING/HOUNDOUR/SLUGMA/MISDREAVUS/MAGMAR de decoração**:
  mesmo problema do `OBJ_EVENT_GFX_MON_BASE+SPECIES_x`.
- **Duas placas de "estátua" que o hns citava** (`RuinsOfAlph_..._StatueDescription`):
  não existem neste repo e não são minhas; conferido contra o `pokecrystal`
  original, BurnedTower1F nem tem estátua lá — era um script trocado por
  engano no hns. Não recriei.

### 4.5 Farol de Olivine — só a metade que fecha sem mexer no ginásio

1F: Sailor e Pokéfan (falas) funcionam. As 9 batalhas (Huey, Alfred, Theo,
Terrell, Preston, Kent, Connie, Ernest, Denis) estão escritas mas não
compilam ainda (seção 4.1). Item Protein, Hyper Potion, Rare Candy, Ether
funcionam.

No topo, a AMPHY doente virou um `bg_event`: o jogador acha a AMPHY (grito
via `playmoncry`) e um bilhete com a fala real da JASMINE (texto do hns,
só reenquadrado como bilhete em vez de falado por um NPC de pé). **Isso NÃO
fecha a história.** Curar a AMPHY com o Secret Potion e liberar a JASMINE de
volta pro ginásio precisa de:
- `ITEM_SECRET_POTION`, que não existe em `include/constants/items.h`;
- sprite da JASMINE (`OBJ_EVENT_GFX_JASMINE` não existe como constante nesta
  build, nem dentro de `#if IS_FRLG`);
- editar `OlivineCity_Gym` (`clearflag FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE` no
  hns), que não é meu nesta tarefa.

Cortado: **TM Shock Wave** que o hns também deixa nesta sala — o script
(`OlivineCity_EventScript_Item_Shockwave`) é da OlivineCity e
`ITEM_TM_SHOCK_WAVE` nem existe aqui; fora de escopo, não inventei.

## 5. Simplificações deliberadas dentro do que FOI entregue

- **Kurt** não some nem anda pela cidade: é um objeto só, sempre no poço, e a
  fala dele muda depois do PROTON. O hns usa quatro flags de Kurt e um `warp`
  para a casa dele; nada disso foi portado (nem a GS Ball, nem a Ilex Forest).
- **Item balls do Slowpoke Well** (2 Super Potion, 1 Great Ball, 1 Full Heal)
  foram removidas. Cada uma precisa de uma `FLAG_ITEM_...` própria; com
  `flag: 0` o item renasce a cada entrada no mapa, que é bug de item infinito.
- **Quiz do rádio e a WHITNEY no 1F da Torre** saíram: dependem de `ITEM_RADIO`
  (não existe) e de `FLAG_ENABLE_RADIO` + `VAR_GOLDENROD_CITY_STATE`.
  `FLAG_ENABLE_RADIO` existe (`FLAG_UNUSED_0x040`) mas o item não.
- **DIRETOR de verdade da Torre** não aparece. A recompensa dele é a asa do
  Lugia/Ho-Oh, escolhida por `VAR_LUGIA_OR_HOOH`. O PETREL continua sendo o
  falso diretor e some junto com os outros quando o ARCHER cai.
- **Chave do porão** (`ITEM_BASEMENT_KEY`) não existe: a frase do PETREL que
  entregava a chave foi cortada, o resto do texto dele é o do hns.
- **PETREL fica em tile bloqueado** em `(11,9)` do 5F, atrás da mesa da sala do
  diretor, igual ao hns. O `valida_mapas_sinnoh.py` acusa isso como "bloqueado":
  é falso positivo, o jogador fala com ele de `(11,8)` ou `(11,10)`.
  **Não rodar `--corrigir` nesse objeto.**
- **Sprites**: esta build não desenha `ROCKET_M`, `ROCKET_F`, `PROTON`, `KURT`,
  `SILVER` (o rival usa `OBJ_EVENT_GFX_RED` no lugar, ver seção 3),
  `SLOWPOKE_NO_TAIL`, `ARCHER`, `ARIANA`, `PETREL`, `POLICEMAN`,
  `SUPER_NERD`, `COOLTRAINER_F`, `SCIENTIST_M`, `WORKER_M` nem
  `OBJ_EVENT_GFX_MON_BASE+SPECIES_*` (aqui `MON_BASE` cai no fallback
  `POKE_BALL`, então somar espécie dá índice lixo). Os Rockets viraram
  `AQUA_MEMBER_M/F`, o PROTON virou `ARCHIE`, o ARCHER virou `MAXIE` e o KURT
  virou `EXPERT_M`. Em batalha, o pic é o de Kanto de verdade
  (`TRAINER_PIC_ROCKET_GRUNT_M_FRLG` / `_F_FRLG`), que esta build compila fora
  de `#if`.
- **Decoração removida**: os objetos que a importação deixou como
  `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` (Slowpoke, Zubat, Geodude, árvore
  de berry, rival escondido) foram apagados dos mapas tocados. Eram item balls
  sólidas e inertes no meio da cidade, não decoração.

---

## Treinadores de rota importados do hns (05/08/2026)

144 treinadores entraram, em 33 mapas, pelos ids 2274 a 2417 da faixa 2274-2599.
Gerados por `dev_scripts/importa_treinadores_johto.py`; rodar de novo reescreve
o mesmo bloco e mais nada. Johto passou de 69 para 213 treinadores com time
próprio, e de 179 para 504 Pokémon de treinador, todos dentro de 45 a 100.

Provado na ROM pelos casos `T30.1` a `T30.3` (Dirk na Rota 35, Ron na Rota 43,
Erik na Rota 45), com a asserção por **faixa** 2274-2599 e não por nome: o
controle negativo, trocando a faixa esperada pela de Kanto, derruba os três.

### O que ficou de fora, e por quê

- **Batalha dentro de cena, 12 casos.** Rival Silver nos túneis de Goldenrod
  (Cyndaquil/Totodile/Chikorita), o Rocket e as cinco irmãs Kimono do teatro de
  Ecruteak, o Eusine de Cianwood, o Kiyo do Mt. Mortar, o Giovanni das Tohjo
  Falls e o RED do cume do Mt. Silver. Nesses o `trainerbattle` vem depois de
  `applymovement`, `playbgm`, `setvar` de enredo ou câmera: portar só a linha da
  batalha entrega um NPC que anda para lugar nenhum. Cada um é uma cena a portar
  inteira, não um treinador de rota.
- **Rota 26, dois NPCs.** `Jake` e `Joyce` estão em coordenada negativa no hns
  (`(16,-10)` e `(9,-19)`) e o import de mapa já tinha descartado os objetos:
  nosso `map.json` tem 10 objetos contra 16 lá. O script e o time deles entraram,
  o NPC não existe, então a batalha é inalcançável hoje. `Beth` nem script tem.
- **Nenhum time foi inventado.** Todo treinador acima tem time no hns; o que
  falta é o NPC ou a cena, não o dado.

### Substituições feitas de propósito

- Sprites que só existem sob `#if IS_FRLG` (id aponta para o vazio e reinicia a
  ROM): `SUPER_NERD` virou `SCIENTIST_1`, `FIREBREATHER` virou `MANIAC`,
  `BURGLAR` virou `BIKER`, `JUGGLER` virou `EXPERT_M`, `BATTLE_GIRL` virou
  `CRUSH_GIRL`. Conferido contra `object_event_graphics_info_pointers.h` fora do
  ramo FRLG, em tempo de execução, e o script aborta se a tabela apontar para
  sprite sem gráfico.
- Classe e pic sem nome igual aqui: `PSYCHIC_M` -> `PSYCHIC`, `FIREBREATHER` ->
  `KINDLER`, `POLICEMAN` -> `GENTLEMAN`. O resto resolve sozinho pelo sufixo
  `_FRLG`, que esta build compila (é a mesma arte que os 474 de Kanto usam).
- **NPC que não é treinador continua `OBJ_EVENT_GFX_ITEM_BALL` inerte** nesses
  33 mapas. O escopo aqui foi treinador; devolver os moradores, as placas e as
  berry trees das rotas de Johto é outra tarefa, e é grande.

---

## 6. Bloco B6, primeira leva (12/08/2026): 80 NPCs, duas cenas e a fila que sobrou

Ferramenta: `dev_scripts/porta_cenas_johto.py` (`--flags`, `--vars`,
`--treinadores`, `--pokemon`, `--cenas`, `--demo`). Tudo idempotente, medido
rodando a leva inteira duas vezes e comparando md5 de `scripts.inc`,
`trainers.party` e `flags.h`: byte a byte igual.

**A régua que decidiu quem entrou.** Uma `FLAG_HIDE_*` do `hns` nasce APAGADA;
só é acesa em jogo novo quem está em `EventScript_ResetAllMapFlags`. Então
NPC de **classe A** (flag apagada em jogo novo) é visível desde o primeiro dia
NA FONTE, e restaurá-lo sem a cena não cria bloqueio nenhum. NPC de **classe B**
(flag acesa) fica escondido até uma cena apagar a flag, e por isso só entra
junto com ela. Dos 95 NPCs que `restaura_npcs_johto.py` recusava por flag
inexistente, 63 eram classe A aproveitável e entraram; 32 esperam, cada um com
o motivo escrito em `ESPERA` dentro da ferramenta.

### O que falta, em ordem de quanto paga

1. **As cinco KIMONO GIRLS do teatro (5 batalhas) e o fim do arco lendário.**
   A cadeia da fonte, medida: `Route39_EventScript_LegendaryTrigger` (o BAOBA
   escolhe LUGIA ou HO-OH e põe `VAR_LUGIA_OR_HOOH`) → `EcruteakCity_EventScript_Trigger`
   (a chegada na cidade, que acende meia dúzia de flags) → `EcruteakCity_Trigger_Silver`
   (o cameo do rival, que é quem põe `VAR_ECRUTEAK_CITY_THEATER` em 5) → o
   desafio no teatro → `TinTower_RoofDay` ou `WhirlIslands_LugiaChamber`.
   Bloqueio duro no fim: `ITEM_TIDAL_BELL` e `ITEM_CLEAR_BELL` NÃO existem
   nesta ROM, e são o presente que fecha o desafio.
2. **Duelos de cena: EUSINE e GIOVANNI FEITOS em 15/08/2026** (detalhe no
   bloco no fim deste arquivo). Continua faltando o **RED_2 no Mt. Silver**,
   que tem bloqueio de arte: `OBJ_EVENT_GFX_RED` já é o rival de Johto (seção
   3), então o RED precisaria de outro sprite. **Nota medida em 15/08/2026, e
   ela muda a conta**: `OBJ_EVENT_GFX_RED_NORMAL` HOJE DESENHA nesta build
   (tem entrada em `object_event_graphics_info_pointers.h` fora de qualquer
   `#if IS_FRLG`), o que não era verdade quando esta linha foi escrita. Quem
   for portar o RED começa por aí, e não por criar arte.

   O **"GRUNT do subterrâneo" NÃO EXISTE na fonte.** Procurado em 15/08/2026
   varrendo `trainerbattle*` em TODO mapa de Johto do hns e comparando com o
   que este repo já tem: as únicas batalhas da fonte sem par aqui eram
   `TRAINER_EUSINE`, `TRAINER_GIOVANNI`, os três `TRAINER_RIVAL_*_4` (que são
   o 4º duelo do rival, item 3) e `TRAINER_RED_2`. Os seis Rockets do
   `GoldenrodCity_UndergroundSwitches` e os três do
   `GoldenrodCity_UndergroundStorage` já estão na ROM desde 05/08, como
   treinadores de rota. O item da fila era eco de uma lista velha; pode ser
   riscado.
3. ~~**4º duelo do rival**~~ **FEITO em 15/08/2026**, ver a seção 3.
4. **Cenas de ginásio do B5.** A da WHITNEY **entrou em 15/08/2026**: a
   derrota dela não entrega mais a insígnia na hora, ela chora, a BRIDGET
   explica no `coord_event` de (15,11) e só então a PLAINBADGE sai. Custou UMA
   var (`VAR_JOHTO_GOLDENROD_GYM_STATE`, com os mesmos números 3/4/5 da
   fonte). O gatilho é seguro por construção: (15,10) é o ÚNICO acesso ao
   nicho da WHITNEY e o único vizinho dele é (15,11), então todo jogador que
   chega nela pisa no gatilho (conferido tile a tile na colisão de
   `LAYOUT_GOLDENROD_CITY_GYM`).

   **A de Olivine NÃO entrou, e o motivo é duro.** A "cena" é só isso: dois
   NPCs (o GENT e a LASS) se viram e falam quando o jogador cruza as fileiras
   y=14 e y=10, gastando 10 `coord_event`. Os TEXTOS que eles dizem são
   exatamente os mesmos que já dizem hoje quando o jogador fala com eles
   (`OlivineCity_Gym_Text_Gent` e `_Lass`, já na ROM), ou seja, a cena não
   acrescenta uma linha de conteúdo novo. E o portão dela,
   `VAR_OLIVINE_CITY_STATE` em 5, na fonte só é aceso pelo FAROL, no fim da
   história da AMPHY doente, que esta ROM não tem como chegar: falta
   `ITEM_SECRET_POTION` (não existe em `include/constants/items.h`) e falta a
   JASMINE (`OBJ_EVENT_GFX_JASMINE` não existe no enum). Portá-la hoje
   significaria INVENTAR um gatilho novo para repetir um texto que o jogador
   já pode ler. Ficou de fora de propósito; quando o arco do farol existir,
   ela é meia hora de trabalho.
5. **44 pares ambíguos** (duas coisas da fonte na mesma coordenada), que
   `restaura_npcs_johto.py` recusa de propósito. Resolver exige tabela
   escrita à mão, mapa a mapa.
   **Os 8 sem par FECHADOS em 18/08/2026** (raio 2, autorizado pela
   condutora): coordenada exata vazia passa a buscar em anel de Chebyshev até
   2 tiles, com desempate por sprite igual e depois por flag existente, mesma
   régua de sempre. Resultado, NÃO pendência: 7 dos 8 (`Route26` (18,8),
   `Route28` (19,19) e (7,16), `Route29` (37,11), (13,21), (29,18) e (14,10))
   têm vizinho dentro do raio 2, mas nenhum é gente (berry tree ou Pokémon de
   overworld dia/noite) e caem corretamente em "par não é gente"; só
   `LakeOfRage (49,34)` não tem absolutamente nada num quadrado 5x5 em volta e
   continua "sem par na fonte". Zero dos 8 vira NPC. Nota definitiva do
   censo: ver `demo()` de `restaura_npcs_johto.py`.
6. **4 gráficos sem equivalente**: `OBJ_EVENT_GFX_TRAIN_FRONT`,
   `OBJ_EVENT_GFX_SHINY_GYARADOS` (o GYARADOS vermelho do Lake of Rage) e dois
   `OBJ_EVENT_GFX_WHIRLPOOL`. O GYARADOS agora tem saída barata que não existia
   quando a tabela foi escrita: `OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS)`, do
   mesmo mecanismo que os 16 Pokémon de ginásio usam.

### Recursos consumidos nesta leva

- Flags `FLAG_UNUSED_0x1840` a `0x186B` (44 de 192 da faixa reservada).
- Var `VAR_UNUSED_0x4101` (1 de 48; a 0x4100 ficou de fora porque um comentário
  de exemplo em `vars.h` a cita e o alocador prefere errar para o lado seguro).
- Ids de treinador **2460** (`TRAINER_JOHTO_GRUNT_33`) e **2461**
  (`TRAINER_JOHTO_KIYO`), de 2460 a 2499.

---

## 7. Bloco B6, segunda leva (15/08/2026): dois duelos de cena, o rival de volta ao subterrâneo e a WHITNEY chorando

Tudo o que segue foi conferido ESTATICAMENTE (esta sessão não compila nem roda
emulador): colisão lida do `map.bin` tile a tile, constante por constante com
`grep` no header de origem, e as três validações do repo rodadas depois
(`valida_mapas_sinnoh.py`: `mapas com problema: 0`; `valida_conectividade.py`:
nenhum mapa de Johto/Sinnoh inalcançável; `texto_sinnoh.rotulos_repetidos()`:
0).

### O que entrou

| Cena | Mapa | Como sai |
|---|---|---|
| 4º duelo do SILVER | `GoldenrodCity_UndergroundSwitches` | treinador com raio de visão em (34,3), ON_TRANSITION por `goto_if_defeated` |
| GIOVANNI | `TohjoFalls_GiovanniRoom` | treinador com raio de visão em (5,4), aparece depois que o ARCHER cai na Torre Rádio |
| SUICUNE + EUSINE | `CianwoodCity` | `coord_event` em (18,22), cena com movimento de NPC, batalha e saída |
| choro da WHITNEY | `GoldenrodCity_Gym` | `coord_event` da BRIDGET em (15,11); a insígnia sai no galho 4 |
| raio de visão dos 17 da torre/farol | Sprout, Burned, Farol | campo `trainer_type` devolvido da fonte |

### Recursos consumidos nesta leva (números, não estimativa)

- **Flags: 3**, na faixa exclusiva desta frente, todas apelidadas em
  `include/constants/flags.h` com o prefixo pedido:
  `FLAG_JOHTO_HIDE_TOHJO_GIOVANNI` = `FLAG_UNUSED_0x186C`,
  `FLAG_JOHTO_HIDE_CIANWOOD_SUICUNE` = `0x186D`,
  `FLAG_JOHTO_HIDE_CIANWOOD_EUSINE` = `0x186E`.
  Sobram `0x186F` a `0x18FF`. O 4º duelo do rival e a cena da WHITNEY gastaram
  **zero** flag.
- **Vars: 2**, em `include/constants/vars.h`:
  `VAR_JOHTO_CIANWOOD_SUICUNE` = `VAR_UNUSED_0x4102` e
  `VAR_JOHTO_GOLDENROD_GYM_STATE` = `VAR_UNUSED_0x4103`. Sobram `0x4104` a
  `0x412F`. As duas existem por UM motivo só: `coord_event` do gen 3 compara
  VAR e não aceita flag. Todo o resto do estado sai de `goto_if_defeated`.
- **Ids de treinador: 2**, na faixa reservada: **2462** `TRAINER_JOHTO_EUSINE`
  e **2463** `TRAINER_JOHTO_GIOVANNI`. Livres agora: 2464 a 2499.
  `MAX_TRAINERS_COUNT_EMERALD` NÃO foi tocado (é 4000; maior id em uso, 2522).
- **Objetos de mapa: ZERO objeto novo.** As quatro cenas ocupam vagas que já
  existiam como item ball muda, no MESMO índice (a save guarda índice).

### Times dos dois treinadores novos

Saem do hns pelo mesmo caminho dos outros, `porta_cenas_johto.py
--treinadores`, com o nível remapeado por `curva_de_nivel.py` para a faixa de
Johto. Nada foi inventado nem escolhido a dedo:

- `TRAINER_JOHTO_EUSINE`: POLITOED, HYPNO e ELECTRODE, nível 74 (27 na fonte).
  Classe `TRAINER_CLASS_PSYCHIC`, pic `TRAINER_PIC_PSYCHIC_M`, porque
  `MYSTERY_MAN` do hns não existe aqui.
- `TRAINER_JOHTO_GIOVANNI`: KANGASKHAN 111, HONCHKROW 113, NIDOQUEEN 113,
  PERSIAN 113, URSALUNA 111 e NIDOKING 114 (60 a 62 na fonte). Classe
  `TRAINER_CLASS_BOSS_FRLG`, pic `TRAINER_PIC_LEADER_GIOVANNI_FRLG`, porque
  `ROCKET_ADMIN` do hns não existe aqui. Passar de 100 não é bug: a fórmula da
  região já entrega 45 a 128 (o maior é o `TRAINER_JOHTO_GARRETT`, 128), e
  `MAX_LEVEL` desta build é 255.

Os dois blocos ficam em `src/data/trainers.party`, dentro do acervo
`ACERVO CENAS JOHTO`. Não foram para `src/data/trainers_johto.party` porque
aquele acervo é dos GINÁSIOS e das torres (78 blocos, com o nível original do
gen 2, sem remapear); treinador de cena nunca entrou lá, nem o
`TRAINER_JOHTO_GRUNT_33` nem o `TRAINER_JOHTO_KIYO` de 12/08.

### Duas armadilhas achadas de raspão, e o que foi feito

1. **`troca_acervo()` teria apagado 8 treinadores de outras frentes.** Os cinco
   de cena de Sinnoh e as três Campeãs de Unova tinham sido apensados a
   `trainers.party` DEPOIS do acervo de Johto sem marcador `/*===` próprio, e
   aquela função corta do marcador pedido até o próximo marcador — ou até o fim
   do arquivo, se não houver. O `assert` de contagem de blocos da própria
   ferramenta pegou antes de escrever. Consertado com uma sentinela
   `/*=== ACERVO CENAS SINNOH E CAMPEA DE UNOVA ===*/` antes do primeiro deles.
2. **`porta_cenas_johto.py --treinadores` reescrevia o bloco de ids a partir só
   do que era NOVO**, e como a escrita troca o bloco inteiro, a rodada que
   acrescentava dois nomes apagava os dois que já estavam; duas rodadas
   seguidas faziam os quatro se revezarem. Consertado (o bloco agora é escrito
   a partir de TODOS os pedidos, com o id de quem já entrou preservado) e
   medido: duas rodadas seguidas dão md5 idêntico em `trainers.party` e em
   `opponents.h`.

### Landmine que NÃO é minha, mas quem for mexer precisa saber

`dev_scripts/porta_ginasios_johto.py` REESCREVE por inteiro o `scripts.inc` e o
`map.json` dos 8 ginásios de Johto, e o `map.json` que ele escreve tem só os
objetos que ele mesmo gera. Rodá-lo hoje APAGARIA os 16 Pokémon de enfeite que
`porta_cenas_johto.py --pokemon` pôs em Azalea, Ecruteak, Mahogany e
Blackthorn em 12/08. Medido em 15/08 rodando a ferramenta numa cópia isolada:
dos 8 ginásios, 6 saem diferentes do que está no repo hoje. Por isso a cena da
WHITNEY foi escrita DENTRO do gerador (função `cena_choro`, chave `choro` na
tabela `GINASIOS`) mas aplicada copiando só os dois arquivos de
`GoldenrodCity_Gym` da cópia isolada. Quem precisar rodar o gerador de verdade:
rode `porta_cenas_johto.py --pokemon --aplica` logo depois, e confira os 8
`map.json` antes de aceitar.

---

## 8. Bloco B6, terceira leva (15/08/2026): o arco dos sinos inteiro, de ponta a ponta

Sete cenas, todas portadas por `dev_scripts/porta_cenas_johto.py --cenas`, que
RECUSA a cena quando falta um simbolo em vez de deixar o build descobrir.
Conferido estaticamente (esta sessao nao compila nem roda emulador).

### A cadeia, do comeco ao fim, e onde cada elo mora

| Elo | Mapa | Gatilho |
|---|---|---|
| o BAOBA e a escolha GOLD/SILVER | `Route39` | `coord_event` em (35,20..23), `VAR_LUGIA_OR_HOOH == 0` |
| o ROCKET do teatro (ja existia, 12/08) | `EcruteakCity_Theater` | estado 0 -> 1 -> 2 -> 3 |
| o cameo do rival na porta do teatro | `EcruteakCity` | `coord_event` em (39,41), estado 3 -> 5 |
| o desafio das CINCO KIMONO GIRLS | `EcruteakCity_Theater` | tres `coord_event` de estado 5; estado 6 -> sino -> 7 |
| a danca e o HO-OH | `TinTower_RoofDay` | `coord_event` em (10,13), `VAR_COMPLETED_HO_OH == 2` |
| a danca e o LUGIA | `WhirlIslands_LugiaChamber` | `coord_event` em (29,22), `VAR_COMPLETED_LUGIA == 2` |
| o RED do cume | `MtSilver_SummitDay` | ON_TRANSITION, oitava insignia |

**A UNICA renumeracao**: a fonte arma o cameo do rival em
`VAR_ECRUTEAK_CITY_THEATER == 4`, e quem poe 4 la e o laboratorio do ELM em New
Bark, chamando o jogador de volta. Essa ida ao laboratorio nao existe nesta ROM,
entao o 4 era inalcancavel e o arco morreria ali. O gatilho passou a ser 3, que
e o valor que o proprio teatro ja poe. Removeu um passo; nao inventou nenhum.

### Recursos consumidos (numeros)

- **Itens: 2**, no FIM da lista. `ITEM_CLEAR_BELL` = 875 e `ITEM_TIDAL_BELL` =
  876. Nome e descricao vindos do hns palavra por palavra; icone e paleta
  emprestados do SOOTHE BELL, que ja e um sino desenhado aqui (mesmo padrao do
  `ITEM_GALACTIC_KEY`). Os dois sao excludentes: o desafio entrega UM, escolhido
  por `VAR_LUGIA_OR_HOOH`.
- **Flags: 4**, na faixa desta frente: `FLAG_HIDE_TIN_TOWER_KIMONO_GIRLS` =
  `FLAG_UNUSED_0x186F`, `FLAG_HIDE_WHIRL_ISLANDS_KIMONO_GIRLS` = `0x1870`,
  `FLAG_HIDE_MTSILVER_RED` = `0x1871`, `FLAG_HIDE_ECRUTEAK_SILVER` = `0x1872`.
  Livres: `0x1873` a `0x18FF`. As flags do proprio lendario
  (`FLAG_HIDE_HO_OH`, `FLAG_HIDE_LUGIA`, `FLAG_CAUGHT_*`, `FLAG_DEFEATED_*`) JA
  EXISTIAM, sao as do Emerald de fabrica, e foram reaproveitadas: um HO-OH por
  jogo, o mesmo que o de Navel Rock em Hoenn.
- **Vars: 3**: `VAR_LUGIA_OR_HOOH` = `VAR_UNUSED_0x4104`, `VAR_COMPLETED_LUGIA`
  = `0x4105`, `VAR_COMPLETED_HO_OH` = `0x4106`. Livres: `0x4107` a `0x412F`.
- **Ids de treinador: 6**: 2464 KIMONO_KUNI, 2465 KIMONO_MIKI, 2466
  KIMONO_NAOKO, **2467 `TRAINER_JOHTO_RED`**, 2468 KIMONO_SAYO, 2469
  KIMONO_ZUKI. Livres: 2470 a 2499.
- **Grafico: 1**, `OBJ_EVENT_GFX_RED_2`, mais o tag de paleta
  `OBJ_EVENT_PAL_TAG_JOHTO_RED_2` = `0x1134`.
- **Lista de multichoice: 1**, `MULTI_JOHTO_GOLD_SILVER`, com `gText_Gold` e
  `gText_Silver`, que ja existiam.
- **Musica: 5 apelidos** (`MUS_HG_VS_HO_OH`, `_VS_LUGIA`, `_KIMONO_GIRL_DANCE`,
  `_ENCOUNTER_RIVAL`, `_RIVAL_EXIT`), no mesmo padrao `#ifndef` das trinta que
  ja estavam em `songs.h`. Nenhuma faixa nova foi criada.
- **Objeto de mapa novo: ZERO.** As 26 vagas usadas ja existiam como item ball
  muda, no mesmo indice.

### O RED, e por que ele NAO fecha o jogo

`OBJ_EVENT_GFX_RED_NORMAL` desenha nesta build, mas nao servia: aquele graphics
info declara `PALSLOT_PLAYER` e a paleta do jogador, entao um NPC com ele
recolore o jogador de verdade. `OBJ_EVENT_GFX_RED_2` reaproveita a MESMA ARTE
(`sPicTable_RedNormal`) com tag e slot proprios, e o tag entrou em
`sObjectEventSpritePalettes` apontando para o mesmo dado de paleta, que e o
truque que a linha do `OBJ_EVENT_PAL_TAG_PLAYER_GREEN` ja usava. Sem a entrada
na tabela seria o bug dos NPCs verdes de novo, que o caso T96.1 guarda.

Portao: no hns quem revela o RED e o barco para Kanto (`SSAqua_1F`); aqui e a
OITAVA insignia, que ja existe e e o fim honesto de Johto. E o `special
GameClear` da fonte **saiu**: no hns o RED roda os creditos, e aqui Johto e a
segunda de cinco regioes. Junto com ele saiu o `clearflag` que vinha depois dos
creditos e que, sem eles, faria o RED renascer na proxima carga do mapa.

Time do RED: 129 a 149, o mais alto de Johto (a regiao vai de 45 a 128). E o
que a formula de `curva_de_nivel.py` produz a partir dos 73 a 88 da fonte, sem
nenhum ajuste a mao. O HO-OH e o LUGIA da historia ficaram em **100**, o teto
nominal da regiao, contra 50 da fonte.

### Tres bugs achados no caminho

1. **QUEDA DE ROTULO, e um deles estava VIVO na ROM desde 12/08.** O `.asm` da
   fonte encadeia cena por vizinhanca: um rotulo acaba sem `end` e a execucao
   entra no rotulo escrito logo abaixo. A ferramenta emite um bloco por rotulo,
   em outra ordem, entao a queda vira execucao de dado de movimento. Pior:
   rotulo que ninguem CITA nunca entra no fecho e some inteiro. Foi o que
   aconteceu com as QUATRO batalhas depois da ZUKI e com as duas pontas do sino,
   que simplesmente nao existiam no primeiro porte desta leva. E o
   `MountMortar4_EventScript_Kiyo`, portado em 12/08, tem DUAS quedas e nenhuma
   tinha sido reposta: a cena do KARATE KING sai executando o bloco seguinte
   depois da batalha. Consertado, e agora **existe portao**: `fecho_traduzido`
   reprova qualquer bloco de script que nao termine em `end`, `goto`, `return`,
   `release*`, `waitstate` ou `step_end`.
2. **`guarda_save.py` contava oito nomes que nao sao item** (`ITEM_FIELD_ARROW`,
   que e apelido de `ITEMS_COUNT`, e os sete `ITEM_USE_*` do `enum ItemType`),
   porque varria o arquivo inteiro atras de `ITEM_*`. Com isso, acrescentar UM
   item no fim da lista, que e a unica forma segura de acrescentar item, fazia o
   guarda gritar "INSERIDO NO MEIO". A varredura agora para em `ITEMS_COUNT`.
   O `save_impressao.json` continua com os oito nomes fantasmas gravados, entao
   o guarda ainda acusa 11 quebras ate alguem rodar `--gravar`; a decisao de
   regravar a impressao NAO e de agente.
3. **Rotulo indentado na fonte vira corpo do bloco anterior** para o
   `RN.blocos`, e os tres `Movement_*Correction::` do teatro estao indentados
   logo depois do `BeatGauntlet`. Sem podar, o fecho saia atras de um rotulo que
   ele nao consegue indexar.

### O que ficou de fora, e por que

- **Todo `applymovement` que anda com o JOGADOR** por rota longa: os tres
  gatilhos que atravessam o teatro (10 a 14 tiles) e as tres "correcoes" que
  reposicionam o jogador antes da primeira batalha. Movimento roteirizado do
  JOGADOR consulta colisao (o do NPC nao, `InitNpcForMovement`), e rota que
  encoste em parede trava o `waitmovement` para sempre. Ficaram os DOIS andares
  curtos que deu para conferir tile a tile: os tres passos ate o centro dos dois
  telhados, todos com colisao 0.
- **A sombra do lendario na Route 39**: `OBJ_EVENT_GFX_LEGENDARY_SHADOW` nao
  existe no enum, e sprite sem grafico reinicia a ROM. O BAOBA continua
  perguntando de que cor era a sombra.
- **A revanche pos-jogo** dos dois lendarios (`VAR_COMPLETED_* == 4`): o codigo
  esta portado, mas nada nesta ROM leva a var a 4.
- **`setmaplayoutindex` de dia/noite** nos dois telhados e no cume: os layouts
  `*_NIGHT` nao existem aqui, e apontar para layout inexistente e tela preta.

### Dois defeitos que o lote de testes pegou, e o conserto (15/08/2026)

1. **O KIYO voltou a chamar o treinador de Hoenn.** O `TRAINER_KIYO` do Mt.
   Mortar so morava em `cena["treinadores"]`, tabela que serve para GERAR o time
   e o id e que NUNCA foi usada para TRADUZIR o identificador. O porte de 12/08
   emitiu `TRAINER_KIYO` cru (id 181, o KIYO de Hoenn, que divide a flag de
   derrotado com a Rota 132), alguem consertou o ARQUIVO a mao no commit
   `2e03d4b561`, e a primeira rodada seguinte da ferramenta reescreveu o bloco e
   apagou o conserto. Conserto de arquivo gerado tem que morar no GERADOR: agora
   `SUBST` recebe o `treinadores` de cada cena, entao os onze nomes de treinador
   de cena traduzem sozinhos. Varredura dos blocos gerados por `TRAINER_` sem
   prefixo `JOHTO_`: **zero**.
2. **O LUGIA pousava dentro da agua.** A metade norte da camara e AGUA:
   elevacao 1 e `ELEVATION_SURF`, e na coluna x=29 a terra (elevacao 3, ate
   y=15) encosta na agua (elevacao 1, de y=14 para cima) SEM tile de transicao
   (0) nem de nivel multiplo (15), entao `IsElevationMismatchAt` barra quem anda
   e o jogador para em (29,15). A fonte poe o LUGIA em (29,12), sobre a agua,
   porque la se chega de SURF. **O blockdata NAO esta errado**: e byte a byte
   igual ao da fonte (conferido celula a celula), entao nada de `map.bin` foi
   tocado. O conserto foi na CENA: o LUGIA desce tres tiles a mais e pousa na
   BEIRA, em (29,15), o tile mais ao norte que da para alcancar a pe, e as duas
   linhas de `setobjectxyperm` (fim da danca e reencontro de pos-jogo)
   acompanham. Quem tiver SURF continua podendo nadar; quem nao tiver deixa de
   ficar preso olhando para um lendario inalcancavel depois de vencer as cinco
   KIMONO. O HO-OH da Tin Tower nao tinha o problema: o telhado e terra inteira.
