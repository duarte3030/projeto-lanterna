#!/usr/bin/env python3
"""Devolve a Johto as placas que a importação não trouxe, com o script junto.

MEDIDO em 22/08/2026 com `dev_scripts/completude.py`: Johto tem 487 `bg_events`
contra 506 da fonte (96,2%). O buraco está em SETE mapas, e nenhuma das 24 que
faltam é placa de texto solto: todas têm mecânica atrás (o painel de cartão da
Torre Rádio, os três interruptores do subterrâneo, a porta do porão, o santuário
de Ilex e os oito painéis das Ruínas de Alph).

POR QUE ESTE GERADOR COPIA EM VEZ DE ESCREVER

A fonte `fontes-mapas/hns` é um hack de gen 3 baseado em pokeemerald, ou seja o
`scripts.inc` dela é assembly do MESMO dialeto que o nosso. Reescrever esses
scripts à mão seria reescrever conteúdo que já existe pronto, com chance de
errar um `setmetatile` e só descobrir dentro do jogo. Então o gerador PORTA por
FECHO TRANSITIVO DE RÓTULO, a mesma técnica do `restaura_npcs_johto.fecho()`:

1. parte dos rótulos que as placas apontam;
2. varre o corpo de cada um atrás de rótulos definidos no MESMO arquivo da
   fonte e os arrasta junto, até fechar;
3. **confere todo símbolo de FORA do pacote contra ESTE repo** (flag, var,
   item, special, movimento, rótulo comum). Um símbolo que não existe aqui
   REPROVA o mapa inteiro, com o nome do símbolo no relatório. Nada entra pela
   metade: rótulo solto derruba o build, e símbolo silenciosamente ausente é
   pior, porque compila e faz a coisa errada.

Os `setmetatile` vêm com os ids da fonte, e isso é seguro por MEDIÇÃO e não por
fé: os `map.bin` de Johto são byte a byte os do hns (o `--demo` remede o md5 dos
mapas tocados a cada execução), então id de metatile daqui é id de metatile de
lá.

AS FLAGS

As que os scripts pedem e que não existem aqui nascem apelidando `FLAG_UNUSED`
que já existe, na faixa de transbordo de Johto (0x1D0E em diante, declarada na
seção 0.a do `PENDENCIAS-JOHTO.md`). `FLAGS_COUNT` não muda, então a save fica
intacta. O `flags.h` é escrito DEPOIS de reler o arquivo, porque há outros
executores nesta árvore.

O QUE FICA DE FORA, com número e motivo

- `GoldenrodCity_House1`, 3 placas: as três dependem de `special` que este motor
  não tem (`NameRival` e `ToggleShinyColors`, conferido por grep em
  `data/specials.inc`). Portar a caixa de texto sem o special prometeria ao
  jogador uma tela que não existe.

Uso:
    python3 dev_scripts/completa_placas_johto.py            # só relata
    python3 dev_scripts/completa_placas_johto.py --aplica   # escreve
    python3 dev_scripts/completa_placas_johto.py --demo     # autoteste
"""
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_npcs_johto as RN  # noqa: E402  HNS
import restaura_gfx_johto as RG   # noqa: E402  grava_como_estava

HNS = RN.HNS
APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

FLAGS_H = os.path.join(REPO, "include/constants/flags.h")
MARCA = "@ Placas e mecanica portadas do hns por completa_placas_johto.py"
MARCA_C = "// PLACAS DE JOHTO (dev_scripts/completa_placas_johto.py)"

# Mapas que este gerador NAO toca, com o motivo medido.
PULA = {
    "GoldenrodCity_House1":
        "as 3 placas dependem dos specials NameRival e ToggleShinyColors, "
        "que nao existem em data/specials.inc deste repo",
}

# Flags que os scripts portados pedem e que este repo ainda nao tem. O gerador
# so cria a que faltar, e sempre apelidando FLAG_UNUSED existente.
FLAGS_PEDIDAS = [
    ("FLAG_UNLOCKED_GOLDENROD_UNDERGROUND_DOOR",
     "porta do porao do subterraneo de Goldenrod, aberta com a BASEMENT KEY"),
    ("FLAG_HIDE_RADIOTOWER_GATE",
     "o portao do 3F da Torre Radio ja foi aberto com o CARD KEY"),
    ("FLAG_GOLDENROD_SWITCH_1", "interruptor 1 do subterraneo, ligado"),
    ("FLAG_GOLDENROD_SWITCH_2", "interruptor 2 do subterraneo, ligado"),
    ("FLAG_GOLDENROD_SWITCH_3", "interruptor 3 do subterraneo, ligado"),
    ("FLAG_GOLDENROD_SWITCH_ORDER",
     "a ordem 3-2-1 dos interruptores esta sendo respeitada ate aqui"),
    ("FLAG_COMPLETED_SWITCHES",
     "os tres interruptores foram acertados na ordem e o caminho ficou aberto"),
    ("FLAG_COMPLETED_HOOH_PUZZLE", "quebra-cabeca do HO-OH das Ruinas de Alph"),
    ("FLAG_COMPLETED_KABUTO_PUZZLE", "quebra-cabeca do KABUTO"),
    ("FLAG_COMPLETED_OMANYTE_PUZZLE", "quebra-cabeca do OMANYTE"),
    ("FLAG_COMPLETED_AERODACTYL_PUZZLE", "quebra-cabeca do AERODACTYL"),
    ("FLAG_HOOH_BROUGHT", "o premio da camara do HO-OH ja foi entregue"),
    ("FLAG_KABUTO_BROUGHT", "o premio da camara do KABUTO ja foi entregue"),
    ("FLAG_OMANYTE_BROUGHT", "o premio da camara do OMANYTE ja foi entregue"),
    ("FLAG_AERODACTYL_BROUGHT", "o premio da camara do AERODACTYL ja foi "
                                "entregue"),
    ("FLAG_ITEM_DOME_FOSSIL", "fossil DOME do RuinsOfAlph_B1F, escondido ate "
                              "o quebra-cabeca do KABUTO cair"),
    ("FLAG_ITEM_HELIX_FOSSIL", "fossil HELIX, escondido ate o do OMANYTE"),
    ("FLAG_ITEM_OLD_AMBER", "AMBAR ANTIGO, escondido ate o do AERODACTYL"),
    ("FLAG_ITEM_GS_BALL", "premio da camara do HO-OH. NAO tem objeto ainda: "
                          "ITEM_GS_BALL nao existe nesta build e a decisao e "
                          "do Gui (ver johto:gs_ball:ruins_of_alph na fila). "
                          "O clearflag da cena e no-op ate la, de proposito"),
]

# Vars que os scripts portados pedem. Mesma regra das flags: apelido de
# VAR_UNUSED que ja existe, VARS_COUNT intacto, save intacta.
VARS_PEDIDAS = [
    ("VAR_RUINSOFALPH_STATE",
     "camaras das Ruinas de Alph: 1 assim que um quebra-cabeca cai"),
]

# Ajuste por mapa, quando a placa NAO pode entrar com o script da fonte inteiro.
# Cada entrada diz o que muda e por quê; sem entrada, o porte é literal.
EXTRA = {
    "IlexForest": dict(
        # A fonte manda o santuário para a cena do CELEBI quando
        # `VAR_AZALEA_TOWN_STATE == 9`, e essa cena depende da GS Ball, que é
        # linha de fila aberta (`johto:gs_ball:ruins_of_alph`) porque
        # `ITEM_GS_BALL` não existe nesta build. Então entra só o ramo
        # incondicional, que é a descrição do santuário, com o TEXTO da fonte.
        raizes=["IlexForest_Text_Shrine"],
        troca={(32, 36): "IlexForest_EventScript_Santuario"},
        corpo=("IlexForest_EventScript_Santuario::\n"
               "\tlock\n"
               "\tmsgbox IlexForest_Text_Shrine, MSGBOX_DEFAULT\n"
               "\tclosemessage\n"
               "\trelease\n"
               "\tend\n"),
        nota="só o ramo do santuário; a cena do CELEBI espera a GS Ball"),
    "RuinsOfAlph_PuzzleAndRewardChambers": dict(
        # Os três fósseis são o PRÊMIO dos quebra-cabeças e moram noutro mapa
        # (`RuinsOfAlph_B1F`), hoje como bola muda sem flag: sem eles, resolver
        # o quebra-cabeça não entrega nada.
        # Os rotulos dos fosseis moram no scripts.inc do B1F, e nao no deste
        # mapa (a fonte os batizou com o prefixo da camara e guardou noutro
        # arquivo). Sem `defs_extra` o fecho nao os achava e o `objetos` abaixo
        # ligava o objeto a um rotulo que ninguem definia: erro de LINK, nao de
        # compilacao, e foi assim que ele apareceu em 22/08/2026.
        defs_extra=["RuinsOfAlph_B1F"],
        raizes=["RuinsOfAlph_PuzzleAndRewardChambers_EventScript_DomeFossil",
                "RuinsOfAlph_PuzzleAndRewardChambers_EventScript_OldAmber",
                "RuinsOfAlph_PuzzleAndRewardChambers_EventScript_HelixFossil"],
        objetos=[
            ("RuinsOfAlph_B1F", 21, 4,
             "RuinsOfAlph_PuzzleAndRewardChambers_EventScript_DomeFossil",
             "FLAG_ITEM_DOME_FOSSIL"),
            ("RuinsOfAlph_B1F", 21, 21,
             "RuinsOfAlph_PuzzleAndRewardChambers_EventScript_OldAmber",
             "FLAG_ITEM_OLD_AMBER"),
            ("RuinsOfAlph_B1F", 5, 21,
             "RuinsOfAlph_PuzzleAndRewardChambers_EventScript_HelixFossil",
             "FLAG_ITEM_HELIX_FOSSIL"),
        ],
        nota="os 3 fósseis do B1F ganham script e flag; a GS Ball não"),
}

# Palavra que aparece no corpo de um script e que NAO e simbolo para conferir:
# opcode, macro de montador, registrador de script, numero e afins.
RUIDO = re.compile(r"^(0x[0-9A-Fa-f]+|\d+|[-+]?\d+|TRUE|FALSE|NULL|"
                   r"MSGBOX_\w+|FADE_\w+|CRY_MODE_\w+|DIR_\w+|B_OUTCOME_\w+|"
                   r"byte|2byte|4byte|string|align|set|incbin)$")


def blocos(texto):
    """{rotulo: corpo} de um scripts.inc, aceitando `X::` e `X:`."""
    saida, atual, corpo = {}, None, []
    for linha in texto.splitlines():
        m = re.match(r"^(\w+)::?\s*(@.*)?$", linha)
        if m:
            if atual:
                saida[atual] = "\n".join(corpo)
            atual, corpo = m.group(1), []
            saida.setdefault(atual, "")
            continue
        if atual is not None:
            corpo.append(linha)
    if atual:
        saida[atual] = "\n".join(corpo)
    return saida


def ordem_dos_blocos(texto):
    return [m.group(1) for m in re.finditer(r"^(\w+)::?\s*(@.*)?$", texto,
                                            re.M)]


def simbolos_do_repo(_cache=set()):
    """Tudo que ESTE repo define e que um script portado pode citar."""
    if _cache:
        return _cache
    for base, exts in ((os.path.join(REPO, "include"), (".h",)),
                       (os.path.join(REPO, "data"), (".inc", ".s")),
                       (os.path.join(REPO, "asm"), (".inc", ".s"))):
        for raiz, _, arquivos in os.walk(base):
            for nome in arquivos:
                if not nome.endswith(exts):
                    continue
                with open(os.path.join(raiz, nome), encoding="utf-8",
                          errors="replace") as f:
                    txt = f.read()
                _cache.update(re.findall(r"^#define\s+(\w+)", txt, re.M))
                _cache.update(re.findall(r"^(\w+)::?\s*$", txt, re.M))
                _cache.update(re.findall(r"^\s*\.macro\s+(\w+)", txt, re.M))
                _cache.update(re.findall(r"^\s*def_special\s+(\w+)", txt, re.M))
                # movimento: `create_movement_action step_end, ...` em
                # asm/macros/movement.inc define a macro `step_end` por outra
                # macro, entao `.macro` sozinho nao a enxerga.
                _cache.update(re.findall(
                    r"^\s*create_movement_action\s+(\w+)", txt, re.M))
                _cache.update(re.findall(r"^\s*(\w+)\s*[,=]", txt, re.M))
    return _cache


def citados(corpo):
    """Identificadores citados no corpo, já sem ruído de sintaxe.

    As três limpezas abaixo custaram uma rodada de falso negativo cada, em
    22/08/2026, quando o gerador recusou cinco mapas por "símbolo que este repo
    não tem: CARD, It, KEY, The, x378":

    1. **Texto de diálogo não é código.** Toda `"..."` sai antes de tokenizar,
       senão cada palavra da fala vira símbolo inexistente.
    2. **Hexadecimal não é identificador.** `0x378` tokeniza como `x378` se o
       número não sair antes.
    3. **Comentário `@` também não é código.**
    """
    corpo = "\n".join(l.split("@")[0].split("//")[0]
                      for l in corpo.splitlines())
    corpo = re.sub(r'"(?:[^"\\]|\\.)*"', " ", corpo)
    corpo = re.sub(r"\b0[xX][0-9A-Fa-f]+\b", " ", corpo)
    fora = set()
    for tok in re.findall(r"[A-Za-z_]\w*", corpo):
        if RUIDO.match(tok):
            continue
        fora.add(tok)
    return fora


def fecho(raizes, defs):
    """Pacote fechado a partir das raízes, e o que ele cita de fora."""
    pendentes, pacote = list(raizes), []
    vistos = set()
    externos = set()
    while pendentes:
        r = pendentes.pop(0)
        if r in vistos:
            continue
        vistos.add(r)
        if r not in defs:
            externos.add(r)
            continue
        pacote.append(r)
        for tok in citados(defs[r]):
            if tok in defs:
                pendentes.append(tok)
            else:
                externos.add(tok)
    return pacote, externos


def placas_que_faltam(mapa):
    """bg_events da fonte sem par nosso na coordenada, na ordem da fonte."""
    nosso = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
    fonte = json.load(open(os.path.join(HNS, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
    tem = {(b["x"], b["y"]) for b in nosso["bg_events"]}
    return nosso, [b for b in fonte["bg_events"] if (b["x"], b["y"]) not in tem]


def mapas_com_buraco():
    saida = []
    for mapa in sorted(RN.mapas_de_johto()):
        p = os.path.join(HNS, "data/maps", mapa, "map.json")
        if not os.path.exists(p):
            continue
        try:
            _, faltam = placas_que_faltam(mapa)
        except (OSError, KeyError):
            continue
        if faltam:
            saida.append(mapa)
    return saida


def monta():
    conhecidos = simbolos_do_repo()
    # As flags que ESTE gerador vai criar contam como conhecidas.
    conhecidos = (conhecidos | {n for n, _ in FLAGS_PEDIDAS}
                  | {n for n, _ in VARS_PEDIDAS})
    plano, relato, flags_usadas = {}, [], set()
    # Os mapas de EXTRA entram SEMPRE, mesmo sem placa faltando: eles tambem
    # carregam rotulo e objeto de OUTRO mapa (os 3 fosseis do B1F), e uma
    # segunda rodada precisa poder completar o que a primeira deixou pela
    # metade sem depender de ainda haver buraco de placa.
    for mapa in sorted(set(mapas_com_buraco()) | set(EXTRA)):
        if mapa not in PULA and not os.path.exists(
                os.path.join(HNS, "data/maps", mapa, "map.json")):
            continue
        nosso, faltam = placas_que_faltam(mapa)
        if mapa in PULA:
            relato.append((mapa, 0, len(faltam), PULA[mapa]))
            continue
        fonte_inc = os.path.join(HNS, "data/maps", mapa, "scripts.inc")
        if not os.path.exists(fonte_inc):
            relato.append((mapa, 0, len(faltam), "a fonte nao tem scripts.inc"))
            continue
        texto = open(fonte_inc, encoding="utf-8").read()
        extra = EXTRA.get(mapa, {})
        for outro in extra.get("defs_extra", []):
            outro_inc = os.path.join(HNS, "data/maps", outro, "scripts.inc")
            if os.path.exists(outro_inc):
                texto += "\n" + open(outro_inc, encoding="utf-8").read()
        defs = blocos(texto)
        troca = extra.get("troca", {})
        raizes = []
        for b in faltam:
            r = troca.get((b["x"], b["y"]), b.get("script"))
            if r not in (None, "NULL", "0") and r in defs:
                raizes.append(r)
        raizes += [r for r in extra.get("raizes", []) if r in defs]
        pacote, externos = fecho(raizes, defs)
        # o corpo escrito a mao (quando existe) tambem cita simbolos
        externos |= citados(extra.get("corpo", ""))
        nosso_inc = open(os.path.join(REPO, "data/maps", mapa, "scripts.inc"),
                         encoding="utf-8").read()
        ja_temos = set(blocos(nosso_inc))
        # rotulo que ESTE repo ja define nao entra de novo: duplicata derruba
        # o build inteiro com `symbol already defined`
        pacote = [r for r in pacote if r not in ja_temos]
        conhecidos_aqui = (conhecidos | set(pacote) | ja_temos
                           | set(blocos(extra.get("corpo", ""))))
        # RÓTULO DUPLICADO derruba o build inteiro com `symbol already
        # defined`, e ja custou 134 erros numa leva de Sinnoh. `ja_temos` so
        # olha o scripts.inc DESTE mapa; aqui a conferencia e no repo inteiro.
        # Reaproveitar em silencio seria pior: o corpo daqui pode divergir do
        # corpo de la, e o mapa passaria a rodar a cena errada.
        choque = sorted(r for r in pacote if r in conhecidos and
                        r not in ja_temos)
        if choque:
            relato.append((mapa, 0, len(faltam),
                           "rotulo que este repo ja define noutro arquivo: "
                           + ", ".join(choque[:4])))
            continue
        faltantes = sorted(t for t in externos if t not in conhecidos_aqui)
        if faltantes:
            relato.append((mapa, 0, len(faltam),
                           "simbolo que este repo nao tem: "
                           + ", ".join(faltantes[:4])))
            continue
        flags_usadas |= {t for t in externos if t.startswith("FLAG_")}
        ordem = [r for r in ordem_dos_blocos(texto) if r in set(pacote)]
        vistos, ordenado = set(), []
        for r in ordem:
            if r not in vistos:
                vistos.add(r)
                ordenado.append(r)
        plano[mapa] = (nosso, faltam, ordenado, defs, texto, extra)
        nota = f"{len(ordenado)} rotulos"
        if extra.get("nota"):
            nota += " (" + extra["nota"] + ")"
        relato.append((mapa, len(faltam), 0, nota))
    return plano, relato, flags_usadas


# ------------------------------------------------------------------- flags

def cria_flags(pedidas):
    """Apelida no flags.h só as que faltam. Devolve o relato."""
    txt = open(FLAGS_H, encoding="utf-8").read()
    linhas, feito = [], []
    ocupadas = {int(h, 16) for h in
                re.findall(r"^#define\s+\w+\s+FLAG_UNUSED_0x([0-9A-Fa-f]+)",
                           txt, re.M)}
    for nome, comentario in FLAGS_PEDIDAS:
        if nome not in pedidas:
            continue
        if re.search(rf"^#define\s+{nome}\b", txt, re.M):
            feito.append(f"{nome}: ja existe")
            continue
        alvo = None
        for n in range(0x1D0E, 0x2026):
            if n in ocupadas:
                continue
            if not re.search(rf"^#define\s+FLAG_UNUSED_0x{n:X}\b", txt, re.M):
                continue
            alvo = n
            break
        if alvo is None:
            raise SystemExit("faixa de transbordo de Johto sem vaga")
        ocupadas.add(alvo)
        linhas.append(f"#define {nome:46} FLAG_UNUSED_0x{alvo:X}  "
                      f"// {comentario}")
        feito.append(f"{nome} = FLAG_UNUSED_0x{alvo:X}")
    if linhas and APLICA:
        atual = open(FLAGS_H, encoding="utf-8").read()
        bloco = ("\n" + MARCA_C + "\n"
                 "// Apelido de FLAG_UNUSED que ja existe: FLAGS_COUNT nao "
                 "muda, save intacta.\n" + "\n".join(linhas) + "\n")
        with open(FLAGS_H, "w", encoding="utf-8") as f:
            f.write(atual.rstrip("\n") + "\n" + bloco)
    return feito


def cria_vars():
    """Apelida no vars.h so as vars que faltam. Mesma regra das flags."""
    vars_h = os.path.join(REPO, "include/constants/vars.h")
    txt = open(vars_h, encoding="utf-8").read()
    ocupadas = {int(h, 16) for h in
                re.findall(r"^#define\s+\w+\s+VAR_UNUSED_0x([0-9A-Fa-f]+)",
                           txt, re.M)}
    linhas, feito = [], []
    for nome, comentario in VARS_PEDIDAS:
        if re.search(rf"^#define\s+{nome}\b", txt, re.M):
            feito.append(f"{nome}: ja existe")
            continue
        alvo = None
        for n in range(0x4110, 0x4200):
            if n in ocupadas:
                continue
            if not re.search(rf"^#define\s+VAR_UNUSED_0x{n:X}\b", txt, re.M):
                continue
            alvo = n
            break
        if alvo is None:
            raise SystemExit("sem VAR_UNUSED livre na faixa 0x4110+")
        ocupadas.add(alvo)
        linhas.append(f"#define {nome:38} VAR_UNUSED_0x{alvo:X}  "
                      f"// {comentario}")
        feito.append(f"{nome} = VAR_UNUSED_0x{alvo:X}")
    if linhas and APLICA:
        atual = open(vars_h, encoding="utf-8").read()
        bloco = ("\n" + MARCA_C + "\n"
                 "// Apelido de VAR_UNUSED que ja existe: VARS_COUNT nao muda.\n"
                 + "\n".join(linhas) + "\n")
        with open(vars_h, "w", encoding="utf-8") as f:
            f.write(atual.rstrip("\n") + "\n" + bloco)
    return feito


# ------------------------------------------------------------------ escrita

def escreve(plano):
    for mapa, (nosso, faltam, ordenado, defs, texto, extra) in plano.items():
        troca = extra.get("troca", {})
        for b in faltam:
            nosso["bg_events"].append({
                "type": "sign", "x": b["x"], "y": b["y"],
                "elevation": b.get("elevation", 0),
                "player_facing_dir": b.get("player_facing_dir",
                                           "BG_EVENT_PLAYER_FACING_ANY"),
                "script": troca.get((b["x"], b["y"]),
                                    b.get("script") or "NULL")})
        RG.grava_como_estava(
            os.path.join(REPO, "data/maps", mapa, "map.json"), nosso)

        # objetos de OUTRO mapa que a cena portada precisa ligar (os fosseis)
        for alvo_mapa, x, y, script, flag in extra.get("objetos", []):
            if script not in ordenado and script not in blocos(
                    open(os.path.join(REPO, "data/maps", alvo_mapa,
                                      "scripts.inc"), encoding="utf-8").read()):
                raise SystemExit(
                    f"{alvo_mapa} ({x},{y}) apontaria para {script}, que "
                    "ninguem define: erro de LINK garantido")
            pa = os.path.join(REPO, "data/maps", alvo_mapa, "map.json")
            da = json.load(open(pa, encoding="utf-8"))
            mudou = False
            for o in da["object_events"]:
                if (o["x"], o["y"]) == (x, y):
                    o["script"], o["flag"] = script, flag
                    mudou = True
            if mudou:
                RG.grava_como_estava(pa, da)

        ja_no_arquivo = blocos(open(
            os.path.join(REPO, "data/maps", mapa, "scripts.inc"),
            encoding="utf-8").read())
        ordenado = [r for r in ordenado if r not in ja_no_arquivo]
        if not ordenado and not (extra.get("corpo") and not set(
                blocos(extra["corpo"])) <= set(ja_no_arquivo)):
            continue
        p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        atual = open(p, encoding="utf-8").read()
        corpo = [] if MARCA in atual else [MARCA]
        for r in ordenado:
            duplo = "::" if re.search(rf"^{r}::", texto, re.M) else ":"
            corpo.append(f"{r}{duplo}")
            corpo.append(defs[r].rstrip())
        if extra.get("corpo"):
            corpo.append(extra["corpo"].rstrip())
        with open(p, "w", encoding="utf-8") as f:
            f.write(atual.rstrip("\n") + "\n\n" + "\n".join(corpo) + "\n")


def demo():
    """Autoteste: o fecho, a régua de símbolo e o md5 dos map.bin."""
    # 1. fecho: raiz que chama outro rotulo arrasta o outro junto
    defs = {"A": "\tcall B\n\tend", "B": "\tmsgbox T\n\tend", "T": "\t.string"}
    pacote, externos = fecho(["A"], defs)
    assert set(pacote) == {"A", "B", "T"}, pacote
    # opcode TAMBEM sai como externo, de proposito: ele nao e definido no
    # arquivo da fonte. O que o protege de virar falso negativo e a base de
    # simbolos do repo, que conhece as macros de `asm/macros/`.
    assert {"call", "msgbox", "end"} <= externos, externos
    assert {"call", "msgbox", "end"} <= simbolos_do_repo(), (
        "a base de simbolos do repo nao enxerga os opcodes de script")

    # 2. simbolo de fora que nao existe aqui TEM que aparecer como externo
    pacote, externos = fecho(["A"], {"A": "\tsetflag FLAG_QUE_NAO_EXISTE\n"})
    assert "FLAG_QUE_NAO_EXISTE" in externos

    # 3. a base de simbolos do repo enxerga o que ela promete enxergar
    c = simbolos_do_repo()
    for s in ("FLAG_SYS_POKEDEX_GET", "ITEM_CARD_KEY", "ITEM_BASEMENT_KEY",
              "EventScript_BookShelf", "DrawWholeMapView"):
        assert s in c, f"{s} deveria estar na base de simbolos do repo"
    assert "NameRival" not in c, "NameRival nao existe aqui; a base mentiu"

    # 4. os map.bin dos mapas tocados sao byte a byte os do hns, senao os
    #    `setmetatile` portados apontariam para outro tile
    ours = {L["id"]: L for L in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"] if L}
    theirs = {L["id"]: L for L in json.load(
        open(os.path.join(HNS, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"] if L}
    plano, relato, flags = monta()
    divergentes = []
    for mapa in plano:
        a = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))["layout"]
        b = json.load(open(os.path.join(HNS, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))["layout"]
        if a not in ours or b not in theirs:
            continue
        ha = hashlib.md5(open(os.path.join(
            REPO, ours[a]["blockdata_filepath"]), "rb").read()).hexdigest()
        hb = hashlib.md5(open(os.path.join(
            HNS, theirs[b]["blockdata_filepath"]), "rb").read()).hexdigest()
        if ha != hb:
            divergentes.append(mapa)
    assert not divergentes, (
        f"map.bin diferente do hns em {divergentes}: os setmetatile portados "
        "apontariam para outro metatile")
    for mapa, (nosso, faltam, ordenado, defs, texto, extra) in plano.items():
        for r in ordenado:
            assert r not in simbolos_do_repo(), (
                f"{mapa}: {r} ja existe no repo e sairia duplicado")
    entram = sum(a for _, a, _, _ in relato)
    print(f"demo ok: {entram} placas entrariam em {len(plano)} mapas, "
          f"{len(flags)} flags citadas, map.bin identico ao hns nos "
          f"{len(plano)} mapas tocados")


def main():
    if DEMO:
        demo()
        return 0
    plano, relato, flags = monta()
    entram = sum(a for _, a, _, _ in relato)
    fora = sum(b for _, _, b, _ in relato)
    print(f"placas que entram: {entram}   recusadas: {fora}\n")
    for mapa, a, b, nota in relato:
        marca = "OK " if a else "NAO"
        print(f"  {marca} {mapa:42} {a or b:2}  {nota}")
    print("\nflags:")
    for l in cria_flags(flags):
        print(f"   {l}")
    print("vars:")
    for l in cria_vars():
        print(f"   {l}")
    if APLICA:
        escreve(plano)
        print("\nescrito.")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
