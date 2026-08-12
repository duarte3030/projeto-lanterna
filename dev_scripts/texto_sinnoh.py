#!/usr/bin/env python3
"""Tira do mudo os NPC de Sinnoh e da texto proprio as placas importadas.

Continua a corrente que `texto_placas_sinnoh.py` ja percorria, e conserta o elo
fraco dela. O texto NUNCA e escrito aqui: sai inteiro do pokeplatinum.

    events_<mapa>.json    objeto com "script": N
    scripts_<mapa>.s      N-esimo `ScriptEntry` da lista do topo do arquivo
    corpo do rotulo       `Message X` / `NPCMessage X` / `ShowLandmarkSign X`
    res/text/<mapa>.json  mensagem de id X, em en_US

O elo fraco e ligar o NOSSO evento ao evento DELES: o importador
(`importa_npcs_sinnoh.py`) nao gravou o indice de origem, so a marca
`"origem": "pokeplatinum"`. Sobra a ORDEM, e a ordem so vale se nada tiver sido
descartado no meio. Por isso:

- **NPC**: so casa mapa onde a contagem bate E o `graphics_id` de cada um bate,
  um a um, contra o que o importador teria escrito (`TROCA_SPRITE`). Sprite
  diferente em qualquer posicao reprova o mapa inteiro. E a mesma politica
  conservadora da ferramenta de placa: fala trocada e pior que NPC mudo.
- **Placa**: so casa mapa onde a contagem bate. A ordem la e
  `object_events` com grafico de placa, depois `bg_events`, que e exatamente a
  ordem em que o importador gravou.

**Item escondido nao ganha texto.** No Platinum placa e item escondido moram no
MESMO array `bg_events` e so se distinguem pela faixa do `script`: abaixo de
2500 e placa, 8000 a 8799 e `SCRIPT_ID_OFFSET_HIDDEN_ITEMS`, acima disso e
Safari/Chatot. O importador copiou os tres como placa. Escrever fala para um
item escondido e trabalho jogado fora, entao eles ficam com o rotulo generico e
saem listados em `--itens`, com o item que a fonte diz que deveria estar no
chao. Virar item de verdade custa uma flag por item e depende do dono do
projeto (decisao 13 do ESTADO.md).

**Teto conhecido, criado em 11/08/2026 e nao consertado de proposito:**
`dev_scripts/itens_escondidos_sinnoh.py` resolveu esses 146 (50 viraram item
escondido, 96 foram apagados), e apagar bg_event DESALINHA a contagem que este
arquivo usa para casar placa com placa. Nos 53 mapas que ele tocou,
`len(n_placas) == len(f_placas)` deixa de valer, entao eles passam a cair em
`placa_mapa_pulado` e nao recebem texto novo de placa. O texto de placa daqueles
mapas ja foi aplicado antes (229 placas, na leva de 11/08), entao a perda e de
capacidade futura, nao de conteudo. Quem precisar reabrir esses mapas tem que
gravar o indice de origem no proprio evento em vez de depender da ordem.

Uso:
    python3 dev_scripts/texto_sinnoh.py            # so relata
    python3 dev_scripts/texto_sinnoh.py --itens    # lista os itens escondidos
    python3 dev_scripts/texto_sinnoh.py --aplica
    python3 dev_scripts/texto_sinnoh.py --demo
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAT = os.path.join(os.path.dirname(REPO), "fontes-mapas/pokeplatinum")
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I  # noqa: E402
import valida_mapas_sinnoh as V  # noqa: E402
from texto_placas_sinnoh import (campos_do_header, entradas_de_script,  # noqa: E402
                                 banco_de_texto, para_gba)

GENERICO = I.SCRIPT_PLACA
APLICA = "--aplica" in sys.argv

# Faixas do campo `script` de um bg_event do Platinum (include/script_manager.h).
ITEM_ESCONDIDO = range(8000, 8800)

# Todo comando do Platinum que poe texto na tela. O primeiro argumento e o id da
# mensagem, menos em PokemonCryAndMessage, onde e a especie.
MOSTRA = re.compile(
    r"^(Message|NPCMessage|EventMessage|MessageAndWaitButton|MessageSynchronized"
    r"|MessageInstant|MessageNoSkip|UndergroundNPCMessage"
    r"|ShowLandmarkSign|ShowArrowSign|ShowScrollingSign|ShowMapSign)\s+(\w+)")
CRY = re.compile(r"^PokemonCryAndMessage\s+\w+,\s*(\w+)")
GOTO = re.compile(r"^GoTo\s+(\w+)\s*$")
BUFFER = re.compile(r"^Buffer(\w+)\s+(\d+)(?:\s*,\s*([^\s,]+))?")


def texto_do_rotulo(corpos, rot, visto=None):
    """(id da mensagem, buffers) do primeiro texto do caminho de fall-through.

    Desvio condicional (`GoToIfSet`, `GoToIfEq`, ...) e ignorado de proposito: o
    que queremos e a fala padrao, a que o jogador ouve sem gatilho nenhum. So
    `GoTo` cru, que e incondicional, e seguido.

    `buffers` ACUMULA ao longo do caminho: `{N: (tipo, argumento)}`. A primeira
    versao zerava o dicionario a cada rotulo, e por isso perdia o buffer posto
    ANTES de um `GoTo` (`PalParkLobby_Daughter` enche o 0 com `BufferPlayerName`
    e so entao desvia). O texto chegava com um `{STRVAR}` sem dono e era
    reprovado inteiro, ou seja, o NPC ficava mudo por um defeito nosso.
    """
    visto = visto or set()
    buffers = {}
    while rot and rot not in visto:
        visto.add(rot)
        prox = None
        for linha in corpos.get(rot, []):
            b = BUFFER.match(linha)
            if b:
                buffers[int(b.group(2))] = (b.group(1), b.group(3))
                continue
            m = MOSTRA.match(linha) or CRY.match(linha)
            if m:
                return m.group(m.lastindex), buffers
            g = GOTO.match(linha)
            if g:
                prox = g.group(1)
                break
        rot = prox
    return None, {}


# `{STRVAR_1 3, N, 0}` e o conteudo do buffer N.
#
# `{RIVAL}` do pokeemerald e o rival de HOENN, e Barry nao e ele: `RivalName` e
# `CounterpartName` continuam reprovando o texto inteiro. O que ganhou
# equivalente honesto aqui e o que o expansion sabe encher com UM comando antes
# do `msgbox` (`asm/macros/event.inc`), e nada mais.
#
# Ceiling assumido, de proposito: `PartyMonSpecies` vira o LIDER do time.
# O Platinum le o slot de uma var que o caminho padrao nunca escreve, ou seja,
# 0, que e o lider; num caminho que a escolha do jogador tivesse mexido, a fala
# nomearia outro bicho. Sao quatro NPC de sabor ("Oh, your X..."), e errar o
# apelido ali nao muda nada do jogo.
STRVAR = re.compile(r"\{STRVAR_\d+ \d+, (\d+), \d+\}")

# tipo do Buffer do Platinum -> (o que vai no texto, comando que enche a var).
# `{N}` no comando e trocado pelo numero da STR_VAR.
BUFFER_EQUIV = {
    "PlayerName": ("{PLAYER}", None),
    "PartyMonSpecies": ("{STR_VAR_%d}", "bufferleadmonspeciesname STR_VAR_%d"),
    "PartyMonNickname": ("{STR_VAR_%d}", "bufferpartymonnick STR_VAR_%d, 0"),
    "ItemName": ("{STR_VAR_%d}", "bufferitemname STR_VAR_%d, %s"),
}

# `♫` e `♪` nao existem no charmap do GBA (o preproc recusa o arquivo inteiro
# com "unexpected character"). O repo ja tem o simbolo, com outro nome:
# `EMOJI_NOTE` (charmap.txt:1109), usado em `src/text_input_strings.c:63`.
NOTA = re.compile(r"[♫♪]")

# `'$' = FF` no charmap.txt: o cifrao NAO desenha dinheiro, ELE TERMINA A
# STRING. Deixar passar cortou seis falas no meio antes desta guarda existir
# ("Moomoo Milk, $500 a bottle" virou "Moomoo Milk, "). O simbolo de dinheiro
# desta ROM e `¥` (`src/strings.c:242`, `gText_PokedollarVar1`).
DINHEIRO = re.compile(r"\$(?=[0-9])")


def desenhaveis():
    """Os caracteres que o `charmap.txt` desta build sabe virar byte.

    O banco do DS tem sinal que o GBA nunca teve. A nota musical de
    `OreburghCity_Text_MachopCryChopChopMachop` ("Chop, chop away on rocks! ~♫")
    e um caractere so em 791 linhas, e ela bastaria para o preproc recusar o
    arquivo com "unexpected character". Quem decide e o charmap, nao uma lista
    minha de acentos.
    """
    global _CHARS
    try:
        return _CHARS
    except NameError:
        pass
    _CHARS = set()
    with open(os.path.join(REPO, "charmap.txt"), encoding="utf-8") as f:
        for linha in f:
            # O apostrofo aparece escapado (`'\''  = B4`), e ele sozinho esta em
            # 674 das 790 falas: regex que so aceita `'X'` reprovaria quase
            # tudo, calada, na segunda passada.
            m = re.match(r"^'(\\?.)'\s*=", linha)
            if m:
                _CHARS.add(m.group(1)[-1])
    return _CHARS


ITEM_CONST = re.compile(r"^ITEM_[A-Z0-9_]+$")


def itens_desta_rom():
    """Todo `ITEM_*` que o enum desta ROM define. Nome que nao existe reprova."""
    global _ITENS_ROM
    try:
        return _ITENS_ROM
    except NameError:
        txt = open(os.path.join(REPO, "include/constants/items.h"),
                   encoding="utf-8", errors="replace").read()
        _ITENS_ROM = set(re.findall(r"\b(ITEM_[A-Z0-9_]+)\b", txt))
        return _ITENS_ROM


def resolve(linhas, buffers):
    """(texto pronto para `.string`, comandos de buffer), ou (None, []).

    O segundo item da tupla e o que o script precisa rodar ANTES do `msgbox`
    para as `{STR_VAR_n}` terem conteudo. Texto sem buffer devolve lista vazia,
    que e o caso de 780 das 790 falas.
    """
    if isinstance(linhas, str):
        linhas = [linhas]
    saida, comandos, usados = [], [], {}
    falhou = False

    def troca(m):
        nonlocal falhou
        n = int(m.group(1))
        tipo, arg = buffers.get(n) or (None, None)
        eq = BUFFER_EQUIV.get(tipo)
        if not eq:
            falhou = True
            return "\x00"
        molde, cmd = eq
        if cmd is None:
            return molde
        if n not in usados:
            if "%s" in cmd:
                if not (arg and ITEM_CONST.match(arg) and arg in itens_desta_rom()):
                    falhou = True
                    return "\x00"
                cmd = cmd.replace("%s", arg)
            usados[n] = len(usados) + 1
            comandos.append(cmd % usados[n])
        return molde % usados[n]

    for t in linhas:
        t = STRVAR.sub(troca, t)
        # {SIZE 200}, {COLOR ...} e afins nao existem no motor do GBA.
        t = re.sub(r"\{(SIZE|COLOR|CLEAR|SET_FONT)[^}]*\}", "", t)
        t = NOTA.sub("{EMOJI_NOTE}", t)
        t = DINHEIRO.sub("¥", t)
        if "$" in t:                      # cifrao solto continua sendo terminador
            return None, []
        if "\x00" in t or falhou or \
                re.search(r"\{(?!PLAYER\}|STR_VAR_\d\}|EMOJI_NOTE\})", t):
            return None, []
        saida.append(t)
    pronto = para_gba(saida)
    # O charmap so julga o que vira BYTE DE LETRA. `{PLAYER}` e `{EMOJI_NOTE}`
    # sao codigo de controle e saem da conta inteiros: deixar o `_` deles na
    # lista de permitidos abriria a porta para underline de verdade no texto.
    ok = desenhaveis() | set("\\$")
    nu = re.sub(r"\{[^}]*\}", "", pronto)
    return (pronto, comandos) if all(c in ok for c in nu) else (None, [])


def sprite_esperado(e, sprites):
    g = e.get("graphics_id", "")
    return g if g in sprites else V.TROCA_SPRITE.get(g, V.SPRITE_PADRAO)


RAIO = 8            # o mesmo raio de busca de `importa_npcs_sinnoh.livre`


def _layouts():
    global _LAY
    try:
        return _LAY
    except NameError:
        _LAY = {l["id"]: l for l in json.load(open(
            os.path.join(REPO, "data/layouts/layouts.json"),
            encoding="utf-8"))["layouts"]}
        return _LAY


def subsequencias(fonte_conv, nossos, limite=64):
    """Todo casamento ordem-preservante fonte->nosso com grafico e raio ok.

    Mais de um casamento ja reprova o mapa, entao a busca para em `limite`.
    """
    saida = []

    def anda(i, j, escolhido):
        if len(saida) >= limite:
            return
        if j == len(nossos):
            saida.append(tuple(escolhido))
            return
        if len(fonte_conv) - i < len(nossos) - j:
            return
        _e, (fx, fy), g = fonte_conv[i]
        _, nosso = nossos[j]
        if g == nosso.get("graphics_id") and \
                max(abs(fx - nosso.get("x", 0)), abs(fy - nosso.get("y", 0))) <= RAIO:
            anda(i + 1, j + 1, escolhido + [i])
        anda(i + 1, j, escolhido)

    anda(0, 0, [])
    return saida


def alinha_npcs(header, matriz, fonte, d, sprites):
    """({indice do nosso object_event: evento da fonte}, metodo), ou (None, ...).

    POR QUE NAO BASTA A ORDEM. A regra original exigia que a contagem batesse e
    que o `graphics_id` batesse posicao a posicao. Ela e certa quando bate, e
    reprova o mapa inteiro quando o importador descartou alguem por nao caber
    (`fora_sem_espaco`), que e o caso de `OreburghMine_B2F` e `Route205_North`.

    A coordenada resolve isso sem virar chute, pela mesma via que
    `itens_escondidos_sinnoh.alinha_por_coordenada` usa para placa: o importador
    percorre a fonte EM ORDEM e poe cada NPC no tile livre mais proximo de
    `conv(e)`, dentro do raio 8 de `importa_npcs_sinnoh.livre`. Logo o casamento
    certo e uma SUBSEQUENCIA da fonte, com grafico igual e distancia de
    Chebyshev dentro daquele raio. Duas guardas mantem isso honesto:

    - **so vale se for UNICA.** Duas subsequencias possiveis reprovam o mapa, do
      mesmo jeito que duas placas na mesma coordenada reprovam la.
    - **a regra da ordem tem prioridade.** Onde a contagem bate, o resultado e o
      de antes, byte por byte: mapa ja resolvido nao muda de resposta.
    """
    f_npcs, _ = separa_fonte(fonte)
    nossos = [(i, o) for i, o in enumerate(d.get("object_events") or [])
              if o.get("origem") == "pokeplatinum"]
    if not nossos:
        return {}, "vazio"
    esperado = [sprite_esperado(e, sprites) for e in f_npcs]
    if len(nossos) == len(f_npcs) and \
            all(g == o.get("graphics_id") for g, (_, o) in zip(esperado, nossos)):
        return {i: e for (i, _), e in zip(nossos, f_npcs)}, "ordem"

    L = _layouts().get(d.get("layout"))
    if not L:
        return None, "sem_layout"
    conv = I.conversor_de_coordenada(fonte, L["width"], L["height"], header, matriz)
    if conv is None:
        return None, "sem_conversor"
    fc = [(e, conv(e), g) for e, g in zip(f_npcs, esperado)]
    op = subsequencias(fc, nossos)
    if len(op) != 1:
        return None, ("ambiguo" if op else "sem_casamento")
    return {nossos[j][0]: f_npcs[i] for j, i in enumerate(op[0])}, "coordenada"


def separa_fonte(fonte):
    """Os eventos da fonte na MESMA ordem em que o importador os gravou."""
    npcs, placas = [], []
    for e in fonte.get("object_events", []):
        classe = e.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
        if any(t in classe for t in I.GRAFICOS_PROIBIDOS):
            continue
        if any(t in classe for t in I.NOMES_PROPRIOS):
            continue
        if str(e.get("hidden_flag", "0")) not in ("0", "0x0"):
            continue
        (placas if any(t in classe for t in I.GRAFICOS_PLACA) else npcs).append(e)
    return npcs, placas + list(fonte.get("bg_events", []))


def casados():
    """(nosso mapa, MAP_HEADER, arquivo de eventos) de cada par."""
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev, mx))
    for m in I.mapas_editaveis_sinnoh():
        h = I.APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(I.chave(m))
        if alvo:
            yield (m, alvo[0], alvo[1])


def tabela_de_itens():
    """indice do bg_event (script - 8000) -> (item, quantidade, flag).

    O indice NAO e a posicao na tabela `gHiddenItems`: e a posicao da FLAG
    dentro do bloco que comeca em `HIDDEN_ITEM_FLAGS_START`
    (`src/script_manager.c:534` faz exatamente essa conta). Os dois numeros
    divergem porque o bloco de flags tem 284 posicoes e a tabela tem 257
    entradas, com `FLAG_UNUSED_*` no meio do bloco. Ler pela posicao da tabela
    resolvia 255 dos 262 e deixava sete sem nome, todos acima do indice 256.
    """
    global _ITENS
    try:
        return _ITENS
    except NameError:
        pass
    linhas = [l.strip() for l in
              open(os.path.join(PLAT, "generated/vars_flags.txt"), encoding="utf-8")]
    i = linhas.index("HIDDEN_ITEM_FLAGS_START")
    ordem = []
    for l in linhas[i + 1:]:
        if l.startswith("HIDDEN_ITEM_FLAGS_END"):
            break
        ordem.append(l.split("=")[0].strip())
    txt = open(os.path.join(PLAT, "include/data/field/hidden_items.h"),
               encoding="utf-8").read()
    por_flag = {f: (it, q) for it, q, _r, f in re.findall(
        r"HIDDEN_ITEM_ENTRY\(\s*(\w+),\s*(\d+),\s*(\d+),\s*(\w+)\s*\)", txt)}
    _ITENS = [por_flag.get(n, ("?", "?")) + (n,) for n in ordem]
    return _ITENS


def rotulo_livre(usados, mapa, tipo, seq):
    """`<Mapa>_EventScript_<tipo><n>`, pulando numero que o arquivo ja usa.

    `usados` TEM que vir semeado com os rotulos que o scripts.inc ja tem. A
    primeira versao comecava com o conjunto vazio e renumerava do 1, por cima de
    `<Mapa>_EventScript_Placa4` que `texto_placas_sinnoh.py` ja tinha escrito:
    134 `symbol already defined` em 50 mapas, e o build inteiro parado.
    """
    while True:
        seq[0] += 1
        n = f"{mapa}_EventScript_{tipo}{seq[0]}"
        if n not in usados and n.replace("_EventScript_", "_Text_") not in usados:
            usados.add(n)
            return n


def rotulos_repetidos():
    """[(rotulo, [arquivos])] definido mais de uma vez na unidade de montagem.

    Conferir que o rotulo EXISTE nao prova nada: rotulo duplicado existe duas
    vezes e passa nessa checagem. Quem reprova e o assembler, entao a pergunta
    tem que ser feita na camada dele: `data/event_scripts.s` inclui os 2018
    `scripts.inc` num arquivo so, e o nome tem que ser unico no CONJUNTO, nao
    dentro de cada arquivo.

    `.if/.else` fica de fora: o vanilla define o mesmo rotulo nos dois ramos de
    proposito (`MtChimney_EventScript_BagIsFull`) e so um e montado.
    """
    raiz = os.path.join(REPO, "data/event_scripts.s")
    incs = re.findall(r'\.include\s+"([^"]+)"', open(raiz, errors="replace").read())
    dono = {}
    for p in [raiz] + [os.path.join(REPO, i) for i in incs]:
        if not os.path.exists(p):
            continue
        ramo = 0
        for linha in open(p, errors="replace"):
            t = linha.strip()
            if t.startswith(".if"):
                ramo += 1
            elif t.startswith(".endif"):
                ramo = max(0, ramo - 1)
            m = re.match(r"^(\w+):{1,2}\s*$", linha)
            if m and not ramo:
                dono.setdefault(m.group(1), []).append(os.path.relpath(p, REPO))
    return [(k, v) for k, v in dono.items() if len(v) > 1]


def main():
    sprites = V.sprites_utilizaveis()
    heads = I.headers_do_platinum()
    st = dict(npcs=0, placas=0, npc_mapa_pulado=0, placa_mapa_pulado=0,
              npc_sem_texto=0, placa_sem_texto=0, itens=0, safari=0)
    itens, plano = [], {}

    for meu, header, arq_ev in casados():
        pe = os.path.join(PLAT, "res/field/events", arq_ev + ".json")
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if not (os.path.exists(pe) and os.path.exists(pm)):
            continue
        fonte = json.load(open(pe, encoding="utf-8"))
        d = json.load(open(pm, encoding="utf-8"))
        f_npcs, f_placas = separa_fonte(fonte)
        # O indice dentro do array e o que vai para o plano: na hora de escrever
        # o arquivo e relido, e a troca so acontece se o evento daquele indice
        # ainda for o mesmo. Outro agente pode ter mexido no mesmo map.json.
        n_npcs = [(i, o) for i, o in enumerate(d.get("object_events", []))
                  if o.get("origem") == "pokeplatinum"]
        n_placas = [(i, b) for i, b in enumerate(d.get("bg_events", []))
                    if b.get("origem") == "pokeplatinum"]
        if not (n_npcs or n_placas):
            continue

        campos = campos_do_header(header)
        if not campos:
            continue
        arq_scr, arq_msg, _ = campos
        ordem, corpos = entradas_de_script(arq_scr) if arq_scr else ([], {})
        banco = banco_de_texto(arq_msg) if arq_msg else {}

        # Alinhamento. Ordem primeiro, coordenada depois; ver `alinha_npcs`.
        # Placa continua so por contagem, porque `itens_escondidos_sinnoh.py` ja
        # e o dono do alinhamento por coordenada dela.
        pares_npc, _metodo = alinha_npcs(header, heads[header][1], fonte, d, sprites)
        ok_placa = len(n_placas) == len(f_placas)
        if n_npcs and pares_npc is None:
            st["npc_mapa_pulado"] += 1
        if n_placas and not ok_placa:
            st["placa_mapa_pulado"] += 1

        # Semente: todo rotulo que o scripts.inc do mapa JA tem. Sem isso, uma
        # segunda passada renumera do 1 e reescreve rotulo que ja existe, o que
        # nao e erro de logica nenhum, e sim `symbol already defined` no build.
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        usados = set(re.findall(r"^(\w+)::?", open(ps, errors="replace").read(), re.M)) \
            if os.path.exists(ps) else set()
        trecho, seq = "", [0]
        troca_obj, troca_bg = [], []

        def texto_de(dela):
            idx = dela.get("script")
            if not isinstance(idx, int) or not (1 <= idx <= len(ordem)):
                return None, []
            tid, buffers = texto_do_rotulo(corpos, ordem[idx - 1])
            if not tid or tid not in banco:
                return None, []
            return resolve(banco[tid], buffers)

        if pares_npc:
            for pos, dela in sorted(pares_npc.items()):
                nossa = d["object_events"][pos]
                if str(nossa.get("script", "0")) not in ("0", "0x0", "NULL", ""):
                    continue
                pronto, comandos = texto_de(dela)
                if not pronto:
                    st["npc_sem_texto"] += 1
                    continue
                lab = rotulo_livre(usados, meu, "Npc", seq)
                txt = lab.replace("_EventScript_", "_Text_")
                enche = "".join(f"\t{c}\n" for c in comandos)
                trecho += (f"\n{lab}::\n{enche}\tmsgbox {txt}, MSGBOX_NPC\n\tend\n\n"
                           f'{txt}:\n\t.string "{pronto}"\n')
                troca_obj.append((pos, lab))
                st["npcs"] += 1

        if ok_placa:
            for dela, (pos, nossa) in zip(f_placas, n_placas):
                if nossa.get("script") != GENERICO:
                    continue
                idx = dela.get("script")
                if isinstance(idx, int) and idx in ITEM_ESCONDIDO:
                    st["itens"] += 1
                    tab = tabela_de_itens()
                    ent = tab[idx - 8000] if idx - 8000 < len(tab) else ("?",) * 3
                    itens.append((meu, nossa.get("x"), nossa.get("y")) + ent)
                    continue
                if isinstance(idx, int) and idx >= 8800:
                    st["safari"] += 1
                    continue
                pronto, comandos = texto_de(dela)
                # Placa nao ganha comando de buffer: `msgbox MSGBOX_SIGN` roda
                # sem `lock`, e encher STR_VAR ali seria script novo escondido
                # numa placa. Fala com buffer fica de fora, como antes.
                if not pronto or comandos:
                    st["placa_sem_texto"] += 1
                    continue
                lab = rotulo_livre(usados, meu, "Placa", seq)
                txt = lab.replace("_EventScript_", "_Text_")
                trecho += (f"\n{lab}::\n\tmsgbox {txt}, MSGBOX_SIGN\n\tend\n\n"
                           f'{txt}:\n\t.string "{pronto}"\n')
                troca_bg.append((pos, lab))
                st["placas"] += 1

        if troca_obj or troca_bg:
            plano[meu] = (troca_obj, troca_bg, trecho)

    print(f"NPC que deixam de ser mudos: {st['npcs']}")
    print(f"placas com texto proprio:    {st['placas']}")
    print(f"itens escondidos preservados: {st['itens']}   safari/chatot: {st['safari']}")
    print(f"sem texto na fonte: {st['npc_sem_texto']} NPC, {st['placa_sem_texto']} placas")
    print(f"mapas pulados por alinhamento: {st['npc_mapa_pulado']} de NPC, "
          f"{st['placa_mapa_pulado']} de placa")
    print(f"mapas escritos: {len(plano)}")

    if "--itens" in sys.argv:
        print("\nitem escondido que hoje e placa generica "
              "(mapa, x, y, item, quantidade, flag do Platinum):")
        for linha in itens:
            print("   ", "\t".join(str(c) for c in linha))

    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    escritos = recusados = 0
    for meu, (troca_obj, troca_bg, trecho) in plano.items():
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        # Releitura tardia: outro agente pode ter mexido no mesmo arquivo entre
        # a leitura la de cima e agora. So o `script` de um evento que continua
        # marcado como importado E continua mudo/generico e trocado; qualquer
        # outra coisa e recusada em vez de sobrescrita.
        atual = json.load(open(pm, encoding="utf-8"))
        feito = ""
        for chave, trocas, antes in (("object_events", troca_obj,
                                      ("0", "0x0", "NULL", "")),
                                     ("bg_events", troca_bg, (GENERICO,))):
            lista = atual.get(chave) or []
            for pos, lab in trocas:
                if pos >= len(lista):
                    recusados += 1
                    continue
                ev = lista[pos]
                if ev.get("origem") != "pokeplatinum" \
                        or str(ev.get("script", "0")) not in antes:
                    recusados += 1
                    continue
                ev["script"] = lab
                feito += lab
        if not feito:
            continue
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        with open(ps, "a", encoding="utf-8") as f:
            f.write("\n@ Fala de NPC e de placa vinda do pokeplatinum "
                    "(dev_scripts/texto_sinnoh.py)\n" + trecho)
        escritos += 1
    print(f"\nescrito: {st['npcs']} NPC e {st['placas']} placas em {escritos} mapas"
          f"   recusados na releitura: {recusados}")
    return 0


def demo():
    """As tres regras que a primeira versao errou."""
    P = ("PlayerName", None)
    corpos = {
        "A": ["PlaySE SEQ_SE_CONFIRM", "LockAll", "FacePlayer",
              "GoToIfSet FLAG_X, B", "BufferPlayerName 0",
              "Message T_Padrao", "End"],
        "B": ["Message T_Ramo", "End"],
        "C": ["LockAll", "GoTo A"],
        "D": ["NPCMessage T_Npc", "End"],
        "E": ["BufferPlayerName 0", "GoTo F"],
        "F": ["Message T_Depois", "End"],
    }
    # 1. desvio condicional nao desvia: a fala padrao e a do fall-through
    assert texto_do_rotulo(corpos, "A") == ("T_Padrao", {0: P})
    # 2. `GoTo` cru e incondicional e tem que ser seguido
    assert texto_do_rotulo(corpos, "C")[0] == "T_Padrao"
    # 3. NPCMessage conta tanto quanto Message (era o comando de 656 falas que
    #    a extracao anterior nao conhecia)
    assert texto_do_rotulo(corpos, "D")[0] == "T_Npc"
    # 4. buffer posto ANTES do GoTo continua valendo depois dele
    assert texto_do_rotulo(corpos, "E") == ("T_Depois", {0: P})
    # 5. buffer do jogador vira {PLAYER} e nao custa comando nenhum
    assert resolve(["Hi, {STRVAR_1 3, 0, 0}!"], {0: P}) == ("Hi, {PLAYER}!$", [])
    # 6. buffer sem dono, e buffer sem equivalente honesto, reprovam o texto
    assert resolve(["Hi, {STRVAR_1 3, 1, 0}!"], {0: P}) == (None, [])
    assert resolve(["Hi, {STRVAR_1 3, 0, 0}!"], {0: ("RivalName", None)}) == (None, [])
    assert resolve(["{SIZE 200}Thud!!\r"], {}) == ("Thud!!$", [])
    # 7. os buffers que TEM equivalente saem com o comando que os enche
    assert resolve(["Your {STRVAR_1 0, 0, 0}!"], {0: ("PartyMonSpecies", "0")}) == \
        ("Your {STR_VAR_1}!$", ["bufferleadmonspeciesname STR_VAR_1"])
    assert resolve(["Hold this {STRVAR_1 8, 0, 0}."],
                   {0: ("ItemName", "ITEM_QUICK_CLAW")}) == \
        ("Hold this {STR_VAR_1}.$", ["bufferitemname STR_VAR_1, ITEM_QUICK_CLAW"])
    # item que esta ROM nao tem reprova em vez de virar simbolo inexistente
    assert resolve(["x {STRVAR_1 8, 0, 0}"],
                   {0: ("ItemName", "ITEM_NAO_EXISTE_AQUI")}) == (None, [])
    # 8. a nota musical tem simbolo aqui, com outro nome
    assert resolve(["Chop away! ~♫"], {}) == ("Chop away! ~{EMOJI_NOTE}$", [])
    # 9. o cifrao TERMINA a string (charmap.txt:162 '$' = FF): dinheiro vira ¥ e
    #    cifrao solto reprova. Sem esta regra, seis falas ja escritas foram
    #    cortadas no meio ("Moomoo Milk, $500 a bottle").
    assert resolve(["Milk, $500 a bottle."], {}) == ("Milk, ¥500 a bottle.$", [])
    assert resolve(["Pay in $ please."], {}) == (None, [])
    # 10. rotulo que o arquivo ja tem NAO pode ser reusado: numero ocupado se
    #    pula, e o par _Text_ conta tanto quanto o _EventScript_
    ja = {"Foo_EventScript_Placa1", "Foo_Text_Placa2"}
    assert rotulo_livre(ja, "Foo", "Placa", [0]) == "Foo_EventScript_Placa3"
    # 11. alinhamento por subsequencia: unico casamento passa, dois reprovam
    fc = [({}, (10, 10), "G1"), ({}, (20, 20), "G1"), ({}, (99, 99), "G1")]
    assert subsequencias(fc, [(0, {"graphics_id": "G1", "x": 11, "y": 12}),
                              (1, {"graphics_id": "G1", "x": 22, "y": 20})]) == [(0, 1)]
    assert len(subsequencias([({}, (10, 10), "G1"), ({}, (12, 12), "G1")],
                             [(0, {"graphics_id": "G1", "x": 11, "y": 11})])) == 2
    assert subsequencias([({}, (10, 10), "G2")],
                         [(0, {"graphics_id": "G1", "x": 10, "y": 10})]) == []
    # 12. e a checagem na camada da afirmacao: nenhum rotulo escrito por este
    #    script pode estar definido duas vezes no mesmo scripts.inc
    repetidos = rotulos_repetidos()
    assert not repetidos, (f"{len(repetidos)} rotulo(s) duplicado(s), o build "
                           f"reprova: {repetidos[:5]}")
    print("demo ok (unidade de montagem de data/event_scripts.s conferida, "
          "zero rotulo duplicado)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
