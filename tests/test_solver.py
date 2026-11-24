from amida.solver import endpoint_probs


def test_probs_sum_to_one():
    # With no known rungs, probabilities over all endpoints must sum to 1.
    known = [[None, None], [None, None]]
    probs = endpoint_probs(n=3, h=2, K=1, start=0, known=known)
    assert abs(sum(probs) - 1) < 1e-9


def test_known_rung_forces_path():
    # One known rung at row 0, slot 0, and K=1 means it is the only rung,
    # so start 0 must end at line 1.
    known = [[1, None], [None, None]]
    probs = endpoint_probs(n=3, h=2, K=1, start=0, known=known)
    assert probs == [0, 1, 0]