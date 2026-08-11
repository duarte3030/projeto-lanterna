# Pendências da travessia entre regiões (barco)

Estado em 11/08/2026. Verificado estaticamente **não é** verificado: este arquivo
existe para separar as duas coisas.

**As 20 rotas dirigidas estão provadas na ROM**, cada uma com o par
`(mapGroup, mapNum)` lido da EWRAM depois da travessia. As 12 que faltavam
fecharam em 11/08/2026, em `dev_scripts/testes_criticos/86_travessias_diagonais.json`
(casos `T86.1` a `T86.12`), sem gastar flag, var, id de treinador, mapa, warp nem
objeto: são só casos de teste. Detalhe na seção 1.

---

## 0. Olivine ↔ Vermilion passa por dentro do S.S. Aqua (05/08/2026)

Das 20 rotas dirigidas, **duas deixaram de ser teleporte**: o marinheiro de
Olivine e o de Vermilion agora embarcam o jogador em `MAP_SSAQUA_1F`, e quem
desembarca do outro lado é o marinheiro da porta, dentro do navio. Os pontos de
desembarque continuam os mesmos de antes (`MAP_VERMILION_CITY` 15,10 e
`MAP_OLIVINE_CITY_PORT_INSIDE` 8,17), de propósito: os roteiros já provados não
precisaram ser re-derivados, só ganharam o trecho de bordo no fim.

Quem manda o sentido é `FLAG_SSAQUA_RUMO_KANTO`, posta no embarque. A porta do
cais em (29,1) é `MAP_DYNAMIC` e o `setdynamicwarp` do porto a aponta de volta
para o próprio porto; hoje ela é inalcançável a pé, porque o marinheiro da porta
fica em (29,2) e tranca o único acesso, então ela é seguro, não caminho.

Provado na ROM: **T4.2** (Kanto → navio → Johto), **T10.3** (Johto → navio →
Kanto, com a descida ao convés) e **T10.4** (11 tiles de convés e entrada na
cabine do jogador). `dev_scripts/valida_barco.py` ganhou a regra dos dois saltos
e reprova se o `setflag`/`clearflag` do sentido ou o `setdynamicwarp` sumirem.

As outras 18 rotas continuam teleporte direto, e está certo: o S.S. Aqua liga
Johto a Kanto, não os outros portos.

---

## 1. As 20 rotas dirigidas, e o que cada prova vale

Os cinco portos formam **20 rotas dirigidas** (5 portos x 4 destinos cada), e
todas as 20 estão provadas na ROM. A cadeia cronológica nos dois sentidos são as
8 primeiras, provadas em 05/08/2026:

| rota | caso |
|---|---|
| Kanto → Johto | T4.2 (cadeia inteira: campeão, passe, embarque) |
| Johto → Kanto | T10.3 |
| Johto → Hoenn | T6.2 |
| Hoenn → Johto | T8.2 |
| Hoenn → Sinnoh | T8.3 |
| Sinnoh → Hoenn | T8.5 |
| Sinnoh → Unova | T10.1 |
| Unova → Sinnoh | T10.2 (ida e volta) |

### As 12 diagonais, provadas em 11/08/2026

Até 11/08/2026 elas só tinham passado pelo `dev_scripts/valida_barco.py`, que lê
a fonte e afirma que o `case` do porto aponta para o script que dá `warpsilent`
no mapa que o nome do item promete, e que todo `warpsilent` tem `waitstate`.
Isso pega lista fora de ordem e `case` trocado, e **não** pega marinheiro
inalcançável, tile de desembarque ruim nem colisão, que foram exatamente os três
bugs achados nas 8 anteriores.

Agora cada uma tem o par `(mapGroup, mapNum)` lido da EWRAM no fim da travessia,
e a posição de chegada bate com a coordenada do `warpsilent` da fonte:

| caso | rota | DOWN no menu | EWRAM `location` no fim | pos |
|---|---|---|---|---|
| T86.1 | Kanto → Hoenn | 1 (SLATEPORT) | (9,9) = `MAP_SLATEPORT_CITY_HARBOR`, layout 88 | (8,14) |
| T86.2 | Kanto → Sinnoh | 4 (CANALAVE) | (75,11) = `MAP_CANALAVE_CITY`, layout 787 | (17,49) |
| T86.3 | Kanto → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.4 | Johto → Sinnoh | 4 (CANALAVE) | (75,11) = `MAP_CANALAVE_CITY`, layout 787 | (17,49) |
| T86.5 | Johto → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.6 | Hoenn → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.7 | Hoenn → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.8 | Sinnoh → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.9 | Sinnoh → Johto | 0 (OLIVINE, zero DOWN) | (91,8) = `MAP_OLIVINE_CITY_PORT_INSIDE`, layout 1031 | (8,17) |
| T86.10 | Unova → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.11 | Unova → Johto | 0 (OLIVINE, zero DOWN) | (91,8) = `MAP_OLIVINE_CITY_PORT_INSIDE`, layout 1031 | (8,17) |
| T86.12 | Unova → Hoenn | 1 (SLATEPORT) | (9,9) = `MAP_SLATEPORT_CITY_HARBOR`, layout 88 | (8,14) |

ROM usada: a build de 06/08/2026 01:15 que estava na árvore, com `include/`
congelado ao lado dela para o `--src`, porque três outros agentes escrevem no
repo ao mesmo tempo e `map_groups.h` deslocado descreveria outro jogo.

**Re-rodar os 20 casos na primeira build depois desta.** Não é ritual: enquanto
estes casos eram escritos, a frente de Sinnoh estava dando script de fala a dez
NPCs de `data/maps/CanalaveCity/map.json`, e cinco dos casos novos (`T86.8` a
`T86.12`) atravessam Canalave a pé, como já faziam `T8.5`, `T10.1` e `T10.2`.
Posição nenhuma mudou nesse diff, então a expectativa é verde; expectativa não é
medida.

**As 12 passaram na primeira tentativa, e é por isso que quatro mutantes foram
rodados**: resultado limpo demais é verificação quebrada até que se explique por
que é real (ESTADO.md, portão 4). Cada mutante caiu exatamente onde a mutação
prevê, e nenhum caiu em "passou assim mesmo":

- `T86.2` com **3 DOWN** em vez de 4 desembarca em `MAP_UNOVA_VIRBANK_PORT`
  (112,7), não em Canalave: o índice do menu é lido de verdade.
- `T86.9` com **1 DOWN** onde o certo é zero desembarca em
  `MAP_SLATEPORT_CITY_HARBOR` (9,9), não em Olivine.
- `T86.10` com **1 DOWN na segunda perna** desembarca em Slateport (9,9), e não
  em Vermilion.

Esse mutante sozinho **não** prova que o menu da segunda perna é o de Virbank e
não o de Canalave: 1 DOWN dá SLATEPORT nas duas listas, e 0 e 2 também coincidem.
Quem prova é a sequência de `location` lida ao longo da corrida inteira, e não só
o estado final. Medida, para os três casos que saem de Virbank:

```
T86.10  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (37,5)  VERMILION_CITY
T86.11  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (91,8)  OLIVINE_CITY_PORT_INSIDE
T86.12  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (9,9)   SLATEPORT_CITY_HARBOR
```

O jogador **passou** pelo Porto de Virbank e saiu dele para três destinos
diferentes: é o marinheiro de Virbank que está sendo lido, e a lista dele tem os
quatro destinos certos.
- `T86.5` **sem o `20:DOWN*12`** que leva até o marinheiro fica em
  `MAP_OLIVINE_CITY_PORT_INSIDE` (91,8): os `A` do roteiro não abrem menu
  nenhum sozinhos, então "chegou no marinheiro" não é suposição.
- `T86.1` **sem `FLAG_SYS_GAME_CLEAR`** fica em `MAP_VERMILION_CITY` (37,5): o
  portão do PASSE TRI vale para as três diagonais de Vermilion, não só para a
  rota de Johto. (Os casos `T4.5` e `T4.6` já guardavam esse controle; o mutante
  só confirmou que ele cobre também as diagonais.)

### Receita para escrever esses casos

A lista `MULTI_CINCO_REGIOES_BARCO` é sempre a mesma:
`0 OLIVINE, 1 SLATEPORT, 2 VERMILION, 3 VIRBANK, 4 CANALAVE, 5 Sair`.
O cursor começa em 0 e o menu **não dá a volta**, então o número de `DOWN` é o
próprio índice do destino. Cada porto pula o próprio índice, e é por isso que
sair de Vermilion rumo a Canalave custa 4 DOWN mesmo Vermilion não tendo `case 2`.

Como chegar em cada marinheiro (medido, não chutado):

| porto | warp de debug | roteiro até o marinheiro |
|---|---|---|
| Vermilion | `MAP_VERMILION_CITY` warp 4 | `16:DOWN*4` (o marinheiro em (15,11) trava o passo) |
| Olivine | `MAP_OLIVINE_CITY_PORT_INSIDE` warp 0 | `16:DOWN*12` |
| Slateport | `MAP_SLATEPORT_CITY_HARBOR` warp 0 | `20:UP*2,20:LEFT*10` |
| Canalave | `MAP_CANALAVE_CITY` warp 1 | `20:DOWN*20,20:LEFT*20,20:RIGHT*4,20:UP*12` |
| Virbank | **não aceita warp de debug** | chegar de barco de Canalave, depois `16:RIGHT*5,16:UP` |

O Porto de Virbank não aceita warp de debug porque os três warps dele caem em
cima de outro warp ou fora do mapa 10x8: o warp 0 larga o jogador em (4,8),
abaixo do mapa, e o passo seguinte re-dispara o warp para Virbank City. Por isso
o T10.2 é ida e volta.

Depois de encostar no marinheiro, o diálogo é sempre:
`A` (fala) → `A` (fecha a caixa, o menu abre) → `DOWN` x N → `A` (escolhe) →
`A` (fecha o "Zarpando...") → o warp acontece. Em Vermilion entra antes a
conversa do assistente do Prof. Carvalho, que precisa de 4 `A` e depois `B` para
limpar o que sobrou sem re-disparar o NPC.

**Prioridade:** baixa em jogo (a progressão cronológica só usa as 8 da cadeia),
alta em teste de regressão: as 12 são o que quebra calado quando alguém
acrescentar um sexto destino no meio da lista, e agora existe caso de emulador
para cada uma.

### O que continua aberto

1. **O Porto de Virbank continua sem aceitar warp de debug**, e por isso três
   casos (`T86.10` a `T86.12`, além do `T10.2`) gastam uma travessia inteira de
   Canalave só para chegar lá. Os três warps do mapa 10x8 caem em cima de outro
   warp ou fora do mapa. Consertar é mexer em mapa de Unova, dono de outra
   frente; enquanto não for, o custo é ~4 s por caso, e nenhum resultado muda.
2. **Todo o texto de jogo do barco está em português**, nos cinco portos:
   `VermilionCity_Text_WhereTo` ("Bem-vindo ao Porto de Vermilion City em
   Kanto!"), `VermilionCity_Text_FerrySemPasse`, os quatro
   `..._Text_SettingSailTo*` / `..._Text_Zarpar*` de cada porto e os
   `Text_ParaOnde` / `Text_Volte` de Canalave e de Virbank. A regra do projeto é
   texto de jogo em **inglês**; documentação e comentário é que são em
   português. **Não foi consertado nesta leva de propósito**, por dois motivos:
   dois dos cinco arquivos são mapa de Sinnoh (`CanalaveCity`) e de Unova
   (`Unova_VirbankPort`), de outras frentes; e o número de páginas de cada caixa
   (`\p`) está embutido na contagem de `A` de 20 roteiros de teste já provados,
   então reescrever texto sem re-rodar os 20 casos quebra a suíte calada.
   Quem for traduzir: mantenha uma página por caixa e re-rode `T4`, `T6`, `T8`,
   `T10` e `T86` na build seguinte.
3. **As três `FLAG_REGIAO_*_LIBERADA` estão reservadas e NÃO estão ligadas em
   lugar nenhum.** Medido em 11/08/2026: `FLAG_REGIAO_JOHTO_LIBERADA` (0x22),
   `FLAG_REGIAO_HOENN_LIBERADA` (0x23) e `FLAG_REGIAO_SINNOH_LIBERADA` (0x24)
   aparecem **só** em `include/constants/flags.h:2546-2548`, e nenhum script de
   `data/`, nenhum `.c` de `src/` as lê ou acende. O comentário ao lado delas
   descreve o desenho pretendido ("o marinheiro do cais monta o menu de destinos
   lendo estas três"), e ele ainda não existe no jogo: **hoje os cinco portos
   oferecem os quatro destinos desde sempre**, e o único portão da travessia
   inteira é o PASSE TRI de Vermilion. Não é bug de alcance em jogo (só se chega
   aos outros portos de barco), mas é a diferença entre o desenho escrito e o
   jogo rodando, e é decisão do Gui ligar ou não. As flags continuam intactas.

A travessia continua não gastando var nenhuma, e os 12 casos novos são só JSON
de teste: sem flag, var, id de treinador, mapa, warp ou objeto novo. A faixa
0x881 a 0x887, reservada para esta frente, **voltou inteira**.

---

## 2. O canal de Canalave é caminhável, e o cais é uma ilha

Achado em 05/08/2026 ao provar Hoenn → Sinnoh. **Não consertei de propósito: é
`data/layouts/CanalaveCity/map.bin`, arquivo do import de Sinnoh, não meu.**

O barco desembarca em (17,49) e o marinheiro Eldritch fica em (17,48). Os dois
estão **dentro do canal**: os tiles x=16..20 são desenhados como água e têm
`colisão 0`, com a mesma `elevação 1` do chão que o jogador anda no resto da
cidade. Resultado na tela: o jogador e o NPC ficam em pé sobre a água.

```
     x=12    13      14      15      16      17      18      19      20     21
y=46 c0e3   c0e3    c0e3    c0e3  | c0e1    c0e1    c0e1    c0e1 |  c1e0   c0e3
y=47 c0e3   c0e3    c0e3    c0e3  | c0e1    c0e1    c0e1    c0e1 |  c1e0   c0e3
y=48 c0e3   c1e0    c0e1    c0e1  | c0e1   [NPC]   c0e1    c0e1  |  c1e0   c0e3
y=49 c0e3   c1e0    c0e1    c0e1  | c0e1  [barco]  c0e1    c0e1  |  c1e0   c0e3
                                    ^--------- o canal ---------^
```

O cais de verdade é o retângulo de **elevação 3** em (13..15, 46..47), ligado à
margem oeste. Mas ele é **isolado por elevação** do chão `e1` onde o jogador
anda: mover o marinheiro para o cais tornaria o porto inalcançável, porque não
existe tile de transição (elevação 0 ou 15) entre `e1` e `e3` ali. Por isso o
marinheiro fica onde está.

**Conserto, no dono do layout:** dar `colisão 1` aos tiles do canal
(x=16..20 em toda a faixa y=40..55) e abrir uma transição de elevação no cais,
depois mover o marinheiro para (15,47) e o desembarque para (14,47). Os
roteiros de T8.3, T8.5, T10.1 e T10.2 precisam ser re-derivados junto, porque
todos hoje atravessam o canal a pé.
