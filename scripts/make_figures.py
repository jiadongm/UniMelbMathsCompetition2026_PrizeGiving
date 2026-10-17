"""Draw the illustrative SVG figures for the prize-giving deck.

Every figure here is a deliberately simplified, invented illustration.
Run from the project root: python3 scripts/make_figures.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figs"
OUT.mkdir(exist_ok=True)

INK = "#24333d"
MUTED = "#60737e"
LINE = "#4a5a64"
CELL_FILL = "#f1ecf8"
CELL_EDGE = "#7a5ea8"
NUCLEUS = "#8f74c0"
STEM_FILL = "#d9eef1"
STEM_EDGE = "#236779"
ORANGE = "#e07b2c"
GREY = "#c3ccd2"
FONT = "Helvetica Neue, Arial, sans-serif"

# Lineage marks: colour plus shape, so they never rely on colour alone.
MARKS = {
    "blue": ("#2f6fdf", "circle"),
    "orange": (ORANGE, "triangle"),
    "green": ("#2a9d5c", "square"),
    "purple": ("#8e5bd0", "star"),
    "pink": ("#d9467a", "diamond"),
}


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="{FONT}">\n{body}\n</svg>\n')


def text(x, y, s, size=28, fill=INK, anchor="middle", weight="normal", style=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" {style}>{s}</text>')


def white_cell(x, y, r):
    """A white blood cell: pale body with a round nucleus."""
    k = r / 50
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CELL_FILL}" '
            f'stroke="{CELL_EDGE}" stroke-width="{max(2, 3 * k):.1f}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.5:.1f}" fill="{NUCLEUS}"/>')


def stem_cell(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STEM_FILL}" stroke="{STEM_EDGE}" stroke-width="4"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.45:.1f}" fill="{STEM_EDGE}" opacity="0.75"/>')


def mark(name, x, y, s=18):
    colour, shape = MARKS[name]
    stroke = 'stroke="white" stroke-width="3"'
    if shape == "circle":
        return f'<circle cx="{x}" cy="{y}" r="{s}" fill="{colour}" {stroke}/>'
    if shape == "square":
        return f'<rect x="{x - s * 0.9}" y="{y - s * 0.9}" width="{s * 1.8}" height="{s * 1.8}" rx="3" fill="{colour}" {stroke}/>'
    if shape == "triangle":
        pts = f"{x},{y - s * 1.15} {x + s * 1.1},{y + s * 0.8} {x - s * 1.1},{y + s * 0.8}"
        return f'<polygon points="{pts}" fill="{colour}" {stroke}/>'
    if shape == "diamond":
        pts = f"{x},{y - s * 1.25} {x + s},{y} {x},{y + s * 1.25} {x - s},{y}"
        return f'<polygon points="{pts}" fill="{colour}" {stroke}/>'
    if shape == "star":
        import math
        pts = []
        for i in range(10):
            rad = s * 1.3 if i % 2 == 0 else s * 0.55
            a = -math.pi / 2 + i * math.pi / 5
            pts.append(f"{x + rad * math.cos(a):.1f},{y + rad * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{colour}" {stroke}/>'
    raise ValueError(shape)


def path(d, colour=LINE, width=5):
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


# Opening slide: a human family tree ----------------------------------------
KIN = "#5a9fad"       # blood relatives
IN_LAW = "#c3ccd2"    # partners who married in


def person(x, y, fill, s=1.0):
    """A simple person icon centred on (x, y)."""
    head = f'<circle cx="{x}" cy="{y - 26 * s:.1f}" r="{19 * s:.1f}" fill="{fill}"/>'
    body = (f'<path d="M{x - 30 * s:.1f},{y + 34 * s:.1f} V{y + 10 * s:.1f} '
            f'Q{x - 30 * s:.1f},{y - 4 * s:.1f} {x - 14 * s:.1f},{y - 4 * s:.1f} H{x + 14 * s:.1f} '
            f'Q{x + 30 * s:.1f},{y - 4 * s:.1f} {x + 30 * s:.1f},{y + 10 * s:.1f} V{y + 34 * s:.1f} Z" fill="{fill}"/>')
    return head + body


def fig_human_tree():
    W, H = 1030, 560
    s = 1.25                           # person size
    g1, g2, g3 = 70, 270, 460          # centre y of each generation
    gp = (440, 560)                    # grandparents
    par_partner, par = 120, 240        # your parents
    aunt, aunt_partner = 760, 880      # aunt and uncle
    kids_l, kids_r = (100, 260), (740, 900)
    neck = 56                          # head top above centre
    body = []
    # couple lines
    for a, b, y in [(gp[0], gp[1], g1), (par_partner, par, g2), (aunt, aunt_partner, g2)]:
        body.append(path(f"M{a + 40},{y + 8} H{b - 40}", LINE, 4))
    # grandparents to their two children
    gmid, bar1 = sum(gp) / 2, g1 + 115
    body.append(path(f"M{gmid},{g1 + 8} V{bar1} M{par},{bar1} H{aunt} "
                     f"M{par},{bar1} V{g2 - neck} M{aunt},{bar1} V{g2 - neck}", LINE, 4))
    # each couple to their children
    for (a, b), (k1, k2) in [((par_partner, par), kids_l), ((aunt, aunt_partner), kids_r)]:
        mid, bar2 = (a + b) / 2, g2 + 105
        body.append(path(f"M{mid},{g2 + 8} V{bar2} M{k1},{bar2} H{k2} "
                         f"M{k1},{bar2} V{g3 - neck} M{k2},{bar2} V{g3 - neck}", LINE, 4))
    for x in gp:
        body.append(person(x, g1, KIN, s))
    body.append(person(par_partner, g2, IN_LAW, s))
    body.append(person(par, g2, KIN, s))
    body.append(person(aunt, g2, KIN, s))
    body.append(person(aunt_partner, g2, IN_LAW, s))
    body.append(person(kids_l[0], g3, STEM_EDGE, s))
    body.append(person(kids_l[1], g3, KIN, s))
    for x in kids_r:
        body.append(person(x, g3, KIN, s))
    # labels sit beside or above each couple, clear of the lines
    body.append(text(gp[1] + 50, g1 + 12, "Grandparents", 36, INK, "start"))
    body.append(text(par_partner, g2 - 70, "Parents", 36, INK))
    body.append(text(aunt_partner + 20, g2 - 70, "Aunt &amp; uncle", 36, INK))
    body.append(text(kids_l[0], g3 + 82, "You", 38, STEM_EDGE, weight="bold"))
    body.append(text(kids_l[1], g3 + 82, "Sibling", 36, INK))
    body.append(text(kids_r[0], g3 + 82, "Cousin", 36, INK))
    body.append(text(kids_r[1], g3 + 82, "Cousin", 36, INK))
    return svg(W, H, "\n".join(body))


# Slide 1: look-alike white blood cells -------------------------------------
def fig_lookalikes():
    xs = [110, 300, 490, 680, 870, 1060]
    ys = [130, 175, 120, 170, 125, 165]
    body = "".join(white_cell(x, y, 72) for x, y in zip(xs, ys))
    return svg(1170, 280, body)


# Slide 2: one blood-making cell, a whole family ------------------------------
def fig_family():
    W, H = 1170, 520
    leaves = 16
    left, right = 70, 1100
    step = (right - left) / (leaves - 1)
    xs = [left + i * step for i in range(leaves)]
    levels = [70, 165, 255, 340, 420]   # y of root, then each split
    leaf_y = 462
    family = set(range(4, 8))          # the 4 leaves below the marked branch
    body = []
    # highlight the cell family
    fx0, fx1 = xs[4] - 36, xs[7] + 36
    body.append(f'<rect x="{fx0}" y="{levels[2] + 20}" width="{fx1 - fx0}" height="{leaf_y + 38 - levels[2] - 20}" '
                f'rx="22" fill="#fdf0e5" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="10 7"/>')

    def node_x(level, idx):
        span = leaves // (2 ** level)
        return sum(xs[idx * span:(idx + 1) * span]) / span

    for level in range(4):
        for idx in range(2 ** level):
            x = node_x(level, idx)
            y = levels[level] + (40 if level == 0 else 0)
            xl, xr = node_x(level + 1, 2 * idx), node_x(level + 1, 2 * idx + 1)
            ny = levels[level + 1] if level < 3 else leaf_y - 26
            in_fam = level >= 2 and (idx * 2 ** (4 - level)) in range(4, 8)
            col = ORANGE if in_fam else LINE
            body.append(path(f"M{x},{y} V{levels[level + 1] - 40 if level < 3 else levels[4]} ", col, 4))
            ytop = levels[level + 1] - 40 if level < 3 else levels[4]
            body.append(path(f"M{xl},{ny} V{ytop} H{xr} V{ny}", col, 4))
    body.append(stem_cell(node_x(0, 0), levels[0], 40))
    for i, x in enumerate(xs):
        body.append(white_cell(x, leaf_y, 26))
        if i in family:
            body.append(mark("orange", x, leaf_y - 46, 9))
    # the DNA typo happens once, on one branch
    mx = node_x(2, 1)
    body.append(mark("orange", mx, levels[2] - 48 + 60, 17))
    # large labels, so they stay readable when the figure is shown small;
    # the typo label sits in the clear band between the first two splits
    body.append(text(node_x(0, 0) + 58, levels[0] + 17, "blood-making cell", 50, STEM_EDGE, "start", "bold"))
    body.append(text(mx + 34, levels[1] + 36, "a DNA typo", 50, ORANGE, "start", "bold"))
    body.append(path(f"M{mx + 30},{levels[1] + 46} L{mx + 10},{levels[2] - 6}", ORANGE, 4))
    return svg(W, H + 10, "\n".join(body))


# Slides 3: the tree puzzle -------------------------------------------------
CELLS = {
    "A": ["blue", "orange"],
    "B": ["blue", "orange", "purple"],
    "C": ["blue", "green"],
    "D": ["blue", "green", "pink"],
}
PUZ_X = {"A": 190, "B": 440, "C": 730, "D": 980}


def fig_puzzle(with_tree):
    W, H = 1170, 535
    cell_y, label_y, marks_y = 345, 445, 505
    body = []
    if with_tree:
        root_x = (PUZ_X["A"] + PUZ_X["D"]) / 2
        lx = (PUZ_X["A"] + PUZ_X["B"]) / 2
        rx = (PUZ_X["C"] + PUZ_X["D"]) / 2
        top, split1, split2, leaf_top = 15, 85, 170, cell_y - 72
        body.append(path(f"M{root_x},{top} V{split1}"))
        body.append(path(f"M{lx},{split2} V{split1} H{rx} V{split2}"))
        body.append(path(f"M{PUZ_X['A']},{leaf_top} V{split2} H{PUZ_X['B']} V{leaf_top}"))
        body.append(path(f"M{PUZ_X['C']},{leaf_top} V{split2} H{PUZ_X['D']} V{leaf_top}"))
        body.append(mark("blue", root_x, (top + split1) / 2 + 6, 17))
        body.append(mark("orange", lx, (split1 + split2) / 2, 17))
        body.append(mark("green", rx, (split1 + split2) / 2, 17))
        body.append(mark("purple", PUZ_X["B"], (split2 + leaf_top) / 2, 17))
        body.append(mark("pink", PUZ_X["D"], (split2 + leaf_top) / 2, 17))
        body.append(text(root_x + 34, 60, "shared by all", 24, MUTED, "start"))
        body.append(text(PUZ_X["D"] + 32, (split2 + leaf_top) / 2 + 8, "only D", 24, MUTED, "start"))
        body.append(text(PUZ_X["B"] + 32, (split2 + leaf_top) / 2 + 8, "only B", 24, MUTED, "start"))
    for name, x in PUZ_X.items():
        body.append(white_cell(x, cell_y, 70))
        body.append(text(x, label_y + 10, name, 46, INK, weight="bold"))
        ms = CELLS[name]
        x0 = x - (len(ms) - 1) * 26
        for i, m in enumerate(ms):
            body.append(mark(m, x0 + i * 52, marks_y, 18))
    return svg(W, H, "\n".join(body))


# Bridge slide: younger versus older family trees ---------------------------
# Leaves are "s" (a family of one) or a family letter; big families in colour.
YOUNG_LEAVES = "s" * 24
OLD_LEAVES = "ss" + "O" * 5 + "sss" + "G" * 3 + "ssss" + "B" * 2 + "sssss"
FAMILY_STYLE = {   # line colour, box fill, y of the family's split
    "O": (ORANGE, "#fdf0e5", 215),
    "G": ("#2a9d5c", "#e6f4ec", 245),
    "B": ("#2f6fdf", "#e7effc", 270),
}


def tree_panel(x0, leaves, title, caption):
    gap, leaf_y, bar_y, r = 20.5, 382, 100, 8
    xs = [x0 + i * gap for i in range(len(leaves))]
    mid = (xs[0] + xs[-1]) / 2
    body = [text(mid, 36, title, 30, INK, weight="bold")]
    groups = []   # (label, [x, ...]) in leaf order
    for x, lab in zip(xs, leaves):
        if lab != "s" and groups and groups[-1][0] == lab:
            groups[-1][1].append(x)
        else:
            groups.append((lab, [x]))
    for lab, gx in groups:
        if lab == "s":
            continue
        _, fill, _ = FAMILY_STYLE[lab]
        body.append(f'<rect x="{gx[0] - 14}" y="{FAMILY_STYLE[lab][2] - 18}" width="{gx[-1] - gx[0] + 28}" '
                    f'height="{leaf_y + 22 - FAMILY_STYLE[lab][2] + 18}" rx="12" fill="{fill}"/>')
    tops = [sum(gx) / len(gx) for _, gx in groups]
    body.append(path(f"M{mid},70 V{bar_y}", LINE, 3))
    body.append(path(f"M{min(tops)},{bar_y} H{max(tops)}", LINE, 3))
    for (lab, gx), tx in zip(groups, tops):
        if lab == "s":
            body.append(path(f"M{tx},{bar_y} V{leaf_y - r}", LINE, 3))
            continue
        col, _, split_y = FAMILY_STYLE[lab]
        body.append(path(f"M{tx},{bar_y} V{split_y}", col, 4))
        body.append(path(f"M{gx[0]},{leaf_y - r} V{split_y} H{gx[-1]} V{leaf_y - r}", col, 4))
        for x in gx[1:-1]:
            body.append(path(f"M{x},{split_y} V{leaf_y - r}", col, 4))
    body += [white_cell(x, leaf_y, r) for x in xs]
    body.append(text(mid, 440, caption, 26, MUTED))
    return body


def fig_young_old():
    W, H = 1170, 460
    body = [text(32, 82, "birth", 20, MUTED), text(32, 392, "now", 20, MUTED),
            '<defs><marker id="tarr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>',
            f'<path d="M32,98 V362" stroke="{MUTED}" stroke-width="3" marker-end="url(#tarr)"/>']
    body += tree_panel(90, YOUNG_LEAVES, "Younger adult", "many small families share the work")
    body += tree_panel(660, OLD_LEAVES, "Over 75", "a few big families make much of the blood")
    return svg(W, H, "\n".join(body))


# Evolutionary game: computer runs of a simple model ------------------------
def moran_runs(runs=20, N=100, r=1.1, rounds=80, seed=11):
    """Each run starts with one cell carrying a helpful typo among N cells.

    Each step one cell is lost (chosen at random) and replaced by a copy of
    another, chosen in proportion to fitness (r for typo cells, 1 otherwise).
    A round is N steps. Returns the typo family's share after each round.
    Seed 11 gives 2 takeovers in 20 runs, close to the expected 1.8.
    """
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(runs):
        k, traj = 1, [1 / N]
        for _ in range(rounds):
            for _ in range(N):
                if k in (0, N):
                    break
                born = rng.random() < r * k / (r * k + N - k)
                lost = rng.random() < k / N
                k += born - lost
            traj.append(k / N)
        out.append(traj)
    return out


def fig_game():
    W, H = 760, 540
    x0, x1, y0, y1 = 120, 730, 470, 40   # plot area (y0 = 0%, y1 = 100%)
    runs = moran_runs()
    n = len(runs[0]) - 1
    X = lambda t: x0 + (x1 - x0) * t / n
    Y = lambda v: y0 - (y0 - y1) * v
    body = [path(f"M{x0},{y1} V{y0} H{x1}", MUTED, 3)]
    for v, lab in [(0, "0%"), (0.5, "50%"), (1, "100%")]:
        body.append(text(x0 - 14, Y(v) + 10, lab, 28, MUTED, "end"))
        if v:
            body.append(f'<path d="M{x0},{Y(v)} H{x1}" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 8"/>')
    body.append(text((x0 + x1) / 2, H - 18, "time →", 28, MUTED))
    body.append(text(30, (y0 + y1) / 2, "share of the blood", 28, MUTED,
                     style=f'transform="rotate(-90 30 {(y0 + y1) / 2})"'))
    losers = [t for t in runs if t[-1] == 0]
    winners = [t for t in runs if t[-1] > 0]
    for t in losers + winners:
        end = next((i for i, v in enumerate(t) if v == 0), n)
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(t[:end + 1]))
        col, w = (ORANGE, 6) if t in winners else ("#6f7d86", 4)
        body.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" '
                    f'stroke-linejoin="round" stroke-linecap="round"/>')
    # labels sit in empty parts of the plot: top left and lower right
    body.append(text(x0 + 24, Y(0.86), f"{len(winners)} took over", 34, ORANGE, "start", "bold"))
    body.append(text(x0 + 250, Y(0.1), f"{len(losers)} vanished", 34, "#5d6b74", "start", "bold"))
    return svg(W, H, "\n".join(body))


# Slide 6: the research loop ------------------------------------------------
def fig_loop():
    W, H = 640, 560
    cx, cy = 320, 280
    boxes = [
        (cx, 70, ["Look at", "the clues"]),
        (cx + 205, cy, ["Guess", "the rules"]),
        (cx, 490, ["Run the rules", "forward"]),
        (cx - 205, cy, ["Check:", "does it match?"]),
    ]
    body = [
        '<defs><marker id="arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{STEM_EDGE}"/></marker></defs>'
    ]
    # curved arrows between boxes, clockwise
    arcs = [
        (cx + 115, 92, cx + 215, cy - 72),
        (cx + 215, cy + 72, cx + 125, 470),
        (cx - 125, 470, cx - 215, cy + 72),
        (cx - 215, cy - 72, cx - 115, 92),
    ]
    for x0, y0, x1, y1 in arcs:
        body.append(f'<path d="M{x0},{y0} A230,230 0 0 1 {x1},{y1}" fill="none" stroke="{STEM_EDGE}" '
                    f'stroke-width="5" marker-end="url(#arr)"/>')
    for x, y, lines in boxes:
        body.append(f'<rect x="{x - 112}" y="{y - 58}" width="224" height="116" rx="18" '
                    f'fill="{STEM_FILL}" stroke="{STEM_EDGE}" stroke-width="3"/>')
        for j, s in enumerate(lines):
            body.append(text(x, y - 8 + j * 36, s, 29, INK, weight="bold"))
    body.append(text(cx, cy - 6, "keep the", 25, MUTED))
    body.append(text(cx, cy + 26, "explanations", 25, MUTED))
    body.append(text(cx, cy + 58, "that fit", 25, MUTED))
    return svg(W, H, "\n".join(body))


FIGS = {
    "human-tree.svg": fig_human_tree(),
    "lookalikes.svg": fig_lookalikes(),
    "family.svg": fig_family(),
    "puzzle.svg": fig_puzzle(False),
    "puzzle-tree.svg": fig_puzzle(True),
    "young-old.svg": fig_young_old(),
    "game.svg": fig_game(),
    "loop.svg": fig_loop(),
}

for name, content in FIGS.items():
    (OUT / name).write_text(content)
    print("wrote", OUT / name)
