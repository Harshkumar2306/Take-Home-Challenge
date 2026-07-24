"""
Loop Convergence Detector

Detects when a Planner–Critic feedback loop has stalled by finding
near-duplicate outputs within a sliding window using difflib.SequenceMatcher.
"""

import difflib


def detect_stall(round_outputs: list[str], window: int, threshold: float) -> int:
    """
    Returns the 0-indexed round number at which a stall is first detected.
    
    A stall occurs when the current round's output is highly similar
    (>= threshold) to any output within the previous `window` rounds.

    Args:
        round_outputs: Text output from each round of the Planner/Critic loop.
        window: The maximum number of previous rounds to compare against.
        threshold: The similarity ratio (0.0 to 1.0) required to declare a stall.

    Returns:
        The 0-indexed round where a stall is first detected, or -1 if no stall occurs.
    """
    for current_round in range(1, len(round_outputs)):
        current_output = round_outputs[current_round]
        
        # Compare only against the previous `window` rounds
        lookback_start = max(0, current_round - window)
        
        for previous_round in range(lookback_start, current_round):
            previous_output = round_outputs[previous_round]
            
            similarity = difflib.SequenceMatcher(None, current_output, previous_output).ratio()
            
            if similarity >= threshold:
                return current_round
                
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
