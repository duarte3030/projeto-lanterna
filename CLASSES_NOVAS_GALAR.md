# Classes de treinador que Galar tem e este motor nao

Gerado por `dev_scripts/treinadores_galar.py`. O demake reescreveu
os nomes de `gTrainerClassNames` para o elenco de Galar; as classes
abaixo NAO existem entre as 117 deste motor (RSE + FRLG) e por isso
entraram por de-para escrito a mao ou, quando nem isso havia, com o
placeholder `TRAINER_CLASS_COOLTRAINER_FRLG`.

Criar classe nova custa sprite, nome, musica de encontro e uma
entrada em `trainer_class_lookups.h`: e obra propria, nao desta
onda. A lista existe para o Gui decidir se quer pagar.

| classe da fonte | indice | classe usada aqui | por que |
|---|---|---|---|
| Ace Trainer | - | `TRAINER_CLASS_COOLTRAINER_FRLG` | de-para a mao: 'Ace Trainer' e o nome moderno do Cooltrainer do FRLG |
| Backpacker | - | `TRAINER_CLASS_HIKER_FRLG` | de-para a mao: backpacker |
| Beldade | - | `TRAINER_CLASS_BEAUTY_FRLG` | de-para a mao: e 'beauty' em portugues |
| Cabbie | - | `TRAINER_CLASS_SAILOR_FRLG` | de-para a mao: trabalhador de uniforme |
| Cook Derek | - | `TRAINER_CLASS_KINDLER` | de-para a mao: cozinheiro |
| Dancer | - | `TRAINER_CLASS_GUITARIST` | de-para a mao: artista de palco |
| Doctor | - | `TRAINER_CLASS_SCIENTIST_FRLG` | de-para a mao: jaleco |
| Dojo Master | - | `TRAINER_CLASS_BLACK_BELT_FRLG` | de-para a mao: mestre de dojo |
| Macro Cosmos | - | `TRAINER_CLASS_MAGMA_ADMIN` | de-para a mao: seguranca de corporacao, terno |
| Madame | - | `TRAINER_CLASS_LADY_FRLG` | de-para a mao: senhora rica |
| Membro | - | `TRAINER_CLASS_TEAM_AQUA` | de-para a mao: capanga generico |
| Mochileira | - | `TRAINER_CLASS_HIKER_FRLG` | de-para a mao: backpacker feminino |
| Model | - | `TRAINER_CLASS_BEAUTY_FRLG` | de-para a mao: modelo |
| Musician | - | `TRAINER_CLASS_GUITARIST` | de-para a mao: musico |
| Office Worke | - | `TRAINER_CLASS_GENTLEMAN_FRLG` | de-para a mao: escritorio, terno |
| Policial | - | `TRAINER_CLASS_GENTLEMAN_FRLG` | de-para a mao: uniforme, adulto |
| Swimmer♀ | - | `TRAINER_CLASS_SWIMMER_M_FRLG` | de-para a mao: swimmer sem simbolo de genero |
| Swimmer♂ | - | `TRAINER_CLASS_SWIMMER_M_FRLG` | de-para a mao: swimmer sem simbolo de genero |
| TEAM YELL | - | `TRAINER_CLASS_TEAM_AQUA` | de-para a mao: gangue de rua; a Aqua e a gangue do motor |
| Trainer Star | - | `TRAINER_CLASS_COOLTRAINER_FRLG` | de-para a mao: estrela de liga |
| Worker | - | `TRAINER_CLASS_HIKER_FRLG` | de-para a mao: operario |
| ウエ Ranger | - | `TRAINER_CLASS_PKMN_RANGER_FRLG` | de-para a mao: 'ウエ Ranger' e `PKMN Ranger` com a tabela de nome errada |
| ウエ Trainter | - | `TRAINER_CLASS_COOLTRAINER_FRLG` | de-para a mao: 'ウエ Trainter' e `PKMN Trainer` torto na fonte |
