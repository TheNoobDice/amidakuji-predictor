from amida.solver import endpoint_probs


def test_probs_sum_to_one():
    # With no known rungs, probabilities over all endpoints must sum to 1.
    known = [[None, None], [None, None]]
    probs = endpoint_probs(n=3, h=2, K=1, start=0, known=known, require_cover=False)
    assert abs(sum(probs) - 1) < 1e-9


def test_known_rung_forces_path():
    # One known rung at row 0, slot 0, and K=1 means it is the only rung,
    # so start 0 must end at line 1.
    known = [[1, None], [None, None]]
    probs = endpoint_probs(n=3, h=2, K=1, start=0, known=known, require_cover=False)
    assert probs == [0, 1, 0]


def test_cover_forces_second_gap():
    # K=2 with cover: row 0 uses gap 0, so row 1 must use gap 1.
    # Path: line 0 -> 1 -> 2.
    known = [[1, None], [None, None]]
    probs = endpoint_probs(n=3, h=2, K=2, start=0, known=known)
    assert probs == [0, 0, 1]


def test_k5_never_returns_to_start():
    # 6 lines, 5 rows, K=5: every gap used once, result is a 6-cycle,
    # so no line can end where it started.
    known = [[None] * 5 for _ in range(5)]
    probs = endpoint_probs(n=6, h=5, K=5, start=0, known=known)
    assert probs[0] == 0
    assert abs(sum(probs) - 1) < 1e-9