"""Animation engine for terminal sprite rendering.

Supports two modes:
1. Single-state animation (for individual state preview)
2. Unified demo (states transition seamlessly in one view)
"""

import sys
import time

from .palette import fg, RST, BOLD, HIDE, SHOW, CLR, UP, DY, Y, SUBTLE
from .renderer import grid_to_lines

# Max display lines for consistent cursor management
MAX_DISPLAY_LINES = 6


def animate(name, frames, duration=8, fps=3, decorate_fn=None, session=None):
    """Animate a single state with cursor-up overwrite."""
    rendered = [grid_to_lines(f) for f in frames]
    total = int(duration * fps)
    nf = len(rendered)

    w = sys.stdout.write
    fl = sys.stdout.flush
    frame_lines = MAX_DISPLAY_LINES + 1

    w(HIDE)
    w(f"\n  {fg(DY)}{'━' * 56}{RST}\n")
    w(f"  {fg(Y)}{BOLD}■ {name}{RST}\n")
    w(f"  {fg(SUBTLE)}Ctrl+C to stop{RST}\n")
    w(f"  {fg(DY)}{'━' * 56}{RST}\n\n")
    fl()

    for _ in range(frame_lines):
        w(f"{CLR}\n")
    fl()

    try:
        for tick in range(total):
            w(UP(frame_lines))
            sprite = rendered[tick % nf]
            if decorate_fn:
                lines = decorate_fn(sprite, tick, session=session)
            else:
                lines = [f"  {sp}" for sp in sprite]
            while len(lines) < MAX_DISPLAY_LINES:
                lines.append("")
            for line in lines[:MAX_DISPLAY_LINES]:
                w(f"{CLR}{line}\n")
            w(f"{CLR}\n")
            fl()
            time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass
    finally:
        w(SHOW)
        w("\n")
        fl()
        print(f"  {fg(SUBTLE)}Done.{RST}\n")


def animate_unified(segments, loop=True, session=None):
    """Unified animation: multiple states transition in one view.

    segments: list of (label, frames, fps, duration_secs, decorate_fn).
    """
    seg_data = []
    for label, frames, fps, dur, dec_fn in segments:
        rendered = [grid_to_lines(f) for f in frames]
        total_ticks = int(dur * fps)
        seg_data.append((label, rendered, fps, total_ticks, dec_fn))

    w = sys.stdout.write
    fl = sys.stdout.flush
    frame_lines = MAX_DISPLAY_LINES + 1

    w(HIDE)
    w(f"\n  {fg(DY)}{'━' * 56}{RST}\n")
    w(f"  {fg(Y)}{BOLD}■ pikabar — Unified Demo{RST}\n")
    w(f"  {fg(SUBTLE)}Ctrl+C to stop{RST}\n")
    w(f"  {fg(DY)}{'━' * 56}{RST}\n\n")
    fl()

    for _ in range(frame_lines):
        w(f"{CLR}\n")
    fl()

    try:
        while True:
            for label, rendered, fps, total_ticks, dec_fn in seg_data:
                nf = len(rendered)
                for tick in range(total_ticks):
                    w(UP(frame_lines))
                    sprite = rendered[tick % nf]
                    if dec_fn:
                        lines = dec_fn(sprite, tick, session=session)
                    else:
                        lines = [f"  {sp}" for sp in sprite]
                    while len(lines) < MAX_DISPLAY_LINES:
                        lines.append("")
                    for line in lines[:MAX_DISPLAY_LINES]:
                        w(f"{CLR}{line}\n")
                    w(f"{CLR}\n")
                    fl()
                    time.sleep(1.0 / fps)
            if not loop:
                break
    except KeyboardInterrupt:
        pass
    finally:
        w(SHOW)
        w("\n")
        fl()
        print(f"  {fg(SUBTLE)}Done.{RST}\n")
