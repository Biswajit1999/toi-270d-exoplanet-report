# Data sources

## TESS light curve

- File: `tess2018263035959-s0003-0000000259377017-0123-s_lc.fits`
- Archive: Mikulski Archive for Space Telescopes (MAST), TESS SPOC light-curve product
- TESS sector: 3
- TIC target ID: 259377017
- MAST observation ID: 60920224
- MAST data URI: `mast:TESS/product/tess2018263035959-s0003-0000000259377017-0123-s_lc.fits`
- Exact download URL: <https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:TESS%2Fproduct%2Ftess2018263035959-s0003-0000000259377017-0123-s_lc.fits>
- Collection DOI: [10.17909/t9-nmc8-f686](https://doi.org/10.17909/t9-nmc8-f686) (TESS 2-minute light curves, all sectors; sector 3 used here)
- Retrieved: 2026-08-15
- SHA-256: `edaa0de029f6fde3d045352887ef1a2950bb9b38fc18075066c81d7638feb695`

The FITS file is stored unmodified. The analysis reads `TIME`, `PDCSAP_FLUX`,
`PDCSAP_FLUX_ERR`, and `QUALITY`. PDCSAP flux is the SPOC light curve with common
instrumental trends removed and aperture/crowding corrections applied; this does
not make it free of residual stellar or instrumental systematics.

## System parameters

- File: `system_parameters.csv`
- Service: NASA Exoplanet Archive TAP, `pscomppars` table
- Exact query: <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name%2Chostname%2Cra%2Cdec%2Cpl_orbper%2Cpl_tranmid%2Cpl_trandur%2Cpl_rade%2Cpl_bmasse%2Cpl_eqt%2Cpl_orbsmax%2Csy_dist%2Csy_tmag%2Cst_teff%2Cst_rad%2Cst_mass%2Cdisc_year%2Cdiscoverymethod%2Cdisc_refname%2Cdisc_pubdate%2Cdisc_facility+from+pscomppars+where+pl_name%3D%27TOI-270+d%27&format=csv>
- Retrieved: 2026-08-15

The saved row is the input actually used by `scripts/analyze_transit.py`; the
analysis does not query a changing live service at run time.

## Companion-planet ephemerides for the BLS mask

- File: `companion_ephemerides.csv`
- Service: NASA Exoplanet Archive TAP, `pscomppars` table
- Exact query: <https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name%2Cpl_orbper%2Cpl_tranmid%2Cpl_trandur+from+pscomppars+where+hostname%3D%27TOI-270%27&format=csv>
- Retrieved: 2026-08-15

The saved TOI-270 b and c period, transit-midpoint, and duration values define
the companion masks in `scripts/analyze_bls_crosscheck.py`. Masking prevents
the strong two-times-TOI-270-c harmonic near 11.32 days from being mistaken for
TOI-270 d. The BLS script never queries the live service at run time.


## Additional TESS sectors for robustness analysis

All are unmodified standard-cadence SPOC light curves from the same [MAST TESS collection](https://doi.org/10.17909/t9-nmc8-f686).

- Sector 3: `tess2018263035959-s0003-0000000259377017-0123-s_lc.fits` (1,998,720 bytes)
  - MAST URI: `mast:TESS/product/tess2018263035959-s0003-0000000259377017-0123-s_lc.fits`
  - SHA-256: `edaa0de029f6fde3d045352887ef1a2950bb9b38fc18075066c81d7638feb695`
- Sector 4: `tess2018292075959-s0004-0000000259377017-0124-s_lc.fits` (1,897,920 bytes)
  - MAST URI: `mast:TESS/product/tess2018292075959-s0004-0000000259377017-0124-s_lc.fits`
  - SHA-256: `09f1e69d89dce001e447fbc509b9453f033b2428d183add334b43b93dbc8c93b`
- Sector 5: `tess2018319095959-s0005-0000000259377017-0125-s_lc.fits` (1,923,840 bytes)
  - MAST URI: `mast:TESS/product/tess2018319095959-s0005-0000000259377017-0125-s_lc.fits`
  - SHA-256: `739250df0d1ccda4304e01213f1f0f53c24603e3e223ff646157b6721665a9d5`
