# Onde estao as ROMs e fontes avaliadas

As ROMs NAO entram no repo: sao 16 a 32 MB cada e o .gitignore bloqueia *.gba e
*.nds de proposito. Ficam soltas na maquina do Gui.

| arquivo | caminho na maquina | veredito |
|---|---|---|
| sword-shield-gba-2020-11-25.gba | ~/Downloads/ | Galar REAL, 485 mapas, 44 bancos |
| PKM SwSh ULTIMATE+.gba | ~/Downloads/PKM SwSh ULTIMATE+_pokebat.net/ | Galar REAL, fork do de cima |
| Pokemon Scarlet,Violet & Indigo[COMPLETE].gba | ~/Downloads/ | Kanto com nome trocado, NAO serve |
| pokemon_liquid_crystal_beta_3.3.00100.gba | ~/Downloads/ | sem fonte; pokecrystal e melhor |
| platinum.nds | pokeemerald-expansion/ | fonte de gen 4, ver DEMAKE-DS.md |
| black.nds | pokeemerald-expansion/ | gen 5, formato so metade resolvido |

Clones de fonte aberta (fora do repo, em /tmp durante a sessao; reclonar quando
precisar):

    git clone --depth 1 https://github.com/pret/pokecrystal
    git clone --depth 1 https://github.com/pret/pokeemerald

E os que ja moram em ~/Projetos/pokemon-claude/fontes-mapas/:
sinnoh (port GBA), hns (Heart n Soul), pokeplatinum (decomp de DS).

Para reavaliar qualquer ROM:  python3 dev_scripts/avalia_rom_gba.py caminho.gba
