"""Pikachu and Pokeball pixel art sprites.

Design N final: eyes look RIGHT, tail on LEFT.
6 rows x 15 cols = 3 terminal lines per pikachu.
7 rows x 11 cols = 4 terminal lines per pokeball.
"""

from .palette import Y, LY, DY, BK, RD, W, PW, PR

_ = None  # transparent pixel


# ============================================================
# Pikachu sprite factory
# ============================================================

def make_pika(left_eye=(BK, W), right_eye=(BK, W),
              tail_variant=0, feet_variant=0):
    """Generate a Pikachu grid with configurable eyes, tail, feet.

    Eyes: tuple of (pupil, highlight) colors.
    Tail: 0=center, 1=shifted.
    Feet: 0=spread, 1=together.
    """
    # Tail pixel maps
    if tail_variant == 0:
        tail = {
            (1, 1): Y,
            (2, 1): Y, (2, 2): Y,
            (3, 1): Y,
            (4, 2): Y, (4, 3): Y,
            (5, 4): Y,
        }
    else:
        tail = {
            (1, 1): Y, (1, 2): Y,
            (2, 2): Y,
            (3, 1): Y, (3, 2): Y,
            (4, 2): Y,
            (5, 4): Y,
        }

    # Feet pixel maps
    if feet_variant == 0:
        feet = {(5, 7): DY, (5, 11): DY}
    else:
        feet = {(5, 8): DY, (5, 10): DY}

    # Build 6x15 grid
    grid = [[None] * 15 for _ in range(6)]

    # Ears
    grid[0][5] = BK; grid[0][6] = Y; grid[0][12] = Y; grid[0][13] = BK

    # Head
    for c in range(6, 13):
        grid[1][c] = Y

    # Eyes row
    grid[2][5] = Y; grid[2][6] = Y
    grid[2][7] = left_eye[0]; grid[2][8] = left_eye[1]
    grid[2][9] = Y
    grid[2][10] = right_eye[0]; grid[2][11] = right_eye[1]
    grid[2][12] = Y; grid[2][13] = Y

    # Cheeks
    grid[3][5] = Y; grid[3][6] = RD; grid[3][7] = RD; grid[3][8] = Y
    grid[3][9] = Y; grid[3][10] = Y
    grid[3][11] = RD; grid[3][12] = RD; grid[3][13] = Y

    # Body
    for c in range(6, 13):
        grid[4][c] = Y

    # Apply tail, feet
    for (r, c), color in tail.items():
        grid[r][c] = color
    for (r, c), color in feet.items():
        grid[r][c] = color

    return grid


# ============================================================
# Pokeball sprite factory
# ============================================================

def _shift_row(row, n):
    """Shift row contents by n pixels. Positive=right, negative=left."""
    if n == 0:
        return row[:]
    if n > 0:
        return [None] * n + row[:-n]
    else:
        return row[-n:] + [None] * (-n)


def make_pokeball(tilt=0):
    """Generate a Pokeball grid (7 rows x 11 cols).

    Wobble: bottom-pivot physics. Top rows shift ±1px, bottom stays fixed.
    """
    base = [
        [_,  _,  _,  BK, BK, BK, BK, BK, _,  _,  _],   # 0: top curve
        [_,  BK, PR, PR, PR, PR, PR, PR, PR, BK, _],     # 1: red
        [BK, PR, PR, PR, PR, BK, PR, PR, PR, PR, BK],    # 2: red + btn top
        [BK, BK, BK, BK, BK, W,  BK, BK, BK, BK, BK],   # 3: band + button
        [BK, PW, PW, PW, PW, BK, PW, PW, PW, PW, BK],    # 4: white + btn bot
        [_,  BK, PW, PW, PW, PW, PW, PW, PW, BK, _],     # 5: white
        [_,  _,  _,  BK, BK, BK, BK, BK, _,  _,  _],     # 6: bottom curve
    ]

    if tilt == 0:
        return base

    # Bottom-pivot: rows 0-3 shift, rows 4-6 stay
    shift_amounts = [1, 1, 1, 1, 0, 0, 0]
    direction = tilt
    return [_shift_row(row, direction * shift_amounts[r])
            for r, row in enumerate(base)]


# ============================================================
# Pre-built animation frame sets
# ============================================================

# --- Thinking: eyes glance left <-> right ---
THINK_FRAMES = [
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
    make_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0),
    make_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
]

# --- Streaming: one eye wink ---
STREAM_FRAMES = [
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
    make_pika(left_eye=(BK, W), right_eye=(Y, DY), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(Y, DY), tail_variant=1),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
]

# --- Tool Use: standard pose, effects via decoration ---
TOOL_FRAMES = [
    make_pika(tail_variant=0, feet_variant=0),
    make_pika(tail_variant=1, feet_variant=1),
    make_pika(tail_variant=0, feet_variant=0),
    make_pika(tail_variant=1, feet_variant=1),
]

# --- Subagent: standard pose, hearts via decoration ---
SUBAGENT_FRAMES = [
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0),
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1),
]

# --- Compacting: eyes closed, sleeping ---
COMPACT_FRAME = make_pika(
    left_eye=(Y, DY), right_eye=(Y, DY),
    tail_variant=0, feet_variant=0,
)

# --- Rate Limited: Pokeball wobble (pendulum easing) ---
_B0 = make_pokeball(tilt=0)
_BR = make_pokeball(tilt=1)
_BL = make_pokeball(tilt=-1)
BALL_FRAMES = [
    _BR, _BR,    # lean right (hold)
    _B0,          # pass through center
    _BL, _BL,    # lean left (hold)
    _B0,          # pass through center
]
