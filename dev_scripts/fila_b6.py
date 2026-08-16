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
                                         header, matriz)
        do_hack = d.get("object_events") or []
        coords_hack = [(int(c.get("x", 0)), int(c.get("y", 0)))
                       for c in (d.get("coord_events") or [])]

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
    return itens


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
    dict(id="johto:npcs:44_pares_ambiguos", tipo="portavel",
         mapa_destino="vários", tamanho=44, precisa=[],
         motivo="duas coisas da fonte na mesma coordenada; restaura_npcs_johto.py "
                "recusa de propósito, resolver exige tabela à mão"),
    dict(id="johto:npcs:8_sem_par", tipo="portavel",
         mapa_destino="vários", tamanho=8, precisa=[],
         motivo="sem par na fonte; mesma tabela à mão"),
    dict(id="johto:arte:4_graficos", tipo="portavel",
         mapa_destino="vários", tamanho=4, precisa=[],
         motivo="TRAIN_FRONT, SHINY_GYARADOS e dois WHIRLPOOL; o GYARADOS tem "
                "saída barata em OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS)"),
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


# --------------------------------------------------------------------- main

def gera():
    unova, chamadas = fila_unova()
    sinnoh = fila_sinnoh()
    johto, livres = fila_johto()
    itens = unova + sinnoh + johto + [dict(tem=[], **f) for f in FEITAS]
    return itens, chamadas, livres


def resumo(itens, chamadas, livres):
    print(f"{'região':8} {'tipo':20} {'pend.':>6} {'feitas':>6} {'linhas':>8}")
    conta = collections.Counter()
    for i in itens:
        conta[(i["regiao"], i["tipo"], i["status"])] += 1
    tam = collections.Counter()
    for i in itens:
        tam[(i["regiao"], i["tipo"])] += i["tamanho"]
    for reg, tipo in sorted({(r, t) for r, t, _ in conta}):
        print(f"{reg:8} {tipo:20} {conta[(reg, tipo, 'pendente')]:6} "
              f"{conta[(reg, tipo, 'feita')]:6} {tam[(reg, tipo)]:8}")
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
