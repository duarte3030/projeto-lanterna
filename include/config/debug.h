#ifndef GUARD_CONFIG_DEBUG_H
#define GUARD_CONFIG_DEBUG_H

// Overworld Debug
// ponytail: modo de montagem. Jogo novo cai direto no mapa, sem professor, sem
// escolha de genero, sem nome, sem cutscene da mae. So enquanto o hack esta
// sendo montado; deixe FALSE antes de qualquer versao jogavel.
// FALSE desde 05/08/2026: a abertura de Sinnoh (quarto em Twinleaf -> mae ->
// Barry -> Rota 201 -> laboratorio do Rowan em Sandgem) ja existe e e jogavel.
#define DEV_SKIP_INTRO                  FALSE
#define DEV_START_X                     7  // posicao no mapa de partida
#define DEV_START_Y                     6
#define DEV_START_MAP                   MAP_OREBURGH_CITY_POKEMON_CENTER_1F // para onde o jogo novo warpa

#define DEBUG_OVERWORLD_MENU            DISABLED_ON_RELEASE // Enables an overworld debug menu to change flags, variables, giving Pokémon and more, accessed by holding R and pressing START while in the overworld by default.
#define DEBUG_OVERWORLD_HELD_KEYS       (R_BUTTON)          // The keys required to be held to open the debug menu.
#define DEBUG_OVERWORLD_TRIGGER_EVENT   pressedStartButton  // The event that opens the menu when holding the key(s) defined in DEBUG_OVERWORLD_HELD_KEYS.
#define DEBUG_OVERWORLD_IN_MENU         FALSE               // Replaces the overworld debug menu button combination with a start menu entry (above Pokédex).

// Battle Debug Menu
#define DEBUG_BATTLE_MENU               DISABLED_ON_RELEASE // If set to TRUE, enables a debug menu to use in battles by pressing the Select button.
#define DEBUG_AI_DELAY_TIMER            FALSE // If set to TRUE, displays the number of frames it takes for the AI to choose a move. Replaces the "What will PKMN do" text. Useful for devs or anyone who modifies the AI code and wants to see if it doesn't take too long to run.

// Pokémon Debug
#define DEBUG_POKEMON_SPRITE_VISUALIZER DISABLED_ON_RELEASE // Enables a debug menu for Pokémon sprites and icons, accessed by pressing Select in the summary screen.

#endif // GUARD_CONFIG_DEBUG_H
