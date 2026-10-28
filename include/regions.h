#ifndef GUARD_REGIONS_H
#define GUARD_REGIONS_H

#include "global.h"
#include "constants/regions.h"
#include "constants/map_groups.h"
#include "constants/maps.h"

enum KantoSubRegion GetKantoSubregion(u32 mapSecId);

static inline enum Region GetRegionForSectionId(u32 sectionId)
{
    if (sectionId >= KANTO_MAPSEC_START && sectionId < MAPSEC_SPECIAL_AREA)
        return REGION_KANTO;
    // >>> Dex completa: as outras regioes (dev_scripts/distribui_dex.py) >>>
    // MEDIDO em 21/08/2026, e nao lembrado: as tres faixas abaixo sao as unicas
    // do enum de MAPSEC que pertencem a UMA regiao so. `MAPSEC_SS_AQUA` (entre
    // Unova e Galar) fica de fora de proposito: e o barco, e ele liga Johto a
    // Kanto.
    if (sectionId >= MAPSEC_SINNOH_WEST && sectionId <= MAPSEC_SINNOH_NORTH)
        return REGION_SINNOH;
    if (sectionId >= MAPSEC_UNOVA_WEST && sectionId <= MAPSEC_UNOVA_NORTH)
        return REGION_UNOVA;
    if (sectionId >= MAPSEC_GALAR_SOUTH && sectionId <= MAPSEC_GALAR_OTHER)
        return REGION_GALAR;
    // <<< Dex completa <<<
    return REGION_HOENN;
}

// CARTUCHO 2 (28/10/2026, fase 0 do PRD de assets): a regiao do motor sai
// SO da MAPSEC, nunca do grupo de mapa.
//
// Antes, Johto era deduzida por FAIXA DE GRUPO (os grupos de
// gMapGroup_TownsAndRoutes_Johto a gMapGroup_SpecialArea_Johto), porque os
// apelidos de MAPSEC de Johto eram todos MAPSEC_SINNOH_WEST. Essa regra errava
// em silencio: as quatro casas de Johto que moravam no grupo 128
// (gMapGroup_JohtoPortas) ficavam fora da faixa e o motor achava que eram
// Sinnoh (achado M1 da trilha F do PRD de assets). Johto saiu desta branch,
// e a regra por grupo saiu junto, para que nenhuma regiao nova a repita.
//
// Regra daqui em diante: regiao nova ganha uma FAIXA CONTIGUA de MAPSEC no
// enum (como MAPSEC_UNOVA_WEST..NORTH e MAPSEC_GALAR_SOUTH..OTHER) e uma linha
// em GetRegionForSectionId. Mapa fora de faixa de regiao do cartucho 2
// (MAPSEC_NONE, MAPSEC_SPECIAL_AREA, tumulo do cartucho 1) e REGION_NONE: nao
// existe "Hoenn por omissao" num cartucho sem Hoenn.
//
// GetRegionForSectionId continua respondendo Kanto, Sinnoh e Hoenn para uma
// MAPSEC dessas regioes, porque ela tambem le o LOCAL DE CAPTURA gravado no
// Pokemon (metLocation), que pode vir de outro jogo por troca.
//
// Custo de save ZERO: e leitura do cabecalho do mapa atual.
static inline enum Region GetCurrentRegion(void)
{
    enum Region regiao = GetRegionForSectionId(gMapHeader.regionMapSectionId);

    if (regiao == REGION_UNOVA || regiao == REGION_GALAR)
        return regiao;
    return REGION_NONE;
}

#endif // GUARD_REGIONS_H
