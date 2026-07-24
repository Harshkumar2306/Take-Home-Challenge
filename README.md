# Loop Convergence Detector

Detects when an AI feedback loop begins repeating similar outputs within a configurable lookback window.

## Problem

Given a sequence of outputs from consecutive rounds, return the index of the first round whose output has a similarity score greater than or equal to `threshold` when compared with any output from the previous `window` rounds.

```python
def detect_stall(
    round_outputs: list[str],
    window: int,
    threshold: float,
) -> int:
```

### AI Example

```text
Round 0: "Summarize the article."
Round 1: "Summarize the article with bullet points."
Round 2: "Summarize the article."

window = 2
threshold = 0.9

-> Stall detected at Round 2
```

## Algorithm

For each round, the algorithm compares the current output only against the previous `window` rounds.

```text
Round 0
  |
Round 1
  |
Round 2
   |
   |-- compare with Round 1
   |-- compare with Round 0
   |
   v
similarity >= threshold ?
  Yes -> return 2
  No  -> continue
```

## Usage

```python
from solution import detect_stall

rounds = [
    "Summarize the article.",
    "Summarize the article with bullet points.",
    "Summarize the article.",
]

print(detect_stall(rounds, window=2, threshold=0.9))
# Output: 2
```

## Assumptions

- Text similarity is measured using Python's `difflib.SequenceMatcher`.
- A stall is detected only within the previous `window` rounds.
- The first detected stall is returned immediately.

## Design Decisions

- **Sliding window**: The assignment defines a stall only within the previous `window` rounds. Older outputs are intentionally ignored because they fall outside the required lookback range. A sliding window directly models this requirement without unnecessary comparisons.
- **`difflib.SequenceMatcher`**: Part of Python's standard library and provides a reasonable string similarity score. This satisfies the assignment's requirement for "any reasonable string similarity measure" without adding external dependencies.
- **Early return**: The function returns immediately on the first stall because the problem asks for the first occurrence.

## Complexity

- **Time:** `O(N * W * L^2)` where `N` is the number of rounds, `W` is the window size, and `L` is the average string length. The algorithm does at most `N * W` comparisons; `SequenceMatcher` accounts for the `L^2` factor.
- **Space:** `O(1)` (excluding the input).

Given the constraints (at most 50 rounds and window up to 10), this is more than adequate.

## Trade-offs

`SequenceMatcher` is simple, built into Python, and adequate for this task. For a production AI system, embedding-based semantic similarity could catch rephrased duplicates, but that would add dependencies and complexity beyond the assignment's scope.

## Tests

The test suite (`test_solution.py`) includes 22 test cases that verify every assignment constraint:

- **Core Logic:** Validates the provided sample input and basic stall/no-stall scenarios.
- **Window Boundaries:** Proves that exact duplicates falling *outside* the lookback window are correctly ignored. Tests `window=1` through `window=10` using parameterized inputs.
- **Threshold Extremes:** Verifies behavior at exact bounds (`0.0` always stalls, `1.0` requires an exact string match). Tests precise threshold boundary behavior (e.g., `0.9` vs `0.91`).
- **Constraint Limits:** Tests maximum input length (50 rounds) and stall detection at the last possible round.
- **Edge Cases:** Handles empty strings, cyclic looping patterns, and special characters safely.

To run the tests:

```bash
pytest test_solution.py -v
```
