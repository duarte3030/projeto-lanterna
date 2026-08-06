# Pendências da travessia entre regiões (barco)

Estado em 05/08/2026, commit `acf0eefebd`. Verificado estaticamente **não é**
verificado: este arquivo existe para separar as duas coisas.

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

## 1. As 12 diagonais que nunca foram jogadas em ROM

Os cinco portos formam **20 rotas dirigidas** (5 portos x 4 destinos cada).
Destas, **8 estão provadas na ROM**, com o mapa final lido da EWRAM, e são a
cadeia cronológica nos dois sentidos:

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

**As 12 restantes só passaram pelo `dev_scripts/valida_barco.py`**, que lê a
fonte e afirma que o `case` do porto aponta para o script que dá `warpsilent` no
mapa que o nome do item promete, e que todo `warpsilent` tem `waitstate`. Isso
pega lista fora de ordem e `case` trocado. **Não** pega marinheiro inalcançável,
tile de desembarque ruim nem colisão, que foram exatamente os três bugs achados
nas 8 provadas.

| # | rota | porto de saída | DOWN no menu |
|---|---|---|---|
| 1 | Kanto → Hoenn | Vermilion | 1 (SLATEPORT) |
| 2 | Kanto → Sinnoh | Vermilion | 4 (CANALAVE) |
| 3 | Kanto → Unova | Vermilion | 3 (VIRBANK) |
| 4 | Johto → Sinnoh | Olivine | 4 (CANALAVE) |
| 5 | Johto → Unova | Olivine | 3 (VIRBANK) |
| 6 | Hoenn → Kanto | Slateport | 2 (VERMILION) |
| 7 | Hoenn → Unova | Slateport | 3 (VIRBANK) |
| 8 | Sinnoh → Kanto | Canalave | 2 (VERMILION) |
| 9 | Sinnoh → Johto | Canalave | 0 (OLIVINE, zero DOWN) |
| 10 | Unova → Kanto | Virbank | 2 (VERMILION) |
| 11 | Unova → Johto | Virbank | 0 (OLIVINE, zero DOWN) |
| 12 | Unova → Hoenn | Virbank | 1 (SLATEPORT) |

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

**Prioridade:** baixa em jogo (a progressão cronológica só usa as 8 provadas),
alta em teste de regressão (as 12 são o que quebra calado quando alguém
acrescentar um sexto destino no meio da lista).

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
