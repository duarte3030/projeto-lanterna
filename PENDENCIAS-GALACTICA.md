# Pendências da Equipe Galáctica

Escrito pela sessão que criou os 17 mapas da Galáctica (QG de Veilstone, prédio
de Eterna, Spear Pillar e armazém). Tudo aqui é coisa que **não** podia ser
feita nesta tarefa porque os arquivos estavam com outro agente, ou porque exigia
flag/var nova. Quem orquestra registra.

## 1. BLOQUEIA O BUILD: quatro treinadores que não existem

Sem estes quatro `#define`, o link falha com símbolo indefinido. Foi opção
deliberada: a instrução era montar a cena com o nome que o treinador **deve**
ter, em vez de reusar um treinador errado só para compilar.

Entram em `include/constants/opponents.h` (os ids são sugestão: o maior id em uso
hoje é 1310, `TRAINER_JOHTO_LEADER_CLAIR`):

```c
#define TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING        1311
#define TRAINER_SINNOH_COMMANDER_MARS_SPEAR_PILLAR              1312
#define TRAINER_SINNOH_COMMANDER_JUPITER_SPEAR_PILLAR           1313
#define TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR         1314
```

E as entradas correspondentes em `src/data/trainers_sinnoh.party` (e no
`src/data/trainers.party`, que é onde as duas comandantes de hoje aparecem
duplicadas). Times do Platinum, com o nível do momento da história:

| Constante | Onde | Classe / nome | Time sugerido |
|---|---|---|---|
| `..._JUPITER_ETERNA_BUILDING` | `data/maps/TeamGalacticEternaBuilding_4F/scripts.inc` | Commander Jupiter | Zubat 18, Skuntank 20 |
| `..._MARS_SPEAR_PILLAR` | `data/maps/SpearPillar/scripts.inc` | Commander Mars | Bronzor 44, Golbat 44, Purugly 46 |
| `..._JUPITER_SPEAR_PILLAR` | `data/maps/SpearPillar/scripts.inc` | Commander Jupiter | Bronzor 44, Golbat 44, Skuntank 46 |
| `..._CYRUS_SPEAR_PILLAR` | `data/maps/SpearPillar/scripts.inc` | Galactic Boss Cyrus | Houndoom 45, Gyarados 46, Honchkrow 47, Weavile 47, Crobat 46 |

Espelhar o `trainerClass`/`trainerPic` no padrão que Mars e Saturn já usam.

## 2. Saturn do QG está reusando o Saturn do Lago Valor

`data/maps/GalacticHQ_ControlRoom/scripts.inc` chama
`TRAINER_SINNOH_COMMANDER_SATURN_VALOR_CAVERN`, que **já é usado** em
`data/maps/LakeValor/scripts.inc`. Consequência real: quem bater no Saturn no
lago primeiro chega na sala de controle com a cena já vencida (ele só fala).

Conserto: criar `TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ` (id 1315, time do
Platinum: Kadabra 34, Bronzor 34, Toxicroak 36) e trocar a chamada. As três
consultas `goto_if_defeated` do mesmo arquivo, e as duas de
`GalacticHQ_1F/scripts.inc`, passam a apontar para a constante nova.

## 3. ~~Flags que fariam a cena parar de se repetir~~ FEITO em 04/08/2026

As quatro flags foram criadas (0x38 a 0x3B) e estão registradas em
`SINNOH-PADRAO.md`. Detalhe:

| Flag | O que resolve |
|---|---|
| `FLAG_GALACTICA_LAKE_TRIO_FREED` (0x39) | o botão solta os três Pokémon uma vez só; depois responde que o console está morto |
| `FLAG_CAUGHT_DIALGA` (0x3A) / `FLAG_CAUGHT_PALKIA` (0x3B) | a fenda fecha em vitória ou captura. Fuga, derrota e teleporte deixam a fenda aberta de propósito, senão uma Poké Ball errada apagaria o lendário do save |
| `FLAG_GALACTICA_ETERNA` (0x38) | os três grunts da rua de Eterna somem depois da Jupiter. Quem liga a flag é um `ON_TRANSITION` novo em `EternaCity/scripts.inc`, que lê a flag de derrota da Jupiter, porque a cena dela mora no 4F do prédio (mapa de outro dono) |

## 4. ~~Itens-chave que ficaram de fora~~ FEITO em 04/08/2026

- **Galactic Key**: `ITEM_GALACTIC_KEY` (id 874) existe, está numa Poké Ball em
  `GalacticHQ_2F` (2,8), e dois guardas com `FLAG_GALACTICA_QG_CHAVE` (0x3C) ficam
  em cima do único tile de acesso às escadas de (13,1) no 2F e de (3,1) no 3F.
- **Storage Key**: reusa `ITEM_STORAGE_KEY` (a de Hoenn, mesmo nome). O Looker
  entrega a chave, e a porta enferrujada agora exige o item.
- **HM Fly**: entregue pela porta enferrujada, marcada por `FLAG_RECEIVED_HM_FLY`,
  que já existia e ninguém lia.

Tudo detalhado em `SINNOH-PADRAO.md`.

## 5. Bug pré-existente que NÃO foi tocado (é de outro dono)

Achado ao conferir os warps das duas cidades, e deixado como está porque mexer
em ginásio estava fora do escopo:

- `data/maps/EternaCity/map.json`, warp 1 em **(19,18)** para
  `MAP_ETERNA_CITY_GYM`: (19,18) não é tile de porta. Os tiles de porta desse
  prédio são **(16,17)** e **(21,17)**. Do jeito que está, o warp nunca dispara e
  o ginásio de Eterna é inacessível.
- `data/maps/VeilstoneCity/map.json`, warp 4 em **(33,34)** para
  `MAP_VEILSTONE_CITY_GYM`: mesmo problema. As portas livres da cidade estão em
  (38,14), (35,27), (41,27), (8,36), (41,36), (14,47), (20,47), (31,47), (40,47).

Motivo de warp não disparar: `src/field_control_avatar.c`,
`IsWarpMetatileBehavior` exige que o metatile do tile tenha behavior de warp
(porta, escada, escalator, painel). `warp_def` em chão comum é inerte.

## 6. Cenas que ficaram simplificadas de propósito

- **Discurso do Cyrus no salão do QG** não dispara sozinho ao entrar: gatilho por
  `coord_event` precisa de uma var para lembrar que já rodou. Falar com o Cyrus
  (ou com o Looker) roda a cena inteira, e ela pode ser revista.
- **Spear Pillar distorcido** é um mapa separado, alcançado por um portal que só
  aparece depois que o Cyrus cai (`setmetatile` no `ON_LOAD`). O Giratina e o
  Mundo Distorcido não existem: a Cynthia explica o Giratina e as duas fendas
  levam ao Dialga e ao Palkia.
- **Escada do Mt Coronet para o Spear Pillar** (`MtCoronet_1F_North_Room2`, tile
  (15,3)) está sempre aberta. Trancar até a hora certa da história pediria flag
  ou var.

## 7. Hall da Fama de Sinnoh: FEITO em 04/08/2026

`MAP_SINNOH_LEAGUE_HALL_OF_FAME` existe. Vencer a Cynthia leva o jogador para lá,
o time é registrado e o "Continue" pós-créditos cai em Sandgem Town, não em
Littleroot. Precisou de um special novo (`SetGameClearHealLocation`), porque
`GameClear` cravava a volta em Hoenn. Ver `SINNOH-PADRAO.md`.
