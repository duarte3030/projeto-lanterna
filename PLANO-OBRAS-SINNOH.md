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
  2508-2519, times literais da fonte com o remapeamento da curva conferido
  contra irmãos já escalados). Onda 4. **Ids e nomes PRÉ-ATRIBUÍDOS pela
  condutora (18/08)** para as duas frentes da onda citarem sem corrida:
  2508 `TRAINER_SINNOH_RIVAL_PASTORIA_TURTWIG`, 2509 `_CHIMCHAR`,
  2510 `_PIPLUP`; 2511 `TRAINER_SINNOH_RIVAL_ROUTE_209_TURTWIG`,
  2512 `_CHIMCHAR`, 2513 `_PIPLUP`. Quem define é o executor de
  treinadores; quem cita em cena usa esses nomes literais.
- **Onda 5 (18/08), pré-atribuição da condutora**: 2514
  `TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_GALACTIC_HQ` (a batalha do Cyrus no
  4F do QG, time literal da fonte, executor de treinadores define e liga a
  cena do 4F). O escritor que falta de `VAR_SINNOH_PASTORIA_ESTADO=1` é a
  cena do HM Fly do `VeilstoneCity_GalacticWarehouse`
  (`scripts_veilstone_city_galactic_warehouse.s:89` na fonte), que entra na
  S7 junto com a bomba de Pastoria (Crasher Wake aparece como NPC de cena,
  SEM batalha, que é fiel à fonte no set-piece).
- **Fechos que moram em script de vitória de líder** (Veilstone counterpart
  na vitória da Maylene; rival do portão 209 na vitória da Fantina): é
  fiação de cena, NÃO polimento de time (decisão 2 do Gui intocada); o
  executor da onda 4 edita só o trecho pós-vitória do scripts.inc do
  ginásio, sem tocar em time.
- Set-piece da bomba de Pastoria + BlockGreatMarsh: onda 4, junto do arco
  S6 (é Equipe Galáctica). FaceBoard/Croagunk cruza com Valor Lakefront e
  fica para a S7, como o plano já previa.

### Registros da onda 4 para o S8 (18/08/2026, consertador)

- **`coord_event` herdado do S1 em tile decorativo de portão, 4 casos.** Os
  dois portões de molde 13x9 (`Route209_Access` e `Route218_West`) têm três
  linhas jogáveis (y=4,5,6) e duas linhas decorativas sem ligação com o
  resto do mapa, y=2 e y=8. O gerador do S1 plantou gatilho nessas linhas:
  `Route209_Access` (5,2) e (5,8), `Route218_West` (7,2) e (7,8). Não são
  bug de cena e não foram tocados: são a mesma calibração de andabilidade
  que a decisão do S1 já mandou o S8 escrever (`maquina_sinnoh.py` conferir
  o tile plantado contra `map.bin`). Quando essa checagem entrar, ela deve
  varrer também os gatilhos já gravados, não só os novos.
- **Coordenada convertida pode cair em parede no meio da coreografia.** Em
  `PastoriaCity`, a rota da fonte (descer 9, andar 4 a oeste na linha do
  jogador) atravessa quatro tiles de colisão 1 depois da conversão
  proporcional; a cena foi desviada para a linha 27, que está livre, e o
  desvio está escrito no `scripts.inc`. `applymovement` de NPC ignora
  colisão, então o sintoma é visual, não travamento: o S8 não vai achar
  isso rodando o jogo, só medindo o `map.bin` contra o movimento.
- **`VAR_SINNOH_PASTORIA_ESTADO=1` e `VAR_SINNOH_QG_SALA_CONTROLE_ESTADO`**
  eram os dois gatilhos sem escritor da onda. O segundo foi portado (mora na
  vitória do Saturn, `scripts_galactic_hq_control_room.s:47`, com o par que
  volta a 0 no botão, linha 184). O primeiro continua sem escritor de
  propósito: quem grava o 1 na fonte é a cena do armazém da Galáctica em
  Veilstone (`scripts_veilstone_city_galactic_warehouse.s:89`), que este
  porte ainda não tem. Quem escrever o armazém leva o `setvar` junto.

### Decisões da condutora sobre os retornos do S7 (18/08/2026)

- **Decisão 4 (Amity) CORRIGIDA pela fonte**: os 27 gatilhos não são warps
  de saída, são reposicionamentos INTERNOS (pulos de cerca dentro da praça,
  via applymovement), e o nosso Amity é passagem provisória com planta
  emprestada. Nada a portar enquanto o exterior real do Platinum não for
  importado; os 27 ficam descartados-por-mapa-provisório na fila, e a
  importação do mapa real vira pendência FORA desta obra (registrar na
  regeneração).
- **Villa/Resort**: a máquina de visitantes (`VAR_RESORT_VILLA_VISITOR` e
  afins) não existe neste motor; os grupos e gatilhos dependentes ficam
  ADIADOS por mecânica, mesma categoria da decisão 5. Não inventar.
- **Bomba de Pastoria, leva final (junto do S8)**: AUTORIZADAS
  `FLAG_SINNOH_ESCONDE_PASTORIA_WAKE` (0x1B9F) e
  `FLAG_SINNOH_ESCONDE_PASTORIA_CROAGUNK` (0x1BA0). A nota de 18/08 sobre o
  Warehouse escrever `VAR_SINNOH_PASTORIA_ESTADO=1` está DESATUALIZADA (o
  Warehouse foi redesenhado sem a var e está provado): o executor da leva
  final alinha os valores da corrente de Pastoria ao fluxo NOSSO já
  commitado, documentando o desvio da fonte valor a valor.
- **PokemonLeagueNorthPokecenter1F**: batalha com treinador da fonte entra
  na leva final com id PRÉ-ATRIBUÍDO 2515 (nome conforme a fonte, executor
  mede o time como sempre). Se a fonte não tiver treinador ali, reporta.

### Registros da onda 5 para o S8 (18/08/2026, consertador)

- **Buck da Route 227: `coord_event` embaixo do próprio corpo, e é o ÚNICO
  vermelho de `maquina_sinnoh.py --demo` hoje.** O objeto
  `LOCALID_ROUTE227_BUCK` (sem flag de esconder) está em (30,19) e o gatilho
  de `VAR_SINNOH_R227_BUCK_ESTADO == 0` está no MESMO tile, ou seja,
  inalcançável. O `--demo` para exatamente aí ("gravado em (30,19), tile
  inandavel que o gerador nao sabe realocar"), e para SÓ aí: rodando a mesma
  checagem sem `assert`, o repo inteiro tem 1 tile ruim gravado, este. O
  gerador, hoje, já sabe a resposta: o censo dele traz o Buck com
  `tiles_movidos [[33,19] -> [29,19]]`, isto é, o tile certo é **(29,19)**, e
  (30,19) é resto de uma gravação anterior. Não foi mexido nesta onda porque
  a condutora pediu registro, não conserto, e porque a cena vive pelo clique
  (o `script` do objeto é `Route227_EventScript_AskPatrolStarkMountain`, o
  mesmo corpo), o que é fiel à fonte. Para o S8 é uma linha: mover o
  `coord_event` para (29,19) fecha o `--demo`.
- **Grunts da Stark: cena morta por mapa provisório**
  (descartado-por-mapa-provisório na regeneração da fila, mesma categoria do
  Amity da decisão 4 corrigida). `StarkMountainOutside` usa
  `LAYOUT_ROUTE226_ACCESS`, o molde de portão 13x9 com três linhas jogáveis
  (y=4,5,6) e duas decorativas (y=2 e y=8), exatamente o caso registrado na
  onda 4. Medido no `map.bin`: o gatilho está em (6,2), linha decorativa sem
  ligação com o corredor; o Grunt 1 em (3,2) mora na mesma linha morta e o
  Grunt 2 em (4,3) está em colisão 1. A cena (diálogo, coreografia, `setflag`
  + `removeobject`, `setvar` para 1) está escrita e correta; ela só volta a
  existir quando o exterior real da Stark Mountain for importado. Não foi
  reposicionada porque mover NPC e gatilho para o corredor do portão seria
  inventar geografia de um mapa que ainda não é o mapa.
- **Valor Lakefront: o bloqueio do Collector fecha UMA das duas saídas.**
  Medido no `map.bin` de `LAYOUT_VALOR_LAKEFRONT` (56x66) com busca em
  largura: da praça saem duas ligações andáveis para `MAP_ROUTE222` (a
  estrada de Sunyshore), a sul pela borda direita nas linhas 57 a 61 e a
  norte pelo corredor de uma casa de altura da linha 39 (chegando pelo
  corredor vertical x=49). O corte mínimo para fechar as duas de uma vez são
  dois tiles longe dali, no gargalo (34,55)/(34,56), que também trancaria
  Lake Valor, a Route 214 e a casa leste: bloqueio errado. O gatilho desta
  obra (span de 3 da fonte) foi posto na seção inteira da estrada sul,
  (45,57)/(45,58)/(45,59), com o Collector em (46,58). A saída norte fica
  aberta; fechá-la pedia um segundo bloqueador que a fonte não tem.
- **`MAP_ROUTE222` está partida no meio (fora desta obra, mas relevante).**
  ~~Busca em largura no layout dela: nenhuma das entradas do lado de Valor
  (coluna x=0, linhas 3,4,7,10,21,22,23,24,25,27,31) alcança a coluna x=91,
  que é a borda de Sunyshore. Ou seja, hoje a estrada Valor -> Route222 ->
  Sunyshore não é andável de ponta a ponta, independentemente do Collector.
  Pendência de mapa, não de cena.~~
  **DIAGNÓSTICO SUPERADO EM 18/08/2026.** O texto riscado acima fica de
  propósito, porque o erro dele é instrutivo: a medição estava certa e a
  conclusão não. Ver a correção datada logo abaixo.

- **Escritores de var achados e ligados nesta onda** (ficam anotados para
  quem for reconferir a corrente): `VAR_SINNOH_SUNYSHORE_ESTADO = 2` mora na
  vitória contra o Volkner (fonte
  `scripts_sunyshore_city_gym_room_3.s:51`; aqui
  `SunyshoreCity_Gym_EventScript_Leader`), e `VAR_SINNOH_VILLA_ESTADO = 1`
  mora na tabela de frame da própria Villa (fonte `scripts_init_villa.s:9` +
  `Villa_OnFrame_FirstEntry`; aqui `Villa_OnFrameTable`). Continua SEM
  escritor, de propósito, `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE = 1`: quem
  grava na fonte é a cena pós-8ª insígnia do laboratório de Sandgem
  (`scripts_sandgem_town_pokemon_research_lab.s:110-111`), que este porte não
  tem. Mesmo tratamento do `VAR_SINNOH_PASTORIA_ESTADO = 1` da onda 4.

### CORREÇÃO DE ROUTE 222, 18/08/2026 (fora de onda, condutora Fable, executor Opus)

**A coluna 91 nunca foi a estrada, então medi-la não dizia nada sobre ela.**
A Route 222 entrega em Sunyshore por WARP, não pela costura de mapa: warp 0 em
`(89,23)` -> `Route222_Access` -> warp 1 em `(11,5)` -> `SunyshoreCity (4,48)`,
e os três disparam (`valida_warp_tile.py`, Sinnoh em 97,7%). A borda direita do
layout tem terra só em `(91,13)` e `(91,14)`, um bolso de dois tiles que a
fonte desenha como anel decorativo; do outro lado da costura a coluna x=0 de
`SunyshoreCity` é água ou parede em TODAS as linhas (medido: sy=0..13 e
sy=55..63 em elevação 1, o resto colisão 1). Abrir a coluna 91 não levaria a
lugar nenhum, e por isso ela continua intocada.

**O que estava partido de verdade era a ENTRADA NORTE**, e era pior do que o
registrado: das 11 entradas da coluna x=0 só duas têm vizinho andável do lado
de Valor E são alcançáveis dentro do próprio `ValorLakefront` (as outras,
`(55,43)`, `(55,46)` e `(55,63)`, não são alcançáveis lá). São a do sul
(Route222 y=21..25), que é a que o Collector tranca e que **não desarma neste
porte**, e a do norte (y=3), que o bullet acima diz que "fica aberta" de
propósito. A norte caía num **bolso de 4 tiles**, `(0,3)` a `(3,3)`: linha 3 em
elevação 3, região grande logo abaixo em elevação 4, e `IsElevationMismatchAt`
(`src/event_object_movement.c:10010`) barra 3 contra 4 sem nada aparecer na
colisão (lição 6 do ESTADO 0.e). Somando as duas, **Sunyshore era inalcançável
a pé vindo de Valor**.

**O conserto vive em `dev_scripts/conserta_route222.py`** (com `--demo` de
mutação plantada, idempotente): `(0,3)`, `(1,3)` e `(2,3)` passam a
`ELEVATION_TRANSITION`, o idioma que o próprio mapa já usa em `(21,10)`,
`(21,11)`, `(21,19)`, `(21,20)`, `(39,10)`, `(39,11)`, `(81,18)` e `(81,19)`.
Diff binário contra o HEAD anterior: **3 palavras**, metatile e colisão
idênticos, arquivo com os mesmos 5888 bytes, `guarda_save.py` sem `--gravar`
seguindo SAVE COMPATIVEL. Depois disso, 9 das 11 entradas da coluna 0 alcançam
o portão com 1143 tiles cada (a norte dava 4); as duas que sobram são `(0,27)`,
praia de 22 tiles cujo lado de Valor não é alcançável, e `(0,31)`, que é água.

**Prova: `T107.1`** em `dev_scripts/testes_criticos/107_pendencias.json`.
Atravessa `ValorLakefront` -> Route 222 inteira -> portão -> `SunyshoreCity`
por rota medida no traço de EWRAM, e é discriminador de verdade: revertendo os
três tiles para elevação 3 e recompilando, ele fica vermelho com "mapa errado:
obtido MAP_ROUTE222". Suíte completa na build do conserto: **358/359**, só o
`T11.3` pulado (é o caso de duas ROMs).

**NÃO foi feita reconversão do blockdata pela fonte**, e o motivo é medido: a
grade do pokeplatinum (`map_data_149/150/151.bin`, as três células de
`MAP_HEADER_ROUTE_222`) alinha com o nosso layout em dx=0 / dy=+2 com **81,7%
de acordo** na máscara de bloqueio, ou seja o mapa é um redesenho à mão (commit
`f97a18dc82`), não uma conversão. A fonte não tem elevação por tile (as três
células têm `altitudes` 0), então reconverter apagaria a elevação 4 da metade
oeste, que CASA com o `ValorLakefront` em y=21..25 e é o que faz a estrada sul
existir, e levaria junto a arte, os dois warps de casa (prédio de gen 4 é
modelo 3D, a grade só entrega buraco bloqueado) e os 23 `object_events`.

~~**Fica aberto, dito:** a estrada sul continua trancada de propósito, sem
escritor para `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE`, então o jogo tem UMA
estrada a pé para Sunyshore, a norte.~~ **FECHADO no mesmo 18/08/2026, na onda
de pendências**: o escritor entrou em `data/maps/SandgemTown_RowanLab/
scripts.inc` (`SandgemTown_RowanLab_EventScript_RowanAbreSunyshore`). Na fonte
quem escreve é `SandgemTownLab_ObtainSunyshoresBadge`, chamado pelo ON_FRAME da
volta do Mundo Distorcido; como o Distorcido não está portado, o gatilho aqui é
`FLAG_GALACTICA_QG_TOMADO`, o último passo do arco da Galáctica que existe nesta
ROM e que na fonte fica imediatamente ANTES do Coronet/Spear Pillar/Distorcido
(o texto da fonte concorda: "You've got seven already! That only leaves
Sunyshore's Gym"). Zero flag e zero var novas: quem marca "já aconteceu" é a
própria `FLAG_SINNOH_ESCONDE_VALOR_LAKEFRONT_COLLECTOR` que a cena acende.
Provas **T107.2** (var 0x415B vira 1 e a flag acende) e **T107.3** (par
negativo, sem a flag da Galáctica nada é escrito); o efeito da var na estrada já
era provado por T103.5/T103.6, que a pinam na mão.

E a busca em largura desta casa **não
modela `SIDEWAYS_STAIRS`**: a Route 222 tem escada lateral nas colunas 21, 28,
39 e 46, que desloca o jogador uma linha ao andar de lado. Aqui não atrapalhou
porque o degrau era de elevação pura, mas qualquer conta de alcance em mapa de
Sinnoh com escada lateral é conservadora demais e tem que ser conferida no
traço.

### AMITY SQUARE E STARK MOUNTAIN OUTSIDE: medição feita, execução PARADA (18/08/2026)

Decisão da condutora: os dois **ficam parados** e vão para a **fila de
conteúdo**, não entram em onda agora. Esta seção existe para a fase de conteúdo
não remedir nada; tudo abaixo foi lido da fonte e do repo em 18/08/2026, nada é
estimativa de memória. Hoje os dois usam `LAYOUT_ROUTE226_ACCESS`, o molde de
portão 13x9, e estão marcados na fila como descartados-por-mapa-provisório.

**Nenhum dos dois precisa de tileset, tile ou gráfico novo.** Conferido na
tabela de atributos: todos os metatiles que a tradução do `demake_ds.py` usa
(1 chão, 13 grama alta, 161 água parada, 368 água do mar, 470/471/478/479
árvore bloqueante) já existem no `gTileset_GeneralSinnoh`, que tem 512
metatiles e é o primário da maioria dos layouts de Sinnoh. O que falta não é
tile, é **arte**: a grade 2D entrega grama com parede de árvore, e o desenho
real dos dois (o jardim do Amity, a encosta vulcânica da Stark) é modelo 3D que
a grade não carrega. Vale a taxa já registrada no `DEMAKE-DS.md`, 1 a 3 h de
acabamento à mão por lugar.

**AmitySquare**
- Matriz PRÓPRIA, `map_matrix_050`, 2x2 células, **64x64**, nível único
  (`altitudes` vazio). 4096 tiles, **2212 bloqueados (54%)**; comportamentos
  0x00 (1658 andáveis), 0x10 água parada (221) e 7 tiles soltos.
- **As coordenadas dos eventos da fonte são LOCAIS** (x 10..53, z 17..51,
  dentro do 64x64), porque o mapa tem matriz só dele. Ou seja o alinhamento é
  de graça. Isso **corrige a leitura larga da decisão 5 do
  `importa_npcs_sinnoh.py`** ("coordenada de exterior é GLOBAL e não há offset
  que alinhe"): aquilo vale para mapa que divide a `map_matrix_000`, não para
  quem tem matriz própria.
- Fonte: 4 warps (dois pares de porta em z=51, que são os dois portões de
  Hearthome), 16 objetos, 31 coord_events. Hoje temos 1 warp e zero eventos.

**StarkMountainOutside**
- UMA célula da `map_matrix_000`, em (23,7), **32x32**, nível único. 1024
  tiles, **763 bloqueados (74,5%)**, 98 de grama alta (0x02), 12 bloqueados de
  0x4B e 1 de 0x6E. Tem tabela de encontro selvagem
  (`encounters_stark_mountain_outside`) e clima de cinza.
- As coordenadas dos eventos são GLOBAIS (x 740..762, z 231..248), mas a célula
  é identificável, então **o offset é exato: (736, 224)**. Alinha tile a tile,
  sem adivinhação.
- Fonte: 1 warp, 8 objetos, 1 coord_event.
- **DECISÃO FUTURA DA CONDUTORA COM O GUI, não do executor:** a fonte tem UM
  warp só, para `StarkMountainRoom1`. A volta para a Route 227 **não existe
  lá**, porque o Platinum entra nesse mapa ANDANDO pela matriz, não por porta.
  A nossa planta provisória tem essa porta de volta. Converter o mapa real sem
  resolver isso deixa a Stark Mountain de MÃO ÚNICA, que é a lição 4.1 do
  ESTADO e o erro que o `abre_exteriores_sinnoh.py` já pagou uma vez ("os três
  exteriores nasceram com entrada boa e SEM saída"). As duas saídas possíveis
  são inventar a porta de volta ou assumir a mão única; nenhuma é escolha de
  executor.

**Custo e risco do dia em que entrar.** Encanamento: um layout novo apendado
por mapa (`map.bin` de 8 KB para o Amity, 2 KB para a Stark, mais borda e
registro), append puro, save-compatível pela mesma régua do resto. A ROM está
em **98,54% de 32 MB**, então os ~10 KB cabem, mas o orçamento está apertado e
tem que ser reconferido na hora. E o trabalho maior **não é de mapa**: entrar
com os mapas reais reabre o bloco de CENA que a obra fechou por mapa
provisório, os 27 itens do Amity mais os 16 NPCs, e os 8 da Stark.


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

### POVOAR OS MAPAS VAZIOS DE SINNOH: o que a medição achou, 18/08/2026

**A premissa da onda estava errada, e a medição é curta de explicar.** A onda
nasceu para levar "1235 objetos que a fonte tem em mapas que entraram vazios"
para dentro da ROM. Medido mapa a mapa (`dev_scripts/npcs_sinnoh_censo.tsv`,
gerado pelo `importa_npcs_sinnoh.py`, 1236 linhas): os mapas nossos com ZERO
`object_events` cujo par na fonte tem objeto são **62**, e a fonte põe neles
**594 objetos**, assim repartidos:

| bucket | quantos | régua que barra |
|---|---|---|
| mobiliário e item | **497** | decisão 4 do gerador |
| nome próprio sem sprite | 31 | decisão do Gui, 05/08 |
| `hidden_flag` | 22 | decisão 2 do gerador |
| **elegível a virar NPC mudo** | **44** | — |

E dos 497 de mobiliário, **447 são `OBJ_EVENT_GFX_ROCK_SMASH`**, quase todos
nas sete salas da Turnback Cave (30 por sala) e no Mt Coronet. Ou seja: o buraco
de objetos de Sinnoh **não é gente que falta, é pedra que falta**. Enquanto a
decisão 4 valer como está, Sinnoh tem um teto de completude de objetos bem
abaixo de 100%, e nenhuma onda de NPC muda isso.

**DECIDIDO PELA CONDUTORA NO MESMO 18/08/2026, e FEITO: as pedras entram.** A
decisão 4 do `importa_npcs_sinnoh.py` proíbe virar BONECO, e nunca proibiu
portar obstáculo como obstáculo; pedra de Rock Smash é obstáculo funcional do
Platinum, então trazê-la é fidelidade, não invenção. A emenda está escrita na
própria decisão 4, com a data, para ninguém reabrir isto lendo a versão velha.
Quem faz é `dev_scripts/pedras_sinnoh.py`, com `OBJ_EVENT_GFX_BREAKABLE_ROCK` e
`EventScript_RockSmash`, os dois nativos e os mesmos da Route 111 de Hoenn. O
risco que a decisão 4 temia (trancar quem não tem Rock Smash) virou PORTÃO
MEDIDO, e ele manda mais que a fidelidade; está detalhado logo abaixo.

**O que entrou nesta onda: 39 objetos em 20 mapas** (5 NPC mudos, 34 placas),
todos por `importa_npcs_sinnoh.py --aplicar`, append no fim da lista de objetos
do mapa, sem flag, item, mapa nem heal location novos. Custo de ROM calculado
pelos tamanhos de struct (`ObjectEventTemplate` 0x18, `BgEvent` 0x0C):
`5*24 + 34*12 = 528 B`. Provas: `T113.1` a `T113.4`.

**Três portões novos no gerador, e o primeiro é o que mais recusou.**

1. **Planta provisória, e o critério é COMPARAÇÃO DE `map.bin` CONTRA O MOLDE
   DE PORTÃO, nunca nome de mapa** (`data/layouts/Route226_Access/map.bin`;
   quem for medir o próximo não precisa refazer a descoberta, só rodar
   `importa_npcs_sinnoh.planta_provisoria`). `AmitySquare`,
   `StarkMountainOutside`, `BattleFrontier`, `IronIsland`, `SendoffSpring`,
   `PalPark`, `GreatMarsh6`, `Route204North`, `MtCoronetOutsideNorth`,
   `MtCoronetOutsideSouth`, `SpringPath` e `TrophyGarden` **não têm mapa: têm
   o molde de portão 13x9**. `SendoffSpring` não estava em lista de suspeito
   nenhuma e caiu por medição, que é exatamente a razão de o critério ser
   medida. Os 12 estão na fila como UM item,
   `sinnoh:planta_provisoria:12_mapas_de_molde`, com o prêmio medido e o
   critério de aceite (geometria real primeiro, objeto depois); os 10 de escala
   viraram `sinnoh:escala_nao_provada:10_mapas`.
   Medido byte a byte: `BattleFrontier` e `IronIsland` têm `map.bin` próprio e
   mesmo assim são idênticos ao `Route226_Access/map.bin` em todas as linhas
   menos a `y=1`, onde as portas são furadas (4 e 2 tiles de diferença). O
   critério do gerador é esse, não uma lista de nomes. **Recusa o maior prêmio
   da onda de propósito**: só o Battle Frontier tinha 24 NPC e 25 placas
   elegíveis, espalhados numa área de 48x47 da fonte que não cabe honestamente
   em 117 tiles.
2. **Escala não entra em mapa que nasce agora.** A conversão por proporção é a
   regra que a correção da Route 222 provou errada, e aqui ela nem chega perto:
   em `MtCoronet_1F_North_Room2` a caixa da matriz mede 1x1 e a conta joga todos
   os eventos em (0,0). Os 10 mapas que só têm escala (`ValorLakefront`,
   `LakeValor`, `LakeVerity`, `SpearPillar`, `GalacticHQ_B2F`,
   `HearthomeCityGymLeaderRoom`, `VeilstoneCity_GalacticWarehouse`,
   `JubilifeCity_Flat1_F3`, `MtCoronet_1F_North_Room1` e `_Room2`) vão para a
   fila de conteúdo, para medição um a um como a Route 222 teve. Em troca, a
   **translação provada por warp deixou de precisar da lista `REDESENHO_1PARA1`
   quando o mapa está VAZIO**: a lista existe porque mudar a régua de quem já
   tem placa gravada órfã a placa, e onde nada foi gravado não há nada a
   órfãnar. Quem já tem conteúdo continua recebendo a conta de antes, byte a
   byte (`itens_escondidos_sinnoh`, `texto_sinnoh`, `maquina_sinnoh`,
   `fila_b6`), porque o parâmetro novo é `vazio=` e o padrão é `False`.
3. **Posição provada, não empurrada.** NPC tem que cair em tile ALCANÇÁVEL pela
   BFS com regra de elevação (`conserta_route222.alcance`, reusada, semeada
   pelos nossos warps), com empurrão de no máximo 1 tile; o `livre()` de raio 8
   não vale para mapa que nasce agora, porque raio 8 é invenção de posição.
   Placa exige tile de leitura andável, o critério da Route 222. O censo marca
   as placas que são legíveis mas cujo tile de leitura não sai dos warps a pé,
   que em Mt Coronet quase sempre quer dizer Surf ou Strength.

**O que NÃO foi tocado, dito:** os 360 mapas que já tinham import não foram
reabertos (a marca `origem` os pula, e a onda é de mapa vazio); Amity Square e
Stark Mountain Outside continuam parados pela decisão de 18/08, agora também
pelo portão medido; nenhuma flag, var, item, mapa ou heal location foi criado.

### AS PEDRAS DE ROCK SMASH DE SINNOH ENTRARAM, 18/08/2026 (decisão da condutora)

Ferramenta: `dev_scripts/pedras_sinnoh.py` (idempotente, `--demo` com duas
mutações plantadas, censo em `dev_scripts/pedras_sinnoh_censo.tsv`, 591 linhas).
**478 pedras em 28 mapas**, como `OBJ_EVENT_GFX_BREAKABLE_ROCK` com
`EventScript_RockSmash`, os dois nativos e os mesmos da Route 111 de Hoenn.

| onde | quantas |
|---|---|
| as 12 salas de pilar 2 e 3 da Turnback Cave | 29 cada, 348 |
| as 6 salas de pilar 1 da Turnback Cave | 11 a 13, 74 |
| `MtCoronet1FTunnelRoom`, `MtCoronet_B1F`, `MtCoronet4FRooms1And2`, `MtCoronet_1F_South` | 32 |
| `WaywardCave1F`, `SinnohVictoryRoad2F`, `RavagedPath`, `OreburghGate_1F`, `SnowpointTempleB2F`, `StarkMountainRoom2` | 24 |

**A FLAG: esta onda NÃO GASTA FAIXA NENHUMA, e a conta é esta.**
`EventScript_RockSmash` termina em `removeobject`, que faz
`FlagSet(GetObjectEventFlagIdByObjectEventId(...))`
(`src/event_object_movement.c:1700`). Duas medições:

- **`flag: "0"` seria veneno.** O spawn lê `!FlagGet(template->flagId)` sem
  guarda de `flagId != 0` (`src/event_object_movement.c:2893`), então quebrar
  uma pedra de flag 0 acenderia a flag 0 e sumiria com TODO objeto de flag 0
  do mapa, que é quase todo NPC do jogo.
- **Flag permanente não é preciso.** A faixa `FLAG_TEMP_*` (`TEMP_FLAGS_START`
  0x0 a `TEMP_FLAGS_END` 0x1F) é zerada na troca de mapa e não é estado de
  jogo: pedra quebrada fica quebrada enquanto o jogador está na sala e volta
  quando ele sai e entra, que é o comportamento do jogo original. **Zero flag
  nova, zero endereço das 4448 livres, `guarda_save.py` sem quebra nova.**

O preço disso é um TETO POR MAPA: **29 pedras**, que são as 31 temps de 0x1 a
0x1F menos `FLAG_TEMP_7` (é para onde `P_FLAG_FORCE_SHINY` aponta desde o
fechamento da Fase E: acendê-la faz todo selvagem nascer shiny) e
`FLAG_TEMP_E` (o motor usa para não criar o Pokémon que segue). Duas pedras
com a mesma temp somem juntas, então cada pedra do MESMO mapa precisa da sua;
mapas diferentes reusam à vontade. **Custou 8 pedras**, uma em cada sala de
pilar de 30, cortadas pela ordem da fonte.

**O PORTÃO QUE MANDA MAIS QUE A FIDELIDADE, e ele mordeu.** Antes de gravar,
`pedras_sinnoh.py` prova por BFS com regra de elevação, tratando toda pedra
nova como bloqueio e SEM Rock Smash na mochila, e a aceitação é UMA A UMA (a
pedra entra se, junto com as já aceitas, o mapa continua bom; medir as 30 de
uma vez reprovaria e jogaria fora as 29 boas). São dois portões, e o segundo
existe porque o primeiro tem um ponto cego medido:

1. **Não perder ligação que existia.** Todo alvo da LINHA DE BASE (pouso de
   warp e tile de leitura de item que já se alcançavam com zero pedra)
   continua alcançável. A régua é a linha de base e não a conectividade
   absoluta porque 6 mapas já nascem com warp fora do alcance a pé
   (`Route213` com 6 alvos soltos, `MtCoronet4FRooms1And2` com 2,
   `MtCoronet_1F_South`, `RavagedPath`, `Route210_North` e `WaywardCave1F`
   com 1 cada; a fonte pede Surf ou Strength ali e a BFS não modela nenhum
   dos dois). Cobrar perfeição reprovaria toda pedra por defeito que não é da
   pedra. **Recusou 2.**
2. **Ninguém fica preso.** Todo tile pisável antes das pedras ainda chega a
   algum warp depois delas. Este portão existe porque em `WaywardCave1F` e
   `MtCoronet4FRooms1And2` a linha de base liga UM alvo só, e com um alvo só o
   portão 1 não tem dente nenhum. **Recusou 12.**

Os dois estados são provados, não um: com as pedras e com tudo quebrado, mais
a inclusão `alcance com pedra ⊆ alcance sem pedra`, que é asserção do gerador
e falha alto se a conta inverter.

Outras recusas, todas com tile e motivo no censo: **31 por tile não andável**,
e essa merece leitura, porque não é defeito do gerador: `demake_ds.traduz_gen4`
converte tile com bit 0x8000 em PAREDE, e a fonte marca o tile da pedra como
bloqueado. Ou seja **a nossa conversão já assou boa parte das pedras dentro da
parede**, e nesses lugares a passagem não está fechada por pedra quebrável,
está fechada por rocha. `RavagedPath` é o caso extremo: 17 das 27 pedras dela
são parede aqui, e o warp norte dela já era inalcançável a pé antes desta onda.
Isso é dívida de GEOMETRIA, não de objeto, e está dita aqui para a fase de
conteúdo não remedir. Mais **21 por planta provisória** e **39 por escala não
provada**, os mesmos dois portões da onda de NPC.

**Provas: `T113.5` (a pedra é sólida, sala de pilar da Turnback), `T113.6` (a
linha de parada ANDA JUNTO com a pedra ao trocar de coluna, que é o que separa
"tem pedra" de "aquela linha é intransponível") e `T113.7` (par negativo: a
linha 4 da mesma sala não tem pedra e o jogador atravessa a sala inteira).**

---

## OS MAPAS DE MOLDE: o conversor está pronto, a decisão não (21/08/2026)

`dev_scripts/converte_moldes_sinnoh.py` converte os mapas que vestem o molde de
portão 13x9 pela grade 2D do Platinum. `--dry-run` imprime uma linha por mapa,
`--demo` é o autoteste com mutação plantada, e `--aplicar <mapa>` escreve, um
mapa por vez de propósito. **Os 12 exteriores continuam parados por decisão de
gosto do Gui** (a arte cai de 46-48 metatiles distintos para 6-10, o que leva
Sinnoh de 104 para 116 mapas abaixo do piso da régua); o que travava por
FERRAMENTA não trava mais.

**Eram 13 e não 12.** O `OreburghGateB1F` vestia o segundo molde
(`LAYOUT_ROUTE208_ACCESS`) e ficou fora da lista escrita à mão da fila. O
`planta_provisoria` sempre pegou os dois moldes; o texto da fila é que mentia.
Ele é caverna na fonte, foi convertido em 21/08/2026 (64x32, `map_matrix_004`)
e a fila passou a tirar a lista da medição em vez da mão.

**Tile debaixo do warp, medido e não decorado.** Warp não dispara em chão comum
neste motor: quem dispara é o comportamento do metatile. A primeira conversão do
`OreburghGateB1F` gravou o warp sobre o metatile 513 e o mapa nasceu de MÃO
ÚNICA. A tabela abaixo saiu de varrer os dois `metatile_attributes.bin` de
Sinnoh e conferir os warps que já funcionam:

| destino | tile | comportamento |
|---|---|---|
| de caverna para caverna | 575 | `MB_LADDER` |
| de caverna para fora | 519 | `MB_SOUTH_ARROW_WARP` |
| de exterior para lugar fechado | 167 | `MB_NON_ANIMATED_DOOR` |
| de exterior para exterior | 484 / 36 / 94 / 93 | seta N / S / L / O |

Porta ANIMADA (33, 65, 97, 461, 475, 553, 556, 594) é casada com a fachada do
prédio e por isso não entra: Sandgem usa três delas em três portas vizinhas. As
setas saem do `gTileset_GeneralSinnoh`, que é o primário de todos os layouts de
Sinnoh, porque as do `gTileset_PetalburgSinnoh` só existem em norte e sul e
deixariam metade das bordas sem valor.

**A porta de volta da Stark Mountain é INVENTADA, por decisão do condutor em
21/08/2026**, e está declarada em `PORTAS_INVENTADAS`. A fonte tem um warp só
(entra-se andando pela matriz do mundo) e converter cru deixaria a Stark de mão
única, o que a lição 4.1 do ESTADO proíbe.

**DOIS CASOS DA SUÍTE FIXAM O MOLDE DO SENDOFF SPRING E VÃO QUEBRAR NO DIA DA
CONVERSÃO.** Quem converter reescreve os dois na MESMA rodada, senão a suíte
fica vermelha por motivo certo e ninguém entende:

- **`T93.6`** prova `layout: LAYOUT_SENDOFFSPRING`, que é o molde 13x9. Com a
  planta nova o id do layout muda e a prova cai sozinha.
- **`T85.1`** anda `16:RIGHT*11` dentro do `SendoffSpring` e prova a chegada em
  `MAP_TURNBACK_CAVE_ENTRANCE`. A rota é de um mapa de 13 colunas; no 64x64
  convertido ela não chega a lugar nenhum.

Régua para as rotas novas: a andabilidade se mede por COLISÃO **e ELEVAÇÃO**
(o lago do OreburghGateB1F tem colisão zero e elevação 1, e quem só olhou
colisão achou caminho que o jogador não pode fazer), e neste harness **a
primeira tecla de uma direção nova só VIRA o boneco**, não anda.
