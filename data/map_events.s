#include "constants/global.h"
#include "constants/event_bg.h"
#include "constants/event_object_movement.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/secret_bases.h"
#include "constants/vars.h"
#include "constants/weather.h"
#include "constants/trainer_hill.h"
#include "constants/trainer_types.h"
@ Acrescentado em 18/08/2026: o campo `flag` de um object_event pode ser a flag
@ de treinador derrotado do motor (TRAINER_FLAGS_START + id), que e como o
@ BRONIUS de Unova_VirbankComplexB1F e a INFER de Unova_PinwheelForest somem
@ depois da cena sem gastar flag nova. Sem isto o id do treinador nao existe
@ nesta unidade. So macros, conferido: nenhuma redefinicao contra os headers
@ acima.
#include "constants/opponents.h"
#include "constants/berry.h"
#include "constants/species.h"
#include "constants/apricorn_tree.h"
	.include "asm/macros.inc"
	.include "constants/constants.inc"

	.section .rodata

	.include "data/maps/events.inc"
