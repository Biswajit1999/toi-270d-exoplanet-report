"""Regression tests for the independent Box Least Squares cross-check."""

import analyze_bls_crosscheck as bls


def test_bls_recovers_a_coherent_archive_period_signal():
    result = bls.main()
    assert result["sectors"] == 3
    assert result["companion_masked_cadences"] > 0
    assert abs(result["recovered_period_days"] / result["archive_period_days"] - 1) < 0.001
    assert 2500 < result["box_depth_ppm"] < 4000
    assert result["box_depth_snr"] > 30
    assert bls.CSV_FILE.stat().st_size > 200
    assert bls.FIGURE_FILE.stat().st_size > 10_000
