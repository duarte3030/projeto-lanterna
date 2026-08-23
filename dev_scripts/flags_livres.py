#!/usr/bin/env python3
"""Diz quais flags estao REALMENTE livres, e reserva faixa para um agente.

Uso:
    python3 dev_scripts/flags_livres.py               # lista as faixas livres
    python3 dev_scripts/flags_livres.py --reserva 16  # sugere uma faixa de 16

Existe porque eu distribui cinco faixas de flag para cinco agentes em
05/08/2026 e **as cinco estavam ocupadas**. Olhei `grep -c FLAG_UNUSED`, vi 460,
e cravei 0x020-0x02F, 0x030-0x03F e por aí. Um agente foi usar e descobriu que
0x030-0x037 eram as insignias de Johto, 0x038-0x03C a Galactica e 0x03D-0x03F os
Rockets: a faixa inteira em uso.

O erro e simples e nao aparece no grep. Em flags.h uma flag ocupada continua
existindo como `FLAG_UNUSED_0x030`; o que muda e que ALGUEM apelida ela:

    #define FLAG_BADGE_JOHTO_ZEPHYR   FLAG_UNUSED_0x030

Contar `FLAG_UNUSED` conta o pool inteiro, ocupadas junto. O que vale e contar
quantas NAO tem apelido apontando para elas.

Mesma familia de erro do resto da sessao: medir uma camada mais rasa que a da
afirmacao. "A flag existe como UNUSED" nao e "a flag esta livre".
"""
import re
import subprocess
import sys
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS_H = f"{RAIZ}/include/constants/flags.h"

# Faixa que o motor limpa sozinho todo dia. Lida do proprio flags.h por
# `faixa_diaria()` no import; o par abaixo e so o valor de fabrica do
# pokeemerald, usado se a leitura falhar.
DIARIA = (0x920, 0x95F)


def faixa_diaria():
    """Le do flags.h quais FLAG_UNUSED sao definidas como DAILY_FLAGS_START + n.

    Ler em vez de cravar porque a faixa muda se alguem mexer no pool: cravar o
    par seria a mesma classe de erro que este arquivo inteiro existe para evitar.
    """
    s = open(FLAGS_H).read()
    ns = [int(n, 16) for n in re.findall(
        r"^#define\s+FLAG_UNUSED_0x([0-9A-Fa-f]+)\s+\(DAILY_FLAGS_START", s, re.M)]
    return (min(ns), max(ns)) if ns else DIARIA


def usadas_cruas():
    """FLAG_UNUSED_0xNNN citada DIRETO em data/ ou src/, sem apelido nenhum.

    TERCEIRA CAMADA DE ARMADILHA, achada em 16/08/2026. Nem toda flag ocupada
    ganha apelido em flags.h: quem importou Johto escreveu o nome cru no campo
    `flag` das item balls (data/maps/SproutTower_1F/map.json:93 e companhia,
    0x264 a 0x26F). Esse uso nao aparece em nenhum `#define`, entao as duas
    camadas anteriores davam a faixa como livre, e ela ja estava valendo por
    baixo: as MESMAS doze flags tambem eram apelido de FLAG_HIDE_* de Kanto
    (Fame Checker, bonecos da casa da Lorelei, Lift Key). Acender a de Kanto
    apagava a Pokebola de Johto, e vice-versa.
    """
    r = subprocess.run(
        ["git", "grep", "-hoE", r"FLAG_UNUSED_0x[0-9A-Fa-f]+", "--",
         "data", "src"], cwd=RAIZ, capture_output=True, text=True)
    return {int(n.split("0x")[1], 16) for n in r.stdout.split("\n") if n}


def livres():
    """Devolve (lista de numeros livres, total definido, total apelidado)."""
    global DIARIA
    DIARIA = faixa_diaria()
    s = open(FLAGS_H).read()
    apelidada = set(re.findall(
        r"^#define\s+FLAG_(?!UNUSED)[A-Z0-9_]+\s+(FLAG_UNUSED_0x[0-9A-Fa-f]+)\b",
        s, re.M))
    todas = set(re.findall(r"^#define\s+(FLAG_UNUSED_0x[0-9A-Fa-f]+)\b", s, re.M))
    nums = sorted(int(n.split("0x")[1], 16) for n in todas - apelidada)
    # SEGUNDA CAMADA DE ARMADILHA, achada em 06/08/2026: existir sem apelido
    # ainda nao e servir. De FLAG_UNUSED_0x920 a 0x95F o proprio flags.h define
    # cada uma como (DAILY_FLAGS_START + n), e `ClearDailyFlags()`
    # (src/event_data.c) da memset na faixa inteira a cada virada de dia do RTC.
    # Flag de estado ali some sozinha durante a noite, sem erro, sem log, e o
    # jogador acorda com a porta destrancada. Eu ja tinha despachado
    # 0x946-0x95F para um agente antes de descobrir; ninguem chegou a gastar.
    nums = [n for n in nums if not (DIARIA[0] <= n <= DIARIA[1])]
    cruas = usadas_cruas()
    nums = [n for n in nums if n not in cruas]
    return nums, len(todas), len(apelidada)


def faixas(nums):
    """Agrupa numeros consecutivos em (inicio, fim)."""
    out = []
    ini = ant = None
    for v in nums:
        if ini is None:
            ini = ant = v
        elif v == ant + 1:
            ant = v
        else:
            out.append((ini, ant))
            ini = ant = v
    if ini is not None:
        out.append((ini, ant))
    return out


def dobradas():
    """FLAG_UNUSED que tem apelido em flags.h E tambem e citada crua em data/src.

    Duas frentes escrevendo na mesma flag por nomes diferentes. Nem sempre e
    erro (o elenco da Liga de Unova de proposito compartilha uma flag entre
    cinco objetos, e ali o nome cru e o apelido sao a mesma coisa), por isso
    aqui e aviso, nao excecao. Erro e quando as duas pontas sao de REGIOES
    diferentes: foi assim que 0x264-0x26F ficaram sendo, ao mesmo tempo,
    FLAG_HIDE_* de Kanto e a Pokebola de item de Johto.
    """
    s = open(FLAGS_H).read()
    apelido = {a: n for n, a in re.findall(
        r"^#define\s+(FLAG_(?!UNUSED)[A-Za-z0-9_]+)\s+(FLAG_UNUSED_0x[0-9A-Fa-f]+)\b",
        s, re.M)}
    cruas = usadas_cruas()  # UMA vez: dentro do `if` seriam 800 git grep
    return sorted((int(a.split("0x")[1], 16), n)
                  for a, n in apelido.items()
                  if int(a.split("0x")[1], 16) in cruas)


def main():
    nums, total, ocupadas = livres()
    fs = faixas(nums)
    print(f"FLAG_UNUSED definidas: {total}")
    print(f"  ja apelidadas por outra flag (OCUPADAS): {ocupadas}")
    print(f"  realmente livres: {len(nums)}")

    for n, nome in dobradas():
        print(f"  AVISO: 0x{n:03X} tem apelido ({nome}) E uso cru em data/src")

    if "--reserva" in sys.argv:
        n = int(sys.argv[sys.argv.index("--reserva") + 1])
        cabe = [f for f in fs if f[1] - f[0] + 1 >= n]
        if not cabe:
            print(f"\nNAO HA faixa contigua de {n} flags livres.")
            return 1
        # a menor que serve, para nao picotar a maior a toa
        a, b = min(cabe, key=lambda f: f[1] - f[0])
        print(f"\nreserve 0x{a:03X} a 0x{a+n-1:03X} ({n} flags), "
              f"de uma faixa de {b-a+1}")
        return 0

    print("\nfaixas contiguas livres, da maior para a menor:")
    for a, b in sorted(fs, key=lambda f: -(f[1] - f[0]))[:10]:
        print(f"  0x{a:03X} a 0x{b:03X}   {b-a+1:3d} flags")
    return 0


def demo():
    """A regra que importa: apelidada nao e livre."""
    import tempfile
    txt = (
        "#define FLAG_UNUSED_0x030   (0x030)\n"
        "#define FLAG_UNUSED_0x031   (0x031)\n"
        "#define FLAG_UNUSED_0x032   (0x032)\n"
        "#define FLAG_BADGE_JOHTO_ZEPHYR   FLAG_UNUSED_0x030\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write(txt)
        caminho = f.name
    global FLAGS_H
    guardado, FLAGS_H = FLAGS_H, caminho
    try:
        nums, total, ocup = livres()
        assert total == 3, total
        assert ocup == 1, ocup
        # 0x030 esta apelidada por FLAG_BADGE_JOHTO_ZEPHYR, entao NAO e livre
        assert nums == [0x31, 0x32], [hex(x) for x in nums]
        assert faixas(nums) == [(0x31, 0x32)]
    finally:
        FLAGS_H = guardado
        os.unlink(caminho)

    # Segunda regra: flag da faixa que o motor limpa todo dia NAO e livre,
    # mesmo sem apelido nenhum.
    txt = (
        "#define FLAG_UNUSED_0x91F   (0x91F)\n"
        "#define FLAG_UNUSED_0x920   (DAILY_FLAGS_START + 0x0)\n"
        "#define FLAG_UNUSED_0x921   (DAILY_FLAGS_START + 0x1)\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write(txt)
        caminho = f.name
    guardado, FLAGS_H = FLAGS_H, caminho
    try:
        assert faixa_diaria() == (0x920, 0x921)
        nums, _, _ = livres()
        assert nums == [0x91F], [hex(x) for x in nums]
    finally:
        FLAGS_H = guardado
        os.unlink(caminho)

    # Terceira regra: sem apelido nenhum, mas citada crua num map.json, tambem
    # NAO e livre. Sem isso a faixa 0x264-0x26F sai de novo para o proximo
    # agente, por cima das item balls de Johto.
    txt = ("#define FLAG_UNUSED_0x264   (0x264)\n"
           "#define FLAG_UNUSED_0x300   (0x300)\n")
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write(txt)
        caminho = f.name
    guardado, FLAGS_H = FLAGS_H, caminho
    global usadas_cruas
    real_cruas, usadas_cruas = usadas_cruas, lambda: {0x264}
    try:
        nums, _, _ = livres()
        assert nums == [0x300], [hex(x) for x in nums]
    finally:
        FLAGS_H, usadas_cruas = guardado, real_cruas
        os.unlink(caminho)

    # E a regra tem que valer no repo de verdade: nada que este arquivo chame de
    # livre pode estar citado cru em data/ ou src/.
    assert not (set(livres()[0]) & real_cruas()), "faixa livre colide com uso cru"
    print("demo ok")


# ---------------------------------------------------- alocacao APPEND-ONLY --
# Nasceu de defeito MEDIDO em 23/08/2026: entre a ROM `22f` e a de hoje, 16
# enderecos de flag e de var de Galar trocaram de DONO. Nenhum guarda viu,
# porque `guarda_save.py` mede TAMANHO e INDICE e nao ATRIBUICAO, e a save
# guarda BIT, nao nome: quem tivesse a save antiga carregaria na ROM nova com o
# estado de Galar trocado de lugar, calado.
#
# A causa era sempre a mesma linha, repetida em quatro geradores:
#
#     alocadas = {n: livres[i] for i, n in enumerate(sorted(nomes))}
#
# Um nome novo no meio de `sorted(nomes)` empurra todos os seguintes um
# endereco para baixo. E a MESMA familia do id de treinador que a 0.r
# consertou lendo o de-para do proprio `opponents.h`; aqui o de-para mora no
# `flags.h`/`vars.h`, e e ele a fonte da verdade.


def apelidos_gravados(caminho, prefixo, pool="UNUSED_0x"):
    """{apelido: endereco} JA GRAVADOS no header. O de-para publicado."""
    texto = open(caminho, encoding="utf-8").read()
    return {m.group(1): int(m.group(2), 16) for m in re.finditer(
        r"#define\s+(%s\w*)\s+\(?\s*\w*%s([0-9A-Fa-f]{3,4})\b"
        % (prefixo, pool), texto)}


def aloca_append_only(nomes, livres, gravados):
    """{nome: endereco}. Nome ja gravado NUNCA muda; nome novo entra no FIM.

    `nomes`   nomes que esta rodada quer, em qualquer ordem.
    `livres`  enderecos que ninguem apelida (o bloco do proprio gerador conta
              como livre, porque ele e reescrito inteiro a cada rodada).
    `gravados` o de-para que ja esta no header, de `apelidos_gravados`.

    Nome novo entra depois do MAIOR endereco ja atribuido, e nao no primeiro
    buraco: buraco e endereco que alguma ROM publicada ja usou para outra
    coisa, e reaproveita-lo faz a save velha ler estado alheio.
    """
    fora, tomados = {}, set()
    for n in sorted(nomes):
        e = gravados.get(n)
        if e is not None and e not in tomados:
            fora[n] = e
            tomados.add(e)
    teto = max(tomados, default=-1)
    sobra = [e for e in sorted(livres) if e > teto and e not in tomados]
    for n in sorted(nomes):
        if n in fora:
            continue
        if not sobra:
            raise SystemExit("PARE: acabou endereco livre acima de 0x%04X "
                             "para %s" % (teto, n))
        fora[n] = sobra.pop(0)
    return fora


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
