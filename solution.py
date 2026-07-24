"""
Loop Convergence Detector

Detects when a Planner–Critic feedback loop has stalled by finding
near-duplicate outputs within a sliding window using difflib.SequenceMatcher.
"""

import difflib


def detect_stall(round_outputs: list[str], window: int, threshold: float) -> int:
    """
    Returns the 0-indexed round number at which a stall is first detected
    (i.e., current round's output is >= threshold similar to any output within
    the previous `window` rounds), or -1 if no stall is detected.

    Args:
        round_outputs: Text output from each round (2 ≤ len ≤ 50).
        window: How many previous rounds to compare against (1 ≤ window ≤ 10).
        threshold: Similarity ratio at or above which a stall is declared (0.0–1.0).

    Returns:
        The 0-indexed round where stall is first detected, or -1.
        
    Raises:
        ValueError: If any of the input constraints are violated.
    """
    if not (2 <= len(round_outputs) <= 50):
        raise ValueError(f"Constraint violated: 2 <= len(round_outputs) <= 50. Got {len(round_outputs)}")
    if not (1 <= window <= 10):
        raise ValueError(f"Constraint violated: 1 <= window <= 10. Got {window}")
    if not (0.0 <= threshold <= 1.0):
        raise ValueError(f"Constraint violated: 0.0 <= threshold <= 1.0. Got {threshold}")

    for i in range(1, len(round_outputs)):
        start = max(0, i - window)
        for j in range(start, i):
            similarity = difflib.SequenceMatcher(None, round_outputs[i], round_outputs[j]).ratio()
            if similarity >= threshold:
                return i
    return -1


# ── Quick demo ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_rounds = [
        "draft A about cats",
        "draft B about dogs",
        "draft A about cats, revised",
    ]
    result = detect_stall(sample_rounds, window=2, threshold=0.8)
    print(f"Stall detected at round: {result}")  # Expected: 2
