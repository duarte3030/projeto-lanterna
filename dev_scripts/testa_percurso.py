#!/usr/bin/env python3
"""Joga a ROM sozinho e acusa reset, travamento e tela preta.

Uso:
    python3 dev_scripts/testa_percurso.py [rom.gba]

Existe porque "compila" e "os validadores passam" nao provam que o jogo roda: os
dois crashes desta sessao passaram por seis agentes e por dois validadores, e so
apareceram quando alguem abriu no emulador. Este script automatiza esse olhar.

Como decide, sem ninguem olhar a tela:
  - RESET: a tela de abertura tem assinatura propria (poucas cores, muito escura).
    Se ela reaparece DEPOIS de o jogo ja estar no mapa, o jogo reiniciou. Foi
    exatamente assim que o crash do sprite de FRLG se manifestou.
  - TRAVOU: N quadros seguidos byte a byte identicos com o jogo em movimento.
  - PRETA: uma cor so na tela por muito tempo.

Nao substitui jogar. Cobre a familia de bug que mais apareceu aqui: mapa que
derruba a ROM ao carregar.
"""
import glob
import os
import subprocess
import sys

RUNNER = ("/Users/duarte/Documents/ANTIGRAVITY/Pokemon Claude/Pokemon Claude"
          "/ferramentas/gba_runner")
SAIDA = "/tmp/claude-501/percurso"

# Abertura ate o jogador andando. NAO duplicar aqui: ela e medida quadro a
# quadro em testa_critico.py e ja mudou uma vez, quando o jogo passou a comecar
# no quarto de Pallet Town em vez de Twinleaf. Com a copia velha deste arquivo o
# jogador terminava a abertura com a caixa de texto do NES aberta, o START da
# prova de vida nao abria menu nenhum, e os 6 percursos falhavam com o jogo
# inteiro certo. Era o teste velho, nao regressao do jogo.
def _abertura():
    import importlib.util
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "testa_critico.py")
    spec = importlib.util.spec_from_file_location("_tc", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ABERTURA


ABERTURA = _abertura()

# Cada percurso e um trecho jogado depois da abertura.
PERCURSOS = {
    # todo percurso termina em "60:NADA,40:START!" de proposito: e a prova de vida
    "sai de casa e anda": "20:DOWN*12,20:NADA,20:DOWN*12,60:NADA,20:LEFT*10,60:NADA,40:START!",
    "anda para o norte": "20:UP*20,60:NADA,20:UP*20,60:NADA,40:START!",
    "anda para o sul": "20:DOWN*20,60:NADA,20:DOWN*20,60:NADA,40:START!",
    "anda para leste": "20:RIGHT*20,60:NADA,20:RIGHT*20,60:NADA,40:START!",
    "abre menu e fecha": "40:START!,90:NADA,40:B,90:NADA,40:START!",
    "fala com tudo em volta": "20:A*8,20:UP,20:A*8,20:RIGHT,20:A*8,20:DOWN,20:A*8,60:NADA,40:START!",
}


def cores_e_media(caminho):
    from PIL import Image
    d = list(Image.open(caminho).getdata())
    return len(set(d)), sum(sum(p) for p in d) // len(d)


def roda(rom, roteiro, prefixo):
    for f in glob.glob(f"{SAIDA}/{prefixo}-*.png"):
        os.remove(f)
    subprocess.run([RUNNER, rom, "900", roteiro, f"{SAIDA}/{prefixo}.png"],
                   capture_output=True)
    quadros = sorted(glob.glob(f"{SAIDA}/{prefixo}-*.png"))
    return [(f,) + cores_e_media(f) for f in quadros]


def parece_abertura(cores, media):
    """Assinatura medida da tela de abertura: poucas cores e muito escura."""
    return cores > 150 and media < 120


def analisa(quadros, passos_abertura):
    """Devolve lista de problemas encontrados."""
    problemas = []
    # so olha o que vem DEPOIS da abertura
    depois = quadros[passos_abertura:]
    for i, (f, cores, media) in enumerate(depois):
        if parece_abertura(cores, media):
            problemas.append(f"RESET: {os.path.basename(f)} tem a cara da tela de "
                             f"abertura ({cores} cores, media {media}) depois do jogo ja ter comecado")
            break
        if cores <= 2 and i > 1:
            problemas.append(f"TELA PRETA ou branca: {os.path.basename(f)} "
                             f"({cores} cor, media {media})")
            break
    # Travamento NAO se detecta por quadro repetido: jogador parado encostado na
    # parede produz quadros identicos e isso e normal. A primeira versao deste
    # script acusou 4 falsos positivos assim. O teste certo e de VIDA: o roteiro
    # termina apertando START, e se o menu nao abre o jogo nao esta respondendo.
    if len(depois) >= 2:
        antes_do_start, depois_do_start = depois[-2], depois[-1]
        if open(antes_do_start[0], "rb").read() == open(depois_do_start[0], "rb").read():
            problemas.append("NAO RESPONDE: apertar START no fim do percurso nao "
                             "mudou nada na tela")
    return problemas


def main():
    rom = sys.argv[1] if len(sys.argv) > 1 else "pokeemerald.gba"
    if not os.path.exists(rom):
        raise SystemExit(f"ROM nao encontrada: {rom}")
    if not os.path.exists(RUNNER):
        raise SystemExit(f"runner nao encontrado: {RUNNER}")
    os.makedirs(SAIDA, exist_ok=True)
    n_abertura = ABERTURA.count(",") + 1

    total = 0
    for nome, trecho in PERCURSOS.items():
        quadros = roda(rom, ABERTURA + "," + trecho, nome.replace(" ", "_"))
        problemas = analisa(quadros, n_abertura)
        marca = "OK  " if not problemas else "FALHA"
        print(f"  [{marca}] {nome}  ({len(quadros)} quadros)")
        for p in problemas:
            print(f"          {p}")
        total += len(problemas)
    print(f"\n{'nenhum problema' if not total else str(total)+' problema(s)'} "
          f"em {len(PERCURSOS)} percursos")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
