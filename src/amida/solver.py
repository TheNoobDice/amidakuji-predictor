from itertools import product


def endpoint_probs(n, h, K, start, known, no_adjacent=True):
    # Enumerate every legal rung pattern for each row, given known info.
    row_patterns = []
    for r in range(h):
        patterns = []
        for p in product([0, 1], repeat=n - 1):
            if no_adjacent and any(p[i] and p[i + 1] for i in range(n - 2)):
                continue
            if any(known[r][i] is not None and known[r][i] != p[i] for i in range(n - 1)):
                continue
            patterns.append(p)
        row_patterns.append(patterns)

    # dp maps (current line, rungs used so far) -> number of ways.
    dp = {(start, 0): 1}
    for patterns in row_patterns:
        next_dp = {}
        for (pos, used), ways in dp.items():
            for p in patterns:
                if pos < n - 1 and p[pos]:
                    new_pos = pos + 1
                elif pos > 0 and p[pos - 1]:
                    new_pos = pos - 1
                else:
                    new_pos = pos
                key = (new_pos, used + sum(p))
                next_dp[key] = next_dp.get(key, 0) + ways
        dp = next_dp

    # Keep only configurations with exactly K rungs, then normalize.
    counts = [0] * n
    for (pos, used), ways in dp.items():
        if used == K:
            counts[pos] += ways
    total = sum(counts)
    return [c / total for c in counts] if total else counts


def start_probs(n, h, K, end, known, **kwargs):
    # Amidakuji is reversible: flip the rows and reuse the same function.
    return endpoint_probs(n, h, K, end, known[::-1], **kwargs)