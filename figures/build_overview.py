"""Build the paper's original three-panel IEWC lead figure in revised notation."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch


PRIMARY = "#3F21B6"
INK = "#172033"
MUTED = "#5F6878"
RDW = "#C15F18"
PAPER = "#FFFFFF"
PALE = "#F4F1FF"


def add_box(fig, xy, width, height, text, *, edge=INK, face=PAPER, fontsize=12.5):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.008",
        transform=fig.transFigure,
        linewidth=1.0,
        edgecolor=edge,
        facecolor=face,
    )
    fig.add_artist(patch)
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


def add_arrow(fig, start, end, *, color=INK, linewidth=1.0):
    fig.add_artist(
        FancyArrowPatch(
            start,
            end,
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=linewidth,
            color=color,
        )
    )


def add_penalty_panel(
    fig,
    rect,
    *,
    title,
    color,
    ellipse_ratio,
    ellipse_angle,
    left_label,
    right_label,
    formula,
    takeaway,
):
    ax = fig.add_axes(rect)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.92, 1.1)
    ax.axis("off")

    center = (0.0, 0.02)
    for index in range(1, 10):
        scale = index / 9
        ellipse = Ellipse(
            center,
            width=1.72 * scale,
            height=1.72 * ellipse_ratio * scale,
            angle=ellipse_angle,
            fill=False,
            linewidth=1.05,
            edgecolor=color,
            alpha=0.48 + 0.045 * index,
        )
        ax.add_patch(ellipse)

    ax.annotate(
        "",
        xy=(0.0, 1.02),
        xytext=(0.0, -0.66),
        arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.0},
    )
    ax.annotate(
        "",
        xy=(0.96, -0.62),
        xytext=(0.0, -0.66),
        arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.0},
    )
    ax.annotate(
        "",
        xy=(-0.80, -0.86),
        xytext=(0.0, -0.66),
        arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.0},
    )

    ax.text(0.02, 1.01, r"penalty $p$", color=INK, fontsize=11, va="bottom")
    ax.text(1.00, -0.66, right_label, color=INK, fontsize=10.5, ha="left", va="center")
    ax.text(-0.83, -0.87, left_label, color=INK, fontsize=10.5, ha="right", va="top")
    ax.set_title(title, color=INK, fontsize=15, fontweight="bold", pad=2)

    xmid = rect[0] + rect[2] / 2
    fig.text(xmid, 0.185, formula, ha="center", va="center", color=INK, fontsize=12)
    add_box(
        fig,
        (rect[0] + 0.015, 0.025),
        rect[2] - 0.03,
        0.075,
        takeaway,
        edge=color,
        face=PALE if color == PRIMARY else PAPER,
        fontsize=11.5,
    )
    add_arrow(fig, (xmid, 0.10), (xmid, 0.16), color=color)


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "dejavusans",
            "pdf.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )
    fig = plt.figure(figsize=(12.0, 6.45), facecolor=PAPER)

    add_box(
        fig,
        (0.22, 0.895),
        0.56,
        0.065,
        "CLOC: preserving learned behavior as an optimization constraint",
        edge=PRIMARY,
        face=PALE,
        fontsize=14,
    )
    fig.add_artist(
        Line2D([0.16, 0.84], [0.84, 0.84], transform=fig.transFigure, color=INK, lw=1.0)
    )
    for x in (0.17, 0.50, 0.83):
        add_arrow(fig, (x, 0.84), (x, 0.79), color=INK)

    panels = [
        (0.02, 0.25, 0.30, 0.50),
        (0.35, 0.25, 0.30, 0.50),
        (0.68, 0.25, 0.30, 0.50),
    ]
    add_penalty_panel(
        fig,
        panels[0],
        title="EWC (OPG)",
        color=INK,
        ellipse_ratio=0.38,
        ellipse_angle=25,
        left_label=r"$a_{\mathrm{well\ fit}}$",
        right_label=r"$a_{\mathrm{poorly\ fit}}$",
        formula=r"$p=\lambda(s_p a_p^2+s_w a_w^2),\quad s_p\gg s_w$",
        takeaway="Implicitly favors high-gradient samples",
    )
    add_penalty_panel(
        fig,
        panels[1],
        title="Uniform IEWC",
        color=PRIMARY,
        ellipse_ratio=0.72,
        ellipse_angle=18,
        left_label=r"$a_2$",
        right_label=r"$a_1$",
        formula=r"$p=\lambda(a_1^2+a_2^2)$",
        takeaway="Estimates normalized task sensitivity",
    )
    add_penalty_panel(
        fig,
        panels[2],
        title="Weighted IEWC",
        color=RDW,
        ellipse_ratio=0.40,
        ellipse_angle=-5,
        left_label=r"$a_{\mathrm{novel}}$",
        right_label=r"$a_{\mathrm{redundant}}$",
        formula=r"$p=\lambda(h_r a_r^2+h_n a_n^2),\quad h_r\ll h_n$",
        takeaway="Makes the aggregation measure explicit",
    )

    output = Path(__file__).with_name("overview.pdf")
    fig.savefig(
        output,
        bbox_inches="tight",
        pad_inches=0.03,
        metadata={"CreationDate": None, "ModDate": None},
    )
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
