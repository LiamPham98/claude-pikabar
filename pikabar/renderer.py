"""Half-block pixel art renderer.

Each terminal character represents 2 pixel rows using the upper half-block
character (U+2580). Foreground = top pixel, background = bottom pixel.
"""

from .palette import fg, bg, RST


def render_line(top_row, bot_row):
    """Render a single terminal line from two pixel rows."""
    cols = max(len(top_row), len(bot_row))
    out = ""
    for c in range(cols):
        top = top_row[c] if c < len(top_row) else None
        bot = bot_row[c] if c < len(bot_row) else None
        if top is None and bot is None:
            out += " "
        elif top == bot:
            out += f"{fg(top)}█{RST}"
        elif top is not None and bot is None:
            out += f"{fg(top)}▀{RST}"
        elif top is None and bot is not None:
            out += f"{fg(bot)}▄{RST}"
        else:
            out += f"{fg(top)}{bg(bot)}▀{RST}"
    return out


def grid_to_lines(grid):
    """Convert a pixel grid (list of rows) to terminal lines.

    Each pair of pixel rows becomes one terminal line via half-block rendering.
    Pads with an empty row if the grid has an odd number of rows.
    """
    g = [row[:] for row in grid]
    if len(g) % 2 != 0:
        g.append([None] * len(g[0]))
    return [render_line(g[r], g[r + 1]) for r in range(0, len(g), 2)]
