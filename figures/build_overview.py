"""Build the paper's original three-panel IEWC lead figure in revised notation."""

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
PALE = "#F4F1FF"
PALE_NEUTRAL = "#F0F2F6"
PALE_ORANGE = "#FFF0E3"


def add_box(fig, xy, width, height, text, *, face, fontsize=12.5):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        transform=fig.transFigure,
        linewidth=0,
        edgecolor="none",
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
    curvature,
    x_label,
    y_label,
    formula,
    takeaway,
    box_face,
):
    plot_rect = (rect[0] + 0.025, rect[1] + 0.055, rect[2] - 0.05, rect[3] - 0.075)
    ax = fig.add_axes(plot_rect, projection="3d")
    coordinates = np.linspace(-1.0, 1.0, 31)
    x_grid, y_grid = np.meshgrid(coordinates, coordinates)
    x_curvature, y_curvature = curvature
    z_grid = (x_curvature * x_grid**2 + y_curvature * y_grid**2) / (
        x_curvature + y_curvature
    )
    ax.plot_surface(
        x_grid,
        y_grid,
        z_grid,
        color=color,
        alpha=0.10,
        edgecolor="none",
        shade=False,
        antialiased=True,
    )
    ax.plot_wireframe(
        x_grid,
        y_grid,
        z_grid,
        rstride=5,
        cstride=5,
        color=color,
        linewidth=0.55,
        alpha=0.72,
    )

    axis_length = 1.22
    ax.quiver(0, 0, 0, axis_length, 0, 0, color=INK, linewidth=0.8, arrow_length_ratio=0.09)
    ax.quiver(0, 0, 0, 0, -axis_length, 0, color=INK, linewidth=0.8, arrow_length_ratio=0.09)
    ax.quiver(0, 0, 0, 0, 0, 0.90, color=INK, linewidth=0.8, arrow_length_ratio=0.09)
    ax.text(1.30, 0, 0, x_label, color=INK, fontsize=8.5, ha="left", va="center")
    ax.text(0, -1.30, 0, y_label, color=INK, fontsize=8.5, ha="right", va="center")
    ax.text(0, 0, 0.99, r"penalty $p$", color=INK, fontsize=8.5, ha="center", va="bottom")
    ax.set_xlim(-1.12, 1.38)
    ax.set_ylim(-1.12, 1.38)
    ax.set_zlim(0, 1.05)
    ax.set_box_aspect((1.0, 1.0, 0.72))
    ax.set_proj_type("ortho")
    ax.view_init(elev=27, azim=-58)
    ax.set_axis_off()

    xmid = rect[0] + rect[2] / 2
    fig.text(xmid, rect[1] + rect[3] + 0.015, title, ha="center", va="bottom", color=INK, fontsize=14, fontweight="bold")

    fig.text(xmid, 0.240, formula, ha="center", va="center", color=INK, fontsize=11.5)
    add_box(
        fig,
        (rect[0], 0.035),
        rect[2],
        0.088,
        takeaway,
        face=box_face,
        fontsize=11.1,
    )
    add_arrow(fig, (xmid, 0.128), (xmid, 0.212), color=color)


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
        (0.18, 0.892),
        0.64,
        0.074,
        "CLOC: preserving learned behavior as an optimization constraint",
        face=PALE,
        fontsize=13.5,
    )
    fig.add_artist(
        Line2D([0.16, 0.84], [0.84, 0.84], transform=fig.transFigure, color=INK, lw=1.0)
    )
    for x in (0.17, 0.50, 0.83):
        add_arrow(fig, (x, 0.84), (x, 0.79), color=INK)

    panels = [
        (0.01, 0.285, 0.31, 0.455),
        (0.345, 0.285, 0.31, 0.455),
        (0.68, 0.285, 0.31, 0.455),
    ]
    add_penalty_panel(
        fig,
        panels[0],
        title="EWC (OPG)",
        color=INK,
        curvature=(2.5, 0.55),
        x_label=r"$a_{\mathrm{poorly\ fit}}$",
        y_label=r"$a_{\mathrm{well\ fit}}$",
        formula=r"$p=\lambda(s_p a_p^2+s_w a_w^2),\quad s_p\gg s_w$",
        takeaway="Implicitly favors high-gradient samples",
        box_face=PALE_NEUTRAL,
    )
    add_penalty_panel(
        fig,
        panels[1],
        title="Uniform IEWC",
        color=PRIMARY,
        curvature=(1.0, 1.0),
        x_label=r"$a_1$",
        y_label=r"$a_2$",
        formula=r"$p=\lambda(a_1^2+a_2^2)$",
        takeaway="Estimates normalized task sensitivity",
        box_face=PALE,
    )
    add_penalty_panel(
        fig,
        panels[2],
        title="Weighted IEWC",
        color=RDW,
        curvature=(0.50, 2.35),
        x_label=r"$a_{\mathrm{redundant}}$",
        y_label=r"$a_{\mathrm{novel}}$",
        formula=r"$p=\lambda(h_r a_r^2+h_n a_n^2),\quad h_r\ll h_n$",
        takeaway="Makes the aggregation measure explicit",
        box_face=PALE_ORANGE,
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
