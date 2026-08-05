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

## 2. Arco de Mahogany: impossível hoje, faltam os mapas

O esconderijo da Rocket em Mahogany **não existe neste repo**. O hns tem
`RocketHideout_B1F`, `_B2F` e `_B3F`; aqui só existem os `RocketHideout_*_Frlg`,
que são o esconderijo de Celadon (Kanto), outro lugar.

Sem esses três mapas, o que o hns encadeia (Lance invade a loja de Mahogany →
esconderijo → gerador → Ariana → só então a Torre Rádio) não tem onde acontecer.
Esta sessão não podia criar mapa (`data/layouts/layouts.json` e
`data/maps/map_groups.json` estavam com outro agente).

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

## 4. Cenas de cidade (prioridade 4): não portadas

Nenhuma foi feita. O que cada uma ia custar:

| Cena | O que falta |
|---|---|
| Sprout Tower (Violet) | 3 sábios = 3 vagas de treinador; o ancião entrega HM Flash (item + flag de "já peguei") |
| Burned Tower (Ecruteak) | os três cães lendários fogem: `OBJ_EVENT_GFX_RAIKOU/ENTEI/SUICUNE` não existem fora de `#if IS_FRLG`; Eusine = 1 vaga |
| Farol de Olivine (Amphy) | a JASMINE não tem sprite; a cena só fecha com o Secret Potion de Cianwood (item + flag) e mexendo em `OlivineCity_Gym`, que não é meu |

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
