#!/usr/bin/env python3
"""Prova, NO EMULADOR, qual faixa cada mapa toca de verdade.

Por que existe
--------------
Em 06/09/2026 o Gui trouxe do playtest o defeito "toda cidade de Johto toca
musica de caverna". A causa era de-para: 23 apelidos `MUS_HG_*` de
`include/constants/songs.h` apontavam para `MUS_PETALBURG_WOODS`, que nesta
build tambem era o destino de `MUS_CAVE`, `MUS_ROCK_TUNNEL` e `MUS_SHOAL_CAVE`.
Consertar isso e trocar constante, e "compilou" nao prova nada sobre som: o
`map.json` podia estar certo e o jogo continuar tocando outra coisa.

Esta ferramenta responde a pergunta na camada da afirmacao, e em DUAS camadas:

1. `gMapHeader.music` (u16 em gMapHeader + 0x10). E o header que o motor
   CARREGOU, nao o JSON que o gerador escreveu. Prova que a constante nova
   chegou na ROM e no mapa certo.
2. `gMPlayInfo_BGM.songHeader` (u32 no comeco de gMPlayInfo_BGM). E o ponteiro
   que o DRIVER DE SOM esta tocando naquele quadro. Ele e traduzido de volta
   para o numero da faixa procurando o ponteiro em `gSongTable` dentro do
   binario da ROM (entrada de 8 bytes: `.4byte header, .2byte player,
   .2byte unk`, ver asm/macros/m4a.inc). Sem esta segunda camada, um header
   certo com o driver tocando a musica anterior passaria verde.

Os dois enderecos saem SEMPRE do `pokeemerald.map` ao lado da ROM. Endereco
cravado aqui envelheceria calado no primeiro relink.

Uso
---
    python3 dev_scripts/prova_musica_johto.py
    python3 dev_scripts/prova_musica_johto.py --rom outra.gba --map outra.map
    python3 dev_scripts/prova_musica_johto.py --demo     # so autotesta o parser
"""
import argparse
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import testa_critico as tc  # noqa: E402

SAIDA = "/tmp/claude-501/musica-johto"

# offsetof(struct MapHeader, music), include/global.fieldmap.h:236. Comentario
# do header confere com a ordem dos quatro ponteiros que vem antes.
OFF_MUSIC = 0x10
# offsetof(struct MusicPlayerInfo, songHeader) = 0, include/gba/m4a_internal.h.
OFF_SONG_HEADER = 0
TAM_ENTRADA_SONG = 8  # asm/macros/m4a.inc, macro `song`

# (mapa, faixa esperada, o que este caso cobre). O nome do mapa e resolvido pela
# tabela de map_groups.h, nunca digitado como numero.
CASOS = [
    ("MAP_GOLDENROD_CITY",        "MUS_RG_CELADON",     "cidade grande"),
    ("MAP_NEW_BARK_TOWN",         "MUS_LITTLEROOT",     "cidade inicial"),
    ("MAP_OLIVINE_CITY",          "MUS_RG_VERMILLION",  "cidade que herdava a de Violet"),
    ("MAP_BLACKTHORN_CITY",       "MUS_EVER_GRANDE",    "cidade que herdava a de Azalea"),
    ("MAP_ROUTE29",               "MUS_ROUTE101",       "rota"),
    ("MAP_VIOLET_CITY_GYM",       "MUS_GYM",            "ginasio"),
    ("MAP_CHERRYGROVE_CITY_MART", "MUS_POKE_MART",      "loja"),
    ("MAP_ICE_PATH_1F",           "MUS_RG_MT_MOON",     "caverna, que PODE ser caverna"),
    ("MAP_OLIVINE_CITY_LIGHTHOUSE", "MUS_RG_POKE_TOWER", "farol, que tocava musica de CIDADE"),
    ("MAP_MT_SILVER_2F",          "MUS_RG_POKE_TOWER",  "MT SILVER divide o apelido do farol"),
    ("MAP_PETALBURG_CITY",        "MUS_PETALBURG",      "CONTROLE de Hoenn, nao foi tocado"),
]


def numero_da_faixa(nome, src=None):
    """Nome de constante -> numero, resolvido pelo PRE-PROCESSADOR.

    Regex nao serve: quase toda faixa daqui e APELIDO de outra (`MUS_HG_AZALEA`
    -> `MUS_VERDANTURF` -> 398), e foi exatamente uma cadeia dessas que criou o
    defeito. Quem responde qual numero sai no fim e o compilador.
    """
    inc = os.path.join(src or RAIZ, "include")
    fonte = f'#include "constants/songs.h"\nRESPOSTA {nome}\n'
    saida = subprocess.run(
        ["cc", "-E", "-P", "-I", inc, "-I", os.path.join(inc, "constants"), "-"],
        input=fonte, capture_output=True, text=True)
    if saida.returncode:
        raise SystemExit(f"pre-processador recusou {nome}:\n{saida.stderr}")
    m = re.search(r"RESPOSTA\s+(\S+)", saida.stdout)
    if not m:
        raise SystemExit(f"nao achei a resposta de {nome} em:\n{saida.stdout}")
    return int(m.group(1), 0)


def tabela_de_ponteiros(rom, endereco_tabela, quantas):
    """ponteiro do songHeader -> indice em gSongTable, lido do binario da ROM."""
    dados = open(rom, "rb").read()
    base = endereco_tabela - 0x08000000
    por_ponteiro = {}
    for i in range(quantas):
        off = base + i * TAM_ENTRADA_SONG
        ptr = int.from_bytes(dados[off:off + 4], "little")
        por_ponteiro.setdefault(ptr, i)
    return por_ponteiro


def simbolo(mapfile, nome):
    padrao = re.compile(r"^\s+(0x[0-9a-f]+)\s+" + re.escape(nome) + r"\s*$")
    for linha in open(mapfile):
        m = padrao.match(linha)
        if m:
            return int(m.group(1), 16)
    raise SystemExit(f"simbolo {nome} nao achado em {mapfile}")


def conta_songs():
    return sum(1 for l in open(os.path.join(RAIZ, "sound", "song_table.inc"))
               if re.match(r"\s*song\s+", l))


def roda_caso(rom, simbolos, addr_music, addr_player, grupo, num, prefixo):
    os.makedirs(SAIDA, exist_ok=True)
    roteiro = ",".join([tc.ABERTURA, tc.rota_warp(grupo, num, 0), "240:NADA"])
    cmd = [tc.RUNNER, rom, "900", roteiro, f"{SAIDA}/{prefixo}.png",
           "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"],
           "--oponente", simbolos["gTrainerBattleParameter"],
           "--mem16", hex(addr_music),
           "--mem32", hex(addr_player)]
    saida = subprocess.run(cmd, capture_output=True, text=True)
    estados = []
    for linha in saida.stdout.splitlines():
        m = tc.LINHA_ESTADO.match(linha)
        if m:
            estados.append(dict(p.split("=", 1) for p in m.group(2).split()))
    if not estados:
        raise SystemExit(f"gba_runner nao imprimiu estado. stderr:\n{saida.stderr}")
    return estados[-1]


def demo():
    """Autoteste do que da para autotestar sem emulador."""
    n = numero_da_faixa("MUS_HG_AZALEA")
    assert n == numero_da_faixa("MUS_VERDANTURF"), "apelido nao bate com o alvo"
    assert n != numero_da_faixa("MUS_PETALBURG_WOODS"), "ainda em Petalburg Woods"
    assert numero_da_faixa("MUS_GYM") == 364, n
    assert conta_songs() > 500
    por_nome, _ = tc.carrega_mapas()
    faltam = [c[0] for c in CASOS if c[0] not in por_nome]
    assert not faltam, f"mapa desconhecido: {faltam}"
    print(f"demo OK: {len(CASOS)} mapas resolvidos, "
          f"MUS_HG_AZALEA={n}, {conta_songs()} faixas na tabela")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=os.path.join(RAIZ, "pokeemerald.gba"))
    ap.add_argument("--map", dest="mapfile",
                    default=os.path.join(RAIZ, "pokeemerald.map"))
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        return demo()

    simbolos = tc.carrega_simbolos(args.mapfile)
    addr_music = simbolo(args.mapfile, "gMapHeader") + OFF_MUSIC
    addr_player = simbolo(args.mapfile, "gMPlayInfo_BGM") + OFF_SONG_HEADER
    por_ponteiro = tabela_de_ponteiros(
        args.rom, simbolo(args.mapfile, "gSongTable"), conta_songs())
    por_nome, _ = tc.carrega_mapas()

    print(f"gMapHeader.music em {addr_music:#010x}, "
          f"gMPlayInfo_BGM.songHeader em {addr_player:#010x}")
    print(f"{'mapa':30s} {'esperada':20s} {'header':>7s} {'driver':>7s}  veredito")
    ruins = 0
    for nome, faixa, motivo in CASOS:
        grupo, num = por_nome[nome]
        esperado = numero_da_faixa(faixa)
        est = roda_caso(args.rom, simbolos, addr_music, addr_player,
                        grupo, num, nome.lower())
        lido = int(est[f"mem16_0x{addr_music:08X}"])
        ptr = int(est[f"mem32_0x{addr_player:08X}"], 16)
        tocando = por_ponteiro.get(ptr, -1)
        chegou = (int(est["grupo"]), int(est["num"])) == (grupo, num)
        ok = chegou and lido == esperado and tocando == esperado
        ruins += not ok
        veredito = "OK" if ok else (
            "NAO CHEGOU NO MAPA" if not chegou else "FAIXA ERRADA")
        print(f"{nome:30s} {faixa:20s} {lido:7d} {tocando:7d}  {veredito}  ({motivo})")
    print(f"\n{len(CASOS) - ruins} de {len(CASOS)} mapas com a faixa certa "
          f"no header E no driver de som.")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main() or 0)
