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
          "…": "...", "—": "-", "–": "-"}


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
    return saida.removesuffix("\\p") + "$"


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
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
