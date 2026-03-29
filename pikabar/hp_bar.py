"""HP and PP bar rendering + status badges.

HP = Rate limit quota REMAINING (100 - used%).
     Full HP = safe. Empty HP = rate limited.
PP = Context window REMAINING (100 - used%).
     Full PP = fresh context. Empty PP = compaction imminent.
"""

from .palette import (
    fg, bg, RST, BOLD,
    HP_GREEN, HP_YELLOW, HP_RED, DIM, SUBTLE,
    BADGE_PAR, BADGE_SLP, BADGE_PSN, BADGE_BRN, BADGE_FRZ,
)

# Bar dimensions (shorter to fit both HP + PP on one line)
BAR_WIDTH = 10
BAR_FILL = "█"
BAR_EMPTY = "░"

# PP bar fixed color (steel blue — distinct from HP's green/yellow/red)
PP_COLOR = 75


def hp_color(hp_pct):
    """Return the 256-color code for the given HP percentage."""
    if hp_pct > 50:
        return HP_GREEN
    elif hp_pct > 20:
        return HP_YELLOW
    else:
        return HP_RED


def render_hp_bar(hp_pct, tick=0, width=BAR_WIDTH):
    """Render the HP bar: HP ██████░░░░ 64%"""
    if hp_pct is None:
        unknown = "?" * width
        return f"{fg(SUBTLE)}HP {fg(DIM)}{unknown}{RST} {fg(SUBTLE)}---{RST}"

    hp_pct = max(0, min(100, hp_pct))
    filled = int(width * hp_pct / 100)
    empty = width - filled

    color = hp_color(hp_pct)

    # Flash effect at critical HP (<5%)
    if hp_pct < 5 and tick % 2 == 1:
        color = DIM

    bar = f"{fg(color)}{BAR_FILL * filled}{fg(DIM)}{BAR_EMPTY * empty}{RST}"
    pct_str = f"{fg(color)}{hp_pct:>3}%{RST}"

    return f"{fg(SUBTLE)}HP{RST} {bar} {pct_str}"


def render_pp_bar(pp_pct, width=BAR_WIDTH):
    """Render the PP bar: PP ████████░░ 80%"""
    if pp_pct is None:
        unknown = "?" * width
        return f"{fg(SUBTLE)}PP {fg(DIM)}{unknown}{RST} {fg(SUBTLE)}---{RST}"

    pp_pct = max(0, min(100, pp_pct))
    filled = int(width * pp_pct / 100)
    empty = width - filled

    bar = f"{fg(PP_COLOR)}{BAR_FILL * filled}{fg(DIM)}{BAR_EMPTY * empty}{RST}"
    pct_str = f"{fg(PP_COLOR)}{pp_pct:>3}%{RST}"

    return f"{fg(SUBTLE)}PP{RST} {bar} {pct_str}"


# ============================================================
# Status badges (Pokemon game-accurate colors)
# ============================================================

def _badge(text, colors):
    """Render a colored badge like [PAR]."""
    return f"{BOLD}{fg(colors['fg'])}{bg(colors['bg'])} {text} {RST}"


BADGE_SPECS = {
    "FRZ": BADGE_FRZ,
    "PAR": BADGE_PAR,
    "SLP": BADGE_SLP,
    "PSN": BADGE_PSN,
    "BRN": BADGE_BRN,
}


def get_badge(hp_pct, is_compacting=False, is_rate_limited=False):
    """Determine which status badge to show (one at a time, priority order).

    Priority: FRZ > PAR > SLP > PSN > BRN > none.
    """
    if is_rate_limited and is_compacting:
        return _badge("FRZ", BADGE_FRZ)
    if is_rate_limited:
        return _badge("PAR", BADGE_PAR)
    if is_compacting:
        return _badge("SLP", BADGE_SLP)
    if hp_pct is not None:
        if hp_pct <= 15:
            return _badge("PSN", BADGE_PSN)
        if hp_pct <= 35:
            return _badge("BRN", BADGE_BRN)
    return ""
