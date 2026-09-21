"""
AI Search Algorithms - Romania Map

Start: Arad
Goal : Bucharest

Algorithms included:
1. Greedy Best-First Search
2. A*
3. Memory-Bounded Heuristic Search (RBFS)
4. Hill Climbing
5. Simulated Annealing
6. Breadth First Search (BFS)
7. Uniform Cost Search (UCS)
8. Depth First Search (DFS)

Run in VS Code terminal:
    python3 search_algorithms.py

The Romania map uses the standard road costs and straight-line heuristic values
commonly used in Artificial Intelligence search examples.
"""

from collections import deque
import heapq
import math
import random
import time
from typing import Dict, List, Tuple, Optional, Any

Graph = Dict[str, List[Tuple[str, int]]]
Heuristic = Dict[str, int]

# -----------------------------------------------------------------------------
# Romania road map: (neighbor, road distance)
# -----------------------------------------------------------------------------
GRAPH: Graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Pitesti", 97), ("Craiova", 146)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)],
}

# Straight-line distance to Bucharest (admissible heuristic for A*).
H: Heuristic = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374,
}

START = "Arad"
GOAL = "Bucharest"

# Theoretical complexity reference (standard worst-case forms).
COMPLEXITIES = {
    "Breadth First Search (BFS)": ("O(b^d)", "O(b^d)"),
    "Depth First Search (DFS)": ("O(b^m)", "O(bm)"),
    "Uniform Cost Search (UCS)": ("O(b^(1 + floor(C*/epsilon)))", "O(b^(1 + floor(C*/epsilon)))"),
    "Greedy Best-First Search": ("O(b^m)", "O(b^m)"),
    "A* Search": ("O(b^d) worst-case", "O(b^d)"),
    "Memory-Bounded Heuristic Search (RBFS)": ("Exponential worst-case", "O(bd) typical linear-space form"),
    "Hill Climbing": ("O(bL)", "O(b)"),
    "Simulated Annealing": ("O(K) for one sampled neighbor/iteration", "O(1)"),
}


def path_cost(path: List[str]) -> int:
    """Return the total road cost of a path."""
    total = 0
    for a, b in zip(path, path[1:]):
        for neighbor, cost in GRAPH[a]:
            if neighbor == b:
                total += cost
                break
        else:
            raise ValueError(f"No edge between {a} and {b}")
    return total


def format_path(path: Optional[List[str]]) -> str:
    return " -> ".join(path) if path else "No solution"


# -----------------------------------------------------------------------------
# 1. Breadth First Search (BFS)
# -----------------------------------------------------------------------------
def bfs(start: str, goal: str) -> Optional[List[str]]:
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path

        for neighbor, _ in GRAPH[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


# -----------------------------------------------------------------------------
# 2. Depth First Search (DFS)
# -----------------------------------------------------------------------------
def dfs(start: str, goal: str) -> Optional[List[str]]:
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)

        # Reverse so that earlier listed neighbors are explored first.
        for neighbor, _ in reversed(GRAPH[node]):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None


# -----------------------------------------------------------------------------
# 3. Uniform Cost Search (UCS)
# -----------------------------------------------------------------------------
def ucs(start: str, goal: str) -> Optional[List[str]]:
    frontier = [(0, start, [start])]
    best_cost = {start: 0}

    while frontier:
        g, node, path = heapq.heappop(frontier)
        if g != best_cost.get(node):
            continue
        if node == goal:
            return path

        for neighbor, edge_cost in GRAPH[node]:
            new_g = g + edge_cost
            if new_g < best_cost.get(neighbor, math.inf):
                best_cost[neighbor] = new_g
                heapq.heappush(frontier, (new_g, neighbor, path + [neighbor]))

    return None


# -----------------------------------------------------------------------------
# 4. Greedy Best-First Search
# -----------------------------------------------------------------------------
def greedy_best_first(start: str, goal: str) -> Optional[List[str]]:
    frontier = [(H[start], start, [start])]
    visited = set()

    while frontier:
        _, node, path = heapq.heappop(frontier)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)

        for neighbor, _ in GRAPH[node]:
            if neighbor not in visited:
                heapq.heappush(frontier, (H[neighbor], neighbor, path + [neighbor]))

    return None


# -----------------------------------------------------------------------------
# 5. A* Search
# -----------------------------------------------------------------------------
def a_star(start: str, goal: str) -> Optional[List[str]]:
    # Heap entry: (f, g, node, path)
    frontier = [(H[start], 0, start, [start])]
    best_g = {start: 0}

    while frontier:
        f, g, node, path = heapq.heappop(frontier)
        if g != best_g.get(node):
            continue
        if node == goal:
            return path

        for neighbor, edge_cost in GRAPH[node]:
            new_g = g + edge_cost
            if new_g < best_g.get(neighbor, math.inf):
                best_g[neighbor] = new_g
                new_f = new_g + H[neighbor]
                heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))

    return None


# -----------------------------------------------------------------------------
# 6. Memory-Bounded Heuristic Search: Recursive Best-First Search (RBFS)
# -----------------------------------------------------------------------------
def rbfs(start: str, goal: str) -> Optional[List[str]]:
    """
    Recursive Best-First Search.
    It uses f=g+h and backtracks while retaining an f-limit.
    Space is linear in search depth (apart from the stored successors at a node).
    """

    def recursive(node: str, path: List[str], g: int, f_limit: float):
        if node == goal:
            return path, g

        successors = []
        for neighbor, edge_cost in GRAPH[node]:
            if neighbor in path:
                continue
            new_g = g + edge_cost
            f_value = max(new_g + H[neighbor], g)
            successors.append([neighbor, path + [neighbor], new_g, f_value])

        if not successors:
            return None, math.inf

        while True:
            successors.sort(key=lambda item: item[3])
            best = successors[0]

            if best[3] > f_limit:
                return None, best[3]

            alternative = successors[1][3] if len(successors) > 1 else math.inf

            result, new_f = recursive(
                best[0], best[1], best[2], min(f_limit, alternative)
            )

            if result is not None:
                return result, new_f

            best[3] = new_f

    result, _ = recursive(start, [start], 0, math.inf)
    return result


# -----------------------------------------------------------------------------
# 7. Hill Climbing
# -----------------------------------------------------------------------------
def hill_climbing(start: str, goal: str) -> Optional[List[str]]:
    current = start
    path = [current]
    visited = {current}

    while current != goal:
        candidates = [
            (H[neighbor], neighbor, edge_cost)
            for neighbor, edge_cost in GRAPH[current]
            if neighbor not in visited
        ]

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0])
        best_h, next_node, _ = candidates[0]

        # Move only if the heuristic strictly improves.
        if best_h >= H[current]:
            return None

        current = next_node
        path.append(current)
        visited.add(current)

    return path


# -----------------------------------------------------------------------------
# 8. Simulated Annealing
# -----------------------------------------------------------------------------
def simulated_annealing(
    start: str,
    goal: str,
    initial_temperature: float = 100.0,
    cooling: float = 0.995,
    iterations: int = 10000,
    seed: int = 42,
) -> Optional[List[str]]:
    """
    Local-search style simulated annealing.
    A worse heuristic move may be accepted with probability exp(-delta/T).
    """
    rng = random.Random(seed)
    current = start
    path = [current]
    visited_recently = {start}
    temperature = initial_temperature
    best_node = current
    best_h = H[current]

    for _ in range(iterations):
        if current == goal:
            return path

        neighbors = GRAPH[current]
        if not neighbors:
            break

        # Prefer not to immediately revisit a recently visited node.
        candidates = [
            (neighbor, cost)
            for neighbor, cost in neighbors
            if neighbor not in visited_recently
        ] or neighbors

        next_node, _ = rng.choice(candidates)
        delta = H[next_node] - H[current]

        if delta <= 0:
            accept = True
        else:
            probability = math.exp(-delta / max(temperature, 1e-12))
            accept = rng.random() < probability

        if accept:
            current = next_node
            path.append(current)
            visited_recently.add(current)

            if H[current] < best_h:
                best_h = H[current]
                best_node = current

        temperature *= cooling
        if temperature < 1e-8:
            temperature = 1e-8

    # Return a partial result only if the goal was actually reached.
    return path if best_node == goal else None


# -----------------------------------------------------------------------------
# Timing / display
# -----------------------------------------------------------------------------
def run_algorithm(name: str, function, *args) -> dict:
    start_time = time.perf_counter()
    path = function(*args)
    elapsed = time.perf_counter() - start_time

    return {
        "name": name,
        "path": path,
        "cost": path_cost(path) if path else None,
        "time": elapsed,
    }


def print_result(result: dict) -> None:
    print(f"\n{'=' * 60}")
    print(result["name"])
    print(f"{'=' * 60}")
    print(f"Path : {format_path(result['path'])}")
    if result["cost"] is not None:
        print(f"Cost : {result['cost']} km")
    else:
        print("Cost : N/A")
    print(f"Time : {result['time'] * 1000:.4f} ms")


def main() -> None:
    print("ROMANIA MAP - AI SEARCH ALGORITHMS")
    print(f"Start = {START}")
    print(f"Goal  = {GOAL}")
    print("\nHeuristic = straight-line distance to Bucharest")

    algorithms = [
        ("Breadth First Search (BFS)", bfs),
        ("Depth First Search (DFS)", dfs),
        ("Uniform Cost Search (UCS)", ucs),
        ("Greedy Best-First Search", greedy_best_first),
        ("A* Search", a_star),
        ("Memory-Bounded Heuristic Search (RBFS)", rbfs),
        ("Hill Climbing", hill_climbing),
        ("Simulated Annealing", simulated_annealing),
    ]

    results = []
    for name, algorithm in algorithms:
        results.append(run_algorithm(name, algorithm, START, GOAL))

    for result in results:
        print_result(result)

    print(f"\n{'=' * 60}")
    print("QUICK COMPARISON")
    print(f"{'=' * 60}")
    print(f"{'Algorithm':40} {'Cost':>8} {'Time (ms)':>12}")
    print("-" * 64)
    for result in results:
        cost = str(result["cost"]) if result["cost"] is not None else "N/A"
        print(f"{result['name'][:40]:40} {cost:>8} {result['time'] * 1000:>12.4f}")

    print("\nTHEORETICAL COMPLEXITY")
    print(f"{'Algorithm':40} {'Time':35} {'Space'}")
    print("-" * 95)
    for result in results:
        time_c, space_c = COMPLEXITIES[result["name"]]
        print(f"{result['name'][:40]:40} {time_c:35} {space_c}")

    print("\nExpected concept:")
    print("- BFS finds the shallowest path, not necessarily the cheapest weighted path.")
    print("- DFS goes deep first and is not guaranteed optimal.")
    print("- UCS finds the least-cost path without a heuristic.")
    print("- Greedy uses h(n) only and can be non-optimal.")
    print("- A* uses g(n)+h(n) and is optimal with an admissible heuristic.")
    print("- RBFS keeps A*-style guidance with much lower memory use.")
    print("- Hill climbing can get stuck at local optima/plateaus.")
    print("- Simulated annealing can escape local optima, but is not guaranteed optimal.")


if __name__ == "__main__":
    main()
