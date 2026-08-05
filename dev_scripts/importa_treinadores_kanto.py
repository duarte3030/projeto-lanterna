#!/usr/bin/env python3
"""Porta os treinadores de Kanto do pret/pokefirered para o formato .party daqui.

Uso:
    python3 dev_scripts/importa_treinadores_kanto.py /caminho/do/pokefirered

O que faz, em duas frentes:

1. Renumera, em include/constants/opponents_frlg.h, os nomes que scripts de mapa
   realmente usam, tirando-os da faixa 0..623 (que colide com Hoenn/Johto/Sinnoh
   no MESMO espaco de ids) e jogando para 1400..1799, faixa exclusiva de Kanto.
   Sem isso, TRAINER_LEADER_BROCK vale 314, que e TRAINER_SHELBY_2, um montanhista
   de Hoenn: quem entra no ginasio de Pewter luta contra o Shelby.

2. Escreve o time de verdade de cada um em src/data/trainers.party, APENSANDO no
   fim. Nada e inventado: especie, nivel, IV, golpes e item saem iguais aos do
   pokefirered. Classe e pic sao resolvidas contra as constantes que existem
   NESTE repo, lidas em tempo de execucao, preferindo sempre o ramo _FRLG.

A lista de quem entra vem de dev_scripts/kanto_usados.txt (nome<TAB>id<TAB>mapas),
ou do caminho passado em --usados.

Modo 2 (nao precisa do clone de pokefirered):

    python3 dev_scripts/importa_treinadores_kanto.py --scripts

Porta os treinadores citados por data/scripts/trainers_frlg.inc, que e script
COMPARTILHADO (entra na ROM por data/event_scripts.s, nao e script de mapa) e por
isso ficou de fora da primeira leva. A fonte aqui e src/data/trainers_frlg.party,
que ja esta no formato certo mas NAO entra nesta ROM: src/data.c so inclui
data/trainers_frlg.h sob `#if IS_FRLG`, e esta build e Emerald. Fonte, nao
solucao. Este modo escreve um acervo separado e nao toca no da primeira leva,
para nao mexer em bloco ja provado na ROM (lideres, Elite dos Quatro, rival).
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER = os.path.join(REPO, "include/constants/opponents_frlg.h")
HEADER_PRINCIPAL = os.path.join(REPO, "include/constants/opponents.h")
PARTY = os.path.join(REPO, "src/data/trainers.party")

# Faixas exclusivas desta frente. Abaixo de 1400 e de Hoenn, Johto e Sinnoh, e
# 1800..2199 e de Unova. Kanto precisa de 474 ids e a primeira faixa so tem 400:
# em 05/08/2026 MAX_TRAINERS_COUNT_EMERALD subiu de 2200 para 2400 e a segunda
# faixa de Kanto e 2200..2399. As faixas sao consumidas na ordem, e a segunda so
# comeca quando a primeira estiver cheia.
FAIXAS = [(1400, 1799), (2200, 2399)]
ID_MIN, ID_MAX = FAIXAS[0]

MARCA = "=== ACERVO KANTO (importa_treinadores_kanto.py) ==="
# Sentinela do modo --scripts. Separada de MARCA de proposito: o corte de apensa()
# e por texto, e ja houve um estrago quando o marcador mudou de nome e a rodada
# seguinte anexou uma segunda copia de tudo. Estas duas strings sao literais fixas
# e nao derivam do nome do arquivo; mexer nelas exige mexer no .party junto.
MARCA_SCRIPTS = "=== ACERVO KANTO 2, scripts compartilhados (importa_treinadores_kanto.py) ==="

PARTY_FRLG = os.path.join(REPO, "src/data/trainers_frlg.party")
INC_SCRIPTS = os.path.join(REPO, "data/scripts/trainers_frlg.inc")

# Classe do pokefirered sem equivalente aqui, nem com sufixo _FRLG nem sem ele.
CLASSE_SUB = {
    "TRAINER_CLASS_PKMN_TRAINER": "TRAINER_CLASS_PKMN_TRAINER_1",
    "TRAINER_CLASS_PKMN_TRAINER_UNUSED": "TRAINER_CLASS_PKMN_TRAINER_2",
}

# Pic do pokefirered sem equivalente aqui.
PIC_SUB = {}

# Golpes que o expansion renomeou.
RENOMEIA_MOVE = {
    "MOVE_FAINT_ATTACK": "MOVE_FEINT_ATTACK",
    "MOVE_VICEGRIP": "MOVE_VISE_GRIP",
    "MOVE_SMELLINGSALT": "MOVE_SMELLING_SALTS",
}

AI_SUB = {
    "AI_SCRIPT_CHECK_BAD_MOVE": "AI_FLAG_CHECK_BAD_MOVE",
    "AI_SCRIPT_TRY_TO_FAINT": "AI_FLAG_TRY_TO_FAINT",
    "AI_SCRIPT_CHECK_VIABILITY": "AI_FLAG_CHECK_VIABILITY",
}


def le(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def constantes(caminho, prefixo):
    return set(re.findall(rf"\b{prefixo}[A-Z0-9_]+", le(os.path.join(REPO, caminho))))


def blocos_de_chave(corpo):
    """Os grupos {...} de primeiro nivel. Regex nao serve: o mon tem um
    `.moves = {...}` dentro, e [^{}]* nunca casa o bloco de fora."""
    fora, prof, inicio = [], 0, None
    for i, c in enumerate(corpo):
        if c == "{":
            if prof == 0:
                inicio = i + 1
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                fora.append(corpo[inicio:i])
    return fora


def parse_parties(texto):
    """symbol -> lista de mons. Resolve as macros DUMMY_* por substituicao previa."""
    dummies = {}
    for m in re.finditer(r"#define (DUMMY_\w+)\s+\\\n((?:.*\\\n)*.*)", texto):
        dummies[m.group(1)] = m.group(2).replace("\\", " ")
    saida = {}
    for m in re.finditer(
        r"static const struct TrainerMon\w+ (\w+)\[\] = \{(.*?)\n?\};", texto, re.S
    ):
        nome, corpo = m.group(1), m.group(2)
        for d, texto_d in dummies.items():
            corpo = re.sub(rf"\b{d}\b", texto_d, corpo)
        mons = []
        for b in blocos_de_chave(corpo):
            if ".species" not in b:
                continue
            campo = lambda p: (re.search(p, b).group(1) if re.search(p, b) else None)
            moves = re.search(r"\.moves\s*=\s*\{([^}]*)\}", b)
            mons.append({
                "lvl": campo(r"\.lvl\s*=\s*(\d+)"),
                "species": campo(r"\.species\s*=\s*(SPECIES_\w+)"),
                "item": campo(r"\.heldItem\s*=\s*(ITEM_\w+)"),
                "iv": campo(r"\.iv\s*=\s*(\d+)"),
                "moves": [x.strip() for x in moves.group(1).split(",")
                          if x.strip().startswith("MOVE_")] if moves else [],
            })
        saida[nome] = mons
    return saida


def parse_trainers(texto):
    saida = {}
    for m in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", texto, re.S):
        tid, corpo = m.group(1), m.group(2)
        campo = lambda p: (re.search(p, corpo).group(1)
                           if re.search(p, corpo) else None)
        itens = re.search(r"\.items\s*=\s*\{([^}]*)\}", corpo)
        saida[tid] = {
            "class": campo(r"\.trainerClass\s*=\s*(\w+)"),
            "pic": campo(r"\.trainerPic\s*=\s*(\w+)"),
            "name": campo(r'\.trainerName\s*=\s*_\("([^"]*)"\)') or "",
            "music": campo(r"(TRAINER_ENCOUNTER_MUSIC_\w+)"),
            "female": "F_TRAINER_FEMALE" in corpo,
            "double": ".doubleBattle = TRUE" in corpo,
            "ai": re.findall(r"AI_SCRIPT_\w+", corpo),
            "items": re.findall(r"ITEM_\w+", itens.group(1)) if itens else [],
            "party": campo(r"\.party\s*=\s*\w+\((\w+)\)"),
            "macro": campo(r"\.party\s*=\s*(\w+)\("),
        }
    return saida


def resolve(valor, subs, existentes):
    """Constante do pokefirered -> constante daqui. Prefere sempre o ramo _FRLG,
    porque este repo guarda a arte de Kanto sob esse sufixo."""
    if valor is None:
        return None, None
    if valor in subs:
        return subs[valor], f"{valor} -> {subs[valor]}"
    if valor + "_FRLG" in existentes:
        return valor + "_FRLG", None
    if valor in existentes:
        return valor, None
    return None, f"{valor} SEM EQUIVALENTE"


def blocos_party(nome, t, mons, ctx):
    """Um bloco .party. Devolve (linhas, avisos)."""
    avisos = []
    classe, aviso = resolve(t["class"], CLASSE_SUB, ctx["classes"])
    if aviso:
        avisos.append(f"classe: {aviso}")
    pic, aviso = resolve(t["pic"], PIC_SUB, ctx["pics"])
    if aviso:
        avisos.append(f"pic: {aviso}")
    if not pic:
        return None, avisos + [f"{nome}: sem pic utilizavel, pulado"]

    L = [f"=== {nome} ==="]
    L.append(f"Name: {t['name'].title()}")
    if classe:
        L.append(f"Class: {classe}")
    L.append(f"Pic: {pic}")
    L.append("Gender: " + ("Female" if t["female"] else "Male"))
    # encounterMusic_gender junta o jingle e o bit de sexo no mesmo campo; aqui
    # sao duas linhas. Sem esta, todo treinador de Kanto entra com o jingle padrao.
    if t["music"] and t["music"] in ctx["musicas"]:
        L.append(f"Music: {t['music']}")
    elif t["music"]:
        avisos.append(f"{nome}: musica {t['music']} nao existe aqui")
    itens = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx["itens"]]
    if itens:
        L.append("Items: " + " / ".join(itens))
    L.append("Double Battle: " + ("Yes" if t["double"] else "No"))
    ai = [AI_SUB[a] for a in dict.fromkeys(t["ai"]) if a in AI_SUB]
    if ai:
        L.append("AI: " + " / ".join(ai))

    # ITEM_* / NO_ITEM_* e *_CUSTOM_MOVES / *_DEFAULT_MOVES dizem quais campos do
    # struct valem. Sem CUSTOM_MOVES o jogo usa os 4 ultimos golpes de nivel, que
    # e exatamente o default do trainerproc: nao escrever move nenhum.
    macro = t["macro"] or "NO_ITEM_DEFAULT_MOVES"
    usa_item = macro.startswith("ITEM_")
    usa_moves = macro.endswith("CUSTOM_MOVES")

    for mon in mons:
        sp = mon["species"]
        if sp not in ctx["species"]:
            avisos.append(f"{nome}: especie {sp} nao existe aqui, mon pulado")
            continue
        cabeca = sp
        if usa_item and mon["item"] and mon["item"] != "ITEM_NONE":
            if mon["item"] in ctx["itens"]:
                cabeca += f" @ {mon['item']}"
            else:
                avisos.append(f"{nome}: item {mon['item']} nao existe aqui")
        L += ["", cabeca, f"Level: {mon['lvl'] or 5}"]
        # pokefirered guarda iv 0..255 num numero so; o .party quer 0..31 por stat.
        # A conta e a mesma do jogo: fixedIV = iv * MAX_PER_STAT_IVS / 255.
        v = min(31, int(mon["iv"] or 0) * 31 // 255)
        L.append(f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe")
        if usa_moves:
            for mv in mon["moves"]:
                mv = RENOMEIA_MOVE.get(mv, mv)
                if mv == "MOVE_NONE":
                    continue
                if mv not in ctx["moves"]:
                    avisos.append(f"{nome}: golpe {mv} nao existe aqui")
                    continue
                L.append(f"- {mv}")
    return L, avisos


def renumera(nomes_ok):
    """Reescreve os #define dos nomes portados para a faixa 1400+, na ordem em que
    aparecem no header. Devolve {nome: novo_id}."""
    texto = le(HEADER)
    ordem = [n for n in re.findall(r"^#define (TRAINER_\w+)\s", texto, re.M)
             if n in nomes_ok]
    if len(ordem) + ID_MIN > ID_MAX + 1:
        sys.exit(f"faixa {ID_MIN}..{ID_MAX} nao cabe {len(ordem)} treinadores")
    novos = {n: ID_MIN + i for i, n in enumerate(ordem)}
    def troca(m):
        nome = m.group(1)
        if nome not in novos:
            return m.group(0)
        return f"#define {nome:<42} {novos[nome]}"
    texto = re.sub(r"^#define (TRAINER_\w+)\s+(\d+)\s*$", troca, texto, flags=re.M)
    open(HEADER, "w", encoding="utf-8").write(texto)
    return novos


def apensa(linhas, marca=MARCA, fonte="pret/pokefirered"):
    """Troca UM acervo de Kanto no fim de trainers.party, sem tocar no resto.

    Sao DOIS acervos hoje, e o corte vai so do marcador pedido ate o marcador
    seguinte, nunca ate o fim do arquivo. Cortar ate o fim era o caminho para o
    estrago classico: rodar o modo antigo apagaria calado os 147 do modo
    --scripts, e o gcc so reclama muito depois, se reclamar."""
    # Ler ANTES de abrir para escrita: open(PARTY,"w") e avaliado primeiro numa
    # linha so, trunca o arquivo, e o le(PARTY) de dentro leria zero byte.
    saida = troca_acervo(le(PARTY), linhas, marca, fonte)
    open(PARTY, "w", encoding="utf-8").write(saida)


def troca_acervo(texto, linhas, marca, fonte):
    """A parte pura de apensa(), separada so para caber no --autoteste."""
    cabeca, rabo = texto, ""
    ini = texto.find(f"/*{marca}")
    if ini != -1:
        cabeca = texto[:ini]
        prox = texto.find("/*=== ACERVO KANTO", ini + 4)
        rabo = texto[prox:].strip("\n") if prox != -1 else ""
    novo = (
        f"/*{marca}\n"
        f"   Times portados de {fonte}. Nada aqui foi escrito a mao: quem\n"
        "   gera e dev_scripts/importa_treinadores_kanto.py. Rodar de novo troca so\n"
        "   este bloco. Comentario em bloco porque o formato .party nao aceita //. */\n\n"
        + "\n".join(linhas).rstrip("\n") + "\n"
    )
    return cabeca.rstrip("\n") + "\n\n" + novo + (("\n" + rabo + "\n") if rabo else "")


def autoteste():
    """Um acervo trocado nao pode levar o outro junto. Foi assim que uma rodada
    anexou copia dobrada de tudo e o gcc so acusou no fim."""
    base = "=== TRAINER_HOENN ===\nName: Hoenn\n"
    t = troca_acervo(base, ["=== TRAINER_A ==="], MARCA, "x")
    t = troca_acervo(t, ["=== TRAINER_B ==="], MARCA_SCRIPTS, "y")
    nomes = re.findall(r"^=== (TRAINER_\w+) ===", t, re.M)
    assert nomes == ["TRAINER_HOENN", "TRAINER_A", "TRAINER_B"], nomes
    # Reescrever o PRIMEIRO acervo tem que preservar o segundo, e nao duplicar nada.
    t2 = troca_acervo(t, ["=== TRAINER_C ==="], MARCA, "x")
    nomes = re.findall(r"^=== (TRAINER_\w+) ===", t2, re.M)
    assert nomes == ["TRAINER_HOENN", "TRAINER_C", "TRAINER_B"], nomes
    assert t2.count(f"/*{MARCA}") == 1 and t2.count(f"/*{MARCA_SCRIPTS}") == 1
    # E reescrever o SEGUNDO nao pode tocar no primeiro.
    t3 = troca_acervo(t2, ["=== TRAINER_D ==="], MARCA_SCRIPTS, "y")
    nomes = re.findall(r"^=== (TRAINER_\w+) ===", t3, re.M)
    assert nomes == ["TRAINER_HOENN", "TRAINER_C", "TRAINER_D"], nomes

    # As duas grafias de classe tem que dar a MESMA chave. A primeira versao
    # comparava as grafias cruas, cruzava zero classe e corrigia zero genero, sem
    # erro nenhum na saida: so o contador em zero denunciava.
    assert classe_de("Class: TRAINER_CLASS_LASS_FRLG") == classe_de("Class: Lass Frlg")
    assert e_feminina("SWIMMER_F_FRLG", {"SWIMMER_F"})
    assert not e_feminina("FISHERMAN_FRLG", {"SWIMMER_F"})
    print("autoteste ok")
    return 0


def blocos_do_party(texto):
    """nome -> corpo do bloco, de um texto no formato .party."""
    partes = re.split(r"^=== (TRAINER_[A-Z0-9_]+) ===[ \t]*$", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip("\n")
            for i in range(1, len(partes), 2)}


def classe_de(corpo):
    """Classe do bloco, normalizada. O campo `Class:` aceita as duas grafias e os
    dois arquivos usam grafias diferentes: o acervo 1 escreve
    TRAINER_CLASS_LASS_FRLG e trainers_frlg.party escreve `Lass Frlg`. Sem
    normalizar, a tabela de genero cruza zero classe."""
    m = re.search(r"^Class: (.+)$", corpo, re.M)
    if not m:
        return ""
    chave = re.sub(r"[^A-Z0-9]+", "_", m.group(1).strip().upper()).strip("_")
    return re.sub(r"^TRAINER_CLASS_", "", chave)


def classes_femininas():
    """Classes que o acervo 1 marca como Female, lidas do proprio acervo 1.

    src/data/trainers_frlg.party traz `Gender: Male` em 624 de 624 blocos, entao
    copiar o bloco cru masculiniza toda Lass, Beauty, Picnicker e Channeler de
    Kanto, enquanto os 253 do primeiro porte (vindos do pokefirered, que tem o bit
    F_TRAINER_FEMALE) estao certos. Derivado do dado, nao chutado, e classe que
    aparece com os DOIS generos no acervo 1 (Cooltrainer, Leader, Elite Four,
    Ranger, Psychic) fica de fora por ambigua. Le so o que vem ANTES do acervo 2,
    senao os blocos masculinizados que esta funcao existe para consertar entrariam
    na conta e tornariam toda classe ambigua."""
    anterior = le(PARTY).split(f"/*{MARCA_SCRIPTS}")[0]
    por_classe = {}
    for corpo in blocos_do_party(anterior).values():
        por_classe.setdefault(classe_de(corpo), set()).add(
            bool(re.search(r"^Gender: Female", corpo, re.M)))
    return {c for c, generos in por_classe.items() if generos == {True}}


def e_feminina(classe, femininas):
    """A classe, ou a mesma classe sem o sufixo _FRLG (que e so a arte de Kanto da
    mesma classe: SWIMMER_F_FRLG e a SWIMMER_F de Hoenn). Sem esse degrau, classe
    que so existe com o sufixo fica sem precedente e a Swimmer F entra masculina.
    Continua sendo dado do repo, nao chute: se a classe base tambem for ambigua ou
    inexistente, nada muda."""
    return classe in femininas or re.sub(r"_FRLG$", "", classe) in femininas


def citados_por_scripts():
    """Treinadores citados por data/scripts/trainers_frlg.inc, na ordem do arquivo.

    Essa ordem e a da historia (Rota 3 primeiro, ilhas de Sevii por ultimo), o que
    importa quando nao ha id para todos: quem entra primeiro e quem o jogador
    encontra primeiro."""
    return list(dict.fromkeys(re.findall(r"\bTRAINER_[A-Z0-9_]+\b", le(INC_SCRIPTS))))


def porta_dos_scripts():
    """Modo --scripts. Devolve o codigo de saida."""
    frlg = {n: int(v) for n, v in re.findall(
        r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$", le(HEADER), re.M)}
    # De fora do acervo 2, porque apensa() reescreve o acervo 2 inteiro: quem ja
    # esta LA DENTRO tem que ser regerado junto, senao a rodada seguinte apagaria
    # os blocos anteriores e deixaria so os novos. Idempotente: a ordem de
    # citados_por_scripts() e fixa, entao rodar de novo devolve os mesmos ids.
    anterior = le(PARTY).split(f"/*{MARCA_SCRIPTS}")[0]
    com_bloco = set(re.findall(r"^=== (TRAINER_[A-Z0-9_]+) ===", anterior, re.M))
    fonte = blocos_do_party(le(PARTY_FRLG))
    femininas = classes_femininas()

    faltam = [n for n in citados_por_scripts()
              if n in frlg and n not in com_bloco]
    sem_fonte = [n for n in faltam if n not in fonte]
    faltam = [n for n in faltam if n in fonte]

    # Vagas: id das faixas que ninguem com time proprio ja ocupa. Ocupado e quem
    # tem BLOCO, de qualquer um dos dois headers: id sem bloco e vaga vazia no
    # array, e apelido inerte nao reserva nada.
    principal = {n: int(v) for n, v in re.findall(
        r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$", le(HEADER_PRINCIPAL), re.M)}
    ocupados = {d[n] for d in (frlg, principal) for n in com_bloco if n in d}
    livres = [i for lo, hi in FAIXAS for i in range(lo, hi + 1) if i not in ocupados]
    entram, sobram = faltam[:len(livres)], faltam[len(livres):]

    linhas = []
    for nome in entram:
        corpo = fonte[nome]
        if e_feminina(classe_de(corpo), femininas):
            corpo = re.sub(r"^Gender: Male$", "Gender: Female", corpo, flags=re.M)
        linhas += [f"=== {nome} ===", corpo, ""]
    novos = dict(zip(entram, livres))

    def troca(m):
        n = m.group(1)
        return f"#define {n:<42} {novos[n]}" if n in novos else m.group(0)
    cabecalho = re.sub(r"^#define (TRAINER_\w+)\s+(\d+)\s*$", troca, le(HEADER),
                       flags=re.M)
    open(HEADER, "w", encoding="utf-8").write(cabecalho)
    apensa(linhas, MARCA_SCRIPTS, "src/data/trainers_frlg.party")

    faixas_txt = ", ".join(f"{lo}..{hi}" for lo, hi in FAIXAS)
    print(f"citados por {os.path.relpath(INC_SCRIPTS, REPO)} sem time proprio fora "
          f"deste acervo: {len(faltam) + len(sem_fonte)}")
    print(f"vagas nas faixas {faixas_txt}: {len(livres)}")
    print(f"portados: {len(entram)}"
          + (f" (ids {min(novos.values())}..{max(novos.values())})" if novos else ""))
    print(f"corrigidos para Gender: Female: "
          f"{sum(1 for n in entram if e_feminina(classe_de(fonte[n]), femininas))} "
          f"(classes {sorted(femininas)})")
    if sem_fonte:
        print(f"\nSEM FONTE em trainers_frlg.party ({len(sem_fonte)}):")
        for n in sem_fonte:
            print("  ", n)
    if sobram:
        print(f"\nFICARAM DE FORA por falta de id nas faixas {faixas_txt} "
              f"({len(sobram)}), na ordem da historia:")
        for n in sobram:
            print("  ", n)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("firered", nargs="?", help="raiz do clone de pret/pokefirered")
    ap.add_argument("--scripts", action="store_true",
                    help="porta os citados por data/scripts/trainers_frlg.inc, "
                         "usando src/data/trainers_frlg.party como fonte")
    ap.add_argument("--autoteste", action="store_true",
                    help="confere o corte dos acervos, sem tocar em arquivo")
    ap.add_argument("--usados", default=os.path.join(REPO, "dev_scripts/kanto_usados.txt"))
    a = ap.parse_args()

    if a.autoteste:
        return autoteste()
    if a.scripts:
        return porta_dos_scripts()
    if not a.firered:
        ap.error("informe a raiz do pokefirered, ou use --scripts")

    quero = [l.split("\t")[0].strip()
             for l in le(a.usados).strip().split("\n") if l.strip()]
    trainers = parse_trainers(le(os.path.join(a.firered, "src/data/trainers.h")))
    parties = parse_parties(le(os.path.join(a.firered, "src/data/trainer_parties.h")))
    ctx = {
        "species": constantes("include/constants/species.h", "SPECIES_"),
        "moves": constantes("include/constants/moves.h", "MOVE_"),
        "itens": constantes("include/constants/items.h", "ITEM_"),
        "classes": constantes("include/constants/trainers.h", "TRAINER_CLASS_"),
        "pics": constantes("include/constants/trainers.h", "TRAINER_PIC_"),
        "musicas": constantes("include/constants/trainers.h", "TRAINER_ENCOUNTER_MUSIC_"),
    }
    # So o que existe FORA do acervo desta ferramenta conta como "ja tem time":
    # o bloco que ela mesma escreveu vai ser substituido, entao nao bloqueia nada.
    anterior = le(PARTY).split(f"/*{MARCA}")[0]
    ja_tem = set(re.findall(r"^=== (TRAINER_\w+) ===", anterior, re.M))

    linhas, avisos, ok, fora = [], [], [], []
    for nome in quero:
        # Nome renomeado aqui para nao colidir com Johto: o dado esta no original.
        fonte = nome if nome in trainers else re.sub(r"_FRLG$", "", nome)
        t = trainers.get(fonte)
        if not t:
            fora.append(f"{nome}: nao existe em pokefirered")
            continue
        mons = parties.get(t["party"] or "", [])
        if not mons:
            fora.append(f"{nome}: time {t['party']} vazio em pokefirered")
            continue
        if nome in ja_tem:
            fora.append(f"{nome}: ja tem entrada em trainers.party, nao mexido")
            continue
        bloco, av = blocos_party(nome, t, mons, ctx)
        avisos += av
        if bloco is None:
            fora.append(f"{nome}: pulado")
            continue
        linhas += bloco + [""]
        ok.append(nome)

    novos = renumera(set(ok))
    apensa(linhas)

    print(f"portados: {len(ok)} de {len(quero)}")
    print(f"ids {min(novos.values())}..{max(novos.values())} (faixa {ID_MIN}..{ID_MAX})")
    if fora:
        print(f"\nFORA ({len(fora)}):")
        for f in fora:
            print("  ", f)
    if avisos:
        print(f"\nAVISOS ({len(set(avisos))}):")
        for f in sorted(set(avisos)):
            print("  ", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
