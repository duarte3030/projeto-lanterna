#!/usr/bin/env python3
"""Testes críticos T1 a T11: prova, lendo a EWRAM, que o jogo faz o que deve.

Uso:
    python3 dev_scripts/testa_critico.py                 # roda tudo
    python3 dev_scripts/testa_critico.py T2              # roda só os casos T2.*
    python3 dev_scripts/testa_critico.py --lista         # lista sem rodar
    python3 dev_scripts/testa_critico.py --rom outra.gba # ROM congelada
    python3 dev_scripts/testa_critico.py --censo         # varre TODOS os grupos de mapa
    python3 dev_scripts/testa_critico.py --treinadores   # acusa constante de treinador falsa

T11, a save do Gui sobrevive à atualização da ROM
-------------------------------------------------
Precisa de duas builds e das duas árvores de fonte correspondentes, porque os
offsets dentro do SaveBlock1 têm que ser lidos de CADA uma (ver
`offsets_da_fonte`). Guarde a ROM antiga com um `include/` ao lado dela:

    python3 dev_scripts/testa_critico.py T11 \
        --rom  ~/roms/antiga/pokeemerald.gba  --src  ~/roms/antiga \
        --rom2 pokeemerald.gba                --src2 .

T11.1 joga e salva, T11.2 confere que a save volta na mesma ROM (é o controle
que prova que o .sav está mesmo sendo lido), e T11.3 carrega a MESMA save na
ROM nova. Sem `--rom2`, o T11.3 é PULADO e dito em voz alta, nunca contado
como passou.

Por que este arquivo existe
---------------------------
`testa_percurso.py` olha pixel: ele sabe dizer que a tela mudou, não que o jogo
está certo. Dois crashes da sessão de 05/08/2026 passaram por seis agentes e
dois validadores porque todo teste era desse tipo. Aqui cada teste afirma um
fato lido da memória do jogo: "o mapa atual é MAP_PEWTER_CITY_GYM", "o time tem
1 Pokémon", "a flag FLAG_X está acesa". Critério "não travou" não existe aqui:
`prova` é campo obrigatório do caso de teste, e caso sem prova é recusado.

Como funciona
-------------
1. O `gba_runner` roda a ROM headless e imprime linhas `ESTADO ... chave=valor`
   lidas da EWRAM (ver o cabeçalho de ferramentas/gba_runner.c).
2. Os endereços que mudam a cada link (`gSaveBlock1Ptr`, `gPartiesCount`) saem
   do `pokeemerald.map` ao lado da ROM, então rebuild não invalida o teste.
3. Cada caso vive em `dev_scripts/testes_criticos/*.json`, um arquivo por bloco
   de testes, para várias pessoas escreverem caso sem conflitar no mesmo arquivo.

Formato de um caso
------------------
{
  "id": "T2.1",
  "nome": "Ginásio de Pewter carrega",
  "flags": ["FLAG_BADGE01_GET", "0x2A0"],   # acesas por escrita direta na EWRAM
  "vars": {"0x4001": 3},                    # opcional
  "warp": "MAP_PEWTER_CITY_GYM",            # warp pelo menu de debug, opcional
  "roteiro": "20:UP*6,60:NADA",             # botões depois do warp, opcional
  "prova": {                                # obrigatório, e não pode ser vazio
     "mapa": "MAP_PEWTER_CITY_GYM",         # mapa atual no fim
     "time": 1,                             # tamanho do time (>= por padrão? não: igual)
     "time_min": 1,                         # alternativa: pelo menos N
     "flags_acesas": ["FLAG_..."],          # cada uma tem que estar em 1
     "flags_apagadas": ["FLAG_..."],
     "vars": {"0x4001": 3},
     "mapa_grupo": 79                       # quando só o grupo importa (região)
  }
}
"""
import glob
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Fonte do runner: dev_scripts/gba_runner.c (o cabeçalho dele tem o comando de
# compilação). Se o binário local não existir, cai no que já está compilado na
# pasta de ferramentas do workspace.
RUNNER = os.path.join(RAIZ, "dev_scripts", "gba_runner")
if not os.path.exists(RUNNER):
    RUNNER = ("/Users/duarte/Documents/ANTIGRAVITY/Pokemon Claude/Pokemon Claude"
              "/ferramentas/gba_runner")
SAIDA = "/tmp/claude-501/frenteA/testes"
CASOS_DIR = os.path.join(RAIZ, "dev_scripts", "testes_criticos")

# Abertura até o jogador ter o controle no overworld. Medido nesta sessão.
ABERTURA = ("90:A,90:A,90:A,90:A,90:A,240:NADA,120:A*14,240:NADA,120:A*10,"
            "240:NADA,120:A*20,300:NADA,120:A*20,300:NADA")

# Com um .sav existente, o menu de título abre em "CONTINUAR" e um A basta.
CONTINUAR = "90:A,90:A,90:A,240:NADA,120:A,300:NADA,300:NADA"

ABERTURAS = {"novo": ABERTURA, "continuar": CONTINUAR, "nenhuma": ""}


# --------------------------------------------------------------------------
# Tabelas do repo. Nunca chutar número de mapa ou de flag de memória.
# --------------------------------------------------------------------------
def carrega_mapas():
    caminho = os.path.join(RAIZ, "include", "constants", "map_groups.h")
    por_nome, por_id = {}, {}
    padrao = re.compile(r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)")
    for nome, num, grupo in padrao.findall(open(caminho).read()):
        chave = (int(grupo), int(num))
        por_nome[nome] = chave
        por_id.setdefault(chave, nome)
    return por_nome, por_id


def carrega_flags():
    caminho = os.path.join(RAIZ, "include", "constants", "flags.h")
    padrao = re.compile(r"^#define\s+(FLAG_[A-Z0-9_]+)\s+(0[xX][0-9A-Fa-f]+|\d+)\s*$", re.M)
    return {n: int(v, 0) for n, v in padrao.findall(open(caminho).read())}


def carrega_layouts():
    caminho = os.path.join(RAIZ, "include", "constants", "layouts.h")
    padrao = re.compile(r"^#define\s+(LAYOUT_[A-Z0-9_]+)\s+(\d+)\s*$", re.M)
    return {n: int(v) for n, v in padrao.findall(open(caminho).read())}


def carrega_simbolos(mapfile):
    alvos = {"gSaveBlock1Ptr": None, "gPartiesCount": None}
    padrao = re.compile(r"^\s+(0x[0-9a-f]+)\s+(\w+)\s*$")
    with open(mapfile) as f:
        for linha in f:
            m = padrao.match(linha)
            if m and m.group(2) in alvos and alvos[m.group(2)] is None:
                alvos[m.group(2)] = m.group(1)
    faltando = [k for k, v in alvos.items() if v is None]
    if faltando:
        raise SystemExit(f"símbolo não achado em {mapfile}: {faltando}")
    return alvos


def offsets_da_fonte(src):
    """Offsets dentro de SaveBlock1, MEDIDOS compilando contra o global.h do `src`.

    Existe porque leitor com offset chumbado não é testemunha, é adivinho. Se
    alguém mover `flags[]` dentro do SaveBlock1, uma save antiga continua tendo
    o valor velho no offset velho: o leitor chumbado lê aquele valor, acha tudo
    certo, e o teste de compatibilidade de save passa com a save quebrada. Foi
    exatamente o que aconteceu em 05/08/2026 quando eu inseri um u32 antes de
    `flags[]` de propósito e o T11 passou mesmo assim.

    Também pega o caso silencioso do comentário mentiroso: `include/global.h`
    diz `/*0x139C*/ u16 vars[...]` e o valor real desta build é 0x13E0.
    """
    devkit = os.environ.get("DEVKITARM",
                            os.path.expanduser("~/toolchains/arm-gnu-toolchain-15.2."
                                               "rel1-darwin-arm64-arm-none-eabi"))
    gcc = os.path.join(devkit, "bin", "arm-none-eabi-gcc")
    objdump = os.path.join(devkit, "bin", "arm-none-eabi-objdump")
    if not os.path.exists(gcc):
        raise SystemExit(f"arm-none-eabi-gcc não encontrado em {gcc}. "
                         "Exporte DEVKITARM.")
    tmp = "/tmp/claude-501/frenteA/offsets"
    os.makedirs(tmp, exist_ok=True)
    probe = os.path.join(tmp, "probe.c")
    obj = os.path.join(tmp, "probe.o")
    with open(probe, "w") as f:
        f.write("#include \"global.h\"\n"
                "const unsigned gP[] = {\n"
                "  offsetof(struct SaveBlock1, location),\n"
                "  offsetof(struct SaveBlock1, mapLayoutId),\n"
                "  offsetof(struct SaveBlock1, playerPartyCount),\n"
                "  offsetof(struct SaveBlock1, flags),\n"
                "  offsetof(struct SaveBlock1, vars),\n"
                "  FLAGS_COUNT, VARS_COUNT,\n"
                "};\n")
    r = subprocess.run([gcc, "-c", "-iquote", "include", "-Wno-trigraphs",
                        "-DMODERN=1", "-DTESTING=0", "-DEMERALD", "-std=gnu17",
                        "-mthumb", "-mabi=apcs-gnu", "-march=armv4t", "-O0",
                        "-o", obj, probe],
                       cwd=src, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("não consegui medir os offsets de SaveBlock1 em "
                         f"{src}:\n{r.stderr[-800:]}")
    d = subprocess.run([objdump, "-s", "-j", ".rodata", obj],
                       capture_output=True, text=True).stdout
    palavras = []
    for linha in d.splitlines():
        m = re.match(r"^ [0-9a-f]{4} ((?:[0-9a-f]{8} ?){1,4})", linha)
        if m:
            for p in m.group(1).split():
                palavras.append(int.from_bytes(bytes.fromhex(p), "little"))
    if len(palavras) < 7:
        raise SystemExit(f"leitura de offsets falhou em {src}: {d[:300]}")
    return palavras[:7]


def num_flag(nome, tabela):
    if isinstance(nome, int):
        return nome
    if nome.startswith("0x") or nome.isdigit():
        return int(nome, 0)
    if nome not in tabela:
        raise KeyError(f"flag desconhecida: {nome}")
    return tabela[nome]


# --------------------------------------------------------------------------
# Roteiro de botões do menu de debug.
#
# Lido de src/debug.c, não descoberto por tentativa e erro:
#   - R+START abre sDebugMenu_Actions_Main, cursor no item 0 "Utilities…"
#   - dentro de Utilities, item 0 é "Fly to map…" e item 1 "Warp to map warp…"
#   - a entrada é numérica de 3 dígitos (Debug_HandleInput_Numeric):
#     UP soma sPowersOfTen[tDigit], e sPowersOfTen[0] == 1, ou seja tDigit 0 é a
#     unidade; RIGHT anda para o dígito mais significativo, LEFT volta.
#     A ordem centena -> dezena -> unidade nunca ultrapassa o máximo no meio do
#     caminho, então nunca bate no clamp de Debug_HandleInput_Numeric.
# --------------------------------------------------------------------------
def digita_numero(valor):
    c, d, u = valor // 100, (valor // 10) % 10, valor % 10
    passos = ["12:RIGHT", "12:RIGHT"]
    if c:
        passos.append(f"12:UP*{c}")
    passos.append("12:LEFT")
    if d:
        passos.append(f"12:UP*{d}")
    passos.append("12:LEFT")
    if u:
        passos.append(f"12:UP*{u}")
    return ",".join(passos)


def rota_warp(grupo, num, warp=0):
    return ",".join([
        "40:R+START!", "60:NADA",
        "20:A", "40:NADA",
        "20:DOWN", "20:A", "60:NADA",
        digita_numero(grupo), "20:A", "40:NADA",
        digita_numero(num), "20:A", "40:NADA",
        digita_numero(warp), "20:A", "300:NADA",
    ])


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------
LINHA_ESTADO = re.compile(r"^ESTADO (\S+) (.*)$")


def roda(rom, simbolos, roteiro, prefixo, flags_lidas=(), vars_lidas=(), sav=None,
         offsets=None):
    os.makedirs(SAIDA, exist_ok=True)
    for f in glob.glob(f"{SAIDA}/{prefixo}-*.png"):
        os.remove(f)
    cmd = [RUNNER, rom, "900", roteiro, f"{SAIDA}/{prefixo}.png", "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"]]
    if offsets:
        cmd += ["--offsets", ",".join(str(v) for v in offsets)]
    for f in flags_lidas:
        cmd += ["--flag", hex(f)]
    for v in vars_lidas:
        cmd += ["--var", hex(v)]
    if sav:
        cmd += ["--sav", sav]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    estados = []
    for linha in p.stdout.splitlines():
        m = LINHA_ESTADO.match(linha)
        if not m:
            continue
        d = {"rotulo": m.group(1)}
        for par in m.group(2).split():
            k, _, v = par.partition("=")
            d[k] = int(v, 0)
        estados.append(d)
    if not estados:
        raise RuntimeError("gba_runner não imprimiu estado nenhum. stderr:\n"
                           + p.stderr[-800:])
    return estados


def monta_roteiro(caso, por_nome, tabela_flags):
    modo = caso.get("abertura", "novo")
    if modo not in ABERTURAS:
        raise KeyError(f"abertura desconhecida: {modo}. Use {list(ABERTURAS)}")
    partes = [ABERTURAS[modo]] if ABERTURAS[modo] else []
    for f in caso.get("flags", []):
        partes.append(f"6:FLAG={num_flag(f, tabela_flags)}")
    for var, val in caso.get("vars", {}).items():
        partes.append(f"6:VAR={int(var, 0)}={val}")
    if caso.get("warp"):
        if caso["warp"] not in por_nome:
            raise KeyError(f"mapa de warp desconhecido: {caso['warp']}")
        g, n = por_nome[caso["warp"]]
        partes.append(rota_warp(g, n, caso.get("warp_id", 0)))
    if caso.get("roteiro"):
        partes.append(caso["roteiro"])
    # prova de vida no fim: abrir o menu tem que mudar a tela. Não substitui a
    # prova de estado, é só um sinal a mais quando a prova falha.
    partes.append("60:NADA")
    return ",".join(partes)


def confere(caso, estados, por_nome, por_id, tabela_flags, layouts):
    falhas = []
    final = estados[-1]
    prova = caso["prova"]

    if not final.get("sb1"):
        return ["RESET: gSaveBlock1Ptr voltou a zero, o jogo reiniciou"]

    atual = (final["grupo"], final["num"])
    nome_atual = por_id.get(atual, f"grupo {atual[0]} mapa {atual[1]} (sem nome)")

    # Checagem que TODO caso ganha de graça, e que existe por um erro medido:
    # SetWarpDestination grava location ANTES de o mapa carregar, então
    # "location está certo" NÃO prova que o mapa entrou. Em 05/08/2026 um warp
    # para MAP_PEWTER_CITY deixou location=37.2 com a tela preta e
    # mapLayoutId=26651, lixo fora de faixa. mapLayoutId só muda quando o mapa
    # carrega de verdade, então é ele que separa "chegou" de "tentou".
    maior_layout = max(layouts.values())
    if not (1 <= final.get("layout", 0) <= maior_layout):
        falhas.append(f"MAPA NÃO CARREGOU: mapLayoutId={final.get('layout')} está fora da "
                      f"faixa 1..{maior_layout}. O jogo gravou location={nome_atual} mas "
                      "nunca entrou no mapa (tela preta).")
    elif "layout" in prova:
        esperado = layouts.get(prova["layout"])
        if esperado is None:
            falhas.append(f"layout da prova não existe: {prova['layout']}")
        elif final["layout"] != esperado:
            falhas.append(f"layout errado: esperado {prova['layout']}={esperado}, "
                          f"obtido {final['layout']}")

    if "mapa" in prova:
        esperado = por_nome.get(prova["mapa"])
        if esperado is None:
            falhas.append(f"mapa da prova não existe em map_groups.h: {prova['mapa']}")
        elif atual != esperado:
            falhas.append(f"mapa errado: esperado {prova['mapa']} ({esperado[0]}.{esperado[1]}), "
                          f"obtido {nome_atual} ({atual[0]}.{atual[1]})")

    if "mapa_grupo" in prova and final["grupo"] != prova["mapa_grupo"]:
        falhas.append(f"grupo de mapa errado: esperado {prova['mapa_grupo']}, "
                      f"obtido {final['grupo']} ({nome_atual})")

    if "mapa_um_de" in prova:
        aceitos = {por_nome[m] for m in prova["mapa_um_de"] if m in por_nome}
        if atual not in aceitos:
            falhas.append(f"mapa fora da lista aceita: obtido {nome_atual}")

    if "time" in prova and final["timevivo"] != prova["time"]:
        falhas.append(f"time com {final['timevivo']} Pokémon, esperado {prova['time']}")

    if "time_min" in prova and final["timevivo"] < prova["time_min"]:
        falhas.append(f"time com {final['timevivo']} Pokémon, esperado pelo menos "
                      f"{prova['time_min']}")

    for nome in prova.get("flags_acesas", []):
        chave = f"flag_{hex(num_flag(nome, tabela_flags)).upper().replace('0X', '0x')}"
        if final.get(chave) != 1:
            falhas.append(f"flag {nome} deveria estar acesa e está {final.get(chave)}")

    for nome in prova.get("flags_apagadas", []):
        chave = f"flag_{hex(num_flag(nome, tabela_flags)).upper().replace('0X', '0x')}"
        if final.get(chave) != 0:
            falhas.append(f"flag {nome} deveria estar apagada e está {final.get(chave)}")

    for var, val in prova.get("vars", {}).items():
        chave = f"var_{hex(int(var, 0)).upper().replace('0X', '0x')}"
        if final.get(chave) != val:
            falhas.append(f"var {var} vale {final.get(chave)}, esperado {val}")

    return falhas


def censo(rom, simbolos, offsets, por_nome, por_id, layouts, trabalhadores=6):
    """Warpa para o mapa 0 de CADA grupo e diz quais não carregam.

    Os casos de teste cobrem mapa nomeado, um a um. Este censo cobre o resto: é
    ele que responde "quais regiões inteiras estão quebradas" em três minutos,
    em vez de descobrir mapa por mapa. Foi assim que a tela preta de Kanto
    apareceu como classe, e não como caso isolado.
    """
    from concurrent.futures import ThreadPoolExecutor
    maior_layout = max(layouts.values())
    grupos = sorted({g for g, _ in por_id})

    def um(grupo):
        nome = por_id.get((grupo, 0), f"grupo {grupo} mapa 0")
        try:
            est = roda(rom, simbolos, ABERTURA + "," + rota_warp(grupo, 0),
                       f"censo_{grupo:03d}", offsets=offsets)[-1]
        except Exception as e:                                      # noqa: BLE001
            return grupo, nome, f"ERRO {e}"
        if not est.get("sb1"):
            return grupo, nome, "RESET"
        if not (1 <= est.get("layout", 0) <= maior_layout):
            return grupo, nome, f"NÃO CARREGA (layout={est.get('layout')})"
        if (est["grupo"], est["num"]) != (grupo, 0):
            return grupo, nome, f"foi parar em {est['grupo']}.{est['num']}"
        return grupo, nome, "ok"

    with ThreadPoolExecutor(max_workers=trabalhadores) as ex:
        resultados = list(ex.map(um, grupos))

    ruins = [r for r in resultados if r[2] != "ok"]
    for grupo, nome, veredito in resultados:
        if veredito != "ok":
            print(f"[FALHA] grupo {grupo:3d}  {nome:45} {veredito}")
    print(f"\n{len(resultados) - len(ruins)}/{len(resultados)} grupos carregam o mapa 0")
    return 1 if ruins else 0


def confere_treinadores():
    """Acusa constante de treinador que é apelido de OUTRO treinador.

    `include/constants/opponents_frlg.h` numera os treinadores de Kanto de 0 a
    623, e `include/constants/opponents.h` numera os de Hoenn, Johto e Sinnoh de
    0 a 1366, no MESMO espaço. Quem só tem nome ali e não tem entrada em
    `src/data/trainers.party` não é um treinador: é um apelido que aponta para
    quem já ocupa aquele id. `TRAINER_YOUNGSTER_BEN` (Kanto, 1) é
    `TRAINER_SAWYER_1` (Hoenn, 1).

    Isso ficou inerte enquanto os 418 includes de Kanto estavam atrás do
    `.if IS_FRLG` de data/event_scripts.s. Abrindo o portão, cada batalha de
    treinador de Kanto passa a chamar o treinador errado, e o jogo não reclama:
    o id existe, o time existe, só é de outra pessoa. Nenhum teste de tela pega
    isso, e nenhum aviso de compilação também, porque os nomes são únicos.

    Roda sem ROM e sem emulador: é fato de compilação.
    """
    def defines(caminho):
        return dict(re.findall(r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$",
                               open(os.path.join(RAIZ, caminho)).read(), re.M))

    frlg = defines("include/constants/opponents_frlg.h")
    principal = defines("include/constants/opponents.h")
    party = set(re.findall(r"^=== (TRAINER_[A-Z0-9_]+) ===",
                           open(os.path.join(RAIZ, "src/data/trainers.party")).read(), re.M))
    por_id = {int(v): k for k, v in principal.items()}

    apelidos = {n: int(v) for n, v in frlg.items() if n not in party}
    usados = set()
    for arq in glob.glob(os.path.join(RAIZ, "data/maps/*/scripts.inc")):
        texto = open(arq, errors="ignore").read()
        for nome in re.findall(r"\bTRAINER_[A-Z0-9_]+\b", texto):
            if nome in apelidos:
                usados.add((os.path.basename(os.path.dirname(arq)), nome))

    print(f"constantes de treinador em opponents_frlg.h: {len(frlg)}")
    print(f"  sem time próprio em trainers.party (apelidam outro treinador): {len(apelidos)}")
    print(f"  desses, usados por script de mapa: {len({n for _, n in usados})} "
          f"em {len({m for m, _ in usados})} mapas")
    for mapa, nome in sorted(usados)[:10]:
        print(f"    {mapa:38} {nome:34} -> id {apelidos[nome]} = "
              f"{por_id.get(apelidos[nome], '?')}")
    if len(usados) > 10:
        print(f"    ... e mais {len(usados) - 10}")

    colisoes = [n for n in frlg if n in principal and frlg[n] != principal[n]]
    for n in colisoes:
        print(f"[FALHA] {n} vale {frlg[n]} em opponents_frlg.h e {principal[n]} em "
              "opponents.h. Um dos dois scripts luta com o treinador errado.")

    if not apelidos and not colisoes:
        print("nenhum apelido e nenhuma colisão de constante de treinador")
        return 0
    return 1


def carrega_casos():
    casos = []
    for arq in sorted(glob.glob(os.path.join(CASOS_DIR, "*.json"))):
        for caso in json.load(open(arq)):
            if not caso.get("prova"):
                raise SystemExit(f"{os.path.basename(arq)}: caso {caso.get('id')} "
                                 "não tem prova. Teste sem prova não entra.")
            caso["_arquivo"] = os.path.basename(arq)
            casos.append(caso)
    casos.sort(key=lambda c: [int(p) for p in c["id"].lstrip("T").split(".")])
    return casos


def main():
    args = sys.argv[1:]
    rom = os.path.join(RAIZ, "pokeemerald.gba")
    rom2 = None
    if "--rom" in args:
        i = args.index("--rom")
        rom = args[i + 1]
        del args[i:i + 2]
    src, src2 = RAIZ, None
    if "--rom2" in args:
        i = args.index("--rom2")
        rom2 = args[i + 1]
        del args[i:i + 2]
    if "--src" in args:
        i = args.index("--src")
        src = args[i + 1]
        del args[i:i + 2]
    if "--src2" in args:
        i = args.index("--src2")
        src2 = args[i + 1]
        del args[i:i + 2]
    so_lista = "--lista" in args
    if so_lista:
        args.remove("--lista")
    faz_censo = "--censo" in args
    if faz_censo:
        args.remove("--censo")
    if "--treinadores" in args:
        return confere_treinadores()
    filtro = args[0] if args else None

    mapfile = os.path.splitext(rom)[0] + ".map"
    if not os.path.exists(rom):
        raise SystemExit(f"ROM não encontrada: {rom}")
    if not os.path.exists(mapfile):
        raise SystemExit(f"mapfile não encontrado ao lado da ROM: {mapfile}")
    if not os.path.exists(RUNNER):
        raise SystemExit(f"gba_runner não encontrado: {RUNNER}")

    por_nome, por_id = carrega_mapas()
    tabela_flags = carrega_flags()
    layouts = carrega_layouts()
    simbolos = carrega_simbolos(mapfile)
    if faz_censo:
        return censo(rom, simbolos, offsets_da_fonte(src), por_nome, por_id, layouts)

    casos = carrega_casos()
    if filtro:
        casos = [c for c in casos if c["id"].split(".")[0] == filtro or c["id"] == filtro]

    if so_lista:
        for c in casos:
            print(f"{c['id']:8} {c['nome']}   [{c['_arquivo']}]")
        return 0
    if not casos:
        raise SystemExit("nenhum caso de teste encontrado em " + CASOS_DIR)

    offsets = offsets_da_fonte(src)
    offsets2 = offsets_da_fonte(src2) if (rom2 and src2) else offsets
    print(f"ROM  {rom}")
    print(f"sym  gSaveBlock1Ptr={simbolos['gSaveBlock1Ptr']} "
          f"gPartiesCount={simbolos['gPartiesCount']}")
    print(f"off  location={offsets[0]} layout={offsets[1]} party={offsets[2]} "
          f"flags=0x{offsets[3]:X} vars=0x{offsets[4]:X} "
          f"nflags={offsets[5]} nvars={offsets[6]}  (fonte: {src})")
    if rom2:
        print(f"ROM2 {rom2}")
        if src2:
            print(f"off2 flags=0x{offsets2[3]:X} vars=0x{offsets2[4]:X}  (fonte: {src2})")
        else:
            print("off2 SEM --src2: os offsets da ROM2 estão sendo presumidos iguais "
                  "aos da ROM1. Se o SaveBlock mudou, este teste NÃO detecta.")
    print()

    reprovados = []
    pulados = []
    for caso in casos:
        prova = caso["prova"]
        # Caso marcado "rom": "rom2" roda na SEGUNDA ROM, para provar que uma save
        # feita na ROM antiga continua valendo depois de atualizar (T11). Sem
        # --rom2 o caso é PULADO e dito em voz alta, nunca contado como passou.
        if caso.get("rom") == "rom2":
            if not rom2:
                print(f"[PULA ] {caso['id']:8} {caso['nome']}")
                print("           faltou --rom2 <outra build>. Este caso só prova algo "
                      "com duas ROMs diferentes.")
                pulados.append(caso["id"])
                continue
            rom_do_caso = rom2
            simbolos_do_caso = carrega_simbolos(os.path.splitext(rom2)[0] + ".map")
            offsets_do_caso = offsets2
        else:
            rom_do_caso, simbolos_do_caso = rom, simbolos
            offsets_do_caso = offsets
        if caso.get("apaga_sav") and caso.get("sav") and os.path.exists(caso["sav"]):
            os.remove(caso["sav"])
        flags_lidas = [num_flag(n, tabela_flags)
                       for n in prova.get("flags_acesas", []) + prova.get("flags_apagadas", [])]
        vars_lidas = [int(v, 0) for v in prova.get("vars", {})]
        try:
            roteiro = monta_roteiro(caso, por_nome, tabela_flags)
            estados = roda(rom_do_caso, simbolos_do_caso, roteiro,
                           caso["id"].replace(".", "_"),
                           flags_lidas, vars_lidas, caso.get("sav"),
                           offsets_do_caso)
            falhas = confere(caso, estados, por_nome, por_id, tabela_flags, layouts)
        except Exception as e:                                  # noqa: BLE001
            falhas = [f"ERRO ao rodar: {e}"]
        marca = "OK   " if not falhas else "FALHA"
        print(f"[{marca}] {caso['id']:8} {caso['nome']}")
        for f in falhas:
            print(f"           {f}")
        if falhas:
            reprovados.append(caso["id"])

    passaram = len(casos) - len(reprovados) - len(pulados)
    print(f"\n{passaram}/{len(casos)} passaram")
    if reprovados:
        print("reprovados: " + ", ".join(reprovados))
    if pulados:
        print("pulados (não provam nada): " + ", ".join(pulados))
    return 1 if reprovados else 0


if __name__ == "__main__":
    sys.exit(main())
