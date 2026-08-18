# Plano da obra de Sinnoh (máquina de vars + cenas de hidden_flag)

Documento de referência único da obra de Sinnoh do bloco B6, desenhada pela
condutora em 16/08/2026. Destrava os 411 pendentes de Sinnoh da fila
(`dev_scripts/fila_b6.json`: 247 grupos de `hidden_flag` e 164 gatilhos de
`coord_event`). Os executores consomem as tabelas daqui e os defines que o
bloco S1 gravar em `include/constants/vars.h` e `include/constants/flags.h`
como fonte única de valor. Ninguém inventa número: se um valor não está aqui
nem na tabela gerada do S1, ele não existe ainda, e o certo é voltar aqui.

Escrito medindo `dev_scripts/fila_b6.json` (gerado em 15/08/2026) e a fonte
`fontes-mapas/pokeplatinum` (`res/field/events/events_*.json`,
`res/field/scripts/scripts_*.s`, `src/script_manager.c`,
`src/field_map_change.c`). Nenhum número digitado de memória; os comandos de
varredura estão citados onde importam.

## O que a varredura diz (16/08/2026)

- 164 gatilhos pendentes citam **70 nomes de var do Platinum**, e **zero**
  deles existe em `include/constants/vars.h` (já conferido pelo cabeçalho de
  `fila_b6.py`).
- Desses 70, **9 são `VAR_MAP_LOCAL_0x*`** (0x00 a 0x07 e 0x0F): locais de
  mapa do motor da fonte. Prova da semântica: `src/script_manager.c:480`
  zera a faixa inteira, e quem chama é `src/field_map_change.c:254` e `:311`,
  ou seja, **zeram na troca de mapa**. É exatamente o contrato das
  `VAR_TEMP_0` a `VAR_TEMP_F` deste motor.
- Sobram **61 vars nomeadas**. Depois dos descartes e adiamentos das decisões
  3 a 5 abaixo, **49 viram alias** (tabela adiante).
- Dos 247 grupos de `hidden_flag`: **8 estão sem bloqueio** (12 objetos, a
  cena já existe, falta pôr o resto do grupo), **41 são mecânica de
  Pokécenter/Mart repetida por prédio** (decisão 6), 2 estão bloqueados por
  mapa não importado (`MAP_HEADER_ROUTE_210_NORTH`), e o resto é cena de
  história com flag a criar.
- Orçamento de flags: faixa de Sinnoh `0x190B` a `0x19FF` com **245 livres**
  (`dev_scripts/flags_livres.py` em 16/08/2026), transbordo em `0x1B00+`
  (fora da reserva de Unova, que vai até `0x1AFF`).
- Orçamento de vars: gap `0x4130` a `0x415F` com **48 livres**, transbordo
  `0x41C2` a `0x41FF` (62 livres; `0x41C0`/`0x41C1` são do Turnback, B1.b).

### CORREÇÃO DE ORÇAMENTO, 17/08/2026 (bloco S1)

**A faixa primária de flags deste plano não existe mais.** A consolidação de
Kanto (commit `652776174a`, do mesmo dia) apelidou os **245 de 245** endereços
de `0x190B` a `0x19FF` e seguiu até `0x1A4B`. Prova de que a invasão é real, e
não leitura torta: `FLAG_HIDE_ROUTE24_TM45` está definida como
`FLAG_UNUSED_0x191A`, dentro da faixa que este plano tinha reservado.

Remedido em 17/08/2026 com `python3 dev_scripts/flags_livres.py`: 2420
`FLAG_UNUSED` declaradas, **837 ocupadas**, **1519 realmente livres**, e o
maior bloco contíguo livre vai de **`0x1A4C` a `0x2025` (1498 flags)**.

**Faixa nova da obra de Sinnoh: `0x1B00` a `0x1BFF`**, com transbordo em
`0x1C00+` dentro do mesmo bloco contíguo. Não é `0x1A4C` porque `0x1A00` a
`0x1AFF` é a reserva de Unova, e ocupar reserva alheia foi exatamente o erro
que custou esta correção. `0x1B00+` já era o transbordo que este plano
apontava, então a decisão 9 continua valendo palavra por palavra, só com a
faixa trocada. O dono está anotado em `include/constants/flags.h`, no bloco
`B6 Sinnoh, flags dos grupos de hidden_flag`.

Consumo real medido pelo gerador: **157 flags novas** (`0x1B00` a `0x1B9C`),
4 reusadas e 2 devolvidas à condutora por empate de reuso. Sobra: **99**
endereços até `0x1BFF`, mais **1062** de `0x1C00` a `0x2025`.

**A tabela de vars continua válida, e isso foi conferido, não presumido**:
`grep` por apelido em `include/constants/vars.h` e por uso cru em `data/` e
`src/` dá **zero ocupação** em `0x4130` a `0x415F` e em `0x41C2`, e todos os
50 endereços existem como `VAR_UNUSED_0xNNNN`. Nenhum endereço de var mudou.

**O orçamento de flags encolheu por um motivo que não é aritmética.** Dos 247
grupos de `hidden_flag`, **34 nunca foram flag**: o campo `hidden_flag` da
fonte guarda o `MAP_HEADER_*` de origem quando o objeto é CLONE (`clone_id`
preenchido; ex.: a placa da creche em `events_route_210_south.json`). Esses 34
saem do orçamento inteiro, e a leitura do plano de que "2 estão bloqueados por
mapa não importado" era esta armadilha vista pela metade.

### Decisões da condutora sobre os retornos do S1 (17/08/2026)

- **`FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC` reusa `FLAG_GALACTICA_QG_TOMADO`.**
  Semântica idêntica ao que a leva da espinha já fez: os 20 grunts do Hall
  somem com a queda do Saturn, e os grupos escondidos do QG são o mesmo
  momento de enredo. `QG_CHAVE` é portão de entrada, momento diferente.
- **`FLAG_HIDE_SPEAR_PILLAR_GRUNTS`: RESOLVIDA pela evidência do S2.** O
  irmão do grupo já usa `FLAG_GALACTICA_MT_CORONET` (estrutura da leva da
  espinha, provada em suíte), e o S2 completou o grupo com a mesma flag e o
  mesmo script. As duas "ambíguas" do censo do S1 morrem aqui: os grupos do
  QG e do pilar estão COMPLETOS, nenhuma leva futura precisa dos alias
  `FLAG_HIDE_*` deles (anotar no censo como resolvidas por grupo completo).
- **Registros do S2 para o S8**: a fila marca "feita" por engano o grupo
  `VEILSTONE_CITY_GRUNT_M_STORAGE_KEY` (o desempate por distância roubou o
  lugar dele; o script 13, "antennae", não está portado em lugar nenhum);
  e os 3 trainers do `MtCoronet1FTunnelRoom` foram deliberadamente portados
  para `MtCoronet_1F_South`/`MtCoronet_B1F` (id de treinador não pode
  duplicar entre mapas: derrotável uma vez). Os dois viram calibração de
  fila, não trabalho de cena.
- **Arco dos 53 gatilhos de `VAR_TEMP` (`@ TODO S?`)**: ginásio de Pastoria e
  salas de elevador do ginásio de Hearthome -> S5; Route206 -> S4; elevador
  da Liga -> S6; ruínas dos Regi (Iceberg/Iron/RockPeak), Iron Island
  (salas/elevador), Villa -> S7. O executor de cada leva assume os TODO dos
  seus mapas; o rótulo `S?` no esqueleto não se corrige em massa, corrige-se
  ao escrever a cena.
- **Tile empilhado de Twinleaf (2,7)** (2 gatilhos, mesma var, mesmo valor
  0): o executor S3 des-empilha respeitando a ordem relativa da fonte
  (desloca um dos gatilhos para o tile vizinho que a fonte indica); os
  demais empilhados do censo (`tiles_empilhados`) têm valores distintos e
  não travam, ficam como estão.
- **QA ganha item novo (S8)**: `fila_b6.py` precisa aprender que gatilho
  cujo rótulo só tem `@ TODO` + `end` NÃO conta como feito (senão a fila
  para de cobrar 95 cenas), e o gerador ganha a checagem de andabilidade do
  tile plantado contra `map.bin` (a conversão proporcional pode ter posto
  gatilho em tile intransponível; hoje só a leva descobre).

### Decisões da condutora sobre os retornos do S5 (18/08/2026)

- **Duas flags novas AUTORIZADAS na faixa de Sinnoh** (próximas livres após
  `0x1B9C`): `FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE` (o
  `FLAG_PASTORIA_CITY_GRUNT_M_MOVED_EAST` da fonte, set-piece da bomba) e
  `FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO` (o
  `FLAG_BLOCK_PASTORIA_CITY_CROAGUNK_EVENT`). Quem grava os defines é o
  executor da onda 4 que escrever as cenas, anotando o consumo na faixa.
- **Rivais de Pastoria e Route 209**: mesma régua do rival da Route 203
  (executor de treinadores, 3 variantes por inicial, ids na faixa
  2508-2519, times literais da fonte com o par de remapeamento 7→147/9→149
  conferido na curva). Onda 4.
- **Fechos que moram em script de vitória de líder** (Veilstone counterpart
  na vitória da Maylene; rival do portão 209 na vitória da Fantina): é
  fiação de cena, NÃO polimento de time (decisão 2 do Gui intocada); o
  executor da onda 4 edita só o trecho pós-vitória do scripts.inc do
  ginásio, sem tocar em time.
- Set-piece da bomba de Pastoria + BlockGreatMarsh: onda 4, junto do arco
  S6 (é Equipe Galáctica). FaceBoard/Croagunk cruza com Valor Lakefront e
  fica para a S7, como o plano já previa.

## Decisões da condutora (16/08/2026)

1. **`VAR_MAP_LOCAL_0xNN` da fonte vira `VAR_TEMP_N` daqui, sem alias novo.**
   Custo de save zero. Obrigação do executor: antes de usar, `grep` no
   `scripts.inc` do mapa de destino por `VAR_TEMP_` para conferir que o mapa
   não usa aquele temp para outra coisa; colisão volta ao plano.
2. **Var nomeada portada é alias 1:1 e os VALORES são os da fonte, número a
   número.** Nada de renumerar estado: o `value` do gatilho e os `SetVar`
   das cenas entram literais. Isso mantém qualquer cena futura do mesmo arco
   compatível sem tabela de conversão de valores.
3. **Descartadas por mecânica inexistente, não portadas nem inventadas**
   (mesma régua da decisão 7 de Unova):
   - `VAR_GTS_ACCESS_STATE` (GTS não existe aqui);
   - `VAR_POKETCH_CAMPAIGN_STATE` (Pokétch não existe);
   - `VAR_PAL_PARK_STATE` (migração de gen 3 não existe);
   - `VAR_BATTLE_FRONTIER_DUMMY_STATE` (dummy declarado na própria fonte);
   - `VAR_FOLLOWER_MON_ACTIVE` (`OW_FOLLOWERS_ENABLED` é `FALSE` em
     `include/config/overworld.h:61`).
   Os gatilhos dessas vars saem da fila como descartados na próxima
   regeneração de `fila_b6.py` (anotar lá, como foi feito com
   `ShoppingMallNine` na decisão 5 de Unova).
4. **Amity Square vira praça aberta, sem máquina.** Os 27 gatilhos de
   `VAR_AMITY_SQUARE_STATE` são warps roteirizados de saída (conferido:
   `AmitySquare_Warp2` faz `SetVar VAR_0x8003, 2` e `GoTo AmitySquare_DoWarp`,
   que existe para devolver o follower antes de sair). Sem follower, viram
   `warp_events` comuns no `map.json`, e os 4 gatilhos de
   `VAR_FOLLOWER_MON_ACTIVE` (o portão que barra quem não tem Pokémon fofo)
   caem com a mecânica. `VAR_AMITY_SQUARE_STATE` não vira alias.
5. **Acompanhantes ADIADOS, não descartados.** As 6 vars de parceiro que
   anda junto (`VAR_FOLLOWER_RIVAL_STATE`, `VAR_ETERNA_FOREST_FOLLOWER_
   CHERYL_STATE`, `VAR_IRON_ISLAND_B2F_LEFT_ROOM_FOLLOWER_RILEY_STATE`,
   `VAR_STARK_MOUNTAIN_ROOM_2_FOLLOWER_BUCK_STATE`,
   `VAR_VICTORY_ROAD_1F_ROOM_2_FOLLOWER_MARLEY_STATE`,
   `VAR_WAYWARD_CAVE_1F_FOLLOWER_MIRA_STATE`) são conteúdo real (os cinco
   stat trainers e o rival) mas pedem mecânica de parceiro em dupla que não
   tem desenho. Ficam na fila com bloqueio "mecânica de parceiro sem
   desenho"; ganham var quando a mecânica ganhar desenho.
6. **Pokécenter/Mart ADIADOS em bloco.** Os 41 grupos repetidos
   (`FLAG_HIDE_POKECENTER_DAILY_TRAINER_1`/`_2` em 28 prédios,
   `FLAG_HIDE_MART_MYSTERY_GIFT_DELIVERYMAN` em 13) são mecânica de batalha
   diária e Mystery Gift, não cena de história. Batalha é polimento de fim de
   projeto (decisão 2 do Gui) e Mystery Gift não existe aqui. Bloqueio na
   fila: "mecânica diária/Mystery Gift, decisão 6 do plano de Sinnoh".
7. **Gatilho com `width`/`length` expande em N `coord_events` de 1 tile.**
   O formato da fonte tem span (ex.: Twinleaf tem um de `width: 8`); o nosso
   `map.json` não tem. O gerador expande, e a contagem de gatilhos gerados
   por isso é maior que a contagem da fila (a fila conta `(mapa, var,
   script)`, o mapa recebe um `coord_event` por tile do span).
8. **Índice de script da fonte é 1-based na lista de `ScriptEntry`.**
   Prova dupla: no Amity, os gatilhos de script 18 a 44 caem exatos em
   `Warp1` a `Warp27` contando a partir de 1; em Twinleaf, `script: 2` cai em
   `TwinleafTown_CoordEvent_RivalThud` (a cena do rival, var do rival) e
   `script: 4` em `TwinleafTown_CoordEvent_RivalWasLookingForYou` (gatilho
   pós-guitarrista). O gerador confere isso no autoteste com esses dois
   mapas antes de gerar qualquer coisa.
9. **Flags dos grupos de `hidden_flag`: alias mecânico gerado, reuso
   semântico tem precedência.** Nome padrão `FLAG_SINNOH_ESCONDE_<resto do
   nome da fonte>` na faixa `0x190B` a `0x19FF` (transbordo `0x1B00+`, dono
   anotado). ANTES de criar, o gerador confere se o mesmo momento de enredo
   já tem flag aqui (`FLAG_GALACTICA_*`, `FLAG_SINNOH_*`, as 5 da leva 3) e
   reusa; a tabela gerada marca `reusada` ou `nova`. Grupos distintos da
   fonte NUNCA são fundidos numa flag só por parecerem iguais; fusão é
   decisão de condutora, caso a caso.
10. **A tabela gerada é artefato, o plano é a régua.** O gerador
    (`dev_scripts/maquina_sinnoh.py`, bloco S1) grava
    `dev_scripts/maquina_sinnoh.json` com o censo completo (var da fonte →
    alias → endereço; FLAG_HIDE → flag → endereço; gatilho → tiles →
    script). O JSON não se edita à mão; o que este plano não cobre volta
    para este plano, nunca vira invenção de executor.

## Tabela de vars (fonte → alias → endereço)

As 49 vars nomeadas portadas, em ordem alfabética da fonte, endereços
sequenciais no gap `0x4130` a `0x415F` (48) e transbordo `0x41C2` (1).
Gerada por script em 16/08/2026 a partir da fila; a coluna "gatilhos" é o
peso pendente de `coord_event` (as cenas de `hidden_flag` do mesmo arco
consomem as mesmas vars por dentro dos scripts).

| var da fonte | alias aqui | endereço | gatilhos |
|---|---|---|---|
| `VAR_ACUITY_LAKEFRONT_STATE` | `VAR_SINNOH_ACUITY_BEIRA_ESTADO` | 0x4130 | 1 |
| `VAR_CANALAVE_CITY_STATE` | `VAR_SINNOH_CANALAVE_ESTADO` | 0x4131 | 1 |
| `VAR_CELESTIC_TOWN_ELDER_STATE` | `VAR_SINNOH_CELESTIC_ANCIA_ESTADO` | 0x4132 | 1 |
| `VAR_ETERNA_CITY_BLOCK_EXITS_STATE` | `VAR_SINNOH_ETERNA_BLOQUEIO_SAIDAS` | 0x4133 | 2 |
| `VAR_ETERNA_CITY_STATE` | `VAR_SINNOH_ETERNA_ESTADO` | 0x4134 | 4 |
| `VAR_GALACTIC_HQ_4F_STATE` | `VAR_SINNOH_QG_4F_ESTADO` | 0x4135 | 1 |
| `VAR_GALACTIC_HQ_CONTROL_ROOM_STATE` | `VAR_SINNOH_QG_SALA_CONTROLE_ESTADO` | 0x4136 | 1 |
| `VAR_GALACTIC_HQ_HALL_STATE` | `VAR_SINNOH_QG_HALL_ESTADO` | 0x4137 | 1 |
| `VAR_HALL_OF_ORIGIN_STATE` | `VAR_SINNOH_SALAO_ORIGEM_ESTADO` | 0x4138 | 3 |
| `VAR_HEARTHOME_CITY_STATE` | `VAR_SINNOH_HEARTHOME_ESTADO` | 0x4139 | 1 |
| `VAR_JUBILIFE_CITY_STATE` | `VAR_SINNOH_JUBILIFE_ESTADO` | 0x413A | 3 |
| `VAR_JUBILIFE_LOOKER_PAL_PAD_STATE` | `VAR_SINNOH_JUBILIFE_LOOKER_ESTADO` | 0x413B | 1 |
| `VAR_MT_CORONET_1F_SOUTH_STATE` | `VAR_SINNOH_CORONET_1F_SUL_ESTADO` | 0x413C | 1 |
| `VAR_MT_CORONET_2F_STATE` | `VAR_SINNOH_CORONET_2F_ESTADO` | 0x413D | 1 |
| `VAR_OREBURGH_CITY_STATE` | `VAR_SINNOH_OREBURGH_ESTADO` | 0x413E | 2 |
| `VAR_OREBURGH_GATE_1F_HIKER_STATE` | `VAR_SINNOH_OREBURGH_PORTAO_ANDARILHO` | 0x413F | 1 |
| `VAR_PASTORIA_CITY_CROAGUNK_SCENE_STATE` | `VAR_SINNOH_PASTORIA_CROAGUNK_CENA` | 0x4140 | 1 |
| `VAR_PASTORIA_CITY_OBSERVATORY_GATE_1F_STATE` | `VAR_SINNOH_PASTORIA_OBSERVATORIO_ESTADO` | 0x4141 | 1 |
| `VAR_PASTORIA_CITY_STATE` | `VAR_SINNOH_PASTORIA_ESTADO` | 0x4142 | 3 |
| `VAR_PLAYER_HOUSE_RIVAL_STATE` | `VAR_SINNOH_CASA_JOGADOR_RIVAL_ESTADO` | 0x4143 | 4 |
| `VAR_PLAYER_HOUSE_STATE` | `VAR_SINNOH_CASA_JOGADOR_ESTADO` | 0x4144 | 1 |
| `VAR_POKEMON_MANSION_OFFICE_BLOCK_STATUE_STATE` | `VAR_SINNOH_MANSAO_ESTATUA_ESTADO` | 0x4145 | 1 |
| `VAR_RESORT_AREA_STATE` | `VAR_SINNOH_RESORT_ESTADO` | 0x4146 | 1 |
| `VAR_RIVAL_BEAT_SUNYSHORE_GYM` | `VAR_SINNOH_RIVAL_VENCEU_SUNYSHORE` | 0x4147 | 1 |
| `VAR_ROUTE_202_STATE` | `VAR_SINNOH_R202_ESTADO` | 0x4148 | 1 |
| `VAR_ROUTE_203_RIVAL_STATE` | `VAR_SINNOH_R203_RIVAL_ESTADO` | 0x4149 | 1 |
| `VAR_ROUTE_207_COUNTERPART_TRIGGER_STATE` | `VAR_SINNOH_R207_COMPANHEIRO_ESTADO` | 0x414A | 1 |
| `VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE` | `VAR_SINNOH_R209_PORTAO_HEARTHOME` | 0x414B | 1 |
| `VAR_ROUTE_217_STATE` | `VAR_SINNOH_R217_ESTADO` | 0x414C | 1 |
| `VAR_ROUTE_218_GATE_TO_CANALAVE_CITY_STATE` | `VAR_SINNOH_R218_PORTAO_CANALAVE` | 0x414D | 1 |
| `VAR_ROUTE_224_STATE` | `VAR_SINNOH_R224_ESTADO` | 0x414E | 1 |
| `VAR_ROUTE_227_BUCK_STATE` | `VAR_SINNOH_R227_BUCK_ESTADO` | 0x414F | 1 |
| `VAR_ROUTE_227_WAKE_RIVAL_STATE` | `VAR_SINNOH_R227_WAKE_RIVAL_ESTADO` | 0x4150 | 1 |
| `VAR_SANDGEM_TOWN_STATE` | `VAR_SINNOH_SANDGEM_ESTADO` | 0x4151 | 1 |
| `VAR_SNOWPOINT_CITY_STATE` | `VAR_SINNOH_SNOWPOINT_ESTADO` | 0x4152 | 1 |
| `VAR_SOLACEON_TOWN_STATE` | `VAR_SINNOH_SOLACEON_ESTADO` | 0x4153 | 1 |
| `VAR_SPEAR_PILLAR_STATE` | `VAR_SINNOH_SPEAR_PILLAR_ESTADO` | 0x4154 | 2 |
| `VAR_STARK_MOUNTAIN_OUTSIDE_STATE` | `VAR_SINNOH_STARK_FORA_ESTADO` | 0x4155 | 1 |
| `VAR_SUNYSHORE_CITY_STATE` | `VAR_SINNOH_SUNYSHORE_ESTADO` | 0x4156 | 1 |
| `VAR_TWINLEAF_TOWN_GUITARIST_TRIGGER_STATE` | `VAR_SINNOH_TWINLEAF_GUITARRISTA` | 0x4157 | 1 |
| `VAR_TWINLEAF_TOWN_RIVAL_TRIGGER_STATE` | `VAR_SINNOH_TWINLEAF_RIVAL` | 0x4158 | 1 |
| `VAR_VALLEY_WINDWORKS_STATE` | `VAR_SINNOH_WINDWORKS_ESTADO` | 0x4159 | 2 |
| `VAR_VALLEY_WINDWORKS_TEAM_GALACTIC_STATE` | `VAR_SINNOH_WINDWORKS_GALACTICA_ESTADO` | 0x415A | 1 |
| `VAR_VALOR_LAKEFRONT_BLOCK_SUNYSHORE_STATE` | `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE` | 0x415B | 1 |
| `VAR_VEILSTONE_CITY_CRASHER_WAKE_STATE` | `VAR_SINNOH_VEILSTONE_WAKE_ESTADO` | 0x415C | 1 |
| `VAR_VEILSTONE_CITY_GALACTIC_WAREHOUSE_STATE` | `VAR_SINNOH_VEILSTONE_ARMAZEM_ESTADO` | 0x415D | 1 |
| `VAR_VEILSTONE_WAREHOUSE_GUARDS_FIGHTABLE` | `VAR_SINNOH_VEILSTONE_GUARDAS_DUELAVEIS` | 0x415E | 1 |
| `VAR_VERITY_LAKEFRONT_STATE` | `VAR_SINNOH_VERITY_BEIRA_ESTADO` | 0x415F | 1 |
| `VAR_VILLA_STATE` | `VAR_SINNOH_VILLA_ESTADO` | 0x41C2 | 1 |

Var interna de script que aparecer durante o porte (a fonte usa vars soltas
dentro de cena, ex.: `VAR_VISITED_LAKE_VERITY_WITH_RIVAL` em Twinleaf) NÃO
ganha endereço de executor: volta ao plano, entra nesta tabela em append
(transbordo `0x41C3+`), e só então é usada.

## Tabela de conversão Platinum → este motor

Régua de tradução das cenas. O que não estiver nela volta para cá.

| item da fonte (Platinum) | como entra aqui |
|---|---|
| `coord_event` (`var`, `value`, `script`) | `coord_event` no `map.json` com a var aliasada e `var_value` literal da fonte (igualdade nos dois motores); span expandido, decisão 7 |
| índice `script: N` | N-ésimo `ScriptEntry` (1-based) de `res/field/scripts/scripts_<mapa>.s`, decisão 8 |
| `SetVar` / `AddVar` | `setvar` / `addvar` na var aliasada, valores literais |
| `GoToIfEq`/`GoToIfGe`/`GoToIfSet` e afins | `goto_if_eq`/`goto_if_ge`/`goto_if_set` (mesma família daqui) |
| `CallIfEq` e afins | `call_if_eq` e afins |
| `SetFlag`/`ClearFlag` de `FLAG_HIDE_*` | `setflag`/`clearflag` da flag aliasada + `removeobject`/`addobject` na cena; o campo `flag` do `object_event` leva a flag aliasada |
| `LockAll`/`FacePlayer`/`ReleaseAll` | `lockall`/`faceplayer`/`releaseall`; terminadores obrigatórios como em Unova (`release`/`releaseall` + `end`) |
| `PlaySE`/`PlayFanfare`/`PlayBGM` | `playse`/`playfanfare`/`playbgm` com o equivalente sonoro daqui (mapeamento de música é escolha documentada no arquivo, como o MARLON fez) |
| `Message`/caixas de texto | texto palavra a palavra, requebrado para a largura daqui |
| coordenada (`x`, `z` da fonte) | `conversor_de_coordenada` de `dev_scripts/importa_npcs_sinnoh.py` (o mesmo dos NPCs mudos) |
| `ApplyMovement` no jogador | permitido com rota conferida contra `data/layouts/<Layout>/map.bin` |
| specials de mecânica inexistente (Pokétch, GTS, Pal Park, seguidor) | descartados, sem substituto, listados no comentário da cena |

## A máquina (bloco S1): `dev_scripts/maquina_sinnoh.py`

Molde: `changeblock_gen2.py` (trava de censo) + `fila_b6.py` (varredura).

- Lê `events_*.json` + `scripts_*.s` da fonte, só dos mapas casados da fila.
- Grava, com `--gravar`: os alias de vars (tabela acima) e de flags (decisão
  9) em `vars.h`/`flags.h`, os `coord_events` expandidos nos `map.json` com
  rótulo de cena esqueleto no `scripts.inc` (corpo `@ TODO S<leva>` + `end`,
  contando o que o fecho da fonte alcança), e o censo
  `dev_scripts/maquina_sinnoh.json`.
- `--demo` (autoteste, roda antes de qualquer `--gravar`): reconta os 164
  gatilhos da fila, bate a decisão 8 nos dois mapas de prova, confere que
  nenhum endereço gerado colide com `vars.h`/`flags.h` atuais, e que a
  expansão de span devolve o total esperado. Qualquer divergência: para e
  reporta, não grava.
- Esqueleto NÃO é cena: a fila continua cobrando a cena até o executor da
  leva escrever o corpo. O gerador só garante que gatilho, var, flag e
  endereço nunca sejam inventados à mão.
- Conserto de arquivo gerado mora no gerador (lição Kiyo).

## Plano de blocos executáveis

Ordem de risco crescente, um dono por arquivo compartilhado por leva.
`vars.h`/`flags.h` são do S1; `trainers.party`/`opponents.h` não entram
nesta obra (batalha fica para o fim, decisão 2 do Gui).

- **S1 — máquina.** Escrever `maquina_sinnoh.py`, rodar `--demo`, depois
  `--gravar`. Único bloco que toca `vars.h`/`flags.h`. Sai com o censo
  gravado e os esqueletos plantados.
- **S2 — os 8 grupos sem bloqueio** (12 objetos: EternaCity,
  GalacticHQ_2F/3F/B2F, MtCoronet1FTunnelRoom, SpearPillar,
  TeamGalacticEternaBuilding_3F, VeilstoneCity). Não depende do S1 (as cenas
  e flags já existem); pode rodar em paralelo desde já.
- **S3 — arco de abertura.** Twinleaf, casa do jogador, Verity Lakefront,
  Sandgem, R202. As vars de menor valência; estabelece o molde de cena.
- **S4 — arco Jubilife/Oreburgh/Eterna.** Jubilife (+Looker), Oreburgh
  (+portão), R203, R207, Eterna (cidade, bloqueio de saídas), Windworks
  (as duas), Floaroma se a fila cobrar.
- **S5 — arco Hearthome/Veilstone/Pastoria.** Hearthome, R209 portão,
  Solaceon, Veilstone (3 vars), Pastoria (3 vars), Celestic.
- **S6 — arco Galáctica/clímax.** QG (3 vars), Coronet (2), Acuity,
  Snowpoint, R217, Spear Pillar + Salão da Origem, Canalave, R218.
  Por último entre os de história: depende dos marcos dos arcos anteriores.
- **S7 — pós-liga e beira.** Sunyshore, Valor Lakefront, R224, R227 (Buck e
  Wake/rival), Stark, Resort, Villa, Mansão, Fight Area (a fila corrige o
  falso "sem bloqueio" dele desde 15/08). Amity Square (decisão 4, só
  warps) entra aqui por ser trabalho de mapa, não de cena.
- **S8 — QA.** `maquina_sinnoh.py --demo`, `fila_b6.py --gravar` (com as
  anotações de descarte das decisões 3, 4 e 6), casos de suíte novos (autor
  de caso ≠ autor de cena, prova por EWRAM, par negativo obrigatório), build
  e T11 pelo checklist do fechamento.

## O que fica de fora, dito

- Acompanhantes (decisão 5) e Pokécenter/Mart (decisão 6): na fila, com
  bloqueio nomeado.
- `Route210_North` (2 grupos): bloqueado por mapa não importado.
- Biblioteca de Canalave: continua sem escopo escrito (herdado do ESTADO 0).
- Os 29 de Unova e 4 de Johto não são desta obra.
