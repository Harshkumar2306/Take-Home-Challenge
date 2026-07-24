"""Loop Convergence Detector.

Detects when a Planner-Critic feedback loop has stalled by finding
near-duplicate outputs within a sliding window.
"""

import difflib


def detect_stall(round_outputs: list[str], window: int, threshold: float) -> int:
    """
    Detect the first stalled round in a sequence of outputs.

    A stall occurs when the current round's output is at least `threshold`
    similar to any output within the previous `window` rounds.

    Args:
        round_outputs: Outputs produced at each round (2 to 50 items).
        window: Number of previous rounds to compare against (1 to 10).
        threshold: Minimum similarity score to count as a stall (0.0 to 1.0).

    Returns:
        The 0-indexed round number at which a stall is first detected,
        or -1 if no stall is detected.
    """
    for current_round in range(1, len(round_outputs)):
        current_output = round_outputs[current_round]
        lookback_start = max(0, current_round - window)

        for previous_round in range(lookback_start, current_round):
            previous_output = round_outputs[previous_round]

            similarity = difflib.SequenceMatcher(
                None,
                current_output,
                previous_output,
            ).ratio()

            if similarity >= threshold:
                return current_round

    return -1
