import math

GRAPH = {
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
H = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242,
    "Eforie": 161, "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151,
    "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193, "Sibiu": 253,
    "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374,
}
START, GOAL = "Arad", "Bucharest"

def path_cost(path):
    return sum(next(c for n, c in GRAPH[a] if n == b) for a, b in zip(path, path[1:]))

def rbfs(start, goal):
    def recursive(node, path, g, f_limit):
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
            result, new_f = recursive(best[0], best[1], best[2], min(f_limit, alternative))
            if result is not None:
                return result, new_f
            best[3] = new_f

    result, _ = recursive(start, [start], 0, math.inf)
    return result

if __name__ == "__main__":
    path = rbfs(START, GOAL)
    print("MEMORY-BOUNDED HEURISTIC SEARCH (RBFS)")
    print("Formula: f(n) = g(n) + h(n)")
    print("Path:", " -> ".join(path))
    print("Cost:", path_cost(path), "km")
