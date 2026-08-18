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
- J2: item balls 1:1 (decisão 3), gerador por região, suíte por amostra
  (pegar item, flag liga, item não volta; par negativo).
- J3: heal locations + Chapter Jump de Sinnoh (decisão 4).
- J4: vars de Kanto fora da colisão + guarda de colisão (decisão 5).
- J5: fecho (decisão 8), com adversarial antes do fechador porque J1,
  J2 e J4 mexem em terreno de save.
