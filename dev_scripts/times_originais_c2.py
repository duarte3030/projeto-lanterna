#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Times e encontros ORIGINAIS de Galar (Shield) e Unova (Black 2) na campanha
do cartucho 2. Decisão 130 do Gui (28/10/2026, "siga o recomendado") e
autorização 150.

    python3 dev_scripts/times_originais_c2.py --casar    # grava as duas tabelas de casamento
    python3 dev_scripts/times_originais_c2.py --aplicar  # escreve party, ids, Fase F, retratos, NPCs e encontros
    python3 dev_scripts/times_originais_c2.py --demo     # confere as invariantes no que está escrito

O que muda, e o que NÃO muda:

1. Cada treinador de Galar e de Unova que já está nos mapas é casado com o
   treinador do jogo original (Shield ou Black 2) por classe, nome e local.
   A tabela sai em `dev_scripts/casamento_treinadores_<regiao>.json`, com a
   confiança de cada par. O que não casa fica com o time de hoje e entra na
   lista `nao_casados` da mesma tabela, com o motivo.
2. Casado: a constante de hoje (a que o mapa chama) passa a ter o time
   ORIGINAL, no nível original. O time do hack (Ultimate Plus em 255, BW3G em
   223) vai, byte a byte, para uma constante NOVA `<constante>_REVANCHE`, com id
   apendado acima do maior id que existia (o `guarda_save.py` só aceita
   apendar no fim). A revanche não é chamada por mapa nenhum ainda. Clone com
   time igual ao de outro casado não gera segunda revanche.
3. Chefe da Fase F que foi casado: a entrada dele em `fase_f_chefes.json`
   passa a apontar para a constante de revanche. O time da Fase F continua
   inteiro, só muda de dono; o `guarda_party.py` continua cobrando o mesmo
   conteúdo.
4. Retrato: todo treinador de Galar e de Unova (campanha e revanche) cujo
   personagem tem retrato novo aprovado (`TRAINER_PIC_GALAR_*` e
   `TRAINER_PIC_UNOVA_*`) passa a usá-lo. NPC: só personagem nomeado (líder,
   Elite 4, campeão, rival, vilão), trocando o `graphics_id` do objeto que
   abre a batalha dele ou cujo rótulo de script leva o nome dele.
5. Encontro: Unova pelos 51 mapas do Black 2 que já validam no conversor do
   repo; Galar pela zona do Shield que mais divide espécie com a tabela de
   hoje. Só a subtabela que o original tem é trocada; a que ele não tem fica
   como está.

As fontes ficam fora do repo (dado de jogo é só local):
`fontes-mapas/prd-assets/poc-A/saida/` (`bw2_todos.party`,
`bw2_treinadores.json`, `bw2_wild_encounters.json`, `swsh_todos.party`,
`swsh_encontros.json`, `up_treinadores.json`, este último com o nível que o
demake tinha antes do 255, lido da ROM do Ultimate Plus). `POC_A` e `FONTES` sobrescrevem
os caminhos.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.environ.get("FONTES", os.path.expanduser("~/Projetos/pokemon-claude/fontes-mapas"))
POC_A = os.environ.get("POC_A", os.path.join(FONTES, "prd-assets", "poc-A"))
SAIDA = os.path.join(POC_A, "saida")

PARTY = os.path.join(RAIZ, "src/data/trainers.party")
OPPS = os.path.join(RAIZ, "include/constants/opponents.h")
FASE_F = os.path.join(RAIZ, "dev_scripts/fase_f_chefes.json")
WILD = os.path.join(RAIZ, "src/data/wild_encounters.json")
INC_GALAR = os.path.join(RAIZ, "data/scripts/galar_treinadores.inc")
CASAMENTO = os.path.join(RAIZ, "dev_scripts/casamento_treinadores_%s.json")
ENCONTROS = os.path.join(RAIZ, "dev_scripts/casamento_encontros_c2.json")

# O maior id de treinador no commit de referência do guarda de save
# (REF_TREINADOR = 618a884812) é 3276. Id novo só pode nascer acima dele.
PRIMEIRO_ID_REVANCHE = 3277
TETO_ID = 3999
SUFIXO_REVANCHE = "_REVANCHE"
MARCA_INI = "// >>> Revanches: times do hack guardados (dev_scripts/times_originais_c2.py) >>>"
MARCA_FIM = "// <<< Revanches: times do hack guardados <<<"
P_INI = "/* >>> Revanches: times do hack guardados (dev_scripts/times_originais_c2.py) >>> */"
P_FIM = "/* <<< Revanches: times do hack guardados <<< */"

# ------------------------------------------------------------------ Galar
# Personagem nomeado, Team Yell e Macro Cosmos: casados à mão, um por um, pelo
# nível e pelo time que o Ultimate Plus tinha ANTES do 255 (lido da ROM do
# demake) e pelo texto da cena. O Hop sai sempre na variante de Scorbunny,
# que é a que o demake usa. Chave: constante BASE (o clone `_2` herda).
GALAR_MANUAL = {
    "TRAINER_GALAR_KEVIN_1": (33, "alta", "Team Yell de Motostoke: Zigzagoon nível 9 nos dois"),
    "TRAINER_GALAR_JONH_5": (205, "alta", "Team Yell: Zigzagoon e Thievul 17/18 nos dois"),
    "TRAINER_GALAR_BEDE_11": (240, "alta", "Bede na Galar Mine: Solosis, Gothita, Ponyta e Hatenna nos dois, 21 a 25"),
    "TRAINER_GALAR_GRUNT_12": (160, "media", "Team Yell da Galar Mine: Thievul nos dois, nível 20 a 22"),
    "TRAINER_GALAR_GRUNT_13": (207, "media", "Team Yell da Rota 6: Linoone nos dois, nível 29/30"),
    "TRAINER_GALAR_BEA_27": (77, "alta", "ginásio de Stow-on-Side: as quatro espécies e o nível iguais"),
    "TRAINER_GALAR_GORDIE_49": (135, "alta", "ginásio de Circhester: três espécies e o nível iguais"),
    "TRAINER_GALAR_ANA_59": (137, "alta", "Team Yell da Rota 9: Linoone e Pangoro 39/40 nos dois"),
    "TRAINER_GALAR_MARNIE_60": (138, "alta", "Marnie na Rota 9: as quatro espécies e o nível iguais"),
    "TRAINER_GALAR_MARNIE_76": (145, "alta", "semifinal da Champion Cup (texto da cena) e as cinco espécies iguais"),
    "TRAINER_GALAR_ERIC_77": (285, "media", "Macro Cosmos de Wyndon, nível 47, mesmo nome; espécies diferentes"),
    "TRAINER_GALAR_FELIPE_78": (286, "media", "Macro Cosmos de Wyndon, nível 47, Mawile nos dois"),
    "TRAINER_GALAR_VINICIUS_79": (287, "media", "Macro Cosmos de Wyndon, nível 47, Steelix nos dois"),
    "TRAINER_GALAR_OLENA_80": (143, "alta", "Oleana: as cinco espécies e o nível iguais"),
    "TRAINER_GALAR_ROSE_85": (175, "alta", "Rose: três espécies e o nível iguais"),
    "TRAINER_GALAR_MILO_304": (32, "media", "mapa do ginásio de Turffield; o demake pôs ali o time de revanche"),
    "TRAINER_GALAR_NESSA_307": (36, "media", "mapa do ginásio de Hulbury; o demake pôs ali o time de revanche"),
    "TRAINER_GALAR_KABU_308": (37, "media", "mapa do ginásio de Motostoke; o demake pôs ali o time de revanche"),
    "TRAINER_GALAR_ALLISTER_310": (78, "media", "mapa do ginásio de Stow-on-Side; o demake pôs ali o time de revanche"),
    "TRAINER_GALAR_MELONY_336": (136, "media", "mapa do ginásio de Circhester; o demake pôs ali o time de revanche"),
    "TRAINER_GALAR_HOP_332": (123, "alta", "Hop: Wooloo, Corvisquire e Raboot 18 a 21 nos dois"),
    "TRAINER_GALAR_HOP_429": (126, "alta", "Hop: Toxel, Silicobra e Raboot 28 a 33 nos dois"),
    "TRAINER_GALAR_HOP_432": (129, "alta", "Hop: Trevenant, Snorlax, Boltund e Cinderace 34 a 37 nos dois"),
    "TRAINER_GALAR_HOP_435": (204, "alta", "Hop: Dubwool, Pincurchin, Snorlax, Corviknight e Cinderace 39 a 41 nos dois"),
    "TRAINER_GALAR_HOP_438": (132, "alta", "Hop na Champion Cup: as cinco espécies e o nível iguais"),
    "TRAINER_GALAR_GRUNT_375": (101, "media", "Team Yell de Spikemuth, nível 42; espécie diferente, casado pela ordem"),
    "TRAINER_GALAR_GRUNT_378": (102, "media", "Team Yell de Spikemuth, nível 42; espécie diferente, casado pela ordem"),
    "TRAINER_GALAR_GRUNT_379": (105, "alta", "Team Yell de Spikemuth: Liepard 42/43 nos dois"),
    "TRAINER_GALAR_GRUNT_391": (103, "media", "Team Yell de Spikemuth, nível 42; espécie diferente, casado pela ordem"),
    "TRAINER_GALAR_OPAL_418": (108, "alta", "ginásio de Ballonlea: as quatro espécies e o nível iguais"),
    "TRAINER_GALAR_PIERS_419": (107, "alta", "Piers em Spikemuth: as quatro espécies e o nível iguais"),
    "TRAINER_GALAR_LEON_739": (190, "alta", "final da Champion Cup: as seis espécies iguais (variante Rhyperior e Rillaboom)"),
}
# Batalha só de pós-jogo do demake (torre de Turffield depois da Champion Cup,
# youtubers de Wyndon, DLC): fica com o time do hack, mesmo quando é clone de
# um casado da campanha.
POS_JOGO_GALAR = re.compile(r"^Galar_(TurffieldIndoor(09|[1-6]\d)|WyndonIndoor|IsleOfArmor|CrownTundra|DynamaxAdventure)")
# Casamento automático recusado depois de olhar o par um por um.
RECUSA_GALAR = {"TRAINER_GALAR_GILLI_E_CAM_278": "batalha dupla de dois treinadores; o Shield tem só o Cam, outra classe"}
RECUSA_UNOVA = {"TRAINER_UNOVA_N": "o N do BW3G luta no quarto dele com time próprio; o par do Black 2 é a revanche de clima do castelo",
                "TRAINER_UNOVA_BIANCA": "a Bianca do BW3G está no PWT, que é pós-jogo"}
# Personagem com retrato novo, e o apelido de nome quando o demake escreve diferente.
PIC_GALAR = {"ALLISTER", "AVERY", "BEA", "BEDE", "GORDIE", "HOP", "KABU", "KLARA", "LEON",
             "MARNIE", "MELONY", "MILO", "MUSTARD", "NESSA", "OLEANA", "OPAL", "PEONY",
             "PIERS", "RAIHAN", "ROSE"}
PIC_UNOVA = {"ALDER", "BIANCA", "BURGH", "CAITLIN", "CHEREN", "CHILI", "CILAN", "CLAY",
             "COLRESS", "CRESS", "DRAYDEN", "ELESA", "GHETSIS", "GRIMSLEY", "HUGH", "IRIS",
             "MARLON", "MARSHAL", "N", "NATE", "ROSA", "ROXIE", "SHAUNTAL", "SKYLA", "ZINZOLIN"}
APELIDO = {"OLENA": "OLEANA"}
# Os sábios da Plasma do BW3G não têm retrato próprio: o de sábio é o deles.
SABIOS_UNOVA = {"GIALLO", "BRONIUS", "GORM", "RYOKU"}
GFX_GALAR = {"ALLISTER", "BEA", "BEDE", "GORDIE", "HOP", "KABU", "KLARA", "LEON", "MARNIE",
             "MELONY", "MILO", "NESSA", "OLEANA", "OPAL", "PIERS", "RAIHAN", "ROSE"}
GFX_UNOVA = {"ALDER", "BIANCA", "BURGH", "CAITLIN", "CHEREN", "CLAY", "COLRESS", "DRAYDEN",
             "ELESA", "GHETSIS", "GRIMSLEY", "HUGH", "IRIS", "MARLON", "MARSHAL", "NATE",
             "ROSA", "ROXIE", "SHAUNTAL", "SKYLA", "ZINZOLIN"}

# Classe do BW3G (o token do nome da constante) contra a classe do Black 2.
CLASSE_UNOVA = {"ACETRAINER": "acetrainer", "VETERAN": "veteran", "GRUNT": "teamplasma",
                "E4": "elitefour", "LEADER": "leader", "CHAMPION": "champion",
                "PKMNRANGER": "pkmnranger", "PKMNBREEDER": "pkmnbreeder",
                "SCHOOLKID": "schoolkid", "POKEFAN": "pokefan", "FISHER": "fisherman",
                "BACKPACKER": "backpacker", "BACKERS": "backers", "PILOT": "pilot",
                "HARLEQUIN": "harlequin", "JANITOR": "janitor", "NURSE": "nurse",
                "WORKER": "worker", "HIKER": "hiker", "SCIENTIST": "scientist",
                "PSYCHIC": "psychic", "ROUGHNECK": "roughneck", "BIKER": "biker",
                "BATTLEGIRL": "battlegirl", "BLACKBELT": "blackbelt", "YOUNGSTER": "youngster",
                "LASS": "lass", "SWIMMER": "swimmer", "GENTLEMAN": "gentleman", "LADY": "lady",
                "BEAUTY": "beauty", "GUITARIST": "guitarist", "PARASOLLADY": "parasollady",
                "SMASHER": "smasher", "HOOPSTER": "hoopster", "LINEBACKER": "linebacker",
                "STRIKER": "striker", "INFIELDER": "infielder", "PRESCHOOLER": "preschooler",
                "NURSERYAIDE": "nurseryaide", "DOCTOR": "doctor", "POLICEMAN": "policeman",
                "RICHBOY": "richboy", "SOCIALITE": "socialite", "TWINS": "twins",
                "DANCER": "dancer", "MAID": "maid", "WAITER": "waiter", "WAITRESS": "waitress",
                "BAKER": "baker", "ARTIST": "artist", "CYCLIST": "cyclist", "CLERK": "clerk",
                "MUSICIAN": "musician", "CLAY": "leader"}
NOMEADOS_UNOVA = {"BIANCA", "N", "CHEREN", "HUGH", "ZINZOLIN", "COLRESS", "GHETSIS", "IRIS",
                  "ALDER", "NATE", "ROSA", "GIALLO", "BRONIUS", "GORM", "RYOKU"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("é", "e"))


# ------------------------------------------------------------------ leitura
def blocos(texto):
    """[(constante, início, fim)] de cada bloco `=== X ===` do .party."""
    ms = list(re.finditer(r"(?m)^=== (\S+) ===[ \t]*$", texto))
    return [(m.group(1), m.start(), ms[k + 1].start() if k + 1 < len(ms) else len(texto))
            for k, m in enumerate(ms)]


def fatia(bloco):
    """(linhas de cabeçalho, linhas de time, rabo) de um bloco sem a linha ===.
    O time começa na primeira linha de espécie (com ou sem apelido)."""
    linhas = bloco.split("\n")
    i = next((k for k, ln in enumerate(linhas) if re.match(r"^(SPECIES_|\S.*\(SPECIES_)", ln)), len(linhas))
    cab = [ln for ln in linhas[:i] if ln.strip()]
    time = linhas[i:]
    rabo = []
    while time and (not time[-1].strip() or time[-1].startswith("/*") or "*/" in time[-1]):
        rabo.insert(0, time.pop())
    return cab, time, rabo


def campo(cab, chave):
    for ln in cab:
        if ln.startswith(chave + ":"):
            return ln.split(":", 1)[1].strip()
    return ""


def le_party(caminho):
    texto = open(caminho, encoding="utf-8").read()
    return texto, {c: texto[a:b] for c, a, b in blocos(texto)}


def fonte_party(arquivo, prefixo):
    """{id numérico da fonte: (constante, bloco)} do .party gerado pela trilha A."""
    _, bl = le_party(os.path.join(SAIDA, arquivo))
    fora = {}
    for c, b in bl.items():
        m = re.match(r"TRAINER_%s_(\d+)_" % prefixo, c)
        if m:
            fora[int(m.group(1))] = (c, b)
    return fora


def especies_do_bloco(b):
    return [re.sub(r"\s.*", "", s) for s in re.findall(r"(?m)^(SPECIES_\S+)", b)]


def niveis_do_bloco(b):
    return [int(x) for x in re.findall(r"(?m)^Level: (\d+)", b)]


def referencias():
    """{constante: [mapas que a chamam]} para Galar (pelo .inc gerado) e Unova."""
    refs = collections.defaultdict(set)
    for f in glob.glob(os.path.join(RAIZ, "data/maps/*/scripts.inc")):
        mp = f.split(os.sep)[-2]
        if mp.startswith(("Unova_", "Galar_")):
            for x in set(re.findall(r"\bTRAINER_(?:UNOVA|GALAR)_\w+", open(f).read())):
                refs[x].add(mp)
    cur = None
    for ln in open(INC_GALAR, encoding="utf-8"):
        m = re.match(r"@ ---- (\S+) ----", ln)
        if m:
            cur = m.group(1)
        for x in re.findall(r"\bTRAINER_GALAR_\w+", ln):
            if cur:
                refs[x].add(cur)
    return {k: sorted(v) for k, v in refs.items()}


def base_de(const):
    """`TRAINER_GALAR_HOP_429_2` -> `TRAINER_GALAR_HOP_429` (clone de objeto)."""
    return re.sub(r"_\d+$", "", const) if re.search(r"_\d+_\d+$", const) else const


# ------------------------------------------------------------------ Ultimate Plus
def up_fonte():
    """{id do demake: (classe, nome, [(espécie, nível)])}. Lido de
    `saida/up_treinadores.json`, extraído da ROM do demake pelo MESMO leitor do
    balde d (`treinadores_galar.treinadores_da_fonte`), com o nível original."""
    d = json.load(open(os.path.join(SAIDA, "up_treinadores.json"), encoding="utf-8"))
    return {int(k): (v["classe"], v["nome"], [tuple(x) for x in v["time"]]) for k, v in d.items()}


# ------------------------------------------------------------------ casamento
def casa_galar(atual, refs):
    sw = fonte_party("swsh_todos.party", "SWSH")
    up = up_fonte()
    casados, nao = [], []
    # um treinador do Shield serve a uma só base do demake (o clone herda)
    dono_sw = {fid: base for base, (fid, _, _) in GALAR_MANUAL.items()}
    for const, b in sorted(atual.items(), key=lambda kv: (base_de(kv[0]) not in GALAR_MANUAL, kv[0])):
        if not const.startswith("TRAINER_GALAR_") or const.endswith(SUFIXO_REVANCHE):
            continue
        cab, _, _ = fatia(b[b.index("\n") + 1:])
        nome, classe = campo(cab, "Name"), campo(cab, "Class")
        base = base_de(const)
        reg = dict(constante=const, nome=nome, classe=classe, mapas=refs.get(const, []))
        if reg["mapas"] and all(POS_JOGO_GALAR.match(m) for m in reg["mapas"]):
            nao.append(dict(reg, motivo="só aparece em mapa de pós-jogo do demake; fica o time do hack"))
            continue
        if base in RECUSA_GALAR:
            nao.append(dict(reg, motivo=RECUSA_GALAR[base]))
            continue
        if base in GALAR_MANUAL:
            fid, conf, motivo = GALAR_MANUAL[base]
            if base != const:
                motivo += " (clone de %s, mesmo treinador do demake)" % base
            casados.append(dict(reg, fonte=dict(jogo="Shield", id=fid, constante=sw[fid][0]),
                                confianca=conf, motivo=motivo))
            continue
        m = re.search(r"_(\d+)$", base)
        u = up.get(int(m.group(1))) if m else None
        if not u or not u[2]:
            nao.append(dict(reg, motivo="sem time na fonte do demake"))
            continue
        ucls, unome, utime = u
        ulv = sum(lv for _, lv in utime) / len(utime)
        if ulv >= 60:
            nao.append(dict(reg, motivo="pós-jogo do demake (nível médio %d na fonte); fica o time do hack" % ulv))
            continue
        cand = []
        for fid, (fc, fb) in sw.items():
            fn = campo(fatia(fb[fb.index("\n") + 1:])[0], "Name")
            if len(norm(fn)) < 3 or not (norm(fn) == norm(unome) or norm(unome).endswith(norm(fn))):
                continue
            flv = niveis_do_bloco(fb)
            dif = abs(sum(flv) / len(flv) - ulv)
            esp = {norm(re.sub(r"^SPECIES_|_GALAR$", "", s)) for s in especies_do_bloco(fb)}
            ov = len({norm(s) for s, _ in utime} & esp)
            cls_ok = norm(ucls.split()[0]) in norm(fc) if ucls else False
            if dif <= 2 or (dif <= 4 and (ov or cls_ok)):
                cand.append((-(ov + cls_ok), dif, fid, ov, cls_ok))
        if not cand:
            nao.append(dict(reg, motivo="nenhum treinador do Shield com o mesmo nome e nível perto (%s %s, nível %d)"
                            % (ucls, unome, ulv)))
            continue
        cand.sort()
        cand = [c for c in cand if dono_sw.setdefault(c[2], base) == base]
        if not cand:
            nao.append(dict(reg, motivo="o par do Shield já foi para outro treinador desta região"))
            continue
        _, dif, fid, ov, cls_ok = cand[0]
        conf = "alta" if ov and cls_ok else "media"
        casados.append(dict(reg, fonte=dict(jogo="Shield", id=fid, constante=sw[fid][0]), confianca=conf,
                            motivo="nome igual, nível a %.0f, %d espécie(s) em comum, classe %s"
                            % (dif, ov, "igual" if cls_ok else "diferente")))
    return casados, nao


def casa_unova(atual, refs):
    b2 = {x["id"]: x for x in json.load(open(os.path.join(SAIDA, "bw2_treinadores.json"), encoding="utf-8"))}
    bp = fonte_party("bw2_todos.party", "BW2")

    def pk(s):
        return re.sub(r"[^a-z0-9]", "", s.lower().replace("route ", "rt").replace("é", "e"))

    def lugar_casa(mapas, lugares):
        for mp in mapas:
            m = pk(mp.replace("Unova_", ""))
            for p in lugares:
                p = pk(p)
                for q in {p, re.sub(r"(city|town)$", "", p)}:
                    if q and m.startswith(q) and not (len(m) > len(q) and m[len(q)].isdigit() and q[-1].isdigit()):
                        return True
        return False

    pedidos = []
    for const, b in atual.items():
        if not const.startswith("TRAINER_UNOVA_") or const.endswith(SUFIXO_REVANCHE):
            continue
        cab, _, _ = fatia(b[b.index("\n") + 1:])
        nome = campo(cab, "Name")
        resto = const[len("TRAINER_UNOVA_"):]
        if const in RECUSA_UNOVA:
            pedidos.append((const, nome, campo(cab, "Class"), [], RECUSA_UNOVA[const]))
            continue
        tok = resto.replace("_", "")
        cls_b3 = next((v for k, v in sorted(CLASSE_UNOVA.items(), key=lambda kv: -len(kv[0]))
                       if tok.startswith(k)), None)
        nomeado = next((n for n in NOMEADOS_UNOVA if resto == n or resto.startswith(n + "_")
                        or re.match(n + r"\d", resto)), None)
        esp = {norm(re.sub(r"^SPECIES_", "", s).split("_")[0]) for s in especies_do_bloco(b)}
        cands = []
        for x in b2.values():
            if norm(x["nome"]) != norm(nome) or x["id"] not in bp or x["classe"] == "no data":
                continue
            lugar = lugar_casa(refs.get(const, []), [l["lugar"] for l in x["lugares"]])
            classe = cls_b3 is not None and norm(x["classe"]).startswith(cls_b3)
            ov = len(esp & {norm(y["especie"]) for y in x["time"]})
            if lugar and classe:
                conf, mot = "alta", "nome, classe e local iguais"
            elif nomeado and (classe or ov):
                conf, mot = "media", "personagem nomeado, %s" % ("mesma classe" if classe else "%d espécie(s) em comum" % ov)
            elif classe and not x["lugares"] and ov >= 1:
                conf, mot = "media", "nome e classe iguais, %d espécie(s) em comum, local sem registro no Black 2" % ov
            elif lugar and ov >= 2:
                conf, mot = "media", "nome e local iguais, classe diferente, %d espécies em comum" % ov
            else:
                continue
            cands.append((0 if conf == "alta" else 1, -ov, x["id"], conf, mot + ("; %d espécie(s) em comum" % ov if conf == "alta" else "")))
        pedidos.append((const, nome, campo(cab, "Class"), sorted(cands), None))
    # Um treinador do Black 2 serve a UM só da Unova de hoje: os grunts da
    # Plasma repetem nome e lugar, e sem isto dez grunts virariam o mesmo.
    usados, casados, nao = set(), [], []
    for const, nome, classe, cands, recusa in sorted(pedidos, key=lambda p: (p[3][0][:2] if p[3] else (9, 0), p[0])):
        reg = dict(constante=const, nome=nome, classe=classe, mapas=refs.get(const, []))
        if recusa:
            nao.append(dict(reg, motivo=recusa))
            continue
        livre = [c for c in cands if c[2] not in usados]
        if not livre:
            nao.append(dict(reg, motivo="nenhum treinador do Black 2 com o mesmo nome e (classe ou local) livre"
                            if not cands else "o par do Black 2 já foi para outro treinador desta região"))
            continue
        _, _, fid, conf, mot = livre[0]
        usados.add(fid)
        casados.append(dict(reg, fonte=dict(jogo="Black 2", id=fid, constante=bp[fid][0],
                                            lugares=[l["lugar"] for l in b2[fid]["lugares"]]),
                            confianca=conf, motivo=mot))
    casados.sort(key=lambda r: r["constante"])
    nao.sort(key=lambda r: r["constante"])
    return casados, nao


def casar():
    _, atual = le_party(PARTY)
    refs = referencias()
    for regiao, f in (("galar", casa_galar), ("unova", casa_unova)):
        casados, nao = f(atual, refs)
        doc = collections.OrderedDict(
            sobre="Casamento dos treinadores de %s do cartucho 2 com o jogo original (%s). "
                  "Gerado por dev_scripts/times_originais_c2.py --casar; decisão 130 do Gui."
                  % (regiao.capitalize(), "Shield" if regiao == "galar" else "Black 2"),
            contagem=dict(casados=len(casados), alta=sum(c["confianca"] == "alta" for c in casados),
                          media=sum(c["confianca"] == "media" for c in casados), nao_casados=len(nao)),
            casados=casados, nao_casados=nao)
        json.dump(doc, open(CASAMENTO % regiao, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("%s: %d casados (%d alta, %d média), %d não casados" % (
            regiao, len(casados), doc["contagem"]["alta"], doc["contagem"]["media"], len(nao)))


# ------------------------------------------------------------------ retrato e NPC
def personagem(const, nome, regiao):
    chars = PIC_GALAR if regiao == "galar" else PIC_UNOVA | SABIOS_UNOVA
    toks = const.split("_")[2:]
    n = APELIDO.get(norm(nome).upper(), norm(nome).upper())
    for t in toks:
        t2 = APELIDO.get(t, t)
        t2 = re.sub(r"\d+$", "", t2)
        if t2 in chars and n.startswith(t2) and len(t2) >= (1 if t2 == "N" else 2):
            if t2 == "N" and norm(nome) != "n":
                continue
            return t2
    return None


def pic_de(char, regiao):
    if regiao == "unova" and char in SABIOS_UNOVA:
        return "TRAINER_PIC_UNOVA_PLASMA_SAGE"
    return "TRAINER_PIC_%s_%s" % (regiao.upper(), char)


def troca_cab(bloco, chave, valor):
    return re.sub(r"(?m)^%s: .*$" % chave, "%s: %s" % (chave, valor), bloco, count=1)


# ------------------------------------------------------------------ aplicar
def aplica_party(gravar=True):
    texto, atual = le_party(PARTY)
    fontes = {"Shield": fonte_party("swsh_todos.party", "SWSH"),
              "Black 2": fonte_party("bw2_todos.party", "BW2")}
    doc = json.load(open(FASE_F, encoding="utf-8"))
    na_fase_f = {c["id"] for c in doc["chefes"]}
    novos, revanches, vistos = {}, [], {}
    for regiao in ("galar", "unova"):
        cas = json.load(open(CASAMENTO % regiao, encoding="utf-8"))["casados"]
        # o dono da revanche de um time repetido é o chefe da Fase F, se houver
        cas.sort(key=lambda r: (r["constante"] not in na_fase_f, r["constante"]))
        for r in cas:
            const = r["constante"]
            velho = atual[const]
            corpo = velho[velho.index("\n") + 1:]
            cab, time, rabo = fatia(corpo)
            chave = "\n".join(time).strip()
            if chave not in vistos:
                vistos[chave] = const + SUFIXO_REVANCHE
                revanches.append((const + SUFIXO_REVANCHE, "=== %s%s ===\n" % (const, SUFIXO_REVANCHE)
                                  + "\n".join(cab) + "\n\n" + chave + "\n\n", const, regiao))
            r["revanche"] = vistos[chave]
            fc, fb = fontes[r["fonte"]["jogo"]][r["fonte"]["id"]]
            fcab, ftime, _ = fatia(fb[fb.index("\n") + 1:])
            nome = (campo(fcab, "Name") or campo(cab, "Name"))[:10]
            ncab = [("Name: %s" % nome) if ln.startswith("Name:") else ln for ln in cab]
            novos[const] = ("=== %s ===\n" % const + "\n".join(ncab) + "\n\n"
                            + "\n".join(ftime).strip() + "\n\n"
                            + "".join(x + "\n" for x in rabo if x.strip()))
        json.dump(json.load(open(CASAMENTO % regiao, encoding="utf-8")) | {
            "casados": sorted(cas, key=lambda r: r["constante"])},
            open(CASAMENTO % regiao, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 1. troca os blocos da campanha, preservando o resto do arquivo
    out = []
    pos = 0
    for c, a, b in blocos(texto):
        if c in novos:
            out.append(texto[pos:a])
            out.append(novos[c])
            pos = b
    out.append(texto[pos:])
    texto = "".join(out)
    # 2. revanches num bloco próprio no fim (some e volta inteiro se rodar de novo)
    texto = re.sub(re.escape(P_INI) + r".*?" + re.escape(P_FIM) + r"\n?", "", texto, flags=re.S)
    texto = texto.rstrip("\n") + "\n\n" + P_INI + "\n" + "".join(b for _, b, _, _ in revanches) + P_FIM + "\n"
    # 3. retrato novo para todo treinador de Galar e Unova cujo personagem tem arte
    trocas = 0
    out, pos = [], 0
    for c, a, b in blocos(texto):
        if not c.startswith(("TRAINER_GALAR_", "TRAINER_UNOVA_")):
            continue
        regiao = "galar" if c.startswith("TRAINER_GALAR_") else "unova"
        bl = texto[a:b]
        ch = personagem(c, campo(bl.split("\n"), "Name"), regiao)
        if ch:
            pic = pic_de(ch, regiao)
            if campo(bl.split("\n"), "Pic") != pic:
                out.append(texto[pos:a])
                out.append(troca_cab(bl, "Pic", pic))
                pos = b
                trocas += 1
    out.append(texto[pos:])
    texto = "".join(out)
    # 4. ids novos, apendados acima de 3276
    opp = open(OPPS, encoding="utf-8").read()
    opp = re.sub(re.escape(MARCA_INI) + r".*?" + re.escape(MARCA_FIM) + r"\n?", "", opp, flags=re.S)
    usados = {int(v) for v in re.findall(r"(?m)^#define TRAINER_\w+\s+(\d+)", opp)}
    nid, linhas = PRIMEIRO_ID_REVANCHE, []
    for const, _, dono, _ in revanches:
        while nid in usados:
            nid += 1
        assert nid <= TETO_ID, "acabou a faixa de ids de treinador"
        linhas.append("#define %-48s %d  // time do hack de %s" % (const, nid, dono))
        nid += 1
    bloco_ids = (MARCA_INI + "\n// Decisão 130: a campanha usa o time original; o do hack fica aqui,\n"
                 "// sem mapa ainda, para revanche e pós-jogo. Ids acima de 3276 (append-only).\n"
                 + "\n".join(linhas) + "\n" + MARCA_FIM + "\n")
    alvo = "#define MAX_TRAINERS_COUNT_EMERALD"
    i = opp.index(alvo)
    i = opp.rfind("\n", 0, i) + 1
    opp = opp[:i] + bloco_ids + "\n" + opp[i:]
    # 5. Fase F: o chefe casado passa a ser a revanche
    dono = {}
    for regiao in ("galar", "unova"):
        for r in json.load(open(CASAMENTO % regiao, encoding="utf-8"))["casados"]:
            dono[r["constante"]] = r["revanche"]
    movidos = 0
    for c in doc["chefes"]:
        if c["id"] in dono:
            c["id"] = dono[c["id"]]
            movidos += 1
    if gravar:
        open(PARTY, "w", encoding="utf-8").write(texto)
        open(OPPS, "w", encoding="utf-8").write(opp)
        # mesmo formato do arquivo de hoje: recuo de 1, sem quebra no fim
        open(FASE_F, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1))
    print("party: %d times de campanha trocados, %d revanches, %d retratos, %d chefes da Fase F movidos"
          % (len(novos), len(revanches), trocas, movidos))
    return dict(campanha=len(novos), revanches=len(revanches), retratos=trocas, fase_f=movidos)


def rotulos_e_treinadores():
    """{rótulo de script: primeira constante de treinador da batalha dele}."""
    arquivos = glob.glob(os.path.join(RAIZ, "data/maps/*/scripts.inc")) + [INC_GALAR]
    fora = {}
    for f in arquivos:
        rot = None
        for ln in open(f, encoding="utf-8", errors="ignore"):
            m = re.match(r"^(\w+):{1,2}\s*$", ln)
            if m:
                rot = m.group(1)
                continue
            if rot and rot not in fora and re.match(r"\s*trainerbattle", ln):
                t = re.search(r"\bTRAINER_(?:GALAR|UNOVA)_\w+", ln)
                if t:
                    fora[rot] = t.group(0)
    return fora


def aplica_npcs(gravar=True):
    _, atual = le_party(PARTY)
    rt = rotulos_e_treinadores()
    gfx_ok = set(re.findall(r"(?m)^\s*(?:#define\s+)?(OBJ_EVENT_GFX_(?:GALAR|UNOVA)_\w+)\b",
                            open(os.path.join(RAIZ, "include/constants/event_objects.h")).read()))
    trocas = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "data/maps/*/map.json"))):
        mp = f.split(os.sep)[-2]
        if not mp.startswith(("Galar_", "Unova_")):
            continue
        regiao = "galar" if mp.startswith("Galar_") else "unova"
        chars = GFX_GALAR if regiao == "galar" else GFX_UNOVA
        texto = open(f, encoding="utf-8").read()
        d = json.loads(texto)
        mudou = False
        for k, o in enumerate(d.get("object_events", [])):
            g = o.get("graphics_id", "")
            if g.startswith("OBJ_EVENT_GFX_VAR") or g.startswith("OBJ_EVENT_GFX_%s_" % regiao.upper()):
                continue
            ch = None
            t = rt.get(o.get("script", ""))
            if t and t in atual:
                ch = personagem(t, campo(atual[t].split("\n"), "Name"), regiao)
            if not ch and regiao == "unova":
                partes = re.split(r"_", o.get("script", ""))
                ult = partes[-1] if partes else ""
                for c in chars:
                    if re.fullmatch(r"(Cena)?%s\d*" % c.capitalize(), ult):
                        ch = c
            if ch in chars:
                novo = "OBJ_EVENT_GFX_%s_%s" % (regiao.upper(), ch)
                if novo in gfx_ok:
                    trocas.append(dict(mapa=mp, objeto=k, de=g, para=novo, script=o.get("script")))
                    o["graphics_id"] = novo
                    mudou = True
        if mudou and gravar:
            novo = json.dumps(d, indent=2, ensure_ascii=False)
            open(f, "w", encoding="utf-8").write(novo + ("\n" if texto.endswith("\n") else ""))
    print("NPC: %d objetos trocados" % len(trocas))
    return trocas


# ------------------------------------------------------------------ encontros
TAXAS = {"land_mons": [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1],
         "fishing_mons": [70, 30, 60, 20, 20, 40, 40, 15, 4, 1]}
GRUPOS_PESCA = [(0, 2), (2, 5), (5, 10)]


def quantiza(slots, taxas):
    """Distribui espécies de chance livre nas cotas fixas do GBA: cada cota vai
    para a espécie que mais falta receber (maior chance restante)."""
    total = sum(c for _, c in slots) or 1
    resta = {i: c * sum(taxas) / total for i, (_, c) in enumerate(slots)}
    fora = []
    for t in taxas:
        i = max(resta, key=lambda j: (resta[j], -j))
        fora.append(slots[i][0])
        resta[i] -= t
    return fora


def especie_swsh(ent, especies_ok):
    sys.path.insert(0, POC_A)
    import gera_party_swsh as GS  # noqa: E402
    e, f = ent["especie_id"], ent["forma"]
    suf = GS.FORMAS.get((e, f)) if f else GS.FORMA_ZERO.get(e)
    sp = "SPECIES_" + suf if suf else GS.const("SPECIES", ent["especie"])
    return sp if sp in especies_ok else None


def aplica_encontros(gravar=True):
    especies_ok = set(re.findall(r"(?m)^\s*(?:#define\s+)?(SPECIES_\w+)\s*[=\s]", open(os.path.join(RAIZ, "include/constants/species.h")).read()))
    pasta = {}
    for f in glob.glob(os.path.join(RAIZ, "data/maps/*/map.json")):
        d = json.load(open(f, encoding="utf-8"))
        pasta[d["id"]] = f.split(os.sep)[-2]
    texto = open(WILD, encoding="utf-8").read()
    wild = json.loads(texto)
    grupo = wild["wild_encounter_groups"][0]
    enc = grupo["encounters"]
    por_mapa = collections.defaultdict(list)
    for e in enc:
        por_mapa[e["map"]].append(e)
    rel = dict(unova=dict(trocados=[], novos=[], mantidos=[], subtabelas_mantidas=0),
               galar=dict(trocados=[], mantidos=[], subtabelas_mantidas=0))
    # Unova: o JSON do Black 2 já está no formato do repo e valida no conversor.
    bw2 = json.load(open(os.path.join(SAIDA, "bw2_wild_encounters.json"), encoding="utf-8"))
    for e in bw2["wild_encounter_groups"][0]["encounters"]:
        mp = e["map"]
        if mp not in pasta:
            continue
        if mp in por_mapa and len(por_mapa[mp]) == 1:
            cur = por_mapa[mp][0]
            for k in ("land_mons", "water_mons", "fishing_mons", "rock_smash_mons"):
                if k in e:
                    taxa = cur.get(k, {}).get("encounter_rate", e[k]["encounter_rate"])
                    cur[k] = dict(encounter_rate=taxa, mons=e[k]["mons"])
                elif k in cur:
                    rel["unova"]["subtabelas_mantidas"] += 1
            rel["unova"]["trocados"].append(mp)
        elif mp not in por_mapa and any(k in e for k in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons")):
            novo = collections.OrderedDict(map=mp, base_label="g" + pasta[mp].replace("_", ""))
            for k in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
                if k in e:
                    novo[k] = e[k]
            enc.append(novo)
            rel["unova"]["novos"].append(mp)
    rel["unova"]["mantidos"] = sorted(m for m in por_mapa if m.startswith("MAP_UNOVA_")
                                      and m not in rel["unova"]["trocados"])
    # Galar: zona do Shield que mais divide espécie com a grama de hoje.
    sw = json.load(open(os.path.join(SAIDA, "swsh_encontros.json"), encoding="utf-8"))
    zonas = []
    for z in sw["shield_zonas"]:
        st = z["subtabelas"]
        if not st[0]["slots"]:
            continue
        esp = {especie_swsh(s, especies_ok) for s in st[0]["slots"]} - {None}
        zonas.append((z["zona"], esp, z))
    for mp in sorted(por_mapa):
        if not mp.startswith("MAP_GALAR_") or len(por_mapa[mp]) != 1:
            if mp.startswith("MAP_GALAR_"):
                rel["galar"]["mantidos"].append(dict(mapa=mp, motivo="mapa com mais de uma tabela (variantes)"))
            continue
        cur = por_mapa[mp][0]
        if "land_mons" not in cur:
            rel["galar"]["mantidos"].append(dict(mapa=mp, motivo="sem grama hoje"))
            continue
        hoje = {m["species"] for m in cur["land_mons"]["mons"]}
        melhor = None
        for nome, esp, z in zonas:
            ov = len(hoje & esp)
            jac = ov / len(hoje | esp)
            rota = re.match(r"MAP_GALAR_ROUTE(\d\d)_", mp)
            bonus = 0.05 if rota and nome.startswith("z_r%s" % rota.group(1)) else 0
            if ov >= 2 and (melhor is None or jac + bonus > melhor[0]):
                melhor = (jac + bonus, nome, z, ov, jac)
        if not melhor or melhor[4] < 0.25:
            rel["galar"]["mantidos"].append(dict(mapa=mp, motivo="nenhuma zona do Shield divide 2 espécies e 25% da grama"
                                                 + (" (melhor: %s, %.0f%%)" % (melhor[1], 100 * melhor[4]) if melhor else "")))
            continue
        _, nome, z, ov, jac = melhor
        st = z["subtabelas"]
        slots = [(especie_swsh(s, especies_ok), s["chance"]) for s in st[0]["slots"]]
        slots = [(s, c) for s, c in slots if s]
        mons = [dict(min_level=st[0]["nivel_min"], max_level=st[0]["nivel_max"], species=s)
                for s in quantiza(slots, TAXAS["land_mons"])]
        cur["land_mons"] = dict(encounter_rate=cur["land_mons"]["encounter_rate"], mons=mons)
        pesca = [(especie_swsh(s, especies_ok), s["chance"]) for s in st[10]["slots"]]
        pesca = [(s, c) for s, c in pesca if s]
        if pesca:
            pm = []
            for a, b in GRUPOS_PESCA:
                pm += [dict(min_level=st[10]["nivel_min"], max_level=st[10]["nivel_max"], species=s)
                       for s in quantiza(pesca, TAXAS["fishing_mons"][a:b])]
            taxa = cur.get("fishing_mons", {}).get("encounter_rate", 30)
            cur["fishing_mons"] = dict(encounter_rate=taxa, mons=pm)
        for k in ("water_mons", "rock_smash_mons") + (() if pesca else ("fishing_mons",)):
            if k in cur:
                rel["galar"]["subtabelas_mantidas"] += 1
        rel["galar"]["trocados"].append(dict(mapa=mp, zona=nome, especies_em_comum=ov,
                                             semelhanca=round(jac, 2), pesca=bool(pesca)))
    if gravar:
        open(WILD, "w", encoding="utf-8").write(json.dumps(wild, indent=2, ensure_ascii=False) + "\n")
        json.dump(rel, open(ENCONTROS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("encontros: Unova %d trocados e %d novos (%d mantidos); Galar %d trocados (%d mantidos)"
          % (len(rel["unova"]["trocados"]), len(rel["unova"]["novos"]), len(rel["unova"]["mantidos"]),
             len(rel["galar"]["trocados"]), len(rel["galar"]["mantidos"])))
    return rel


# ------------------------------------------------------------------ demo
def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-66s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    _, atual = le_party(PARTY)
    opp = open(OPPS, encoding="utf-8").read()
    ids = {k: int(v) for k, v in re.findall(r"(?m)^#define (TRAINER_\w+)\s+(\d+)", opp)}
    doc = json.load(open(FASE_F, encoding="utf-8"))
    for regiao in ("galar", "unova"):
        cas = json.load(open(CASAMENTO % regiao, encoding="utf-8"))
        rs = cas["casados"]
        caso("%s: toda revanche existe no .party e tem id acima de 3276" % regiao,
             all(r["revanche"] in atual and ids.get(r["revanche"], 0) >= PRIMEIRO_ID_REVANCHE for r in rs))
        caso("%s: nenhum casado ficou com nível 223 ou 255 na campanha" % regiao,
             all(not set(niveis_do_bloco(atual[r["constante"]])) & {223, 255} for r in rs))
        caso("%s: casado e não casado não se cruzam" % regiao,
             not {r["constante"] for r in rs} & {r["constante"] for r in cas["nao_casados"]})
    ids_f = {c["id"] for c in doc["chefes"]}
    caso("nenhum chefe da Fase F aponta para constante sem bloco", ids_f <= set(atual))
    caso("nenhuma constante de campanha casada continua na Fase F",
         not ids_f & {r["constante"] for g in ("galar", "unova")
                      for r in json.load(open(CASAMENTO % g, encoding="utf-8"))["casados"]})
    # mutação: um time de 255 plantado na campanha tem que reprovar a régua acima
    r0 = json.load(open(CASAMENTO % "galar", encoding="utf-8"))["casados"][0]
    sujo = atual[r0["constante"]].replace("Level: ", "Level: 255\n#", 1)
    caso("mutação: nível 255 plantado num casado é visto", 255 in niveis_do_bloco(sujo))
    caso("quantiza: 40/30/15/10/5 em 12 cotas soma 100 e o mais comum leva as duas maiores",
         quantiza([("A", 40), ("B", 30), ("C", 15), ("D", 10), ("E", 5)], TAXAS["land_mons"])[:2] == ["A", "B"])
    print("DEMO", "VERDE" if ok else "VERMELHO")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--casar", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.casar:
        casar()
    if a.aplicar:
        aplica_party()
        aplica_npcs()
        aplica_encontros()
    if a.demo:
        sys.exit(0 if demo() else 1)
    if not (a.casar or a.aplicar or a.demo):
        ap.print_help()


if __name__ == "__main__":
    main()
