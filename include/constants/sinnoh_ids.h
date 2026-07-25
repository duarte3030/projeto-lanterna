#ifndef GUARD_CONSTANTS_SINNOH_IDS_H
#define GUARD_CONSTANTS_SINNOH_IDS_H

// ponytail: os ids de evento de Sinnoh moram em um arquivo por grupo de mapas,
// para varios agentes escreverem em paralelo sem corrida de escrita.
//
// Este arquivo existe porque os includes ficavam em map_event_ids.h e foram
// apagados DUAS vezes por agentes que reescreveram aquele arquivo inteiro.
// Aqui ninguem mexe.

#include "constants/sinnoh/cidades.h"
#include "constants/sinnoh/rotas_oeste.h"
#include "constants/sinnoh/rotas_leste.h"
#include "constants/sinnoh/rotas_norte.h"
#include "constants/sinnoh/cavernas.h"
#include "constants/sinnoh/interiores_a.h"
#include "constants/sinnoh/interiores_b.h"
#include "constants/sinnoh/interiores_c.h"
#include "constants/sinnoh/interiores_d.h"
#include "constants/sinnoh/interiores_e.h"
#include "constants/sinnoh/interiores_f.h"
#include "constants/sinnoh/interiores_g.h"
#include "constants/sinnoh/interiores_h.h"
#include "constants/sinnoh/treinadores_a.h"
#include "constants/sinnoh/treinadores_b.h"
#include "constants/sinnoh/treinadores_c.h"

#endif // GUARD_CONSTANTS_SINNOH_IDS_H
