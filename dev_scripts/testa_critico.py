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
        --rom2 pokeemerald.gba                --src2 . \
        --abertura intro_carvalho

O `--abertura intro_carvalho` é obrigatório quando a ROM antiga é anterior a
16/08/2026: o T11.1 grava a save NELA, e ela ainda tem a introdução do Carvalho,
que a abertura de hoje não sabe atravessar.

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
  "opcoes": 32,                             # byte do modo de teste, opcional.
                                            # LV.5 TRAINERS nasce LIGADA desde
                                            # 19/08/2026, então quem mede nível
                                            # natural de inimigo declara 32 aqui
                                            # (32 = só TURBO A/B; 36 = com LV.5)
  "antes_do_warp": "20:DOWN,60:NADA,20:A",  # apertos ANTES do warp, opcional
  "warp": "MAP_PEWTER_CITY_GYM",            # warp pelo menu de debug, opcional
  "roteiro": "20:UP*6,60:NADA",             # botões depois do warp, opcional
  "prova": {                                # obrigatório, e não pode ser vazio
     "mapa": "MAP_PEWTER_CITY_GYM",         # mapa atual no fim
     "time": 1,                             # tamanho do time (>= por padrão? não: igual)
     "time_min": 1,                         # alternativa: pelo menos N
     "flags_acesas": ["FLAG_..."],          # cada uma tem que estar em 1
     "flags_apagadas": ["FLAG_..."],
     "vars": {"0x4001": 3},
     "pos": [16, 2],                        # onde o jogador PAROU (x,y da save).
                                            # Prova de tile ocupado: objeto sólido
                                            # para o passo, então a posição final
                                            # separa "a bola estava lá" de "não".
     "palobj_presentes": ["0x32B9"],        # cor de 15 bits presente na PLTT OBJ
                                            # (prova que a palette do sprite carregou)
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

# Abertura até o jogador ter o controle no overworld.
#
# REMEDIDA em 17/08/2026, quadro a quadro no framebuffer, porque o jogo novo
# mudou: New Game não passa mais pela introdução do Carvalho (nem escolha de
# gênero, nem digitação de nome). Ele grava RED/GREEN/masculino direto e cai no
# quarto de Pallet Town, e no primeiro quadro em que o jogador ganha o controle
# abre o SELETOR DE CAPÍTULO (src/chapter_jump.c, gChapterJumpModo). A abertura
# antiga, feita de marteladas de A contra a introdução que não existe mais,
# gastava os apertos dentro do seletor e levava o jogo para outra região.
#
# A sequência medida (PNG por passo, o `roda` abaixo grava um por passo), já
# contando os 900 quadros iniciais que o gba_runner roda antes do roteiro:
#
#   1o A  intro do mato -> logotipo Pokémon
#   2o A  logotipo      -> tela de título
#   3o A  título        -> menu principal (NEW GAME / OPTION)
#   4o A  NEW GAME      -> quarto de Pallet Town, com o seletor de capítulo
#   DOWN  desce o cursor até "START FROM BEGINNING", a última linha
#   A     escolhe, o seletor fecha e o jogo segue do quarto, como sempre
#
# Regras de robustez, que valem para quem mexer aqui:
# - ESPERA é de graça, APERTO DE A não é. Depois que o seletor abre, dois A
#   seguidos escolhem região e capítulo, e o caso inteiro acorda em outro mapa.
#   Por isso os quatro A são exatos e as esperas é que são generosas.
# - `20:DOWN*5` é UM passo do roteiro com cinco toques rápidos, e a lista não dá
#   a volta: o cursor gruda na última linha. Toque a mais ali é inofensivo, e é
#   essa a folga que protege contra a lista mudar de tamanho.
# - Os dois B do fim são rede de segurança: no overworld B não faz nada, e se
#   por algum motivo um menu tiver ficado aberto, eles o fecham (B no seletor de
#   regiões cai no mesmo `releaseall` de "START FROM BEGINNING").
#
# ATE_O_SELETOR para no seletor ABERTO, e existe para os casos que provam o
# próprio seletor (T99): eles precisam escolher outra coisa que não
# "START FROM BEGINNING".
ATE_O_SELETOR = ("300:NADA,120:A,120:NADA,120:A,180:NADA,120:A,180:NADA,120:A,"
                 "420:NADA")
ABERTURA = ATE_O_SELETOR + ",20:DOWN*5,60:NADA,20:A,180:NADA,20:B*2,60:NADA"

# A abertura de ANTES de 16/08/2026, quando New Game ainda passava pela
# introdução do Carvalho. Ela NÃO serve para a build de hoje (as marteladas de A
# caem dentro do seletor de capítulo e mandam o jogo para outra região), e existe
# só para rodar contra uma ROM ANTIGA: é o caso do T11, que grava a save na build
# velha para provar que ela carrega na nova. Use `--abertura intro_carvalho`
# quando `--rom` for uma ROM anterior a 16/08/2026.
INTRO_CARVALHO = ("90:A,90:A,90:A,90:A,90:A,240:NADA,120:A*14,240:NADA,120:A*10,"
                  "240:NADA,120:A*20,300:NADA,120:A*20,300:NADA,"
                  # A ordem importa: A termina o diálogo, B fecha a caixa do NES
                  # se ela ainda estiver aberta (com caixa aberta o R+START não
                  # abre o menu de debug). Cadência medida no framebuffer.
                  "20:A*30,240:NADA,20:B*10,240:NADA")

# Com um .sav existente, o menu de título abre em "CONTINUAR" e um A basta.
CONTINUAR = "90:A,90:A,90:A,240:NADA,120:A,300:NADA,300:NADA"

ABERTURAS = {"novo": ABERTURA, "continuar": CONTINUAR, "nenhuma": "",
             "intro_carvalho": INTRO_CARVALHO, "seletor": ATE_O_SELETOR}

# Qual abertura vale para o caso que não declara a sua. Trocado por `--abertura`.
ABERTURA_PADRAO = "novo"


# --------------------------------------------------------------------------
# Tabelas do repo. Nunca chutar número de mapa ou de flag de memória.
# --------------------------------------------------------------------------
def carrega_mapas(src=None):
    """Tabela de mapas da FONTE DA ROM, não do repo.

    Os dois agentes de teste bateram nisto: se o repo já tem Unova e a ROM sob
    teste não, `map_groups.h` do repo descreve outro jogo. Mapa inserido no meio
    de um grupo desloca todos os seguintes, e o caso passa a apontar para o mapa
    errado sem ninguém notar. Por isso a tabela sai do `--src`, que é o
    `include/` guardado ao lado da ROM.
    """
    caminho = os.path.join(src or RAIZ, "include", "constants", "map_groups.h")
    por_nome, por_id = {}, {}
    padrao = re.compile(r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)")
    for nome, num, grupo in padrao.findall(open(caminho).read()):
        chave = (int(grupo), int(num))
        por_nome[nome] = chave
        por_id.setdefault(chave, nome)
    return por_nome, por_id


_FLAGS_CACHE = {}


def carrega_flags(src=None):
    """Nome de flag -> número, resolvido pelo PRÉ-PROCESSADOR, não por regex.

    A primeira versão lia só `#define FLAG_X 0x123` cru, e isso resolvia 1301
    dos 2377 defines: ficavam de fora `(TEMP_FLAGS_START + 0x1)`, os apelidos
    (`FLAG_A FLAG_UNUSED_0x0AB`) e qualquer linha com comentário no fim. O
    agente de Johto teve que escrever hexadecimal cru nos casos por causa disso.
    Regex não avalia expressão de C; o `cpp` avalia. Aqui ele faz o trabalho.
    """
    src = src or RAIZ
    if src in _FLAGS_CACHE:
        return _FLAGS_CACHE[src]
    caminho = os.path.join(src, "include", "constants", "flags.h")
    # `A-Za-z` e não `A-Z`: o pool inteiro se chama `FLAG_UNUSED_0xNNNN`, com
    # `x` minúsculo, e a classe só-maiúscula parava o casamento em
    # `FLAG_UNUSED_0`. Resultado medido em 19/08/2026: nenhum dos 1375 rótulos
    # do pool era nomeável num caso, e quem quisesse usá-los como par negativo
    # tinha que escrever o hexadecimal cru e perder o nome. Um caractere.
    nomes = sorted(set(re.findall(r"^#define\s+(FLAG_[A-Za-z0-9_]+)\b",
                                  open(caminho).read(), re.M)))
    tmp = "/tmp/claude-501/frenteA/offsets"
    os.makedirs(tmp, exist_ok=True)
    fonte = os.path.join(tmp, "flags.c")
    with open(fonte, "w") as f:
        f.write('#include "constants/flags.h"\n')
        for n in nomes:
            # o nome vai como STRING: dentro de @@X@@ o cpp expandia o próprio
            # nome e o rótulo sumia. String literal não é macro-expandida.
            f.write(f'"{n}" {n}\n')
    r = subprocess.run(["cc", "-E", "-P", "-iquote", "include", "-DMODERN=1",
                        "-DTESTING=0", "-DEMERALD", fonte],
                       cwd=src, capture_output=True, text=True)
    tabela = {}
    for linha in r.stdout.splitlines():
        m = re.match(r'^"(FLAG_[A-Za-z0-9_]+)"\s+(.+?)\s*$', linha)
        if not m:
            continue
        expr = m.group(2)
        # depois do cpp sobra só aritmética; recusa qualquer coisa que não seja
        # número e operador, para não virar eval de código arbitrário
        # O `%` entrou em 06/08/2026: DAILY_FLAGS_START é
        # `(FLAG_UNUSED_0x91F + (8 - FLAG_UNUSED_0x91F % 8))`, e sem o `%` na
        # lista TODAS as 64 flags da faixa diária (0x920..0x95F) caíam fora da
        # tabela e o caso de teste tinha que chumbar o hexadecimal. Continua
        # sendo só aritmética: nada de nome, chamada ou atributo chega ao eval.
        if not re.fullmatch(r"[0-9a-fA-FxX()+\-*/%<>|&~^ ]+", expr):
            continue
        try:
            tabela[m.group(1)] = int(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307
        except Exception:                                                   # noqa: BLE001
            continue
    # O cpp resolve as expressões, o regex resolve os `#define FLAG_X 0x123`
    # crus. Nenhum dos dois pega tudo: ~270 flags saem do cpp ainda com
    # identificador dentro (dependem de enum, que o pré-processador não conhece).
    # Por isso os dois SOMAM, com o cpp por cima, em vez de um substituir o
    # outro. A primeira versão substituía, e um limiar de 90% jogava fora as 1678
    # que o cpp acertava para ficar com as 1332 do regex.
    padrao = re.compile(r"^#define\s+(FLAG_[A-Z0-9_]+)\s+(0[xX][0-9A-Fa-f]+|\d+)", re.M)
    final = {n: int(v, 0) for n, v in padrao.findall(open(caminho).read())}
    final.update(tabela)
    if r.returncode != 0:
        print(f"AVISO: cpp falhou em {caminho}, só o regex valeu. "
              f"stderr: {r.stderr[-200:]}")
    _FLAGS_CACHE[src] = final
    return final


def carrega_treinadores(src=None):
    """Nome de treinador -> id, das DUAS tabelas, com a de Kanto por último.

    Serve para a prova `oponente`, que é o que separa "abriu batalha no ginásio
    de Pewter" de "lutou contra o Brock".
    """
    base = src or RAIZ
    tabela = {}
    for arq in ("opponents_frlg.h", "opponents.h"):
        caminho = os.path.join(base, "include", "constants", arq)
        if os.path.exists(caminho):
            # O `(?://.*)?` existe porque 12 constantes têm comentário no fim da
            # linha (os quatro duelos do Silver e os oito líderes de Unova). Sem
            # ele a tabela não os enxergava e o caso reprovava dizendo
            # "treinador da prova não existe", que é falso: mentira de validador
            # é pior que validador nenhum (lição 4.3 do ESTADO).
            tabela.update(dict(re.findall(
                r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*(?://.*)?$",
                open(caminho).read(), re.M)))
    return {k: int(v) for k, v in tabela.items()}


def carrega_layouts(src=None):
    """Idem: a faixa válida de mapLayoutId é a DA ROM.

    Com a tabela do repo (1596 layouts, já com Unova) contra uma ROM de 1305, um
    layout-lixo entre 1306 e 1596 passaria na checagem de "o mapa carregou".
    """
    caminho = os.path.join(src or RAIZ, "include", "constants", "layouts.h")
    padrao = re.compile(r"^#define\s+(LAYOUT_[A-Z0-9_]+)\s+(\d+)\s*$", re.M)
    return {n: int(v) for n, v in padrao.findall(open(caminho).read())}


# Símbolos que uma ROM ANTIGA pode não ter (o T11 roda contra o .map dela).
# Faltar um deles não é erro: o caso que precisa dele é que reprova, dizendo o
# nome, em vez de a suíte inteira morrer na carga.
SIMBOLOS_OPCIONAIS = ("gSaveBlock2Ptr", "gBattleMons", "gBattleStruct")


def carrega_simbolos(mapfile):
    alvos = {"gSaveBlock1Ptr": None, "gPartiesCount": None,
             "gTrainerBattleParameter": None, "gParties": None}
    alvos.update({k: None for k in SIMBOLOS_OPCIONAIS})
    padrao = re.compile(r"^\s+(0x[0-9a-f]+)\s+(\w+)\s*$")
    with open(mapfile) as f:
        for linha in f:
            m = padrao.match(linha)
            if m and m.group(2) in alvos and alvos[m.group(2)] is None:
                alvos[m.group(2)] = m.group(1)
    faltando = [k for k, v in alvos.items()
                if v is None and k not in SIMBOLOS_OPCIONAIS]
    if faltando:
        raise SystemExit(f"símbolo não achado em {mapfile}: {faltando}")
    return {k: v for k, v in alvos.items() if v is not None}


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
                # Bytes de gParties até gParties[B_TRAINER_OPPONENT_A][0].level.
                # Medido e não chutado porque sizeof(struct Pokemon) muda com a
                # versão do expansion, e offset chumbado não é testemunha.
                "  sizeof(struct Pokemon) * PARTY_SIZE * B_TRAINER_OPPONENT_A\n"
                "    + offsetof(struct Pokemon, level),\n"
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
    if len(palavras) < 8:
        raise SystemExit(f"leitura de offsets falhou em {src}: {d[:300]}")
    return palavras[:8]


_BATALHA_CACHE = {}


def offsets_de_batalha(src):
    """Offsets de BATALHA e das opções do modo de teste, medidos compilando.

    Separado de `offsets_da_fonte` de propósito: aquele é chamado também sobre a
    ÁRVORE ANTIGA no T11, e não se mexe no contrato dele. Este só é chamado
    quando um caso pede prova de batalha.

    O achado que justifica a última entrada: `opponentMonCanTera:6` e
    `opponentMonCanDynamax:6` (include/battle.h) são CAMPOS DE BITS, e
    `offsetof` não fala de bit. Então o probe compila uma `struct BattleStruct`
    constante com `.opponentMonCanDynamax = 0x3F` e o Python procura o primeiro
    byte não zero do dump: o u16 que contém os dois campos está ali. Ler o u16
    inteiro é de propósito, porque a prova é comparar o MESMO valor com a opção
    LV.5 ligada e desligada, e isso não depende de saber em que bit cada gimmick
    mora.
    """
    if src in _BATALHA_CACHE:
        return _BATALHA_CACHE[src]
    devkit = os.environ.get("DEVKITARM",
                            os.path.expanduser("~/toolchains/arm-gnu-toolchain-15.2."
                                               "rel1-darwin-arm64-arm-none-eabi"))
    gcc = os.path.join(devkit, "bin", "arm-none-eabi-gcc")
    objdump = os.path.join(devkit, "bin", "arm-none-eabi-objdump")
    if not os.path.exists(gcc):
        raise SystemExit(f"arm-none-eabi-gcc não encontrado em {gcc}. Exporte DEVKITARM.")
    tmp = "/tmp/claude-501/frenteA/offsets"
    os.makedirs(tmp, exist_ok=True)

    def compila(nome, corpo):
        c, o = os.path.join(tmp, nome + ".c"), os.path.join(tmp, nome + ".o")
        with open(c, "w") as f:
            f.write('#include "global.h"\n#include "battle.h"\n' + corpo)
        r = subprocess.run([gcc, "-c", "-iquote", "include", "-Wno-trigraphs",
                            "-DMODERN=1", "-DTESTING=0", "-DEMERALD", "-std=gnu17",
                            "-mthumb", "-mabi=apcs-gnu", "-march=armv4t", "-O0",
                            "-o", o, c], cwd=src, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"probe de batalha não compilou em {src}:\n{r.stderr[-800:]}")
        d = subprocess.run([objdump, "-s", "-j", ".rodata", o],
                           capture_output=True, text=True).stdout
        crus = bytearray()
        for linha in d.splitlines():
            m = re.match(r"^ [0-9a-f]{4} ((?:[0-9a-f]{2,8} ?){1,4})", linha)
            if m:
                crus.extend(bytes.fromhex(m.group(1).replace(" ", "")))
        return crus

    b = compila("batalha", "const unsigned gP[] = {\n"
                "  offsetof(struct SaveBlock2, filler_90),\n"
                "  sizeof(struct Pokemon),\n"
                "  sizeof(struct BattlePokemon),\n"
                "  offsetof(struct BattlePokemon, species),\n"
                "  offsetof(struct BattlePokemon, level),\n"
                "  offsetof(struct BattlePokemon, moves),\n"
                # Os cinco de baixo servem ao `--timeinimigo` do runner, que
                # DECIFRA o time do adversario em gParties. Sem eles a prova de
                # time parava no batalhador ativo, e o ACE, que e quem carrega a
                # pedra Mega, e o ULTIMO slot e nunca o ativo.
                "  offsetof(struct Pokemon, box.personality),\n"
                "  offsetof(struct Pokemon, box.otId),\n"
                "  offsetof(struct Pokemon, box.secure),\n"
                "  sizeof(union PokemonSubstruct),\n"
                "  offsetof(struct Pokemon, level),\n"
                "};\n")
    v = [int.from_bytes(b[i:i + 4], "little") for i in range(0, 44, 4)]
    g = compila("gimmick", "const struct BattleStruct gB = "
                "{ .opponentMonCanDynamax = 0x3F };\n")
    nz = [i for i, x in enumerate(g) if x]
    if not nz:
        raise SystemExit("probe de gimmick saiu todo zero: o campo de bits sumiu "
                         "de struct BattleStruct?")
    fora = {"opcoes_offset": v[0], "tam_pokemon": v[1], "tam_bmon": v[2],
            "bmon_especie": v[3], "bmon_nivel": v[4], "bmon_golpes": v[5],
            "mon_pers": v[6], "mon_otid": v[7], "mon_secure": v[8],
            "tam_substruct": v[9], "mon_nivel": v[10],
            "gimmick_offset": nz[0] & ~1}
    _BATALHA_CACHE[src] = fora
    return fora


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


# O campo do WARP era diferente dos outros dois, e isso custou um teste em
# 06/08/2026: `DebugAction_Util_Warp_SelectWarp` não tratava DPAD_LEFT nem
# DPAD_RIGHT (o dígito ficava sempre na unidade) e clampava o valor em 10, então
# pedir o warp 10 entrava o warp 1 e a casa leste de Sunyshore reprovava com o
# mapa e a porta corretos.
#
# CONSERTADO EM 18/08/2026 (G5 de Galar), no motor e não no roteiro: aquele laço
# à mão virou o mesmo `Debug_HandleInput_Numeric(taskId, 0, 127, 3)` que os
# campos de grupo e de mapa logo acima já usavam. O teto 127 é o do motor (`s8
# warpId` em `struct WarpData`), não um número escolhido. Com isso o campo passa
# a ser de três dígitos como os outros e `digita_warp` é `digita_numero`; caso
# de suíte não precisa mais evitar warp_id acima de 10. Roteiro antigo continua
# valendo: para warp de 0 a 9 as duas formas digitam o mesmo valor.
def digita_warp(valor):
    return digita_numero(valor)


def rota_warp(grupo, num, warp=0):
    return ",".join([
        "40:R+START!", "60:NADA",
        "20:A", "40:NADA",
        "20:DOWN", "20:A", "60:NADA",
        digita_numero(grupo), "20:A", "40:NADA",
        digita_numero(num), "20:A", "40:NADA",
        digita_warp(warp), "20:A", "300:NADA",
    ])


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------
LINHA_ESTADO = re.compile(r"^ESTADO (\S+) (.*)$")


def roda(rom, simbolos, roteiro, prefixo, flags_lidas=(), vars_lidas=(), sav=None,
         offsets=None, palobj_lidas=(), batalha=None):
    os.makedirs(SAIDA, exist_ok=True)
    for f in glob.glob(f"{SAIDA}/{prefixo}-*.png"):
        os.remove(f)
    cmd = [RUNNER, rom, "900", roteiro, f"{SAIDA}/{prefixo}.png", "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"],
           "--oponente", simbolos["gTrainerBattleParameter"]]
    if offsets:
        cmd += ["--offsets", ",".join(str(v) for v in offsets[:7])]
        if len(offsets) > 7:
            cmd += ["--inimigo", simbolos["gParties"],
                    "--nivel-offset", str(offsets[7])]
    if batalha:
        cmd += ["--nivel-passo", str(batalha["tam_pokemon"])]
        if "--inimigo" in cmd:
            cmd += ["--timeinimigo", ",".join(str(batalha[k]) for k in (
                "mon_pers", "mon_otid", "mon_secure", "tam_substruct",
                "mon_nivel"))]
        if "gSaveBlock2Ptr" in simbolos:
            cmd += ["--opcoes", f"{simbolos['gSaveBlock2Ptr']},{batalha['opcoes_offset']}"]
        if "gBattleMons" in simbolos:
            cmd += ["--batalhamons", ",".join(str(x) for x in (
                simbolos["gBattleMons"], batalha["tam_bmon"], batalha["bmon_especie"],
                batalha["bmon_nivel"], batalha["bmon_golpes"]))]
        if "gBattleStruct" in simbolos:
            cmd += ["--gimmick", f"{simbolos['gBattleStruct']},{batalha['gimmick_offset']}"]
    for f in flags_lidas:
        cmd += ["--flag", hex(f)]
    for v in vars_lidas:
        cmd += ["--var", hex(v)]
    for c in palobj_lidas:
        cmd += ["--palobj", hex(c)]
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
    modo = caso.get("abertura", ABERTURA_PADRAO)
    if modo not in ABERTURAS:
        raise KeyError(f"abertura desconhecida: {modo}. Use {list(ABERTURAS)}")
    partes = [ABERTURAS[modo]] if ABERTURAS[modo] else []
    for f in caso.get("flags", []):
        partes.append(f"6:FLAG={num_flag(f, tabela_flags)}")
    for var, val in caso.get("vars", {}).items():
        partes.append(f"6:VAR={int(var, 0)}={val}")
    # `opcoes`: o byte do modo de teste (SaveBlock2.filler_90[0]) escrito direto
    # na EWRAM. Existe desde 19/08/2026, quando LV.5 TRAINERS passou a NASCER
    # LIGADA no jogo novo por pedido do Gui: quem mede a curva NATURAL de nível
    # (T95.2, T97.5, T97.6, T107.4) tem que dizer que quer a opção desligada, e
    # dizer isso pelo menu OPTION custaria ~700 quadros de navegação por caso.
    # 32 é o mundo em repouso menos o LV.5 (só TURBO A/B), 36 é com ele.
    if "opcoes" in caso:
        partes.append(f"6:OPT={caso['opcoes']}")
    # Apertos ANTES do warp de debug. Existe por um caso só, e ele é real: para
    # provar cena que precisa de PARTY (surfar, por exemplo), o roteiro tem que
    # passar pelo seletor de capítulo primeiro, que é quem dá o Pikachu com SURF
    # ao jogador de party vazia (src/chapter_jump.c). O seletor abre ANTES de o
    # jogador ter controle, então esses apertos não cabem no `roteiro`, que roda
    # depois do warp.
    if caso.get("antes_do_warp"):
        partes.append(caso["antes_do_warp"])
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


def confere(caso, estados, por_nome, por_id, tabela_flags, layouts, treinadores=None):
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

    # "andou": prova que o jogo continua RESPONDENDO, não só que carregou.
    # ponytail: "não travou" é critério proibido aqui. Um mapa cheio de NPC novo
    # pode carregar e depois congelar (sprite sem gráfico anda e reinicia), e a
    # tela preta do reset também "não trava". Se a posição do jogador mudou entre
    # o primeiro e o último ESTADO, alguém andou, e para andar o jogo tem que
    # estar rodando o loop de campo com os objetos do mapa vivos.
    # "pos": onde o jogador PAROU, lido de gSaveBlock1Ptr->pos. Serve para a
    # família de prova em que o que importa é se um tile estava OCUPADO ou não:
    # item ball, pedra, NPC de bloqueio. Objeto sólido para o passo, e a posição
    # final diz se ele estava lá sem precisar de nenhum efeito colateral. Foi o
    # que faltou ao J2 (a prova de que a bola pega NÃO renasce ao recarregar o
    # mapa): com a bola de volta o jogador para um tile antes.
    if "pos" in prova:
        alvo = tuple(prova["pos"])
        obtido = (final.get("x"), final.get("y"))
        if obtido != alvo:
            falhas.append(f"posição final errada: esperado {alvo}, obtido {obtido}")

    if prova.get("andou"):
        # Só valem os estados JÁ dentro do mapa final: o próprio warp muda a
        # posição, e contar com ele faria a prova passar com o jogo congelado.
        aqui = [(e.get("x"), e.get("y")) for e in estados
                if (e.get("grupo"), e.get("num")) == atual]
        if len(set(aqui)) < 2:
            falhas.append(f"jogador NÃO andou: posição ficou em {aqui[-1:] or '?'} "
                          f"nos {len(aqui)} estados lidos dentro de {nome_atual}. "
                          "O mapa carregou mas o jogo não respondeu ao controle.")

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

    if "oponente" in prova:
        alvo = prova["oponente"]
        esperado = alvo if isinstance(alvo, int) else (treinadores or {}).get(alvo)
        if esperado is None:
            falhas.append(f"treinador da prova não existe: {alvo}")
        elif final.get("oponente") != esperado:
            inverso = {v: k for k, v in (treinadores or {}).items()}
            falhas.append(f"a batalha começou contra o treinador errado: esperado "
                          f"{alvo}={esperado}, obtido {final.get('oponente')} "
                          f"({inverso.get(final.get('oponente'), 'sem nome')})")

    if "oponente_faixa" in prova:
        # Prova do conserto dos apelidos de Kanto. Só o id NÃO serve: o script
        # usa TRAINER_CAMPER_LIAM e o apelido devolve exatamente o id do apelido,
        # então "id bate" é verdade mesmo com o treinador errado na tela. O que
        # muda quando o conserto entra é a FAIXA: os treinadores de Kanto com
        # time próprio moram em 1400 a 1799. Medido em 05/08/2026, antes do
        # conserto, o Liam do ginásio de Pewter abria batalha como o id 52, que
        # é TRAINER_GABBY_AND_TY_2, uma dupla de repórteres de Hoenn.
        lo, hi = prova["oponente_faixa"]
        obtido = final.get("oponente")
        if not (lo <= (obtido or 0) <= hi):
            inverso = {v: k for k, v in (treinadores or {}).items()}
            falhas.append(f"a batalha começou contra o id {obtido} "
                          f"({inverso.get(obtido, 'sem nome')}), fora da faixa "
                          f"{lo}..{hi} de quem deveria estar naquela batalha")

    if "nivel_inimigo_faixa" in prova:
        # Prova do bloco B8, lado do mato. "Abriu batalha selvagem" nao diz nada
        # sobre a curva: antes do remapeamento o jogador chegava em Sinnoh com
        # time de nivel 145 e a grama cuspia nivel 30, e um teste de "apareceu
        # um Pokemon" passava igual. O que muda e a FAIXA, e ela vem lida de
        # gParties[B_TRAINER_OPPONENT_A][0].level, que num encontro selvagem e o
        # bicho que apareceu.
        lo, hi = prova["nivel_inimigo_faixa"]
        obtido = final.get("nivelinimigo")
        if obtido is None:
            falhas.append("o runner nao reportou nivelinimigo: recompile o "
                          "dev_scripts/gba_runner.c (precisa de --inimigo)")
        elif not (lo <= obtido <= hi):
            falhas.append(f"o Pokemon selvagem veio no nivel {obtido}, fora da "
                          f"faixa {lo}..{hi} remapeada para aquela regiao")

    for var, val in prova.get("vars", {}).items():
        chave = f"var_{hex(int(var, 0)).upper().replace('0X', '0x')}"
        if final.get(chave) != val:
            falhas.append(f"var {var} vale {final.get(chave)}, esperado {val}")

    # Prova do caso dos NPCs verdes de Kanto (12/08/2026): as palettes FRLG
    # (NPC_WHITE, NPC_GREEN etc.) existiam na ROM mas nunca eram registradas,
    # porque a tabela sObjectEventSpritePalettes ficou presa num #if IS_FRLG
    # quando os graficos foram destravados. O sprite desenhava com a palette
    # de outro dono e nenhum teste via, porque a suite so lia EWRAM. A cor de
    # 15 bits vem lida da PLTT OBJ pelo runner, entao continua sendo fato de
    # memoria, nao pixel.
    for cor in prova.get("palobj_presentes", []):
        chave = f"palobj_0x{int(cor, 0):04X}"
        if final.get(chave) != 1:
            falhas.append(f"cor {cor} ausente das palettes OBJ carregadas: a "
                          f"palette do sprite nao foi registrada (runner velho? "
                          f"recompile dev_scripts/gba_runner.c)")

    # `campos`: qualquer chave que o runner reporte, com valor exato ou faixa
    # [lo, hi]. Existe para não crescer uma chave de prova por leitura nova: o
    # modo de teste em nível 5 precisa provar de uma vez o byte das opções
    # (`opcoes`), os SEIS níveis do time (`nivelinimigo`, `nivelinimigo1..5`), a
    # espécie e os golpes do adversário ativo (`bespecie`, `bgolpe0..3`) e a
    # palavra de gimmick (`gimmick`). Chave ausente é FALHA dita pelo nome, e
    # não silêncio, que é o modo como uma prova morre sem ninguém ver.
    for chave, esperado in prova.get("campos", {}).items():
        obtido = final.get(chave)
        if obtido is None:
            falhas.append(f"o runner nao reportou `{chave}`: runner velho "
                          f"(recompile dev_scripts/gba_runner.c) ou simbolo "
                          f"ausente do pokeemerald.map")
        elif isinstance(esperado, list):
            if not (esperado[0] <= obtido <= esperado[1]):
                falhas.append(f"{chave}={obtido}, fora da faixa "
                              f"{esperado[0]}..{esperado[1]}")
        elif obtido != esperado:
            falhas.append(f"{chave}={obtido}, esperado {esperado}")

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
    # Varre TODO .inc de data/, não só data/maps/*/scripts.inc. O buraco: os
    # scripts de treinador de Kanto moram em data/scripts/trainers_frlg.inc, que
    # entra na ROM por data/event_scripts.s e não é script de mapa nenhum. Com a
    # varredura antiga, 221 apelidos usados por esse arquivo davam VERDE aqui.
    for arq in glob.glob(os.path.join(RAIZ, "data/**/*.inc"), recursive=True):
        texto = open(arq, errors="ignore").read()
        for nome in re.findall(r"\bTRAINER_[A-Z0-9_]+\b", texto):
            if nome in apelidos:
                usados.add((os.path.relpath(arq, RAIZ), nome))

    print(f"constantes de treinador em opponents_frlg.h: {len(frlg)}")
    print(f"  sem time próprio em trainers.party (apelidam outro treinador): {len(apelidos)}")
    print(f"  desses, usados por script: {len({n for _, n in usados})} "
          f"em {len({m for m, _ in usados})} arquivos")
    for mapa, nome in sorted(usados)[:10]:
        print(f"    {mapa:38} {nome:34} -> id {apelidos[nome]} = "
              f"{por_id.get(apelidos[nome], '?')}")
    if len(usados) > 10:
        print(f"    ... e mais {len(usados) - 10}")

    colisoes = [n for n in frlg if n in principal and frlg[n] != principal[n]]
    for n in colisoes:
        print(f"[FALHA] {n} vale {frlg[n]} em opponents_frlg.h e {principal[n]} em "
              "opponents.h. Um dos dois scripts luta com o treinador errado.")

    # Reprova por apelido USADO, não por apelido existir. Sobram 370 nomes de
    # Kanto que nenhum script referencia, e eles são inertes: não há mapa que
    # possa entregar o treinador errado. A primeira versão reprovava por eles, e
    # o portão nunca podia ficar verde, o que treina todo mundo a ignorar a
    # saída. Foi assim que dois crashes sobreviveram a seis agentes nesta sessão.
    if not usados and not colisoes:
        print(f"nenhum apelido usado por script, e nenhuma colisão "
              f"({len(apelidos)} apelidos inertes, sem mapa que os cite)")
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
    if "--abertura" in args:
        global ABERTURA_PADRAO
        i = args.index("--abertura")
        ABERTURA_PADRAO = args[i + 1]
        if ABERTURA_PADRAO not in ABERTURAS:
            raise SystemExit(f"--abertura desconhecida: {ABERTURA_PADRAO}. "
                             f"Use uma de {list(ABERTURAS)}")
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

    por_nome, por_id = carrega_mapas(src)
    tabela_flags = carrega_flags(src)
    layouts = carrega_layouts(src)
    treinadores = carrega_treinadores(src)
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
        palobj_lidas = [int(c, 0) for c in prova.get("palobj_presentes", [])]
        try:
            roteiro = monta_roteiro(caso, por_nome, tabela_flags)
            estados = roda(rom_do_caso, simbolos_do_caso, roteiro,
                           caso["id"].replace(".", "_"),
                           flags_lidas, vars_lidas, caso.get("sav"),
                           offsets_do_caso, palobj_lidas,
                           batalha=offsets_de_batalha(
                               src2 if (caso.get("rom") == "rom2" and src2) else src)
                           if (prova.get("campos") or "opcoes" in caso) else None)
            falhas = confere(caso, estados, por_nome, por_id, tabela_flags, layouts,
                             treinadores)
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
