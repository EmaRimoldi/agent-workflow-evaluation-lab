"""Generate public figures for the agent memory ablation study."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "agent_memory_ablation"
RESULTS = STUDY / "results" / "probe_ablation" / "analysis" / "probe_wave1_2_3_4_results.json"
FIGURES = STUDY / "results" / "figures"

BASELINE_BPB = 0.925845

BLUE = "#2563eb"
GREEN = "#16a34a"
RED = "#dc2626"
PURPLE = "#7c3aed"
GRAY = "#64748b"
LIGHT_GRAY = "#e2e8f0"
DARK = "#111827"

VALID_PROBES = [
    "P02",
    "P03",
    "P04",
    "P09",
    "P10",
    "P11",
    "P12",
    "P13",
    "P15",
    "P16",
    "P17",
]

BROKEN_MEMORY_PROBES = {
    "P05": "private-memory context was empty",
    "P06": "shared-memory log was empty",
    "P07": "shared-memory log was empty",
    "P08": "private-memory context was empty",
}

CONTEXT_ONLY_PROBES = {
    "P01": "legacy training template used about 315 seconds per run",
}

NOT_RUN_PROBES = {
    "P14": "planned private-memory probe, not executed",
    "P18": "planned seeded parallel probe, not executed",
}

PROBE_META = {
    "P01": ("parallel, same settings", "context", "15 min"),
    "P02": ("parallel, mixed search styles", "no_memory", "15 min"),
    "P03": ("single-agent control", "no_memory", "15 min"),
    "P04": ("single agent, 30-second train", "no_memory", "15 min"),
    "P05": ("excluded: private memory broken", "excluded", "15 min"),
    "P06": ("excluded: shared memory broken", "excluded", "15 min"),
    "P07": ("excluded: shared memory broken", "excluded", "30 min"),
    "P08": ("excluded: private memory broken", "excluded", "30 min"),
    "P09": ("parallel, mixed search styles", "no_memory", "30 min"),
    "P10": ("parallel, same search style", "no_memory", "15 min"),
    "P11": ("exploratory, no memory", "no_memory", "45 min"),
    "P12": ("exploratory + shared memory", "valid_memory", "45 min"),
    "P13": ("two exploratory agents", "no_memory", "45 min"),
    "P14": ("private memory + exploratory", "missing", "not run"),
    "P15": ("seeded learning-rate hint", "seeded", "45 min"),
    "P16": ("start from seeded baseline", "seeded", "45 min"),
    "P17": ("shared + private memory", "valid_memory", "45 min"),
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
    "seeded": PURPLE,
    "context": GRAY,
    "excluded": GRAY,
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
    probes = VALID_PROBES
    y = list(range(len(probes)))

    fig, ax = plt.subplots(figsize=(11.4, 7.0), constrained_layout=True)
    ax.axvline(
        BASELINE_BPB,
        color=RED,
        linestyle="--",
        linewidth=1.8,
        label="baseline to beat",
    )

    for idx, probe in enumerate(probes):
        _, kind, _ = PROBE_META[probe]
        value = results.get(probe, {}).get("best_bpb")
        color = COLORS[kind]
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
    ax.set_title("Valid probe outcomes after excluding corrupted memory trials")
    ax.grid(axis="y", visible=False)

    handles = [
        plt.Line2D([0], [0], color=RED, linestyle="--", linewidth=1.8, label="baseline"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markersize=9, label="no memory"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=GREEN, markersize=9, label="valid memory"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PURPLE, markersize=9, label="seeded"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor=DARK, markersize=12, label="beat baseline"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=9)
    fig.text(
        0.5,
        -0.01,
        "Filter: P05-P08 excluded because memory was silently broken; P01 kept only as legacy context; P14/P18 did not run.",
        ha="center",
        fontsize=9.4,
        color=GRAY,
    )

    save(fig, "figure-01-probe-outcomes")


def figure_memory_stabilization(results: dict) -> None:
    probes = ["P11", "P12", "P09", "P13"]
    labels = [
        "P11\nexploratory\nno memory",
        "P12\nexploratory\nshared memory",
        "P09\nmixed style\nno memory",
        "P13\ntwo exploratory\nno memory",
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
    ax.set_title("Shared memory keeps exploratory agents near the baseline")
    ax.set_ylim(0.84, 2.02)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="x", visible=False)

    for i, (mean, best) in enumerate(zip(mean_values, best_values)):
        ax.text(i - width / 2, mean + 0.035, f"{mean:.3f}", ha="center", fontsize=9)
        ax.text(i + width / 2, best - 0.055, f"{best:.3f}", ha="center", fontsize=9)

    ax = axes[1]
    ax.bar(labels, worst_values, color=colors, alpha=0.82)
    ax.set_ylabel("Worst validation BPB")
    ax.set_title("Shared memory reduces catastrophic outcomes")
    ax.set_ylim(0, 8.4)
    ax.grid(axis="x", visible=False)
    for i, (value, n) in enumerate(zip(worst_values, runs)):
        ax.text(i, value + 0.16, f"{value:.2f}\n{n} runs", ha="center", fontsize=9.5)

    fig.text(
        0.5,
        -0.02,
        "Only valid-memory probes are used. P11/P12/P13 use exploratory prompt style for 45 minutes; P09 is a shorter mixed-style no-memory reference.",
        ha="center",
        fontsize=9.4,
        color=GRAY,
    )

    save(fig, "figure-02-memory-stabilization")


def figure_validity_filter(results: dict) -> None:
    labels = [
        "planned\nprobes",
        "not\nrun",
        "excluded:\nbroken memory",
        "context only:\nlegacy timing",
        "primary valid\nanalysis set",
    ]
    counts = [
        len(PROBE_META),
        len(NOT_RUN_PROBES),
        len(BROKEN_MEMORY_PROBES),
        len(CONTEXT_ONLY_PROBES),
        len(VALID_PROBES),
    ]
    colors = [LIGHT_GRAY, GRAY, GRAY, GRAY, GREEN]

    fig, ax = plt.subplots(figsize=(9.6, 4.8), constrained_layout=True)
    x = range(len(labels))
    ax.bar(x, counts, color=colors)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Probe count")
    ax.set_title("Validity filter used for public analysis")
    ax.set_ylim(0, max(counts) + 2)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", visible=False)
    for i, value in enumerate(counts):
        ax.text(i, value + 0.35, str(value), ha="center", fontsize=11, color=DARK)

    valid_runs = sum(results[p]["n_runs"] for p in VALID_PROBES)
    broken_runs = sum(results[p]["n_runs"] for p in BROKEN_MEMORY_PROBES)
    fig.text(
        0.5,
        -0.02,
        f"The canonical figures use {valid_runs} training records. The {broken_runs} records from P05-P08 are retained only as operational evidence of a memory-pipeline failure.",
        ha="center",
        fontsize=9.4,
        color=GRAY,
    )

    save(fig, "figure-03-validity-filter")


def main() -> None:
    style()
    results = load_results()
    figure_probe_outcomes(results)
    figure_memory_stabilization(results)
    figure_validity_filter(results)


if __name__ == "__main__":
    main()
