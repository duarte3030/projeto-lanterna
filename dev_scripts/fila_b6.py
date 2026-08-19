#!/usr/bin/env python3
"""Regenera a FILA do bloco B6 (cenas de história das três regiões portadas).

    python3 dev_scripts/fila_b6.py            # só o resumo por região e tipo
    python3 dev_scripts/fila_b6.py --gravar   # escreve dev_scripts/fila_b6.json
    python3 dev_scripts/fila_b6.py --demo     # autoteste (não escreve nada)

## Por que este arquivo existe

Até 15/08/2026 o B6 não tinha fila: `ESTADO.md`, `PLANO-UNOVA.md`,
`PENDENCIAS-JOHTO.md` e `PENDENCIAS-NPC-SINNOH.md` guardavam só NÚMEROS
AGREGADOS, escritos à mão em datas diferentes, e por isso divergiam entre si
(104 x 107 x 40 cenas de `changeblock`; 348/176 x 230/84 objetos e gatilhos de
Sinnoh). Número agregado escrito à mão envelhece calado: ninguém consegue
conferir de onde ele veio, e quem for executar não sabe QUAL cena falta, só
quantas.

A fila aqui é a **saída de uma varredura**, nunca um texto digitado. Base nova
(mapa novo importado, cena portada, item criado), roda de novo e o JSON conta a
verdade daquele dia. `fila_b6.json` é artefato gerado: não editar à mão.

## O critério de classificação, e por que é o mesmo da casa

Uma "cena" do gen 2 não é um script só: o `coord_event` aponta para um rótulo
que salta para outros rótulos, e o comando que decide o QUANTO de trabalho a
cena dá (o `changeblock`, o `callasm`) quase sempre mora dois ou três saltos
adiante. Medir só o corpo do primeiro rótulo mente para baixo: a varredura
anterior achou **8 `callasm` literais em 5 arquivos** de `bw3g/maps/`, enquanto
a cadeia inteira mostra **16 cenas** que chegam a `callasm`, porque quase todos
estão em `engine/events/` e são alcançados por `jumpstd`/`farsjump`.

Por isso a travessia usa o MESMO regex que o inventário da casa já usa para
saber se um NPC fala: `SEGUE_GEN2` em `dev_scripts/inventario.py` (linha ~468),
que é `sjump|jump|callasm|scall|farsjump`, mais o `JUMPSTD` da linha seguinte
(que leva para `engine/events/std_scripts.asm`). Os dois são IMPORTADOS daqui,
não copiados: duas cópias do critério divergiriam no dia em que uma fosse
ajustada, e o preço seria uma fila que discorda do inventário sobre o que é
cena. A profundidade é 6 saltos (o inventário usa 3 porque só quer saber se há
texto; aqui o interesse é o fecho inteiro).

### FALLTHROUGH: o corpo de um rótulo não acaba no rótulo de baixo

`corpos_gen2` corta o corpo de um rótulo no rótulo seguinte, e o dialeto de
gen 2 **cai de um rótulo para o outro** quando o de cima não termina em
terminador de fluxo. Quem lê só o pedaço cortado vê uma cena de duas linhas onde
existe uma cutscene inteira.

O caso que pegou isto, achado pelo executor de Unova em 15/08/2026, está em
`bw3g/maps/DragonspiralTower6F.asm:29`:

    DragonspiralTowerInferScript1:
        moveobject DRAGONSPIRALTOWER6F_INFER, 2, 8
        ; fallthrough
    DragonspiralTowerInferScript2:
        special FadeOutMusic
        ...

O `coord_event` de (2,13) aponta para o `Script1`. Cortado no rótulo, ele tem
**2 linhas e nenhum comando caro**, e a fila o despachou como `portavel`, sem
bloqueio. Seguindo o fallthrough ele tem **67 linhas** e alcança `setscene`,
`special` e batalha: é o encontro do Infer, não uma cena portável. As QUATRO
cenas de Unova que a fila tinha marcado como prontas para executor estavam todas
nesta condição (`DragonspiralTower6F`, `PlayersHouse1F` em `MeetMomLeftScript`,
`NacreneCity` em `LenoraScript4`, `OpelucidCity` em `IrisScript3`).

Agora o corpo CONTINUA no rótulo de baixo, recursivamente, quando não termina em
terminador, e o que ele alcança conta para tipo e bloqueio exatamente como o que
foi alcançado por salto. A lista de terminadores está em `TERMINADORES`, e foi
levantada da fonte, não chutada (ver o comentário lá).

**Cena x chamada x arquivo, que é a origem das três divergências:**

- **cena** = um `coord_event` de um mapa que foi importado. É a unidade da fila,
  porque é o que o jogador dispara. Unova tem **209**.
- **chamada** = uma linha `changeblock` dentro do fecho de uma cena. A MESMA
  linha conta de novo se duas cenas chegam nela, e é por isso que as 1226
  chamadas cabem em 884 linhas de fonte.
- **arquivo** = um `.asm` de `bw3g/maps/`. São **40** os que citam `changeblock`
  em qualquer lugar, inclusive em script que nenhum `coord_event` alcança. Esse
  40 nunca foi contagem de cena, e comparar com 107 é comparar coisas
  diferentes.

O tipo de cada cena sai por PRIORIDADE, não por soma: uma cena que tem
`changeblock` e `setscene` entra uma vez só, como `changeblock`, que é o
trabalho mais caro. Os totais por tipo dos documentos são SOBREPOSTOS (somam
250 para 209 cenas), e o JSON guarda os dois: `tipo` é o exclusivo, `tem` lista
todos os comandos caros que a cena alcança.

## Sinnoh: a fila sai da MESMA recusa do importador

`dev_scripts/importa_npcs_sinnoh.py` recusa, de propósito, objeto com
`hidden_flag` (decisão 2 do cabeçalho dele) e todo `coord_event` (a var do
Platinum não existe aqui). Este script IMPORTA aquele módulo e repete a recusa
na mesma ordem (mobília -> nome próprio -> hidden_flag), sobre todos os mapas
casados, com uma diferença que é o ponto:

**o atalho `ja_importado` fica de fora.** Lá ele existe para não dobrar a
população da cidade ao rodar `--aplicar` duas vezes, e por isso o `resumo:` que
o importador imprime encolhe a cada rodada: em 15/08/2026 ele diz 78/46 porque
pula 360 mapas já marcados. Esse número mede "o que sobrou de não visitado",
não "quanto falta de cena", e foi ele que produziu os 348/176 do `ESTADO.md`.
A população é invariante e não depende de quantas vezes alguém rodou o
importador.

A unidade da fila de Sinnoh não é o objeto: é a **`FLAG_HIDE_*`**, porque o que
falta é a CENA que apaga a flag, e uma cena apaga a flag de todos os objetos
dela de uma vez (regra escrita em `PENDENCIAS-NPC-SINNOH.md` seção 3). Para os
gatilhos, a unidade é `(mapa, var, script)`.

### "Feita" de Sinnoh olha o CONTEÚDO do hack, não uma lista de referência

A primeira versão deste arquivo decidia o `status` de Sinnoh por PROXY: cruzava
a `FLAG_HIDE_*` com a lista de cenas de `cena_galactica_sinnoh.py`. Proxy erra
por construção, e errou: em 15/08/2026 o executor achou que **20 dos 23 objetos
que a fila dava como pendentes já estavam nos `map.json`**, plantados pela leva
"Sinnoh ganha voz" (`c7c8b4a201`), que não deixou marca `origem` nem aparece em
lista nenhuma. Trabalho feito por quem não avisou continua feito.

Agora a conferência lê o mapa de verdade. Um objeto da fonte conta como FEITO
quando existe, no `data/maps/<Mapa>/map.json` do hack casado, um `object_event`
que satisfaz os três:

1. **mesmo gráfico**, depois de passar pela MESMA tabela de troca do importador
   (`V.TROCA_SPRITE`, `V.SPRITE_PADRAO`): `OBJ_EVENT_GFX_GRUNT_M` da fonte
   procura `OBJ_EVENT_GFX_MAGMA_MEMBER_M` aqui, porque GRUNT não existe nesta
   ROM e procurar pelo nome da fonte daria pendente para tudo;
2. **coordenada igual ou vizinha** dentro de `RAIO_PADRAO` tiles (Chebyshev),
   com a coordenada da fonte passada pelo `conversor_de_coordenada` do
   importador, que é o mesmo que pôs os NPCs mudos no lugar. **Exceção, e ela
   pesa: objeto de cena não passa pelo raio.** Se o objeto do hack carrega uma
   `flag` que EXISTE em `include/constants/flags.h`, alguém escreveu a cena dele
   de propósito, e a coordenada escolhida por essa pessoa não tem obrigação de
   bater com a conta proporcional. Medido em 15/08/2026, depois da rodada da
   rota principal de Sinnoh: o ROWAN de Jubilife está em (43,38) e a conversão
   pede (51,4); os grunts da Valley Windworks estão em y=74 contra y=47. Com
   âncora de posição, nove cenas recém-escritas continuavam na fila cobrando
   trabalho já feito;
3. **casamento 1:1**: cada objeto do hack é consumido por um objeto da fonte só.
   Sem isso, os cinco grunts do QG casariam todos com o primeiro grunt do mapa e
   a fila zeraria sozinha.

O desempate, quando mais de um par cabe, é a **flag de esconder**: objeto do
hack com `flag` de verdade é objeto de cena, e casa primeiro com quem nasce
escondido na fonte.

**A mesma flag decide o BLOQUEIO, e por causa de um falso positivo medido.** Um
grupo só parcialmente posto sai como "sem bloqueio" (a cena existe, falta pôr o
resto) **apenas se algum objeto casado carregar flag de verdade**. Sem isso, o
"parcialmente posto" pode ser um NPC de rua que calhou de cair perto com o mesmo
sprite, que foi o caso do `FightArea` na rodada anterior: ele apareceu como
pronto para executor e a leva de Sinnoh provou que não era. Regra: **flag de
esconder citada que não existe em `flags.h` => BLOQUEADO.**

`tamanho` de uma linha de Sinnoh passa a ser **quanto FALTA** (objetos ainda
ausentes), e `objetos_fonte` guarda o total da fonte. Grupo com zero faltando
sai como `feita`.

## >>> REGRA DE PROCESSO, e ela vale mais que qualquer número deste arquivo <<<
##
##      PENDENTE É COBRANÇA, NÃO CERTEZA.
##
## O executor CONFERE O CONTEÚDO DO MAPA antes de escrever qualquer objeto, e
## REPORTA FALSO PENDENTE DE VOLTA À FILA. Nenhum medidor automático substitui
## isso, e nem precisa: foi exatamente esse laço que pegou o caso dos 20 de 23
## objetos que a fila cobrava e já estavam no mapa, e pegou barato. Fila que se
## corrige pelo retorno do executor erra menos que fila que tenta adivinhar
## certo de primeira.

**O teto deste critério, medido e dito:** ele acha o que está no lugar
convertido, e a leva "Sinnoh ganha voz" não posicionou pela mesma conta (ela
pôs gente onde o mapa convertido pedia). O número de pares cresce com o raio
(medido: 19 objetos no raio 0, 25 no raio 2, 37 no raio 4, 50 no raio 8, 90
ignorando posição), e o raio certo é calibração, não gosto. Por isso `--raio N`
existe e o relatório sempre diz com que raio foi medido. Aumentar demais casa
NPC com o vizinho errado, e aí a fila mente para baixo, que é pior do que mentir
para cima, mas o erro dos dois lados está coberto pela regra de processo acima.

**Divergência conhecida entre os dois medidores, anotada de propósito:** o
executor de Sinnoh casa por **TEXTO DE FALA**, byte a byte contra a fonte (via
`dev_scripts/texto_sinnoh.py`, função `resolve`, linha ~190), e nos mesmos 7
mapas reconheceu 20 de 23 objetos, contra 16 de 27 do casamento por
gráfico+posição daqui. Os denominadores são diferentes (ele conta o que foi
olhar, esta fila conta o que a fonte tem), então os dois números não se
contradizem, mas o método dele é mais forte: texto é identidade, posição é
palpite. **Upgrade futuro, se um dia doer:** casar pelo texto, comparando os
rótulos `.string` dos `data/maps/<Mapa>/scripts.inc` com o que `texto_sinnoh.resolve`
extrai da fonte. Não foi feito agora porque a ferramenta já serve ao propósito,
e casar por texto é bem mais caro que casar por sprite e tile.

**Gatilho (`coord_event`) não tem como casar por nome, e isto é medição, não
preguiça:** o `script` da fonte é índice de narc (um número), e as **70 vars do
Platinum não existem nesta ROM** (conferido contra `include/constants/vars.h`:
zero das 70). Não há nome dos dois lados para comparar. O que corresponde de
verdade é o TILE que dispara, então o gatilho conta como feito quando o mapa do
hack tem um `coord_event` na coordenada convertida, dentro do mesmo raio.

### Unova também confere conteúdo. Johto não dá, e isto está declarado

A mesma pergunta feita a Unova pegou outra mentira de proxy: a fila dava as 209
como pendentes porque `PLANO-UNOVA.md` diz "0 de 209", e em 15/08/2026 o hack já
tinha **16 `coord_events` em 4 mapas de Unova** (`AspertiaGym`, `CasteliaGym`,
`ChampionsRoomEntrance`, `LentimasGym`), postos por quem está executando esta
fila agora. Documento que diz "0" envelhece igual a todo o resto.

Unova é conferência mais barata que Sinnoh e não tem raio para calibrar: o
importador de Unova copia `x,y` da fonte tal e qual (a geometria de gen 2 entra
1:1), então cena feita é cena cujo par `(x, y)` já aparece nos `coord_events` do
nosso `map.json`. Par exato, sem vizinhança.

**Johto continua por proxy, e não há como não ser.** A fila de lá é transcrição
de prosa, e os dois `status: feita` (Teatro de Ecruteak, 18 heal locations) são
texto de documento, não leitura de mapa: não existe fonte de máquina de Johto
que dê para varrer do mesmo jeito. O que É lido do repo, e vale, são os
BLOQUEIOS: `include/constants/items.h`, `event_objects.h` e `opponents.h`
respondem por si se o sino, o sprite e o id existem.

## Johto: transcrição, e isto está declarado

Johto é a única região cuja fila NÃO sai de varredura: a fonte dela é a seção 6
de `PENDENCIAS-JOHTO.md`, escrita à mão por quem fechou a primeira leva, e não
existe artefato de máquina que a reproduza. O que este script faz é transcrever
aquela seção para o mesmo formato e **conferir os bloqueios contra o repo**
(`ITEM_TIDAL_BELL` existe? `OBJ_EVENT_GFX_RED_NORMAL` existe? sobrou id de
treinador na faixa 2462-2499?), para que o bloqueio pare de ser memória de
documento e vire leitura de `include/`.
"""
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import inventario as INV                # noqa: E402  SEGUE_GEN2/JUMPSTD/corpos_gen2
import importa_unova as U               # noqa: E402  le_grupos/le_eventos/indice_asm
import importa_npcs_sinnoh as S         # noqa: E402  a régua de recusa de Sinnoh
import valida_mapas_sinnoh as V         # noqa: E402  TROCA_SPRITE/sprites_utilizaveis

SAIDA = os.path.join(REPO, "dev_scripts/fila_b6.json")
PROFUNDIDADE = 6

# Comandos que decidem o custo de uma cena de gen 2, em ORDEM DE PRIORIDADE.
# A ordem é a do PLANO-UNOVA.md: o `changeblock` primeiro porque é o único que
# obriga a traduzir id de bloco do gen 2 para metatile daqui, um por um.
COMANDOS = [
    ("changeblock", re.compile(r"^\s*changeblock\b", re.M)),
    ("setscene",    re.compile(r"^\s*(?:setscene|setmapscene)\b", re.M)),
    ("batalha",     re.compile(r"^\s*(?:loadtrainer|startbattle|loadwildmon"
                               r"|winlosstext)\b", re.M)),
    ("special",     re.compile(r"^\s*special\b", re.M)),
    ("callasm",     re.compile(r"^\s*callasm\b", re.M)),
]
# Cena que empurra o jogador. É o sinal do "bloqueio" de PLANO-UNOVA.md: o NPC
# vira, fala e devolve o jogador, e como o enredo nunca avança aqui, portar isso
# planta parede permanente (a armadilha das 39 pedras de Strength).
MOVE_JOGADOR = re.compile(r"^\s*applymovement\s+PLAYER\b", re.M)


# Comando que ENCERRA o fluxo de um rótulo. A lista foi LEVANTADA da fonte, não
# chutada: varrendo o último comando de cada corpo de rótulo em `bw3g/maps/*.asm`
# (2570 `done`, 932 `end`, 373 `step_end`, 335 `itemball`, 295
# `jumptextfaceplayer`, 160 `jumptext`, 129 `hiddenitem`, 126 `jumpstd`, 53
# `jump`, 47 `return`...), e conferindo cada nome contra a definição de macro em
# `macros/scripts/`. `done` é o fim de CAIXA DE TEXTO (`macros/scripts/text.asm`
# linha 7), e por isso bloco de texto também não escorre. `sjump` e `farsjump`
# não existem neste dialeto, ficam por segurança porque `SEGUE_GEN2` os cita.
TERMINADORES = frozenset("""
done end endall return ret jump sjump farsjump jumptext farjumptext
jumptextfaceplayer jumpstd itemball hiddenitem hiddengrotto fruittree
rematchgift describedecoration step_end warpfacing
""".split())


def termina(corpo):
    """O corpo acaba sozinho, ou escorre para o rótulo de baixo?"""
    for linha in reversed(corpo.splitlines()):
        limpa = linha.split(";")[0].strip()
        if limpa:
            return limpa.split()[0] in TERMINADORES
    return True   # corpo vazio: rótulo que é só apelido do de baixo


def indice_de_rotulos():
    """rótulo -> corpo, e rótulo -> rótulo SEGUINTE, em TODO o bw3g.

    O `callasm` indireto mora em `engine/events/`; sem varrer a árvore inteira a
    cadeia morre no primeiro salto para fora de maps/ e a fila mente para baixo.
    O mapa de "seguinte" é por ARQUIVO, e existe para o fallthrough (ver
    cabeçalho): só o vizinho de baixo no mesmo `.asm` recebe a execução que
    escorre.
    """
    corpos, seguinte = {}, {}
    for raiz, _, arquivos in os.walk(U.BW3G):
        if os.sep + ".git" in raiz:
            continue
        for a in sorted(arquivos):
            if not a.endswith(".asm"):
                continue
            txt = open(os.path.join(raiz, a), encoding="utf-8",
                       errors="replace").read()
            itens = list(INV.corpos_gen2(txt).items())
            for i, (k, v) in enumerate(itens):
                if k in corpos:
                    continue
                corpos[k] = v
                if i + 1 < len(itens):
                    seguinte[k] = itens[i + 1][0]
    return corpos, INV.corpos_std_gen2(U.BW3G), seguinte


def fecho(rot, corpos, std, seguinte, prof=0, visto=None):
    """Corpos alcançados a partir de `rot`: SEGUE_GEN2, JUMPSTD e FALLTHROUGH."""
    if visto is None:
        visto = set()
    if not rot or rot in visto or prof > PROFUNDIDADE:
        return []
    visto.add(rot)
    corpo = corpos.get(rot)
    if corpo is None:
        return []
    saida = [corpo]
    for m in INV.SEGUE_GEN2.finditer(corpo):
        saida += fecho(m.group(1), corpos, std, seguinte, prof + 1, visto)
    for m in INV.JUMPSTD.finditer(corpo):
        alvo, chave = std.get(m.group(1).lower()), "jumpstd:" + m.group(1).lower()
        if alvo is not None and chave not in visto:
            visto.add(chave)
            saida.append(alvo)
            for mm in INV.SEGUE_GEN2.finditer(alvo):
                saida += fecho(mm.group(1), corpos, std, seguinte, prof + 1, visto)
    # ponytail: fallthrough NÃO gasta profundidade. Salto é escolha do roteiro e
    # 6 níveis já cobrem o mais fundo que a fonte tem; escorrer é a MESMA cena
    # continuando, e cortá-la no meio por orçamento de recursão traria de volta
    # justamente o defeito que este trecho conserta. O ciclo já está travado por
    # `visto`.
    if not termina(corpo):
        saida += fecho(seguinte.get(rot), corpos, std, seguinte, prof, visto)
    return saida


# ------------------------------------------------------------------- unova

def coords_do_hack(mapa):
    """Os `coord_events` que o nosso `map.json` já tem, por coordenada.

    Serve de conferência de conteúdo para Unova. Aqui a coordenada é 1:1 (o
    importador de Unova copia x,y da fonte, ao contrário de Sinnoh, que é
    proporcional), então o par exato basta e não há raio para calibrar.
    """
    p = os.path.join(REPO, "data/maps", mapa, "map.json")
    if not os.path.exists(p):
        return set()
    d = json.load(open(p))
    return {(int(c.get("x", 0)), int(c.get("y", 0)))
            for c in (d.get("coord_events") or [])}


def fila_unova():
    corpos, std, seguinte = indice_de_rotulos()
    idx = U.indice_asm()
    itens, chamadas = [], collections.Counter()
    for _, mapas in U.le_grupos():
        for camel, const, *_ in mapas:
            p = idx.get(camel) or f"{U.BW3G}/maps/{camel}.asm"
            if not os.path.exists(p):
                continue
            asm = open(p, encoding="utf-8", errors="replace").read()
            ja = coords_do_hack(U.PREFIXO + camel)
            for x, y, cena, rot in U.le_eventos(asm, camel)["coord"]:
                corpo = "\n".join(fecho(rot, corpos, std, seguinte))
                tem = [n for n, rx in COMANDOS if rx.search(corpo)]
                for n, rx in COMANDOS:
                    chamadas[n] += len(rx.findall(corpo))
                empurra = bool(MOVE_JOGADOR.search(corpo))
                tipo = tem[0] if tem else ("portavel_bloqueio" if empurra
                                           else "portavel")
                itens.append({
                    "regiao": "unova",
                    "id": f"{camel}.asm:{rot}@{x},{y}",
                    "mapa_destino": U.PREFIXO + camel,
                    "tipo": tipo,
                    "tem": tem,
                    "tamanho": len(corpo.splitlines()),
                    "bloqueio": BLOQUEIO_UNOVA[tipo],
                    "status": "feita" if (int(x), int(y)) in ja else "pendente",
                })
    return itens, chamadas


BLOQUEIO_UNOVA = {
    "changeblock": "traduzir id de bloco do gen 2 para metatile, um por um, "
                   "mais uma flag por estado",
    "setscene": "a máquina de estados do enredo da Plasma não existe nesta ROM",
    "batalha": "treinador da cena precisa de id em opponents.h e time em "
               "trainers.party",
    "special": "o `special` do gen 2 não tem equivalente aqui",
    "callasm": "callasm é código do gen 2 chamado da cena; sem equivalente",
    # O detector é `applymovement PLAYER`, e é MAIS LARGO que a contagem à mão
    # de PLANO-UNOVA.md (17): ele pega também a segunda metade de cena, que move
    # o jogador sem empurrá-lo. Larga de propósito: cena que mexe no jogador sem
    # o enredo por trás é sempre revisão humana, nunca trabalho de executor.
    "portavel_bloqueio": "cena mexe no jogador (applymovement PLAYER); sem o "
                         "enredo por trás vira parede permanente ou movimento "
                         "sem motivo, precisa de revisão humana",
    "portavel": "nenhum",
}


# ------------------------------------------------------------------ sinnoh

# As cenas da Galáctica fechadas em 12/08/2026 por
# `dev_scripts/cena_galactica_sinnoh.py`. A chave é a `FLAG_HIDE_*` da fonte,
# que é o que a cena passou a apagar; lida do próprio script, nunca digitada.
def mapas_casados_sinnoh():
    heads = S.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(S.chave(h), (h, ev, mx))
    saida = []
    for m in S.mapas_editaveis_sinnoh():
        h = S.APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(S.chave(m))
        if alvo:
            saida.append((m,) + alvo)
    return saida


def vars_do_repo():
    p = os.path.join(REPO, "include/constants/vars.h")
    return set(re.findall(r"#define\s+(VAR_\w+)", open(p).read()))


def flags_do_repo():
    """As `FLAG_*` que existem de verdade em `include/constants/flags.h`.

    Serve de prova de cena para Sinnoh, e existe por causa de um falso positivo
    medido em 15/08/2026: o `FightArea` saía como "sem bloqueio" só porque um
    objeto de rua com o mesmo sprite caiu perto da coordenada convertida. Sprite
    igual perto do lugar certo é palpite; objeto carregando uma `flag` que
    EXISTE em flags.h é prova, porque alguém escreveu a cena que a acende.
    Regra: flag de esconder citada que não existe aqui => BLOQUEADO.
    """
    p = os.path.join(REPO, "include/constants/flags.h")
    return set(re.findall(r"#define\s+(FLAG_\w+)", open(p).read()))


# Raio, em tiles, da conferência de conteúdo. É KNOB, não constante de gosto: a
# conversão de coordenada de mapa de rua é PROPORCIONAL (decisão 1 do
# importador), então o mesmo NPC sai alguns tiles fora do lugar do original, e
# levas escritas à mão puseram gente onde o mapa convertido pedia, não onde a
# proporção calcula. Medir com raio errado mente nos dois sentidos: apertado
# demais reabre trabalho feito, largo demais casa NPC com o vizinho.
#   python3 dev_scripts/fila_b6.py --raio 8
# Padrão 4 por decisão do coordenador em 15/08/2026: dobra o reconhecimento
# (37 objetos casados contra 25 no raio 2) sem soltar a âncora de posição.
RAIO_PADRAO = 4


def raio():
    if "--raio" in sys.argv:
        return int(sys.argv[sys.argv.index("--raio") + 1])
    return RAIO_PADRAO


def alvo_grafico(g, sprites):
    """O sprite que o objeto da fonte TERIA neste repo, pela mesma tabela do
    importador (`V.TROCA_SPRITE` / `V.SPRITE_PADRAO`). Sem isto a conferência
    procuraria `OBJ_EVENT_GFX_GRUNT_M`, que não existe aqui, e daria pendente
    para tudo."""
    return g if g in sprites else (V.TROCA_SPRITE.get(g) or V.SPRITE_PADRAO)


def casa_objetos(candidatos, do_hack, r, flags_reais):
    """Casamento 1:1 entre objeto da fonte e objeto que JÁ ESTÁ no map.json.

    `candidatos` = [(x, y, gfx_alvo, tem_hidden_flag)], `do_hack` = os
    `object_events` do nosso mapa. Um par vale quando o gráfico é o mesmo e a
    distância de Chebyshev cabe no raio. A ordem de preferência é
    (flag combina, distância), que é o desempate pedido: objeto do hack que
    carrega `flag` não-zero é objeto de cena, e casa antes com quem nasceu
    escondido na fonte. Cada objeto do hack é consumido uma vez só, senão cinco
    grunts da fonte casariam todos com o mesmo grunt do mapa.

    Devolve `(sem_par, flag_por_candidato)`: os índices que ficaram SEM par, e,
    para cada índice casado, a `flag` do objeto do hack com que ele casou (só
    as não-zero). A segunda metade é a prova de que existe cena, e ela é POR
    CANDIDATO de propósito: um mapa pode ter vários grupos de `hidden_flag`, e
    um grupo provado não pode desbloquear o vizinho.
    """
    livres = list(range(len(do_hack)))
    pares = []
    for i, (x, y, gfx, escondido) in enumerate(candidatos):
        for j in livres:
            o = do_hack[j]
            if o.get("graphics_id") != gfx:
                continue
            d = max(abs(int(o.get("x", 0)) - x), abs(int(o.get("y", 0)) - y))
            # ponytail: OBJETO DE CENA NÃO PRECISA DE RAIO. Posição é palpite,
            # e só serve para desempatar NPC anônimo de rua; um MAGMA_MEMBER que
            # carrega uma `flag` de verdade (existe em flags.h) é prova de que
            # alguém escreveu a cena dele, e a coordenada em que o autor o pôs
            # não tem obrigação de bater com a conta proporcional. Medido em
            # 15/08/2026: o ROWAN de Jubilife está em (43,38) e a conversão pede
            # (51,4); os grunts da Valley Windworks, em y=74 contra y=47. Com
            # âncora de posição, nove cenas recém-escritas continuavam na fila.
            # Teto: se um mapa tiver dois grupos do mesmo sprite e só um tiver
            # cena, o par pode sair trocado. O 1:1 e a ordem por distância
            # seguram o caso comum; se doer, casar por texto (ver upgrade).
            de_cena = str(o.get("flag", "0")) in flags_reais
            if d <= r or de_cena:
                pares.append((0 if de_cena == escondido else 1, d, i, j))
    pares.sort()
    sem_par, usados, flag_de = set(range(len(candidatos))), set(), {}
    for _, _, i, j in pares:
        if i in sem_par and j not in usados:
            sem_par.discard(i)
            usados.add(j)
            f = str(do_hack[j].get("flag", "0"))
            if f not in ("0", "0x0"):
                flag_de[i] = f
    return sem_par, flag_de


# ------------------------------------------- decisões DATADAS da obra de Sinnoh
#
# A obra de Sinnoh (`PLANO-OBRAS-SINNOH.md`, 16 a 18/08/2026) fechou por
# DECISÃO uma parte grande desta fila: mecânica que não existe neste motor,
# mapa que ainda é provisório, e três calibrações que a medição desta fila
# erra sozinha. Sem estas tabelas a fila volta a cobrar tudo isso a cada
# regeneração, e o executor da leva seguinte gasta o dia redescobrindo o que
# já foi decidido, que é exatamente o custo que a fila existe para cortar.
#
# Dois status novos saem de "pendente" e entram no lugar dele:
#   `descartada` = não vai existir neste porte, e o motivo é definitivo;
#   `adiada`     = é conteúdo real, mas depende de coisa FORA desta obra
#                  (mecânica sem desenho, mapa não importado).
# Os dois somem da conta de PENDENTES do resumo, que é o número que a
# condutora usa para dimensionar leva, e continuam no JSON com o motivo
# escrito, que é o que o executor lê antes de decidir mexer.

DESCARTE_VAR = {   # decisão 3: mecânica inexistente, não portada nem inventada
    "VAR_GTS_ACCESS_STATE":
        "GTS não existe aqui (decisão 3 do plano de Sinnoh, 16/08/2026)",
    "VAR_POKETCH_CAMPAIGN_STATE":
        "Pokétch não existe aqui (decisão 3, 16/08/2026)",
    "VAR_PAL_PARK_STATE":
        "migração de gen 3 não existe aqui (decisão 3, 16/08/2026)",
    "VAR_BATTLE_FRONTIER_DUMMY_STATE":
        "dummy declarado na própria fonte (decisão 3, 16/08/2026)",
    "VAR_FOLLOWER_MON_ACTIVE":
        "OW_FOLLOWERS_ENABLED é FALSE em include/config/overworld.h:61 "
        "(decisão 3, 16/08/2026)",
    # decisão 4, CORRIGIDA pela fonte em 18/08/2026 (retorno do S7): os 27
    # gatilhos do Amity não são warp de saída, são reposicionamento INTERNO
    # (pulo de cerca via applymovement), e o nosso Amity é passagem provisória
    # com planta emprestada.
    "VAR_AMITY_SQUARE_STATE":
        "descartado-por-mapa-provisório: os 27 gatilhos são reposicionamento "
        "interno da praça real do Platinum, e o nosso AmitySquare é passagem "
        "com planta emprestada (decisão 4 corrigida, 18/08/2026). Importar o "
        "exterior real do Platinum é pendência FORA desta obra",
}

ADIADO_VAR = {     # decisão 5: acompanhante que anda junto, mecânica sem desenho
    v: "mecânica de parceiro em dupla sem desenho (decisão 5 do plano de "
       "Sinnoh, 16/08/2026); ganha var quando a mecânica ganhar desenho"
    for v in ("VAR_FOLLOWER_RIVAL_STATE",
              "VAR_ETERNA_FOREST_FOLLOWER_CHERYL_STATE",
              "VAR_IRON_ISLAND_B2F_LEFT_ROOM_FOLLOWER_RILEY_STATE",
              "VAR_STARK_MOUNTAIN_ROOM_2_FOLLOWER_BUCK_STATE",
              "VAR_VICTORY_ROAD_1F_ROOM_2_FOLLOWER_MARLEY_STATE",
              "VAR_WAYWARD_CAVE_1F_FOLLOWER_MIRA_STATE")
}

# decisão 6: mecânica de batalha diária e de Mystery Gift, repetida por prédio.
ADIADO_FLAG = ("FLAG_HIDE_POKECENTER_DAILY_TRAINER_1",
               "FLAG_HIDE_POKECENTER_DAILY_TRAINER_2",
               "FLAG_HIDE_MART_MYSTERY_GIFT_DELIVERYMAN")

# Grupos que a obra fechou por decisão, um a um, com o motivo escrito.
# Chave = o `id` da linha da fila.
DECIDIDO_SINNOH = {
    # Stark Mountain, retorno do S5 (18/08/2026): a cena está ESCRITA e
    # correta, e mesmo assim é inalcançável.
    "StarkMountainOutside:FLAG_HIDE_STARK_MOUNTAIN_OUTSIDE_GRUNTS": (
        "descartada",
        "descartado-por-mapa-provisório: StarkMountainOutside usa "
        "LAYOUT_ROUTE226_ACCESS, molde de portão 13x9 com três linhas jogáveis "
        "(y=4,5,6) e duas decorativas (y=2,8). Medido no map.bin: o gatilho "
        "cai em (6,2) e o Grunt 1 em (3,2), linha morta; o Grunt 2 em (4,3) "
        "está em colisão 1. Volta a existir quando o exterior real da Stark "
        "Mountain for importado (18/08/2026)"),
    "StarkMountainOutside:coord:VAR_STARK_MOUNTAIN_OUTSIDE_STATE:3": (
        "descartada",
        "descartado-por-mapa-provisório, mesmo motivo do grupo "
        "FLAG_HIDE_STARK_MOUNTAIN_OUTSIDE_GRUNTS deste mapa (18/08/2026)"),
    # CALIBRAÇÃO 1 (registro do S2 para o S8, 17/08/2026): falso "feita".
    "VeilstoneCity:FLAG_HIDE_VEILSTONE_CITY_GRUNT_M_STORAGE_KEY": (
        "pendente",
        "CALIBRAÇÃO 17/08/2026: a fila deu por feito porque o desempate por "
        "distância casou este grunt com outro objeto do mapa. O script 13 da "
        "fonte (\"antennae\") não está portado em lugar nenhum: continua "
        "pendente de verdade"),
    # CALIBRAÇÃO 2 (mesmo registro): não é trabalho de cena, é id de treinador.
    "MtCoronet1FTunnelRoom:FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS": (
        "feita",
        "CALIBRAÇÃO 17/08/2026: os 3 trainers deste grupo foram portados DE "
        "PROPÓSITO para MtCoronet_1F_South e MtCoronet_B1F, porque id de "
        "treinador não pode duplicar entre mapas (derrotável uma vez só). A "
        "fila os procura aqui e não acha; o trabalho está feito, em outro mapa"),
}

# Notas que NÃO mudam status: calibração conhecida que o executor precisa ler
# antes de "consertar" o que não está quebrado.
NOTA_SINNOH = {
    "Route209_Access:coord:VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE:2":
        "os portões de molde 13x9 têm duas linhas decorativas (y=2 e y=8) sem "
        "ligação com o corredor jogável; o gerador do S1 plantou tile em (5,2) "
        "e (5,8) além dos jogáveis. Registro do S8 (18/08/2026): a checagem de "
        "andabilidade de maquina_sinnoh.py varre também o que já está gravado",
    "Route218_West:coord:VAR_ROUTE_218_GATE_TO_CANALAVE_CITY_STATE:2":
        "mesmo caso do Route209_Access: tiles decorativos em (7,2) e (7,8)",
    "Route210_South:MAP_HEADER_ROUTE_210_NORTH":
        "MAP_HEADER_* no campo hidden_flag é objeto CLONE (clone_id "
        "preenchido), e o campo guarda o MAPA DE ORIGEM, não uma flag. Clone "
        "nunca entrou no orçamento de flags desta obra (34 casos). O "
        "Route210_North em si continua fora: mapa não importado",
}


def rotulos_com_cena(mapa):
    """Rótulos do `data/maps/<mapa>/scripts.inc` que têm CENA de verdade.

    Item de QA pedido pela condutora em 17/08/2026: o esqueleto que
    `dev_scripts/maquina_sinnoh.py` planta é

        <Rotulo>::
            @ TODO S5: cena da fonte, rotulo <RotuloDaFonte>
            end

    e um `coord_event` apontando para isso não é cena nenhuma, é uma promessa.
    Sem esta leitura a fila dá por FEITOS os 95 gatilhos que o S1 plantou e
    para de cobrar as cenas deles, que é a mentira mais cara possível aqui.

    Régua: corpo sem NENHUM comando além de `end` (comentário e linha em
    branco não contam) é esqueleto. Rótulo que a leva resolveu de propósito
    com um `end` só (GalacticHQ_Hall, MtCoronet_1F_South) cai na mesma régua,
    e isso está certo: quem resolveu escreveu o motivo no `scripts.inc` e
    APAGOU o `coord_event`, então nem chega aqui.
    """
    p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
    if not os.path.exists(p):
        return set()
    txt = open(p, encoding="utf-8").read()
    achados, reais = list(re.finditer(r"^(\w+)::", txt, re.M)), set()
    for n, m in enumerate(achados):
        fim = achados[n + 1].start() if n + 1 < len(achados) else len(txt)
        corpo = [l.split("@")[0].strip()
                 for l in txt[m.end():fim].splitlines()]
        corpo = [l for l in corpo if l]
        if corpo != ["end"]:
            reais.add(m.group(1))
    return reais


def fila_sinnoh():
    r = raio()
    conhecidas = vars_do_repo()
    flags_reais = flags_do_repo()
    sprites = V.sprites_utilizaveis()
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    # [total na fonte, faltam, tem prova de cena]
    hid = collections.defaultdict(lambda: [0, 0, False])
    gat = collections.defaultdict(lambda: [0, 0])   # (mapa, var, script) -> idem

    for meu, header, arq, matriz in mapas_casados_sinnoh():
        p = os.path.join(S.PLAT, "res/field/events", arq + ".json")
        if not os.path.exists(p):
            continue
        fonte = json.load(open(p))
        d = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json")))
        L = layouts[d["layout"]]
        conv = S.conversor_de_coordenada(fonte, L["width"], L["height"],
                                         header, matriz, d)
        do_hack = d.get("object_events") or []
        # Gatilho só conta como feito se o rótulo dele tiver CENA: esqueleto
        # `@ TODO` + `end` é promessa, não trabalho (ver `rotulos_com_cena`).
        com_cena = rotulos_com_cena(meu)
        coords_hack = [(int(c.get("x", 0)), int(c.get("y", 0)))
                       for c in (d.get("coord_events") or [])
                       if c.get("script") in com_cena]

        candidatos, chaves = [], []
        for e in fonte.get("object_events", []):
            classe = e.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
            # MESMA ordem do importador: mobília sai como mobília, e só o que
            # sobra é medido pela hidden_flag.
            if any(t in classe for t in S.GRAFICOS_PROIBIDOS):
                continue
            if any(t in classe for t in S.NOMES_PROPRIOS):
                continue
            hf = str(e.get("hidden_flag", "0"))
            if hf in ("0", "0x0"):
                continue
            hid[(meu, hf)][0] += 1
            if conv is None:
                hid[(meu, hf)][1] += 1
                continue
            x, y = conv(e)
            candidatos.append((x, y, alvo_grafico(e["graphics_id"], sprites), True))
            chaves.append((meu, hf))
        sem_par, flag_de = casa_objetos(candidatos, do_hack, r, flags_reais)
        for i in sem_par:
            hid[chaves[i]][1] += 1
        # Prova de cena, por GRUPO: o objeto casado carrega uma `flag` que
        # EXISTE em flags.h. Sem isso, "parcialmente posto" pode ser só sprite
        # de rua que calhou de cair perto (o caso do FightArea).
        for i, f in flag_de.items():
            if f in flags_reais:
                hid[chaves[i]][2] = True

        for ce in fonte.get("coord_events", []):
            k = (meu, str(ce.get("var")), str(ce.get("script")))
            gat[k][0] += 1
            if conv is None:
                gat[k][1] += 1
                continue
            x, y = conv({"x": ce.get("x", 0), "z": ce.get("z", 0)})
            if not any(max(abs(cx - x), abs(cy - y)) <= r
                       for cx, cy in coords_hack):
                gat[k][1] += 1

    itens = []
    for (mapa, flag), (total, faltam, tem_cena) in sorted(hid.items()):
        itens.append({
            "regiao": "sinnoh", "id": f"{mapa}:{flag}", "mapa_destino": mapa,
            "tipo": "hidden_flag", "tem": [], "tamanho": faltam,
            "objetos_fonte": total,
            # Grupo PARCIALMENTE posto não tem bloqueio: se parte do elenco já
            # está no mapa, a cena que apaga a flag existe (foi ela que pôs), e
            # o que falta é só colocar o resto. O bloqueio de PENDENCIAS-NPC-
            # SINNOH §3 vale para grupo em que NADA foi posto ainda.
            "bloqueio": "nenhum" if faltam < total and tem_cena else
                        f"{flag} não existe aqui; trazer o objeto sem a cena que "
                        "a apaga planta bloqueio permanente",
            "status": "feita" if not faltam else "pendente",
        })
    for (mapa, var, script), (total, faltam) in sorted(gat.items()):
        itens.append({
            "regiao": "sinnoh", "id": f"{mapa}:coord:{var}:{script}",
            "mapa_destino": mapa, "tipo": "coord_event", "tem": [],
            "tamanho": faltam, "objetos_fonte": total,
            "bloqueio": "nenhum" if not faltam or var in conhecidas else
                        f"{var} não existe nesta ROM, e o script da fonte é "
                        "índice de narc, não rótulo",
            "status": "feita" if not faltam else "pendente",
        })
    return [decidido(i) for i in itens]


def decidido(i):
    """Aplica as decisões DATADAS da obra de Sinnoh sobre uma linha da fila.

    Ordem: o que foi decidido caso a caso (`DECIDIDO_SINNOH`) manda sobre a
    regra geral, porque a regra geral é que errou; depois vêm as decisões por
    var e por flag do plano. Linha já `feita` pela medição não é rebaixada por
    tabela de descarte/adiamento: trabalho feito continua feito.
    """
    if i["id"] in DECIDIDO_SINNOH:
        i["status"], i["bloqueio"] = DECIDIDO_SINNOH[i["id"]]
    elif i["status"] == "pendente":
        var = i["id"].split(":")[2] if ":coord:" in i["id"] else None
        flag = i["id"].split(":", 1)[1]
        if var in DESCARTE_VAR:
            i["status"], i["bloqueio"] = "descartada", DESCARTE_VAR[var]
        elif var in ADIADO_VAR:
            i["status"], i["bloqueio"] = "adiada", ADIADO_VAR[var]
        elif flag in ADIADO_FLAG:
            i["status"] = "adiada"
            i["bloqueio"] = ("mecânica diária/Mystery Gift, decisão 6 do plano "
                             "de Sinnoh (16/08/2026): batalha é polimento de "
                             "fim de projeto e Mystery Gift não existe aqui")
        elif flag.startswith("MAP_HEADER_"):
            i["status"] = "descartada"
            i["bloqueio"] = ("objeto CLONE: o campo hidden_flag da fonte guarda "
                             "o mapa de ORIGEM do clone, não uma flag. Nunca "
                             "entrou no orçamento de flags (34 casos, medido em "
                             "17/08/2026)")
        elif i["mapa_destino"] == "Villa":
            i["status"] = "adiada"
            i["bloqueio"] = ("máquina de visitantes da Villa "
                             "(VAR_RESORT_VILLA_VISITOR e afins) não existe "
                             "neste motor; adiado por mecânica, mesma categoria "
                             "da decisão 5 (retorno do S7, 18/08/2026)")
    if i["id"] in NOTA_SINNOH:
        i["nota"] = NOTA_SINNOH[i["id"]]
    return i


# ------------------------------------------------------------------- johto

def existe(simbolo, arquivos=("include/constants/items.h",
                              "include/constants/event_objects.h",
                              "include/constants/opponents.h")):
    for a in arquivos:
        p = os.path.join(REPO, a)
        if os.path.exists(p) and re.search(rf"\b{simbolo}\b", open(p).read()):
            return True
    return False


def ids_livres_johto():
    """Quanto sobra da faixa 2460-2499, que `opponents.h` reserva para Johto."""
    p = os.path.join(REPO, "include/constants/opponents.h")
    usados = {int(n) for n in re.findall(r"^#define\s+TRAINER_\w+\s+(\d+)\s*$",
                                         open(p).read(), re.M)}
    return sorted(set(range(2460, 2500)) - usados)


# A seção 6 de PENDENCIAS-JOHTO.md, item a item. `bloqueio` é RECALCULADO contra
# o repo por `fila_johto()`; o texto aqui é só o motivo escrito lá.
JOHTO = [
    dict(id="johto:arco_dos_sinos:kimono_girls", tipo="duelo", feito=True,
         mapa_destino="EcruteakCity_Theater", tamanho=5, precisa=[],
         motivo="15/08/2026: os dois sinos foram criados (875 e 876) e o "
                "desafio das cinco entrou inteiro, ids 2464-2469. Ver a secao "
                "8 do PENDENCIAS-JOHTO.md"),
    dict(id="johto:arco_dos_sinos:lugia_hooh", tipo="arco_sinos", feito=True,
         mapa_destino="TinTower_RoofDay / WhirlIslands_LugiaChamber", tamanho=5,
         precisa=[],
         motivo="15/08/2026: cadeia inteira ligada, Route39 -> EcruteakCity -> "
                "teatro -> telhado. Lendario em nivel 100"),
    dict(id="johto:duelo:eusine_suicune", tipo="duelo", feito=True,
         mapa_destino="CianwoodCity", tamanho=1, precisa=[],
         motivo="15/08/2026: SUICUNE passa e o EUSINE desafia, em CianwoodCity; "
                "TRAINER_JOHTO_EUSINE = 2462. Ver secao 7 do PENDENCIAS-JOHTO.md"),
    dict(id="johto:duelo:giovanni_celebi", tipo="duelo", feito=True,
         mapa_destino="TohjoFalls_GiovanniRoom", tamanho=1, precisa=[],
         motivo="15/08/2026: sem a CELEBI (o `special CheckCelebi` do hns nao "
                "existe aqui); o portao virou a queda do ARCHER na Torre Radio. "
                "TRAINER_JOHTO_GIOVANNI = 2463"),
    dict(id="johto:duelo:red2_mt_silver", tipo="duelo", feito=True,
         mapa_destino="MtSilver_SummitDay", tamanho=1, precisa=[],
         motivo="15/08/2026 (decisao 3 do Gui): OBJ_EVENT_GFX_RED_2 criado, "
                "arte do jogador RED de FRLG com paletteTag proprio registrado "
                "em sObjectEventSpritePalettes. TRAINER_JOHTO_RED = 2467"),
    dict(id="johto:duelo:grunt_subterraneo", tipo="duelo", feito=True,
         mapa_destino="GoldenrodCity_Underground", tamanho=1, precisa=[],
         motivo="DESCARTADO em 15/08/2026: nao existe na fonte. Varri "
                "`trainerbattle*` em todo mapa de Johto do hns; as unicas "
                "batalhas sem par aqui eram EUSINE, GIOVANNI, os tres "
                "RIVAL_*_4 e RED_2. Os nove Rockets do subterraneo de "
                "Goldenrod ja estao na ROM desde 05/08"),
    dict(id="johto:rival:4o_duelo", tipo="duelo", feito=True,
         mapa_destino="GoldenrodCity_UndergroundSwitches", tamanho=1,
         precisa=[],
         motivo="15/08/2026: o objeto de indice 6 virou o SILVER e saiu de "
                "(35,2), que e parede, para (34,3); o da cidade sai por "
                "FLAG_HIDE_SILVER_GOLDENROD, a mesma flag. Zero flag e zero "
                "var novas"),
    dict(id="johto:ginasio:whitney", tipo="setscene", feito=True,
         mapa_destino="GoldenrodCity_Gym", tamanho=1, precisa=[],
         motivo="15/08/2026: a insignia passou a sair no galho da BRIDGET, "
                "nao logo depois da batalha. Custou UMA var "
                "(VAR_JOHTO_GOLDENROD_GYM_STATE). A cena mora no gerador, em "
                "dev_scripts/porta_ginasios_johto.py, funcao cena_choro"),
    dict(id="johto:ginasio:olivine", tipo="setscene",
         mapa_destino="OlivineCity_Gym", tamanho=1, precisa=[],
         motivo="depende de VAR_OLIVINE_CITY_STATE em 5, que só o farol põe"),
    dict(id="johto:npcs:44_pares_ambiguos", tipo="portavel", feito=True,
         mapa_destino="vários", tamanho=44, precisa=[],
         motivo="18/08/2026, Fase B: o número mentia para cima. "
                "restaura_npcs_johto.py checava ambiguidade ANTES do filtro "
                "eh_pessoa, então par Pokémon-dia x Pokémon-noite na mesma "
                "coordenada (26 dos 44, BellchimeTrail/Route41) contava como "
                "pendência de gente sem nunca ter sido. Consertado no "
                "gerador (filtra pessoa antes de julgar ambíguo; desempate "
                "por flag-que-existe, mesma regra de "
                "importa_npcs_sinnoh.py). Sobraram 18 pares de gente de "
                "verdade: 16 eram WHIRLPOOL escondendo ARCHER (Route41 x12, "
                "DragonsDen_Cavern x4, mesmo `script`) e 2 eram "
                "ROCKET_M/BEAUTY em GoldenrodCity (39,14), desempatados pela "
                "flag existente FLAG_HIDE_GOLDENROD_ROCKETS. Os 18 já foram "
                "restaurados (--aplica): GoldenrodCity aponta para "
                "GoldenrodCity_EventScript_Rocket5, script daqui, feita "
                "de verdade; os 16 ARCHER viraram NPC visível de gráfico "
                "certo mas SEM FALA/BATALHA (fecho pede loadtrainer/ "
                "callasm de um boss sem id nesta fase), tarefa nova para a "
                "fila de treinador de Johto, não mais para esta linha"),
    dict(id="johto:npcs:8_sem_par", tipo="portavel", feito=True,
         mapa_destino="vários", tamanho=8, precisa=[],
         motivo="FECHADO em 18/08/2026, os 8, e nenhum virou NPC. Sete "
                "(Route26 18,8; Route28 19,19/7,16; Route29 "
                "37,11/13,21/29,18/14,10) acharam vizinho no raio 2 que NÃO é "
                "gente (berry tree, Pokémon de overworld dia/noite) e caíram "
                "em 'par não é gente'. O oitavo, LakeOfRage (49,34), fechou "
                "sem mexer no raio: LakeOfRage é cópia 1 para 1 do hns (17 "
                "objetos, mesma ordem) e esse era o ÚNICO com coordenada "
                "diferente — o par dele é o objeto 13 da fonte, "
                "MON_BASE+SPECIES_SKARMORY em (52,37), distância 3, que a "
                "importação de 05/08 gravou em (49,34). O objeto voltou para "
                "a coordenada da fonte no map.json e passou a casar no raio "
                "ZERO; alargar o censo para raio 3 teria trocado um objeto "
                "por rede maior em Johto inteira (lição do raio de Sinnoh). "
                "Censo agora: 'sem par na fonte' = 0, travado por assert no "
                "demo() do restaura_npcs_johto.py"),
    dict(id="johto:arte:4_graficos", tipo="portavel",
         mapa_destino="vários", tamanho=2, precisa=[],
         motivo="18/08/2026, Fase B, re-verificado: dos 4 originais, os dois "
                "WHIRLPOOL eram falso positivo (decoração de campo, não "
                "gente, corrigido em EXATOS_NAO_PESSOA do gerador); o "
                "ARCHER que eles escondiam já foi restaurado, ver a linha "
                "44_pares_ambiguos). Sobram só GoldenrodCity_TrainStation "
                "TRAIN_FRONT e LakeOfRage SHINY_GYARADOS, sem equivalente "
                "desenhado nesta ROM; o GYARADOS tem saída barata em "
                "OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS) mas isso é decisão "
                "de arte do Gui, não execução de cena"),
    dict(id="johto:torres_farol:18_treinadores", tipo="batalha", feito=True,
         mapa_destino="SproutTower / BurnedTower / OlivineCity_Lighthouse",
         tamanho=18, precisa=[],
         motivo="15/08/2026: os 18 JA EXISTIAM, ids 1340 a 1357, nas tres "
                "camadas (opponents.h, trainers.party e trainers_johto.party); "
                "a secao 4.1 e que estava velha. O que faltava de verdade era o "
                "raio de visao, devolvido da fonte a 17 deles (o SAGE_LI e "
                "TRAINER_TYPE_NONE na fonte tambem)"),
]


def fila_johto():
    livres = ids_livres_johto()
    itens = []
    for j in JOHTO:
        faltando = []
        for s in j["precisa"]:
            if s == "__RED_2_SPRITE__":
                faltando.append("RED_2 sem sprite próprio (decisão de arte)")
            elif s == "__IDS_JOHTO__":
                if len(livres) < j["tamanho"]:
                    faltando.append(f"faixa 2462-2499: só {len(livres)} ids livres")
            elif not existe(s):
                faltando.append(f"{s} não existe nesta ROM")
        itens.append({
            "regiao": "johto", "id": j["id"], "mapa_destino": j["mapa_destino"],
            "tipo": j["tipo"], "tem": [], "tamanho": j["tamanho"],
            "bloqueio": "; ".join(faltando) if faltando else "nenhum",
            # `feito` e escrito a mao na tabela JOHTO, e nao inferido: o que
            # fecha estes itens e cena escrita, nao par de coordenada, entao
            # nao ha proxy honesto para medir. Quem fecha um item marca aqui.
            "status": "feita" if j.get("feito") else "pendente",
            "motivo": j["motivo"],
        })
    return itens, livres


# ------------------------------------------------------- o que já foi feito

# A leva de 12/08/2026, para a fila não repropor trabalho fechado. Cada linha
# aponta a ferramenta que a fechou, que é onde se confere.
FEITAS = [
    # A leva da Galáctica de 12/08 NÃO entra aqui como memo: desde a conferência
    # de conteúdo, cada grupo de Sinnoh diz sozinho quanto dele já está no
    # map.json, e uma linha de resumo à mão só somaria em cima disso.
    dict(regiao="unova", id="unova:juniper_campea", mapa_destino="Unova (Liga)",
         tipo="batalha", tamanho=1, bloqueio="nenhum", status="feita",
         motivo="fim de Unova fechado em 12/08/2026"),
    dict(regiao="johto", id="johto:teatro_ecruteak",
         mapa_destino="EcruteakCity_DanceTheater", tipo="setscene", tamanho=1,
         bloqueio="nenhum", status="feita",
         motivo="dev_scripts/porta_cenas_johto.py, leva de 12/08/2026"),
    dict(regiao="johto", id="johto:18_heal_locations", mapa_destino="vários",
         tipo="portavel", tamanho=18, bloqueio="nenhum", status="feita",
         motivo="18 heal locations da leva de 12/08/2026"),
]


# ------------------------------------------------- fila de CONTEÚDO (não onda)

# Decisão da condutora em 18/08/2026: estes NÃO entram em onda, vão para a fila
# de conteúdo. Cada um traz o critério de aceite escrito, para a próxima sessão
# não remedir nada.
FILA_DE_CONTEUDO = [
    dict(regiao="sinnoh", id="sinnoh:placas:7_mapas_por_escala",
         mapa_destino="EternaCityCondominiums2F, FloaromaTown, "
                      "HearthomeCity_Gym, HotelGrandLake, Route205_North, "
                      "Route221, WaywardCave1F",
         tipo="portavel", tamanho=15, bloqueio="nenhum", status="pendente",
         motivo="18/08/2026: `conversor_de_coordenada` do importa_npcs_sinnoh."
                "py converte por ESCALA da caixa da matriz do Platinum, e onde "
                "o nosso layout é REDESENHO 1 para 1 a conta certa é "
                "TRANSLAÇÃO. Foi o que pôs três placas da Route 222 dentro de "
                "parede, sem nenhum vizinho andável. Estes 7 mapas passam no "
                "mesmo teste (deslocamento único provado por >= 2 warps, "
                "`deslocamento_de_warp`) e somam 15 placas JÁ GRAVADAS. Mover "
                "placa gravada é CONTEÚDO, e se mede uma a uma: o critério de "
                "aceite é o da Route 222, translação provada pelos warps MAIS "
                "tile de leitura andável e alcançável na região do mapa "
                "(conferido no map.bin, como no --demo do importador). Quem "
                "medir um mapa acrescenta o header em REDESENHO_1PARA1, move "
                "as placas dele no map.json na MESMA rodada (senão "
                "itens_escondidos_sinnoh passa a ver órfão) e escreve a "
                "medição junto"),
    dict(regiao="sinnoh", id="sinnoh:planta_provisoria:12_mapas_de_molde",
         mapa_destino="AmitySquare, StarkMountainOutside, BattleFrontier, "
                      "IronIsland, SendoffSpring, PalPark, GreatMarsh6, "
                      "Route204North, MtCoronetOutsideNorth, "
                      "MtCoronetOutsideSouth, SpringPath, TrophyGarden",
         tipo="mapa", tamanho=12, bloqueio="geometria provisória",
         status="pendente",
         motivo="MEDIDO em 18/08/2026 na onda de povoar: estes 12 mapas NÃO "
                "TÊM MAPA, têm o molde de portão 13x9. O critério é COMPARAÇÃO "
                "DE map.bin contra `data/layouts/Route226_Access/map.bin`, "
                "nunca nome de mapa: `BattleFrontier` e `IronIsland` têm "
                "`map.bin` próprio e mesmo assim são idênticos ao molde em "
                "todas as linhas menos a y=1, onde as portas são furadas (4 e "
                "2 tiles de diferença). `SendoffSpring` entrou nesta lista por "
                "esse critério e NÃO estava na lista de suspeitos de ninguém, "
                "que é a razão de o critério ser medida e não lista. É a mesma "
                "família de Amity Square e Stark Mountain Outside (seção de "
                "18/08 do PLANO-OBRAS-SINNOH), que agora tem 12 membros e não "
                "2. PRÊMIO MEDIDO esperando planta de verdade: só o "
                "`BattleFrontier` são 24 NPCs e 25 placas elegíveis da fonte, "
                "numa área de 48x47 que não cabe honestamente em 117 tiles; "
                "somando os 12, mais as 21 pedras de Rock Smash que "
                "`pedras_sinnoh.py` recusou pelo mesmo portão. CRITÉRIO DE "
                "ACEITE, e a ordem importa: GEOMETRIA REAL PRIMEIRO (layout "
                "convertido da fonte, warps casados nos dois sentidos, sem "
                "mão única), OBJETO DEPOIS, na mesma rodada, pelos geradores "
                "que já existem. Pôr objeto antes é plantar coordenada que vai "
                "ter que ser refeita"),
    dict(regiao="sinnoh", id="sinnoh:escala_nao_provada:10_mapas",
         mapa_destino="ValorLakefront, LakeValor, LakeVerity, SpearPillar, "
                      "GalacticHQ_B2F, HearthomeCityGymLeaderRoom, "
                      "VeilstoneCity_GalacticWarehouse, JubilifeCity_Flat1_F3, "
                      "MtCoronet_1F_North_Room1, MtCoronet_1F_North_Room2",
         tipo="portavel", tamanho=10, bloqueio="nenhum", status="pendente",
         motivo="18/08/2026, onda de povoar: nestes 10 a única régua de "
                "coordenada disponível é a ESCALA da caixa da matriz, que é "
                "justamente a regra que a correção da Route 222 provou errada "
                "(três placas dentro de parede). Em "
                "`MtCoronet_1F_North_Room2` a caixa da matriz mede 1x1 e a "
                "conta joga TODOS os eventos em (0,0), o que mostra o tamanho "
                "do erro. O gerador passou a RECUSAR escala em mapa que nasce "
                "agora, e por isso eles ficam vazios de propósito, somando 39 "
                "pedras e algumas dezenas de objetos e placas não escritos. "
                "CRITÉRIO DE ACEITE, um mapa por vez: achar régua PROVADA para "
                "aquele mapa (translação com deslocamento único provado por "
                ">= 2 warps, ou conversão 1 para 1 do blockdata com acordo de "
                "máscara medido, como os 100% de Mt Coronet), e só então "
                "rodar o gerador com cada objeto conferido no map.bin "
                "(andável e alcançável para gente, tile de leitura para "
                "placa, portão de tranca para pedra)"),
    dict(regiao="johto", id="johto:gyarados:passeio_2x2",
         mapa_destino="LakeOfRage", tipo="portavel", tamanho=1,
         bloqueio="nenhum", status="pendente",
         motivo="DÍVIDA DE FIDELIDADE assumida em 18/08/2026, não descuido: o "
                "GYARADOS vermelho de (32,28) ficou com MOVEMENT_TYPE_NONE, e "
                "a fonte usa MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_UP_DOWN_LEFT "
                "(passeio num quadrado de 2x2). Parado, o tile é fixo e o "
                "T107.4 pode mirar a interação; com o passeio, o bicho está "
                "numa de quatro casas conforme o instante em que o jogador "
                "chega. Devolver o passeio exige reescrever a prova para "
                "mirar as QUATRO casas (ou provar a batalha sem depender da "
                "posição); enquanto isso não existir, determinismo vale mais, "
                "porque o passeio é decorativo"),
    dict(regiao="johto", id="johto:sprite_de_bola_em_quem_nao_e_bola",
         mapa_destino="Johto inteira (54 mapas têm bola de verdade; o estrago "
                      "é bem maior e se mede pelo gfx, não pela lista)",
         tipo="arte_de_campo", tamanho=1211, bloqueio="nenhum",
         status="pendente",
         motivo="ACHADO DO J2, 18/08/2026, e é o mais caro da onda de janela "
                "aberta: o jogador vê BOLA DE ITEM onde a fonte tem outra "
                "coisa. `dev_scripts/sanitize_johto_map_json.py` achatou TODO "
                "object event de Johto em OBJ_EVENT_GFX_ITEM_BALL mudo, e o "
                "`restaura_npcs_johto.py` só devolveu os que eram GENTE. "
                "MEDIÇÃO de 18/08/2026, refeita pelo J7 depois do J2 aplicar: "
                "1212 object events de Johto ainda têm gfx de item ball com "
                "`flag: 0`, `script: \"0\"` e `trainer_sight_or_berry_tree_id: "
                "0`, e desses só UM é bola de verdade (a GS Ball da linha "
                "abaixo). Ou seja 1211 são impostores. Cruzando por "
                "coordenada exata com a fonte `fontes-mapas/hns`, 1364 dos "
                "1372 achatados originais casaram e só 161 eram bola (98 "
                "OBJ_EVENT_GFX_POKE_BALL mais 63 OBJ_EVENT_GFX_ITEM_BALL); o "
                "resto é efeito de luz (219), pedra de Rock Smash, canteiro "
                "de berry, Pokémon de overworld e NPC. CRITÉRIO DE ACEITE: "
                "devolver o graphics_id que a FONTE diz, com a MESMA prova de "
                "coordenada que o J2 usou (casar (mapa, x, y) exato contra o "
                "objeto da fonte, nunca por escala nem por vizinhança), o "
                "conserto morando no gerador e não no map.json, e o censo do "
                "que entrou gravado como `dev_scripts/bolas_johto.json` fez "
                "para as bolas. Esse arquivo é o ponteiro: ele lista as 161 "
                "que a fonte prova serem bola, e portanto define por exclusão "
                "quem NÃO pode continuar com sprite de bola. Cuidado medido: "
                "objeto que deixa de ser bola muda de tamanho de sprite e "
                "pode passar a bloquear passagem, então a prova de cada leva "
                "inclui o tile andável, como no --demo do importador"),
    dict(regiao="johto", id="johto:bolas:2_de_olivine_faltando",
         mapa_destino="OlivineCity (53,47) e OlivineCity_Lighthouse (125,15)",
         tipo="arte_de_campo", tamanho=2, bloqueio="nenhum", status="pendente",
         motivo="18/08/2026, J2: são bolas GENUÍNAS da fonte que não casaram "
                "por coordenada com nenhum objeto nosso, ou seja não estão "
                "achatadas, estão AUSENTES. As duas rodam "
                "`OlivineCity_EventScript_Item_Shockwave` na fonte (o TM de "
                "Shock Wave). Ficaram fora do bloco J2 porque ele só devolve "
                "script, item e flag a objeto que JÁ existe: criar objeto "
                "novo é conteúdo, e conteúdo se mede um a um. CRITÉRIO DE "
                "ACEITE: criar os dois object events com "
                "Common_EventScript_FindItem, item da fonte e uma flag nova "
                "em append no bloco do liga_bolas_johto.py (a faixa tem teto "
                "em FLAG_SOBRA_ITEM_BALLS_START e ainda sobram vagas), mais a "
                "prova de que o tile é alcançável"),
    dict(regiao="johto", id="johto:gs_ball:ruins_of_alph",
         mapa_destino="RuinsOfAlph_B1F (5,4)", tipo="arte_de_campo", tamanho=1,
         bloqueio="ITEM_GS_BALL não existe no expansion", status="pendente",
         motivo="18/08/2026, J2: a 161ª bola de Johto que a fonte prova, e a "
                "única que ficou de fora das 160 gravadas. Está declarada em "
                "`FORA` no dev_scripts/liga_bolas_johto.py, não esquecida. "
                "Escolher outra bola no lugar mudaria conteúdo e inventar "
                "item é outra obra, então isto espera decisão: ou nasce "
                "ITEM_GS_BALL de verdade (com gráfico, texto e o gancho da "
                "cena do Celebi), ou o objeto sai do mapa. CRITÉRIO DE "
                "ACEITE: qualquer um dos dois caminhos, escrito antes de "
                "mexer, e o objeto deixando de ser bola muda de sprite pela "
                "mesma prova de coordenada da linha de cima"),
    dict(regiao="johto", id="johto:flags:day_night_pokemon_em_special_flags",
         mapa_destino="GoldenrodCity_UndergroundTunnel, "
                      "GoldenrodCity_DepartmentStore_5F",
         tipo="divida_tecnica", tamanho=2,
         bloqueio="nenhum",
         status="feita",
         motivo="FEITA no J8, 18/08/2026, linha a linha do critério de aceite: "
                "(1) FLAG_NIGHT_POKEMON foi para FLAG_UNUSED_0x1D01 e "
                "FLAG_DAY_POKEMON para FLAG_UNUSED_0x1D02, no TRANSBORDO DE "
                "JOHTO 0x1D00-0x1D3F e não na reserva do J1: as duas escondem "
                "object event de Johto, exatamente como "
                "FLAG_HIDE_LAKE_OF_RAGE_GYARADOS que já mora em 0x1D00, e a "
                "reserva do J1 nasceu dimensionada para Galar e Wild Area. "
                "Apelidar FLAG_UNUSED que já existe não mexe em FLAGS_COUNT, "
                "então o tamanho da save NÃO mudou por causa desta linha; "
                "(2) o stub `#ifndef` sumiu, e junto com ele FLAG_HIDE_RAYQUAZA "
                "0x4002, que era a mesma armadilha sem nenhum uso medido em "
                "data/, src/, include/ e test/. Para a classe não voltar, o "
                "portão passou a REPROVAR qualquer `#ifndef FLAG_`/`#ifndef "
                "VAR_` nos headers do perfil, com passo de mutação plantada no "
                "`--demo`; (3) o portão de flags voltou a 1 grupo (só o 0x1F4) "
                "e (4) dev_scripts/colisoes_flags_autorizadas.json perdeu as "
                "duas linhas de DEFEITO VIVO. Os 3 usos em map.json NÃO "
                "mudaram, porque referenciam o NOME. Prova na suíte: caso 111, "
                "com par negativo acendendo FLAG_HIDE_MAP_NAME_POPUP. "
                "ACHADO ORIGINAL DO J7 em 18/08/2026 ao estender o portão de colisão "
                "para flags (`dev_scripts/guarda_colisao_vars.py --flags`), "
                "medido e NÃO consertado por ordem do condutor. O import de "
                "Johto deixou um stub em include/constants/flags.h:8192, "
                "`#ifndef FLAG_NIGHT_POKEMON / #define FLAG_NIGHT_POKEMON "
                "0x4000` (e FLAG_DAY_POKEMON 0x4001), que cai exatamente em "
                "cima de FLAG_HIDE_MAP_NAME_POPUP (SPECIAL_FLAGS_START + 0x0, "
                "citada em 17 arquivos) e FLAG_DONT_TRANSITION_MUSIC "
                "(SPECIAL_FLAGS_START + 0x1, 9 arquivos). As duas do stub "
                "estão VIVAS no campo `flag` de object events em "
                "data/maps/GoldenrodCity_UndergroundTunnel/map.json:54 e :67 "
                "e data/maps/GoldenrodCity_DepartmentStore_5F/map.json:28, "
                "então o Pokémon de dia e o de noite somem do mapa sempre que "
                "o motor acende a flag dele, e um `removeobject` neles "
                "acenderia a flag do motor. Pior: 0x4000 em diante é "
                "SPECIAL_FLAGS, que mora na EWRAM e NÃO persiste, ou seja o "
                "endereço está errado também como flag de objeto. CRITÉRIO DE "
                "ACEITE: as duas ganham endereço próprio na reserva do J1 "
                "(FLAG_SOBRA_ITEM_BALLS_START ou FLAG_RESERVA_CONTEUDO_START), "
                "o stub `#ifndef` some, o portão de flags volta a 1 grupo "
                "declarado (só o 0x1F4, que é desenho do pokeemerald) e a "
                "lista dev_scripts/colisoes_flags_autorizadas.json perde as "
                "duas linhas de DEFEITO VIVO"),
    dict(regiao="motor", id="motor:portao_colisao:headers_de_config",
         mapa_destino="include/config/text.h:17, include/config/item.h:39",
         tipo="ferramenta", tamanho=2, bloqueio="nenhum", status="pendente",
         motivo="SOBRA DO J9, 18/08/2026, medida e NÃO consertada porque hoje "
                "não há colisão: o portão dev_scripts/guarda_colisao_vars.py "
                "só lê os headers do PERFIL (constants/flags.h, flags_frlg.h, "
                "constants/vars.h, vars_frlg.h), e include/config/*.h define "
                "flag e var FORA do alcance dele. Hoje são duas, as duas "
                "valendo 0, que é o valor de 'desligado' e não endereço: "
                "FLAG_TEXT_SPEED_INSTANT (text.h:17) e VAR_LAST_REPEL_LURE_USED "
                "(item.h:39). Zero colisão em 18/08/2026, e é por isso que a "
                "linha é DÍVIDA e não defeito. O risco é o dia em que alguém "
                "ligar uma delas: quem escrever `#define FLAG_TEXT_SPEED_"
                "INSTANT FLAG_UNUSED_0x1D10` num header que o portão não lê "
                "recria exatamente a colisão calada que a onda inteira "
                "existiu para matar. Junto vale o aviso do ESTADO 0.f: "
                "P_FLAG_FORCE_SHINY aponta para FLAG_TEMP_7 e mora na mesma "
                "cegueira. CRITÉRIO DE ACEITE: os headers de include/config/ "
                "que definem FLAG_/VAR_ entram nos PERFIS do portão, na ordem "
                "do include, e o --demo ganha um passo plantando alocação de "
                "config em cima de flag viva"),
    dict(regiao="motor", id="motor:portao_colisao:mascara_de_bit_com_nome_de_flag",
         mapa_destino="include/constants/battle_frontier.h:131",
         tipo="ferramenta", tamanho=1, bloqueio="nenhum", status="pendente",
         motivo="SOBRA DO J9, 18/08/2026. FLAG_FRONTIER_MON_FACTORY é `(1 << "
                "0)`, o mesmo número de FLAG_TEMP_1, e as duas são usadas "
                "(src/battle_factory.c, src/battle_frontier.c, src/battle_"
                "factory_screen.c de um lado; src/field_control_avatar.c, "
                "src/debug.c e data/maps/TwoIsland_House_Frlg/scripts.inc do "
                "outro). O portão não pega, e neste caso NÃO PEGAR ESTÁ CERTO: "
                "aquele `(1 << 0)` é máscara de bit de CreateFacilityMonFlags, "
                "não endereço de flag de save, e os dois nomes vivem em "
                "espaços diferentes. Fica escrito porque o perigo é humano, "
                "não do motor: o prefixo FLAG_ num arquivo que não é de flag "
                "convida alguém a passar essa constante para FlagSet(). "
                "CRITÉRIO DE ACEITE: ou o nome ganha prefixo próprio "
                "(F_FRONTIER_MON_FACTORY, que é a convenção dos vizinhos "
                "F_EV_SPREAD_* do mesmo arquivo), ou fica como está e esta "
                "linha vira 'aceito, não mexer'. É renomeação de constante de "
                "motor, portanto decisão do condutor"),
    dict(regiao="motor", id="motor:worktrees_velhas_com_stub",
         mapa_destino=".claude/worktrees/cool-liskov-5a5d35, "
                      ".claude/worktrees/friendly-hawking-e6b67e",
         tipo="ferramenta", tamanho=2, bloqueio="nenhum", status="pendente",
         motivo="AVISO DO J9, 18/08/2026, e é AVISO e não tarefa: as duas "
                "worktrees velhas (bde2d3216a e 20ac2eaac4) ainda têm o stub "
                "`#ifndef FLAG_HIDE_RAYQUAZA / #define FLAG_HIDE_RAYQUAZA "
                "0x4002` que o J8 matou na árvore principal (flags.h:2481 e "
                ":5049). O portão não as lê, porque RAIZES_DE_USO é "
                "data/src/include/test da RAIZ, e está certo assim: worktree "
                "é foto de um commit passado e reescrevê-la seria falsificar "
                "história. O que importa saber é que build feita DE DENTRO "
                "delas continua com o defeito. NÃO MEXER; se a worktree for "
                "reaproveitada para trabalho novo, ela primeiro puxa a "
                "árvore principal"),
]


# --------------------------------------------------------------------- main

def gera():
    unova, chamadas = fila_unova()
    sinnoh = fila_sinnoh()
    johto, livres = fila_johto()
    itens = (unova + sinnoh + johto
             + [dict(tem=[], **f) for f in FEITAS + FILA_DE_CONTEUDO])
    return itens, chamadas, livres


def resumo(itens, chamadas, livres):
    print(f"{'região':8} {'tipo':20} {'pend.':>6} {'feitas':>6} "
          f"{'descart':>8} {'adiadas':>8} {'linhas':>8}")
    conta = collections.Counter()
    for i in itens:
        conta[(i["regiao"], i["tipo"], i["status"])] += 1
    tam = collections.Counter()
    for i in itens:
        tam[(i["regiao"], i["tipo"])] += i["tamanho"]
    for reg, tipo in sorted({(r, t) for r, t, _ in conta}):
        print(f"{reg:8} {tipo:20} {conta[(reg, tipo, 'pendente')]:6} "
              f"{conta[(reg, tipo, 'feita')]:6} "
              f"{conta[(reg, tipo, 'descartada')]:8} "
              f"{conta[(reg, tipo, 'adiada')]:8} {tam[(reg, tipo)]:8}")
    pend = [i for i in itens if i["status"] == "pendente"]
    print(f"\npendentes: {len(pend)}   sem bloqueio: "
          f"{sum(1 for i in pend if i['bloqueio'] == 'nenhum')}")
    print(f"conferência de conteúdo de Sinnoh medida com raio {raio()} tiles")
    print("chamadas alcançadas em Unova:", dict(chamadas))
    print(f"ids de treinador livres na faixa 2460-2499: {len(livres)} "
          f"({livres[0]}-{livres[-1]})" if livres else "faixa 2460-2499 cheia")


def grava(itens):
    linhas = ",\n".join(json.dumps(i, ensure_ascii=False, sort_keys=True)
                        for i in itens)
    open(SAIDA, "w", encoding="utf-8").write("[\n" + linhas + "\n]\n")
    print("escrito:", SAIDA, f"({len(itens)} linhas)")


def demo():
    """Autoteste: o que quebraria calado se a travessia parasse de andar."""
    corpos, std, seguinte = indice_de_rotulos()
    assert len(corpos) > 20000, len(corpos)
    assert std, "std_scripts.asm não foi lido; jumpstd morreria calado"

    unova, chamadas = fila_unova()
    assert len(unova) == 209, f"cenas de Unova: {len(unova)} (esperado 209)"
    # Conferência de conteúdo de Unova: os atalhos do CasteliaGym saíram desta
    # fila como "sem bloqueio" e já foram executados; se voltarem a pendente, a
    # leitura de `coord_events` do map.json quebrou.
    gym = [i for i in unova if i["mapa_destino"] == "Unova_CasteliaGym"]
    assert gym and any(i["status"] == "feita" for i in gym), gym
    # A trava do fallthrough: estas quatro saíram como "portavel, sem bloqueio" e
    # são cutscene inteira uma casa abaixo do rótulo. Se qualquer uma voltar a
    # ficar sem bloqueio, `termina()`/`TERMINADORES` regrediu.
    escorrem = ("DragonspiralTower6F.asm:DragonspiralTowerInferScript1@2,13",
                "PlayersHouse1F.asm:MeetMomLeftScript@8,4",
                "NacreneCity.asm:NacreneCityLenoraScript4@0,11",
                "OpelucidCity.asm:OpelucidCityIrisScript3@40,27")
    for alvo in escorrem:
        i = next(x for x in unova if x["id"] == alvo)
        assert i["bloqueio"] != "nenhum", f"fallthrough perdido em {alvo}: {i}"
    # A trava do bug que este arquivo existe para não repetir: sem seguir a
    # cadeia, `callasm` aparece 8 vezes em 5 arquivos e a fila diria 8.
    ca = sum(1 for i in unova if "callasm" in i["tem"])
    assert ca == 16, f"cenas que chegam a callasm: {ca} (esperado 16)"
    # 108, e não os 107 de PLANO-UNOVA.md: a 108ª só aparece quando o corpo
    # escorre para o rótulo de baixo. O documento foi medido sem fallthrough.
    cb = sum(1 for i in unova if "changeblock" in i["tem"])
    assert cb == 108, f"cenas de changeblock: {cb} (esperado 108)"
    assert chamadas["changeblock"] > 1000, chamadas["changeblock"]

    sinnoh = fila_sinnoh()
    obj = sum(i["objetos_fonte"] for i in sinnoh if i["tipo"] == "hidden_flag")
    tri = sum(i["objetos_fonte"] for i in sinnoh if i["tipo"] == "coord_event")
    assert obj == 371, f"objetos com hidden_flag na fonte: {obj} (esperado 371)"
    assert tri == 177, f"coord_events na fonte: {tri} (esperado 177)"
    assert all(i["tamanho"] <= i["objetos_fonte"] for i in sinnoh), \
        "faltando maior que o total: o casamento 1:1 furou"
    # A trava do proxy que este critério substituiu: os 5 grunts do QG do 3F
    # existem no map.json (leva c7c8b4a201) e o casamento tem de vê-los.
    qg = [i for i in sinnoh if i["id"].startswith("GalacticHQ_3F:FLAG_HIDE")]
    assert qg and qg[0]["tamanho"] < qg[0]["objetos_fonte"], \
        f"conferência de conteúdo não achou os grunts já plantados: {qg}"

    # Item de QA de 17/08/2026: esqueleto NÃO é cena. Se `rotulos_com_cena`
    # regredir, os gatilhos que `maquina_sinnoh.py` plantou voltam a contar
    # como feitos e a fila para de cobrar as cenas deles. Os dois rótulos são
    # do mesmo arquivo e nenhum dos dois é fotografia de contagem.
    reais = rotulos_com_cena("PastoriaCity_Gym")
    assert "PastoriaCity_Gym_EventScript_Leader" in reais, \
        "cena de verdade lida como esqueleto"
    assert "PastoriaCity_Gym_EventScript_BlueButton" not in reais, \
        "rótulo com `end` sozinho passou por cena"
    # E as decisões datadas têm de aparecer: se a tabela deixar de ser
    # aplicada, os 34 clones e os 27 do Amity voltam a cobrar trabalho.
    for st in ("descartada", "adiada"):
        assert any(i["status"] == st for i in sinnoh), \
            f"nenhuma linha de Sinnoh saiu como {st}: DECIDIDO_SINNOH não rodou"

    johto, livres = fila_johto()
    # ponytail: invariante, não fotografia. A faixa esvazia enquanto o executor
    # trabalha (2462 e 2463 viraram EUSINE e GIOVANNI durante esta sessão), e
    # cravar o número do dia faria o autoteste quebrar por trabalho alheio.
    assert livres and set(livres) <= set(range(2460, 2500)), livres
    # ponytail: invariante, não fotografia. A versão anterior cravava "os sinos
    # bloqueiam", e reprovou no dia em que os sinos foram criados (ITEM_TIDAL_BELL
    # e ITEM_CLEAR_BELL, ids 875 e 876). O que tem de valer sempre é outra coisa:
    # o bloqueio escrito na fila CONCORDA com o que `include/` diz. Se o símbolo
    # existe, ele não pode aparecer como bloqueio; se não existe, tem de aparecer.
    for simbolo in ("ITEM_TIDAL_BELL", "ITEM_CLEAR_BELL"):
        citado = any(simbolo in i["bloqueio"] for i in johto)
        assert citado != existe(simbolo), \
            f"{simbolo}: existe={existe(simbolo)} mas a fila diz citado={citado}"
    print("demo ok:", len(unova), "cenas de Unova,", len(sinnoh),
          "unidades de Sinnoh,", len(johto), "itens de Johto")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        itens, chamadas, livres = gera()
        resumo(itens, chamadas, livres)
        if "--gravar" in sys.argv:
            grava(itens)
        else:
            print("\nnada escrito (use --gravar)")
