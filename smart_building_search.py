import heapq
import math
import random
import time
from collections import deque
import matplotlib.pyplot as plt

# ============================================================
# SMART MULTI-STOREY BUILDING SEARCH
# Algorithms:
# 1. BFS
# 2. DFS
# 3. Uniform Cost Search (UCS)
# 4. Greedy Best-First Search
# 5. A*
# 6. Hill Climbing
# 7. Simulated Annealing
# 8. Memory-Bounded A* (SMA*-style simplified implementation)
#
# Start  = Main Gate
# Target = any building location (change TARGET below)
# ============================================================

# ------------------------- BUILDING --------------------------

# Each node is: (floor, location)
# floor 0 = ground floor
# floor 1 = first floor, etc.

FLOORS = 4

# Horizontal nodes on every floor
# A--B--C--D--E is the corridor
LOCATIONS = ["A", "B", "C", "D", "E"]

# Building graph: adjacency list
GRAPH = {}

def add_edge(a, b, cost):
    GRAPH.setdefault(a, []).append((b, cost))
    GRAPH.setdefault(b, []).append((a, cost))

# Create corridor on every floor
for floor in range(FLOORS):
    for loc in LOCATIONS:
        GRAPH.setdefault((floor, loc), [])

    for i in range(len(LOCATIONS) - 1):
        add_edge(
            (floor, LOCATIONS[i]),
            (floor, LOCATIONS[i + 1]),
            1
        )

# Stairs: A on each floor
for floor in range(FLOORS - 1):
    add_edge((floor, "A"), (floor + 1, "A"), 4)

# Lift: C on each floor
for floor in range(FLOORS - 1):
    add_edge((floor, "C"), (floor + 1, "C"), 2)

START = (0, "A")       # Main Gate
TARGET = (3, "E")      # Example: Room 401 on 4th floor


# ------------------------- HEURISTIC -------------------------

def heuristic(node, goal):
    """
    Estimated cost from node to goal.
    Manhattan-like estimate:
    horizontal distance + floor difference.
    """
    floor1, loc1 = node
    floor2, loc2 = goal

    horizontal = abs(LOCATIONS.index(loc1) - LOCATIONS.index(loc2))
    vertical = abs(floor1 - floor2)

    # Minimum possible vertical movement is approximately 2 per floor
    return horizontal + 2 * vertical


# ------------------------- COMMON HELPERS --------------------

def reconstruct_path(parent, goal):
    if goal not in parent:
        return None

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def path_cost(path):
    if not path:
        return math.inf

    total = 0

    for a, b in zip(path, path[1:]):
        for nxt, cost in GRAPH[a]:
            if nxt == b:
                total += cost
                break

    return total


# ============================================================
# 1. BREADTH FIRST SEARCH
# ============================================================

def bfs(start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    expanded = 0

    while queue:
        current = queue.popleft()
        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        for neighbor, _ in GRAPH[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, expanded


# ============================================================
# 2. DEPTH FIRST SEARCH
# ============================================================

def dfs(start, goal):
    stack = [start]
    visited = {start}
    parent = {start: None}
    expanded = 0

    while stack:
        current = stack.pop()
        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        # Reverse only to make the visualization deterministic
        for neighbor, _ in reversed(GRAPH[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, expanded


# ============================================================
# 3. UNIFORM COST SEARCH
# ============================================================

def ucs(start, goal):
    pq = [(0, start)]
    best_cost = {start: 0}
    parent = {start: None}
    expanded = 0

    while pq:
        cost, current = heapq.heappop(pq)

        if cost != best_cost[current]:
            continue

        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        for neighbor, edge_cost in GRAPH[current]:
            new_cost = cost + edge_cost

            if new_cost < best_cost.get(neighbor, math.inf):
                best_cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None, expanded


# ============================================================
# 4. GREEDY BEST-FIRST SEARCH
# ============================================================

def greedy_best_first(start, goal):
    pq = [(heuristic(start, goal), start)]
    visited = {start}
    parent = {start: None}
    expanded = 0

    while pq:
        _, current = heapq.heappop(pq)
        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        for neighbor, _ in GRAPH[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                heapq.heappush(
                    pq,
                    (heuristic(neighbor, goal), neighbor)
                )

    return None, expanded


# ============================================================
# 5. A*
# ============================================================

def a_star(start, goal):
    pq = [(heuristic(start, goal), 0, start)]
    g_cost = {start: 0}
    parent = {start: None}
    expanded = 0

    while pq:
        f, current_g, current = heapq.heappop(pq)

        if current_g != g_cost[current]:
            continue

        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        for neighbor, edge_cost in GRAPH[current]:
            new_g = current_g + edge_cost

            if new_g < g_cost.get(neighbor, math.inf):
                g_cost[neighbor] = new_g
                parent[neighbor] = current

                f_value = new_g + heuristic(neighbor, goal)

                heapq.heappush(
                    pq,
                    (f_value, new_g, neighbor)
                )

    return None, expanded


# ============================================================
# 6. HILL CLIMBING
# ============================================================

def hill_climbing(start, goal):
    current = start
    path = [current]
    visited = {current}
    expanded = 0

    while current != goal:
        expanded += 1

        candidates = [
            (heuristic(n, goal), n)
            for n, _ in GRAPH[current]
            if n not in visited
        ]

        if not candidates:
            return None, expanded

        candidates.sort()
        best_h, best_neighbor = candidates[0]

        # Hill climbing stops at a local minimum.
        if best_h >= heuristic(current, goal):
            return None, expanded

        current = best_neighbor
        visited.add(current)
        path.append(current)

    return path, expanded


# ============================================================
# 7. SIMULATED ANNEALING
# ============================================================

def simulated_annealing(start, goal, max_iterations=10000):
    current = start
    path = [current]
    expanded = 0

    for iteration in range(max_iterations):
        expanded += 1

        if current == goal:
            return path, expanded

        neighbors = GRAPH[current]

        if not neighbors:
            return None, expanded

        next_node, _ = random.choice(neighbors)

        current_h = heuristic(current, goal)
        next_h = heuristic(next_node, goal)

        temperature = max(
            0.01,
            10 * (1 - iteration / max_iterations)
        )

        delta = next_h - current_h

        # Always accept better moves.
        # Sometimes accept worse moves.
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = next_node
            path.append(current)

            # Avoid infinitely cycling in the displayed path.
            if len(path) > 100:
                return None, expanded

    return None, expanded


# ============================================================
# 8. MEMORY-BOUNDED A* (SIMPLIFIED SMA*-STYLE)
# ============================================================

def memory_bounded_a_star(start, goal, memory_limit=12):
    """
    Simplified memory-bounded best-first search.

    Keeps only a fixed number of frontier states.
    When memory is full, the worst f-value is discarded.

    This demonstrates the main idea of memory-bounded heuristic
    search without implementing every detail of textbook SMA*.
    """

    pq = []
    g_cost = {start: 0}
    parent = {start: None}

    counter = 0
    heapq.heappush(
        pq,
        (heuristic(start, goal), counter, start)
    )

    expanded = 0

    while pq:
        f, _, current = heapq.heappop(pq)
        expanded += 1

        if current == goal:
            return reconstruct_path(parent, goal), expanded

        for neighbor, edge_cost in GRAPH[current]:
            new_g = g_cost[current] + edge_cost

            if new_g < g_cost.get(neighbor, math.inf):
                g_cost[neighbor] = new_g
                parent[neighbor] = current

                counter += 1
                new_f = new_g + heuristic(neighbor, goal)

                heapq.heappush(
                    pq,
                    (new_f, counter, neighbor)
                )

        # Memory bound
        if len(pq) > memory_limit:
            # Remove the state with the worst f-value.
            pq.sort()
            pq = pq[:memory_limit]
            heapq.heapify(pq)

    return None, expanded


# ============================================================
# VISUALIZATION
# ============================================================

def node_position(node):
    floor, loc = node

    x = LOCATIONS.index(loc) * 2.0
    y = floor * 2.5

    return x, y


def draw_building(
    path=None,
    title="Building Search",
    visited_order=None,
    show_all_movement=True,
    animate=False,
    pause_time=0.35
):
    """
    Draw the complete building and show search movement.

    visited_order:
        Order in which the algorithm expanded/visited nodes.

    path:
        Final path found by the algorithm.

    show_all_movement=True:
        Shows all explored/visited nodes and edges.

    animate=True:
        Displays the search movement step-by-step.
    """

    if visited_order is None:
        visited_order = []

    fig, ax = plt.subplots(figsize=(13, 9))

    # --------------------------------------------------------
    # Draw building edges
    # --------------------------------------------------------

    drawn_edges = set()

    for node, neighbors in GRAPH.items():

        x1, y1 = node_position(node)

        for neighbor, edge_cost in neighbors:

            edge_key = frozenset([node, neighbor])

            if edge_key in drawn_edges:
                continue

            drawn_edges.add(edge_key)

            x2, y2 = node_position(neighbor)

            # Different line styles for corridor / lift / stairs
            if edge_cost == 1:
                linestyle = "-"
                linewidth = 1.5
                alpha = 0.30
            elif edge_cost == 2:
                linestyle = "--"
                linewidth = 2.0
                alpha = 0.40
            else:
                linestyle = ":"
                linewidth = 2.5
                alpha = 0.45

            ax.plot(
                [x1, x2],
                [y1, y2],
                linestyle=linestyle,
                linewidth=linewidth,
                alpha=alpha
            )

    # --------------------------------------------------------
    # Draw node labels
    # --------------------------------------------------------

    for node in GRAPH:

        x, y = node_position(node)

        if node == START:
            size = 500
        elif node == TARGET:
            size = 550
        else:
            size = 230

        ax.scatter(
            x,
            y,
            s=size,
            zorder=4
        )

        floor, loc = node

        if node == START:
            label = f"F{floor + 1}-{loc}\nMAIN GATE"
        elif node == TARGET:
            label = f"F{floor + 1}-{loc}\nTARGET"
        else:
            label = f"F{floor + 1}-{loc}"

        ax.text(
            x,
            y + 0.20,
            label,
            ha="center",
            va="bottom",
            fontsize=9,
            zorder=6
        )

    # --------------------------------------------------------
    # Legend
    # --------------------------------------------------------

    ax.plot([], [], "-", linewidth=2, label="Corridor")
    ax.plot([], [], "--", linewidth=2, label="Lift")
    ax.plot([], [], ":", linewidth=2, label="Stairs")

    ax.legend(
        loc="upper right",
        fontsize=9
    )

    # --------------------------------------------------------
    # Animate/search movement
    # --------------------------------------------------------

    if show_all_movement and visited_order:

        visited_edges = []

        for i, node in enumerate(visited_order):

            x, y = node_position(node)

            # Current search node
            ax.scatter(
                x,
                y,
                s=420,
                marker="o",
                alpha=0.65,
                zorder=8
            )

            # Draw movement from previous expanded node
            if i > 0:

                previous = visited_order[i - 1]

                x1, y1 = node_position(previous)
                x2, y2 = node_position(node)

                ax.plot(
                    [x1, x2],
                    [y1, y2],
                    linewidth=3,
                    alpha=0.75,
                    zorder=7
                )

                # Direction arrow
                ax.annotate(
                    "",
                    xy=(x2, y2),
                    xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle="->",
                        linewidth=1.8
                    ),
                    zorder=9
                )

            if animate:
                ax.set_title(
                    f"{title}\n"
                    f"Searching... Step {i + 1}/{len(visited_order)}"
                )

                plt.pause(pause_time)

        ax.set_title(
            f"{title}\n"
            f"Search completed — {len(visited_order)} nodes explored"
        )

    # --------------------------------------------------------
    # Highlight final solution path
    # --------------------------------------------------------

    if path:

        for i, (a, b) in enumerate(zip(path, path[1:])):

            x1, y1 = node_position(a)
            x2, y2 = node_position(b)

            ax.plot(
                [x1, x2],
                [y1, y2],
                linewidth=5,
                zorder=10
            )

            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="->",
                    linewidth=2.5
                ),
                zorder=11
            )

        # Add step numbers to final path
        for step, node in enumerate(path):

            x, y = node_position(node)

            ax.text(
                x - 0.25,
                y - 0.35,
                str(step),
                fontsize=10,
                fontweight="bold",
                zorder=12
            )

    # --------------------------------------------------------
    # Floor labels and formatting
    # --------------------------------------------------------

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Building horizontal position"
    )

    ax.set_ylabel(
        "Building floor"
    )

    ax.set_yticks(
        [i * 2.5 for i in range(FLOORS)]
    )

    ax.set_yticklabels(
        [f"Floor {i + 1}" for i in range(FLOORS)]
    )

    ax.set_xticks(
        [i * 2.0 for i in range(len(LOCATIONS))]
    )

    ax.set_xticklabels(
        ["A", "B", "C (Lift)", "D", "E"]
    )

    ax.grid(
        alpha=0.2
    )

    plt.tight_layout()
    plt.show()


# ============================================================
# SEARCH TRACE VERSIONS
# ============================================================

def bfs_trace(start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    order = []

    while queue:

        current = queue.popleft()
        order.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), order

        for neighbor, _ in GRAPH[current]:

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, order


def dfs_trace(start, goal):
    stack = [start]
    visited = {start}
    parent = {start: None}
    order = []

    while stack:

        current = stack.pop()
        order.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), order

        for neighbor, _ in reversed(GRAPH[current]):

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, order


def ucs_trace(start, goal):
    pq = [(0, start)]
    best_cost = {start: 0}
    parent = {start: None}
    order = []

    while pq:

        cost, current = heapq.heappop(pq)

        if cost != best_cost[current]:
            continue

        order.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), order

        for neighbor, edge_cost in GRAPH[current]:

            new_cost = cost + edge_cost

            if new_cost < best_cost.get(neighbor, math.inf):

                best_cost[neighbor] = new_cost
                parent[neighbor] = current

                heapq.heappush(
                    pq,
                    (new_cost, neighbor)
                )

    return None, order


def greedy_trace(start, goal):
    pq = [(heuristic(start, goal), start)]
    visited = {start}
    parent = {start: None}
    order = []

    while pq:

        _, current = heapq.heappop(pq)
        order.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), order

        for neighbor, _ in GRAPH[current]:

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current

                heapq.heappush(
                    pq,
                    (heuristic(neighbor, goal), neighbor)
                )

    return None, order


def astar_trace(start, goal):
    pq = [(heuristic(start, goal), 0, start)]
    g_cost = {start: 0}
    parent = {start: None}
    order = []

    while pq:

        f, current_g, current = heapq.heappop(pq)

        if current_g != g_cost[current]:
            continue

        order.append(current)

        if current == goal:
            return reconstruct_path(parent, goal), order

        for neighbor, edge_cost in GRAPH[current]:

            new_g = current_g + edge_cost

            if new_g < g_cost.get(neighbor, math.inf):

                g_cost[neighbor] = new_g
                parent[neighbor] = current

                heapq.heappush(
                    pq,
                    (
                        new_g + heuristic(neighbor, goal),
                        new_g,
                        neighbor
                    )
                )

    return None, order


# ============================================================
# SHOW EVERY ALGORITHM'S MOVEMENT
# ============================================================

def visualize_all_searches():

    searches = [
        ("BFS", bfs_trace),
        ("DFS", dfs_trace),
        ("UCS", ucs_trace),
        ("Greedy Best-First", greedy_trace),
        ("A*", astar_trace),
    ]

    for name, algorithm in searches:

        path, order = algorithm(
            START,
            TARGET
        )

        print("\n" + "=" * 60)
        print(name)
        print("=" * 60)

        print(
            "Movement order:"
        )

        print(
            " -> ".join(
                f"F{floor + 1}-{loc}"
                for floor, loc in order
            )
        )

        if path:

            print(
                "Final path:"
            )

            print(
                " -> ".join(
                    f"F{floor + 1}-{loc}"
                    for floor, loc in path
                )
            )

            print(
                f"Final path cost: {path_cost(path)}"
            )

        draw_building(
            path=path,
            visited_order=order,
            title=f"{name}: Search Movement",
            show_all_movement=True,
            animate=False
        )


# ============================================================
# ============================================================
# RESULT TABLE
# ============================================================

def run_all_algorithms():
    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", ucs),
        ("Greedy Best-First", greedy_best_first),
        ("A*", a_star),
        ("Hill Climbing", hill_climbing),
        ("Simulated Annealing", simulated_annealing),
        ("Memory-Bounded A*", memory_bounded_a_star),
    ]

    results = []

    print("\n======================================================")
    print("SMART BUILDING SEARCH RESULTS")
    print("======================================================")
    print(f"START  : Floor {START[0] + 1}, {START[1]} (Main Gate)")
    print(f"TARGET : Floor {TARGET[0] + 1}, {TARGET[1]}")
    print("======================================================\n")

    for name, algorithm in algorithms:

        # SA is stochastic, so its result may vary.
        random.seed(42)

        start_time = time.perf_counter()

        try:
            path, expanded = algorithm(START, TARGET)
        except Exception as e:
            path = None
            expanded = 0
            print(f"{name}: ERROR -> {e}")
            continue

        execution_time = (time.perf_counter() - start_time) * 1000

        if path:
            cost = path_cost(path)

            path_string = " -> ".join(
                f"F{floor + 1}-{loc}"
                for floor, loc in path
            )

            print(f"{name}")
            print(f"Path          : {path_string}")
            print(f"Path cost     : {cost}")
            print(f"Nodes expanded: {expanded}")
            print(f"Time          : {execution_time:.4f} ms")
            print()

            results.append(
                (name, cost, expanded, execution_time, path)
            )

        else:
            print(f"{name}")
            print("Path          : NOT FOUND")
            print(f"Nodes expanded: {expanded}")
            print(f"Time          : {execution_time:.4f} ms")
            print()

            results.append(
                (name, math.inf, expanded, execution_time, None)
            )

    return results


# ============================================================
# MEMBER TIME ALLOCATION
# ============================================================

def estimate_travel_time(path):
    """
    Simple illustrative time model.

    Corridor edge  = 10 sec
    Stairs edge    = 35 sec
    Lift edge      = 20 sec
    """

    if not path:
        return math.inf

    total_seconds = 0

    for a, b in zip(path, path[1:]):

        cost = None

        for neighbor, edge_cost in GRAPH[a]:
            if neighbor == b:
                cost = edge_cost
                break

        if cost == 1:
            total_seconds += 10
        elif cost == 2:
            total_seconds += 20
        elif cost == 4:
            total_seconds += 35

    return total_seconds


def allocate_member(member_id, destination):
    """
    Assign a member a route and estimated arrival time.
    A* is used here because it considers both cost already travelled
    and estimated remaining cost.
    """

    path, expanded = a_star(START, destination)

    if not path:
        print(f"Member {member_id}: No route available.")
        return

    cost = path_cost(path)
    seconds = estimate_travel_time(path)

    path_string = " -> ".join(
        f"F{floor + 1}-{loc}"
        for floor, loc in path
    )

    print("\n---------------- MEMBER ALLOCATION ----------------")
    print(f"Member ID       : {member_id}")
    print(f"Destination     : Floor {destination[0] + 1}, {destination[1]}")
    print(f"Assigned Path   : {path_string}")
    print(f"Search Cost     : {cost}")
    print(f"Estimated Time  : {seconds // 60} min {seconds % 60} sec")
    print(f"Nodes Expanded  : {expanded}")
    print("----------------------------------------------------")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # 1. Run every search algorithm
    results = run_all_algorithms()

    # 2. Show A* final route with all search movement
    astar_path, astar_order = astar_trace(
        START,
        TARGET
    )

    draw_building(
        path=astar_path,
        visited_order=astar_order,
        title="A*: Complete Search Movement + Final Route",
        show_all_movement=True,
        animate=False
    )

    # 3. Uncomment the next line if you want separate
    # visualizations for BFS, DFS, UCS, Greedy and A*.
    visualize_all_searches()

    # 4. Demonstrate member allocation
    allocate_member(
        "M001",
        (3, "E")
    )

    allocate_member(
        "M002",
        (2, "B")
    )

    allocate_member(
        "M003",
        (1, "E")
    )
