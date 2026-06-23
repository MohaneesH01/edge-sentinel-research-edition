# Edge Sentinel paper draft

This directory holds the IEEE Access manuscript for Edge Sentinel.

## Files

- `paper.tex` — full LaTeX source, 9 sections, bibliography, ready for
  IEEE Access submission.
- `figures/` — copy PNGs from `../../reports/figures/` here before
  submission.
- `submission/` — empty placeholder for the IEEE submission packet (PDF +
  source + supplementary materials).

## Compile locally

```bash
cd docs/paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Or, easier: open this folder in [Overleaf](https://www.overleaf.com),
import the IEEE Access template, and copy in the contents of
`paper.tex`.

## Status

- [x] Title, abstract, keywords
- [x] Introduction with sharpened research question
- [x] Related work (10 citations, IEEE format)
- [x] Method with H1-H4 sub-hypotheses
- [x] Experimental setup
- [x] Results (synthetic-data table + figure references)
- [x] Discussion
- [x] Threats to validity
- [x] Future work
- [x] Conclusion
- [x] Bibliography
- [ ] Figures embedded as PNGs in submission folder
- [ ] Real-data numbers (replace synthetic when available)
- [ ] Calibration error (ECE) measurement
- [ ] Cross-domain validation results
- [ ] Energy budget numbers
