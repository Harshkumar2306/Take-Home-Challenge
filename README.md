# Loop Convergence Detector

## Problem
A Planner and Critic exchange feedback across rounds. The objective is to detect when the loop has stalled—defined as the current round's output being a near-duplicate of any output within the previous `window` rounds.

## Approach
This implementation uses a sliding window algorithm combined with Python's `difflib.SequenceMatcher`. It evaluates similarity based on the Longest Common Subsequence (LCS) ratio. 

`SequenceMatcher` was chosen because it is part of Python's standard library, requires no external dependencies, and provides a reasonable similarity score for text comparisons, which satisfies the assignment requirements.

**Why this approach?**
The problem defines a stall as similarity with any of the previous `window` rounds. A sliding-window approach naturally models this requirement while limiting comparisons to only the recent history specified in the prompt.

## Algorithm
1. Iterate through `round_outputs` starting from index `1`.
2. For each round `i`, define a lookback window starting at `max(0, i - window)`.
3. Compare the text of round `i` against each round in the window.
4. If the similarity ratio is greater than or equal to the `threshold`, return the round index `i`.
5. If no comparisons meet the threshold, return `-1`.

## Complexity
- **Time Complexity**: The algorithm performs at most `N × W` similarity comparisons. Using Python's `difflib.SequenceMatcher`, a conservative worst-case upper bound is `O(N × W × L²)`, where `N` is the number of rounds, `W` is the window size, and `L` is the average string length.
- **Auxiliary Space**: `O(1)` (excluding the input strings). `SequenceMatcher` performs temporary allocations internally, but the algorithm itself maintains only a few constant variables.

## Running
```bash
python solution.py
```

## Tests
The project includes 14 unit tests covering the sample input, basic behavior, window bounds, threshold edge cases, and empty strings.

To run the tests (requires `pytest`):
```bash
pytest test_solution.py -v
```

## Example
```python
from solution import detect_stall

rounds = ["draft A about cats", "draft B about dogs", "draft A about cats, revised"]
print(detect_stall(rounds, window=2, threshold=0.8))
# Output: 2
```
