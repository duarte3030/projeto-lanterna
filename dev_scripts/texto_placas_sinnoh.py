#!/usr/bin/env python3
"""Da texto de verdade as 425 placas de Sinnoh que dizem "faded with age".

As placas vieram do pokeplatinum em 05/08/2026 apontando todas para um rotulo
unico, porque la o campo `script` da placa e um INDICE numerico e o texto mora
num banco separado. A corrente inteira existe e da para seguir:

    events_<mapa>.json   objeto de placa com "script": N
    scripts_<mapa>.s     N-esimo `ScriptEntry` da lista do topo do arquivo
    o corpo do rotulo    `ShowArrowSign X` / `ShowLandmarkSign X` / `Message X`
    res/text/<mapa>.json mensagem de id X, em en_US

O elo fraco e ligar a NOSSA placa a placa DELES: o importador nao gravou o
indice de origem, so a marca "origem": "pokeplatinum". Sobra a ordem. Por isso
a regra e conservadora: **so casa mapa onde a contagem bate**. Mapa onde o
importador descartou alguma placa por nao caber fica de fora inteiro, com aviso,
em vez de arriscar trocar "Rt. 208 Mt. Coronet" por "Rt. 208 Hearthome City",
que e pior que placa apagada, porque manda o jogador para o lado errado.

Uso:
    python3 dev_scripts/texto_placas_sinnoh.py            # so relata
    python3 dev_scripts/texto_placas_sinnoh.py --aplica
    python3 dev_scripts/texto_placas_sinnoh.py --demo
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAT = os.path.join(os.path.dirname(REPO), "fontes-mapas/pokeplatinum")
APLICA = "--aplica" in sys.argv
GENERICO = "Sinnoh_EventScript_PlacaImportada"

sys.path.insert(0, f"{REPO}/dev_scripts")
import importa_npcs_sinnoh as I  # noqa: E402

# Grafico de placa, mesma lista que o importador usou para separar placa de NPC.
GRAFICOS_PLACA = I.GRAFICOS_PLACA


def le(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def placas_da_fonte(fonte):
    """As placas na MESMA ordem em que o importador as gravou.

    Ele nao guardou o indice de origem, entao a ordem e o unico elo. Ela e:
    primeiro os object_events com grafico de placa que passaram pelos filtros
    dele (mobilia fora, nome proprio fora, hidden_flag fora), depois os
    bg_events. Reproduzir a mesma sequencia e o que faz a contagem bater.
    """
    fora = []
    for e in fonte.get("object_events", []):
        classe = e.get("graphics_id", "").replace("OBJ_EVENT_GFX_", "")
        if any(t in classe for t in I.GRAFICOS_PROIBIDOS):
            continue
        if any(t in classe for t in I.NOMES_PROPRIOS):
            continue
        if str(e.get("hidden_flag", "0")) not in ("0", "0x0"):
            continue
        if any(t in classe for t in GRAFICOS_PLACA):
            fora.append(e)
    return fora + list(fonte.get("bg_events", []))


def campos_do_header(header):
    """scriptsArchiveID, msgArchiveID e eventsArchiveID de um MAP_HEADER."""
    global _HDR
    try:
        _HDR
    except NameError:
        _HDR = le(f"{PLAT}/include/data/map_headers.h")
    m = re.search(rf"\[{header}\]\s*=\s*{{(.*?)}},", _HDR, re.S)
    if not m:
        return None
    corpo = m.group(1)

    def campo(nome):
        c = re.search(rf"\.{nome}\s*=\s*(\w+)", corpo)
        return c.group(1) if c else None
    return campo("scriptsArchiveID"), campo("msgArchiveID"), campo("eventsArchiveID")


def entradas_de_script(arquivo):
    """Lista de rotulos na ordem dos `ScriptEntry`, e o corpo de cada rotulo."""
    p = f"{PLAT}/res/field/scripts/{arquivo}.s"
    if not os.path.exists(p):
        return [], {}
    s = le(p)
    ordem = re.findall(r"^\s*ScriptEntry\s+(\w+)", s, re.M)
    corpos, atual = {}, None
    for linha in s.split("\n"):
        m = re.match(r"^(\w+):\s*$", linha)
        if m:
            atual = m.group(1)
            corpos[atual] = []
        elif atual:
            corpos[atual].append(linha.strip())
    return ordem, corpos


MOSTRA = re.compile(r"^(?:ShowArrowSign|ShowLandmarkSign|ShowScrollingSign"
                    r"|Message|MessageAndWaitButton)\s+(\w+)")


def texto_do_corpo(corpo):
    for l in corpo:
        m = MOSTRA.match(l)
        if m:
            return m.group(1)
    return None


def banco_de_texto(msg_archive):
    """TEXT_BANK_ROUTE_208 -> res/text/route_208.json, id -> lista de linhas."""
    nome = msg_archive.replace("TEXT_BANK_", "").lower()
    p = f"{PLAT}/res/text/{nome}.json"
    if not os.path.exists(p):
        return {}
    return {m["id"]: m.get("en_US", []) for m in json.load(open(p))["messages"]}


# Sinal de fim de linha do DS -> sinal do GBA. \r fecha a caixa (nova caixa
# aqui e \p), \n abre a segunda linha, e da terceira em diante e \l, que rola.
ACENTO = {"’": "'", "‘": "'", "“": '"', "”": '"',
          "…": "...", "—": "-", "–": "-",
          # As setas do enigma do elevador de Hearthome vinham cruas do banco
          # do Platinum e o preproc parava a build com "unknown character
          # U+2190". O charmap tem o glifo, mas só pelo nome entre chaves.
          "←": "{LEFT_ARROW}", "↑": "{UP_ARROW}",
          "→": "{RIGHT_ARROW}", "↓": "{DOWN_ARROW}"}


def para_gba(linhas):
    # Mensagem de uma linha so vem como string crua no banco, e iterar string
    # da CARACTERE: "{STRVAR_1 3, 0, 0}'s House" virou uma placa com uma letra
    # por linha antes deste isinstance.
    if isinstance(linhas, str):
        linhas = [linhas]
    saida, na_caixa = "", 0
    for bruta in linhas:
        # \f (form feed) tambem fecha caixa no banco do Platinum, e o preproc
        # do pokeemerald recusa o byte cru: "unexpected character U+C".
        fecha_caixa = bruta.endswith(("\r", "\f"))
        quebra = bruta.endswith("\n")
        t = bruta.rstrip("\r\n\f")
        t = "".join(c for c in t if c >= " " or c == "\t")
        for a, b in ACENTO.items():
            t = t.replace(a, b)
        t = t.replace('"', "'")  # aspas dupla fecharia a .string
        if na_caixa:  # dentro da caixa: \n na 2a linha, \l da 3a em diante
            saida += "\\n" if na_caixa == 1 else "\\l"
        saida += t
        na_caixa += 1
        if fecha_caixa:  # \p ja e o separador; nao pode vir \n depois dele
            saida += "\\p"
            na_caixa = 0
        del quebra
    return requebra(saida.removesuffix("\\p")) + "$"


# --------------------------------------------------------------------------
# O REQUEBRADOR. Mede em PIXEL, nao em caractere.
#
# A caixa de fala padrao tem 26 tiles de 8 px (208 px uteis) e mostra DUAS
# linhas por vez: `\n` abre a segunda, e da TERCEIRA em diante quem serve e
# `\l`, que rola a janela. Terceiro `\n` escreve fora da janela, e linha mais
# larga que 208 px passa da borda direita: os dois somem sem erro nenhum, nem
# de build nem de motor.
#
# A regra e CONSERVADORA de proposito: so mexe no que estoura. Ponto de quebra
# que ja cabe fica onde esta, porque placa curta ("ETERNA FOREST") e quebra de
# efeito sao desenho, nao defeito. Por isso `requebra` e idempotente e o
# `para_gba` continua devolvendo byte a byte a mesma coisa para texto sao.
#
# A tabela de largura sai de `gFontNormalLatinGlyphWidths` (`src/fonts.c`) e o
# byte de cada letra sai do `charmap.txt` DESTE repo. E a mesma regua do
# `qa/checa_texto.py`, inclusive nos casos torto (`{PLAYER}` vale 42 px,
# chave desconhecida vale 36), senao a ferramenta consertaria uma coisa e a
# auditoria cobraria outra.
# --------------------------------------------------------------------------
LARGURA_CAIXA = 208
LINHAS_POR_CAIXA = 2
NOMINAL = {"PLAYER": 7, "RIVAL": 7, "STR_VAR_1": 0, "STR_VAR_2": 0,
           "STR_VAR_3": 0, "KUN": 0}
_CHAVE = re.compile(r"\{([A-Z0-9_]+)(?:\s+[^}]*)?\}")
_MEDIDA = {}


def _regua():
    """(charmap: letra -> bytes, larguras: byte -> px)."""
    if _MEDIDA:
        return _MEDIDA["charmap"], _MEDIDA["larguras"]
    mapa = {}
    rx1 = re.compile(r"^'(.+?)'\s*=\s*((?:[0-9A-Fa-f]{2}\s*)+)")
    rx2 = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*((?:[0-9A-Fa-f]{2}\s*)+)")
    for linha in open(f"{REPO}/charmap.txt", encoding="utf-8", errors="replace"):
        linha = linha.rstrip("\n")
        if linha.startswith("@"):
            continue
        m = rx1.match(linha) or rx2.match(linha)
        if not m:
            continue
        chave = m.group(1)
        if len(chave) == 2 and chave[0] == "\\":
            chave = {"n": "\n", "l": "\l", "p": "\p"}.get(chave[1], chave[1])
        mapa.setdefault(chave, [int(x, 16) for x in m.group(2).split()])
    txt = le(f"{REPO}/src/fonts.c")
    m = re.search(r"gFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};", txt, re.S)
    nums = [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []
    larguras = nums + [6] * (256 - len(nums))
    _MEDIDA["charmap"], _MEDIDA["larguras"] = mapa, larguras
    return mapa, larguras


def largura_px(trecho):
    """Largura em px de um pedaco SEM quebra de linha."""
    charmap, larguras = _regua()
    px, i = 0, 0
    while i < len(trecho):
        c = trecho[i]
        if c == "{":
            m = _CHAVE.match(trecho, i)
            if m:
                nome = m.group(1)
                n = NOMINAL.get(nome)
                if n is None:
                    n = 6 if nome not in charmap else 1
                px += n * 6
                i = m.end()
                continue
        if c == "\\":       # `\n`, `\l`, `\p` nao ocupam pixel
            i += 2
            continue
        for b in charmap.get(c, [0x00]):
            px += larguras[b] if c in charmap else 6
        i += 1
    return px


def _quebra_larga(ln):
    """[linha] se ja cabe; senao a MESMA linha reparada em pedacos que cabem."""
    if largura_px(ln) <= LARGURA_CAIXA:
        return [ln]
    guardadas = []

    def guarda(m):
        guardadas.append(m.group(0))
        return "\x01%d\x02" % (len(guardadas) - 1)

    def solta(s):
        return re.sub(r"\x01(\d+)\x02",
                      lambda m: guardadas[int(m.group(1))], s)

    palavras = _CHAVE.sub(guarda, ln).split(" ")
    linhas, atual = [], ""
    for p in palavras:
        cand = p if not atual else atual + " " + p
        if atual and largura_px(solta(cand)) > LARGURA_CAIXA:
            linhas.append(solta(atual))
            atual = p
        else:
            atual = cand
    linhas.append(solta(atual))
    return linhas


def requebra(corpo):
    """Corpo de `.string` (sem o `$`) com a caixa respeitada. Idempotente."""
    saida = []
    for caixa in corpo.split("\\p"):
        linhas = re.split(r"\\[nl]", caixa)
        if any(largura_px(l) > LARGURA_CAIXA for l in linhas):
            # Caixa com linha estourada e refluida INTEIRA. Repartir so a linha
            # culpada deixa orfa de uma palavra a linha seguinte, que ja estava
            # cheia: o defeito sai e a fala fica torta do mesmo jeito.
            linhas = _quebra_larga(" ".join(l for l in linhas if l != ""))
        while len(linhas) > 1 and linhas[-1] == "":
            linhas.pop()            # `...round!\n$` e uma terceira linha VAZIA
        montada = linhas[0] if linhas else ""
        for i, ln in enumerate(linhas[1:], start=1):
            montada += ("\\n" if i < LINHAS_POR_CAIXA else "\\l") + ln
        saida.append(montada)
    return "\\p".join(saida)


BLOCO_TEXTO = re.compile(r'^([A-Za-z_]\w*):{1,2}[ \t]*\n'
                         r'((?:[ \t]*\.string ".*"[ \t]*\n)+)', re.M)


# Sinnoh nao mora so nos grupos com "Sinnoh" no nome: os interiores das cinco
# primeiras cidades tem grupo proprio. Mesma lista de `qa/leitor.GRUPO_REGIAO`;
# filtrar so por "Sinnoh" deixava de fora 2 dos 141 textos tortos.
GRUPOS_SINNOH = ("Sinnoh", "TeamGalactic", "IndoorTwinleaf", "IndoorSandgem",
                 "IndoorJubilife", "IndoorOreburgh", "IndoorFloaroma")


def mapas_de_sinnoh():
    mg = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    return sorted({m for g, v in mg.items() if isinstance(v, list)
                   and any(t in g for t in GRUPOS_SINNOH) for m in v})


def aplica_requebra(escreve):
    """Passa o requebrador nos `.string` que JA estao na arvore, em Sinnoh."""
    tocados, blocos = 0, 0
    for nome in mapas_de_sinnoh():
        p = f"{REPO}/data/maps/{nome}/scripts.inc"
        if not os.path.exists(p):
            continue
        original = le(p)

        def um(m):
            nonlocal blocos
            pedacos = re.findall(r'\.string "(.*)"', m.group(2))
            inteiro = "".join(pedacos)
            if not inteiro.endswith("$"):
                return m.group(0)
            novo = requebra(inteiro[:-1])
            if novo == inteiro[:-1]:
                return m.group(0)
            blocos += 1
            partes = re.split(r"(\\[nlp])", novo)
            linhas, i = [], 0
            while i < len(partes):
                pedaco = partes[i] + (partes[i + 1] if i + 1 < len(partes) else "")
                linhas.append(pedaco)
                i += 2
            linhas[-1] += "$"
            corpo = "".join('\t.string "%s"\n' % l for l in linhas)
            return "%s:%s\n%s" % (m.group(1),
                                  ":" if m.group(0).startswith(m.group(1) + "::")
                                  else "", corpo)

        novo_arq = BLOCO_TEXTO.sub(um, original)
        if novo_arq != original:
            tocados += 1
            if escreve:
                open(p, "w", encoding="utf-8").write(novo_arq)
    print(f"requebrador: {blocos} blocos de texto reparados em {tocados} arquivos"
          + ("" if escreve else "  (nada escrito; rode com --aplica)"))
    return 0


def main():
    heads = I.headers_do_platinum()
    mg = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    nossos = {m for g, v in mg.items() if "Sinnoh" in g for m in v}
    norm = lambda s: re.sub(r"[^A-Z0-9]", "", s.upper())  # noqa: E731
    nn = {norm(m): m for m in nossos}

    trocadas = pulados = sem_texto = 0
    avisos = []
    plano = {}  # mapa -> (novos bg_events, trecho de scripts.inc)

    for header in heads:
        nome = nn.get(norm(header.replace("MAP_HEADER_", "")))
        if not nome:
            continue
        p = f"{REPO}/data/maps/{nome}/map.json"
        d = json.load(open(p))
        minhas = [b for b in d.get("bg_events", []) if b.get("script") == GENERICO]
        if not minhas:
            continue
        campos = campos_do_header(header)
        if not campos:
            avisos.append(f"{nome}: header sem campos")
            pulados += len(minhas)
            continue
        scr, msg, ev = campos
        pe = f"{PLAT}/res/field/events/{ev}.json"
        if not os.path.exists(pe):
            pulados += len(minhas)
            continue
        delas = placas_da_fonte(json.load(open(pe)))
        if len(delas) != len(minhas):
            avisos.append(f"{nome}: {len(minhas)} nossas x {len(delas)} delas, pulado")
            pulados += len(minhas)
            continue

        ordem, corpos = entradas_de_script(scr)
        banco = banco_de_texto(msg) if msg else {}
        trecho, novos = "", []
        for i, (nossa, dela) in enumerate(zip(minhas, delas)):
            idx = dela.get("script")
            rot = ordem[idx - 1] if isinstance(idx, int) and 1 <= idx <= len(ordem) else None
            tid = texto_do_corpo(corpos.get(rot, [])) if rot else None
            linhas = banco.get(tid) if tid else None
            # `{STRVAR_1 ...}` e nome montado em tempo de execucao (o dono da
            # casa, o jogador). Sem o mesmo motor de texto, isso nao traduz:
            # a placa fica generica em vez de mostrar chave crua na tela.
            if linhas and "{" in "".join(linhas):
                linhas = None
            if not linhas:
                sem_texto += 1
                novos.append(nossa)
                continue
            lab = f"{nome}_EventScript_Placa{i + 1}"
            trecho += (f"\n{lab}::\n\tmsgbox {nome}_Text_Placa{i + 1}, MSGBOX_SIGN\n"
                       f"\tend\n\n{nome}_Text_Placa{i + 1}:\n"
                       f'\t.string "{para_gba(linhas)}"\n')
            nova = dict(nossa)
            nova["script"] = lab
            novos.append(nova)
            trocadas += 1
        if trecho:
            plano[nome] = (novos, trecho)

    print(f"placas com texto proprio: {trocadas}")
    print(f"puladas por contagem diferente: {pulados}   sem texto na fonte: {sem_texto}")
    for a in avisos[:10]:
        print("   ", a)
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    for nome, (novos, trecho) in plano.items():
        p = f"{REPO}/data/maps/{nome}/map.json"
        d = json.load(open(p))
        it = iter(novos)
        d["bg_events"] = [next(it) if b.get("script") == GENERICO else b
                          for b in d.get("bg_events", [])]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(f"{REPO}/data/maps/{nome}/scripts.inc", "a", encoding="utf-8") as f:
            f.write("\n@ Texto de placa vindo do pokeplatinum "
                    "(dev_scripts/texto_placas_sinnoh.py)\n" + trecho)
    print(f"escrito: {trocadas} placas em {len(plano)} mapas")
    return 0


def demo():
    """\\r fecha caixa (\\p), primeira quebra e \\n, as seguintes sao \\l."""
    assert para_gba(["Rt. 208\n", "Mt. Coronet"]) == "Rt. 208\\nMt. Coronet$"
    assert para_gba(["a\n", "b\r", "c\n", "d"]) == "a\\nb\\pc\\nd$"
    assert para_gba(["um\n", "dois\n", "tres"]) == "um\\ndois\\ltres$"
    assert para_gba(["Don’t\r"]) == "Don't$"

    # --- requebrador -------------------------------------------------------
    # 1. a regua e de PIXEL e nao de caractere, e e A MESMA do qa/checa_texto:
    #    a auditoria de 23/08 mediu 210 px nesta linha de Canalave, e 40 `i`
    #    cabem onde 40 `W` nao cabem (160 px contra 240 px).
    assert largura_px("The access to the Wi-Fi Plaza is through") == 210
    assert largura_px("i" * 40) <= LARGURA_CAIXA < largura_px("W" * 40)
    # 2. texto sao nao e tocado (e por isso os quatro asserts acima sobrevivem)
    for sao in ("um\\ndois", "um\\ndois\\ltres", "a\\nb\\pc\\nd", ""):
        assert requebra(sao) == sao, sao
    # 3. terceira linha com `\\n` vira `\\l` (o defeito de 141 textos de Sinnoh)
    assert requebra("um\\ndois\\ntres") == "um\\ndois\\ltres"
    # 4. terceira linha VAZIA (o `...round!\\n$` dos treinadores de rota) some
    assert requebra("um\\ndois\\n") == "um\\ndois"
    # 5. linha larga demais e repartida, e cada pedaco cabe
    larga = "You've got me beat...Your desire and the noble way " \
            "your Pokemon battled for you...I even felt thrilled"
    assert largura_px(larga) > LARGURA_CAIXA
    quebrada = requebra(larga)
    assert all(largura_px(l) <= LARGURA_CAIXA
               for l in re.split(r"\\[nlp]", quebrada)), quebrada
    # 6. e o resultado nao perde nem inventa palavra
    assert re.split(r"\\[nlp]", quebrada) != [larga]
    assert " ".join(re.split(r"\\[nlp]", quebrada)).split() == larga.split()
    # 7. IDEMPOTENTE: rodar de novo no proprio resultado nao muda nada
    assert requebra(quebrada) == quebrada
    # 8. `{PLAYER}` nao e cortado no meio
    with_chave = "{PLAYER} " + "palavra " * 12 + "{PLAYER}"
    assert "{PLAYER}" in requebra(with_chave)
    assert requebra(with_chave).count("{PLAYER}") == 2
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--requebra" in sys.argv:
        sys.exit(aplica_requebra(APLICA))
    else:
        sys.exit(main())
