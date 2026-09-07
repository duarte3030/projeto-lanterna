#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portão estático da música: pega o erro que o build NÃO pega.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O modo de falha clássico ao trazer faixa nova para esta base é o ÍNDICE
DESLOCADO: uma linha a mais ou a menos em `sound/song_table.inc` e o
`#define MUS_X <n>` de `include/constants/songs.h` passa a apontar para a
faixa do vizinho. Isso NÃO quebra o build, não emite warning, não some no
link. O jogo compila, roda, e a cidade toca a música da caverna.

O segundo modo é o `.mid` sem linha em `sound/songs/midi/midi.cfg`: o
`audio_rules.mk` emite um `$(warning ...)` que se perde num log de 38 mil
linhas e a build só morre no LINK, com erro de símbolo que não diz o nome do
arquivo que faltou.

O terceiro é o `map.json` citando um `music` que não existe: aí o build morre,
mas com erro de C num arquivo gerado, longe do mapa culpado.

Os três são baratos de achar aqui e caros de achar no emulador.

USO
---
    python3 dev_scripts/valida_musica.py          # roda os 5 testes
    python3 dev_scripts/valida_musica.py --demo   # prova que os testes pegam
"""

import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def le(caminho):
    return open(os.path.join(RAIZ, caminho), encoding="utf-8").read()


def tabela_de_faixas(texto_song_table):
    """[(indice, simbolo, player)] na ordem em que o gSongTable é montado."""
    linhas = re.findall(r"^\tsong (\w+),\s*(\w+),", texto_song_table, flags=re.M)
    return [(i, s, p) for i, (s, p) in enumerate(linhas)]


def ids_numericos(texto_songs_h):
    """{id: {NOMES}}. Um id pode ter mais de um nome (MUS_DESERT e MUS_ROUTE111
    sao o mesmo 409 no Emerald), e um `#ifndef` posterior e inerte."""
    out = {}
    vistos = set()
    for nome, val in re.findall(
            r"^#define\s+([A-Z][A-Z0-9_]*)\s+(\d+)\s*(?://.*)?$",
            texto_songs_h, flags=re.M):
        if nome in vistos:
            continue
        vistos.add(nome)
        out.setdefault(int(val), set()).add(nome)
    return out


def nomes_conhecidos(texto_songs_h):
    """Todo nome que songs.h define, com numero ou por apelido."""
    return set(re.findall(r"^#define\s+([A-Z][A-Z0-9_]*)\s", texto_songs_h,
                          flags=re.M))


# Excecoes legitimas herdadas da base: o nome em songs.h e o simbolo da faixa
# divergem de proposito (a expansion renomeou a constante e manteve o .mid).
# Cada linha e um par (id, simbolo esperado na tabela) conferido a mao.
EXCECOES_NOME = {
    409: "mus_route111",   # songs.h chama de MUS_DESERT
}


def teste_indice(song_table, songs_h, erros):
    """A linha N de song_table.inc tem de ser o id N de songs.h."""
    tab = tabela_de_faixas(song_table)
    por_indice = {i: s for i, s, _ in tab}
    por_id = ids_numericos(songs_h)
    for ident in sorted(por_id):
        nomes = por_id[ident]
        if nomes <= {"MUS_ROUTE118", "MUS_NONE"}:
            continue
        if ident not in por_indice:
            erros.append("songs.h: %s = %d, mas gSongTable so tem %d entradas"
                         % (sorted(nomes)[0], ident, len(tab)))
            continue
        achado = por_indice[ident]
        if achado in {n.lower() for n in nomes}:
            continue
        if EXCECOES_NOME.get(ident) == achado:
            continue
        erros.append("INDICE DESLOCADO: songs.h diz %s = %d, mas a linha %d de "
                     "song_table.inc e `song %s`"
                     % ("/".join(sorted(nomes)), ident, ident, achado))


def teste_duplicatas(song_table, erros):
    """Nenhum simbolo pode entrar duas vezes no gSongTable, e toda linha da
    tabela tem de ter nome em songs.h. A linha repetida foi o erro real desta
    onda: `mus_dp_victory_road` estava em duas listas da curadoria, entrou duas
    vezes, e o teste de indice NAO pegou, porque o id extra simplesmente nao
    tinha nome nenhum apontando para ele."""
    simbolos = [s for _, s, _ in tabela_de_faixas(song_table)]
    # `dummy_song_header` e o buraco proposital do gSongTable e se repete
    for s in sorted({x for x in simbolos if simbolos.count(x) > 1}):
        if s in ("mus_dummy", "dummy_song_header"):
            continue
        erros.append("song_table.inc tem `song %s` %d vezes: todos os ids "
                     "depois da segunda estao empurrados" % (s, simbolos.count(s)))


def teste_todas_tem_nome(song_table, songs_h, erros):
    """Toda faixa da tabela precisa de um `#define` que a alcance; sem ele o id
    existe na ROM e ninguem consegue toca-la."""
    nomeados = set()
    for ident, nomes in ids_numericos(songs_h).items():
        nomeados.add(ident)
    for i, sim, _ in tabela_de_faixas(song_table):
        if sim in ("mus_dummy", "dummy_song_header", "se_stop", "se_dummy"):
            continue
        if i not in nomeados:
            erros.append("song_table.inc linha %d (`song %s`) nao tem "
                         "#define em songs.h" % (i, sim))


def teste_midi_cfg(erros):
    # o make usa $(basename ...) na chave do midi.cfg, entao `nome:` e
    # `nome.mid:` dao a mesma regra: comparar sem extensao.
    mids = {os.path.basename(p)[:-4] for p in
            glob.glob(os.path.join(RAIZ, "sound/songs/midi/*.mid"))}
    cfg = {os.path.splitext(l.split(":")[0].strip())[0]
           for l in le("sound/songs/midi/midi.cfg").splitlines() if l.strip()}
    for m in sorted(mids - cfg):
        erros.append("sem linha em midi.cfg (o build so quebra no LINK): %s" % m)
    for c in sorted(cfg - mids):
        erros.append("midi.cfg cita um .mid que nao existe: %s" % c)
    chaves = [os.path.splitext(l.split(":")[0].strip())[0]
              for l in le("sound/songs/midi/midi.cfg").splitlines() if l.strip()]
    for c in sorted({x for x in chaves if chaves.count(x) > 1}):
        erros.append("midi.cfg tem a chave %s duas vezes (o make avisa "
                     "`overriding commands for target`)" % c)


def teste_voicegroups(erros):
    grupos = set()
    for p in glob.glob(os.path.join(RAIZ, "sound/voicegroups/**/*.inc"),
                       recursive=True):
        grupos |= set(re.findall(r"^\s*voice_group\s+(\w+)", open(p).read(),
                                 flags=re.M))
        grupos |= set(re.findall(r"^voicegroup_(\w+)::", open(p).read(),
                                 flags=re.M))
    incluidos = set(re.findall(r'\.include "sound/voicegroups/(\S+)\.inc"',
                               le("sound/voice_groups.inc")))
    for linha in le("sound/songs/midi/midi.cfg").splitlines():
        m = re.search(r"-G_(\S+)", linha)
        if m and m.group(1) not in grupos:
            erros.append("midi.cfg pede -G_%s e nenhum voicegroup tem esse nome (%s)"
                         % (m.group(1), linha.split(":")[0]))
    for p in glob.glob(os.path.join(RAIZ, "sound/voicegroups/**/*.inc"),
                       recursive=True):
        rel = os.path.relpath(p, os.path.join(RAIZ, "sound/voicegroups"))[:-4]
        if rel not in incluidos:
            erros.append("voicegroup %s.inc existe e nao esta em voice_groups.inc"
                         % rel)


def teste_amostras(erros):
    dsd = le("sound/direct_sound_data.inc")
    for sim, arq in re.findall(
            r"DirectSoundWaveData_(\w+)::\s*\n\s*\.incbin \"sound/direct_sound_samples/(\S+?)\.bin\"",
            dsd):
        base = os.path.join(RAIZ, "sound/direct_sound_samples", arq)
        if not (os.path.exists(base + ".wav") or os.path.exists(base + ".aif")):
            erros.append("amostra %s: nao ha %s.wav nem %s.aif" % (sim, arq, arq))
    vistos = re.findall(r"DirectSoundWaveData_(\w+)::", dsd)
    # o mesmo simbolo pode aparecer duas vezes em ramos opostos de um
    # `.if PHONEMES_SHARED` do assembler; so conta duplicata fora de condicional
    fora, prof = [], 0
    for linha in dsd.splitlines():
        t = linha.strip()
        if t.startswith((".if", ".ifdef", ".ifndef")):
            prof += 1
        elif t.startswith(".endif"):
            prof = max(0, prof - 1)
        elif prof == 0:
            m = re.match(r"DirectSoundWaveData_(\w+)::", t)
            if m:
                fora.append(m.group(1))
    for s in sorted({x for x in fora if fora.count(x) > 1}):
        erros.append("simbolo de amostra duplicado: DirectSoundWaveData_%s" % s)
    # todo simbolo que um voicegroup usa tem de existir
    pedidos = set()
    for p in glob.glob(os.path.join(RAIZ, "sound/voicegroups/**/*.inc"),
                       recursive=True):
        pedidos |= set(re.findall(r"DirectSoundWaveData_(\w+)", open(p).read()))
    for s in sorted(pedidos - set(vistos)):
        erros.append("voicegroup usa DirectSoundWaveData_%s e ninguem define" % s)


def teste_mapas(songs_h, erros):
    conhecidos = nomes_conhecidos(songs_h)
    for caminho in sorted(glob.glob(os.path.join(RAIZ, "data/maps/*/map.json"))):
        try:
            j = json.load(open(caminho, encoding="utf-8"))
        except Exception as e:
            erros.append("%s nao e JSON valido: %s" % (caminho, e))
            continue
        m = j.get("music")
        if m and m not in conhecidos:
            erros.append("%s pede music %s, que songs.h nao define"
                         % (os.path.basename(os.path.dirname(caminho)), m))


def roda(song_table, songs_h):
    erros = []
    teste_indice(song_table, songs_h, erros)
    teste_duplicatas(song_table, erros)
    teste_todas_tem_nome(song_table, songs_h, erros)
    teste_midi_cfg(erros)
    teste_voicegroups(erros)
    teste_amostras(erros)
    teste_mapas(songs_h, erros)
    return erros


def demo():
    """Prova que o teste de índice pega o erro que ele existe para pegar."""
    song_table = le("sound/song_table.inc")
    songs_h = le("include/constants/songs.h")

    print("== demo 1: arvore como esta ==")
    erros = []
    teste_indice(song_table, songs_h, erros)
    print("   indice: %d erro(s)" % len(erros))

    print("== demo 2: uma linha a mais no meio do gSongTable ==")
    quebrado = song_table.replace("\tsong mus_littleroot,",
                                  "\tsong mus_dummy, MUSIC_PLAYER_BGM, 0\n"
                                  "\tsong mus_littleroot,", 1)
    erros2 = []
    teste_indice(quebrado, songs_h, erros2)
    print("   indice: %d erro(s), o primeiro:" % len(erros2))
    print("   " + (erros2[0] if erros2 else "NENHUM -- o teste esta cego!"))

    print("== demo 3: um map.json pedindo faixa que nao existe ==")
    erros3 = []
    teste_mapas(songs_h.replace("#define MUS_LITTLEROOT", "#define MUS_NAO_EXISTE"),
                erros3)
    print("   mapas: %d erro(s), o primeiro:" % len(erros3))
    print("   " + (erros3[0] if erros3 else "NENHUM -- o teste esta cego!"))

    print("== demo 4: a MESMA faixa em duas listas da curadoria ==")
    # foi o erro real desta onda: mus_dp_victory_road estava em SINNOH_UNICO e
    # em SINNOH_BATALHA, entrou duas vezes, e o teste de indice sozinho passou
    # verde porque o id extra simplesmente nao tinha nome apontando para ele.
    duplicado = song_table.replace("\tsong mus_littleroot,",
                                   "\tsong mus_littleroot, MUSIC_PLAYER_BGM, 0\n"
                                   "\tsong mus_littleroot,", 1)
    erros4 = []
    teste_duplicatas(duplicado, erros4)
    print("   duplicatas: %d erro(s), o primeiro:" % len(erros4))
    print("   " + (erros4[0] if erros4 else "NENHUM -- o teste esta cego!"))

    ok = (not erros) and erros2 and erros3 and erros4
    print("\nDEMO %s" % ("OK" if ok else "FALHOU"))
    return 0 if ok else 1


def main():
    if "--demo" in sys.argv:
        return demo()
    erros = roda(le("sound/song_table.inc"), le("include/constants/songs.h"))
    if erros:
        print("MUSICA REPROVADA: %d problema(s)" % len(erros))
        for e in erros[:60]:
            print("  - " + e)
        if len(erros) > 60:
            print("  ... e mais %d" % (len(erros) - 60))
        return 1
    print("MUSICA OK: indice, midi.cfg, voicegroups, amostras e map.json batem")
    return 0


if __name__ == "__main__":
    sys.exit(main())
