"""Pikachu and Pokeball pixel art sprites.

Design N final: eyes look RIGHT, tail on LEFT.
6 rows x 15 cols = 3 terminal lines per pikachu.
7 rows x 11 cols = 4 terminal lines per pokeball.

Reaction sprites:
  IDLE_FRAMES   — subtle life cycle (normal + occasional glance)
  THINKING_SP   — glancing, tail raised, alert
  STAGING_SP    — same as thinking (alert but softer via decoration)
  COMMITTED_SP  — winking, tail raised, proud
  RECOVERED_SP  — normal, relaxed
  HIT_SP        — eyes closed (pain squint)
  COMPACTED_SP  — eyes closed (sleeping)
  BALL_FRAMES   — pokeball wobble (faint/ratelimited)
"""

from .palette import Y, LY, DY, BK, RD, W, PW, PR, OR, BR, SY, SLY, SDY, SRD, SOR, SLY2, SOR2

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
# Pichu sprite factory — smaller, cuter, no red cheeks
# ============================================================

def make_pichu(left_eye=(BK, W), right_eye=(BK, W),
               tail_variant=0, feet_variant=0):
    """Generate a Pichu grid — baby Pokemon, big eyes, no cheeks.

    Pichu is the pre-evolution: very small, big round eyes,
    no red cheeks, tiny rounded ears. Much cuter and smaller than Pikachu.
    """
    # Tail pixel maps (small tail on left side, like baby Pikachu)
    if tail_variant == 0:
        tail = {
            (1, 1): Y,
            (2, 1): Y, (2, 2): Y,
            (3, 1): Y,
        }
    else:
        tail = {
            (1, 1): Y, (1, 2): Y,
            (2, 2): Y,
            (3, 1): Y, (3, 2): Y,
        }

    # Feet pixel maps
    if feet_variant == 0:
        feet = {(5, 7): DY, (5, 11): DY}
    else:
        feet = {(5, 8): DY, (5, 10): DY}

    # Build 6x15 grid
    grid = [[None] * 15 for _ in range(6)]

    # Ears — Pichu has tiny round ears (black tips + yellow)
    grid[0][5] = BK; grid[0][6] = Y
    grid[0][11] = Y; grid[0][12] = BK

    # Head — Pichu has a big round head (cols 6-12)
    for c in range(6, 13):
        grid[1][c] = Y

    # Eyes row — BIG EYES! That's Pichu's main characteristic
    # Left eye
    grid[2][5] = Y; grid[2][6] = Y; grid[2][7] = Y
    grid[2][8] = left_eye[0]; grid[2][9] = left_eye[1]
    # Right eye
    grid[2][10] = Y
    grid[2][11] = right_eye[0]; grid[2][12] = right_eye[1]; grid[2][13] = Y

    # Cheeks row — Pichu has YELLOW cheeks (no red yet!)
    for c in range(5, 14):
        grid[3][c] = Y

    # Body — slightly smaller than Pikachu (cols 6-12)
    for c in range(6, 13):
        grid[4][c] = Y

    # Apply tail, feet
    for (r, c), color in tail.items():
        grid[r][c] = color
    for (r, c), color in feet.items():
        grid[r][c] = color

    return grid


# ============================================================
# Raichu sprite factory — evolved form, orange palette, sleek
# ============================================================

def make_raichu(left_eye=(BK, W), right_eye=(BK, W),
                tail_variant=0, feet_variant=0):
    """Generate a Raichu grid — sleek orange body, long pointed ears, lightning tail.

    Raichu is the evolved form: orange (not yellow), longer body,
    distinctive lightning bolt tail, elegant pointed ears.
    """
    # Tail pixel maps (lightning bolt style)
    if tail_variant == 0:
        tail = {
            (0, 1): OR,
            (1, 2): OR,
            (2, 1): OR, (2, 2): OR,
            (3, 1): OR,
            (4, 2): OR,
            (5, 3): OR,
        }
    else:
        tail = {
            (0, 1): OR, (0, 2): OR,
            (1, 1): OR,
            (2, 1): OR, (2, 2): OR,
            (3, 2): OR,
            (4, 1): OR,
            (5, 2): OR,
        }

    # Feet pixel maps
    if feet_variant == 0:
        feet = {(5, 7): DY, (5, 11): DY}
    else:
        feet = {(5, 8): DY, (5, 10): DY}

    # Build 6x15 grid
    grid = [[None] * 15 for _ in range(6)]

    # Ears — longer, pointed, orange with red tips
    grid[0][4] = RD; grid[0][5] = OR; grid[0][6] = OR
    grid[0][11] = OR; grid[0][12] = OR; grid[0][13] = RD

    # Head — sleek, slightly narrower
    for c in range(5, 13):
        grid[1][c] = OR

    # Eyes row
    grid[2][4] = OR; grid[2][5] = OR; grid[2][6] = OR
    grid[2][7] = left_eye[0]; grid[2][8] = left_eye[1]
    grid[2][9] = OR
    grid[2][10] = right_eye[0]; grid[2][11] = right_eye[1]
    grid[2][12] = OR; grid[2][13] = OR

    # Cheeks — same red cheeks as Pikachu (Raichu has them too)
    grid[3][5] = OR; grid[3][6] = RD; grid[3][7] = RD; grid[3][8] = OR
    grid[3][9] = OR; grid[3][10] = OR
    grid[3][11] = RD; grid[3][12] = RD; grid[3][13] = OR

    # Body — sleek orange
    for c in range(5, 13):
        grid[4][c] = OR

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
# Reaction sprites
# ============================================================

# --- Idle: subtle life cycle (frame % 3) ---
IDLE_FRAMES = [
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),  # normal
    make_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),  # glancing
    make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),  # tail sway
]

# --- Thinking: focused, alert ---
THINKING_SP = make_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)

# --- Staging: alert (same sprite as thinking, differentiated by decoration) ---
STAGING_SP = THINKING_SP

# --- Committed: winking, proud ---
COMMITTED_SP = make_pika(left_eye=(BK, W), right_eye=(Y, DY), tail_variant=1, feet_variant=0)

# --- Recovered: normal, relaxed ---
RECOVERED_SP = make_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)

# --- Hit: eyes closed (pain) ---
HIT_SP = make_pika(left_eye=(Y, DY), right_eye=(Y, DY), tail_variant=0, feet_variant=1)

# --- Compacted: eyes closed (sleeping) ---
COMPACTED_SP = make_pika(left_eye=(Y, DY), right_eye=(Y, DY), tail_variant=0, feet_variant=0)

# --- Faint: Pokeball wobble ---
_B0 = make_pokeball(tilt=0)
_BR = make_pokeball(tilt=1)
_BL = make_pokeball(tilt=-1)
BALL_FRAMES = [
    _BR, _BR,    # lean right (hold)
    _B0,          # pass through center
    _BL, _BL,    # lean left (hold)
    _B0,          # pass through center
]


# ============================================================
# Backwards-compat aliases (used by demo.py / animator.py)
# ============================================================

THINK_FRAMES = IDLE_FRAMES
COMPACT_FRAME = COMPACTED_SP


# ============================================================
# Shiny Pikachu variants (Feature 3: 1/500 per session)
# ============================================================

def make_shiny_pika(left_eye=(BK, W), right_eye=(BK, W),
                    tail_variant=0, feet_variant=0):
    """Shiny Pikachu — orange palette swap, like the games."""
    # Reuse make_pika but patch colors after generation
    grid = make_pika(left_eye, right_eye, tail_variant, feet_variant)
    # Swap palette: Y→SY, LY→SLY, DY→SDY, RD→SRD
    COLOR_MAP = {Y: SY, LY: SLY, DY: SDY, RD: SRD}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] in COLOR_MAP:
                grid[r][c] = COLOR_MAP[grid[r][c]]
    return grid


SHINY_IDLE_FRAMES = [
    make_shiny_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),
    make_shiny_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),
    make_shiny_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),
]

SHINY_THINKING_SP = make_shiny_pika(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)
SHINY_STAGING_SP = SHINY_THINKING_SP
SHINY_COMMITTED_SP = make_shiny_pika(left_eye=(BK, W), right_eye=(SY, SDY), tail_variant=1, feet_variant=0)
SHINY_RECOVERED_SP = make_shiny_pika(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)
SHINY_HIT_SP = make_shiny_pika(left_eye=(SY, SDY), right_eye=(SY, SDY), tail_variant=0, feet_variant=1)
SHINY_COMPACTED_SP = make_shiny_pika(left_eye=(SY, SDY), right_eye=(SY, SDY), tail_variant=0, feet_variant=0)


# ============================================================
# Pichu reaction sprites
# ============================================================

PICHU_IDLE_FRAMES = [
    make_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),
    make_pichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),
    make_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),
]

PICHU_THINKING_SP = make_pichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)
PICHU_STAGING_SP = PICHU_THINKING_SP
PICHU_COMMITTED_SP = make_pichu(left_eye=(BK, W), right_eye=(Y, DY), tail_variant=1, feet_variant=0)
PICHU_RECOVERED_SP = make_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)
PICHU_HIT_SP = make_pichu(left_eye=(Y, DY), right_eye=(Y, DY), tail_variant=0, feet_variant=1)
PICHU_COMPACTED_SP = make_pichu(left_eye=(Y, DY), right_eye=(Y, DY), tail_variant=0, feet_variant=0)


# ============================================================
# Raichu reaction sprites
# ============================================================

RAICHU_IDLE_FRAMES = [
    make_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),
    make_raichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),
    make_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),
]

RAICHU_THINKING_SP = make_raichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)
RAICHU_STAGING_SP = RAICHU_THINKING_SP
RAICHU_COMMITTED_SP = make_raichu(left_eye=(BK, W), right_eye=(OR, DY), tail_variant=1, feet_variant=0)
RAICHU_RECOVERED_SP = make_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)
RAICHU_HIT_SP = make_raichu(left_eye=(OR, DY), right_eye=(OR, DY), tail_variant=0, feet_variant=1)
RAICHU_COMPACTED_SP = make_raichu(left_eye=(OR, DY), right_eye=(OR, DY), tail_variant=0, feet_variant=0)


# ============================================================
# Shiny Pichu variants
# ============================================================

def make_shiny_pichu(left_eye=(BK, W), right_eye=(BK, W),
                     tail_variant=0, feet_variant=0):
    """Shiny Pichu — same as regular (already yellowish)."""
    grid = make_pichu(left_eye, right_eye, tail_variant, feet_variant)
    # Swap palette: Y→SY, LY→SLY, DY→SDY
    COLOR_MAP = {Y: SY, LY: SLY, DY: SDY}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] in COLOR_MAP:
                grid[r][c] = COLOR_MAP[grid[r][c]]
    return grid


SHINY_PICHU_IDLE_FRAMES = [
    make_shiny_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),
    make_shiny_pichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),
    make_shiny_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),
]

SHINY_PICHU_THINKING_SP = make_shiny_pichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)
SHINY_PICHU_STAGING_SP = SHINY_PICHU_THINKING_SP
SHINY_PICHU_COMMITTED_SP = make_shiny_pichu(left_eye=(BK, W), right_eye=(SY, SDY), tail_variant=1, feet_variant=0)
SHINY_PICHU_RECOVERED_SP = make_shiny_pichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)
SHINY_PICHU_HIT_SP = make_shiny_pichu(left_eye=(SY, SDY), right_eye=(SY, SDY), tail_variant=0, feet_variant=1)
SHINY_PICHU_COMPACTED_SP = make_shiny_pichu(left_eye=(SY, SDY), right_eye=(SY, SDY), tail_variant=0, feet_variant=0)


# ============================================================
# Shiny Raichu variants
# ============================================================

def make_shiny_raichu(left_eye=(BK, W), right_eye=(BK, W),
                      tail_variant=0, feet_variant=0):
    """Shiny Raichu — golden/tan palette swap."""
    grid = make_raichu(left_eye, right_eye, tail_variant, feet_variant)
    # Swap palette: OR→SOR, LY→SLY2, DY→SOR2
    COLOR_MAP = {OR: SOR, LY: SLY2, DY: SOR2}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] in COLOR_MAP:
                grid[r][c] = COLOR_MAP[grid[r][c]]
    return grid


SHINY_RAICHU_IDLE_FRAMES = [
    make_shiny_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1),
    make_shiny_raichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=0, feet_variant=1),
    make_shiny_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=1, feet_variant=1),
]

SHINY_RAICHU_THINKING_SP = make_shiny_raichu(left_eye=(W, BK), right_eye=(W, BK), tail_variant=1, feet_variant=0)
SHINY_RAICHU_STAGING_SP = SHINY_RAICHU_THINKING_SP
SHINY_RAICHU_COMMITTED_SP = make_shiny_raichu(left_eye=(BK, W), right_eye=(SOR, SOR2), tail_variant=1, feet_variant=0)
SHINY_RAICHU_RECOVERED_SP = make_shiny_raichu(left_eye=(BK, W), right_eye=(BK, W), tail_variant=0, feet_variant=1)
SHINY_RAICHU_HIT_SP = make_shiny_raichu(left_eye=(SOR, SOR2), right_eye=(SOR, SOR2), tail_variant=0, feet_variant=1)
SHINY_RAICHU_COMPACTED_SP = make_shiny_raichu(left_eye=(SOR, SOR2), right_eye=(SOR, SOR2), tail_variant=0, feet_variant=0)


# ============================================================
# Pokemon species registry — maps species key to sprites
# ============================================================

POKEMON_SPECIES = {
    "pichu": {
        "name": "Pichu",
        "idle_frames": PICHU_IDLE_FRAMES,
        "thinking": PICHU_THINKING_SP,
        "staging": PICHU_STAGING_SP,
        "committed": PICHU_COMMITTED_SP,
        "recovered": PICHU_RECOVERED_SP,
        "hit": PICHU_HIT_SP,
        "compacted": PICHU_COMPACTED_SP,
        "shiny_idle_frames": SHINY_PICHU_IDLE_FRAMES,
        "shiny_thinking": SHINY_PICHU_THINKING_SP,
        "shiny_staging": SHINY_PICHU_STAGING_SP,
        "shiny_committed": SHINY_PICHU_COMMITTED_SP,
        "shiny_recovered": SHINY_PICHU_RECOVERED_SP,
        "shiny_hit": SHINY_PICHU_HIT_SP,
        "shiny_compacted": SHINY_PICHU_COMPACTED_SP,
    },
    "pikachu": {
        "name": "Pikachu",
        "idle_frames": IDLE_FRAMES,
        "thinking": THINKING_SP,
        "staging": STAGING_SP,
        "committed": COMMITTED_SP,
        "recovered": RECOVERED_SP,
        "hit": HIT_SP,
        "compacted": COMPACTED_SP,
        "shiny_idle_frames": SHINY_IDLE_FRAMES,
        "shiny_thinking": SHINY_THINKING_SP,
        "shiny_staging": SHINY_STAGING_SP,
        "shiny_committed": SHINY_COMMITTED_SP,
        "shiny_recovered": SHINY_RECOVERED_SP,
        "shiny_hit": SHINY_HIT_SP,
        "shiny_compacted": SHINY_COMPACTED_SP,
    },
    "raichu": {
        "name": "Raichu",
        "idle_frames": RAICHU_IDLE_FRAMES,
        "thinking": RAICHU_THINKING_SP,
        "staging": RAICHU_STAGING_SP,
        "committed": RAICHU_COMMITTED_SP,
        "recovered": RAICHU_RECOVERED_SP,
        "hit": RAICHU_HIT_SP,
        "compacted": RAICHU_COMPACTED_SP,
        "shiny_idle_frames": SHINY_RAICHU_IDLE_FRAMES,
        "shiny_thinking": SHINY_RAICHU_THINKING_SP,
        "shiny_staging": SHINY_RAICHU_STAGING_SP,
        "shiny_committed": SHINY_RAICHU_COMMITTED_SP,
        "shiny_recovered": SHINY_RAICHU_RECOVERED_SP,
        "shiny_hit": SHINY_RAICHU_HIT_SP,
        "shiny_compacted": SHINY_RAICHU_COMPACTED_SP,
    },
}


def get_species_sprites(species="pikachu", shiny=False):
    """Get sprite set for a species. Falls back to Pikachu."""
    spec = POKEMON_SPECIES.get(species, POKEMON_SPECIES["pikachu"])
    prefix = "shiny_" if shiny else ""
    return {
        "idle_frames": spec.get(f"{prefix}idle_frames", spec["idle_frames"]),
        "thinking": spec.get(f"{prefix}thinking", spec["thinking"]),
        "staging": spec.get(f"{prefix}staging", spec["staging"]),
        "committed": spec.get(f"{prefix}committed", spec["committed"]),
        "recovered": spec.get(f"{prefix}recovered", spec["recovered"]),
        "hit": spec.get(f"{prefix}hit", spec["hit"]),
        "compacted": spec.get(f"{prefix}compacted", spec["compacted"]),
    }
