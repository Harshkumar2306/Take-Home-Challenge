"""Tests for detect_stall."""

from solution import detect_stall


# ── Sample from the problem statement ────────────────────────────────────────

def test_sample_input():
    rounds = ["draft A about cats", "draft B about dogs", "draft A about cats, revised"]
    assert detect_stall(rounds, window=2, threshold=0.8) == 2


# ── Basic behaviour ─────────────────────────────────────────────────────────

def test_no_stall():
    rounds = ["The weather is sunny", "Machine learning needs data", "Python is great"]
    assert detect_stall(rounds, window=2, threshold=0.8) == -1


def test_exact_duplicate():
    assert detect_stall(["hello world", "hello world"], window=1, threshold=1.0) == 1


def test_all_identical():
    assert detect_stall(["same"] * 5, window=1, threshold=0.5) == 1


def test_returns_first_stall():
    rounds = ["hello", "hello", "hello"]
    assert detect_stall(rounds, window=1, threshold=0.5) == 1  # first, not 2


# ── Window behaviour ────────────────────────────────────────────────────────

def test_match_outside_window_is_ignored():
    rounds = ["aaa", "bbb", "ccc", "aaa"]
    # window=1 → round 3 only checks round 2 ("ccc"), not round 0
    assert detect_stall(rounds, window=1, threshold=0.8) == -1


def test_match_inside_window():
    rounds = ["aaa", "bbb", "ccc", "aaa"]
    # window=4 → round 3 can see round 0
    assert detect_stall(rounds, window=4, threshold=0.8) == 3


def test_window_larger_than_history():
    assert detect_stall(["cat", "cat"], window=10, threshold=0.9) == 1


# ── Threshold edge cases ────────────────────────────────────────────────────

def test_threshold_zero_always_stalls():
    rounds = ["completely unique text", "totally different string"]
    assert detect_stall(rounds, window=1, threshold=0.0) == 1


def test_threshold_one_needs_exact_match():
    assert detect_stall(["almost same", "almost same!"], window=1, threshold=1.0) == -1
    assert detect_stall(["exact", "exact"], window=1, threshold=1.0) == 1


# ── Edge cases ──────────────────────────────────────────────────────────────

def test_empty_strings():
    assert detect_stall(["", ""], window=1, threshold=0.5) == 1


def test_minimum_input():
    assert detect_stall(["x", "y"], window=1, threshold=0.9) == -1


def test_cyclic_pattern():
    rounds = ["plan A", "plan B", "plan A", "plan B"]
    assert detect_stall(rounds, window=2, threshold=0.9) == 2


def test_special_characters():
    rounds = ["héllo @#$!", "goodbye", "héllo @#$!"]
    assert detect_stall(rounds, window=3, threshold=0.9) == 2
