"""Model-independent Box Least Squares cross-check across the committed TESS sectors."""

from __future__ import annotations

import csv

from astropy.timeseries import BoxLeastSquares
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import analyze_transit as base


CSV_FILE = base.FIG_DIR / "bls_crosscheck.csv"
FIGURE_FILE = base.FIG_DIR / "toi270d_bls_crosscheck.png"
COMPANION_FILE = base.DATA_DIR / "companion_ephemerides.csv"


def mask_companion_transits(
    time: np.ndarray, flux: np.ndarray, error: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    """Mask disclosed TOI-270 b/c transit windows to avoid their period harmonics."""
    keep = np.ones(len(time), dtype=bool)
    with COMPANION_FILE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            period = float(row["period_days"])
            epoch = float(row["transit_midpoint_bjd"])
            duration = float(row["duration_hours"]) / 24
            phase = ((time - epoch + period / 2) % period) - period / 2
            keep &= np.abs(phase) > 0.65 * duration
    return time[keep], flux[keep], error[keep], int((~keep).sum())


def main() -> dict[str, float | int]:
    """Search a disclosed ±5% period window with a box model, independent of batman."""
    files = sorted(base.DATA_DIR.glob("tess*_lc.fits"))
    if not files:
        raise FileNotFoundError("No committed TESS SPOC light curves were found")
    curves = [base.load_light_curve(path) for path in files]
    time = np.concatenate([curve[0] for curve in curves])
    flux = np.concatenate([curve[1] for curve in curves])
    error = np.concatenate([curve[2] for curve in curves])
    cadences_before_mask = len(time)
    time, flux, error, companion_masked = mask_companion_transits(time, flux, error)
    time = time - time.min()

    period_grid = np.linspace(base.PERIOD_DAYS * 0.95, base.PERIOD_DAYS * 1.05, 4001)
    durations = np.asarray([0.8, 1.0, 1.2]) * base.DURATION_HOURS / 24
    model = BoxLeastSquares(time, flux, dy=error)
    periodogram = model.power(period_grid, durations, objective="snr", oversample=10)
    index = int(np.nanargmax(periodogram.power))
    recovered_period = float(periodogram.period[index])
    recovered_duration = float(periodogram.duration[index])
    recovered_time = float(periodogram.transit_time[index])
    statistics = model.compute_stats(recovered_period, recovered_duration, recovered_time)
    depth, depth_error = (float(value) for value in statistics["depth"])
    result: dict[str, float | int] = {
        "sectors": len(files),
        "cadences": len(time),
        "cadences_before_companion_mask": cadences_before_mask,
        "companion_masked_cadences": companion_masked,
        "archive_period_days": base.PERIOD_DAYS,
        "recovered_period_days": recovered_period,
        "period_offset_percent": (recovered_period / base.PERIOD_DAYS - 1) * 100,
        "box_duration_hours": recovered_duration * 24,
        "box_depth_ppm": depth * 1e6,
        "box_depth_error_ppm": depth_error * 1e6,
        "box_depth_snr": float(periodogram.depth_snr[index]),
    }

    base.FIG_DIR.mkdir(exist_ok=True)
    with CSV_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["quantity", "value", "unit"])
        units = {
            "sectors": "count",
            "cadences": "count",
            "cadences_before_companion_mask": "count",
            "companion_masked_cadences": "count",
            "archive_period_days": "days",
            "recovered_period_days": "days",
            "period_offset_percent": "percent",
            "box_duration_hours": "hours",
            "box_depth_ppm": "ppm",
            "box_depth_error_ppm": "ppm",
            "box_depth_snr": "sigma-equivalent depth/error",
        }
        for key, value in result.items():
            writer.writerow([key, f"{value:.12g}" if isinstance(value, float) else value, units[key]])

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.plot(periodogram.period, periodogram.depth_snr, color="#364fc7", lw=1.8)
    ax.axvline(base.PERIOD_DAYS, color="#17212b", ls=":", lw=1.5, label="archive period")
    ax.axvline(recovered_period, color="#b54708", ls="--", lw=1.5, label="BLS maximum")
    ax.scatter([recovered_period], [periodogram.depth_snr[index]], color="#b54708", zorder=3)
    ax.set(
        xlabel="Trial period [days]",
        ylabel="Box depth / uncertainty",
        title="TOI-270 d: companion-masked three-sector BLS cross-check",
    )
    ax.text(
        0.02,
        0.97,
        f"BLS: {recovered_period:.4f} d, {depth * 1e6:.0f} ± {depth_error * 1e6:.0f} ppm",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "#dce3e8"},
    )
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_FILE, dpi=190)
    plt.close(fig)
    return result


if __name__ == "__main__":
    summary = main()
    print(
        f"TOI-270 d BLS: period={summary['recovered_period_days']:.5f} d; "
        f"depth={summary['box_depth_ppm']:.1f} +/- {summary['box_depth_error_ppm']:.1f} ppm; "
        f"S/N={summary['box_depth_snr']:.1f}"
    )
