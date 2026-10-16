# Tithi Singh: Finance Analyst Portfolio

Two projects built from SEC filings (10-K, 10-Q, 8-K):

1. **Coca-Cola vs PepsiCo vs Monster**: five years of financial-statement analysis (growth, margins, DuPont ROE, working capital, leverage, free cash flow, shareholder payouts).
2. **Monster Beverage valuation**: TTM build, CAPM/WACC, five-year DCF with live sliders, WACC x terminal-growth sensitivity, reverse DCF, trading comps and a football field.

Live site: `https://YOUR-USERNAME.github.io/tithi-singh-portfolio/` (after you enable GitHub Pages).

## Files
- `index.html` is the whole site (Chart.js loads from a CDN).
- `src/data.py` holds every figure taken from the filings, with accession numbers listed on the page.
- `src/analysis.py` checks and computes the results; `src/build.py` + `src/page.js` generate the page from `results.json`.
- `src/profile.json` holds name, email, LinkedIn and GitHub. Fill these in, rerun the build (below), and the Contact section updates.

## Rebuild
```bash
cd src && python analysis.py && python build.py   # writes index.html in src/
```
(Copy the generated page body into `../index.html`, or ask Claude to regenerate it with your contact details.)

Educational project, not investment advice. Share prices were taken from public quote pages on Oct 14-15, 2026.
