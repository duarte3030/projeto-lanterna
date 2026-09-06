# Estado do cartucho 2, e como trabalhar nesta branch

Ponto de entrada da branch `cartucho-2`. Leia este arquivo antes de qualquer coisa aqui.
O `ESTADO.md` ao lado continua sendo o diário do **cartucho 1** e do motor, e não é
atualizado por esta frente.

Aberto em 06/09/2026 pelo preparador da Frente A (Galar), sobre a base `fccccc0265`.

---

## 0. O PRIMEIRO COMANDO DE TODA RODADA

```
git ls-remote --heads origin cartucho-2
```

Antes de ler qualquer outra coisa aqui, rode essa linha. Ela diz onde o `origin` está de
verdade, e é a única coisa que separa "continuar a onda anterior" de "reescrever por cima
dela". Esta branch tem worktree persistente e mais de uma sessão escrevendo perto, então
`HEAD` local não é prova de nada até o `ls-remote` bater com ele.

## Onda 2 (07/09/2026), FECHAMENTO: GALAR ESVAZIA A FILA INTEIRA, GANHA 168 NPCs COM FALA, FECHA A GERAÇÃO 8 DENTRO DE SI E PERDE 9 ÓRFÃOS (condutora Opus, quatro executores, fechador Opus)

Fechamento da onda 2 da Frente A. Quatro lotes (F, G, H, I) deixaram o trabalho no
disco e os pedidos escritos; este fechador colou os pedidos, rodou os geradores na
ordem, provou e commitou lote a lote. Tudo abaixo foi medido NESTA worktree, com o
comando ao lado, e `[V]` marca o que foi conferido nesta rodada.

### Placar por lote, antes e depois

**Lote G, portas mortas** (`dev_scripts/portas_mortas_galar.py`, `galar_portas_fechadas.inc`)

| medida | antes | depois |
|---|---|---|
| fila `porta_morta` pendente | 226 | **0** `[V]` |
| placas de porta fechada no `map.json` | 0 | **45**, em 23 mapas `[V]` |
| travas P1 da `lente_portas` em Galar | 268 | **276** (+8) `[V]` |

`[V] python3 dev_scripts/fila_galar.py`, `[V] grep -c 'porta fechada (portas_mortas_galar.py)' data/maps/*/map.json`,
`[V] python3 dev_scripts/qa/lente_portas.py`

**Lote F, portas de script** (`galar_portas_script.inc`, `valida_conectividade.py`)

| medida | antes | depois |
|---|---|---|
| órfãos de Galar | 141 | **132** `[V]` |
| alcance geral | 2.052 de 2.289 | **2.061 de 2.289** `[V]` |
| warps quebrados | 0 | **0** `[V]` |
| becos sem saída | 11 | **14** `[V]` |

`[V] python3 dev_scripts/valida_conectividade.py`

**Lote I, NPCs e placas** (`galar_objetos_i.inc`, `galar_placas_c.inc`)

| medida | antes | depois |
|---|---|---|
| completude de Galar, `script` | 59,2% | **72,9%** `[V]` |
| completude de Galar, `placas` | 72,3% | **104,5%** `[V]` |
| completude de Galar, `objetos` | 103,6% | **104,5%** `[V]` |
| NPC com fala | 746 de 1.260 | **933 de 1.279** `[V]` |
| fila `script_objeto` pendente | 0 | **0** (226 adiadas) `[V]` |
| blocos de Galar em português (`checa_texto` T07) | 1 | **1** `[V]` |

`[V] python3 dev_scripts/completude.py --detalhe Galar`, `[V] python3 dev_scripts/qa/checa_texto.py`

**Lote H, Dex, encontros e estáticos** (`distribui_dex.py`, `estaticos_galar.py`)

| medida | antes | depois |
|---|---|---|
| censo da Dex, Galar | 592 | **631** `[V]` |
| gen 8 com fonte DIRETA em Galar | 58 | **84** `[V]` |
| colocações de Galar | 0 | **27** (12 mato, 10 estático, 5 presente) `[V]` |
| encontros do `wild_encounters.json` | 96 mapas | **107 mapas**, 164 tabelas, 1.638 slots `[V]` |
| antros de raide que trocaram de espécie | 0 | **51** `[V]` |

`[V] python3 dev_scripts/censo_dex.py`, `[V] python3 dev_scripts/importa_encontros_galar.py --aplicar`,
`[V] python3 dev_scripts/distribui_dex.py --galar --aplica`, `[V] python3 dev_scripts/estaticos_galar.py --aplicar`

**O que NÃO andou, e é bom que esteja escrito:** a `lente_warps` de Galar caiu de 130
para **128** (P2 48, P4 80, P1 e P3 zero) `[V]`, e a de Unova ficou em 38. `checa_scripts`
continua em **13 travas, nenhuma em Galar**, e a **C28 continua em 0 achados em todas as
regiões** `[V]`. O `checa_texto` fecha em **2.124 achados**, o mesmo número da abertura, com
o único bloco em português de Galar sendo o defeito de charmap deixado à vista de propósito.

### As decisões da condutora, e como cada uma foi executada

1. **Os 7 táxis do lote F usam `OBJ_EVENT_GFX_SPECIES(CORVIKNIGHT)`** (opção a). Os sete
   objetos de gfx 232 da fonte abrem porta para balcão de táxi, e as placas daquele balcão
   já nomeiam o Corviknight. Aplicados com `origem: "porta de script
   (portas_script_galar.py)"`.
2. **A régua de conectividade passa a ler `data/scripts/galar_*.inc`.** Foi a mudança que
   mais valeu da onda: os 438 `scripts.inc` de Galar não têm uma linha de `warp`, e a
   varredura media a região inteira com o bytecode do demake fora do grafo. A atribuição é
   pelo cabeçalho `@ ---- Galar_X ----` de cada bloco.
3. **Os três iniciais de Galar saem do mato e viram presente.** Ver a seção própria abaixo.
4. **As 10 linhas de `script_objeto` com item fora da tabela do FireRed** continuam
   `descartada`, decisão 6 da onda 1, e sobreviveram à regeneração `[V]`.
5. **Os 2 textos do lote I sem tradução** (`dev_scripts/onda2_lote_i_pulados.txt`, índices
   056 e 070) ficam aguardando o Gui. Os outros 107 entraram, com 0 estouro de caixa, 0 de
   charmap e 0 de token `[V] dev_scripts/onda2_lote_i_blocos/validacao.txt`.

### As decisões que ESTE fechador teve que tomar, com a medição de cada uma

**(a) O objeto 7 de `Galar_Motostoke06` foi pedido pelos DOIS lotes.** O lote F queria
`GalarPorta_G06M12_o7` (a transcrição da fonte, que tem a fala E o `warp` para
`MAP_GALAR_WEDGEHURST_09`); o lote I queria `GalarFalaI_G06M12_o7`, que é só a fala. **F
venceu, por conter I.** O rótulo do lote I fica sem dono dentro do `.inc`: ele ocupa ROM e
nunca dispara. Se a próxima rodada quiser recuperar o espaço, é o primeiro lugar para
olhar.

**(b) O pedido 4 do lote G é FALSO POSITIVO, e a medição está aqui para ninguém refazer.**
O achado era `warp MAP_GALAR_WILD_AREA_09, 37` num `.inc` para um mapa que tem 1 warp só. A
linha de verdade é `warp MAP_GALAR_WILD_AREA_09, 37, 28`, e o macro `formatwarp`
(`asm/macros/event.inc:448`) trata DOIS argumentos como **par de coordenadas**, com
`WARP_ID_NONE`: não é índice de warp nenhum. O tile (37,28) foi medido no `map.bin`: dentro
dos 59 por 51 do layout, colisão 0, elevação 1 `[V]`. Nada a consertar.

**(c) O pedido 2 do lote G foi RESOLVIDO, e sem o `special`.** O warp 1 de
`Galar_IsleOfArmor30` (4,7) é a porta por onde DOIS mapas entram. Ele virou `MAP_DYNAMIC`,
e o motor grava a origem sozinho: `SetupWarp` (`src/field_control_avatar.c:1130`) chama
`SetDynamicWarp` com o mapa e o warp de onde o jogador veio sempre que o warp de DESTINO é
dinâmico. **O `DefinirRetornoPredioCompartilhado` NÃO entrou, e isso foi medido, não
preferido:** a guarda dele repõe o retorno pelo `escapeWarp` sempre que a origem não é mapa
AO AR LIVRE (`IsMapTypeOutdoors`, `src/overworld.c:1546`), e as duas origens desta porta
são `Galar_IsleOfArmor28` (`MAP_TYPE_NONE`) e `Galar_IsleOfArmor33` (`MAP_TYPE_INDOOR`).
Com o special, a porta mandaria o jogador para o último ponto de fuga em vez de devolvê-lo
para a rua. O gerador aprendeu a regra (`portas_mortas_galar.py`, veredito `religada` para
warp `MAP_DYNAMIC`), e a linha saiu de `adiada` para `feita` pela fila, não à mão `[V]`.

**(d) O pedido 3 do lote G fica REGISTRADO como está.** As 131 medidas da `lente_warps` em
Galar são prédio compartilhado, não índice errado, e ZERO delas se conserta trocando o
índice de chegada. Depois desta onda a lente mede 128, e o conserto continua sendo retorno
dinâmico caso a caso.

**(e) O pedido 5 do lote G foi CONFERIDO no fim, e as 45 placas estão inteiras** `[V]`.
Nenhum gerador rodado nesta rodada regravou `bg_events` de Galar. **Armadilha medida de
passagem:** rodar `portas_mortas_galar.py` uma segunda vez sobre a árvore já escrita relata
**40** lápides e não 45, porque 5 delas já viraram `apagada` (mapa que ficou com zero
warps). A placa continua no `map.json`; o que envelheceu é o relatório, não a obra. Quem
comparar os dois números sem esta linha vai caçar 5 placas que nunca sumiram.

### Os três iniciais de Galar: Wedgehurst NÃO tem laboratório

A decisão da condutora dizia "no laboratório de Wedgehurst, e se não houver laboratório
reconhecível, use o Centro Pokémon e registre". **Não há laboratório, e isso foi medido:**
nenhum dos 17 mapas `Galar_Wedgehurst*` tem NPC de cientista, e as únicas citações da Sonia
em Galar inteiro estão em NPC de rua (`Galar_Route0202`) e da praça (`Galar_Wedgehurst05`)
`[V]`. O prédio escolhido é o **Centro Pokémon, `Galar_Wedgehurst03`**, reconhecido por três
marcas do próprio mapa: `MUS_RG_POKE_CENTER`, a `OBJ_EVENT_GFX_NURSE_FRLG` do balcão e
`MAP_TYPE_INDOOR`.

O molde é o do laboratório do Birch, linha por linha: **um** NPC com `dynmultichoice` dos
três, `givemon` de nível 5, flag própria `FLAG_INICIAL_GALAR` e a mesma armadilha já paga lá
(nada de `waitstate` depois do `dynmultistack`). O tile é (3,5), e a busca em largura contra
o `map.bin` prova que pôr objeto ali não ilha tile nenhum: 80 alcançáveis viram 77, que é
exatamente 80 menos os três tiles `[V]`.

**Por que a decisão valia a rodada.** Antes dela o `distribui_dex --galar` classificava os
três como `selvagem` (eles não são lenda) e o rodízio de bioma os espalhava por slot
duplicado: o **Grookey caía em `MAP_GALAR_UNDERWATER_02`**, o Scorbunny em
`MAP_GALAR_MOTOSTOKE_18` e o Sobble num slot de pesca. Inicial não nasce no mato em jogo
nenhum da série. A troca de balde está no CÓDIGO (`INICIAIS_GALAR` em `distribui_dex.py`) e
não na tabela, porque `escreve_tabela_galar` refaz os quatro baldes do censo a cada chamada
e uma linha escrita à mão seria apagada na rodada seguinte, calada.

Os **10 estáticos e os 2 event-only** entraram pelo mesmo mecanismo, num escritor novo
(`distribui_dex.py --galar-objetos`), com a marca `distribui_dex galar` e não a das cinco
regiões: `limpa_mapas_orfaos` varre todo `map.json` e apaga objeto com a marca das cinco que
não esteja na tabela DELAS, e Galar não está. Mesma marca, e a próxima chamada de
`--estaticos --aplica` apagaria Galar inteiro em silêncio.

### A ordem de rodagem, e por que ela não é enfeite

Os quatro passos do lote H foram rodados na ordem que o pedido manda, e o terceiro tem uma
consequência que precisa ficar escrita:

1. `importa_encontros_galar.py --aplicar` (107 mapas, 1.638 slots) `[V]`
2. `distribui_dex.py --galar --aplica` (12 linhas de mato) `[V]`
3. `estaticos_galar.py --aplicar` `[V]`
4. `distribui_dex.py --galar-objetos --aplica` (os objetos e as cenas) `[V]`

O passo 3 **tira todos os objetos dele de todos os 438 `map.json` e os repõe no FIM da
lista.** O diff medido é `+204/-204` no `galar_estaticos.inc` e **135 linhas em 24 mapas**, e
não as "51 linhas em 21 mapas" que a simulação do lote H previu. A diferença inteira é essa
reposição: em 5 mapas (`Galar_IsleOfArmor05`, `08`, `09`, `12` e `Galar_WildArea22`) os
objetos do lote F, que tinham sido acrescentados no fim, passaram para ANTES do bloco de
estáticos. **Nenhum objeto de outro lote foi perdido: a lista dos que não são de
`estaticos_galar` é byte a byte a mesma nos 24 mapas** `[V]`, e o que mudou foi só o índice
deles. Isso não quebra script nenhum porque os únicos `local_id` numéricos de Galar estão em
`GalarPorta_G06M12_o7`, e `Galar_Motostoke06` não é um dos 24 `[V]`. O passo 4 vem DEPOIS por
isso: rodado antes, os objetos da Dex ficariam no meio e andariam de índice a cada passada.

### As premissas que esta rodada DERRUBOU

1. **"A régua de conectividade já lia os scripts de Galar."** Não lia nada. A varredura de
   `warp` de script olhava `data/maps/<mapa>/scripts.inc`, e os 438 daquela região só têm o
   `MapScripts`. Nove órfãos saíram da lista sem uma linha de obra, e a repartição foi
   MEDIDA rodando a régua com a varredura desligada e com o `galar_portas_script.inc` fora:
   **5 caíram por medir certo o que já estava escrito** (141 para 136) e **4 pelas portas
   novas do lote F** (136 para 132) `[V]`.
2. **"As 226 `porta_morta` são 226 portas que o jogador abre."** Das 226, **43 disparam** e
   183 não `[V]`. A obra de fechar é sobre as 43; as outras já eram tile sem gatilho.
3. **"Os 514 NPCs mudos são uma fila."** São uma REPARTIÇÃO: o denominador da coluna
   `script` cresce junto quando NPC novo entra. Nesta rodada o numerador foi de 746 para 933
   e o denominador de 1.260 para 1.279, e é por isso que 168 NPCs valeram 13,7 pontos e não
   os 13,3 que a régua da abertura previa.
4. **"O molde de prédio compartilhado do `master` serve para qualquer porta com duas
   entradas."** Não serve: a guarda dele só está certa quando a origem é mapa AO AR LIVRE.
   Ver a decisão (c).
5. **"Dois argumentos depois de `warp MAP_X` são mapa e índice de warp."** São mapa e par de
   coordenadas. Ver a decisão (b).

### Armadilhas de gerador que a próxima rodada herda

Estão aqui juntas porque todas têm a mesma forma: **rodar o gerador no modo padrão desfaz
trabalho de outro lote, e nada fica vermelho.**

- `objetos_galar.py` e `fala_galar.py` no modo PADRÃO devolvem `galar_objetos.inc` e
  `galar_fala.inc` ao português. Quem os rodar por engano roda
  `aplica_traducao_galar.py --aplica` em seguida e confere 849 de 849 e `checa_texto` T07 de
  Galar em 1.
- `cenas_galar.py` reescreve `data/maps/Galar_*/scripts.inc`, e agora é lá que moram as
  cenas da Dex de Galar (os 7 mapas do bloco `@ >>> Dex completa >>>`). Rodá-lo apaga o
  bloco; repor é `distribui_dex.py --galar-objetos --aplica`.
- `placas_galar_c.py` e `objetos_galar.py` reescrevem `bg_events` de Galar, e as 45 placas de
  porta fechada só sobrevivem porque eles preservam quem tem `origem: "porta fechada
  (portas_mortas_galar.py)"`.
- `escreve_tabela_galar` refaz os quatro baldes de Galar do censo. Decisão de conteúdo
  escrita à mão no `dex_distribuicao.json` não sobrevive: ela tem que virar código.
- **Dois geradores que repõem os objetos deles no FIM da lista brigam entre si.** O
  `estaticos_galar.py` faz isso, e o escritor novo da Dex de Galar fazia também: depois de
  rodar os dois na ordem certa, uma segunda passada do primeiro mexeria em 3 mapas sem nada
  ter mudado, e o `--demo` dele reprovava por não ser idempotente. Consertado pondo os
  objetos da Dex ANTES do bloco de estáticos (`aplica_galar_objetos`), e os dois `--demo`
  voltaram ao verde `[V]`. Quem escrever o terceiro gerador de objeto de Galar herda a
  regra: o bloco de `estaticos_galar` é o último da lista, sempre.
- **Checagem que existe para pegar nome de OUTRO dono precisa tirar o próprio bloco da
  busca.** O `--demo-galar` reprovou com as 10 flags da Dex de Galar assim que o escritor as
  gravou pela primeira vez: ele procurava o nome no `flags.h` inteiro e passou a acusar quem
  o escreveu. Consertado `[V]`.

### O portão desta rodada

`[V] export DEVKITARM=...; make -j8 > /tmp/build-cartucho2.log 2>&1; echo $?`

| medida | antes (abertura da onda 2) | depois |
|---|---|---|
| exit code do `make` | 0 | **0** |
| ROM ocupada | 32.387.740 B, 96,52% | **32.408.516 B, 96,58%** (+20.776 B) |
| EWRAM | 225.856 B, 86,16% | **225.856 B, 86,16%** |
| IWRAM | 28.404 B, 86,68% | **28.404 B, 86,68%** |
| md5 da ROM | `d9ecacb2d27bd84e99b1d07371305dd3` | **`fb4e4c5a81298a52a4b827945ed4942d`** |

Os três `.inc` novos e o bloco de cena dos 7 mapas compilaram de primeira. O lock
(`mkdir /tmp/pokemon-claude-build.lock`) envolveu **só o `make`** e foi devolvido com
`rm -rf` logo depois dele; T11 e suíte rodaram FORA do lock, sobre a cópia
`/private/tmp/claude-501/c2-onda2b/c2-onda2b.gba` **com o `pokeemerald.map` copiado ao
lado**, que é o que o T11.3 lê.

`[V] python3 dev_scripts/guarda_save.py` -> **SAVE COMPATIVEL**. SaveBlock1 em 14.964 B de
15.872 (94,3%), 2.400 mapas, 2.252 ids de treinador e **1.733** apelidos de flag/var (eram
1.720; os 13 novos são as 12 da Dex de Galar mais a `FLAG_GALAR_PORTA_G06M12_72C` do lote F,
e apelidar `FLAG_UNUSED` é ACRÉSCIMO, não mudança de índice).

`[V] T11 3 de 3`, contra `/private/tmp/claude-501/c2-t11-antiga` (md5
`ac8ed5419ab69cacece45ad6479e6063`, intacta no disco).

`[V]` **Suíte inteira: 1.062 de 1.063**, com o T11.3 pulado (ele só prova algo com duas
ROMs) e **ZERO reprovados**, que é exatamente o piso. Rodada **bloco a bloco**, 115 blocos,
com o placar gravado em disco a cada bloco em
`/private/tmp/claude-501/c2-onda2b-suite/placar.txt` e o log de cada bloco ao lado, sobre a
cópia da ROM e FORA do lock. O total foi conferido de dois jeitos independentes, somando os
`[OK]` de cada log e somando as linhas `N/M passaram`.

**Quatro casos reprovaram na primeira varredura, e os quatro eram RÉGUA VELHA.** Cada um foi
provado com caso de diagnóstico no emulador ANTES de mudar linha nenhuma, e a recalibração
saiu em commit próprio (`91e0ba7bb8`), depois dos lotes:

- **T130.5 e T130.6** entravam em `Galar_Postwick21` pelo **warp 2**, que era o auto-warp de
  (10,2). O lote G o FECHOU nesta onda, e o índice 2 virou lápide em (5,8): os dois casos
  caíam em (2,7) e nem chegavam perto da TV. O sinal de que era entrada e não obra é que o
  **par negativo reprovou junto, com a MESMA posição errada** (defeito de placa reprova só o
  positivo). O `bg_event` de (6,1) com `GalarObj_G04M00_bg0` está intacto no `map.json` `[V]`.
  Diagnóstico: mesma prova, entrada pelo warp 3 em (3,9), dez UP até (3,2), quatro RIGHT até
  (6,2), um UP para virar, A. **Passou, e o par negativo também** `[V]`. Bloco refeito
  inteiro: **T130 10 de 10** `[V]`.
- **T159.1 e T159.2** cravavam a espécie de dois antros de raide (439 e 989). Esta onda
  rodou `estaticos_galar.py --aplicar` com o tradutor de espécie corrigido, e a rotação andou
  em 51 antros: hoje são 975 (`PONYTA_GALAR`) e 987 (`ZIGZAGOON_GALAR`), conferidos no
  `map.json` dos dois tiles `[V]`. Mapa, posição e nível continuam certos, e as duas espécies
  continuam DIFERENTES uma da outra, que é o que o par prova (o veto de vizinhança de 3
  mapas). Diagnóstico com as espécies de hoje: **os dois passaram** `[V]`. Bloco refeito
  inteiro: **T159 14 de 14** `[V]`.

**Armadilha que custou uma varredura inteira, e que a próxima rodada não deve repetir:**
`carrega_casos()` do `testa_critico.py` lê TODOS os `dev_scripts/testes_criticos/*.json` a
cada bloco. Escrever um arquivo de diagnóstico ali COM A SUÍTE RODANDO derrubou os 13 blocos
seguintes (T164 a T181 saíram com 0 caso rodado, e o placar mostrava `ok=0 ruim=0`, que lê
como "bloco vazio" e não como "bloco que morreu"). Os 13 foram refeitos e deram verde. Arquivo
de diagnóstico vai para fora de `testes_criticos/`, ou espera a suíte acabar.

**O T176.3 é INTERMITENTE, e não regressão.** Ele reprovou em duas passadas do bloco e passou
**3 de 3 rodado sozinho**; o bloco inteiro deu 12 de 12 na terceira, e o MESMO bloco sobre a
ROM da abertura também dá 12 de 12 `[V]`. O diário da abertura já o nomeia como um dos dois
instáveis conhecidos, junto com o T108.2.

`[V] python3 dev_scripts/qa/roda_qa.py --demo` -> **verde nas SEIS varreduras**.
`[V] python3 dev_scripts/valida_conectividade.py --demo` -> a varredura nova tem mutação
plantada própria, e ela morde.
`[V] python3 dev_scripts/distribui_dex.py --demo-galar` e `--demo-galar-objetos` -> os dois
verdes, o segundo com mutação plantada no prefixo `GALAR` do nome de flag (sem ele,
`FLAG_HIDE_DEX_ZACIAN_HERO` colide com o Zacian que a Dex das cinco pôs em Kanto).

### Os commits desta rodada

| # | hash | lote |
|---|---|---|
| 1 | `090f1bff9a` | G: portas mortas, 45 placas e o gerador |
| 2 | `c4177136bd` | F: portas de script e a régua de conectividade |
| 3 | `f5761643a1` | I: 168 NPCs, 20 placas e o resgate de texto |
| 4 | `d1593199eb` | H: Dex de geração 8 em Galar, encontros, estáticos e presentes |
| 5 | `91e0ba7bb8` | recalibração de T130.5, T130.6, T159.1 e T159.2, no portão |

**A partição de arquivo foi por ÚLTIMO DONO, e não por reconstrução de estado
intermediário.** Cada `map.json` entrou no commit do último lote que o tocou, para que
nenhum commit tivesse mapa apontando para rótulo ainda não commitado. `data/event_scripts.s`
e `include/constants/flags.h` foram os únicos partidos de verdade, com uma versão por commit
feita com `git hash-object` mais `git update-index --cacheinfo`; a versão final de cada um
bate byte a byte com a árvore `[V]`. Consequência a saber: o commit do lote F **não tem
nenhum `map.json`**, porque os 6 mapas dele foram tocados depois pelo I ou pelo H. Cada
commit usou `GIT_INDEX_FILE` próprio e lista fechada, nunca `add -A`, e no fim a árvore de
trabalho é IDÊNTICA ao `HEAD` `[V] git diff-index --cached --name-status HEAD` vazio.

Os intermediários do lote I (`bloco_*.json`, `*.en.json` e `en/`) foram apagados depois de
conferido que `resgate_galar_texto.json` tem as 107 entradas; do diretório ficou versionado
só o `validacao.txt`. Varredura de blob: nada acima de 5 MB, nenhum `.gba` e nenhum `.sav`
no intervalo `origin/cartucho-2..HEAD` `[V]`.

### O que ficou de fora, e por quê

- **10 portas `GalarTrn_*`**, em `galar_treinadores.inc`. O gerador de treinadores não tem a
  regra de precedência de `GalarPorta_`, então pendurá-las agora arriscaria apagar o script
  de treinador. Elas não creditam alcance nenhum hoje: a régua nova só conta rótulo que o
  mapa CHAMA, e nenhuma delas está pendurada.
- **131 prédios compartilhados** da `lente_warps` (hoje 128). Cada um é uma decisão de para
  onde a saída devolve, e o mecanismo é o `MAP_DYNAMIC` provado na decisão (c).
- **8 travas P1 novas da `lente_portas`**, consequência de fechar porta. Mesma natureza das 8
  de Sinnoh.
- **226 linhas `script_objeto` adiadas** e **34 `map_script` adiadas**. A fila não tem mais
  nada PENDENTE (0 de 3.195), e o que sobra tem motivo escrito na própria linha.
- **42 órfãos sem saída nenhuma e 27 mapas de FireRed dentro dos grupos de Galar** continuam
  aguardando decisão de escopo do Gui.
- **`distribui_dex.py --demo` GERAL continua vermelho**, e não foi consertado de propósito:
  ele começa pelo `plano_congelado`, que compara a tabela das cinco regiões (de 21/08) com um
  plano refeito do censo de hoje, e o censo mudou quando Galar ganhou fonte. Reconciliar
  aquela tabela é obra própria, com medição própria, e não pode ser efeito colateral desta.
  O `--demo-galar` e o `--demo-galar-objetos` são verdes.
- **A curva de nível de Galar continua fora do lugar.** Os encontros importados vão de nível
  2 a 60 e os treinadores estão em 255. Ninguém mediu ainda qual dos dois está errado.
- **A tela de créditos dentro do jogo** continua sendo pendência da fase de montagem.
- **`portas_script_galar.py --demo` fica VERMELHO em três asserções, e NÃO foi
  recalibrado.** Ele crava o tamanho dos quatro baldes de porta de script medidos ANTES
  desta onda, e os três primeiros mudaram porque a obra mexeu neles: o balde A (o objeto da
  fonte não existe no nosso `map.json`) caiu de 22 para 15, que são exatamente os 7 objetos
  novos do lote F; o balde B (objeto mudo) caiu de 22 para 2, porque F e I penduraram
  script neles; e o balde C (objeto com rótulo de outra coisa) subiu de 16 para 43 pelo
  mesmo motivo `[V]`. O balde D e as outras oito asserções continuam verdes. **Mexer em
  régua na mesma sessão que criou a mudança é o movimento que mais merece desconfiança**, e
  por isso a recalibração fica como decisão da condutora, com a repartição acima já medida.
  Enquanto isso, quem rodar esse `--demo` lê este parágrafo antes de caçar defeito.

### Perguntas ao Gui

As três da onda 1 continuam abertas (datamine canônico de encontros, os 42 mapas sem saída,
e agora os 27 de FireRed). Duas novas:

4. **Os 2 textos do lote I sem tradução** (`dev_scripts/onda2_lote_i_pulados.txt`) ficaram de
   fora por bloqueio na transcrição. São 2 de 109.
5. **O nível dos presentes e dos iniciais de Galar é 5**, que é o padrão do molde das cinco
   regiões. Galar hoje é conteúdo de fim de jogo (encontros até 60, estáticos em 70), e um
   inicial nível 5 entregue ali é decoração e não jogo. Subir custa uma linha.

### A ROM para o Gui

`Claude Workspace - Pokemon Rom Hacks/roms/pokemon-claude-cartucho-2-2026-09-06b.gba`, com o
`.md5` ao lado, fora do repo. É a ROM que os portões desta seção mediram.

### Como retomar

O primeiro comando continua sendo o da seção 0:

```
git ls-remote --heads origin cartucho-2
```

---

## Onda 2, abertura (07/09/2026): MERGE DO MASTER `80b064ee91`, A C28 VIRA NATIVA E O MOLDE DE PLACA FICA O DO CARTUCHO 1 (mesclador Opus)

Abertura da onda 2 da Frente A, pela política da seção 2: enquanto o commit de remoção de
Unova e Galar não existir na `master`, cada rodada começa com `git merge master`. **Conferido
hoje, não presumido:** a `master` ainda tem 438 pastas `Galar_*`, então é MERGE e não
cherry-pick. Tudo abaixo foi medido nesta worktree, com o comando ao lado, e `[V]` marca o
que foi conferido nesta rodada.

### Os conflitos, e a resolução de cada um

O merge trouxe 233 arquivos. **Cinco foram tocados pelos dois lados**, e só um deu conflito
de texto; os outros dois que precisaram de julgamento o git casou CALADO, que é o pior jeito
de um conflito aparecer.

| arquivo | o que houve | resolução |
|---|---|---|
| `data/scripts/galar_treinadores.inc` | 12 conflitos de texto, todos no `Galar_Circhester03`: as duas frentes consertaram o MESMO defeito C28 com moldes diferentes | ficou o do `master`, por medição e não por hierarquia (abaixo) |
| `dev_scripts/treinadores_galar.py` | conflito SEMÂNTICO: o auto-merge empilhou os dois moldes de placa, o nosso (`de_placa`, com `continue`) ANTES do do `master` (`e_placa`) | o bloco nosso saiu, 60 linhas; o `motivos_de_linha` e o `--fila` da onda 1 ficaram |
| `include/constants/vars.h` | colisão de ENDEREÇO sem conflito de texto: a rodada 13 deu `VAR_UNUSED_0x4114` a `VAR_ELEVADOR_GOLDENROD`, e a onda 1 já tinha dado o mesmo a `VAR_GALAR_G10M23_CENA` | a nossa var foi para `VAR_UNUSED_0x4116`, que estava livre `[V]` |
| `src/chapter_jump.c` | auto-merge, conferido | o campo `flagEnredo` do `master` entrou no fim da `GinasioDoHack` e a nossa `ParadaDoHack` com o `sParadasGalar` ficou inteira `[V]` |
| `data/event_scripts.s` | auto-merge, conferido | os 7 includes de Galar e o `portas_fechadas.inc` do `master` estão todos lá `[V]` |

**Por que o molde do `master` e não o nosso.** Os dois escrevem `lock` + `goto_if_defeated` +
`msgbox` + `trainerbattle_no_intro`; a diferença é uma linha. O nosso punha `setvar
VAR_LAST_TALKED, LOCALID_NONE`, e `EventScript_DoNoIntroTrainerBattle` faz `applymovement
VAR_LAST_TALKED, Movement_RevealTrainer` sem perguntar: com `LOCALID_NONE` o
`GetObjectEventIdByLocalId` devolve `OBJECT_EVENTS_COUNT` e o `applymovement` escreve **um
elemento depois do fim de `gObjectEvents`**. O `LOCALID_PLAYER` do `master` aponta para objeto
que existe, e `reveal_trainer` em objeto que não é BURIED nem disfarce é no-op
(`src/event_object_movement.c:8769`). O rótulo `_Fim` virou `_Depois` junto, porque é o que o
gerador do `master` emite.

**A armadilha que quase passou.** Se o gerador tivesse ficado como o auto-merge deixou, o
`de_placa` (nosso, com `continue`) rodaria ANTES do `e_placa` e apagaria o molde do `master` na
próxima geração, devolvendo o `LOCALID_NONE` ao arquivo em silêncio. Conflito que o git não
marca é o que custa a rodada seguinte. Depois do conserto, `dev_scripts/treinadores_galar.py` é
byte a byte o do `master` MAIS o que a onda 1 acrescentou `[V] diff`.

**Nada de conflito sobrou:** zero marcadores na árvore inteira, e nenhum apelido de
`VAR_UNUSED_*` aponta duas vezes para o mesmo endereço `[V]`. Nenhum `.inc` precisou mudar pela
renumeração da var, porque os dois mapas (`Galar_Route1601` e `Galar_Route1603`) citam a var
pelo nome.

Só **um** `map.json` de Galar mudou pelo merge: `Galar_WarmUpTunnel01` ganhou o warp gêmeo de
(39,37) para a Isle of Armor (`cfa0d30bd4`). O Slumbering Weald NÃO foi tocado, e isso é o que
o próprio commit do `master` diz: ele saiu da lista de meias portas.

### Os números do merge, antes e depois

Tudo abaixo rodado DEPOIS do merge e ANTES do build, que é onde regressão de merge aparece.

| medida | antes (diário da onda 1) | depois do merge | comando |
|---|---|---|---|
| fila `porta_morta` pendente | 226 | **226** `[V]` | `python3 dev_scripts/fila_galar.py` |
| fila, total pendente | 226 de 3.195 | **226 de 3.195** `[V]` | idem |
| completude Galar, `placas` | 72,3% | **72,3%** `[V]` | `python3 dev_scripts/completude.py --detalhe Galar` |
| completude Galar, `script` | 59,2% | **59,2%** `[V]` | idem |
| órfãos de Galar | 141 | **141** `[V]` | `python3 dev_scripts/valida_conectividade.py` |
| warps quebrados | 0 | **0** `[V]` | idem |
| alcance geral | 2.053 de 2.289 | **2.052 de 2.289** `[V]` | idem |
| T07 de Galar (`checa_texto`) | 1 | **1** `[V]` | `python3 dev_scripts/qa/checa_texto.py` |
| português em Galar | 1 | **1** `[V]` | idem |
| total de achados do `checa_texto` | 2.124 | **2.124** `[V]` | idem |
| `checa_scripts`, travas | 13, nenhuma em Galar | **13, nenhuma em Galar** `[V]` | `python3 dev_scripts/qa/checa_scripts.py` |
| **C28** | não existia nesta branch | **NATIVA, 0 achados em TODAS as regiões** `[V]` | idem, e `--demo` verde com a C28 mordendo |
| `lente_warps`, Galar | não existia aqui | **130** (P2 47, P4 83, P1 e P3 zero) `[V]` | `python3 dev_scripts/qa/lente_warps.py` |
| `lente_warps`, Unova | não existia aqui | **38** `[V]` | idem |
| `lente_portas`, travas em Galar | não existia aqui | **268** `[V]` | `python3 dev_scripts/qa/lente_portas.py` |
| censo da dex, Galar | 592 | **592** `[V]` | `python3 dev_scripts/censo_dex.py` |

**A ÚNICA queda é o alcance, de 2.053 para 2.052, e ela é HONESTA e do `master`, não nossa.**
O mapa que saiu do grafo é o `MAP_LAKE_OF_RAGE_LOW_TIDE`, de JOHTO, e ele saiu porque a rodada
13 tirou a conexão duplicada da Route 43. O `ESTADO.md` da `master` registra a mesma queda com
a mesma causa (lá ela aparece como 1.966 -> 1.965, porque a régua dele conta outro
denominador). Galar não perdeu um mapa `[V]`.

Os números de `lente_warps` e `lente_portas` batem exatamente com os que o `ESTADO.md` da
`master` mede (Unova 38 e Galar 130 na lente de warp, Galar 268 na varredura cheia), o que é a
prova de que as ferramentas chegaram inteiras e estão medindo a mesma árvore.

### O portão desta abertura

`[V] export DEVKITARM=...; make -j8 > /tmp/build-cartucho2.log 2>&1; echo $?`

| medida | antes (onda 1) | depois do merge |
|---|---|---|
| exit code do `make` | 0 | **0** |
| ROM ocupada | 32.376.452 B, 96,49% | **32.387.740 B, 96,52%** (+11.288 B) |
| EWRAM | 225.856 B, 86,16% | **225.856 B, 86,16%** |
| IWRAM | 28.404 B, 86,68% | **28.404 B, 86,68%** |
| md5 da ROM | `ea0c2858daf02807ad379a9be20502c5` | **`d9ecacb2d27bd84e99b1d07371305dd3`** |

O lock (`mkdir /tmp/pokemon-claude-build.lock`) envolveu **só o `make`**, e foi devolvido logo
depois dele; T11 e suíte rodaram FORA do lock, sobre cópia da ROM em
`/private/tmp/claude-501/c2-onda2.gba`. **Armadilha medida hoje:** o `rmdir` do lock FALHA
(`Directory not empty`) se alguém tiver escrito arquivo de dono dentro dele, e a mensagem passa
despercebida no meio da saída do `make`. Quem escreve dono devolve com `rm -rf`; quem não escreve
devolve com `rmdir`. Nesta rodada o `rmdir` falhou e o lock só saiu na chamada seguinte.

`[V] python3 dev_scripts/guarda_save.py` -> **SAVE COMPATIVEL**. SaveBlock1 em 14.964 B de
15.872 (94,3%), 2.400 mapas, 2.252 ids de treinador e **1.720** apelidos (eram 1.718: o merge
trouxe os apelidos novos da rodada 13, que são ACRÉSCIMO e não mudança de índice).

`[V] T11 3 de 3`, contra `/private/tmp/claude-501/c2-t11-antiga` (md5
`ac8ed5419ab69cacece45ad6479e6063`, intacta no disco). **Detalhe que custou uma execução:** o
T11.3 lê o `.map` do linker AO LADO da ROM2, então a cópia da ROM precisa do
`pokeemerald.map` copiado junto com o mesmo nome de base, senão o caso morre com
`FileNotFoundError` depois de o T11.1 e o T11.2 já terem passado.

`[V] python3 dev_scripts/qa/roda_qa.py --demo` -> **verde nas SEIS varreduras**, agora com
`lente_warps` e `lente_portas` dentro.

`[V]` **Suíte inteira: 1.062 de 1.063**, com o T11.3 pulado (ele só prova algo com duas ROMs) e
**ZERO reprovados**, o que é exatamente o piso que esta abertura tinha que segurar. Rodada
**bloco a bloco** pela lição 2 da rodada 13, 115 blocos, com o placar gravado em disco a cada
bloco em `/private/tmp/claude-501/c2-onda2-suite/placar.txt` e o log de cada bloco ao lado, sobre
a cópia `/private/tmp/claude-501/c2-onda2.gba` e FORA do lock. O total foi conferido de dois
jeitos independentes: somando os `[OK]` de cada log e somando as linhas `N/M passaram`, e os dois
dão 1.062 de 1.063 `[V]`.

**Não houve queda para diagnosticar.** A suspeita da abertura era a interação merge + onda 1, e
ela não se realizou: os dois casos que a onda 1 recalibrou (T108.8 e T159.13) passaram na
varredura completa desta vez, e nenhum caso novo do `master` sobre Galar (T175, T176, T180,
T181 e o T171 dos prédios compartilhados) reprovou. Nada foi recalibrado nesta rodada, e é bom
que fique escrito: recalibrar régua sem vermelho é como mexer em caso de teste sem motivo.
Também não apareceu o intermitente T108.2 nem o T176.3, os dois instáveis conhecidos.

`[V] git rev-list --objects origin/cartucho-2..HEAD | git cat-file --batch-check` -> o maior
objeto do intervalo é `data/layouts/layouts.json` com 948 KB, e não há nenhum `.gba`, `.sav`
nem nada acima de 5 MB.

### As medições que a onda 2 pediu, e o que elas mudam no plano

Cinco perguntas da condutora, todas respondidas com comando e número, nenhuma com memória.

**(a) O que a coluna `script` da completude conta, exatamente.** O código está em
`dev_scripts/completude.py:888`, e a conta é dos DOIS lados na NOSSA árvore, não na fonte:

- **numerador** = `object_event` de `data/maps/Galar_*/map.json` cujo campo `script` não é
  `"0"` nem vazio **e** cujo `origem` não é `estaticos_galar`: **746**.
- **denominador** = todos os `object_event` de Galar (**2.278**) menos os **1.018** encontros
  estáticos: **1.260**.
- **746 de 1.260 = 59,2%** `[V]`, e os **514** que faltam são NPC colocado e MUDO.

O que faz subir é UMA coisa só: escrever `script` num desses 514. Cada NPC vale **+0,079 pp**;
os 198 `script_objeto` adiados da onda 1 valem **+15,7 pp** se todos entrarem, o que levaria a
coluna a **74,9%**. Colocar NPC novo **não** faz subir: ele entra nos dois lados da fração e o
denominador cresce junto.

**A coluna `placas` é outra régua, e o denominador vem da FONTE**: 214 `bg` do demake, menos os
que são "lixo de leitura" e os 12 "sem item traduzível", dão **202**; o numerador é o total de
`bg_events` que os nossos `map.json` têm hoje, **146**. **146 de 202 = 72,3%** `[V]`. **Sim, as
21 placas adiadas por tile ocupado contam no denominador** e não no numerador: escrevê-las
levaria a coluna a **167 de 202 = 82,7%**.

**(b) Os 40 órfãos com porta de script que parte de mapa VIVO.** São 40 destinos e **77 portas**
(uma porta é um comando de `warp` dentro de um script da fonte). **Nenhuma das 77 está
transcrita na nossa árvore: zero rótulo de `data/scripts/galar_*.inc` contém o `warp`** `[V]`.
A transcrição é do zero em todos os casos, e o balde diz quanto trabalho é cada um:

| situação na NOSSA árvore | portas | destinos |
|---|---|---|
| A. o objeto da fonte NÃO existe no nosso `map.json` (índice fora do array) | 31 | 22 |
| B. o objeto existe e está MUDO (`script: "0"`) | 7 | 5 |
| C. o objeto existe, mas com rótulo de OUTRA coisa (`GalarFala_*` 12, `GalarSelvagem_*` 9, `GalarEstatico_*` 1) | 22 | 15 |
| D. gatilho de coordenada, e o nosso `map.json` de origem tem **zero** `coord_events` | 17 | 5 |

O balde **B** é o mais barato (o objeto já está no lugar, falta o script), o **C** é o mais
delicado (o objeto está lá com outro papel: mexer nele é decidir se a espécie selvagem vira
porta), o **A** e o **D** pedem escrever objeto ou gatilho novo no `map.json`, que é dono
diferente. Os destinos com mais portas são `STOW_ON_SIDE_01` (12, de 9 mapas diferentes),
`HAMMERLOCKE_06` (6, todas gatilho), `UNDERWATER_01` (6) e `HULBURY_01` (5).

**(c) As 226 `porta_morta`, por causa.** Duas causas, e as duas são obra de MAPA:

| causa | linhas |
|---|---|
| destino é mapa vanilla do FireRed que o demake não redesenhou (não está entre os 438) | **188** |
| warp de chegada não existe no mapa de destino (par que falta) | **38** |

São **39 destinos distintos** no primeiro balde, e ele é MUITO concentrado: o destino `0.0` da
fonte responde por **95** das 188, e o `1.76` por mais 25. Do nosso lado, **98 mapas** têm
`porta_morta`, e `Galar_Postwick50` sozinho tem **63**. Todas as 226 têm `no_mapa: true`, ou
seja **o warp EXISTE no nosso `map.json`**, e **225 das 226 apontam para o próprio mapa**
(auto-warp): a porta abre e devolve o jogador para onde ele já estava.

**Cruzamento com a `lente_warps`: a interseção é ZERO** `[V]`. As 130 travas de Galar da lente
(47 P2 e 83 P4) e as 226 `porta_morta` da fila são conjuntos DISJUNTOS, e o motivo é
mecânico: a lente cobra a VOLTA (porta que não devolve, escada que não devolve), e o auto-warp
devolve certinho, para o mesmo lugar. Consertar uma lista não move a outra, e quem prometer
"conserto de warp" tem que dizer qual das duas.

**(d) `dev_scripts/onda1_lote_e_pedidos_scripts.txt`, em cinco linhas.** (1) O lote E já pôs
Galar de 0 para 592 sem tocar em mapa, e nada do arquivo é pré-requisito disso. (2) Pedido 1:
`dex_distribuicao.json` tem 362 colocações e ZERO em Galar, então os 31 pokémon de geração 8 que
só têm fonte nas quatro regiões do cartucho 1 continuam indo para lá; abrir Galar no
`distribui_dex.py` é do lote E, mas o objeto e o script de cada colocação `estatico`/`presente`
são de quem manda em `map.json` e `scripts.inc`. (3) Pedido 2: `Galar_WildArea12`,
`Galar_IsleOfArmor35` e `Galar_IsleOfArmor36` perderam a tabela de grama porque a fonte traz
NÍVEL 0 nos 12 slots, e a decisão que falta é uma linha (que faixa de nível usar). (4) Pedido 3:
7 slots costurados por forma repetida (Indeedee, Sandslash, Burmy, Gastrodon, Raichu, Lycanroc)
mais cinco grafias tortas e o `.` das formas regionais, hoje corrigidos SÓ no
`importa_encontros_galar.py`; levar para `estaticos_galar.py` recupera estático recusado. (5) O
apêndice lista as 140 entradas de geração 8 sem fonte em Galar (de 197: 95 bases e 102 formas,
57 já com fonte), e o arquivo diz em voz alta que o nível dos encontros de Galar é o da FONTE e
nunca passou pelo `curva_selvagem.py`.

**(e) O que o `ESTADO.md` da `master` (seção 0.u) tem de infra que vale para cá.** Sete lições,
e cinco mudam como esta branch trabalha: **(1) lock furado é pior que lock nenhum**, ele envolve
o `make` e nada mais, e frente com build própria usa worktree própria, que é exatamente o que
esta branch já faz; **(2) suíte inteira num processo só é aposta** com várias frentes na
máquina, então roda-se BLOCO A BLOCO com o placar gravado em disco a cada bloco (foi o que esta
rodada fez, em `/private/tmp/claude-501/c2-onda2-suite/placar.txt`); **(3) `.sav` de teste em
caminho absoluto compartilhado é veredito sorteado**, e a dívida continua aberta no
`testa_critico.py`; **(4) índice do git é compartilhado**, então cada frente commita com
`GIT_INDEX_FILE` próprio e lista fechada de arquivos, nunca `add -A`; **(5) sem `--offsets` o
`gba_runner` usa os offsets do cabeçalho dele, e nesta build `vars[]` mora em `0x18B8` e não em
`0x13E0`**, o que faz escrita de var cair no lugar errado em silêncio. As outras duas (nome
genérico de ferramenta descartável, e `open(caminho, "w")` antes do `assert` truncando arquivo)
valem como higiene. Nenhum commit da rodada 13 está marcado MOTOR de um jeito que peça
cherry-pick: o merge trouxe tudo.

### A fila da onda 2, depois destas medições

A ordem da seção "A fila da ONDA 2" da onda 1 continua valendo, com três correções medidas hoje:

1. As **95 portas de script** não têm transcrição nenhuma pronta: as 77 que partem de mapa vivo
   são obra do zero, e o balde **B** (7 portas, 5 destinos) é por onde começar, porque o objeto
   já está no mapa.
2. As **226 `porta_morta`** e as **130 travas da `lente_warps`** são listas DISJUNTAS. São duas
   obras, não uma.
3. A coluna `script` sobe **+0,079 pp por NPC**, e os 198 adiados da onda 1 são **+15,7 pp**: é
   a alavanca mais barata que existe hoje na completude de Galar.

---

## Onda 1 (06/09/2026): GALAR PARA DE SE CHAMAR POSTWICK, PERDE 105 ÓRFÃOS, ESVAZIA A FILA E PASSA A FALAR INGLÊS (condutora Opus, cinco executores Opus, fechador Opus)

Primeira onda de obra da Frente A. Cinco lotes com dono exclusivo por TIPO de arquivo, e
não por mapa, que é o que impediu a colisão prevista na seção 5. Tudo abaixo foi medido
nesta worktree, com o comando ao lado, e `[V]` marca o que foi conferido nesta rodada.

### Placar por lote, antes e depois

**Lote A/AB, MAPSEC** (`dev_scripts/conserta_mapsec_galar.py`)

| medida | antes | depois |
|---|---|---|
| `map.json` com `MAPSEC_GALAR_POSTWICK` | 172 | **32** `[V]` |
| linhas de Galar em `dev_scripts/qa/nomes_popup_revisao.csv` | 140 | **0** `[V]` |
| linhas totais do CSV | 148 | **8** (4 de Sinnoh, 2 de Unova, 1 de Johto) `[V]` |

Os 32 que sobram são os `Galar_Postwick*` de verdade, e eles não foram tocados. A regra é a
da seção 3.4: nome novo da pasta, sem `Galar_`, sem o número do fim, e sem `Indoor`/`Cave`
quando o radical não estiver em `secoes`.

**Lote B, órfãos** (`dev_scripts/liga_orfaos_galar.py`, `dev_scripts/anda_scripts_galar.py`)

| medida | antes | depois |
|---|---|---|
| mapas de Galar que nenhum caminho alcança | 246 | **141** `[V]` |
| alcance geral | 1.966 de 2.289 | **2.053 de 2.289** `[V]` |
| warps quebrados | 0 | **0** `[V]` |
| porta única que não devolve | 4, todas de Galar | **4, as mesmas** `[V]` |
| mapas com `cortado_por` novo | 0 | **34** (16 sobra de FireRed, 18 duplicata) `[V]` |
| warps religados | 0 | **1** (`Galar_WildArea20`) `[V]` |

`[V] python3 dev_scripts/valida_conectividade.py`

**Os 105 que saíram não saíram todos pelo mesmo caminho, e a repartição foi MEDIDA, não
deduzida**: rodando o validador com o `src/chapter_jump.c` velho por cima da árvore nova, os
órfãos de Galar dão **211**. Ou seja, **35 saíram pelos carimbos e pelo warp religado** e
**70 saíram porque o seletor de capítulo ganhou onze paradas novas** `[V]`. O motivo é que
`valida_conectividade.py` tira as SEMENTES de alcance dos `HEAL_LOCATION_*` citados em
`chapter_jump.c` (`sementes_do_seletor`), e com uma semente só a Isle of Armor e a Crown
Tundra inteiras contavam como inalcançáveis sem terem defeito nenhum. Quem for medir órfão
de Galar depois disto olha as duas coisas juntas.

O andador de bytecode do demake (`anda_scripts_galar.py`) andou **3.455 scripts da fonte**,
3.355 limpos e 100 descarrilados, e é ele que separa os 141 que sobram:

| balde | mapas | onde está a lista |
|---|---|---|
| têm porta de SCRIPT na fonte | **95** | `dev_scripts/orfaos_galar_por_script.json` |
| dos 95, a porta parte de mapa VIVO | 40 | mesmo arquivo |
| não têm entrada nenhuma | 46 | mesmo arquivo, campo `orfaos_sem_entrada_nenhuma` |
| dos 46, sobram depois do teste de blockdata | **42** | `dev_scripts/orfaos_galar_sem_saida.txt` |

**Lote C, fila** (`data/scripts/galar_*.inc`, geradores)

`[V] python3 dev_scripts/fila_galar.py`

| tipo | pendente antes | pendente depois | feita | descartada | adiada |
|---|---|---|---|---|---|
| map_script | 175 | **0** | 38 | 122 | 34 |
| placa | 25 | **0** | 113 | 0 | 21 |
| porta_morta | 226 | **226** (todas bloqueadas) | 0 | 0 | 0 |
| script_objeto | 772 | **0** | 1.765 | 678 | 198 |
| **TOTAL** | **1.198** | **226** | 1.916 | 800 | 253 |

`[V] python3 dev_scripts/completude.py --detalhe Galar`

| | mapas | objetos | warps | placas | script | arte |
|---|---|---|---|---|---|---|
| antes | 100,0% | 103,6% | 100,0% | 70,3% | 59,2% | 48 (32) |
| depois | 100,0% | 103,6% | 100,0% | **72,3%** | 59,2% | 48 (32) |

A coluna `script` não anda nesta onda de propósito: ela conta NPC com fala, e o lote C
trabalhou em `map_script` e `placa`. Ela só anda quando `script_objeto` voltar à obra.

**C28**, a checagem que ainda não mora nesta branch (seção 2), medida com a cópia do working
tree da `master`: **18 travas antes (12 em Galar, 6 em Unova), 6 depois (todas de Unova)**
`[V]`. As 12 de Galar eram `trainerbattle_single` chamado de dentro de uma placa, tela azul
garantida em `src/battle_setup.c:1258`; viraram `lock` mais `goto_if_defeated` mais `msgbox`.
`checa_scripts.py` desta branch (C01 a C27) fica em **13 travas, nenhuma em Galar**, igual ao
que era `[V]`.

**Lote D, tradução** (`dev_scripts/traducao_galar.json`, `aplica_traducao_galar.py`)

`[V] python3 dev_scripts/qa/checa_texto.py`

| medida | antes | depois |
|---|---|---|
| T07 de Galar, com a régua NOVA | 310 | **1** `[V]` |
| blocos de Galar em português | 310 | **1** |
| português SEM acento | 58 | **1** |
| blocos de Galar em inglês | 28 | **323** |
| blocos de texto de Galar | 1.120 | **1.124** |
| T01 de Galar | 3 | **0** |
| T02 de Galar | 2 | **1** |
| T08 (acento) | 58, todas de Galar | **não mede mais Galar** |
| total de achados do arquivo | 2.437 (régua nova sobre a árvore velha) | **2.124** |

O 1 que sobra é `GalarFala_G09M10_o14_Text`, defeito de charmap deixado à vista de propósito.
As três medidas de "antes" com a régua nova foram tiradas rodando o `checa_texto.py` de hoje
dentro de uma worktree do commit `8a9ebcb692`, e não deduzidas `[V]`.

O aplicador é idempotente e foi provado nos três passos: `--dry-run` (849 casam, 0 não
casam), `--aplica`, `--dry-run` de novo (849 já aplicadas, 0 casam) `[V]`.

**Lote E, Dex e encontros** (`src/data/wild_encounters.json`, `dev_scripts/censo_dex.py`)

`[V] python3 dev_scripts/censo_dex.py`

| região | antes | depois |
|---|---|---|
| **Galar** | **0** | **592** |
| Kanto | 290 | 295 |
| Johto | 305 | 307 |
| Hoenn | 297 | 301 |
| Sinnoh | 267 | 267 |
| Unova | 315 | 315 |
| Frontier | 8 | 10 |

As outras regiões subiram porque o censo estava errado, não porque ganharam conteúdo: ele
jogava em região "?" tudo que não mora em `data/maps/<pasta>/`, escolhia uma fonte em vez de
unir, e não contava Unown.

Os encontros importados da ROM do demake, medidos no JSON de hoje: **96 mapas `MAP_GALAR_*`,
161 tabelas, 1.602 slots** `[V]`. O relatório do lote E fala em "104 tabelas", que é a conta
do lado da FONTE (107 mapas do demake com tabela, 104 depois do filtro); do nosso lado o
resultado pousa em 96 mapas. Quem for mexer nisso mede o nosso número, não o da fonte.

### As decisões de desenho desta onda, e quem as tomou

Sete, todas da condutora, e todas registradas aqui porque mudam o que a próxima rodada pode
fazer sem perguntar.

1. **As 16 sobras de FireRed dentro dos grupos de Galar** (Lost Cave, Tanoby Key, câmaras
   Liptoo e Scufib) ficam CARIMBADAS, não ligadas e não apagadas: `cortado_por:
   sobra_firered_no_grupo_galar` no `map.json`. O carimbo tira o mapa da régua de
   conectividade e não esvazia nada: id, warps e objetos continuam onde estão, e nenhum
   índice anda, o que é o que mantém a save intacta. Isso responde à pendência aberta na
   seção 5.
2. **As 18 duplicatas do demake** (blockdata cópia byte a byte de mapa vivo) recebem
   `reserva_duplicada_do_demake`, pelo mesmo mecanismo e pelo mesmo motivo.
3. **A T07 do `checa_texto.py` inverteu para Galar**, e a T08 deixou de medir Galar. Era a
   pendência número um da seção 3.5: sem isso a frente entregaria vermelho por acertar. Hoje
   a régua de Galar reprova PORTUGUÊS, e a de Sinnoh e Unova continua reprovando inglês.
4. **A tradução entra por DE-PARA com rótulo e aplicador idempotente**, nunca por busca de
   texto solto. O julgamento inteiro mora no JSON e no `GLOSSARIO-GALAR.md`; o script é só a
   mão que escreve. O motivo é medido: 38 blocos de Galar são literalmente `...`, 19 são
   "Boa batalha. Obrigado!" e 30 são a mesma fala de vendedor, então busca por texto trocaria
   o bloco errado sem avisar.
5. **As 12 paradas de cura de Galar entram no seletor de capítulo** (`src/chapter_jump.c`,
   struct nova `ParadaDoHack`).
6. **As 10 linhas de `script_objeto` cujo item da fonte está fora da tabela do FireRed** (0 a
   374) passam de `adiada` para `descartada`, motivo "item da fonte fora da tabela do
   FireRed; NPC mudo fica". Elas são `g01m109/objeto/13`, `g05m12/objeto/46`,
   `g06m17/objeto/7`, `g06m28/objeto/10`, `g06m32/objeto/5`, `g07m18/objeto/0`,
   `g08m06/objeto/1`, `g08m23/objeto/8`, `g10m21/objeto/0` e `g42m14/objeto/2`. A decisão foi
   escrita na `fila_galar.json` e SOBREVIVEU à regeneração `[V]`, que é o mecanismo da fila
   (`decisoes_anteriores`), e não edição à mão que a próxima varredura apaga.
7. **Os encontros selvagens ficam os do DEMAKE** (opção A). Sobrepor o datamine canônico de
   Sword e Shield é pergunta ao Gui, e está no fim desta seção.

### As premissas do PRD que esta onda DERRUBOU

São cinco, e cada uma custaria uma rodada inteira a quem confiasse nelas.

1. **A fonte NÃO tem a porta de entrada dos órfãos.** O PRD tratava os 246 como obra de
   warp. O andador mediu: **95 dos 141 que sobram só abrem por SCRIPT** (o demake usa
   `warp` dentro de bytecode, não `warp_event` no header), e **46 não têm entrada nenhuma**,
   dos quais 42 sobram depois do teste de blockdata. Ligar esses 42 é DESENHO DE CONTEÚDO,
   não extração: não há porta para copiar.
2. **`valida_mapa.py` não existe.** O PRD cita a ferramenta pelo nome. Os validadores que
   existem são `valida_conectividade.py`, `valida_warp_tile.py`, `valida_mapas_sinnoh.py` e
   `valida_rom.py` (ver `ESTADO.md` seção 7).
3. **O texto de Galar NÃO mora em `data/maps/Galar_*/scripts.inc`.** Os 438 `scripts.inc`
   daquela região têm ZERO `.string`. Os 1.124 blocos de fala moram em
   `data/scripts/galar_fala.inc`, `galar_treinadores.inc`, `galar_objetos.inc`,
   `galar_placas.inc`, `galar_cenas.inc` e agora `galar_placas_c.inc`. Quem planejar
   tradução por mapa planeja no lugar errado.
4. **`lente_warps.py` e a checagem C28 vivem só no working tree sujo da `master`**, não nesta
   branch. Elas entram no primeiro `git merge master` depois que a rodada 13 do cartucho 1
   commitar. Até lá, medir C28 aqui exige copiar o `checa_scripts.py` de lá, e foi o que esta
   rodada fez.
5. **Placa e script na `completude.py` só andam com `map.json`.** Escrever o `.inc` põe o
   texto na ROM e não põe a placa no jogo. Foi por isso que o lote C deixou os 4 `bg_event`
   como pedido em `dev_scripts/onda1_lote_c_pedidos_mapjson.txt` em vez de escrever no
   `map.json` de outro dono, e foi o fechador que os aplicou.

### A fila da ONDA 2, com número

Em ordem de tamanho, e cada item já tem a lista no disco.

1. **95 portas de script a transcrever** (`dev_scripts/orfaos_galar_por_script.json`), e as
   **40 que partem de mapa vivo vêm primeiro**: elas são as únicas que o jogador alcança hoje.
2. **Os 42 sem saída nenhuma** (`dev_scripts/orfaos_galar_sem_saida.txt`) aguardam decisão do
   Gui: ligar por desenho nosso, carimbar `cortado_por` ou deixar como estão.
3. **226 `porta_morta`**, todas bloqueadas por destino que é mapa vanilla do FireRed que o
   demake não redesenhou. Elas não são obra de texto, são obra de MAPA, e não saem da fila
   sem decisão de escopo.
4. **A coluna `script` da completude, em 59,2%**: 746 de 1.260 NPCs têm fala. Andar aqui é
   voltar ao balde `script_objeto`, e os 198 `adiada` que sobraram são o primeiro lugar para
   olhar.
5. **`dev_scripts/onda1_lote_e_pedidos_scripts.txt`**: os 31 pokémon de geração 8 que hoje só
   existem nas regiões que saem do cartucho 2, e o apêndice com as **140 entradas de geração
   8 sem fonte em Galar** (de 197 no total, 95 bases e 102 formas; 57 já têm fonte).
6. **A curva de nível de Galar está fora do lugar, e é defeito visível.** Os encontros
   selvagens importados vão de **nível 2 a 60**, e os treinadores de Galar estão em **255**.
   Um dos dois números está errado e ninguém mediu qual ainda. `curva_selvagem.py` e
   `curva_de_nivel.py` são as ferramentas.
7. **As 4 placas novas do lote C entraram; as 21 `adiada` não.** Elas ficaram bloqueadas por
   coordenada que já tem `bg_event` ou por tile que não é parede.

### Perguntas ao Gui

1. **Datamine canônico de encontros.** Os 1.602 slots de Galar são os do DEMAKE, que é uma
   obra de fã sobre FireRed. Existe datamine canônico de Sword e Shield em
   `fontes-mapas/galar-swsh/`. Sobrepor os encontros pelo canônico muda o jogo inteiro de
   Galar (espécie, nível e raridade) e é decisão de escopo, não de execução. **Recomendação:
   ficar com o demake**, porque ele é coerente com os mapas 2D que ele mesmo desenhou, e o
   canônico traria espécie que não cabe no mapa dele.
2. **Os 42 mapas sem saída nenhuma.** A fonte não tem porta para eles. Ligar é inventar
   caminho. **Recomendação: carimbar `cortado_por`** e tirá-los da régua, como as 16 sobras
   de FireRed, deixando id e conteúdo onde estão.
3. ~~**Os dois casos de suíte que ficaram vermelhos por medirem o desenho velho** (T108.8 e
   T159.13)~~ **RESOLVIDO em 06/09/2026**: a condutora aprovou os dois consertos, eles foram
   aplicados no commit `2b7f2c0903` e os dois blocos voltaram a ficar verdes. O detalhe está
   no portão abaixo. Este item fica escrito porque a recomendação original explica por que
   mexer em caso de teste foi legítimo aqui: eles eram falso positivo, e falso positivo é
   pior do que não ter régua, porque ensina a ignorar a saída.

### O portão desta onda

`[V] export DEVKITARM=...; make -j8 > /tmp/build-cartucho2.log 2>&1; echo $?`

| medida | antes (base da branch) | depois |
|---|---|---|
| exit code do `make` | 0 | **0** |
| ROM ocupada | 32.360.228 B, 96,44% | **32.376.452 B, 96,49%** (+16.224 B) |
| EWRAM | 225.856 B, 86,16% | **225.856 B, 86,16%** |
| IWRAM | 28.404 B, 86,68% | **28.404 B, 86,68%** |
| md5 da ROM | `99b141df69aaa917bd7611e3c1f69298` | **`ea0c2858daf02807ad379a9be20502c5`** |

`src/chapter_jump.c` compilou de primeira: o lote AB2 escreveu a struct `ParadaDoHack` sem
buildar, e não precisou de conserto nenhum `[V]`.

`[V] python3 dev_scripts/guarda_save.py` -> **SAVE COMPATIVEL**. SaveBlock1 em 14.964 B de
15.872 (94,3%), 2.400 mapas, 2.252 ids de treinador e **1.718** apelidos conferidos (eram
1.716: as duas vars de cena do lote C entraram por apelido novo, que é acréscimo e não
mudança de índice).

`[V] T11 3/3`, contra `/private/tmp/claude-501/c2-t11-antiga` (md5
`ac8ed5419ab69cacece45ad6479e6063`), rodado FORA do lock sobre cópia da ROM.

O lock de build foi tomado com `mkdir`, devolvido com `rmdir` logo depois do `make`, e o T11
e a suíte rodaram fora dele.

`python3 dev_scripts/testa_critico.py --rom <cópia da ROM>` -> **1.002 de 1.003**, com o
T11.3 pulado como sempre (ele só prova algo com duas ROMs). A varredura inteira mediu
**1.000 de 1.003** antes do commit `2b7f2c0903`, e os dois vermelhos eram FALSO POSITIVO:
T108.8 e T159.13 mediam desenho que ESTA ONDA trocou de propósito. Os dois foram
recalibrados nesse commit, e os blocos inteiros foram REFEITOS depois dele, sobre cópia da
mesma ROM `ea0c2858daf02807ad379a9be20502c5`: `[V] T108 10 de 10` e `[V] T159 14 de 14`.
O 1.002 é, portanto, os 1.000 medidos na varredura completa mais estes dois casos medidos
verdes à parte, e não uma segunda varredura de mil casos.

**Armadilha medida de passagem, para a próxima rodada não caçar defeito onde não há:** o
**T108.2 é intermitente**. Na primeira passada do bloco ele reprovou com "jogador NÃO andou:
posição ficou em (32,50)", e em seguida passou **5 de 5** rodado sozinho e o bloco inteiro
deu 10 de 10 `[V]`. É a mesma causa que o próprio nome do caso registra desde 22/08: o NPC
`MOVEMENT_TYPE_WANDER_AROUND` de (33,52) fica no gargalo, e o emulador não é determinístico
entre execuções. Vermelho isolado nesse caso pede repetição antes de virar diagnóstico.

**T108.8** (`dev_scripts/testes_criticos/108_galar_qa.json`). Ele afirma, no nome, que "a
lista de capítulos de Galar tem UMA linha só" e que doze DOWN saturam em "Start of region".
A decisão 5 desta onda pôs as onze paradas de Galar nessa lista, então doze DOWN agora caem
na décima segunda linha, CROWN TUNDRA. Esperado `MAP_GALAR_WEDGEHURST_03`, obtido
`MAP_GALAR_CROWN_TUNDRA_06`. `[V] caso de diagnóstico com a MESMA rota e a prova trocada
para MAP_GALAR_CROWN_TUNDRA_06: passou`. O par T108.7 (cinco DOWN, um A, primeira linha) e o
par T108.9 (os mesmos doze DOWN em Unova) continuam verdes, ou seja o menu não quebrou: ele
ficou maior. **Conserto APLICADO em `2b7f2c0903`:** a prova passou a cobrar
`MAP_GALAR_CROWN_TUNDRA_06` e o nome do caso passou a dizer o que ele prova hoje, que é o
seletor de Galar oferecer as paradas de cura e chegar à Crown Tundra. A rota não mudou, e
T108.7 e T108.9 ficaram como estavam.

**T159.13** (`dev_scripts/testes_criticos/159_fechador_r9.json`). Ele joga a cena de
`Galar_Hammerlocke05` inteira com **45 toques de A** calibrados no texto em PORTUGUÊS, sai,
volta e sobe. A tradução manteve as PÁGINAS (`\p` igual: 1, 7 e 3), mas a requebra por pixel
acrescentou **dois `\l`** nos blocos `GalarCena_G09M11_t2_v0_Text1` e `_Text2`, e `\l`
também custa um toque. Com 45 A a cena não fecha, `VAR_GALAR_G09M11_CENA` não vai a 1, a cena
roda de novo na reentrada e come os dez UP: esperado `(11,12)`, obtido `(10,10)`. `[V] caso
de diagnóstico com a MESMA rota mais dez A: passou, com mapa, posição, var e flag exatamente
como o caso original pede`. **Conserto APLICADO em `2b7f2c0903`: dez A a mais na rota**, que
subiu de quarenta e cinco para cinquenta e cinco (dois é o mínimo teórico e não foi medido;
dez foi). A suíte não tem como calibrar toque pelo texto: o `roteiro` é string cravada e o
`testa_critico.py` só a repassa ao `gba_runner`, então calibrar por texto seria motor novo, e
não o conserto pequeno que esta decisão autorizava `[V]`. A folga é inerte, porque A que
sobra depois do fim da cena cai no vazio: o jogador termina parado longe de qualquer NPC.

**Os dois consertos são de RÉGUA, e o fechador não os aplicou de propósito**: editar caso de
teste para deixar a suíte verde é o movimento que mais merece desconfiança, e ele não se faz
sozinho na mesma sessão que criou a mudança. Foram aprovados pela condutora e aplicados por
uma sessão de portão à parte, que rodou os dois blocos INTEIROS, e não só os dois subcasos.

`[V] bash dev_scripts/antes_de_empurrar.sh` sobre o HEAD, em worktree isolada: **oito passos
verdes de nove**. Build do HEAD limpo ok, guarda de save ok, o declarado entrou na ROM ok,
grupo abaixo do teto ok, conectividade ok, sprites e objetos ok, warp em tile que dispara ok,
treinador sem time ok. O que falha é o **`testa_percurso.py`, percurso "fala com tudo em
volta"**, com "NAO RESPONDE: apertar START no fim do percurso nao mudou nada na tela".

**Esse vermelho NÃO é desta onda, e isso foi MEDIDO, não suposto.** A base da branch
(`8a9ebcb692`) foi buildada em worktree separada, deu a ROM md5
`99b141df69aaa917bd7611e3c1f69298`, que é byte a byte a que a seção 4 registrou na abertura,
e o `testa_percurso.py` falha **exatamente no mesmo percurso, com a mesma mensagem** `[V]`. O
portão desta branch já nascia com esse passo vermelho, e nenhuma linha desta onda encosta na
região onde ele roda (ele começa em jogo novo, e a onda inteira é Galar). Fica registrado
aqui porque uma frase de portão sem essa medição faria a próxima rodada caçar o defeito
dentro do diff errado.

**PUSH LIBERADO em 06/09/2026**, depois de a suíte voltar aos 1.002 de 1.003 com a
recalibração dos dois casos. O que barrava o push era o vermelho de régua velha, e ele saiu.
A varredura de blob antes de empurrar não achou nada: nenhum objeto de `.gba` e nenhum acima
de 5 MB entre `origin/cartucho-2..HEAD` `[V]`. Quem retomar confirma onde o `origin` está
com o `git ls-remote --heads origin cartucho-2` da seção 0, que é o primeiro comando de toda
rodada, e não com o `HEAD` local.

### Os commits desta onda

| # | hash | lote |
|---|---|---|
| 1 | `b3b51bb191` | MAPSEC e o CSV |
| 2 | `9f8eb9c9a4` | órfãos: carimbos, warp, andador, listas e `chapter_jump.c` |
| 3 | `bc61b44577` | fila de Galar: placas, cenas, C28, vars, geradores e os 4 `bg_event` |
| 4 | `2f16420f7c` | tradução: régua, glossário, de-para, aplicador e os `.inc` |
| 5 | `af605f13a9` | Dex e encontros |
| 6 | `e11895dd63` | o diário desta onda |
| 7 | `2b7f2c0903` | recalibração de T108.8 e T159.13, no portão |

Os `map.json` e os `.inc` que dois lotes tocaram foram PARTIDOS entre os commits, e não
empilhados no último: os 140 do MAPSEC entram no commit 1 com o campo trocado sobre o
conteúdo do `8a9ebcb692`, e `galar_cenas.inc` e `galar_treinadores.inc` entram no commit 3 na
versão do lote C, ANTES da tradução, reconstruída bloco a bloco. A reconstrução foi provada:
rodar o aplicador em cima dela devolve a árvore de hoje byte a byte, nos cinco arquivos
`[V]`.

### O que ficou de fora, e por quê

- **A coluna `script` não andou** (59,2%), porque `script_objeto` não era escopo desta onda.
- **Os 226 `porta_morta`** continuam inteiros: são obra de mapa, não de conteúdo.
- **Os 6 C28 de Unova** continuam de pé. Unova não é escopo da Frente A.
- **A tela de créditos dentro do jogo** continua sendo pendência da fase de montagem.
- **A ROM desta onda foi copiada para o Gui** em
  `Claude Workspace - Pokemon Rom Hacks/roms/pokemon-claude-cartucho-2-2026-09-06.gba`, com o
  `.md5` ao lado, fora do repo. Ela é a ROM que os portões desta seção mediram.
- **O push saiu em 06/09/2026**, depois da recalibração dos dois casos de régua velha. Quem
  retomar começa pelo `git ls-remote --heads origin cartucho-2` da seção 0, que é a única
  coisa que diz onde o `origin` está de verdade.

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

**RESOLVIDO NA ONDA 1, e os números acima são de ANTES dela.** O que está escrito nesta
seção é a medição de abertura da branch; a régua e o texto mudaram os dois no mesmo dia, e o
placar de hoje está na seção "Onda 1" no topo deste arquivo.

O problema era este: `checa_texto.py` reprovava T07 quando a região era `Sinnoh`, `Unova` ou
`Galar` e o texto estava em inglês, ou seja o QA acusava 28 achados em Galar por estarem em
inglês e traduzir os 310 blocos de português levaria esse número a 338. A frente entregaria
vermelho por acertar.

**A régua inverteu para Galar na onda 1** (decisão 3 daquela seção): lá o defeito é o
PORTUGUÊS, e a T08, que mede acento, deixou de olhar Galar por completo. Sinnoh e Unova
continuam como estavam, reprovando inglês. Com a régua nova, Galar saiu de **310 achados
T07 para 1**, e o 1 é `GalarFala_G09M10_o14_Text`, defeito de charmap deixado à vista.

Quem for mexer em texto de Galar daqui em diante escreve INGLÊS, pela decisão 32 do Gui no
`PRD-CARTUCHO-2.md`, usando o `GLOSSARIO-GALAR.md` para não gerar duas grafias do mesmo
item, golpe, classe de treinador ou nome de cidade.

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

**Esta seção é da ABERTURA da branch, 06/09/2026, e a onda 1 aconteceu depois dela.** Três
pendências listadas mais abaixo já foram fechadas: a régua de T07 inverteu, as 12 travas de
C28 em Galar sumiram e os 16 mapas de sobra de FireRed foram carimbados. A proposta de onda
1 no fim desta seção foi executada com cinco lotes, e não quatro. O estado de hoje está na
seção "Onda 1" no topo deste arquivo.

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
