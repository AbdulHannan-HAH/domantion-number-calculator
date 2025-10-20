import networkx as nx
from itertools import combinations
from collections import deque
import numpy as np

# ===================================================
# 1️⃣ Generate Numerical Semigroup Efficiently
# ===================================================
def generate_semigroup(generators, limit_factor=20):
    """Generate numerical semigroup S = <generators> efficiently."""
    m = min(generators)
    max_check = max(generators) * limit_factor
    S = set()
    frontier = deque([0])

    while frontier:
        current = frontier.popleft()
        if current > max_check or current in S:
            continue
        S.add(current)
        for g in generators:
            nxt = current + g
            if nxt <= max_check:
                frontier.append(nxt)
    return S


# ===================================================
# 2️⃣ Build Gap Graph (Edges if |a-b| ∈ S)
# ===================================================
def build_gap_graph(generators):
    S = generate_semigroup(generators)
    max_s = max(S)
    gaps = sorted([x for x in range(max_s) if x not in S])

    G = nx.Graph()
    G.add_nodes_from(gaps)

    for i, j in combinations(gaps, 2):
        if abs(i - j) in S:
            G.add_edge(i, j)

    return G, gaps, S


# ===================================================
# 3️⃣ Perfect Circular Layout
# ===================================================
def perfect_circle_layout(G):
    nodes = sorted(G.nodes())
    n = len(nodes)
    pos = {
        node: (np.cos(2 * np.pi * i / n - np.pi/2), np.sin(2 * np.pi * i / n - np.pi/2))
        for i, node in enumerate(nodes)
    }
    return pos


# ===================================================
# 4️⃣ Domination Number (Exact + Greedy Fallback)
# ===================================================
def is_dominating_set(G, nodes):
    dominated = set(nodes)
    for n in nodes:
        dominated.update(G.neighbors(n))
    return dominated == set(G.nodes())

def domination_number(G):
    """Exact for small graphs; greedy for large ones."""
    nodes = list(G.nodes())

    # Exact search for small graphs
    if len(nodes) <= 14:
        for r in range(1, len(nodes) + 1):
            for subset in combinations(nodes, r):
                if is_dominating_set(G, subset):
                    return set(subset), r

    # Greedy fallback for larger graphs
    uncovered = set(nodes)
    D = set()
    while uncovered:
        best = max(nodes, key=lambda v: len(set(G.neighbors(v)) & uncovered))
        D.add(best)
        uncovered -= {best} | set(G.neighbors(best))
    return D, len(D)