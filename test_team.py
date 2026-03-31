#!/usr/bin/env python3
"""Test script for team system - simulates multiple Claude Code sessions."""

import json
import os
import subprocess
import sys

# Determine project root (parent of test_team.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR
WORKSPACE = "/tmp/pikabar-test-workspace"
os.makedirs(WORKSPACE, exist_ok=True)

# Change to project root so subprocess can find pikabar/
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

def run_statusline(session_id, model_id="claude-opus-4-6", cost=0.10):
    """Run statusline with given session_id and model."""
    data = {
        "model": {"id": model_id, "display_name": "Opus"},
        "session_id": session_id,
        "workspace": {"current_dir": WORKSPACE},
        "cost": {"total_cost_usd": cost, "total_duration_ms": 1000},
        "rate_limits": {"five_hour": {"used_percentage": 20}},
        "context_window": {"used_percentage": 30},
    }
    result = subprocess.run(
        [sys.executable, "pikabar/statusline.py"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,  # Ensure correct cwd
    )
    return result.stdout

def get_team_state():
    """Read team state from file."""
    import hashlib
    h = hashlib.md5(WORKSPACE.encode()).hexdigest()[:8]
    state_file = f"/tmp/pikabar-state-{h}"

    if not os.path.exists(state_file):
        return None

    with open(state_file) as f:
        return json.load(f)

def test_team_cycling():
    """Test that different sessions get different team slots."""
    # Clear state
    for f in os.listdir("/tmp"):
        if f.startswith("pikabar-state"):
            os.remove(f"/tmp/{f}")

    print("=" * 60)
    print("Team System Test - Session Cycling")
    print("=" * 60)

    sessions = ["abc123", "def456", "ghi789", "jkl012", "mno345", "pqr678"]
    models = ["claude-haiku-4-20250514", "claude-sonnet-4-20250514", "claude-opus-4-6"]

    print("\n--- Session 1 (Pichu slot) ---")
    run_statusline(sessions[0], models[0])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 2 (Pikachu slot) ---")
    run_statusline(sessions[1], models[1])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 3 (Pikachu slot) ---")
    run_statusline(sessions[2], models[2])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 4 (Raichu slot) ---")
    run_statusline(sessions[3], models[0])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 5 (Raichu slot) ---")
    run_statusline(sessions[4], models[1])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 6 (Pichu slot) ---")
    run_statusline(sessions[5], models[2])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Session 7 (Wrap around to slot 0) ---")
    run_statusline("new_session", models[0])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n--- Same session 'abc123' again (should stay on slot 0) ---")
    run_statusline("abc123", models[0])
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Session counts: {[state['team'][k]['session_count'] for k in sorted(state['team'].keys())]}")

    print("\n" + "=" * 60)
    print("Expected behavior:")
    print("- Each new session should cycle to the slot with lowest session_count")
    print("- Same session_id should stay on the same slot")
    print("- Team has 6 slots: [Pikachu, Pikachu, Pichu, Raichu, Pichu, Raichu]")
    print("- After 6 sessions, wraps back to slot 0")
    print("=" * 60)


def test_evolution():
    """Test evolution when cost threshold is reached."""
    print("\n" + "=" * 60)
    print("Evolution Test")
    print("=" * 60)

    # Clear state
    import hashlib
    h = hashlib.md5(WORKSPACE.encode()).hexdigest()[:8]
    state_file = f"/tmp/pikabar-state-{h}"
    if os.path.exists(state_file):
        os.remove(state_file)

    # Session with high cost to trigger evolution
    print("\n--- High cost session (should evolve Pichu→Pikachu) ---")
    data = {
        "model": {"id": "claude-haiku-4-20250514", "display_name": "Haiku"},
        "session_id": "evo_test",
        "workspace": {"current_dir": WORKSPACE},
        "cost": {"total_cost_usd": 1.50, "total_duration_ms": 5000},
        "rate_limits": {"five_hour": {"used_percentage": 20}},
    }
    result = subprocess.run(
        [sys.executable, "pikabar/statusline.py"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    )
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Evolution stage: {state.get('evolution_stage')}")
        print(f"Cost accumulated: ${state['team']['0']['cost_accumulated']:.2f}")

    # Very high cost to trigger Raichu evolution
    print("\n--- Very high cost session (should evolve Pikachu→Raichu) ---")
    data["cost"]["total_cost_usd"] = 15.00
    data["session_id"] = "evo_test2"
    result = subprocess.run(
        [sys.executable, "pikabar/statusline.py"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    )
    state = get_team_state()
    if state:
        print(f"Slot: {state.get('team_slot')} | Species: {state.get('species')}")
        print(f"Evolution stage: {state.get('evolution_stage')}")
        print(f"Cost accumulated: ${state['team']['0']['cost_accumulated']:.2f}")

    print("\n" + "=" * 60)
    print("Expected behavior:")
    print("- Pichu evolves to Pikachu at $1.00 cumulative cost")
    print("- Pikachu evolves to Raichu at $10.00 cumulative cost")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "evolution":
        test_evolution()
    else:
        test_team_cycling()
        if len(sys.argv) > 1 and sys.argv[1] == "all":
            test_evolution()
