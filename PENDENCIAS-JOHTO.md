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

## 1. Vagas de treinador: sobra UMA no jogo inteiro

`MAX_TRAINERS_COUNT_EMERALD` é 1330 e `TRAINERS_COUNT_EMERALD` foi de 1316 para
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

O que ficou de fora do original, tudo por causa do orçamento de var: as 22
armadilhas de piso e as 5 câmeras do B1F, os seis Electrode do B2F e o encontro
com o rival no B3F. Detalhe em cada `scripts.inc`.

Efeito colateral aceito: a fala da ARIANA no 5F cita a derrota dela "no
esconderijo de MAHOGANY", que o jogador nunca viu. O texto é do hns e ficou como
está, de propósito, para não inventar diálogo.

## 3. Rival (prioridade 3): não portado

O hns amarra o rival em `VAR_STARTER_MON` (três `call_if_eq` para escolher entre
`TRAINER_RIVAL_CYNDAQUIL_2`, `..._TOTODILE_2` e `..._CHIKORITA_2`) e dispara a
cena por `coord_event` em `VAR_AZALEA_TOWN_STATE`. São duas vars, e a instrução
era zero var. Além disso:

- Não existe sprite: `OBJ_EVENT_GFX_SILVER` só existe dentro de `#if IS_FRLG`.
  O substituto seria `OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL`, que esta build desenha.
- Seriam 3 treinadores por encontro (um por inicial), e só sobra 1 vaga.

Caminho barato, se um dia for prioridade: um rival só, com time fixo, disparado
por raio de visão de treinador em vez de `coord_event`, gastando 1 vaga e
1 flag. Some com `goto_if_defeated`.

## 4. Torres e farol (prioridade 4): portado o que dava, sem vaga de treinador

Escrito em 05/08/2026 pela sessão que portou Sprout Tower, Burned Tower e o
Farol de Olivine. A nota antiga desta seção subestimava o custo (falava em "3
sábios"); o hns tem 7 batalhas só na Sprout Tower. Os mapas e scripts estão
prontos e passam em `valida_mapas_sinnoh.py` (`sprite: 0`, `fora: 0`) e
`valida_conectividade.py` (`warps quebrados: 0`), mas **nenhuma das 18
batalhas abaixo compila hoje**: cada cena foi montada com o nome de treinador
que ela DEVE ter (instrução explícita de quem orquestrou esta sessão), então
falta criar os 18 `TRAINER_` antes de compilar essas seis maps.

### 4.1 Treinadores que faltam (18, zero vaga sobrando em `opponents.h`)

Todos como `trainerbattle_single` (exceto SAGE_LI, que é
`trainerbattle_no_intro` depois de um `goto_if_set` na flag da HM). Classe,
pic de batalha e sprite de overworld sugeridos; time/nível ficam no hns
(`fontes-mapas/hns/src/data/trainers.h` + `trainer_parties.h`, mesmo nome de
`TRAINER_` sem prefixo, ex. `TRAINER_CHOW`).

| `TRAINER_` que falta criar | Mapa | Fonte no hns | `TRAINER_PIC_` sugerido | `OBJ_EVENT_GFX_` de overworld |
|---|---|---|---|---|
| `TRAINER_SAGE_CHOW` | SproutTower_1F | `TRAINER_CHOW` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_NICO` | SproutTower_2F | `TRAINER_NICO` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_EDMOND` | SproutTower_2F | `TRAINER_EDMOND` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_JIN` | SproutTower_3F | `TRAINER_JIN` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_NEAL` | SproutTower_3F | `TRAINER_NEAL` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_TROY` | SproutTower_3F | `TRAINER_TROY` | `TRAINER_PIC_EXPERT_M` | `OBJ_EVENT_GFX_EXPERT_M` |
| `TRAINER_SAGE_LI` | SproutTower_3F | `TRAINER_LI` | `TRAINER_PIC_EXPERT_F` ou EXPERT_M | `OBJ_EVENT_GFX_OLD_MAN` (ELDER, já está no mapa) |
| `TRAINER_FIREBREATHER_NARD` | BurnedTower_1F | `TRAINER_NARD` | `TRAINER_PIC_KINDLER` | `OBJ_EVENT_GFX_CAMPER` |
| `TRAINER_BURGLAR_RICHARDO` | BurnedTower_1F | `TRAINER_RICHARDO` | sem pic de burglar nesta build; sugestão `TRAINER_PIC_HIKER` | `OBJ_EVENT_GFX_HIKER` |
| `TRAINER_SAILOR_HUEY` | OlivineCity_Lighthouse | `TRAINER_HUEY` | `TRAINER_PIC_SAILOR` | `OBJ_EVENT_GFX_SAILOR` |
| `TRAINER_GENTLEMAN_ALFRED` | OlivineCity_Lighthouse | `TRAINER_ALFRED` | `TRAINER_PIC_GENTLEMAN` | `OBJ_EVENT_GFX_GENTLEMAN` |
| `TRAINER_BIRD_KEEPER_THEO` | OlivineCity_Lighthouse | `TRAINER_THEO` | `TRAINER_PIC_BIRD_KEEPER` | `OBJ_EVENT_GFX_HIKER` (ROCKER não desenha aqui) |
| `TRAINER_SAILOR_TERRELL` | OlivineCity_Lighthouse | `TRAINER_TERRELL` | `TRAINER_PIC_SAILOR` | `OBJ_EVENT_GFX_SAILOR` |
| `TRAINER_GENTLEMAN_PRESTON` | OlivineCity_Lighthouse | `TRAINER_PRESTON` | `TRAINER_PIC_GENTLEMAN` | `OBJ_EVENT_GFX_GENTLEMAN` |
| `TRAINER_SAILOR_KENT` | OlivineCity_Lighthouse | `TRAINER_KENT` | `TRAINER_PIC_SAILOR` | `OBJ_EVENT_GFX_SAILOR` |
| `TRAINER_LASS_CONNIE` | OlivineCity_Lighthouse | `TRAINER_CONNIE` (era COOLTRAINER_F no hns) | `TRAINER_PIC_LASS` | `OBJ_EVENT_GFX_LASS` (COOLTRAINER_F não desenha aqui) |
| `TRAINER_SAILOR_ERNEST` | OlivineCity_Lighthouse | `TRAINER_ERNEST` | `TRAINER_PIC_SAILOR` | `OBJ_EVENT_GFX_SAILOR` |
| `TRAINER_BIRD_KEEPER_DENIS` | OlivineCity_Lighthouse | `TRAINER_DENIS` | `TRAINER_PIC_BIRD_KEEPER` | `OBJ_EVENT_GFX_HIKER` |

Isso também precisa subir `MAX_TRAINERS_COUNT_EMERALD` de novo (já estourado
desde a seção 1) — decisão de quem orquestra, mexe no saveblock.

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
  `SILVER`, `SLOWPOKE_NO_TAIL`, `ARCHER`, `ARIANA`, `PETREL`, `POLICEMAN`,
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
