# TOI-270 d — Real TESS Transit Report

<p align="center">
  <img src="figures/toi270d_tess_transit.png" alt="Phase-folded real TESS transit light curve of TOI-270 d" width="760">
</p>

One real, public TESS SPOC light curve; one saved NASA Exoplanet Archive
ephemeris; one reproducible flat-versus-box statistical comparison.

**[Open the full report](https://biswajit1999.github.io/toi-270d-exoplanet-report/)** — the live GitHub Pages version.

## Data sources

- **System parameters** — the saved `pscomppars` row from the [NASA Exoplanet Archive TAP service](https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name%2Chostname%2Cra%2Cdec%2Cpl_orbper%2Cpl_tranmid%2Cpl_trandur%2Cpl_rade%2Cpl_bmasse%2Cpl_eqt%2Cpl_orbsmax%2Csy_dist%2Csy_tmag%2Cst_teff%2Cst_rad%2Cst_mass%2Cdisc_year%2Cdiscoverymethod%2Cdisc_refname%2Cdisc_pubdate%2Cdisc_facility+from+pscomppars+where+pl_name%3D%27TOI-270+d%27&format=csv).
- **Observed photometry** — unmodified MAST file `tess2018263035959-s0003-0000000259377017-0123-s_lc.fits`, TESS Sector 3, DOI [10.17909/t9-nmc8-f686](https://doi.org/10.17909/t9-nmc8-f686). This is a real SPOC reduced light curve, not simulated data.
- Exact URLs, IDs, retrieval date, and SHA-256 checksum are in [`data/SOURCE.md`](data/SOURCE.md).

## Reproduce the analysis

```bash
pip install -r requirements.txt
python scripts/analyze_transit.py
python scripts/analyze_multisector.py
pytest tests/ -v
```

The script keeps finite `QUALITY == 0` cadences, normalizes `PDCSAP_FLUX`,
applies one symmetric robust outlier rule, and examines ±2.5 published transit
durations around the fixed NASA ephemeris. It compares a weighted constant with
a two-level box whose depth is fitted. Timing and duration are not searched.

## What the numbers show

| Quantity | Result |
|---|---:|
| TESS sector | 3 |
| Cadences in comparison | 631 |
| Fitted box depth | 1854.7 ± 131.5 ppm |
| Flat χ² / dof / p | 1224.62 / 630 / 1.52e-40 |
| Box χ² / dof / p | 1025.71 / 629 / 1.56e-21 |
| Improvement Δχ² / Δdof / p | 198.91 / 1 / 3.62e-45 |

The fixed-window box improves strongly on a flat light curve for these data. This establishes only how these archived fluxes compare with this
pre-specified box model. It does not independently confirm the planet or identify
an atmosphere.

<!-- MULTISECTOR-UPGRADE-START -->
## Multi-sector robustness and correlated noise

The fixed archive ephemeris was fitted independently in 3 usable sector(s) (S3, S4, S5). Formal depth errors were inflated by sqrt(max(reduced chi-square, 1)) times the residual time-averaging beta factor (observed range 1.31-3.33). The robust inverse-variance depth is 2645.1 +/- 137.9 ppm; Cochran Q = 2.18 for 2 dof (p = 0.3362). These scaled errors address underestimated scatter and short-timescale correlation, but they are not a full Gaussian-process or physical limb-darkened transit fit.

<p align="center"><img src="figures/toi270d_multisector_transits.png" alt="Independent sector transit fits for TOI-270 d" width="760"></p>

<p align="center"><img src="figures/toi270d_depth_consistency.png" alt="Sector depth consistency for TOI-270 d" width="760"></p>

<p align="center"><img src="figures/toi270d_noise_diagnostics.png" alt="Residual RMS time-averaging diagnostic for TOI-270 d" width="760"></p>

The per-sector table is in [`figures/multisector_statistics.csv`](figures/multisector_statistics.csv). Regenerate all three figures with `python scripts/analyze_multisector.py`.
<!-- MULTISECTOR-UPGRADE-END -->

## System context

- Radius: 2.00 Earth radii
- Mass: 4.20 Earth masses
- Orbital period: 11.381940 days
- Transit duration: 2.117 hours
- Semi-major axis: 0.0721 AU
- Equilibrium temperature: 383 K
- Host: TOI-270 · distance 22.48 pc
- Discovery: 2019 by Transit (Transiting Exoplanet Survey Satellite (TESS))

## Limitations

- A box is not a limb-darkened physical transit model and does not retrieve radius ratio, impact parameter, or stellar density.
- Period, mid-transit epoch, and duration are fixed to one NASA composite row; their uncertainties and transit-timing variations are not propagated.
- SPOC PDCSAP processing, crowding corrections, stellar variability, time-correlated noise, and underestimated point uncertainties can make absolute χ² p-values poor even when the relative comparison is informative.
- The χ² improvement uses one additional fitted depth parameter and no timing search. It is not a blind detection false-alarm probability, and nearby-star contamination is not ruled out.
- Published global fits combine sectors, instruments, detrending choices, limb darkening, and astrophysical priors. This deliberately smaller test does not replace them.

## Repository structure

```text
README.md
index.html
requirements.txt
data/                       unmodified TESS FITS + NASA row + SOURCE.md
scripts/analyze_transit.py  real-data analysis and figure generation
figures/                    generated plot + summary_statistics.csv
tests/                      real-data regression tests
.github/workflows/tests.yml CI on every push and pull request
LICENSE                     MIT
```

## References

1. [Günther et al. 2019](https://ui.adsabs.harvard.edu/abs/2019NatAs...3.1099G/abstract) — discovery reference as listed by the NASA Exoplanet Archive.
2. Ricker, G. R. et al. (2015), *Transiting Exoplanet Survey Satellite (TESS)*, JATIS 1, 014003, [doi:10.1117/1.JATIS.1.1.014003](https://doi.org/10.1117/1.JATIS.1.1.014003).
3. TESS Team, *TESS Light Curves — All Sectors*, MAST, [doi:10.17909/t9-nmc8-f686](https://doi.org/10.17909/t9-nmc8-f686); Sector 3 used here.
4. [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), `pscomppars` TAP row retrieved 2026-08-15.

## Author

Biswajit Jana — [Portfolio](https://biswajit1999.github.io/Biswajit_Jana.github.io/) · [GitHub](https://github.com/Biswajit1999) · [LinkedIn](https://www.linkedin.com/in/biswajit-jana-27011a151/) · [ORCID](https://orcid.org/0009-0002-2411-1891)
