"""Build the paper's deconfounded CLOC/IEWC lead figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


PRIMARY = "#3F21B6"
INK = "#172033"
MUTED = "#5F6878"
RDW = "#C15F18"
PAPER = "#FFFFFF"


def add_box(fig, xy, width, height, text, *, edge=INK, face=PAPER, fontsize=13):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.008",
        transform=fig.transFigure,
        linewidth=1.0,
        edgecolor=edge,
        facecolor=face,
    )
    fig.add_artist(box)
    fig.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        color=INK,
        fontsize=fontsize,
        fontweight="semibold",
    )


def add_arrow(fig, start, end, *, color=MUTED, linestyle="-"):
    fig.add_artist(
        FancyArrowPatch(
            start,
            end,
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=9,
            linewidth=1.0,
            linestyle=linestyle,
            color=color,
        )
    )


def penalty_surface(ax, x_weight, y_weight, *, color, title, direction_labels):
    grid = np.linspace(-1.0, 1.0, 35)
    x, y = np.meshgrid(grid, grid)
    z = x_weight * x**2 + y_weight * y**2
    ax.plot_wireframe(
        x,
        y,
        z,
        rstride=4,
        cstride=4,
        color=color,
        linewidth=0.75,
        alpha=0.9,
    )
    ax.view_init(elev=25, azim=-58)
    ax.set_box_aspect((1.15, 1.0, 0.72))
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(0, max(x_weight, y_weight) * 2.05)
    ax.set_axis_off()
    ax.set_title(title, color=INK, fontsize=14, fontweight="bold", pad=-2)
    ax.text2D(
        0.02,
        0.06,
        direction_labels[0],
        transform=ax.transAxes,
        color=MUTED,
        fontsize=11.5,
        ha="left",
    )
    ax.text2D(
        0.98,
        0.06,
        direction_labels[1],
        transform=ax.transAxes,
        color=MUTED,
        fontsize=11.5,
        ha="right",
    )


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "dejavusans",
            "pdf.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )
    fig = plt.figure(figsize=(12.0, 6.15), facecolor=PAPER)

    add_box(
        fig,
        (0.315, 0.89),
        0.37,
        0.065,
        "CLOC: choose the old behavior to preserve",
        edge=PRIMARY,
        face="#F4F1FF",
        fontsize=14,
    )
    add_box(
        fig,
        (0.075, 0.755),
        0.37,
        0.065,
        "Scalar-loss change  →  OPG matrix",
        fontsize=13,
    )
    add_box(
        fig,
        (0.555, 0.755),
        0.37,
        0.065,
        "Loss-level-set normal  →  IEF matrix",
        edge=PRIMARY,
        fontsize=13,
    )
    add_arrow(fig, (0.43, 0.89), (0.26, 0.82))
    add_arrow(fig, (0.57, 0.89), (0.74, 0.82), color=PRIMARY)

    axes = [
        fig.add_axes([0.035, 0.255, 0.285, 0.46], projection="3d"),
        fig.add_axes([0.3575, 0.255, 0.285, 0.46], projection="3d"),
        fig.add_axes([0.68, 0.255, 0.285, 0.46], projection="3d"),
    ]
    penalty_surface(
        axes[0],
        2.8,
        0.45,
        color=INK,
        title="OPG · uniform",
        direction_labels=(r"large $s_n$", r"small $s_n$"),
    )
    penalty_surface(
        axes[1],
        1.0,
        1.0,
        color=PRIMARY,
        title="IEF · uniform",
        direction_labels=(r"normalized $a_1$", r"normalized $a_2$"),
    )
    penalty_surface(
        axes[2],
        0.55,
        2.2,
        color=RDW,
        title="IEF · RDW (illustrative)",
        direction_labels=("redundant", "novel"),
    )

    fig.text(
        0.177,
        0.255,
        r"$\sum_n s_n\,a_na_n^\top$",
        ha="center",
        va="center",
        color=INK,
        fontsize=14,
    )
    fig.text(
        0.5,
        0.255,
        r"$\sum_n a_na_n^\top$",
        ha="center",
        va="center",
        color=PRIMARY,
        fontsize=14,
    )
    fig.text(
        0.823,
        0.255,
        r"$\sum_n \bar h_n\,a_na_n^\top$",
        ha="center",
        va="center",
        color=RDW,
        fontsize=14,
    )

    fig.add_artist(
        Line2D([0.05, 0.95], [0.185, 0.185], transform=fig.transFigure, color="#D7DAE0")
    )
    fig.text(
        0.5,
        0.115,
        "Normalization chooses the matrix; aggregation is a separate axis.",
        ha="center",
        va="center",
        color=INK,
        fontsize=14,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.06,
        "The confirmatory 2×2 design crosses OPG/IEF with uniform/RDW weighting.",
        ha="center",
        va="center",
        color=MUTED,
        fontsize=12,
    )

    output = Path(__file__).with_name("overview.pdf")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
