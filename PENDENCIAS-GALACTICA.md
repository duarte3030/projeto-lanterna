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

## 3. Flags que fariam a cena parar de se repetir

Nada disso quebra o jogo, mas deixa cena repetível. Nenhuma foi criada porque
`include/constants/flags.h` estava com outro agente.

| Flag sugerida | O que resolve | Arquivo |
|---|---|---|
| `FLAG_GALACTICA_LAKE_TRIO_FREED` | hoje o botão que solta Uxie/Mesprit/Azelf pode ser apertado quantas vezes o jogador quiser; a mensagem de "já apertou" é decidida pela flag de derrota do Saturn | `data/maps/GalacticHQ_ControlRoom/scripts.inc` |
| `FLAG_CAUGHT_DIALGA` / `FLAG_CAUGHT_PALKIA` | os encontros nas fendas do Spear Pillar são repetíveis: sem flag, `setwildbattle`+`dowildbattle` roda de novo toda vez que se fala com a fenda | `data/maps/SpearPillar_Dialga/scripts.inc`, `data/maps/SpearPillar_Palkia/scripts.inc` |
| `FLAG_GALACTICA_ETERNA` | esconder os três grunts da rua de Eterna depois da Jupiter, como Jubilife já faz com `FLAG_GALACTICA_JUBILIFE` | `data/maps/EternaCity/scripts.inc` |

## 4. Itens-chave que ficaram de fora

Nenhum item novo foi criado (exigiria flag de "já peguei" e entrada em
`include/constants/items.h`).

- **Galactic Key**: no Platinum destranca as portas do 3F e do B2F do QG. Aqui as
  portas estão abertas e os grunts continuam com a fala original sobre a chave.
- **Storage Key** e a **HM Fly** do armazém de Veilstone: o Looker abre a porta
  na fala, sem item, e a HM não é entregue.
  Arquivo: `data/maps/VeilstoneCity_GalacticWarehouse/scripts.inc`.

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
