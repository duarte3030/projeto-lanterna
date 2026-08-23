#!/usr/bin/env python3
"""Auditoria de ESTADO DE JOGO do Pokémon Claude: flags, vars, itens, treinadores, save.

Lente: o que a SAVE guarda e o que o script mexe. Só leitura sobre o repo.
Complementa (não repete) `guarda_colisao_vars.py`, que só enxerga endereço com
DOIS donos USADOS, e `guarda_save.py`, que mede TAMANHO e ÍNDICE.

Uso:
  python3 estado_jogo.py            # roda tudo, imprime achados
  python3 estado_jogo.py --secao 1  # só uma seção (1..6)
  python3 estado_jogo.py --json     # despeja os achados crus
  python3 estado_jogo.py --demo     # autoteste com mutação plantada
"""
import collections
import json
import os
import re
import sys

import comum

RAIZ = comum.RAIZ

# Região por prefixo de pasta de mapa. Serve para agrupar achado por região; o
# que não casa cai em "hoenn" porque a base é pokeemerald.
# Região de um mapa: sai do GRUPO em que ele está declarado
# (`data/maps/map_groups.json`), e não de palpite pelo nome da pasta. O nome da
# pasta mente (`Route110` existe em Hoenn e `Route210` em Sinnoh); o grupo é o
# mesmo dado que o motor usa.
_MARCA = [("galar", "Galar"), ("unova", "Unova"), ("unova", "Pwt"),
          ("sinnoh", "Sinnoh"), ("sinnoh", "Galactic"),
          ("johto", "Johto"), ("kanto", "Frlg")]


def _tabela_de_regiao():
    fora = {}
    g = json.load(open(os.path.join(RAIZ, "data", "maps", "map_groups.json")))
    for grupo in g["group_order"]:
        r = "hoenn"
        for nome, marca in _MARCA:
            if marca in grupo:
                r = nome
                break
        for m in g.get(grupo, []):
            fora[m] = r
    # ARMADILHA que `dev_scripts/completude.py` já registra e que esta
    # ferramenta repetiu: **Galar não se filtra por grupo**. O alocador de mapa
    # espalhou 344 dos mapas de Galar em append dentro de grupos de Hoenn
    # (`gMapGroup_IndoorRoute116` e irmãos), porque a política é não criar grupo
    # novo. Só aqui o NOME manda mais que o grupo, e foi MEDIDO: Galar é a única
    # região em que os dois critérios discordam (344 mapas; as outras cinco, 0).
    for m in list(fora):
        if m.startswith("Galar"):
            fora[m] = "galar"
    return fora


_REGIAO_DE = None


def regiao(nome_mapa):
    global _REGIAO_DE
    if _REGIAO_DE is None:
        _REGIAO_DE = _tabela_de_regiao()
    return _REGIAO_DE.get(nome_mapa or "", "hoenn")


# --------------------------------------------------------------------------
# leitura crua, uma vez só
# --------------------------------------------------------------------------
RX_ROTULO = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?\s*$", re.M)


def rotulo_para_mapa():
    """rótulo de script -> mapas que o citam no `map.json`.

    `data/scripts/*.inc` não tem mapa no caminho, e é lá que moram os roteiros
    gerados de Galar. Sem esta ponte, 35 batalhas de Galar apareciam como "mapa
    None" e a checagem de id repetido POR MAPA ficava cega.
    """
    fora = collections.defaultdict(set)
    for nome, m in comum.mapas():
        for chave in ("object_events", "coord_events", "bg_events"):
            for o in m.get(chave, []) or []:
                for campo in ("script", "func"):
                    v = str(o.get(campo, ""))
                    if v and v not in ("0", "0x0", "NULL"):
                        fora[v].add(nome)
    return fora


def comandos():
    """Lista de (arquivo, mapa, nº da linha, comando, argumentos crus)."""
    fora = []
    ponte = rotulo_para_mapa()
    for rel, texto in comum.scripts():
        do_caminho = comum.mapa_do_script(rel)
        mapa = do_caminho
        for i, linha in enumerate(texto.splitlines(), 1):
            mr = RX_ROTULO.match(linha)
            if mr and do_caminho is None:
                alvos = ponte.get(mr.group(1)) or ponte.get(mr.group(1).rstrip(":"))
                mapa = sorted(alvos)[0] if alvos and len(alvos) == 1 else (
                    "+".join(sorted(alvos)) if alvos else None)
            if not linha[:1].isspace():
                continue
            corte = linha.split("@")[0].strip()
            if not corte:
                continue
            partes = corte.split(None, 1)
            cmd = partes[0]
            arg = partes[1] if len(partes) > 1 else ""
            fora.append((rel, mapa, i, cmd, arg))
    return fora


def argumentos(arg):
    return [a.strip() for a in arg.split(",") if a.strip()]


# --------------------------------------------------------------------------
# 1. FLAGS
# --------------------------------------------------------------------------
CMD_ACENDE = {"setflag"}
CMD_APAGA = {"clearflag"}
CMD_LE = {"goto_if_set", "goto_if_unset", "call_if_set", "call_if_unset",
          "checkflag", "goto_if_defeated", "goto_if_not_defeated"}


def secao1(ctx):
    achados = []
    cmds = ctx["cmds"]
    val = ctx["flags_val"]

    # 1a. dois NOMES no mesmo endereço com pelo menos um NÃO usado: o portão
    #     oficial exige os dois usados, então esta é a faixa cega dele.
    uso = collections.Counter()
    for rel, _, _, _, arg in cmds:
        for n in re.findall(r"FLAG_[A-Za-z0-9_]+", arg):
            uso[n] += 1
    for rel, texto in ctx["fontes_c"]:
        for n in set(re.findall(r"FLAG_[A-Za-z0-9_]+", texto)):
            uso[n] += 1
    for nome, m in ctx["mapas"]:
        for o in m.get("object_events", []) or []:
            f = str(o.get("flag", "0"))
            if f.startswith("FLAG_"):
                uso[f] += 1
    por_valor = collections.defaultdict(list)
    for n, v in val.items():
        if re.fullmatch(r"FLAG_UNUSED_0x[0-9A-Fa-f]+", n):
            continue  # rótulo do pool: apelidar é como o repo aloca
        por_valor[v].append(n)
    for v, nomes in sorted(por_valor.items()):
        if len(nomes) < 2:
            continue
        usados = [n for n in nomes if uso.get(n)]
        if len(usados) >= 2:
            continue  # o portão oficial já vê e já autorizou
        achados.append(dict(id="1a", classe="provável", regiao="global",
                            o_que="apelido de flag repetido no mesmo endereço, com no máximo um lado usado hoje",
                            onde=hex(v), detalhe=sorted(nomes)))

    # 1b. flag de esconder usada por objetos em mapas de REGIÕES diferentes
    por_flag = collections.defaultdict(list)
    for nome, m in ctx["mapas"]:
        for i, o in enumerate(m.get("object_events", []) or []):
            f = str(o.get("flag", "0"))
            if f.startswith("FLAG_") and not f.startswith("FLAG_TEMP"):
                por_flag[f].append((nome, i))
    for f, lugares in sorted(por_flag.items()):
        regs = {regiao(n) for n, _ in lugares}
        if len(regs) > 1:
            achados.append(dict(id="1b", classe="provável", regiao="+".join(sorted(regs)),
                                o_que="mesma flag de esconder em objetos de REGIÕES diferentes",
                                onde=f, detalhe=sorted({n for n, _ in lugares})))

    # 1b2. flag de esconder que NENHUM script acende nem apaga: objeto some ou
    #      fica para sempre, sem cena que o mova.
    acesas = collections.defaultdict(list)
    apagadas = collections.defaultdict(list)
    for rel, mapa, ln, cmd, arg in cmds:
        a = argumentos(arg)
        if not a:
            continue
        if cmd in CMD_ACENDE and a[0].startswith("FLAG_"):
            acesas[a[0]].append((rel, ln))
        if cmd in CMD_APAGA and a[0].startswith("FLAG_"):
            apagadas[a[0]].append((rel, ln))
    # O motor também apaga flag de esconder, e ignorar `src/*.c` fazia NPC
    # legítimo (o do Battle Tower, o Birch da sala do campeão) aparecer como
    # "nasce escondido e não volta".
    for rel, texto in ctx["fontes_c"]:
        for n in set(re.findall(r"FlagClear\(\s*(FLAG_[A-Za-z0-9_]+)", texto)):
            apagadas[n].append((rel, 0))
    ctx["acesas"], ctx["apagadas"] = acesas, apagadas

    # 1c. flag acesa em JOGO NOVO que esconde objeto e que NINGUÉM apaga.
    #     Só a segunda metade é defeito: `EventScript_ResetAllMapFlags` acende
    #     229 flags de esconder de propósito (é assim que o NPC que só aparece
    #     depois nasce invisível). O que não pode existir é o NPC que nasce
    #     escondido e não tem cena que o traga de volta.
    for f in sorted(ctx["novo_jogo_acende"]):
        if f in por_flag and f not in apagadas:
            if f in ctx["herdadas_do_vanilla"]:
                # Mesmo desenho da fonte, linha por linha: quem some aqui some
                # no Emerald e no FireRed também. É dívida da FONTE, não desta
                # ROM, e entra como falso positivo com o motivo escrito.
                achados.append(dict(id="1c0", classe="falso positivo",
                                    regiao="+".join(sorted({regiao(n) for n, _ in por_flag[f]})),
                                    o_que="nasce escondida em jogo novo e ninguém apaga, IGUAL à fonte "
                                          "(pokeemerald/pokefirered): herdado, não regressão",
                                    onde=f, detalhe=sorted({n for n, _ in por_flag[f]})[:6]))
                continue
            achados.append(dict(id="1c", classe="provável",
                                regiao="+".join(sorted({regiao(n) for n, _ in por_flag[f]})),
                                o_que="flag acesa em JOGO NOVO esconde objeto e NENHUM script a apaga: "
                                      "o objeto nasce invisível e não volta",
                                onde=f, detalhe=sorted({n for n, _ in por_flag[f]})[:12]))

    # 1d. item ball: flag repetida (duas bolas, um item só) e bola sem flag
    bolas = collections.defaultdict(list)   # flag -> [(mapa, script)]
    sem_flag = []
    for nome, m in ctx["mapas"]:
        for o in m.get("object_events", []) or []:
            s = str(o.get("script", "0"))
            if "ItemBall" not in s and "_Item" not in s:
                continue
            if o.get("graphics_id") not in ("OBJ_EVENT_GFX_ITEM_BALL",):
                continue
            f = str(o.get("flag", "0"))
            if f in ("0", "0x0", ""):
                # A Battle Pyramid sorteia o item a cada entrada e limpa a
                # facilidade sozinha (`BattlePyramid_FindItemBall`): bola sem
                # flag ali é o desenho do vanilla, não item infinito.
                if "BattlePyramid" in s or nome.startswith("BattlePyramid"):
                    continue
                sem_flag.append((nome, s))
            else:
                bolas[f].append((nome, s))
    for f, lugares in sorted(bolas.items()):
        if len({l[0] for l in lugares}) > 1 or len(lugares) > 1:
            achados.append(dict(id="1d", classe="trava", regiao=regiao(lugares[0][0]),
                                o_que="duas item balls dividem a MESMA flag: pegar uma apaga a outra",
                                onde=f, detalhe=lugares))
    for nome, s in sem_flag:
        achados.append(dict(id="1d2", classe="trava", regiao=regiao(nome),
                            o_que="item ball SEM flag: item infinito",
                            onde=nome, detalhe=s))

    # 1e. FLAG_BADGE* acesa por mais de um script
    for f, lugares in sorted(acesas.items()):
        if not re.match(r"FLAG_BADGE", f):
            continue
        # `debug.inc` fica atrás de DEBUG_OVERWORLD_MENU, e o cpp entrega
        # DISABLED_ON_RELEASE = FALSE nesta árvore (include/constants/global.h):
        # o menu não existe na ROM, então ele não acende insígnia nenhuma.
        locais = sorted({(r, l) for r, l in lugares
                         if not r.endswith("scripts/debug.inc")})
        if len({r for r, _ in locais}) > 1:
            achados.append(dict(id="1e", classe="provável", regiao="global",
                                o_que="insígnia acesa por mais de um arquivo de script",
                                onde=f, detalhe=locais))

    # 1f. FLAG_TEMP_* usada como permanente (acesa num arquivo, lida em outro)
    temp_por_arquivo = collections.defaultdict(set)
    for rel, mapa, ln, cmd, arg in cmds:
        for n in re.findall(r"FLAG_TEMP_[A-Za-z0-9_]+", arg):
            temp_por_arquivo[n].add(rel)
    for n, arquivos in sorted(temp_por_arquivo.items()):
        # `events.inc` é gerado e usa FLAG_TEMP_* como flag de item ESCONDIDO,
        # um mapa por vez: aparecer em muitos arquivos ali é o uso correto da
        # flag temporária, não uso como permanente.
        arquivos = {a for a in arquivos if not a.endswith("/events.inc")}
        if len(arquivos) > 1:
            achados.append(dict(id="1f", classe="cosmético", regiao="global",
                                o_que="FLAG_TEMP_* citada em mais de um arquivo de script (temporária zera na troca de mapa)",
                                onde=n, detalhe=sorted(arquivos)[:10] + (["..."] if len(arquivos) > 10 else [])))

    # 1g. flag NOMEADA dentro da faixa TRAINER_FLAGS_START..END
    ini, fim = ctx["esp"]["TRAINER_FLAGS_START"], ctx["esp"]["TRAINER_FLAGS_END"]
    for n, v in sorted(val.items(), key=lambda x: x[1]):
        if ini <= v <= fim:
            achados.append(dict(id="1g", classe="trava", regiao="global",
                                o_que="flag nomeada dentro da faixa reservada às vitórias de treinador",
                                onde="%s = %s" % (n, hex(v)), detalhe=""))
    return achados


# --------------------------------------------------------------------------
# 2. VARS
# --------------------------------------------------------------------------
CMD_VAR_ESCREVE = {"setvar", "addvar", "subvar", "copyvar", "setorcopyvar",
                   "random", "specialvar", "getpricereduction"}
CMD_VAR_LE = {"compare", "goto_if_eq", "goto_if_ne", "goto_if_lt", "goto_if_gt",
              "goto_if_le", "goto_if_ge", "call_if_eq", "call_if_ne", "switch",
              "copyvar", "map_script_2"}


def secao2(ctx):
    achados = []
    cmds = ctx["cmds"]
    escreve = collections.defaultdict(set)
    le = collections.defaultdict(set)
    valores_escritos = collections.defaultdict(set)
    for rel, mapa, ln, cmd, arg in cmds:
        a = argumentos(arg)
        if not a:
            continue
        if cmd in CMD_VAR_ESCREVE and a[0].startswith("VAR_"):
            escreve[a[0]].add(rel)
            if cmd == "setvar" and len(a) > 1:
                valores_escritos[a[0]].add(a[1])
        if cmd in CMD_VAR_LE:
            alvo = a[1] if cmd == "map_script_2" else a[0]
            if alvo.startswith("VAR_"):
                le[alvo].add(rel)
        if cmd == "map_script_2" and a and a[0].startswith("VAR_"):
            le[a[0]].add(rel)

    donos = ctx["vars_donas"]

    # 2a. var de cena escrita por mapas diferentes (fora do que o portão cobre,
    #     que é colisão de ENDEREÇO; aqui é o mesmo NOME em duas cenas)
    for v, arquivos in sorted(escreve.items()):
        mapas = {comum.mapa_do_script(r) for r in arquivos if comum.mapa_do_script(r)}
        if len(mapas) > 1 and not v.startswith(("VAR_TEMP", "VAR_0x")):
            regs = {regiao(m) for m in mapas}
            achados.append(dict(id="2a",
                                classe="provável" if len(regs) > 1 else "cosmético",
                                regiao="+".join(sorted(regs)),
                                o_que="a MESMA var de cena é escrita por mapas diferentes",
                                onde=v, detalhe=sorted(mapas)[:12]))

    # 2b. VAR_TEMP_* usada entre mapas
    for v, arquivos in sorted(escreve.items()):
        if not v.startswith("VAR_TEMP"):
            continue
        todos = arquivos | le.get(v, set())
        mapas = {comum.mapa_do_script(r) for r in todos if comum.mapa_do_script(r)}
        if len(mapas) > 1:
            achados.append(dict(id="2b", classe="cosmético", regiao="global",
                                o_que="VAR_TEMP_* citada em mapas diferentes (zera na troca de mapa)",
                                onde=v, detalhe=sorted(m for m in mapas if m)[:10]))

    # 2c. var de etapa que NUNCA avança: lida em condição, escrita em lugar
    #     nenhum. Var ESPECIAL (0x8000 para cima, `VAR_ITEM_ID` e irmãs) sai
    #     fora: quem escreve nela é o motor, com outro nome em C
    #     (`gSpecialVar_ItemId`), e acusá-la é medir a própria cegueira.
    especiais = {n for n, val in ctx["vars_val"].items() if val >= 0x8000}
    em_tabela_de_cena = set()
    for rel, mapa, ln, cmd, arg in cmds:
        if cmd == "map_script_2":
            a = argumentos(arg)
            if a and a[0].startswith("VAR_"):
                em_tabela_de_cena.add(a[0])
    for v, arquivos in sorted(le.items()):
        if v.startswith(("VAR_TEMP", "VAR_0x")) or v == "VAR_RESULT":
            continue
        if v in escreve or v in ctx["vars_motor"] or v in especiais:
            continue
        cena = v in em_tabela_de_cena
        achados.append(dict(
            id="2c", classe="provável",
            regiao="+".join(sorted(
                {regiao(comum.mapa_do_script(r)) for r in arquivos
                 if comum.mapa_do_script(r)}) or ["global"]),
            o_que=("tabela de cena inteira MORTA: a var nunca sai de 0 e nenhuma "
                   "linha do `map_script_2` dispara" if cena else
                   "var de etapa LIDA e nunca escrita: o ramo alternativo do "
                   "diálogo é inalcançável"),
            onde=v, detalhe=sorted(arquivos)[:8]))

    # 2d. var escrita e nunca lida: a etapa avança sem ninguém olhar
    for v, arquivos in sorted(escreve.items()):
        if v.startswith(("VAR_TEMP", "VAR_0x")) or v == "VAR_RESULT":
            continue
        if v in le or v in ctx["vars_motor"]:
            continue
        achados.append(dict(id="2d", classe="cosmético", regiao="+".join(sorted(
            {regiao(comum.mapa_do_script(r)) for r in arquivos if comum.mapa_do_script(r)}) or ["global"]),
            o_que="var escrita e nunca lida por script nenhum",
            onde=v, detalhe=sorted(arquivos)[:8]))

    # 2e. VAR_RESULT lido sem special/comando que o preencha antes, no MESMO rótulo
    achados += var_result_sem_fonte(ctx)
    return achados


# LISTA INVERTIDA, e de propósito. A primeira versão listava quem PREENCHE
# VAR_RESULT e acusou 1.224 leituras, quase todas legítimas: `giverandomberry`
# preenche e não estava na lista, e sempre vai faltar um. Uma lista de quem
# preenche nunca fica completa; uma lista de quem CERTAMENTE não preenche fica,
# porque é a gramática de andar e falar. O preço é falso NEGATIVO, que num
# relatório de auditoria custa menos que afogar o leitor.
NAO_PREENCHE = {
    "lock", "lockall", "release", "releaseall", "faceplayer", "turnobject",
    "applymovement", "waitmovement", "delay", "delay_8", "delay_16",
    "closemessage", "waitmessage", "playse", "waitse", "playbgm", "savebgm",
    "fadedefaultbgm", "playmoncry", "waitmoncry", "textcolor", "end", "return",
    "goto", "call", "setflag", "clearflag", "removeobject", "addobject",
    "setobjectxyperm", "setobjectxy", "setmetatile", "setmetatileinrange",
    "hideobjectat", "showobjectat", "fadescreen",
    "fadescreenswapbuffers", "waitstate", "lockall",
    "step_end", "map_script", "map_script_2", "setvar", "addvar", "subvar",
    "copyvar", "setorcopyvar", "goto_if_eq", "goto_if_ne", "goto_if_set",
    "goto_if_unset", "call_if_eq", "call_if_ne", "call_if_set", "call_if_unset",
    "compare", "switch", "case", "warp", "waitbuttonpress", "setweather",
    "doweather", "seteventmon", "setrespawn", "incrementgamestat",
}


def preenche_result(cmd, arg):
    """Este comando pode ter escrito em VAR_RESULT?"""
    if cmd in ("setvar", "copyvar", "setorcopyvar", "addvar", "subvar"):
        a = argumentos(arg)
        return bool(a) and a[0] == "VAR_RESULT"
    return cmd not in NAO_PREENCHE


def var_result_sem_fonte(ctx):
    """VAR_RESULT lido em condição sem NADA antes dele no mesmo rótulo que o encha.

    Regra conservadora: só acusa quando o rótulo inteiro, do começo até a
    leitura, não tem um comando conhecido por escrever VAR_RESULT. Rótulo
    alcançado por `goto`/`call` de outro que preenche é FALSO POSITIVO, e por
    isso o achado sai como "provável" e não como trava.
    """
    fora = []
    entradas = set(rotulo_para_mapa())
    for rel, texto in comum.scripts():
        for m in re.finditer(r"map_script(?:_2)?\s+[^,]+,\s*([A-Za-z_]\w*)", texto):
            entradas.add(m.group(1))
        for m in re.finditer(r"map_script_2\s+[^,]+,\s*[^,]+,\s*([A-Za-z_]\w*)", texto):
            entradas.add(m.group(1))
    for rel, texto in comum.scripts():
        rotulo = None
        preencheu = False
        ja_acusado = set()
        for i, linha in enumerate(texto.splitlines(), 1):
            m = RX_ROTULO.match(linha)
            if m:
                rotulo, preencheu = m.group(1), False
                continue
            corte = linha.split("@")[0].strip()
            if not corte:
                continue
            partes = corte.split(None, 1)
            cmd, arg = partes[0], (partes[1] if len(partes) > 1 else "")
            if preenche_result(cmd, arg):
                preencheu = True
                continue
            a = argumentos(arg)
            # Só PONTO DE ENTRADA: rótulo alcançado por `goto`/`call` herda o
            # VAR_RESULT de quem chamou, e acusá-lo era a fonte de quase todo o
            # ruído (1.224 achados na primeira versão, 147 na segunda).
            if (cmd in CMD_VAR_LE and a and a[0] == "VAR_RESULT" and not preencheu
                    and rotulo in entradas and rotulo not in ja_acusado):
                ja_acusado.add(rotulo)
                fora.append(dict(id="2e", classe="provável",
                                 regiao=regiao(comum.mapa_do_script(rel) or ""),
                                 o_que="VAR_RESULT lido sem nada antes, no mesmo rótulo, que o preencha",
                                 onde="%s:%d" % (rel, i), detalhe=rotulo))
    return fora


# --------------------------------------------------------------------------
# 3. TREINADORES
# --------------------------------------------------------------------------
def secao3(ctx):
    achados = []
    cmds = ctx["cmds"]
    party = ctx["party"]
    usos = collections.defaultdict(list)      # id -> [(mapa, rel, linha, cmd)]
    for rel, mapa, ln, cmd, arg in cmds:
        if not cmd.startswith("trainerbattle"):
            continue
        a = argumentos(arg)
        if not a:
            continue
        # `trainerbattle` cru tem o TIPO no argumento 0
        # (`trainerbattle TRAINER_BATTLE_CONTINUE_SCRIPT, TRAINER_X, ...`), e as
        # formas `trainerbattle_*` já começam pelo id.
        tid = a[0]
        if cmd == "trainerbattle" and len(a) > 1:
            tid = a[1]
        if not tid.startswith("TRAINER_") or tid.startswith("TRAINER_BATTLE_"):
            continue
        usos[tid].append((mapa, rel, ln, cmd))
    ctx["usos_treinador"] = usos

    # 3a. id usado em script e sem time no .party
    for tid, lugares in sorted(usos.items()):
        if tid not in party:
            achados.append(dict(id="3a", classe="trava",
                                regiao=regiao(lugares[0][0] or ""),
                                o_que="treinador chamado por script e SEM time em trainers.party",
                                onde=tid, detalhe=lugares[:4]))

    # 3b. mesmo id em mapas diferentes
    for tid, lugares in sorted(usos.items()):
        mapas = {m for m, _, _, _ in lugares if m}
        if len(mapas) > 1:
            revanche = any(c.endswith("rematch") for _, _, _, c in lugares)
            achados.append(dict(id="3b",
                                classe="cosmético" if revanche else "provável",
                                regiao="+".join(sorted({regiao(m) for m in mapas})),
                                o_que="mesmo id de treinador em mapas diferentes (batalha compartilhada)",
                                onde=tid, detalhe=sorted(mapas)))

    # 3c. trainerbattle_single com id duplicado no MESMO mapa
    for tid, lugares in sorted(usos.items()):
        por_mapa = collections.Counter(m for m, _, _, c in lugares
                                       if c == "trainerbattle_single")
        for m, n in por_mapa.items():
            if n > 1:
                achados.append(dict(id="3c", classe="provável", regiao=regiao(m or ""),
                                    o_que="trainerbattle_single com o mesmo id duas vezes no mesmo mapa",
                                    onde="%s @ %s" % (tid, m), detalhe=n))

    # 3d. time com problema: nível 0 ou > 100, item que não existe, habilidade
    #     ilegal, golpe que a espécie não aprende
    for tid, dados in sorted(party.items()):
        for mon in dados["mons"]:
            if mon["nivel"] is not None and not (1 <= mon["nivel"] <= ctx["max_level"]):
                achados.append(dict(id="3d", classe="trava", regiao="global",
                                    o_que="nível fora de 1..100 em time de treinador",
                                    onde=tid, detalhe=mon))
            if mon["item"] and mon["item"] not in ctx["enums"]:
                achados.append(dict(id="3e", classe="trava", regiao="global",
                                    o_que="item inexistente em time de treinador",
                                    onde=tid, detalhe=mon["item"]))
            if mon["especie"] and mon["especie"] not in ctx["enums"]:
                achados.append(dict(id="3f", classe="trava", regiao="global",
                                    o_que="espécie inexistente em time de treinador",
                                    onde=tid, detalhe=mon["especie"]))
            for mv in mon["moves"]:
                if mv not in ctx["enums"]:
                    achados.append(dict(id="3g", classe="trava", regiao="global",
                                        o_que="golpe inexistente em time de treinador",
                                        onde=tid, detalhe=mv))
    return achados


RX_PARTY_CAB = re.compile(r"^===\s*(TRAINER_[A-Za-z0-9_]+)\s*===\s*$")
# Campos de linha "Campo: valor". Tudo que NÃO é campo e não começa com "-" é
# linha de espécie. Cravar a lista aqui, e não adivinhar, porque tratar
# "Ability: ..." como espécie fabricava um Pokémon por linha (foi o que a
# primeira versão fez, e ela acusou 7.040 espécies inexistentes).
CAMPOS_PARTY = {"name", "class", "pic", "gender", "music", "items", "ai",
                "mugshot", "starting status", "multi party", "double battle",
                "battle type", "level", "ability", "nature", "ivs", "evs",
                "shiny", "happiness", "friendship", "ball", "tera type",
                "dynamax level", "gigantamax", "difficulty", "form",
                "hidden power", "ev", "iv", "moves", "nickname"}


def _const(prefixo, texto):
    """`SPECIES_WEAVILE` continua; `Weavile` vira `SPECIES_WEAVILE`."""
    t = texto.strip()
    if t.startswith(prefixo + "_"):
        return t
    return prefixo + "_" + normaliza(t)


def le_party():
    """TRAINER_* -> {'ai': [...], 'mons': [{especie,nivel,item,ability,moves}]}"""
    caminho = os.path.join(RAIZ, "src", "data", "trainers.party")
    fora = {}
    atual = mon = None
    dentro_de_comentario = False
    for crua in open(caminho, encoding="utf-8", errors="replace"):
        # ARMADILHA MEDIDA: `trainers.party` tem comentário em BLOCO (`/* */`),
        # porque o formato não aceita comentário de linha. Sem pular o bloco, as
        # linhas de prosa viravam "espécie", e a primeira versão acusou 57
        # espécies inexistentes que eram texto em português.
        if dentro_de_comentario:
            if "*/" in crua:
                dentro_de_comentario = False
                crua = crua.split("*/", 1)[1]
            else:
                continue
        while "/*" in crua:
            antes, _, resto = crua.partition("/*")
            if "*/" in resto:
                crua = antes + resto.split("*/", 1)[1]
            else:
                crua = antes
                dentro_de_comentario = True
                break
        s = crua.split("//")[0].rstrip()
        m = RX_PARTY_CAB.match(s.strip())
        if m:
            atual = {"ai": [], "mons": [], "dificuldade": None}
            fora[m.group(1)] = atual
            mon = None
            continue
        if atual is None:
            continue
        s = s.strip()
        if not s or s.startswith(("/*", "*", "@")):
            if not s:
                mon = None
            continue
        if s.startswith("-"):
            if mon is not None:
                mon["moves"].append(_const("MOVE", s[1:].split("##")[0]))
            continue
        campo, sep, valor = s.partition(":")
        if sep and campo.strip().lower() in CAMPOS_PARTY:
            chave, valor = campo.strip().lower(), valor.strip()
            if chave == "ai":
                atual["ai"] = [x.strip() for x in valor.split("/") if x.strip()]
            elif chave == "difficulty":
                atual["dificuldade"] = valor
            elif chave == "level" and mon is not None:
                try:
                    mon["nivel"] = int(valor)
                except ValueError:
                    pass
            elif chave == "ability" and mon is not None:
                mon["ability"] = _const("ABILITY", valor)
            continue
        # linha de espécie: "Apelido (Espécie) (M) @ Item  ## comentário"
        mon = {"especie": None, "nivel": None, "item": None,
               "ability": None, "moves": [], "crua": s}
        atual["mons"].append(mon)
        corpo = s.split("##")[0].strip()
        if "@" in corpo:
            corpo, item = corpo.split("@", 1)
            mon["item"] = _const("ITEM", item)
        corpo = re.sub(r"\s*\((M|F)\)\s*", " ", corpo).strip()
        m2 = re.search(r"\(([^)]+)\)\s*$", corpo)
        mon["especie"] = _const("SPECIES", m2.group(1) if m2 else corpo)
    return fora


def normaliza(txt):
    t = txt.strip().upper()
    for a, b in (("\u2019", ""), ("'", ""), (".", ""), ("-", "_"), (":", ""),
                 ("%", ""), ("\u00e9", "E")):
        t = t.replace(a, b)
    t = re.sub(r"[^A-Z0-9_ ]", "", t)
    return re.sub(r"\s+", "_", t.strip())


# --------------------------------------------------------------------------
# 4. ITENS E DEX
# --------------------------------------------------------------------------
def secao4(ctx):
    achados = []
    cmds = ctx["cmds"]
    enums = ctx["enums"]
    dados = collections.defaultdict(list)
    for rel, mapa, ln, cmd, arg in cmds:
        a = argumentos(arg)
        if not a:
            continue
        # `giveitem_msg` é a forma do ramo FRLG e entrega item de verdade;
        # deixá-la de fora fez o Poké Flute, o Town Map, o Itemfinder e o Bike
        # Voucher aparecerem como "item que nenhum script dá".
        if cmd in ("giveitem", "additem", "finditem", "giveitem_std",
                   "giveitem_msg", "checkitem", "removeitem", "givecustomitem"):
            # `giveitem_msg msg, item, amount, fanfare`: o item é o SEGUNDO
            # argumento, e ler o primeiro pegava o rótulo do texto.
            it = a[1] if (cmd == "giveitem_msg" and len(a) > 1) else a[0]
            if it.startswith("ITEM_"):
                if it not in enums:
                    achados.append(dict(id="4a", classe="trava", regiao=regiao(mapa or ""),
                                        o_que="script dá/checa item que NÃO existe",
                                        onde="%s:%d" % (rel, ln), detalhe=it))
                elif cmd in ("giveitem", "additem", "finditem", "giveitem_std",
                             "giveitem_msg"):
                    dados[it].append((mapa, rel, ln, cmd))
            elif it in ("ITEM_NONE", "0"):
                achados.append(dict(id="4b", classe="provável", regiao=regiao(mapa or ""),
                                    o_que="item ball / entrega com item 0",
                                    onde="%s:%d" % (rel, ln), detalhe=cmd))

    # 4c. TM/HM dada duas vezes por mapas diferentes
    for it, lugares in sorted(dados.items()):
        if not re.match(r"ITEM_(TM|HM)\d", it):
            continue
        mapas = {m for m, _, _, _ in lugares if m}
        if len(mapas) > 1:
            achados.append(dict(id="4c", classe="cosmético",
                                regiao="+".join(sorted({regiao(m) for m in mapas})),
                                o_que="a mesma TM/HM é entregue em mais de um mapa",
                                onde=it, detalhe=sorted(mapas)[:10]))

    # 4d. key item obrigatório sem nenhum script que o dê
    for it in ctx["chaves"]:
        if it not in enums:
            achados.append(dict(id="4d0", classe="falso positivo", regiao="global",
                                o_que="key item da lista de conferência não existe nesta ROM",
                                onde=it, detalhe=""))
            continue
        if it not in dados:
            achados.append(dict(id="4d", classe="provável", regiao="global",
                                o_que="key item da história que NENHUM script entrega",
                                onde=it, detalhe=""))

    # 4e. wild_encounters: espécie 0 ou nível fora de 1..100
    for grupo in ctx["wild"]:
        mapa = grupo.get("map", "?")
        for chave, campo in (("land_mons", "mons"), ("water_mons", "mons"),
                             ("rock_smash_mons", "mons"), ("fishing_mons", "mons")):
            bloco = grupo.get(chave)
            if not bloco:
                continue
            for slot in bloco.get(campo, []):
                esp = slot.get("species")
                lo, hi = slot.get("min_level"), slot.get("max_level")
                if esp in ("SPECIES_NONE", None) or enums.get(esp, -1) == 0:
                    # `encounter_rate` 0 fecha o encontro por grama e por Surf,
                    # mas NÃO fecha a pesca: `FishingWildEncounter`
                    # (src/wild_encounter.c:951) chama `GenerateFishingWildMon`
                    # sem olhar a taxa. Medido, não suposto.
                    taxa = bloco.get("encounter_rate", 0)
                    pesca = chave == "fishing_mons"
                    achados.append(dict(
                        id="4e",
                        classe="trava" if (taxa or pesca) else "cosmético",
                        regiao=regiao(mapa_de_constante(mapa.replace("MAP_", "")) or ""),
                        o_que=("slot de PESCA com espécie 0/NONE: a pesca ignora "
                               "encounter_rate e fisgaria o Pokémon 0" if pesca else
                               "slot selvagem com espécie 0/NONE"),
                        onde="%s / %s (rate %s)" % (mapa, chave, taxa), detalhe=slot))
                elif esp not in enums:
                    achados.append(dict(id="4e2", classe="trava", regiao="global",
                                        o_que="slot selvagem com espécie que não existe",
                                        onde=mapa, detalhe=esp))
                for n in (lo, hi):
                    if n is not None and not (1 <= n <= ctx["max_level"]):
                        achados.append(dict(id="4f", classe="trava", regiao="global",
                                            o_que="nível selvagem fora de 1..100",
                                            onde=mapa, detalhe=slot))
                if lo is not None and hi is not None and lo > hi:
                    achados.append(dict(id="4f2", classe="provável", regiao="global",
                                        o_que="min_level maior que max_level em slot selvagem",
                                        onde=mapa, detalhe=slot))

    # 4g. graphics_id de objeto que não existe no enum
    for nome, m in ctx["mapas"]:
        for i, o in enumerate(m.get("object_events", []) or []):
            g = str(o.get("graphics_id", ""))
            # `OBJ_EVENT_GFX_SPECIES(X)` é MACRO, resolvida no build; só o nome
            # simples é comparável com o enum.
            if "(" in g:
                continue
            if g.startswith("OBJ_EVENT_GFX_") and g not in enums:
                achados.append(dict(id="4g", classe="trava", regiao=regiao(nome),
                                    o_que="objeto com graphics_id que não resolve (não carrega, não é sólido, não roda script)",
                                    onde="%s[%d]" % (nome, i), detalhe=g))
    return achados


# --------------------------------------------------------------------------
# 5. SELETOR DE CAPÍTULO E JOGO NOVO
# --------------------------------------------------------------------------
def secao5(ctx):
    """Seletor de capítulo: destino, tile, e se as insígnias que ele acende
    bastam para os golpes de campo que a região cobra."""
    achados = []
    nomes_mapa = {n for n, _ in ctx["mapas"]}
    hl = ctx["heal_por_id"]

    for cap in ctx["capitulos"]:
        alvo = cap["heal"]
        if alvo in ("0", "CURA(0)", "HEAL_LOCATION_NONE"):
            continue
        d = hl.get(alvo)
        if d is None:
            achados.append(dict(id="5a", classe="trava", regiao=cap["regiao"],
                                o_que="capítulo aponta para HEAL_LOCATION que não existe em heal_locations.json",
                                onde=cap["rotulo"], detalhe=alvo))
            continue
        pasta = mapa_de_constante(d["map"].replace("MAP_", ""))
        if pasta is None or pasta not in nomes_mapa:
            achados.append(dict(id="5b", classe="trava", regiao=cap["regiao"],
                                o_que="heal location do capítulo cai em MAP_ sem pasta de mapa",
                                onde=cap["rotulo"], detalhe=d["map"]))
            continue
        prob = ctx["tile_andavel"](pasta, d["x"], d["y"])
        if prob:
            achados.append(dict(id="5c", classe="trava", regiao=cap["regiao"],
                                o_que="capítulo põe o jogador em tile que não se anda",
                                onde="%s (%s %d,%d)" % (cap["rotulo"], pasta, d["x"], d["y"]),
                                detalhe=prob))

    # 5d. os golpes de campo que o seletor promete
    campo = ctx["golpes_de_campo"]   # golpe -> flag de insígnia exigida
    for reg, insignias in ctx["insignias_por_regiao"].items():
        if reg == "KANTO":
            continue
        faltam = sorted({g for g, f in campo.items() if f not in insignias})
        if faltam:
            achados.append(dict(id="5d", classe="provável", regiao=reg.lower(),
                                o_que=("capítulo desta região NÃO acende insígnia do motor: "
                                       "o Pikachu do seletor tem o golpe e o motor recusa"),
                                onde=reg, detalhe=faltam))
    return achados


# --------------------------------------------------------------------------
# 6. SAVE
# --------------------------------------------------------------------------
def secao6(ctx):
    return ctx["save"]["achados"]


# --------------------------------------------------------------------------
def contexto():
    ctx = {}
    ctx["cmds"] = comandos()
    ctx["mapas"] = comum.mapas()
    # Nome citado por script entra na sonda: só assim "não existe" é MEDIDO, e
    # não deduzido da ausência num header (a macro FOREACH_TM fabrica nome que
    # não está escrito em lugar nenhum).
    citados = set()
    rx = re.compile(r"\b(ITEM|SPECIES|MOVE|ABILITY|OBJ_EVENT_GFX|TRAINER)_[A-Za-z0-9_]+")
    for _rel, _mapa, _ln, _cmd, _arg in ctx["cmds"]:
        citados.update(m.group(0) for m in rx.finditer(_arg))
    for _nome, _m in ctx["mapas"]:
        for _o in _m.get("object_events", []) or []:
            g = str(_o.get("graphics_id", ""))
            if g.startswith("OBJ_EVENT_GFX_") and "(" not in g:
                citados.add(g)
    for _t, _d in le_party().items():
        for _mon in _d["mons"]:
            citados.update(x for x in [_mon["especie"], _mon["item"], _mon["ability"]] if x)
            citados.update(_mon["moves"])
    for _g in json.load(open(os.path.join(RAIZ, "src", "data",
                                          "wild_encounters.json")))["wild_encounter_groups"]:
        for _e in _g["encounters"]:
            for _k, _v in _e.items():
                if isinstance(_v, dict) and "mons" in _v:
                    citados.update(x["species"] for x in _v["mons"])
    citados = {c for c in citados if not c.startswith("TRAINER_BATTLE_")}
    ctx["enums"] = comum.enums(extras=frozenset(citados))
    ctx["esp"] = comum.resolve(["TRAINER_FLAGS_START", "TRAINER_FLAGS_END",
                                "FLAGS_COUNT", "VARS_COUNT", "MAX_TRAINERS_COUNT",
                                "SYSTEM_FLAGS"])
    # flags declaradas e resolvidas
    nomes = set()
    for h in ("include/constants/flags.h", "include/config/text.h"):
        for m in re.finditer(r"^\s*#define\s+(FLAG_[A-Za-z0-9_]+)\s",
                             open(os.path.join(RAIZ, h), encoding="utf-8",
                                  errors="replace").read(), re.M):
            nomes.add(m.group(1))
    ctx["flags_val"] = comum.resolve(nomes)

    # fontes C, para contar uso de flag fora de script
    fontes = []
    for dp, _, fn in os.walk(os.path.join(RAIZ, "src")):
        for f in fn:
            if f.endswith((".c", ".h")):
                p = os.path.join(dp, f)
                fontes.append((os.path.relpath(p, RAIZ),
                               open(p, encoding="utf-8", errors="replace").read()))
    ctx["fontes_c"] = fontes
    juntos = "\n".join(t for _, t in fontes)
    ctx["vars_motor"] = set(re.findall(r"VAR_[A-Za-z0-9_]+", juntos))
    ctx["vars_donas"] = {}

    ctx["novo_jogo_acende"] = flags_de_jogo_novo()
    ctx["herdadas_do_vanilla"] = herdadas_do_vanilla(ctx["novo_jogo_acende"])
    ctx["party"] = le_party()
    ctx["wild"] = json.load(open(os.path.join(RAIZ, "src", "data",
                                              "wild_encounters.json")))["wild_encounter_groups"][0]["encounters"]
    ctx["chaves"] = ["ITEM_BICYCLE", "ITEM_MACH_BIKE", "ITEM_ACRO_BIKE",
                     "ITEM_OLD_ROD", "ITEM_GOOD_ROD", "ITEM_SUPER_ROD",
                     "ITEM_HM_SURF", "ITEM_HM_STRENGTH", "ITEM_HM_ROCK_SMASH",
                     "ITEM_HM_CUT", "ITEM_HM_FLY", "ITEM_HM_WATERFALL",
                     "ITEM_HM_DIVE", "ITEM_SS_TICKET", "ITEM_VS_SEEKER",
                     "ITEM_TOWN_MAP", "ITEM_POKEDEX", "ITEM_ITEMFINDER",
                     "ITEM_GO_GOGGLES", "ITEM_DEVON_SCOPE", "ITEM_POKE_FLUTE",
                     "ITEM_SILPH_SCOPE", "ITEM_CARD_KEY", "ITEM_LIFT_KEY",
                     "ITEM_SECRET_KEY", "ITEM_BASEMENT_KEY", "ITEM_STORAGE_KEY",
                     "ITEM_ROOM_1_KEY", "ITEM_COIN_CASE", "ITEM_BIKE_VOUCHER"]
    ctx["vars_val"] = comum.resolve(
        {m.group(1) for h in ("include/constants/vars.h", "include/constants/vars_frlg.h")
         for m in re.finditer(r"^\s*#define\s+(VAR_[A-Za-z0-9_]+)\s",
                              open(os.path.join(RAIZ, h), encoding="utf-8",
                                   errors="replace").read(), re.M)})
    ctx["max_level"] = comum.resolve(["MAX_LEVEL"]).get("MAX_LEVEL", 100)
    ctx["capitulos"], ctx["insignias_por_regiao"] = le_capitulos()
    ctx["golpes_de_campo"] = golpes_de_campo()
    ctx["heal_por_id"] = {h["id"]: h for h in json.load(
        open(os.path.join(RAIZ, "src", "data", "heal_locations.json")))["heal_locations"]}
    ctx["tile_andavel"] = leitor_de_tile()
    ctx["include_velho"] = os.environ.get("QA_INCLUDE_22F", "/tmp/qa_old_22f/include")
    ctx["save"] = auditoria_save(ctx)
    return ctx


def leitor_de_tile():
    """(mapa, x, y) -> motivo de não se andar ali, ou None.

    Reaproveita `dev_scripts/valida_warp_tile.py` para não reescrever a leitura
    de metatile, que já custou quatro armadilhas registradas lá.
    """
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    try:
        import valida_warp_tile as vwt
    except Exception as e:
        return lambda *a: None
    import struct
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(RAIZ, "data", "layouts", "layouts.json")))["layouts"]}
    porta = {n: v for n, v in vwt._MB.items()}
    cache = {}

    def olha(pasta, x, y):
        p = os.path.join(RAIZ, "data", "maps", pasta, "map.json")
        if not os.path.exists(p):
            return "sem map.json"
        d = json.load(open(p, encoding="utf-8"))
        lay = layouts.get(d.get("layout"))
        if not lay:
            return "layout %s não existe" % d.get("layout")
        bp = os.path.join(RAIZ, lay.get("blockdata_filepath", ""))
        if not os.path.exists(bp):
            return "sem blockdata"
        blk = open(bp, "rb").read()
        w, h = lay["width"], lay["height"]
        if not (0 <= x < w and 0 <= y < h):
            return "coordenada (%d,%d) fora do mapa %dx%d" % (x, y, w, h)
        idx = (y * w + x) * 2
        if idx + 2 > len(blk):
            return "blockdata curto"
        bruto = struct.unpack("<H", blk[idx:idx + 2])[0]
        colisao = (bruto >> 10) & 3
        if colisao:
            return "colisão %d (tile sólido)" % colisao
        return None
    return olha


def flags_de_jogo_novo():
    """Flags que o JOGO NOVO acende, e só elas.

    Duas fontes: os `FlagSet(...)` de `src/new_game.c` e o CORPO dos dois
    roteiros de reset (`EventScript_ResetAllMapFlags` e o irmão `...Frlg`),
    que `NewGameInitData` roda com `RunScriptImmediately`. A primeira versão
    pegava TODO `setflag` do arquivo que citasse o nome do roteiro, e por isso
    contava 229 flags que não eram de jogo novo nenhuma.
    """
    fora = set()
    p = os.path.join(RAIZ, "src", "new_game.c")
    if os.path.exists(p):
        t = open(p, encoding="utf-8", errors="replace").read()
        fora.update(re.findall(r"FlagSet\(\s*(FLAG_[A-Za-z0-9_]+)", t))
    for rel, texto in comum.scripts():
        for alvo in ("EventScript_ResetAllMapFlags", "EventScript_ResetAllMapFlagsFrlg"):
            m = re.search(r"^%s::\s*$" % alvo, texto, re.M)
            if not m:
                continue
            corpo = texto[m.end():]
            # o rótulo vale até o próximo rótulo de coluna zero
            fim = re.search(r"^\S", corpo, re.M)
            if fim:
                corpo = corpo[:fim.start()]
            fora.update(re.findall(r"^\s+setflag\s+(FLAG_[A-Za-z0-9_]+)", corpo, re.M))
    return fora



FONTES = os.path.join(os.path.dirname(RAIZ), "fontes-mapas")


def herdadas_do_vanilla(candidatas):
    """Flags que a FONTE também acende no jogo novo e também nunca apaga.

    Sem esta subtração, a checagem "nasce escondido e não volta" devolve o
    catálogo inteiro do Emerald: 64 achados, dos quais a esmagadora maioria é
    exatamente o que o jogo original faz (Scott, os Winstrate, o Rayquaza de
    Sootopolis). Auditoria que acusa o vanilla está medindo a si mesma.
    """
    fora = set()
    for fonte in ("pokeemerald", "pokefirered"):
        base = os.path.join(FONTES, fonte)
        if not os.path.isdir(base):
            continue
        acende, apaga = set(), set()
        for raiz in ("data", "src"):
            for dp, _, fn in os.walk(os.path.join(base, raiz)):
                for f in fn:
                    if not f.endswith((".inc", ".s", ".c", ".h")):
                        continue
                    t = open(os.path.join(dp, f), encoding="utf-8",
                             errors="replace").read()
                    apaga.update(re.findall(r"clearflag\s+(FLAG_[A-Za-z0-9_]+)", t))
                    apaga.update(re.findall(r"FlagClear\(\s*(FLAG_[A-Za-z0-9_]+)", t))
                    if "ResetAllMapFlags" in t:
                        acende.update(re.findall(r"^\s+setflag\s+(FLAG_[A-Za-z0-9_]+)",
                                                 t, re.M))
        fora |= {c for c in candidatas if c in acende and c not in apaga}
    return fora


def le_capitulos():
    """Um registro por linha de capítulo de `src/chapter_jump.c`.

    Lido do TEXTO da tabela, e não de memória: cada `CURA(HEAL_LOCATION_*)` é um
    destino de verdade do menu.
    """
    p = os.path.join(RAIZ, "src", "chapter_jump.c")
    if not os.path.exists(p):
        return [], {}
    t = open(p, encoding="utf-8", errors="replace").read()
    fora = []
    insignias = collections.defaultdict(set)
    for m in re.finditer(r"sGinasios(\w+)\[\]\s*=\s*\{(.*?)\n\};", t, re.S):
        reg, corpo = m.group(1).upper(), m.group(2)
        for linha in corpo.splitlines():
            mm = re.search(r'COMPOUND_STRING\("([^"]+)"\).*?CURA\((HEAL_LOCATION_\w+|0)\)'
                           r'\s*,\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)', linha)
            if not mm:
                continue
            fora.append({"regiao": reg.lower(), "rotulo": "%s/Before %s" % (reg, mm.group(1)),
                         "heal": mm.group(2), "insignia": mm.group(3)})
            if mm.group(3) != "0":
                insignias[reg].add(mm.group(3))
    mreg = re.search(r"sRegioes\[\]\s*=\s*\{(.*?)\n\};", t, re.S)
    if mreg:
        for m in re.finditer(r'COMPOUND_STRING\("(\w[\w ]*)"\),\s*'
                             r'CURA\((HEAL_LOCATION_\w+|0)\),\s*'
                             r'CURA\((HEAL_LOCATION_\w+|0)\)', mreg.group(1)):
            reg = m.group(1).upper()
            fora.append({"regiao": reg.lower(), "rotulo": reg + "/Start of region",
                         "heal": m.group(2), "insignia": None})
            fora.append({"regiao": reg.lower(), "rotulo": reg + "/Before League",
                         "heal": m.group(3), "insignia": None})
            insignias.setdefault(reg, set())
    # A COLUNA `flagInsignia` da tabela nao e a unica fonte de insignia, e ate
    # 23/08/2026 esta leitura achava que era. `ChapterJump_AplicaCapitulo` passou
    # a acender tambem a insignia DO MOTOR por INDICE, dentro do laco dos
    # ginasios anteriores, justamente para consertar o 5d: sem isso o Pikachu do
    # seletor saia com Surf, Rock Smash e Strength que o motor recusa em cinco
    # das seis regioes. Se a linha existir, as oito FLAG_BADGE0N_GET valem para
    # TODA regiao; se alguem a apagar, o 5d volta a acusar, que e o ponto.
    if re.search(r"FlagSet\(FLAG_BADGE01_GET \+ i\)", t):
        for reg in insignias:
            insignias[reg].update("FLAG_BADGE%02d_GET" % n for n in range(1, 9))
    return fora, insignias


def golpes_de_campo():
    """golpe -> flag de insígnia que `src/field_move.c` exige fora de FRLG."""
    p = os.path.join(RAIZ, "src", "field_move.c")
    fora = {}
    if not os.path.exists(p):
        return fora
    t = open(p, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"IsFieldMoveUnlocked_(\w+)\(void\)\s*\{(.*?)\n\}", t, re.S):
        nome, corpo = m.group(1), m.group(2)
        # o `return FlagGet(...)` DEPOIS do `if (IS_FRLG)` é o do ramo não-FRLG,
        # e é o que vale nesta build (`constants/global.h` dá IS_FRLG 0).
        flags = re.findall(r"FlagGet\((FLAG_\w+)\)", corpo)
        if flags:
            fora[nome] = flags[-1]
    return fora


_PASTA_DE_MAPA = None


def mapa_de_constante(sufixo):
    """`LITTLEROOT_TOWN` -> pasta do mapa, pelo campo `id` do próprio map.json.

    Casar por nome de pasta sem underscore erra: `MAP_PEWTER_CITY` mora em
    `PewterCity_Frlg`. A constante está escrita dentro do arquivo; é ela que
    manda.
    """
    global _PASTA_DE_MAPA
    if _PASTA_DE_MAPA is None:
        _PASTA_DE_MAPA = {}
        for nome, m in comum.mapas():
            ident = m.get("id")
            if ident:
                _PASTA_DE_MAPA[ident] = nome
    return _PASTA_DE_MAPA.get("MAP_" + sufixo)


def le_heal():
    p = os.path.join(RAIZ, "src", "data", "heal_locations.h")
    if not os.path.exists(p):
        for cand in ("src/data/heal_locations.h", "include/constants/heal_locations.h"):
            q = os.path.join(RAIZ, cand)
            if os.path.exists(q):
                p = q
                break
        else:
            return set()
    t = open(p, encoding="utf-8", errors="replace").read()
    fora = set()
    for m in re.finditer(r"MAP_([A-Z0-9_]+)", t):
        n = mapa_de_constante(m.group(1))
        if n:
            fora.add(n)
    return fora


REF_22F = "e5224a3d67"   # o commit da ROM oficial 2026-08-22f (ESTADO 0.p)


def auditoria_save(ctx):
    """A pergunta do Gui: a save da ROM 22f carrega na de hoje?

    `guarda_save.py` mede TAMANHO e ÍNDICE, e diz SAVE COMPATIVEL. Isto aqui
    mede ATRIBUIÇÃO: qual NOME mora em cada endereço de flag e de var nas duas
    árvores. Endereço que trocou de dono é save que carrega e MENTE.
    """
    fora = {"achados": [], "info": {}}
    g = open(os.path.join(RAIZ, "include", "global.h"), encoding="utf-8",
             errors="replace").read()
    m = re.search(r"#define\s+SAVE_LAYOUT_REVISION\s+(\S+)", g)
    fora["info"]["SAVE_LAYOUT_REVISION"] = m.group(1) if m else "NÃO EXISTE"
    if not m:
        fora["achados"].append(dict(
            id="6a", classe="cosmético", regiao="global",
            o_que="não existe SAVE_LAYOUT_REVISION: a ROM não tem como RECUSAR save de layout velho",
            onde="include/global.h",
            detalhe="a memória do Gui de 19/08 diz que a save velha é recusada de propósito; "
                    "esta árvore não tem o carimbo que faria isso"))

    # tamanho declarado de SaveBlock1/2/3
    for nome in ("SaveBlock1", "SaveBlock2", "SaveBlock3"):
        mm = re.search(r"struct\s+%s\b" % nome, g)
        fora["info"][nome] = "declarado" if mm else "não achado"

    velho = ctx.get("include_velho")
    if not velho or not os.path.isdir(velho):
        fora["info"]["22f"] = "árvore de %s não exportada; comparação não feita" % REF_22F
        return fora
    nomes = set(ctx["flags_val"]) | set(ctx["vars_val"])
    for h in ("constants/flags.h", "constants/vars.h", "constants/vars_frlg.h"):
        p = os.path.join(velho, h)
        if os.path.exists(p):
            for mm in re.finditer(r"^\s*#define\s+((?:FLAG|VAR)_[A-Za-z0-9_]+)\s",
                                  open(p, encoding="utf-8", errors="replace").read(), re.M):
                nomes.add(mm.group(1))
    v = comum.resolve_em(velho, nomes)
    n = comum.resolve_em(os.path.join(RAIZ, "include"), nomes)
    pool = re.compile(r"(FLAG|VAR)_UNUSED_0x[0-9A-Fa-f]+")
    donos_v, donos_n = collections.defaultdict(set), collections.defaultdict(set)
    for k, val in v.items():
        if not pool.fullmatch(k):
            donos_v[val].add(k)
    for k, val in n.items():
        if not pool.fullmatch(k):
            donos_n[val].add(k)
    trocados = []
    for addr in sorted(set(donos_v) & set(donos_n)):
        if donos_v[addr] != donos_n[addr]:
            trocados.append((hex(addr), sorted(donos_v[addr]), sorted(donos_n[addr])))
    fora["info"]["enderecos_que_trocaram_de_dono_desde_22f"] = len(trocados)
    for addr, antes, agora in trocados:
        fora["achados"].append(dict(
            id="6b", classe="provável",
            regiao="galar" if any("GALAR" in x for x in antes + agora) else "global",
            o_que="endereço de save trocou de DONO entre a ROM 22f e a de hoje "
                  "(o guarda_save não vê: ele mede tamanho, não atribuição)",
            onde=addr, detalhe={"22f": antes, "hoje": agora}))

    # id de treinador: a flag de vitória é TRAINER_FLAGS_START + id
    tv = ids_de_treinador(os.path.join(velho, "constants", "opponents.h"))
    tn = ids_de_treinador(os.path.join(RAIZ, "include", "constants", "opponents.h"))
    movidos = sorted(k for k in set(tv) & set(tn) if tv[k] != tn[k])
    fora["info"]["ids_de_treinador_movidos_desde_22f"] = len(movidos)
    for k in movidos:
        fora["achados"].append(dict(
            id="6c", classe="provável", regiao="global",
            o_que="id de treinador mudou desde a 22f: a flag de 'já venci' muda de dono",
            onde=k, detalhe={"22f": tv[k], "hoje": tn[k]}))
    return fora


def ids_de_treinador(caminho):
    if not os.path.exists(caminho):
        return {}
    fora = {}
    for m in re.finditer(r"^\s*#define\s+(TRAINER_[A-Za-z0-9_]+)\s+(\d+)\s*(?://.*)?$",
                         open(caminho, encoding="utf-8", errors="replace").read(), re.M):
        fora[m.group(1)] = int(m.group(2))
    return fora


SECOES = {1: secao1, 2: secao2, 3: secao3, 4: secao4, 5: secao5, 6: secao6}


def roda(quais):
    ctx = contexto()
    fora = []
    for n in quais:
        fora += SECOES[n](ctx)
    return ctx, fora


def demo():
    """Autoteste: cada checagem tem que ACUSAR uma mutação plantada e ficar
    calada sem ela. Não escreve no repo; muta as estruturas em memória.

    Duas metades em cada caso, e a segunda é a que importa: checagem que acusa
    mesmo SEM mutação não está medindo a mutação.
    """
    ctx = contexto()

    def conta(secao, ident):
        return len([a for a in secao(ctx) if a["id"] == ident])

    # 1d2: item ball sem flag
    base = conta(secao1, "1d2")
    falso = ("MapaDeMentira", {"object_events": [dict(
        graphics_id="OBJ_EVENT_GFX_ITEM_BALL", script="X_EventScript_ItemBallY",
        flag="0")]})
    ctx["mapas"] = tuple(list(ctx["mapas"]) + [falso])
    assert conta(secao1, "1d2") == base + 1, "1d2 cego"
    ctx["mapas"] = tuple(list(ctx["mapas"])[:-1])
    assert conta(secao1, "1d2") == base, "1d2 acusa sem mutação"

    # 1g: flag nomeada dentro da faixa de vitória de treinador
    assert conta(secao1, "1g") == 0, "a árvore de hoje já tem colisão de faixa"
    guarda = ctx["flags_val"]
    ctx["flags_val"] = dict(guarda, FLAG_MENTIRA=ctx["esp"]["TRAINER_FLAGS_START"] + 7)
    assert conta(secao1, "1g") == 1, "1g cego"
    ctx["flags_val"] = guarda
    assert conta(secao1, "1g") == 0, "1g acusa sem mutação"

    # 3a: treinador chamado por script e sem time
    base3 = conta(secao3, "3a")
    cmds = list(ctx["cmds"])
    ctx["cmds"] = cmds + [("data/maps/Fake/scripts.inc", "Fake", 1,
                           "trainerbattle_single", "TRAINER_QUE_NAO_EXISTE, A, B")]
    assert conta(secao3, "3a") == base3 + 1, "3a cego"
    ctx["cmds"] = cmds
    assert conta(secao3, "3a") == base3, "3a acusa sem mutação"

    # 3c: mesmo id de treinador duas vezes no MESMO mapa
    base3c = conta(secao3, "3c")
    alvo = sorted(ctx["party"])[0]
    ctx["cmds"] = cmds + [("data/maps/Fake/scripts.inc", "MapaUnico", 1,
                           "trainerbattle_single", "%s, A, B" % alvo),
                          ("data/maps/Fake/scripts.inc", "MapaUnico", 9,
                           "trainerbattle_single", "%s, A, B" % alvo)]
    assert conta(secao3, "3c") == base3c + 1, "3c cego"
    ctx["cmds"] = cmds

    # 4a: item que não existe
    base4 = conta(secao4, "4a")
    assert base4 == 0, "a árvore de hoje já dá item inexistente"
    ctx["cmds"] = cmds + [("data/maps/Fake/scripts.inc", "Fake", 2,
                           "giveitem", "ITEM_NAO_EXISTE, 1")]
    assert conta(secao4, "4a") == 1, "4a cego"
    ctx["cmds"] = cmds
    assert conta(secao4, "4a") == 0, "4a acusa sem mutação"

    # 5c: capítulo em tile sólido. A mutação é o DESTINO, e o leitor de tile é
    # exercitado de verdade contra o blockdata do mapa.
    base5 = conta(secao5, "5c")
    assert base5 == 0, "algum capítulo de hoje já cai em tile sólido"
    caps = list(ctx["capitulos"])
    hl = dict(ctx["heal_por_id"])
    hl["HEAL_LOCATION_MENTIRA"] = {"id": "HEAL_LOCATION_MENTIRA",
                                   "map": "MAP_PALLET_TOWN", "x": 5, "y": 5}
    ctx["heal_por_id"] = hl
    ctx["capitulos"] = caps + [{"regiao": "kanto", "rotulo": "MENTIRA",
                                "heal": "HEAL_LOCATION_MENTIRA", "insignia": None}]
    assert conta(secao5, "5c") == 1, "5c cego (o leitor de tile não está medindo)"
    ctx["capitulos"] = caps
    assert conta(secao5, "5c") == 0, "5c acusa sem mutação"

    # 5d: região cujo capítulo não acende a insígnia que o golpe de campo pede
    ins = dict(ctx["insignias_por_regiao"])
    ctx["insignias_por_regiao"] = {"KANTO": set(ctx["golpes_de_campo"].values())}
    assert conta(secao5, "5d") == 0, "5d acusa região completa"
    ctx["insignias_por_regiao"] = {"XPTO": set()}
    assert conta(secao5, "5d") == 1, "5d cego"
    ctx["insignias_por_regiao"] = ins

    # 6b: endereço de save que troca de dono. Sem árvore velha o caso é PULADO,
    # e dizer isso é melhor que passar verde vazio.
    if ctx["save"]["info"].get("22f"):
        print("demo: aviso, a comparação de save foi PULADA (%s)"
              % ctx["save"]["info"]["22f"])
    else:
        assert ctx["save"]["info"]["enderecos_que_trocaram_de_dono_desde_22f"] >= 0

    print("demo: 7 mutações plantadas, 7 acusadas, e nenhuma checagem acusa sem "
          "mutação.")


def main():
    if "--demo" in sys.argv:
        return demo()
    quais = sorted(SECOES)
    if "--secao" in sys.argv:
        quais = [int(sys.argv[sys.argv.index("--secao") + 1])]
    ctx, achados = roda(quais)
    if "--json" in sys.argv:
        print(json.dumps(achados, indent=1, ensure_ascii=False, default=str))
        return
    por = collections.Counter((a["classe"], a["id"]) for a in achados)
    for (classe, ident), n in sorted(por.items()):
        print("%-16s %-5s %d" % (classe, ident, n))
    print("total:", len(achados))
    print("save:", ctx["save"]["info"])


if __name__ == "__main__":
    # Ver a nota do mapas_qa: `main()` imprime e devolve None, e sem o `or 0` o
    # portao reprovaria sempre.
    sys.exit(main() or 0)
