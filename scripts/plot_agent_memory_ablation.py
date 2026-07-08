"""Generate public figures for the agent memory ablation study."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "agent_memory_ablation"
RESULTS = STUDY / "results" / "probe_ablation" / "analysis" / "probe_wave1_2_3_4_results.json"
FIGURES = STUDY / "results" / "figures"

BASELINE_BPB = 0.925845

BLUE = "#2563eb"
GREEN = "#16a34a"
ORANGE = "#f97316"
RED = "#dc2626"
PURPLE = "#7c3aed"
GRAY = "#64748b"
LIGHT_GRAY = "#e2e8f0"
DARK = "#111827"

PROBE_META = {
    "P01": ("parallel, same settings", "no_memory", "15m"),
    "P02": ("parallel, different temps", "no_memory", "15m"),
    "P03": ("single agent", "no_memory", "15m"),
    "P04": ("single, 30s evaluator", "no_memory", "15m"),
    "P05": ("private memory configured", "broken_memory", "15m"),
    "P06": ("shared memory configured", "broken_memory", "15m"),
    "P07": ("shared memory configured", "broken_memory", "30m"),
    "P08": ("private memory configured", "broken_memory", "30m"),
    "P09": ("parallel, different temps", "no_memory", "30m"),
    "P10": ("parallel, same settings", "no_memory", "15m"),
    "P11": ("high exploration, no memory", "no_memory", "45m"),
    "P12": ("high exploration + shared memory", "valid_memory", "45m"),
    "P13": ("two high-exploration agents", "no_memory", "45m"),
    "P14": ("private memory + high exploration", "missing", "not run"),
    "P15": ("seeded learning-rate hint", "seeded", "45m"),
    "P16": ("start from LR hint baseline", "seeded", "45m"),
    "P17": ("shared + private memory", "valid_memory", "45m"),
    "P18": ("seeded parallel agents", "missing", "not run"),
}

MEAN_BPB = {
    "P01": 0.958,
    "P02": 1.136,
    "P03": 1.070,
    "P04": 1.447,
    "P05": 1.051,
    "P06": 1.047,
    "P07": 1.055,
    "P08": 1.390,
    "P09": 1.190,
    "P10": 1.090,
    "P11": 1.816,
    "P12": 1.049,
    "P13": 1.852,
    "P15": 1.501,
    "P16": 1.216,
    "P17": 1.064,
}

COLORS = {
    "no_memory": BLUE,
    "valid_memory": GREEN,
    "broken_memory": ORANGE,
    "seeded": PURPLE,
    "missing": GRAY,
}


def style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": DARK,
            "axes.titlecolor": DARK,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": LIGHT_GRAY,
            "grid.linewidth": 0.8,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "legend.frameon": True,
            "legend.facecolor": "white",
            "legend.edgecolor": "#cbd5e1",
            "legend.framealpha": 0.96,
            "savefig.bbox": "tight",
        }
    )


def load_results() -> dict:
    return json.loads(RESULTS.read_text())


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.png", dpi=260)
    fig.savefig(FIGURES / f"{stem}.pdf")
    plt.close(fig)


def label_for(probe: str) -> str:
    name, _, budget = PROBE_META[probe]
    return f"{probe}: {name}\n{budget}"


def figure_probe_outcomes(results: dict) -> None:
    probes = [f"P{i:02d}" for i in range(1, 19)]
    y = list(range(len(probes)))

    fig, ax = plt.subplots(figsize=(11.2, 9.4), constrained_layout=True)
    ax.axvline(
        BASELINE_BPB,
        color=RED,
        linestyle="--",
        linewidth=1.8,
        label="baseline to beat",
    )

    for idx, probe in enumerate(probes):
        name, kind, _ = PROBE_META[probe]
        value = results.get(probe, {}).get("best_bpb")
        color = COLORS[kind]
        if value is None:
            ax.scatter(1.02, idx, marker="x", s=80, color=color, linewidth=2)
            ax.text(1.028, idx, "not run", va="center", fontsize=9.5, color=GRAY)
            continue
        ax.hlines(idx, xmin=min(value, BASELINE_BPB), xmax=max(value, BASELINE_BPB), color=LIGHT_GRAY, linewidth=2)
        marker = "*" if value < BASELINE_BPB else "o"
        size = 150 if marker == "*" else 90
        ax.scatter(value, idx, s=size, marker=marker, color=color, edgecolor="white", linewidth=1.0, zorder=3)
        ax.text(value + 0.006, idx, f"{value:.3f}", va="center", fontsize=9.5, color=DARK)

    ax.set_yticks(y)
    ax.set_yticklabels([label_for(p) for p in probes])
    ax.invert_yaxis()
    ax.set_xlim(0.86, 1.14)
    ax.set_xlabel("Best validation BPB reached (lower is better)")
    ax.set_title("Agent memory ablation: which probes beat the baseline?")
    ax.grid(axis="y", visible=False)

    handles = [
        plt.Line2D([0], [0], color=RED, linestyle="--", linewidth=1.8, label="baseline"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markersize=9, label="no memory"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=GREEN, markersize=9, label="valid memory"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=ORANGE, markersize=9, label="memory configured but broken"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PURPLE, markersize=9, label="seeded"),
        plt.Line2D([0], [0], marker="x", color=GRAY, markersize=8, linestyle="None", label="not run"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=9)

    save(fig, "figure-01-probe-outcomes")


def figure_memory_stabilization(results: dict) -> None:
    probes = ["P11", "P12", "P09", "P13"]
    labels = [
        "P11\nno memory",
        "P12\nshared memory",
        "P09\nno memory",
        "P13\nno memory",
    ]
    colors = [COLORS[PROBE_META[p][1]] for p in probes]
    mean_values = [MEAN_BPB[p] for p in probes]
    best_values = [results[p]["best_bpb"] for p in probes]
    worst_values = [results[p]["worst_bpb"] for p in probes]
    runs = [results[p]["n_runs"] for p in probes]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2), constrained_layout=True)

    ax = axes[0]
    x = range(len(probes))
    width = 0.34
    ax.bar([i - width / 2 for i in x], mean_values, width=width, color=colors, alpha=0.78, label="mean")
    ax.scatter([i + width / 2 for i in x], best_values, s=130, marker="*", color=colors, edgecolor="white", linewidth=1.0, label="best")
    ax.axhline(BASELINE_BPB, color=RED, linestyle="--", linewidth=1.6, label="baseline")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Validation BPB")
    ax.set_title("Shared memory keeps high exploration closer to baseline")
    ax.set_ylim(0.84, 2.02)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="x", visible=False)

    for i, (mean, best) in enumerate(zip(mean_values, best_values)):
        ax.text(i - width / 2, mean + 0.035, f"{mean:.3f}", ha="center", fontsize=9)
        ax.text(i + width / 2, best - 0.055, f"{best:.3f}", ha="center", fontsize=9)

    ax = axes[1]
    ax.bar(labels, worst_values, color=colors, alpha=0.82)
    ax.set_ylabel("Worst validation BPB")
    ax.set_title("Memory reduces catastrophic outcomes")
    ax.set_ylim(0, 8.4)
    ax.grid(axis="x", visible=False)
    for i, (value, n) in enumerate(zip(worst_values, runs)):
        ax.text(i, value + 0.16, f"{value:.2f}\n{n} runs", ha="center", fontsize=9.5)

    fig.text(
        0.5,
        -0.02,
        "P11/P12/P13 use high-exploration settings; P09 is the 30-minute parallel-diverse no-memory control. Mean values come from the preserved summary report; best/worst/counts come from the JSON probe table.",
        ha="center",
        fontsize=9.4,
        color=GRAY,
    )

    save(fig, "figure-02-memory-stabilization")


def figure_probe_inventory(results: dict) -> None:
    groups = {
        "no memory": [p for p in PROBE_META if PROBE_META[p][1] == "no_memory"],
        "valid memory": [p for p in PROBE_META if PROBE_META[p][1] == "valid_memory"],
        "broken memory": [p for p in PROBE_META if PROBE_META[p][1] == "broken_memory"],
        "seeded": [p for p in PROBE_META if PROBE_META[p][1] == "seeded"],
        "not run": [p for p in PROBE_META if PROBE_META[p][1] == "missing"],
    }
    labels = list(groups)
    counts = [sum(1 for p in groups[label] if results.get(p, {}).get("n_runs", 0) > 0) for label in labels]
    planned = [len(groups[label]) for label in labels]
    colors = [BLUE, GREEN, ORANGE, PURPLE, GRAY]

    fig, ax = plt.subplots(figsize=(9.8, 4.8), constrained_layout=True)
    x = range(len(labels))
    ax.bar(x, planned, color=LIGHT_GRAY, label="planned")
    ax.bar(x, counts, color=colors, label="executed")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Probe count")
    ax.set_title("Probe inventory: what was planned and what actually ran")
    ax.set_ylim(0, max(planned) + 1)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    for i, (done, total) in enumerate(zip(counts, planned)):
        ax.text(i, total + 0.12, f"{done}/{total}", ha="center", fontsize=10)

    save(fig, "figure-03-probe-inventory")


def main() -> None:
    style()
    results = load_results()
    figure_probe_outcomes(results)
    figure_memory_stabilization(results)
    figure_probe_inventory(results)


if __name__ == "__main__":
    main()
