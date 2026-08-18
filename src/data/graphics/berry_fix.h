// dedupe_assets.py: compartilhado por 5 consumidores (lista em dev_scripts/dedupe_assets.json); editar este arquivo muda TODOS.
const u16 gBerryFixGbaConnect_Pal[] = INCGFX_U16("graphics/berry_fix/gba_connect.png", ".gbapal");
const u32 gBerryFixGbaConnect_Gfx[] = INCGFX_U32("graphics/berry_fix/gba_connect.png", ".4bpp.smol");
const u32 gBerryFixGbaConnect_Tilemap[] = INCGFX_U32("graphics/berry_fix/gba_connect.bin", ".smolTM");

const u16 gBerryFixGameboyLogo_Pal[] = INCGFX_U16("graphics/berry_fix/logo.png", ".gbapal");
const u32 gBerryFixGameboyLogo_Gfx[] = INCGFX_U32("graphics/berry_fix/logo.png", ".4bpp.smol");
const u32 gBerryFixGameboyLogo_Tilemap[] = INCGFX_U32("graphics/berry_fix/logo.bin", ".smolTM");

extern const u16 gBerryFixGbaTransfer_Pal[ARRAY_COUNT(gBerryFixGbaConnect_Pal)] ASSET_ALIAS(gBerryFixGbaConnect_Pal); // dedupe_assets.py: mesmos 64 B (md5 01e3ac85)
const u32 gBerryFixGbaTransfer_Gfx[] = INCGFX_U32("graphics/berry_fix/gba_transfer.png", ".4bpp.smol");
const u32 gBerryFixGbaTransfer_Tilemap[] = INCGFX_U32("graphics/berry_fix/gba_transfer.bin", ".smolTM");

extern const u16 gBerryFixGbaTransferHighlight_Pal[ARRAY_COUNT(gBerryFixGbaConnect_Pal)] ASSET_ALIAS(gBerryFixGbaConnect_Pal); // dedupe_assets.py: mesmos 64 B (md5 01e3ac85)
const u32 gBerryFixGbaTransferHighlight_Gfx[] = INCGFX_U32("graphics/berry_fix/gba_transfer_highlight.png", ".4bpp.smol");
const u32 gBerryFixGbaTransferHighlight_Tilemap[] = INCGFX_U32("graphics/berry_fix/gba_transfer_highlight.bin", ".smolTM");

extern const u16 gBerryFixGbaTransferError_Pal[ARRAY_COUNT(gBerryFixGbaConnect_Pal)] ASSET_ALIAS(gBerryFixGbaConnect_Pal); // dedupe_assets.py: mesmos 64 B (md5 01e3ac85)
const u32 gBerryFixGbaTransferError_Gfx[] = INCGFX_U32("graphics/berry_fix/gba_transfer_error.png", ".4bpp.smol");
const u32 gBerryFixGbaTransferError_Tilemap[] = INCGFX_U32("graphics/berry_fix/gba_transfer_error.bin", ".smolTM");

extern const u16 gBerryFixWindow_Pal[ARRAY_COUNT(gBerryFixGbaConnect_Pal)] ASSET_ALIAS(gBerryFixGbaConnect_Pal); // dedupe_assets.py: mesmos 64 B (md5 01e3ac85)
const u32 gBerryFixWindow_Gfx[] = INCGFX_U32("graphics/berry_fix/window.png", ".4bpp.smol");
const u32 gBerryFixWindow_Tilemap[] = INCGFX_U32("graphics/berry_fix/window.bin", ".smolTM");
