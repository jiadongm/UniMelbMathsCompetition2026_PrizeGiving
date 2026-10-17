# The hidden family trees in your blood

Slides for a short talk by Dr Jiadong Mao (University of Melbourne) at the prize-giving of the University of Melbourne School Mathematics Competition, 17 October 2026. The talk is for secondary-school students, teachers and parents.

The talk asks how we can work out the family tree of blood cells that nobody watched dividing. Inherited DNA "typos" act as clues, and maths helps turn those clues into explanations we can test.

## View the slides

**[View the slides online](https://jiadongm.github.io/UniMelbMathsCompetition2026_PrizeGiving/slides.html)**

Or download `slides.html` and open it in a browser. It is self-contained, so it works offline.

- Arrow keys or the space bar move between slides and reveal steps.
- Press `S` to open the speaker view with notes.
- Press `F` for full screen.

## Rebuild

You need [Quarto](https://quarto.org) and Python 3.

```bash
python3 scripts/make_figures.py   # redraw the SVG figures in figs/
quarto render slides.qmd          # rebuild slides.html
```

`scripts/check_slides.cjs` is an optional layout check. It needs Node.js, Playwright and Google Chrome. It saves a screenshot of every slide to `qa/` and reports any content that runs off a slide.

## Files

| Path | Contents |
| --- | --- |
| `slides.qmd` | Slide source and speaker notes (Quarto reveal.js) |
| `styles.css` | Deck styling |
| `figs/` | Figures. The SVGs are drawn by `scripts/make_figures.py` |
| `scripts/` | Figure generator and layout check |
| `AGENTS.md` | Talk plan, plain-language rules and working notes |

## Outline

1. Who is your closest relative? A human family tree
2. Your blood also has a family tree
3. From one cell to a whole family: DNA typos as clues
4. Puzzle: who are the closest relatives?
5. How many family trees are possible?
6. What do we care about family trees? Younger and older blood
7. Why it matters
8. An evolutionary game: luck and fitness
9. Who to talk to: Melbourne Integrative Genomics

## Notes and sources

The diagrams and counts are simplified illustrations, not real data. The evolutionary-game chart shows 20 runs of a simple computer model with a fixed random seed.

- Mitchell et al., [Clonal dynamics of haematopoiesis across the human lifespan](https://www.nature.com/articles/s41586-022-04786-y), *Nature* 2022
- Jaiswal et al., [Age-related clonal hematopoiesis associated with adverse outcomes](https://pubmed.ncbi.nlm.nih.gov/25426837/), *New England Journal of Medicine* 2014
- Felsenstein, The number of evolutionary trees, *Systematic Zoology* 1978
