"""Pokemon-style flavor text pools and easter eggs.

Voice: Pokemon game narrator, third-person present tense.
Max 28 chars per message to fit the info panel layout.

8 reaction pools + easter eggs.
"""

import random
from datetime import datetime

# ============================================================
# Reaction-specific flavor text pools (8 per reaction)
# ============================================================

FLAVOR = {
    "idle": [
        "What will PIKACHU do?",
        "PIKACHU is waiting...",
        "Ready for battle.",
        "Standing by...",
        "PIKACHU is alert.",
        "Awaiting orders...",
        "The field is quiet.",
        "PIKACHU looks around.",
    ],
    "thinking": [
        "PIKACHU used FOCUS.",
        "PIKACHU is thinking...",
        "PIKACHU used DETECT!",
        "Analyzing the field...",
        "A careful approach...",
        "PIKACHU is strategizing.",
        "Weighing the options...",
        "Deep in thought...",
    ],
    "staging": [
        "PIKACHU is on alert!",
        "Something's happening...",
        "PIKACHU senses change!",
        "The field is shifting.",
        "PIKACHU used AGILITY!",
        "Changes detected!",
        "Activity in the area...",
        "PIKACHU perked up!",
    ],
    "committed": [
        "PIKACHU gained EXP!",
        "PIKACHU leveled up!",
        "Commit captured!",
        "PIKACHU is pleased!",
        "A wild commit appeared!",
        "Saved the game!",
        "PIKACHU used CELEBRATE!",
        "Victory fanfare!",
    ],
    "recovered": [
        "HP was restored!",
        "Energy recovered!",
        "Rate limit reset!",
        "Back to full power!",
        "PIKACHU recovered fully.",
        "Moves fully recharged!",
        "Feeling refreshed!",
        "PIKACHU is revitalized!",
    ],
    "compacted": [
        "PIKACHU woke up!",
        "...Where am I?",
        "Memory was cleared!",
        "Hm? What happened?",
        "PIKACHU is confused!",
        "Context was compacted.",
        "PIKACHU used REST!",
        "Recovering memories...",
    ],
    "hit": [
        "It's super effective!",
        "PIKACHU took damage!",
        "PIKACHU flinched!",
        "A heavy blow!",
        "Rate limit pressure!",
        "PIKACHU is struggling.",
        "That really hurt...",
        "HP dropping fast!",
    ],
    "faint": [
        "PIKACHU can't move!",
        "It's fully paralyzed!",
        "Out of PP entirely.",
        "A forced retreat...",
        "Waiting to recover...",
        "PIKACHU was recalled.",
        "The trainer waits...",
        "PIKACHU needs time.",
    ],
}

# ============================================================
# HP threshold messages (trigger once per crossing)
# ============================================================

HP_THRESHOLD = {
    50: [
        "Moves are running low...",
        "Conserve your PP.",
        "PIKACHU is slowing down.",
    ],
    25: [
        "Not many moves remain.",
        "PIKACHU is struggling.",
        "PP dangerously low!",
    ],
    10: [
        "Almost out of moves!",
        "One last stand...",
        "PIKACHU can barely move.",
    ],
    0: [
        "PIKACHU can't move!",
        "Out of PP entirely.",
        "Paralysis took hold.",
    ],
    -1: [  # HP restored (special key)
        "Moves fully recharged!",
        "PIKACHU recovered fully.",
        "Back to full power!",
    ],
}

# ============================================================
# Easter eggs
# ============================================================

DATE_EGGS = {
    (2, 27): "Happy Pokemon Day!",
    (3, 14): "PIKACHU used PI ATTACK!",
    (4, 1):  "DITTO used TRANSFORM!",
    (5, 4):  "Use the FORCE, Pika!",
    (10, 31): "BOO! GENGAR appeared!",
    (12, 25): "DELIBIRD used PRESENT!",
    (1, 1):   "Happy New Year! Lv UP!",
}

COST_MILESTONES = {
    1:   "PIKACHU earned 100P!",
    5:   "That's 500P spent!",
    10:  "Evolved into RAICHU?!",
    25:  "PROF OAK: Impressive!",
    50:  "Elite Four material!",
    100: "PIKACHU is CHAMPION!",
}

RARE_RANDOM = [
    "A shiny PIKACHU appeared!",
    "Wild MISSINGNO. appeared!",
    "PIKACHU learned FLY!",
    "Found a RARE CANDY!",
    "PIKACHU used VOLT TACKLE!",
    "A wild MEW appeared!",
    "Master Ball acquired!",
    "PIKACHU wants to learn...",
    "Old Man glitch activated!",
    "Pika Pika!",
]

# Context-specific number gags
NUMBER_EGGS = {
    42: "The answer to everything.",
    69: "Nice.",
}


def get_flavor_text(state, hp_pct=None, cost_usd=0.0, duration_min=0,
                    tick=0, chance=0.08):
    """Get flavor text for the current reaction state.

    Priority order:
    1. Date-based easter eggs (always fire)
    2. Cost milestones (fire once — caller tracks)
    3. Rare random (0.5% chance)
    4. State flavor (8% chance by default)
    5. Empty string (most of the time)

    Returns:
        Tuple of (text, is_special) where is_special=True for eggs/milestones.
    """
    now = datetime.now()

    # 1. Date-based (check once per session, not per tick)
    if tick == 0:
        key = (now.month, now.day)
        if key in DATE_EGGS:
            return DATE_EGGS[key], True

    # 2. Rare random (0.5%)
    if random.random() < 0.005:
        return random.choice(RARE_RANDOM), True

    # 3. Number eggs (exact HP match)
    if hp_pct is not None and hp_pct in NUMBER_EGGS:
        return NUMBER_EGGS[hp_pct], True

    # 4. Duration milestones
    if duration_min == 60 and tick < 3:
        return "Evolved into RAICHU!", True

    # 5. State flavor (default chance)
    if random.random() < chance and state in FLAVOR:
        return random.choice(FLAVOR[state]), False

    return "", False
