# Plano da onda de janela aberta (autorizada pelo Gui em 18/08/2026)

Desenhado pela condutora em 18/08/2026. O Gui autorizou quebrar a save
atual ("pode quebrar meu save sim, pq temos o teleport de areas e
ginasios"): o Chapter Jump repõe o progresso em minutos, então esta onda
pode mexer no que a janela fechada proibia. A janela abre UMA vez, faz
tudo que estava esperando, e FECHA de novo no fim, com ROM oficial nova
como baseline.

## Leis desta onda (substituem as da janela fechada, SÓ nesta onda)

- `guarda_save.py` continua rodando, mas SAVE INCOMPATIVEL causado pelo
  que está NESTE plano é esperado; incompatibilidade fora do plano
  continua sendo reprovação.
- No fim da onda: `guarda_save.py --gravar` regrava a impressão, o
  baseline do T11 passa a ser a ROM oficial nova (a save da 2026-08-15c
  DEIXA de carregar, e isso está aceito por escrito), e a janela FECHA.
- Conserto de gerado continua morando no gerador. Suíte continua
  mandando. Português com acento, nunca em dash.
- O que NÃO está neste plano não entra: janela aberta não é licença
  para renumerar por estética. Endereço que funciona fica quieto.

## Decisões da condutora

1. **Ordem**: esta onda só roda DEPOIS do fechamento da Fase E (fechador
   combinado + commits + ESTADO 0.f). Uma obra de cada vez na árvore.
2. **Pool de flags CRESCE** o suficiente para os itens 3 e 4 mais folga
   de conteúdo (Galar, Wild Area, cenas). O executor mede o espaço livre
   real do SaveBlock1 (referência de 18/08: 14388 B de 15872, ~1484 B
   livres) e propõe o novo FLAGS_COUNT com a conta explícita; teto duro:
   o SaveBlock1 não passa de 97% do setor. Vars idem, se o item 5 pedir.
3. **As 1362 item balls de Johto/Sinnoh/Unova entram 1:1**: uma flag
   nova por item ball, faixa contígua nova no pool crescido, com dono
   anotado em flags.h e censo gerado por região. O desenho 1:1 que a
   janela fechada proibia (comia o pool de 1519) agora é o desenho
   certo, porque é o do jogo original.
4. **Heal locations das 7 cidades de Sinnoh sem respawn**: entram, e o
   Chapter Jump de Sinnoh passa a usar CURA(...) nelas como as demais
   regiões já fazem.
5. **As 3 vars de cena de Kanto que colidem com Hoenn**
   (VAR_MAP_SCENE_ROUTE22 = VAR_CURRENT_SECRET_BASE etc., vars_frlg.h
   sem guarda): saem da colisão, movidas para endereços novos ou
   comprovadamente livres; vars_frlg.h ganha a guarda que falta (static
   assert ou tabela conferida por gerador) para colisão nova nunca mais
   entrar calada.
6. **Modo de teste**: os bits em filler_90 podem virar campo nomeado de
   verdade no SaveBlock2 (o bitfield que o guarda barrava). Só se o
   custo for trivial; é limpeza, não requisito.
7. **O que fica FORA**: realias existentes que funcionam (Kanto 0x500+,
   Sinnoh 0x1B00+, Galar 0x1C00+ ficam como estão); item balls de cenas
   ainda não portadas (a flag nasce, a cena vem na fase de conteúdo);
   qualquer corte por espaço (portão da condutora com o Gui, como
   sempre).
8. **Fecho da onda**: build + suíte completa + T11 3/3 contra a ROM
   NOVA (o caso ganha o baseline novo), ROM oficial
   `pokemon-claude-2026-08-XX.gba`, ROM de teste com o nome fixo de
   sempre, ESTADO ganha seção datada, e a memória da sessão registra a
   janela FECHADA de novo.

## Bloco executável (um executor, ciclo padrão)

- J1: medição e crescimento do pool (decisão 2), com prova de que jogo
  novo nasce são e o guarda regravado acusa exatamente o esperado.
  **FEITO em 18/08**: FLAGS_COUNT de 8248 para 12856 (+576 B, SaveBlock1
  em 94,3%, folga de 431 B até o teto de 97%), faixa das item balls
  0x2031-0x2630 (1536 vagas) e reserva de conteúdo 0x2631-0x3230 (3072).
  Vars NÃO cresceram, e a conta está no relatório: os endereços do J4 já
  cabiam. Decisão 6 (filler_90) PULADA de propósito: nomear o campo faz o
  guarda acusar quebra falsa por hash de texto, e a lei desta onda proíbe
  mexer por estética.
- J2: item balls 1:1 (decisão 3), gerador por região, suíte por amostra
  (pegar item, flag liga, item não volta; par negativo com a bola
  vizinha, que é a prova de que a flag deixou de ser compartilhada).
- **J3: CANCELADO em 18/08**, já estava feito. O commit `a5dc22e600`
  (Fase C do PRD) deu heal location própria às 7 cidades de ginásio de
  Sinnoh e à Liga sul, em append, e o Chapter Jump já usa os pontos de
  cura de verdade. O plano foi escrito depois disso sem notar.
- J4: **reduzido em 18/08 à guarda de colisão** (decisão 5). O realias
  das 3 vars de cena de Kanto para 0x40F7-0x40F9 também caiu no
  `a5dc22e600`. O que não existe, e é a entrega, é o portão que reprove
  colisão NOVA: valor resolvido pelo pré-processador (não texto), lista
  de realias autorizados para não virar falso positivo, e autoteste com
  mutação plantada.
- **J6, ACRESCENTADO em 18/08 pelo achado do J4**: o portão de colisão
  mediu 38 endereços de var com dois donos usados, e **19 são a doença
  viva** (cena de FRLG contra estado de Hoenn, as duas em `data/maps/`;
  medido: o `setvar` da Pallet Town grava no estado de Littleroot). As
  19 entram nesta onda, no molde do `a5dc22e600`, porque mover endereço
  é exatamente o que a janela aberta autoriza. As outras 19 (0x4025 a
  0x404b, utilitárias de FRLG do lado do motor) ficam declaradas como
  dívida, com motivo. Depois do J2 fechar, o mesmo portão passa a valer
  para `flags.h` (custo medido: trocar duas constantes; ele já achou 3
  grupos lá).
- **J7, ACRESCENTADO em 18/08 (sobras do J1, J2 e J4). FEITO no mesmo
  dia**, três entregas, nenhuma delas tocando código compilado além de
  comentário e declaração:
  1. **Portão de colisão estendido para flags**, `python3
     dev_scripts/guarda_colisao_vars.py --flags` (o arquivo manteve o
     nome; o que mudou é que endereço, prefixo e lista vêm de um PERFIL).
     Duas coisas tiveram que ser diferentes de vars, e as duas são
     medição: a ordem dos headers segue a ordem do include, senão o
     portão grava o corpo de um e o valor do outro (foi o falso positivo
     de 0x20, `FLAG_HIDE_ARTICUNO`), e a regra de apelido é a ESTREITA,
     só a forma exata `#define FLAG_X FLAG_UNUSED_0xNNN`, senão faixa
     gerada com base mais deslocamento ficaria invisível. Acha **3
     grupos**, o mesmo número que o J4 tinha estimado, em
     `dev_scripts/colisoes_flags_autorizadas.json` com dono e motivo por
     linha. **Um deles é desenho** (0x1F4, marcador de faixa) e **dois
     são DEFEITO VIVO** (0x4000 e 0x4001, ver relatório e a fila);
     medidos e NÃO consertados, porque conserto de endereço é decisão do
     condutor.
  2. **Sobra da faixa de item ball redeclarada**: o J1 reservou 1536
     vagas por estimativa, o J2 mediu 160 de demanda real, e as 1376 que
     sobraram (0x20D1-0x2630) passaram a ser reserva de conteúdo em
     `FLAG_SOBRA_ITEM_BALLS_START`, declaradas uma a uma para o
     `flags_livres.py` enxergar (ele passou a ver 0x20D1-0x3230 como uma
     faixa livre contígua de 4448). Custo zero de save: `FLAGS_COUNT`
     continua 0x3238 e nenhum endereço deslizou. O gerador do J2 ganhou
     teto lido do flags.h, para bola nova nunca invadir a sobra.
  3. **Dívidas do J2 registradas na fila** (`dev_scripts/fila_b6.py`,
     `FILA_DE_CONTEUDO`): os 1211 objetos de Johto com sprite de item
     ball sem serem item ball, as 2 bolas genuínas ausentes de Olivine e
     a GS Ball das Ruínas de Alph, mais o defeito de flag do item 1.
- **J8, ACRESCENTADO em 18/08 pelo achado do J7 (item 1). FEITO no mesmo
  dia.** O stub do import de Johto em `include/constants/flags.h`
  (`#ifndef FLAG_NIGHT_POKEMON / #define FLAG_NIGHT_POKEMON 0x4000`, e
  irmãos) morreu. `FLAG_NIGHT_POKEMON` foi para `FLAG_UNUSED_0x1D01` e
  `FLAG_DAY_POKEMON` para `FLAG_UNUSED_0x1D02`, no **transbordo de
  Johto** e não na reserva do J1: as duas escondem object event de
  Johto, igual à `FLAG_HIDE_LAKE_OF_RAGE_GYARADOS` que já mora em
  0x1D00, e a reserva do J1 nasceu dimensionada para Galar e Wild Area.
  Apelidar `FLAG_UNUSED` que já existe **não mexe em `FLAGS_COUNT`**: o
  `guarda_save.py` continua acusando as DUAS quebras do J1 e nada mais.
  `FLAG_HIDE_RAYQUAZA 0x4002` foi **apagada** (zero uso medido em
  `data/`, `src/`, `include/` e `test/`): símbolo que não existe quebra o
  build alto, símbolo com endereço inventado quebra o jogo calado. Para a
  classe não voltar, o portão passou a **reprovar `#ifndef FLAG_`/`#ifndef
  VAR_`** nos headers do perfil, com mutação plantada no `--demo`. Os 3
  usos em `map.json` não mudaram, porque citam o NOME. Prova: caso 111,
  6 casos, com **par negativo** acendendo `FLAG_HIDE_MAP_NAME_POPUP` e
  `FLAG_DONT_TRANSITION_MUSIC` (os dois endereços que o stub roubava) e
  exigindo que o Pokémon CONTINUE no mapa.
- **J9, ACRESCENTADO em 18/08/2026 pelo adversarial da onda. FEITO no
  mesmo dia.** Seis entregas:
  1. **A save velha passou a ser RECUSADA, e não lida errada.** O
     adversarial mediu que a save da `pokemon-claude-2026-08-18b.gba`
     carregava em SILÊNCIO nesta build: o setor é zerado antes de gravar,
     o checksum soma palavras de 32 bits, os 576 B a mais lidos são zeros,
     o checksum bate e `GetSaveValidStatus` devolvia `SAVE_STATUS_OK` para
     uma save que o jogo lia DESLOCADA (as 512 vars 288 posições fora do
     lugar, Pokédex, correio, bases secretas e creche embaralhadas, esta
     com risco de espécie inválida). Conserto MÍNIMO em `include/save.h`:
     `SAVE_LAYOUT_REVISION 1` somada a `SECTOR_SIGNATURE`. Nenhum setor da
     save velha casa a assinatura, os dois slots viram vazios, e o menu
     principal abre em **NEW GAME / OPTION**, sem caixa de erro e sem
     travar. MEDIDO no harness, com print: a mesma save mostra
     `CONTINUE / PLAYER / TIME / BADGES` na ROM de 15/08 e só
     `NEW GAME / OPTION` na de hoje. O `guarda_save.py` era CEGO para essa
     macro (ele nunca leu `save.h`) e passou a guardá-la.
  2. **Buraco H do portão de colisão tapado**, e ele era o grave:
     `#define VAR_MINHA VAR_UNUSED_0x41C3` era descartado como "apelido
     declarado", e apelidar `*_UNUSED_*` é exatamente como Johto, Sinnoh,
     Unova e Galar ALOCAM. A regra virou "todo `#define` é dono; o único
     que deixa de ser é o rótulo do pool que um apelido tomou, e só quando
     o cpp confirma o valor". Vars foram de 19 para 23 grupos e flags de 1
     para 5; os 8 novos são apelidos de rascunho do pokeemerald de fábrica
     (`FLAG_TEMP_*`, `VAR_TEMP_*`), declarados com motivo.
  3. **`maquina_sinnoh.py` mandava alocar var em "0x41C3+"**, que é onde o
     J6 acabou de morar. Consertado NO GERADOR, e sem trocar um número por
     outro: agora ele manda MEDIR (mapa de donos de `vars.h` mais o
     portão). O irmão do bloco de flags ("cabeça livre até 0x2025", morto
     pelo J1) recebeu o mesmo tratamento.
  4. **Quatro buracos de regex tapados**, cada um com mutação plantada no
     `--demo` (que foi de 7 para 13 checagens por perfil): apelido para
     nome VIVO, apelido de apelido, `#ifndef` com comentário na mesma
     linha, `#if !defined(...)`, e `#define` em dois ramos com o cpp
     entregando um número e o leitor guardando o corpo do ramo morto.
  5. **Censo do J2 corrigido**: são CINCO números repetidos, não quatro. O
     quinto é `0x3C` (`FLAG_GALACTICA_QG_CHAVE`), dividido entre a item
     ball do QG e dois NPCs guardas, e é DESENHO escrito em
     `GalacticHQ_2F/scripts.inc:5`. O que ficou registrado é o MÉTODO:
     bola contra bola é cega para bola contra NPC, porque o `removeobject`
     apaga todo objeto com aquele número de flag.
  6. **Sobras na fila** (`fila_b6.py`): flag e var em `include/config/*.h`
     fora do alcance do portão (as duas em 0 hoje, zero colisão),
     `FLAG_FRONTIER_MON_FACTORY` sendo máscara de bit com nome de flag, e
     as duas worktrees velhas que ainda têm o stub de `FLAG_HIDE_RAYQUAZA`
     (aviso, não tarefa: worktree é foto de commit passado).
- J5: fecho (decisão 8), com adversarial antes do fechador porque J1,
  J2, J4 e J6 mexem em terreno de save.
