# PRD GOAL: Pokémon Claude até a ROM completa

Escrito em 18/08/2026 pela condutora Fable, a pedido do Gui, para servir de
objetivo de longo prazo de uma sessão autônoma (comando goal). Este documento
é a CARTA DE OBJETIVOS: diz o que é "pronto", em que ordem e sob que regras.
O ESTADO VIVO nunca mora aqui; mora em `ESTADO.md` (seções 0.x, sempre a mais
nova primeiro), na fila `dev_scripts/fila_b6.json`, no censo
`dev_scripts/maquina_sinnoh.json` e na memória do workspace. Quem executar
este PRD lê o estado vivo ANTES de cada onda e nunca confia em número escrito
aqui como se fosse atual.

## A visão

Um hack de GBA sobre pokeemerald-expansion com SEIS regiões jogáveis de ponta
a ponta (Hoenn, Kanto, Johto, Sinnoh, Unova e, ao fim, Galar), com as 365
espécies de gen 6-9 já integradas, save estável desde a ROM 12b, e uma suíte
de casos de emulador que prova cada pedaço por fato de memória. O jogador de
referência é o Gui, que testa com a ROM de teste (modo de teste no menu de
opções, seletor de capítulo, itens infinitos) e reporta bugs que viram levas.

## Papéis e custo (regra permanente do Gui)

- **Condutor da sessão goal: OPUS.** Segue playbook; commita como o Gui
  (`git -c user.name="Guilherme Duarte" -c user.email="gduarte3030@gmail.com"`),
  sem trailer de IA, português com acento, NUNCA em dash em nada commitável.
- **Executores mecânicos: SONNET** (cenas com molde, censos, casos simples).
  **Julgamento: OPUS** (gerador, consertos de causa, vermelho de suíte,
  autor de casos, fechador).
- **FABLE só para decisão de desenho nova.** Este PRD marca explicitamente os
  portões que EXIGEM desenho de condutora Fable antes de executar. A sessão
  goal PARA nesses portões e avisa o Gui em vez de improvisar desenho.
- Agentes não commitam nem regravam impressão de save; o condutor julga o
  pacote do fechador e commita. Push para `origin` (repo projeto-lanterna).

## O método por onda (não reinventar; provado nas rodadas 1-3 e ondas 1-2)

1. Executores de cena em paralelo com DONO EXCLUSIVO por arquivo
   (`map.json`/`scripts.inc` por arco; `vars.h`/`flags.h`/geradores têm dono
   único por onda; `opponents.h`/`trainers.party` idem).
2. Fila é COBRANÇA, não certeza: executor confere o mapa antes de escrever e
   reporta falso pendente.
3. **Autor de caso ≠ autor de cena.** O autor de casos lê as cenas
   adversarialmente ANTES do fechador (na onda 2 isso achou 7 defeitos
   reais). Prova por fato de memória (EWRAM: var, flag, mapa, oponente),
   nunca pixel. Par negativo obrigatório onde o positivo passaria com o
   mundo quebrado. Caso que depende de sorteio PINA a var.
4. Consertador de causa (Opus) aplica os achados; conserto de arquivo gerado
   mora no GERADOR (regravar idempotente), nunca à mão.
5. Fechador (Opus): build (`export DEVKITARM="$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi"; make -j8`
   via nohup, monitor ESTRITO: "error:" com dois pontos; suíte por
   `^[0-9]+/[0-9]+ passaram`; UMA tarefa de espera bloqueante, nunca
   empilhar vigias), suíte completa, `guarda_save.py` (SAVE COMPATIVEL
   obrigatório), `maquina_sinnoh.py --demo` quando Sinnoh estiver em jogo.
   T11 completo (worktree do commit da ROM de referência +
   `rsync --ignore-existing include/` + `--rom2`) em toda onda que mexa em
   item/flag/var ou antes de cortar ROM nova.
6. Condutor julga, commita a onda, push, e SÓ ENTÃO abre a onda seguinte
   (nunca sobrepor executor de cena com fechador no mesmo working tree).
7. Fechamento de rodada: atualizar `ESTADO.md` (nova seção 0.x), regenerar a
   fila quando a régua permitir, copiar ROM para o workspace
   `~/Documents/CLAUDE/Claude Workspace - Pokemon Rom Hacks/roms/` com
   `.map` ao lado, atualizar a memória do workspace, registrar consumo por
   modelo. A ROM de teste SEMPRE sobrescreve
   `roms/pokemon-claude-teste-2026-08-16.gba` (o Gui casa a save do Delta
   pelo nome); a ROM oficial ganha data nova.

## Decisão do Gui sobre espaço (18/08/2026): 32 MB NÃO é lei de escopo

Caber as 6 regiões num único GBA é DESEJÁVEL, não obrigatório. A ordem de
prioridade é: (1) desenvolver TODOS os assets e conteúdo, sem eliminar nada
vital para caber em 32 MB; (2) recuperar espaço por técnica que não perde
conteúdo (compressão, indireção, deduplicação, o B10 é exatamente isso),
SEM apertar reutilização a ponto de arriscar bug; (3) se no fim não couber,
a saída aceita é SEPARAR EM DOIS GBAs no futuro, decisão de desenho a tomar
quando (e se) o teto apertar de verdade. Consequência prática para qualquer
onda: corte de conteúdo por espaço NÃO é decisão de executor nem de
condutor Opus; é portão Fable + Gui. Otimização agressiva que aumente risco
de regressão precisa de suíte verde e justificativa, e perde para a opção
"deixa para o segundo cartucho".

## Leis invioláveis

- **Janela de save FECHADA**: nada de FLAGS_COUNT/VARS_COUNT/structs; item
  novo só em append no fim + ritual do guarda (leitura de fantasmas zero;
  `--gravar` é ato do condutor depois de suíte verde); objeto/warp novo em
  append; save do Gui congelada é lei (T11 prova).
- **Datamine NUNCA no repo do hack nem em remote público** (`../fontes-mapas/`
  é local; push que morre com "sideband" = procurar blob gigante).
- **Orçamentos são medidos, não presumidos**: flags via `flags_livres.py`
  (que já entende apelido E uso cru), vars pela anotação de dono em
  `vars.h`, espaço de ROM pelo print do linker (teto físico 32 MB). Faixa
  alheia não se ocupa (a invasão de Kanto sobre a faixa de Sinnoh custou
  uma correção de orçamento; está documentada no PLANO-OBRAS-SINNOH.md).
- **Suíte manda em default de jogo novo** (AUTO RUN nasceu desligado por
  isso); enfraquecer caso para passar é proibido; falha que não repete roda
  duas vezes; duas tentativas falhas do mesmo conserto = diagnóstico errado.
- Decisão registrada não se reabre por conveniência de executor: decisões do
  Gui e da condutora vivem nos PLANO-OBRAS-*.md e no ESTADO; o que não está
  coberto volta para o plano, não vira invenção.

## Fases, em ordem, com critério de pronto

### Fase A: obra de Sinnoh (EM CURSO; plano: `PLANO-OBRAS-SINNOH.md`)

Estado ao escrever: ondas 1-2 prontas (máquina/gerador com andabilidade,
grupos livres, arcos de abertura e Jubilife/Oreburgh/Eterna, 16 casos T100),
onda 2 em fechamento. Restam as ondas S5 (Hearthome/Veilstone/Pastoria/
Solaceon/Celestic/R209), S6 (QG/Coronet/Acuity/Snowpoint/R217/Spear Pillar/
Canalave/R218), S7 (pós-liga: Sunyshore/Valor/R224/R227/Stark/Resort/Villa/
Mansão/Fight Area + Amity como warps comuns) e S8 (QA: ensinar a fila que
esqueleto `@ TODO` não é cena; regenerar fila com os descartes anotados;
casos das levas; calibrações registradas no plano, incluindo o grupo
storage-key de Veilstone marcado "feita" por engano).

Inclui um EXECUTOR DE TREINADORES com dono exclusivo de
`opponents.h`/`trainers.party` e faixa de id anotada (ESTADO seção 6), para
os treinadores de HISTÓRIA que as cenas cobram (ex.: rival da Route 203) e a
harmonização do prédio da Windworks com a luta externa da Mars (batalha não
se duplica; id de treinador é derrotável uma vez).

**Pronto quando**: fila de Sinnoh sem pendente executável (sobram SÓ os
adiados por decisão: 6 acompanhantes, 41 Pokécenter/Mart, clones, Route210
sem mapa), suíte verde com os casos de todas as levas, T11 3/3, ESTADO e
ROMs atualizados.

### Fase B: sobras de Unova (29) e Johto (4)

Detalhadas na fila com bloqueio residual documentado. Método idêntico
(executor + autor de caso + fechador). O que estiver bloqueado por decisão
que não existe (arte, mecânica) fica e é reportado ao Gui no fechamento.

**Pronto quando**: fila zerada fora de bloqueio por decisão externa.

### Fase C: dívidas registradas (cada uma com seu portão)

**Portões Fable da Fase C RESOLVIDOS pela condutora em 18/08/2026:**

- **Item 3 (heal locations de Sinnoh): AUTORIZADO em APPEND.** O save guarda
  o último ponto de cura como dados de warp crus (WarpData), não como
  índice, então acrescentar `HEAL_LOCATION_*` no FIM da tabela não fere a
  janela (provar com guarda_save + T11 na onda). Entram as 7 cidades de
  ginásio sem heal location + a Liga sul; o `chapter_jump.c` passa a usar
  `SetLastHealLocationWarp` nelas (fecha o risco registrado do seletor).
- **Item 2 (3 vars de Kanto colidindo com Hoenn): AUTORIZADO o realias.**
  `VAR_MAP_SCENE_ROUTE22` -> `0x40F7`, `VAR_MAP_SCENE_VIRIDIAN_CITY_OLD_MAN`
  -> `0x40F8`, `VAR_MAP_SCENE_ROUTE16` -> `0x40F9` (faixa livre 0x40F7-0x40FE
  medida, dono anotado). Save existente perde o progresso dessas TRÊS cenas
  de Kanto (elas já estavam corrompidas pela colisão com Hoenn; migração
  documentada, guarda_save pode acusar e o condutor aceita com --gravar
  justificado).
- **Item 1 (1362 item balls de J/S/U): ADIADO por desenho.** Não existe
  solução sem flag 1:1 (item ball só persiste por flag neste motor) e o pool
  livre precisa sobrar para a obra de Galar. Fica para a era de reabertura
  da janela de save (quando FLAGS_COUNT puder crescer de novo). Até lá o
  dupe é conhecido e benigno.
- **Item 4 (mecânica de parceiro): segue PORTÃO FABLE aberto** (desenho de
  mecânica, não se executa nesta fase).

1. **1362 item balls duplicáveis de Johto/Sinnoh/Unova**: PORTÃO FABLE
   (desenho de orçamento de flags; 1:1 não cabe no pool sem matar outras
   obras). Não executar sem o desenho.
2. **3 vars de cena de Kanto colidindo com Hoenn** (`vars_frlg.h` sem
   guarda; base secreta remexe a Route 22): conserto pequeno, cabe numa
   onda de fase A/B com dono de vars.h; realias para vars livres medidas.
3. **Heal locations das 7 cidades de ginásio de Sinnoh** (Chapter Jump leva
   mas respawn não atualiza): mexe em `heal_locations`; PORTÃO FABLE curto
   para confirmar que não fere a janela de save; depois é leva mecânica.
4. **Mecânica de parceiro** (destrava 6 acompanhantes de Sinnoh: Cheryl,
   Riley, Mira, Buck, Marley, rival): PORTÃO FABLE (desenho de mecânica).
5. **T90.5/Kiyo** e demais calibrações herdadas: resolver quando a leva da
   região correspondente abrir aquele arquivo.

### Fase D: B10, o espaço (pré-requisito de Galar)

**PORTÃO FABLE DA FASE D RESOLVIDO pela condutora em 18/08/2026** (base:
PRD-ROM-COMPLETA seção 11; overworld dos 330 KB já foi feito em 15/08):

- **D1, indireção de treinador (~485 KB, primeiro por ser o desenho mais
  maduro)**: `u16` de índice denso por id (teto 4000 fica, flags de
  treinador NÃO deslizam, save-neutro), `gTrainers`/`sTrainerSlides` viram
  densos, e TODO acesso passa pelo funil `GetTrainerStructFromId` (varrer o
  repo por acesso direto `gTrainers[` antes; qualquer um fora do funil é
  parte do trabalho). A tabela densa e o índice saem de gerador
  (trainerproc ou dev_script), nunca à mão. Prova: suíte inteira (dezenas
  de casos com `oponente=N`), T11, e a régua de aborto abaixo.
- **D2, duplicatas byte a byte (~155 KB)**: dedupe por
  compartilhamento de ponteiro em build (paletas idênticas, .smol,
  pegadas), gerador com censo e prova de md5 por asset lógico.
- **D3, ícones comprimidos (~673 KB, por último, médio/alto)**: mudar o
  carregamento de `CreateMonIcon` para descomprimir em buffer. Régua de
  aborto EXPLÍCITA: se custar mais de +0,3% de EWRAM/IWRAM ou qualquer
  vermelho de suíte não mecânico, aborta e registra; espaço não vale
  regressão (decisão dos 32 MB do Gui).
- Cada D é uma onda própria com fechador, suíte completa e T11. Meta da
  fase: ~1,3 MB de volta sem perder um byte de conteúdo.

Ícones (~673 KB) e indireção de treinador (~485 KB), ambos mudança de
engine; overworld já foi feito (rodada de 15/08). Meta: ~1,9 MB livres.
PORTÃO FABLE se o desenho da indireção não estiver escrito no PRD-ROM-
COMPLETA.md seção 11 em nível executável; senão, onda de engine com suíte
inteira e T11 obrigatórios (é exatamente o tipo de mudança que quebra save
calado).

**Pronto quando**: ROM abaixo de ~94% com suíte verde e T11 3/3.

### Fase E: obra de Galar (aprovada pelo Gui em 17/08; escopo em
`fontes-mapas/PLANO-GENS-6-9.md` e memória `pokemon-claude-gens-6-9-escopo`)

Galar vira a 6ª região a partir dos 440 mapas GBA extraídos do demake
Ultimate Plus (`fontes-mapas/galar-swsh/extraidos-ultimate/`), campanha base
primeiro (~1,2-1,4 MB). Kalos, Alola e Paldea estão PARADAS por decisão
explícita: nem batalha entra; não despachar nada para elas.

PORTÃO FABLE OBRIGATÓRIO antes de executar: o desenho da obra (molde
PLANO-OBRAS-*: conversão de tileset/metatile do demake para cá, orçamento de
grupos de mapa/flags/vars/ids, ordem de levas, o que da história do demake
entra). Uso privado de trabalho fan-made: nunca publicar sem crédito e
permissão; lembrete permanece no plano.

**Pronto quando**: Galar atravessável de ponta a ponta com insígnias e Liga,
capítulos no Chapter Jump, casos de suíte por leva, T11 3/3.

### Fase F: polimento final (decisão 2 do Gui: batalha fica para o FIM)

Times de líderes/E4/campeões (os 22 blocos com Dynamax sem lenda anotados no
B8), treinadores diários de Pokécenter (41 grupos), balanceamento de curva.
Só abre quando A-E fecharem ou o Gui mandar antes.

## Interação com o Gui durante o goal

- Relatório de fechamento por onda: placar, verificado x presumido, consumo
  por modelo, riscos. CURTO, resposta primeiro (Regra Zero do CLAUDE.md).
- O que vai para o Gui: decisão de gosto/prioridade/dinheiro, aprovação de
  coisa irreversível fora do fluxo normal (o commit+push do repo é fluxo
  normal), bugs de playtest dele viram leva imediata da fase corrente.
- O que NÃO vai para o Gui: status de sistema, pergunta que uma leitura
  responde, confirmação do que a suíte já provou.
- Bug reportado pelo Gui em jogo tem prioridade sobre a onda seguinte
  (consertar no working tree limpo, com caso de suíte, commit próprio).

## Critério de pronto do PRD inteiro

Suíte verde completa (incluindo os casos de todas as fases), T11 3/3 contra
a ROM congelada de referência, fila `fila_b6.json` sem pendente executável
em nenhuma região, Galar jogável, ROM oficial datada + ROM de teste
sobrescrita no workspace, ESTADO.md com a seção de fechamento, memória do
workspace apontando para o estado final, e um handoff de encerramento no
molde de `/tmp/handoff-pokemon-claude-2026-08-15.md`.
