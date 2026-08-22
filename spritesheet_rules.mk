OBJEVENTGFXDIR := graphics/object_events/pics

$(OBJEVENTGFXDIR)/people/brendan/walking.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/brendan/running.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/may/walking.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/may/running.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/ruby_sapphire_brendan/walking.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/ruby_sapphire_brendan/running.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/ruby_sapphire_may/walking.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

$(OBJEVENTGFXDIR)/people/ruby_sapphire_may/running.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 2 -mheight 4

# Quebra-cabeca deslizante das Ruinas de Alph (src/sliding_puzzle.c).
# Cada peca e um sprite de 32x32, entao os tiles saem em blocos de 4x4.
SLIDINGPUZZLESDIR := graphics/sliding_puzzle/puzzles

$(SLIDINGPUZZLESDIR)/kabuto/tiles.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 4 -mheight 4

$(SLIDINGPUZZLESDIR)/omanyte/tiles.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 4 -mheight 4

$(SLIDINGPUZZLESDIR)/aerodactyl/tiles.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 4 -mheight 4

$(SLIDINGPUZZLESDIR)/ho_oh/tiles.4bpp: %.4bpp: %.png
	$(GFX) $< $@ -mwidth 4 -mheight 4
