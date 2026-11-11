"""Generate Figure 1: penalty bowls for EWC (OPG), uniform IEWC, and weighted IEWC."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib import patheffects as pe

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "DejaVu Sans",
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,
})

FIG_W, FIG_H = 16.62, 9.46
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=160)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

blue = "#2978ff"
light_blue = "#85b8ff"
black = "#080808"

S_U = 0.066
S_VX = 0.053
S_VY = 0.042
S_Z = 0.224
Z_TOP = 1.0
Z_AXIS = 1.20


def project(cx, by, u, v, z):
    u = np.asarray(u)
    v = np.asarray(v)
    z = np.asarray(z)
    x = cx + S_U * u - S_VX * v
    y = by - S_VY * v + S_Z * z
    return x, y


M = np.array([[S_U, -S_VX], [0.0, -S_VY]], dtype=float)
M_inv = np.linalg.inv(M)
XY_ASPECT = FIG_H / FIG_W


def glow_line(x, y, lw=1.0, alpha=0.78, zorder=5):
    ax.plot(x, y, color=light_blue, lw=6.0, alpha=0.070, solid_capstyle="round", zorder=zorder)
    ax.plot(x, y, color=blue, lw=lw, alpha=alpha, solid_capstyle="round", zorder=zorder + 0.1)



def draw_arrow(p0, p1, lw=1.35, ms=18, color=black, zorder=20, linestyle="-"):
    arr = FancyArrowPatch(
        p0, p1,
        arrowstyle="-|>",
        mutation_scale=ms,
        lw=lw,
        color=color,
        linestyle=linestyle,
        shrinkA=0,
        shrinkB=0,
        joinstyle="miter",
        capstyle="round",
        zorder=zorder,
    )
    ax.add_patch(arr)
    return arr



def projected_circle_uv(radius_screen, theta):
    target = np.vstack((radius_screen * np.cos(theta), radius_screen * np.sin(theta)))
    uv = M_inv @ target
    return uv[0], uv[1]



def draw_bowl(cx, by, ru, rv, title, x_label, y_label, formula, desc,
              title_size=19, contour_mode="quadratic", z_label=r"$p$"):
    ax.text(cx, 0.785, title, ha="center", va="center", fontsize=title_size, fontweight="bold")

    x_end = project(cx, by, 1.30, 0, 0)
    y_end = project(cx, by, 0, 1.14, 0)
    z_end = project(cx, by, 0, 0, 1.12)
    origin = project(cx, by, 0, 0, 0)

    ax.plot([origin[0], x_end[0]], [origin[1], x_end[1]], color=black, lw=1.15, alpha=0.95, zorder=9)
    ax.plot([origin[0], y_end[0]], [origin[1], y_end[1]], color=black, lw=1.15, alpha=0.95, zorder=9)
    ax.plot([origin[0], z_end[0]], [origin[1], z_end[1]], color=black, lw=1.08, alpha=0.78,
            linestyle=(0, (5, 3)), zorder=8)

    theta = np.linspace(0, 2*np.pi, 420)
    levels = np.linspace(0.045, Z_TOP, 12)

    for z0, z1 in zip(levels[:-1], levels[1:]):
        r0, r1 = np.sqrt(z0), np.sqrt(z1)

        if contour_mode == "screen_circle":
            pixel_metric = np.array([[S_U / XY_ASPECT, -S_VX / XY_ASPECT], [0.0, -S_VY]]) @ np.diag([ru, rv])
            k = float(np.mean(np.linalg.svd(pixel_metric, compute_uv=False)))
            rho1 = k * r1
            rho0 = k * r0
            x1 = cx + XY_ASPECT * rho1 * np.cos(theta)
            y1 = by + S_Z * z1 + rho1 * np.sin(theta)
            x0 = cx + XY_ASPECT * rho0 * np.cos(theta[::-1])
            y0 = by + S_Z * z0 + rho0 * np.sin(theta[::-1])
        else:
            u1, v1 = ru * r1 * np.cos(theta), rv * r1 * np.sin(theta)
            u0, v0 = ru * r0 * np.cos(theta[::-1]), rv * r0 * np.sin(theta[::-1])
            x1, y1 = project(cx, by, u1, v1, z1)
            x0, y0 = project(cx, by, u0, v0, z0)

        poly = np.c_[np.r_[x1, x0], np.r_[y1, y0]]
        alpha = 0.025 + 0.033 * z1
        ax.add_patch(Polygon(poly, closed=True, facecolor=light_blue, edgecolor="none", alpha=alpha, zorder=3 + z1))

    # Contour rings only; no faint perpendicular generatrix lines.
    for z in levels:
        r = np.sqrt(z)

        if contour_mode == "screen_circle":
            pixel_metric = np.array([[S_U / XY_ASPECT, -S_VX / XY_ASPECT], [0.0, -S_VY]]) @ np.diag([ru, rv])
            k = float(np.mean(np.linalg.svd(pixel_metric, compute_uv=False)))
            rho = k * r
            x = cx + XY_ASPECT * rho * np.cos(theta)
            y = by + S_Z * z + rho * np.sin(theta)
        else:
            u, v = ru * r * np.cos(theta), rv * r * np.sin(theta)
            x, y = project(cx, by, u, v, z)

        lw = 1.15 if z < Z_TOP else 1.35
        alpha = 0.72 if z < Z_TOP else 0.90
        glow_line(x, y, lw=lw, alpha=alpha, zorder=6 + z)

    draw_arrow(origin, x_end, lw=1.25, ms=16, zorder=20)
    draw_arrow(origin, y_end, lw=1.25, ms=16, zorder=20)
    draw_arrow(origin, z_end, lw=1.25, ms=16, zorder=20)

    ax.text(z_end[0], z_end[1] + 0.022, z_label, ha="center", va="bottom", fontsize=15)
    ax.text(x_end[0] + 0.010, x_end[1] - 0.024, x_label, ha="center", va="center", fontsize=15)
    ax.text(y_end[0] - 0.017, y_end[1] - 0.019, y_label, ha="center", va="center", fontsize=15)

    ax.text(cx, 0.212, formula, ha="center", va="center", fontsize=18)
    draw_arrow((cx, 0.121), (cx, 0.169), lw=1.25, ms=18, zorder=25)

    box_w, box_h = 0.296, 0.062
    rect = FancyBboxPatch(
        (cx - box_w/2, 0.044), box_w, box_h,
        boxstyle="round,pad=0.004,rounding_size=0.003",
        linewidth=1.05,
        edgecolor=black,
        facecolor="white",
        zorder=15,
    )
    ax.add_patch(rect)
    ax.text(cx, 0.075, desc, ha="center", va="center", fontsize=15, zorder=20)


# Top title box.
title_w, title_h = 0.585, 0.052
title_x, title_y = 0.5 - title_w/2, 0.923
rect = FancyBboxPatch(
    (title_x, title_y), title_w, title_h,
    boxstyle="round,pad=0.004,rounding_size=0.003",
    linewidth=1.05,
    edgecolor=black,
    facecolor="white",
    zorder=15,
)
ax.add_patch(rect)
ax.text(0.5, title_y + title_h/2, "CLOC: preserving learned behavior as an optimization constraint",
        ha="center", va="center", fontsize=14, zorder=20)

branch_y = 0.888
arrow_y = 0.822
panel_xs = [0.18, 0.50, 0.82]
ax.plot([0.5, 0.5], [title_y, branch_y], color=black, lw=1.05, zorder=13)
ax.plot([panel_xs[0], panel_xs[-1]], [branch_y, branch_y], color=black, lw=1.05, zorder=13)
for px in panel_xs:
    draw_arrow((px, branch_y), (px, arrow_y), lw=1.05, ms=15, zorder=14)

base_y = 0.420

draw_bowl(
    0.18, base_y,
    ru=0.62, rv=1.32,
    title="EWC (OPG)",
    x_label=r"$a_{\mathrm{poorly\ fit}}$",
    y_label=r"$a_{\mathrm{well\ fit}}$",
    formula=r"$p = \lambda(s_p(a_{\mathrm{poorly\ fit}})^2 + s_w(a_{\mathrm{well\ fit}})^2),\quad s_p \gg s_w$",
    desc="Implicitly favors high-gradient samples",
    title_size=19,
    contour_mode="quadratic",
    z_label=r"penalty $p$",
)

draw_bowl(
    0.50, base_y,
    ru=1.02, rv=1.02,
    title="Uniform IEWC",
    x_label=r"$a_1$",
    y_label=r"$a_2$",
    formula=r"$p = \lambda((a_1)^2 + (a_2)^2)$",
    desc="Estimates normalized task sensitivity",
    title_size=19,
    contour_mode="quadratic",
    z_label=r"$p$",
)

draw_bowl(
    0.82, base_y,
    ru=1.75, rv=0.56,
    title="Weighted IEWC",
    x_label=r"$a_{\mathrm{redundant}}$",
    y_label=r"$a_{\mathrm{novel}}$",
    formula=r"$p = \lambda(h_r(a_{\mathrm{redundant}})^2 + h_n(a_{\mathrm{novel}})^2),\quad h_r \ll h_n$",
    desc="Favors novel / diverse samples",
    title_size=19,
    contour_mode="quadratic",
    z_label=r"$p$",
)

for t in ax.texts:
    if t.get_fontsize() >= 18 or t.get_text().startswith("Continual"):
        t.set_path_effects([pe.withStroke(linewidth=0.25, foreground="white")])

svg_path = "/tmp/claude-1000/-home-davwis-main/b27a06be-9bbe-46ca-80d3-0dd0987adfa4/scratchpad/fig1/v9_relabeled.svg"
from pathlib import Path

out = Path(__file__).resolve().parent / "overview.pdf"
fig.savefig(out, bbox_inches="tight", pad_inches=0.02, metadata={"CreationDate": None, "ModDate": None})
