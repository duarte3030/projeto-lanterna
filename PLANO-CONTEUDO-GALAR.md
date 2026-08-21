# RASCUNHO da fase de conteúdo de Galar (não é decisão)

**Isto é um rascunho de executor para a condutora julgar.** Nada aqui foi
aprovado, nenhum bloco está autorizado, e os números de vars/flags são
orçamento proposto, não reserva feita. Escrito em 21/08/2026, depois da onda 1
(baldes a e b), a partir de medição no bytecode da fonte, nunca de estimativa.

Fonte: demake fan-made Ultimate Plus v1.2.1.2 em `fontes-mapas/galar-swsh/`
(fora do repo, sem remote). Ferramenta que mede: `dev_scripts/fala_galar.py`,
que parseia a tabela de opcodes de `fontes-mapas/pokefirered/asm/macros/event.inc`
em vez de carregar tabela digitada, e grava `dev_scripts/galar_roteiros.json`.

## Os quatro baldes, medidos (`python3 dev_scripts/fala_galar.py`)

| balde | total | script_objeto | placa | map_script | porta_morta |
|---|---|---|---|---|---|
| a_fala (zero estado novo) | 466 | 414 | 52 | 0 | 0 |
| b_flag | 93 | 93 | 0 | 0 | 0 |
| c_var_cena | 2.311 | 1.821 | 70 | 194 | 226 |
| d_treinador | 325 | 313 | 12 | 0 | 0 |
| **TOTAL** | **3.195** | | | | |

A fila tinha 3.257 linhas e passou a 3.195: **62 map_scripts cobravam cena de
uma tabela VAZIA na fonte** e saíram pelo gerador (`fila_galar.py`, c2 feito).
Da onda 1 estão **feitas 445** (337 falas, 52 placas, 56 bolas) e
**descartadas 104** (os NPCs que a fonte manda falar e o G4 não pôs no mapa;
decisão da condutora de 21/08, motivo gravado na linha).

Motivos de c: 1.385 comando de estado, 390 decodificação incompleta, 226 porta
morta, 194 tabela de map script, 92 sem texto, 22 com mais de um texto, 7 com
marcador de buffer, 4 item vindo de var.

## Orçamento, com o número real

**Flags: sobram 5.711** (`flags_livres.py`), 4.447 numa faixa contígua. Flag
não é gargalo de nada nesta fase, em nenhum cenário. A onda 1 gastou 56.

**Vars: sobram 150, e a estimativa da fase é 200 a 260. DÉFICIT de 50 a 110.**
Medido em 21/08 resolvendo pelo `cpp` todos os `VAR_*` dos headers do perfil
`vars` do `guarda_colisao_vars.py` e cruzando com o índice de uso da árvore:

    endereços 0x4000-0x41FF                                   512
    TEMP_VARS (0x4000-0x400F), não servem para cena            16
    com dono declarado                                        346
      desses, dono referenciado em data/src/include/test      318
      declarado e nunca citado (recuperável, um a um)          28
    SEM dono nenhum, livres de verdade                        150

Faixas livres: 0x417E-0x41BF (66), 0x41D6-0x41FF (42), 0x4107-0x412F (41),
0x4100 (1). Conferido contra a armadilha do uso CRU em `data/src` (a terceira
camada do `flags_livres.py`): os únicos `0x41xx` crus da árvore são 0x417D e
0x4179, que já têm dono, e 0x411C, que é uma tabela de cor em `src/util.c`.

Ou seja: **a fase de conteúdo NÃO cabe em vars sem crescer `VARS_COUNT`**, e
crescer quebra a save. Três saídas, e a escolha é da condutora com o Gui:

1. **Cortar escopo até caber em 150** (mais os 28 recuperáveis = 178). Fecha c1
   e c3 inteiros, deixa c4 pela metade. Não abre janela de save.
2. **Uma var por MAPA em vez de uma por cena**, com o valor codificando a etapa
   (é o que o próprio FireRed faz com `VAR_MAP_SCENE_*`). Cabe folgado, e o
   preço é cena que não pode rodar duas etapas independentes no mesmo mapa.
3. **Abrir janela de save** e crescer `VARS_COUNT`. Não recomendo agora: a
   janela fechou em 18/08 e o ganho não justifica reabrir por uma fase que a
   opção 2 acomoda.

## Blocos propostos, com critério de pronto

- **c1, faixa e portão** (0 linhas da fila; é ferramenta). Declarar
  `VAR_GALAR_*` com dono anotado em `vars.h`, na faixa 0x417E em diante, e
  registrar em `colisoes_vars_autorizadas.json`. Pronto quando
  `guarda_colisao_vars.py` passa e o `--demo` dele reprova uma colisão plantada
  na faixa nova. Custo: 0 vars por enquanto, só reserva.
- **c2, tabela vazia** (62 linhas). **FEITO em 21/08.** Pronto: a fila mede a
  tabela na fonte e o `--demo` reprova se alguma linha de tabela vazia voltar.
- **c3, ON_FRAME_TABLE puro** (144 linhas, o molde repetível). São os mapas
  cujo header só tem `map_script_2 VAR, valor`: cena que dispara ao carregar o
  mapa e termina escrevendo o valor seguinte na mesma var. Pronto quando um
  caso de suíte prova, por par positivo/negativo, que a cena roda UMA vez e não
  volta na segunda entrada. Custo: 144 vars pelo desenho ingênuo, ~30 pela
  opção 2 acima. **Este bloco é o teste da escolha de orçamento**: fazer os 12
  primeiros e medir antes de comprometer a faixa inteira.
- **c4, cena de objeto** (1.385 linhas, o resto). `applymovement`,
  `fadescreen`, `special`, `warp`, `pokemart`, batalha selvagem de overworld.
  Não é um bloco, são vários; só dá para dimensionar depois do c3. Pronto,
  linha a linha, quando o NPC faz na nossa ROM o que faz na fonte.

Nenhum código de c3 ou c4 foi escrito.

## Os 390 indecisos: o que falta ao decodificador

São linhas em que algum ramo do script bate num opcode que o FireRed não tem, e
que por isso caem em c por segurança (emitir fala de script não lido inteiro
seria inventar). Os opcodes que aparecem são 0xD7 a 0xE7 e 0xEE a 0xFF, todos
acima do fim da tabela do FR (0xE2). Duas hipóteses, nenhuma medida ainda:
o demake acrescentou comandos próprios à `gScriptCmdTable`, ou o ponteiro
daquele objeto aponta para dado e o script nunca roda. **Medir a
`gScriptCmdTable` da ROM do demake e comparar o tamanho dela com a do FR
resolve as duas de uma vez**, e é barato: se a tabela cresceu, os comandos
novos existem e dá para dimensioná-los pelo ponteiro de cada entrada.

## (d) treinadores: medição, com o aviso na frente

**AVISO, e ele vale mais que os números abaixo: o struct de party do demake não
é o do FireRed.** Lendo `gTrainers` em 0x23EAC8 com o molde do FR (40 B por
entrada, party de 6/8/14/16 B por `partyFlags`), só **165 dos 741 times passam
na validação** de espécie e nível plausíveis. Os 576 reprovados não são
treinadores vazios, são o molde errado. Quem executar mede o stride antes de
acreditar em qualquer número daqui.

Do que passou: **278 ids de treinador citados pelos scripts de Galar** (faixa 1
a 741), 774 Pokémon, nível mínimo 18, **mediana 70**, e **276 deles exatamente
no nível 100**. A curva da fonte é de pós-jogo, não de campanha: importada crua,
Galar inteira nasce em nível 100. Isso entra na mesma decisão do Gui que
congelou a Fase F, e não se executa aqui.
