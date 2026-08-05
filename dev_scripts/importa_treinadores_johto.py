#!/usr/bin/env python3
"""Porta os treinadores de ROTA de Johto do hns para este repo.

Uso:
    python3 dev_scripts/importa_treinadores_johto.py ../../fontes-mapas/hns
    python3 dev_scripts/importa_treinadores_johto.py --autoteste

Johto veio inteira de fonte (mapas, warps, tilesets, ginasios), mas o import de
mapa zerou `object_events`: todo NPC virou OBJ_EVENT_GFX_ITEM_BALL parado, com
`script: 0`, e todo `scripts.inc` de rota virou um talo de duas linhas. Resultado
medido em 05/08/2026: 69 treinadores em Johto contra 474 de Kanto e 361 de Unova.

Este script devolve os treinadores de rota, em tres frentes que so fazem sentido
juntas (treinador sem NPC nao aparece, NPC sem script nao luta, script sem time
luta contra quem ja ocupa o id):

1. `data/maps/<Mapa>/scripts.inc`: os blocos de batalha e os textos, do hns.
2. `data/maps/<Mapa>/map.json`: sprite, direcao, raio de visao e script do NPC.
3. `src/data/trainers.party` + `include/constants/opponents.h`: o time e o id.

O que NAO e tocado, de proposito:

- Mapa cujo `scripts.inc` ja tem conteudo. Ginasios, Sprout Tower, farol de
  Olivine, torre de radio e esconderijo de Mahogany ja foram portados e provados
  na ROM por outras ferramentas; reescrever aqui seria apagar trabalho provado.
- Bloco de batalha que nao comeca com `trainerbattle_`. Rival, Eusine e as
  irmas Kimono sao cena com movimento, camera e var de enredo: portar so a
  batalha delas entregaria um NPC quebrado. Vao para a lista de pendencias.
- Time inventado. Treinador sem time no hns nao entra.

Faixa de id: 2274..2599, exclusiva desta frente (Kanto tem 1400-1799 e
2200-2273, Unova tem 1367-1379 e 1800-2147).
"""
import argparse
import importlib.util
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTY = os.path.join(REPO, "src/data/trainers.party")
HEADER = os.path.join(REPO, "include/constants/opponents.h")

FAIXA = (2274, 2599)

# Sentinela curto e FIXO. O corte de troca_acervo() e por texto e vai so ate o
# proximo marcador, nunca ate o fim do arquivo: ja houve duas vezes nesta
# semana em que um corte ate o fim apagou calado o acervo seguinte.
MARCA = "=== ACERVO JOHTO ROTAS (importa_treinadores_johto.py) ==="

# Sprite do hns -> sprite que ESTA build desenha. Os cinco de baixo so existem
# dentro de `#if IS_FRLG`, onde o id aponta para o vazio e reinicia a ROM.
# Validado em tempo de execucao contra object_event_graphics_info_pointers.h.
SPRITE = {
    "OBJ_EVENT_GFX_SUPER_NERD": "OBJ_EVENT_GFX_SCIENTIST_1",
    "OBJ_EVENT_GFX_FIREBREATHER": "OBJ_EVENT_GFX_MANIAC",
    "OBJ_EVENT_GFX_BURGLAR": "OBJ_EVENT_GFX_BIKER",
    "OBJ_EVENT_GFX_JUGGLER": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_BATTLE_GIRL": "OBJ_EVENT_GFX_CRUSH_GIRL",
}

# Classe e pic do hns sem nome igual aqui. O sufixo _FRLG e resolvido sozinho
# por resolve(); esta tabela e so para o que nao tem nem isso.
CLASSE = {
    "TRAINER_CLASS_PSYCHIC_M": "TRAINER_CLASS_PSYCHIC",
    "TRAINER_CLASS_FIREBREATHER": "TRAINER_CLASS_KINDLER",
    "TRAINER_CLASS_POLICEMAN": "TRAINER_CLASS_GENTLEMAN",
}
PIC = {
    "TRAINER_PIC_FIREBREATHER": "TRAINER_PIC_KINDLER",
    "TRAINER_PIC_POLICEMAN": "TRAINER_PIC_GENTLEMAN",
}

RENOMEIA_MOVE = {
    "MOVE_FAINT_ATTACK": "MOVE_FEINT_ATTACK",
    "MOVE_VICEGRIP": "MOVE_VISE_GRIP",
    "MOVE_SMELLINGSALT": "MOVE_SMELLING_SALTS",
}


def le(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def _modulo(nome, arquivo):
    spec = importlib.util.spec_from_file_location(
        nome, os.path.join(REPO, "dev_scripts", arquivo))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def constantes(caminho, prefixo):
    return set(re.findall(rf"\b{prefixo}[A-Z0-9_]+", le(os.path.join(REPO, caminho))))


# --------------------------------------------------------------------------
# leitura do hns
# --------------------------------------------------------------------------

def blocos_de_script(fonte):
    """rotulo -> corpo, para cada `Rotulo::` de um scripts.inc."""
    marcas = list(re.finditer(r"^(\w+)::[^\n]*\n", fonte, re.M))
    saida = {}
    for i, m in enumerate(marcas):
        fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(fonte)
        saida[m.group(1)] = fonte[m.end():fim]
    return saida


def batalha_simples(corpo):
    """(tipo, treinador, [textos]) se o bloco COMECA com trainerbattle_, senao None.

    Exigir que seja o primeiro comando e o filtro que separa treinador de rota de
    cena com enredo. Bloco que faz applymovement, setvar ou playbgm antes da
    batalha e cena: portar so a linha da batalha entregaria um NPC que anda para
    lugar nenhum, e por isso ele vai para a lista de pendencias inteiro.
    """
    for linha in corpo.split("\n"):
        t = linha.strip()
        if not t or t.startswith("@"):
            continue
        # A virgula depois do id e OPCIONAL: o hns escreve
        # `trainerbattle_single TRAINER_WILTON Route44_Text_...` em rotas
        # inteiras, e exigir a virgula descartava 60 treinadores calado.
        m = re.match(r"trainerbattle_(single|double)\s+(TRAINER_\w+)\s*,?\s+(.+)$", t)
        if not m:
            return None
        args = [a.strip() for a in m.group(3).split(",") if a.strip()]
        return m.group(1), m.group(2), args
    return None


def textos_do_hns(fonte):
    """rotulo -> corpo do bloco `.string`. Aceita `Rotulo:` e `Rotulo::`.

    O hns usa as duas grafias, as vezes no mesmo arquivo. So a de um dois-pontos
    era reconhecida, e Route47 inteira caiu em texto de fallback sem erro nenhum.
    """
    saida = {}
    for m in re.finditer(
            r"^(\w+):{1,2}[ \t]*\n((?:\s*\.string\s+\"[^\n]*\"\s*\n)+)", fonte, re.M):
        saida[m.group(1)] = m.group(2).rstrip("\n")
    return saida


def textos_ja_nossos():
    """Rotulos de texto que ja existem em data/text/ deste repo.

    Texto compartilhado (Route104_Text_GinaNotEnoughMons e afins) e citado pelos
    scripts do hns e ja esta aqui: copiar cria simbolo duplicado, e inventar um
    fallback joga fora texto que ja existe."""
    saida = set()
    for raiz, _, arquivos in os.walk(os.path.join(REPO, "data/text")):
        for f in arquivos:
            if f.endswith(".inc"):
                saida |= set(re.findall(r"^(\w+):{1,2}[ \t]*$",
                                        le(os.path.join(raiz, f)), re.M))
    return saida


def depois_da_batalha(corpo):
    """Rotulo do msgbox que vem logo depois da batalha, se houver."""
    m = re.search(r"^\s*msgbox\s+(\w+)\s*,", corpo, re.M)
    return m.group(1) if m else None


def times_do_hns(hns):
    """TRAINER_* do hns -> dict com classe, pic, nome, itens, double e time."""
    texto_t = le(os.path.join(hns, "src/data/trainers.h"))
    texto_p = le(os.path.join(hns, "src/data/trainer_parties.h"))

    times = {}
    for m in re.finditer(
            r"static const struct TrainerMon\w* (\w+)\[\] = \{(.*?)\n\};", texto_p, re.S):
        mons = []
        for b in re.finditer(r"\{(.*?)\}(?=\s*,?\s*(?:\{|$))", m.group(2), re.S):
            corpo = b.group(1)
            if ".species" not in corpo:
                continue
            campo = lambda p: (re.search(p, corpo).group(1)
                               if re.search(p, corpo) else None)
            moves = re.search(r"\.moves\s*=\s*\{([^}]*)\}", corpo)
            mons.append({
                "lvl": campo(r"\.lvl\s*=\s*(\d+)"),
                "species": campo(r"\.species\s*=\s*(SPECIES_\w+)"),
                "item": campo(r"\.heldItem\s*=\s*(ITEM_\w+)"),
                "iv": campo(r"\.iv\s*=\s*(\d+)"),
                "moves": [x.strip() for x in moves.group(1).split(",")
                          if x.strip().startswith("MOVE_")] if moves else [],
            })
        times[m.group(1)] = mons

    saida = {}
    for m in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", texto_t, re.S):
        corpo = m.group(2)
        campo = lambda p: (re.search(p, corpo).group(1)
                           if re.search(p, corpo) else None)
        itens = re.search(r"\.items\s*=\s*\{([^}]*)\}", corpo)
        sym = campo(r"\.party\s*=\s*\w+\((\w+)\)")
        saida[m.group(1)] = {
            "class": campo(r"\.trainerClass\s*=\s*(\w+)"),
            "pic": campo(r"\.trainerPic\s*=\s*(\w+)"),
            "name": campo(r'\.trainerName\s*=\s*_\("([^"]*)"\)') or "",
            "double": ".doubleBattle = TRUE" in corpo,
            "items": re.findall(r"ITEM_\w+", itens.group(1)) if itens else [],
            "macro": campo(r"\.party\s*=\s*(\w+)\("),
            "mons": times.get(sym or "", []),
        }
    return saida


# --------------------------------------------------------------------------
# escrita
# --------------------------------------------------------------------------

def troca_acervo(texto, linhas, marca):
    """Troca UM acervo no fim de trainers.party, sem tocar nos outros.

    O corte vai do marcador pedido ate o PROXIMO marcador `/*===`, nunca ate o
    fim do arquivo: cortar ate o fim apagaria calado os dois acervos de Kanto, e
    o gcc so reclamaria muito depois, se reclamasse.
    """
    cabeca, rabo = texto, ""
    ini = texto.find(f"/*{marca}")
    if ini != -1:
        cabeca = texto[:ini]
        prox = texto.find("/*===", ini + 4)
        rabo = texto[prox:].strip("\n") if prox != -1 else ""
    novo = (
        f"/*{marca}\n"
        "   Times portados de fontes-mapas/hns. Nada aqui foi escrito a mao: quem\n"
        "   gera e dev_scripts/importa_treinadores_johto.py. Rodar de novo troca so\n"
        "   este bloco. Comentario em bloco porque o formato .party nao aceita //. */\n\n"
        + "\n".join(linhas).rstrip("\n") + "\n"
    )
    return cabeca.rstrip("\n") + "\n\n" + novo + (("\n" + rabo + "\n") if rabo else "")


def escreve_defines(novos):
    """Apensa os #define novos em opponents.h, entre sentinelas proprias."""
    ini = "// >>> treinadores de rota de Johto (gerado) >>>"
    fim = "// <<< treinadores de rota de Johto (gerado) <<<"
    bloco = "\n".join([ini]
                      + [f"#define {n:<52} {i}" for n, i in novos.items()]
                      + [fim])
    texto = le(HEADER)
    if ini in texto:
        texto = re.sub(re.escape(ini) + r".*?" + re.escape(fim), bloco, texto, flags=re.S)
    else:
        alvo = "\n\n// ponytail: TRAINERS_COUNT nao e"
        texto = texto.replace(alvo, "\n\n" + bloco + alvo, 1)
    open(HEADER, "w", encoding="utf-8").write(texto)


# --------------------------------------------------------------------------

def autoteste():
    """Os dois estragos que ja aconteceram neste arquivo, virados em teste."""
    # 1. Trocar o acervo de Johto nao pode levar os de Kanto junto.
    base = "=== TRAINER_HOENN ===\nName: Hoenn\n"
    t = troca_acervo(base, ["=== TRAINER_J1 ==="], MARCA)
    t = t.rstrip("\n") + "\n\n/*=== ACERVO KANTO ===*/\n\n=== TRAINER_K1 ===\n"
    t2 = troca_acervo(t, ["=== TRAINER_J2 ==="], MARCA)
    nomes = re.findall(r"^=== (TRAINER_\w+) ===", t2, re.M)
    assert nomes == ["TRAINER_HOENN", "TRAINER_J2", "TRAINER_K1"], nomes
    assert t2.count(f"/*{MARCA}") == 1

    # 2. O bloco que comeca com cena nao pode ser confundido com treinador de rota.
    assert batalha_simples("\ttrainerbattle_single TRAINER_X, A, B\n\tend\n")[1] == "TRAINER_X"
    assert batalha_simples("\tlock\n\ttrainerbattle_no_intro TRAINER_X, A\n") is None
    assert batalha_simples("\tapplymovement 1, M\n\ttrainerbattle_single TRAINER_X, A, B\n") is None
    assert batalha_simples("\ttrainerbattle_double TRAINER_X, A, B, C\n")[2] == ["A", "B", "C"]

    # 3. O remapeamento de nivel tem que cair DENTRO da faixa de Johto, sempre.
    curva = _modulo("curva", "curva_de_nivel.py")
    lo, hi = curva.ALVO["Johto"]
    for l in (2, 5, 20, 45, 50):
        v = curva.transforma(l, (2, 50), (lo, hi))
        assert lo <= v <= hi, (l, v)
    print("autoteste ok")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hns", nargs="?", help="raiz do clone do hns")
    ap.add_argument("--autoteste", action="store_true")
    ap.add_argument("--seco", action="store_true", help="mede, nao escreve nada")
    a = ap.parse_args()
    if a.autoteste:
        return autoteste()
    if not a.hns:
        ap.error("informe a raiz do hns, ou use --autoteste")
    hns = os.path.abspath(a.hns)

    pg = _modulo("pg", "porta_ginasios_johto.py")
    curva = _modulo("curva", "curva_de_nivel.py")
    desenhaveis = pg.sprites_desenhaveis()
    ruins = sorted(v for v in SPRITE.values() if v not in desenhaveis)
    if ruins:
        sys.exit("ABORTADO: SPRITE aponta para sprite sem grafico: " + ", ".join(ruins))

    ctx = {
        "species": constantes("include/constants/species.h", "SPECIES_"),
        "moves": constantes("include/constants/moves.h", "MOVE_"),
        "itens": constantes("include/constants/items.h", "ITEM_"),
        "classes": constantes("include/constants/trainers.h", "TRAINER_CLASS_"),
        "pics": constantes("include/constants/trainers.h", "TRAINER_PIC_"),
    }

    def resolve(valor, tabela, existentes, rotulo, avisos):
        for tentativa in (tabela.get(valor), valor, (valor or "") + "_FRLG"):
            if tentativa and tentativa in existentes:
                return tentativa
        avisos.append(f"{rotulo}: {valor} sem equivalente nesta build")
        return None

    grupos = json.load(open(os.path.join(REPO, "data/maps/map_groups.json")))
    mapas = [m for g in grupos["group_order"] if g.endswith("_Johto")
             for m in grupos[g]]

    fonte_times = times_do_hns(hns)
    globais = textos_ja_nossos()

    # Ja tem bloco em trainers.party FORA deste acervo: nao mexer.
    anterior = le(PARTY).split(f"/*{MARCA}")[0]
    ja_tem = set(re.findall(r"^=== (TRAINER_[A-Z0-9_]+) ===", anterior, re.M))
    ids_atuais = {n: int(v) for n, v in re.findall(
        r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$", le(HEADER), re.M)}

    # --- passada 1: descobrir quem entra, por mapa ---
    plano, pendencias, avisos = [], [], []
    for mapa in mapas:
        nosso = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        origem = os.path.join(hns, "data/maps", mapa, "scripts.inc")
        if not os.path.exists(origem):
            continue
        if len(le(nosso).splitlines()) > 3:
            continue  # ja portado por outra ferramenta: nao tocar
        fonte = le(origem)
        if "trainerbattle_" not in fonte:
            continue
        blocos = blocos_de_script(fonte)
        textos = textos_do_hns(fonte)
        objetos = {o.get("script"): o for o in json.load(
            open(os.path.join(hns, "data/maps", mapa, "map.json")))["object_events"]}

        itens = []
        for rotulo, corpo in blocos.items():
            b = batalha_simples(corpo)
            if b is None:
                if re.search(r"^\s*trainerbattle_", corpo, re.M):
                    pendencias.append(f"{mapa}/{rotulo}: batalha dentro de cena, nao portada")
                continue
            tipo, tr, args = b
            obj = objetos.get(rotulo)
            if obj is None:
                pendencias.append(f"{mapa}/{rotulo}: sem NPC no map.json do hns")
                continue
            if tr not in fonte_times or not fonte_times[tr]["mons"]:
                pendencias.append(f"{mapa}/{rotulo}: {tr} sem time no hns, nao inventado")
                continue
            itens.append(dict(rotulo=rotulo, tipo=tipo, tr=tr, args=args, obj=obj,
                              depois=depois_da_batalha(corpo)))
        if itens:
            plano.append((mapa, itens, textos))

    # Nome nosso para cada treinador do hns. Prefixo JOHTO_ obrigatorio: e por
    # ele que curva_de_nivel.py sabe a regiao, e sem ele TRAINER_JOEY colidiria
    # com nome de Hoenn.
    nome_nosso = {}
    for _, itens, _ in plano:
        for it in itens:
            nome_nosso.setdefault(it["tr"], "TRAINER_JOHTO_" + it["tr"][len("TRAINER_"):])
    colide = [n for n in nome_nosso.values() if n in ids_atuais or n in ja_tem]
    if colide:
        sys.exit("ABORTADO: nome ja existe: " + ", ".join(sorted(colide)))

    lo, hi = FAIXA
    if len(nome_nosso) > hi - lo + 1:
        sys.exit(f"ABORTADO: {len(nome_nosso)} treinadores nao cabem em {lo}..{hi}. "
                 f"Faltam {len(nome_nosso) - (hi - lo + 1)} vagas.")
    ocupados = {i for n, i in ids_atuais.items() if n in ja_tem}
    livres = [i for i in range(lo, hi + 1) if i not in ocupados]
    novos = {nome_nosso[t]: livres[i] for i, t in enumerate(nome_nosso)}

    # --- curva de nivel ---
    # A faixa de origem sai dos NIVEIS DO HNS de todos os treinadores citados por
    # mapa de Johto (ginasios inclusive), nao so dos que entram agora: assim o
    # treinador de rota nova cai no mesmo lugar relativo em que os ginasios ja
    # portados cairam, e a forma da curva do HGSS e preservada.
    # Quem NAO entra fica de fora da conta: TRAINER_RED, do cume do Mt. Silver,
    # tem mon de nivel 93 no hns e e cena, nao rota. Com ele na faixa de origem o
    # divisor dobra e Johto inteira desce para o meio da faixa: o topo de 100
    # ficaria reservado para um treinador que nao existe nesta ROM.
    todos_hns = set(nome_nosso) | set(pg.TRAINER)
    niveis = [int(m["lvl"]) for t in todos_hns if t in fonte_times
              for m in fonte_times[t]["mons"] if m["lvl"]]
    origem_faixa = (min(niveis), max(niveis))
    destino = curva.ALVO["Johto"]

    # --- passada 2: escrever ---
    linhas_party, resumo = [], []
    for tr, meu in nome_nosso.items():
        t = fonte_times[tr]
        classe = resolve(t["class"], CLASSE, ctx["classes"], f"classe de {tr}", avisos)
        pic = resolve(t["pic"], PIC, ctx["pics"], f"pic de {tr}", avisos)
        if not pic:
            pendencias.append(f"{tr}: sem pic utilizavel, nao portado")
            continue
        L = [f"=== {meu} ===", f"Name: {t['name'].title()}"]
        if classe:
            L.append(f"Class: {classe}")
        L.append(f"Pic: {pic}")
        itens_ok = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx["itens"]]
        if itens_ok:
            L.append("Items: " + " / ".join(itens_ok))
        L.append("Double Battle: " + ("Yes" if t["double"] else "No"))

        macro = t["macro"] or "NO_ITEM_DEFAULT_MOVES"
        usa_item = macro.startswith("ITEM_")
        usa_moves = macro.endswith("CUSTOM_MOVES")
        for mon in t["mons"]:
            if mon["species"] not in ctx["species"]:
                avisos.append(f"{tr}: especie {mon['species']} nao existe aqui")
                continue
            cabeca = mon["species"]
            if usa_item and mon["item"] and mon["item"] != "ITEM_NONE" \
                    and mon["item"] in ctx["itens"]:
                cabeca += f" @ {mon['item']}"
            nivel = curva.transforma(int(mon["lvl"] or 5), origem_faixa, destino)
            L += ["", cabeca, f"Level: {nivel}"]
            v = min(31, int(mon["iv"] or 0) * 31 // 255)
            L.append(f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe")
            if usa_moves:
                for mv in mon["moves"]:
                    mv = RENOMEIA_MOVE.get(mv, mv)
                    if mv == "MOVE_NONE":
                        continue
                    if mv not in ctx["moves"]:
                        avisos.append(f"{tr}: golpe {mv} nao existe aqui")
                        continue
                    L.append(f"- {mv}")
        linhas_party += L + [""]

    entraram = {n for n in novos if any(
        l == f"=== {n} ===" for l in linhas_party)}
    novos = {n: i for n, i in novos.items() if n in entraram}

    for mapa, itens, textos in plano:
        linhas = [
            f"@ Treinadores de rota de {mapa}, portados de fontes-mapas/hns por",
            "@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.",
            "",
            f"{mapa}_MapScripts::",
            "\t.byte 0",
            "",
        ]
        usados, n_ok = {}, 0
        objetos_novos = {}

        def texto(rotulo_hns, sufixo, fallback):
            if rotulo_hns in globais:
                return rotulo_hns  # texto compartilhado que ja existe aqui
            corpo = textos.get(rotulo_hns)
            rot = f"{mapa}_Text_{sufixo}"
            if corpo is None:
                corpo = f'\t.string "{fallback}$"'
                avisos.append(f"{mapa}: texto {rotulo_hns} nao achado, fallback")
            usados[rot] = pg.limpa(corpo)
            return rot

        for it in itens:
            meu = nome_nosso[it["tr"]]
            if meu not in novos:
                continue
            nome = re.sub(r".*EventScript_", "", it["rotulo"])
            script = f"{mapa}_EventScript_{nome}"
            t_visto = texto(it["args"][0], nome + "Seen", "Let's battle!")
            t_venc = texto(it["args"][1], nome + "Beaten", "I lost!")
            linhas.append(f"{script}::")
            if it["tipo"] == "double":
                t_poucos = (texto(it["args"][2], nome + "NotEnough",
                                  "You need two POKeMON!")
                            if len(it["args"]) > 2 else f"{mapa}_Text_{nome}NotEnough")
                if len(it["args"]) <= 2:
                    usados[t_poucos] = '\t.string "You need two POKeMON to battle!$"'
                linhas.append(
                    f"\ttrainerbattle_double {meu}, {t_visto}, {t_venc}, {t_poucos}")
            else:
                linhas.append(f"\ttrainerbattle_single {meu}, {t_visto}, {t_venc}")
            if it["depois"]:
                linhas.append(
                    f"\tmsgbox {texto(it['depois'], nome + 'After', 'Good battle.')}, "
                    "MSGBOX_AUTOCLOSE")
            linhas += ["\tend", ""]

            gfx = SPRITE.get(it["obj"]["graphics_id"], it["obj"]["graphics_id"])
            if gfx not in desenhaveis:
                avisos.append(f"{mapa}: sprite {it['obj']['graphics_id']} sem grafico, "
                              "virou MAN_1")
                gfx = "OBJ_EVENT_GFX_MAN_1"
            objetos_novos[(it["obj"]["x"], it["obj"]["y"])] = dict(
                graphics_id=gfx,
                movement_type=it["obj"].get("movement_type", "MOVEMENT_TYPE_FACE_DOWN"),
                movement_range_x=it["obj"].get("movement_range_x", 0),
                movement_range_y=it["obj"].get("movement_range_y", 0),
                trainer_type=it["obj"].get("trainer_type", "TRAINER_TYPE_NORMAL"),
                trainer_sight_or_berry_tree_id=it["obj"].get(
                    "trainer_sight_or_berry_tree_id", "0"),
                script=script)
            n_ok += 1

        for rot, corpo in usados.items():
            linhas += [f"{rot}:", corpo, ""]

        caminho_json = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(caminho_json))
        casados = 0
        for o in d["object_events"]:
            novo = objetos_novos.get((o["x"], o["y"]))
            if novo:
                o.update(novo)
                casados += 1
        if casados != len(objetos_novos):
            avisos.append(f"{mapa}: {len(objetos_novos) - casados} NPC sem casar por "
                          "coordenada no nosso map.json")
        if a.seco:
            resumo.append(f"{mapa}: {n_ok} treinadores, {casados} NPCs (seco)")
            continue
        json.dump(d, open(caminho_json, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        open(os.path.join(REPO, "data/maps", mapa, "scripts.inc"), "w",
             encoding="utf-8").write("\n".join(linhas).rstrip("\n") + "\n")
        resumo.append(f"{mapa}: {n_ok} treinadores, {casados} NPCs")

    if not a.seco:
        # Ler ANTES de abrir para escrita. Numa linha so, `open(PARTY,"w")` e
        # avaliado primeiro, trunca o arquivo, e o le(PARTY) de dentro leria zero
        # byte: os 2202 blocos anteriores sumiriam e sobrariam so os 144 novos.
        # Aconteceu nesta sessao, exatamente assim.
        antes_n = len(re.findall(r"^=== TRAINER_", le(PARTY), re.M))
        saida = troca_acervo(le(PARTY), linhas_party, MARCA)
        # Cinto de seguranca: o acervo so pode CRESCER. Se o corte comer bloco de
        # outra frente, o gcc nao reclama, o jogo nao trava, e o treinador errado
        # so aparece na ROM. Barato de conferir, caro de descobrir depois.
        depois_n = len(re.findall(r"^=== TRAINER_", saida, re.M))
        if depois_n < antes_n:
            sys.exit(f"ABORTADO: trainers.party cairia de {antes_n} para {depois_n} "
                     "blocos. Nada foi escrito.")
        open(PARTY, "w", encoding="utf-8").write(saida)
        escreve_defines(novos)

    for r in resumo:
        print(r)
    print(f"\nportados: {len(novos)} treinadores em {len(resumo)} mapas")
    if novos:
        print(f"ids {min(novos.values())}..{max(novos.values())} (faixa {lo}..{hi})")
    print(f"nivel: origem hns {origem_faixa[0]}..{origem_faixa[1]} -> "
          f"{destino[0]}..{destino[1]}")
    if pendencias:
        print(f"\nPENDENCIAS ({len(pendencias)}):")
        for p in pendencias:
            print("  ", p)
    if avisos:
        print(f"\nAVISOS ({len(set(avisos))}):")
        for x in sorted(set(avisos)):
            print("  ", x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
