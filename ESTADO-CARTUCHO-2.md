# Estado do cartucho 2, e como trabalhar nesta branch

Ponto de entrada da branch `cartucho-2`. Leia este arquivo antes de qualquer coisa aqui.
O `ESTADO.md` ao lado continua sendo o diário do **cartucho 1** e do motor, e não é
atualizado por esta frente.

Aberto em 06/09/2026 pelo preparador da Frente A (Galar), sobre a base `fccccc0265`.

---

## 1. O que esta branch é

A branch `cartucho-2` é o fork que guarda **Unova e Galar dentro da árvore**, feito antes de
o cartucho 1 removê-las da `master`. Ela nasce do commit `fccccc0265` (mesmo commit que era
`origin/master` no momento do fork), carimbado pela tag `cartucho-2-base`.

- Repositório e remote: os mesmos da `master` (`origin` =
  `https://github.com/duarte3030/projeto-lanterna.git`).
- Worktree persistente: `/Users/duarte/Projetos/pokemon-claude/cartucho-2`, irmã de
  `pokeemerald-expansion` e de `fontes-mapas`, que é exatamente a posição relativa que os
  scripts de `dev_scripts/` esperam.
- PRD da obra: `Claude Workspace - Pokemon Rom Hacks/Pokemon Claude/PRD-CARTUCHO-2.md`.
- Plano de conteúdo de Galar: `PLANO-CONTEUDO-GALAR.md`, na raiz.

**Nesta fase o cartucho 2 é fábrica de ASSET, não jogo.** Nada de motor, nada de
`SaveBlock`, nada de `SAVE_LAYOUT_REVISION`. Quem quebra save é o cartucho 1, na quebra
única dele.

**O que vai para o `origin`:** asset leve (mapa, tileset, sprite, script, texto, `.mid`).
ROM, romfs e dump de datamine **nunca** vão, e continuam só em `fontes-mapas/`, que não tem
remote (decisão 39 do Gui).

---

## 2. DECISÃO DE DESENHO: como esta branch se sincroniza com a `master`

Registrada aqui em 06/09/2026, na abertura da branch, porque ela muda o custo de toda
rodada e não pode ficar na cabeça de ninguém.

**Enquanto o commit de remoção de Unova e Galar NÃO existir na `master`:**

```
git merge master
```

no começo de cada rodada, trazendo a `master` inteira. Motivo: hoje a `master` e esta
branch são a mesma árvore com o mesmo conteúdo, o cartucho 1 está no meio da rodada 13 com
mais de 200 arquivos ainda sem commit, e escolher commit a commit nesse período custa mais
do que vale. O merge é barato e não perde nada.

**Depois que o commit de remoção existir na `master`:**

```
git cherry-pick <commit>
```

**só** de commits marcados **MOTOR** (assert, letreiro, música, save, ferramenta de QA).
Merge deixa de ser opção a partir daí, porque ele arrastaria a própria remoção de Unova e
Galar para dentro desta branch, que é exatamente o que ela existe para impedir.

**Consequência prática já medida:** a checagem **C28** de `dev_scripts/qa/checa_scripts.py`
(batalha com fala de abertura chamada de gatilho, placa ou script de mapa; tela azul em
`src/battle_setup.c:1258`) **não existe nesta branch**, porque ela mora no working tree
ainda não commitado da rodada 13 da `master`. Esta branch tem C01 a C27. O primeiro
`git merge master` depois do commit da rodada 13 traz a C28 junto, e ela é o portão do
conserto das 12 travas de Galar listadas na seção 3.

---

## 3. Remedição de Galar, 06/09/2026

Tudo abaixo foi medido NESTA sessão, na worktree desta branch, e cada linha traz o comando.

### 3.1 Completude

`[V] python3 dev_scripts/completude.py --detalhe Galar`

| mapas | objetos | warps | placas | script | arte |
|---|---|---|---|---|---|
| 100,0% | 103,6% | 100,0% | **70,3%** | **59,2%** | 48 (32 mapas abaixo de 10) |

Iguais aos números herdados de 23/08/2026. O denominador de `script` é 1.260 NPCs, dos quais
746 já têm script. O de `placas` é 202 bg da fonte.

### 3.2 Fila

`[V] python3 dev_scripts/fila_galar.py`

| tipo | pendente | feita | descartada | das pendentes, bloqueadas |
|---|---|---|---|---|
| map_script | 175 | 19 | 0 | 0 |
| placa | 25 | 109 | 0 | 0 |
| porta_morta | 226 | 0 | 0 | **226** |
| script_objeto | 772 | 1.765 | 104 | **406** |
| **TOTAL** | **1.198** de 3.195 linhas | 1.893 | 104 | 632 |

**O número que importa para planejar rodada é 566: as linhas pendentes SEM bloqueio**
(366 `script_objeto`, 175 `map_script`, 25 `placa`), espalhadas por **265 pastas de mapa**.
As outras 632 estão travadas por motivo de dado, e o maior grupo é
"o NPC não está no mapa: gráfico é pokémon, não vira NPC" (211) seguido de
"destino não está nos 438: é mapa vanilla do FireRed que o demake não redesenhou" (a maior
parte dos 226 `porta_morta`).

### 3.3 Órfãos

`[V] python3 dev_scripts/valida_conectividade.py`

- warps quebrados: **0**
- alcance: 1.966 de 2.289 mapas vivos
- porta única que não devolve: 4, e **as 4 são de Galar**
  (`Galar_Ballonlea04`, `Galar_CrownTundra07`, `Galar_Hulbury01`, `Galar_Motostoke11`)
- mapas que nenhum caminho alcança, em Galar: **246**

Recorte dos 246 por pasta, e ele desmente a conta herdada de "86 de DLC":

| grupo | mapas | é DLC? |
|---|---|---|
| `IsleOfArmor*` | 49 | sim, Isle of Armor |
| `BrawlersCave`, `CourageousCavern`, `WarmUpTunnel` | 3 | sim, Isle of Armor |
| `CrownTundra*` | 21 | sim, Crown Tundra |
| `DynamaxAdventure*` | 4 | sim, Crown Tundra (Max Lair) |
| **subtotal DLC** | **77** | |
| `TurffieldIndoor*` | 58 | não |
| `Postwick*` | 27 | não |
| `WyndonIndoor*` | 22 | não |
| `WildArea*` | 15 | não |
| `LostCave*`, `LiptooChamber`, `ScufibChamber`, `TanobyKey` | 16 | não, e nem são de Galar |
| resto (cidades, rotas, minas, Underwater) | 31 | não |

**Achado:** 16 dos 246 são **sobra de FireRed** (Lost Cave, Tanoby Key e as câmaras Liptoo e
Scufib são as Sevii Islands do jogo base), que o demake deixou dentro dos grupos de Galar.
Eles não são mapa de Galar e não deveriam entrar como obra de warp; a decisão de escopo
sobre eles ainda não foi tomada.

### 3.4 MAPSEC: a conta certa é 140, e a fonte da verdade já existe

`[V] grep -l 'MAPSEC_GALAR_POSTWICK' data/maps/Galar_*/map.json | wc -l` -> **172**
`[V] dev_scripts/qa/nomes_popup_revisao.csv` -> 148 linhas de arquivo, 147 de dados,
**140 de Galar** (não 141), mais 4 de Sinnoh, 2 de Unova e 1 de Johto.

Os dois números são coerentes e o cruzamento fecha exato:

- **32** dos 172 são `Galar_Postwick*` de verdade, e o MAPSEC deles está CERTO. Eles são o
  `balde_sem_nome` de `dev_scripts/galar_mundo.json`, os mapas que nenhum warp limpo ligou a
  uma seção conhecida.
- **140** são pastas que foram RENOMEADAS e ficaram com o `region_map_section` velho. Esses
  140 são exatamente as 140 linhas de Galar do CSV. `[V] script de cruzamento nesta sessão:
  0 no CSV que não esteja no JSON, 32 no JSON que não estejam no CSV`

**Fonte da verdade do MAPSEC certo, e ela é mecânica, não é palpite:**
`dev_scripts/galar_mundo.json`, dois campos:

1. `renomeados` (140 entradas): `Galar_Postwick09` -> `Galar_RoseTower04`. O nome NOVO da
   pasta é o nome verdadeiro do lugar.
2. `secoes` (45 entradas): `{"slug": "RoseTower", "mapsec_real": "MAPSEC_GALAR_NORTH",
   "apelido": "MAPSEC_GALAR_ROSE_TOWER"}`.

A regra é: tirar `Galar_` do nome novo, tirar o número do fim (`RouteNNnn` guarda os dois
primeiros dígitos: `Galar_Route0302` é `Route03`), e, se o resultado não estiver em `secoes`,
tirar o sufixo `Indoor` ou `Cave` (`TurffieldIndoor` -> `Turffield`). **Com essa regra os 140
resolvem, sem sobra.** `[V]`

Destino, por MAPSEC real:

| MAPSEC real | mapas |
|---|---|
| `MAPSEC_GALAR_CENTRAL` | 78 |
| `MAPSEC_GALAR_NORTH` | 33 |
| `MAPSEC_GALAR_SOUTH` | 12 |
| `MAPSEC_GALAR_ISLE_OF_ARMOR` | 12 |
| `MAPSEC_GALAR_CROWN_TUNDRA` | 5 |

O CSV é a lista e `dev_scripts/mundo_galar.py` é quem já sabe escrever
`region_map_section`. O `nome_proposto` do CSV é derivado do mesmo nome de pasta, então ele
serve de conferência cruzada, não de fonte independente.

### 3.5 Fala

`[V] python3 dev_scripts/qa/checa_texto.py`, censo de idioma da região Galar (mapas
`Galar_*` mais arquivos `galar_*`):

| | herdado | hoje |
|---|---|---|
| blocos de texto de Galar | -- | **1.120** |
| em português | 285 | **310** |
| português SEM acento | 58 | **58** |
| em inglês | 28 | **28** |

Os 690 restantes não têm marcador suficiente para classificar (nome, grito, texto de uma
palavra). O número de português SUBIU desde a medição herdada, e é isso que a rodada 9 fez.

**A régua de QA hoje é contra a tradução.** `checa_texto.py` linha 253 reprova T07 quando a
região é `Sinnoh`, `Unova` ou `Galar` e o texto está em inglês. Ou seja: hoje o QA acusa 28
achados T07 em Galar por estarem em inglês, e traduzir os 310 blocos de português faria esse
número ir para 338. **Inverter a régua para Galar é decisão de desenho e precisa acontecer
ANTES de a tradução começar**, senão a frente entrega vermelho por acerto.

### 3.6 Dex

`[V] python3 dev_scripts/censo_dex.py`, bloco "selvagem/estatico/presente por REGIAO":
Kanto 290, Johto 305, Hoenn 297, Sinnoh 267, Unova 315, **Galar 0**, Frontier 8.

`dev_scripts/dex_distribuicao.json` tem 20 entradas com "Galar" no nome, mas todas são
**formas galarianas colocadas em OUTRAS regiões** (Articuno de Galar no AncientTomb de
Hoenn, Zapdos de Galar no Relic Castle de Unova). Nenhuma espécie tem Galar como fonte.

### 3.7 C28: 12 travas em Galar, e o conserto é curto

A checagem não existe nesta branch (seção 2). Medida aqui rodando a versão da `master`
contra ESTA árvore:

`[V] cópia de dev_scripts/qa/checa_scripts.py da master, rodada na worktree`
-> **C28: 18 travas, 12 em Galar e 6 em Unova.**

As 12 de Galar estão TODAS em `data/scripts/galar_treinadores.inc`, todas no mesmo mapa
(`GalarTrn_G12M00_bg2` a `bg13`), todas alcançáveis **de placa**, todas
`trainerbattle_single` em molde que passa por `SetTrainerFacingDirection`. É tela azul
garantida em quem pisar. As 6 de Unova são gatilho de chão em `Unova_AspertiaGym` e
`Unova_LentimasGym`.

---

## 4. Build e portão desta rodada

- Base: `fccccc0265`, tag `cartucho-2-base`, branch `cartucho-2` no `origin`.
- Fork sem blob novo: `git rev-list --objects fccccc0265 --not --remotes=origin` deu **0
  objetos**, porque o commit já era `origin/master`. Nenhum `.gba`, `.sav` ou dump entrou.
- O que o build precisa e o git não traz: **nada além do make**. Os `.mid` (531 arquivos) são
  versionados; `sound/songs/midi/*.s`, `include/constants/map_groups.h`,
  `data/maps/*/header.inc`, `events.inc`, `connections.inc` e
  `src/data/map_popup_names.h` são todos GERADOS pelo próprio `make`, e `tools/` se compila
  sozinha. O único binário que o portão compila à parte é `dev_scripts/gba_runner`, e o
  `antes_de_empurrar.sh` já faz isso quando falta.
- `MODERN` é fixo em 1 neste Makefile (`Makefile:164`), então `make` e `make modern` são a
  mesma coisa aqui, e `tools/agbcc` não é necessário.
- Lock de build: `mkdir /tmp/pokemon-claude-build.lock`. Nesta abertura o lock estava com
  outra sessão (criado 02:38, com `make` do cartucho 1 rodando), e esta rodada ficou na fila
  em vez de tomá-lo à força.

### Build de base da branch, 06/09/2026

`[V] export DEVKITARM=...; make -j8 > log 2>&1; echo $?`

| medida | valor |
|---|---|
| exit code do `make` | **0** |
| `pokeemerald.gba` no disco | 33.554.432 B (32 MiB, já com o padding) |
| md5 | `99b141df69aaa917bd7611e3c1f69298` |
| ROM ocupada (linha do próprio build) | **32.360.228 B, 96,44% de 32 MB** |
| EWRAM | 225.856 B, 86,16% |
| IWRAM | 28.404 B, 86,68% |
| tempo | 3 min 27 s (02:54:09 a 02:57:36) |

`[V] python3 dev_scripts/guarda_save.py` -> **SAVE COMPATIVEL**, SaveBlock1 em 14.964 B de
15.872 (94,3%), 2.400 mapas, 2.252 ids de treinador conferidos.

A ROM ocupada bate byte a byte com a da rodada 13 na `master` (32.360.228 B), o que é o
esperado: a branch nasce do mesmo commit e esta rodada não tocou em nada que entre na ROM.

### T11: 3 de 3

```
python3 dev_scripts/testa_critico.py T11 \
    --rom  /private/tmp/claude-501/c2-t11-antiga/pokeemerald.gba \
    --src  /private/tmp/claude-501/c2-t11-antiga \
    --rom2 pokeemerald.gba --src2 .
```

`[V] 3/3 passaram`, em 06/09/2026. T11.1 grava a save na ROM velha, T11.2 é o controle que
prova que o `.sav` é lido, e T11.3 confirma que a save de layout velho é **recusada** pela
ROM nova, com o jogo caindo em NEW GAME e a flag testemunha `0x2BA` apagada.

**A ROM velha do T11 teve que ser reconstruída nesta rodada**, e isso é ferramenta, não
conteúdo. A worktree que o `ESTADO.md` do cartucho 1 cita
(`/private/tmp/claude-501/t11-antiga`) sumiu do disco, e `/private/tmp/claude-501/t11-r13`
existe sem `.gba`. A nova mora em **`/private/tmp/claude-501/c2-t11-antiga`**, detached em
`cf6786b2ae`, ROM md5 `ac8ed5419ab69cacece45ad6479e6063`. Ela é `/private/tmp`: some no
reboot, e quem precisar do T11 depois disso builda de novo (3 min sob o lock).

---

## 5. Passagem de bastão

### O que esta rodada fez

1. Criou o fork: tag `cartucho-2-base` e branch `cartucho-2`, as duas no `origin`, sem blob
   novo.
2. Criou a worktree persistente `/Users/duarte/Projetos/pokemon-claude/cartucho-2`.
3. Remediu Galar inteira (seção 3), e três números herdados mudaram: o CSV de MAPSEC tem
   **140** linhas de Galar e não 141; os órfãos de DLC são **77** e não 86; a fala em
   português subiu de 285 para **310**.
4. Achou a fonte da verdade do MAPSEC (`galar_mundo.json`, campos `renomeados` e `secoes`),
   que torna o lote A mecânico.
5. Escreveu o crédito a terceiros no `README.md` (decisão 38).
6. Registrou a política de sincronia com a `master` como decisão de desenho (seção 2).

### O que fica aberto, e é onde a próxima rodada começa

- **A régua de T07 precisa inverter para Galar antes da tradução.** É decisão de desenho e
  está na seção 3.5. Sem ela, a Frente A entrega vermelho por acertar.
- **C28 não existe nesta branch.** Primeiro `git merge master` depois do commit da rodada 13.
- **As 12 travas de C28 em Galar** estão em um arquivo só e são o conserto mais barato que a
  frente tem.
- **Os 16 mapas de sobra de FireRed** dentro dos grupos de Galar (Lost Cave, Tanoby Key,
  câmaras Liptoo e Scufib) precisam de decisão de escopo: ligar, carimbar `cortado_por` ou
  deixar como estão.
- **A tela de créditos dentro do jogo** é pendência da fase de montagem.
- **A ROM velha do T11 vive em `/private/tmp`** (`/private/tmp/claude-501/c2-t11-antiga`), e
  portanto some no reboot. Quem for rodar o T11 completo confere se ela existe antes, e
  builda de novo se não existir. Foi o que custou o tempo desta rodada.

### Proposta de ONDA 1, quatro executores Opus, dono exclusivo por arquivo

A colisão é real e é uma só: **lotes A, B e D todos encostam nos mesmos `map.json` e
`scripts.inc` de Galar.** A divisão abaixo evita dono duplo separando por TIPO DE ARQUIVO,
não por mapa.

| lote | dono exclusivo | alvo medido |
|---|---|---|
| **A. MAPSEC** | `data/maps/Galar_*/map.json` (só o campo `region_map_section`) e `dev_scripts/mundo_galar.py` | os **140** do CSV, pela regra de `galar_mundo.json`. Meta: CSV de divergência em 0 e os 32 `Postwick` de verdade intocados |
| **B. Warps dos órfãos** | `data/maps/Galar_*/map.json` (só `warp_events` e `connections`) | os **246**, todos, por decisão 31. Sub-lotes naturais: B1 campanha (153, sem DLC e sem as sobras de FireRed), B2 Isle of Armor (52), B3 Crown Tundra (25), B4 as 16 sobras de FireRed, que são decisão antes de obra |
| **C. Fila** | `data/maps/Galar_*/scripts.inc` e `data/scripts/galar_*.inc` | as **200** linhas de tipo `placa` (25) e `map_script` (175), que são as únicas sem bloqueio fora de `script_objeto`. Primeiro a `placa`, porque é a coluna que está em 70,3% e são só 25 |
| **D. Tradução** | `dev_scripts/qa/checa_texto.py` (a régua) e o glossário novo | **310** blocos em português, dos quais 58 estão sem acento. Antes de tocar em fala: inverter T07 para Galar e escrever `GLOSSARIO-GALAR.md` com o termo do motor (item, golpe, classe de treinador, nome de cidade) para os executores não gerarem duas grafias |

**Por que o lote A e o lote B podem dividir o mesmo `map.json`:** eles não podem, e por isso
**A roda primeiro e sozinho**, num único passe de script idempotente, e só então B abre. A é
mecânico e cabe em minutos; B é a obra longa. Rodar A antes custa quase nada e elimina a
colisão inteira.

**Por que o lote D não começa na onda 1:** ele começa pelo que NÃO é fala (a régua e o
glossário), que são arquivos que ninguém mais toca. A tradução de fato entra na onda 2, com
`scripts.inc` já liberado pelo lote C.

**O lote C e o lote D dividem `scripts.inc`.** Na onda 1 só C escreve lá. Na onda 2, quando D
entrar, C precisa ter fechado ou os dois precisam partir a lista de mapas entre si, sem
sobreposição.
