"""
SMART MULTI-STOREY BUILDING SEARCH SIMULATION
Run directly in VS Code:

    python3 building_search_simulation.py

No external libraries required.
Uses Python Tkinter.

Features:
- 4-floor building
- Main Gate start
- Lift and staircase
- 8 search algorithms
- Animated search movement
- Explored nodes shown live
- Final route shown after search
- Target can be changed
- Pause / Resume / Reset
"""

import tkinter as tk
from tkinter import ttk
from collections import deque
import heapq
import math
import random


# ============================================================
# BUILDING MODEL
# ============================================================

FLOORS = 4
LOCATIONS = ["A", "B", "C", "D", "E"]

# Node = (floor_index, location)
# Example: (3, "E") = Floor 4, Room E

GRAPH = {}


def add_edge(a, b, cost):
    GRAPH.setdefault(a, []).append((b, cost))
    GRAPH.setdefault(b, []).append((a, cost))


# Create corridor nodes
for floor in range(FLOORS):
    for location in LOCATIONS:
        GRAPH.setdefault((floor, location), [])

    # Corridor movement
    for i in range(len(LOCATIONS) - 1):
        add_edge(
            (floor, LOCATIONS[i]),
            (floor, LOCATIONS[i + 1]),
            1
        )


# Stairs are at A
for floor in range(FLOORS - 1):
    add_edge(
        (floor, "A"),
        (floor + 1, "A"),
        4
    )


# Lift is at C
for floor in range(FLOORS - 1):
    add_edge(
        (floor, "C"),
        (floor + 1, "C"),
        2
    )


START = (0, "A")
TARGET = (3, "E")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def node_name(node):
    floor, location = node
    return f"F{floor + 1}-{location}"


def edge_cost(a, b):
    for neighbor, cost in GRAPH[a]:
        if neighbor == b:
            return cost
    return 999


def calculate_path_cost(path):
    if not path:
        return math.inf

    total = 0

    for a, b in zip(path, path[1:]):
        total += edge_cost(a, b)

    return total


def heuristic(node, goal):
    """
    Estimated remaining cost.

    Horizontal distance:
        1 per corridor movement

    Vertical distance:
        2 per floor because the lift is the cheaper
        vertical movement in our model.
    """

    floor1, location1 = node
    floor2, location2 = goal

    horizontal = abs(
        LOCATIONS.index(location1)
        - LOCATIONS.index(location2)
    )

    vertical = abs(floor1 - floor2)

    return horizontal + (2 * vertical)


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


# ============================================================
# 1. BREADTH FIRST SEARCH
# ============================================================

def bfs(start, goal):

    queue = deque([start])
    visited = {start}

    parent = {
        start: None
    }

    order = []

    while queue:

        current = queue.popleft()
        order.append(current)

        if current == goal:
            break

        for neighbor, _ in GRAPH[current]:

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return order, reconstruct_path(parent, goal)


# ============================================================
# 2. DEPTH FIRST SEARCH
# ============================================================

def dfs(start, goal):

    stack = [start]
    visited = {start}

    parent = {
        start: None
    }

    order = []

    while stack:

        current = stack.pop()
        order.append(current)

        if current == goal:
            break

        for neighbor, _ in reversed(GRAPH[current]):

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return order, reconstruct_path(parent, goal)


# ============================================================
# 3. UNIFORM COST SEARCH
# ============================================================

def ucs(start, goal):

    priority_queue = [
        (0, start)
    ]

    best_cost = {
        start: 0
    }

    parent = {
        start: None
    }

    order = []

    while priority_queue:

        cost, current = heapq.heappop(
            priority_queue
        )

        if cost != best_cost[current]:
            continue

        order.append(current)

        if current == goal:
            break

        for neighbor, edge in GRAPH[current]:

            new_cost = cost + edge

            if new_cost < best_cost.get(
                neighbor,
                math.inf
            ):

                best_cost[neighbor] = new_cost
                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor)
                )

    return order, reconstruct_path(parent, goal)


# ============================================================
# 4. GREEDY BEST FIRST SEARCH
# ============================================================

def greedy_best_first(start, goal):

    priority_queue = [
        (heuristic(start, goal), start)
    ]

    visited = {start}

    parent = {
        start: None
    }

    order = []

    while priority_queue:

        _, current = heapq.heappop(
            priority_queue
        )

        order.append(current)

        if current == goal:
            break

        for neighbor, _ in GRAPH[current]:

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        heuristic(
                            neighbor,
                            goal
                        ),
                        neighbor
                    )
                )

    return order, reconstruct_path(parent, goal)


# ============================================================
# 5. A STAR
# ============================================================

def a_star(start, goal):

    priority_queue = [
        (
            heuristic(start, goal),
            0,
            start
        )
    ]

    g_cost = {
        start: 0
    }

    parent = {
        start: None
    }

    order = []

    while priority_queue:

        f, current_g, current = heapq.heappop(
            priority_queue
        )

        if current_g != g_cost[current]:
            continue

        order.append(current)

        if current == goal:
            break

        for neighbor, edge in GRAPH[current]:

            new_g = current_g + edge

            if new_g < g_cost.get(
                neighbor,
                math.inf
            ):

                g_cost[neighbor] = new_g
                parent[neighbor] = current

                f_value = (
                    new_g
                    + heuristic(
                        neighbor,
                        goal
                    )
                )

                heapq.heappush(
                    priority_queue,
                    (
                        f_value,
                        new_g,
                        neighbor
                    )
                )

    return order, reconstruct_path(parent, goal)


# ============================================================
# 6. HILL CLIMBING
# ============================================================

def hill_climbing(start, goal):

    current = start

    visited = {start}

    parent = {
        start: None
    }

    order = []

    while True:

        order.append(current)

        if current == goal:
            break

        candidates = []

        for neighbor, _ in GRAPH[current]:

            if neighbor not in visited:

                candidates.append(
                    (
                        heuristic(
                            neighbor,
                            goal
                        ),
                        neighbor
                    )
                )

        if not candidates:
            break

        candidates.sort()

        best_h, best_neighbor = candidates[0]

        current_h = heuristic(
            current,
            goal
        )

        # Local optimum
        if best_h >= current_h:
            break

        parent[best_neighbor] = current

        current = best_neighbor

        visited.add(current)

    return order, reconstruct_path(parent, goal)


# ============================================================
# 7. SIMULATED ANNEALING
# ============================================================

def simulated_annealing(start, goal):

    current = start

    parent = {
        start: None
    }

    order = [start]

    max_iterations = 150

    for iteration in range(max_iterations):

        if current == goal:
            break

        neighbors = GRAPH[current]

        if not neighbors:
            break

        neighbor, _ = random.choice(
            neighbors
        )

        current_h = heuristic(
            current,
            goal
        )

        next_h = heuristic(
            neighbor,
            goal
        )

        temperature = max(
            0.05,
            10 * (
                1 - iteration / max_iterations
            )
        )

        difference = next_h - current_h

        probability = math.exp(
            -difference / temperature
        )

        if (
            difference < 0
            or random.random() < probability
        ):

            parent[neighbor] = current
            current = neighbor

            order.append(current)

            if len(order) > 80:
                break

    return order, reconstruct_path(parent, goal)


# ============================================================
# 8. MEMORY-BOUNDED A*
# ============================================================

def memory_bounded_a_star(
    start,
    goal,
    memory_limit=8
):

    priority_queue = [
        (
            heuristic(start, goal),
            0,
            start
        )
    ]

    g_cost = {
        start: 0
    }

    parent = {
        start: None
    }

    order = []

    while priority_queue:

        priority_queue.sort(
            key=lambda x: x[0]
        )

        f, current_g, current = priority_queue.pop(0)

        if current_g != g_cost[current]:
            continue

        order.append(current)

        if current == goal:
            break

        for neighbor, edge in GRAPH[current]:

            new_g = current_g + edge

            if new_g < g_cost.get(
                neighbor,
                math.inf
            ):

                g_cost[neighbor] = new_g
                parent[neighbor] = current

                new_f = (
                    new_g
                    + heuristic(
                        neighbor,
                        goal
                    )
                )

                priority_queue.append(
                    (
                        new_f,
                        new_g,
                        neighbor
                    )
                )

        # Keep only the best memory_limit states
        priority_queue.sort(
            key=lambda x: x[0]
        )

        if len(priority_queue) > memory_limit:
            priority_queue = priority_queue[
                :memory_limit
            ]

    return order, reconstruct_path(parent, goal)


# ============================================================
# ALGORITHM SELECTOR
# ============================================================

ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Greedy Best-First": greedy_best_first,
    "A*": a_star,
    "Hill Climbing": hill_climbing,
    "Simulated Annealing": simulated_annealing,
    "Memory-Bounded A*": memory_bounded_a_star
}


# ============================================================
# TKINTER SIMULATION
# ============================================================

class BuildingSimulation:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart Multi-Storey Building Search Simulation"
        )

        self.root.geometry(
            "1250x800"
        )

        self.root.minsize(
            1050,
            700
        )

        self.algorithm_name = tk.StringVar(
            value="A*"
        )

        self.target_name = tk.StringVar(
            value="Floor 4 - E"
        )

        self.speed = tk.IntVar(
            value=500
        )

        self.running = False
        self.paused = False

        self.search_order = []
        self.final_path = []

        self.current_index = 0

        self.explored_nodes = []

        self.setup_ui()

        self.draw_building()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def setup_ui(self):

        title = tk.Label(
            self.root,
            text="SMART BUILDING SEARCH SIMULATION",
            font=("Arial", 22, "bold"),
            pady=12
        )

        title.pack()

        subtitle = tk.Label(
            self.root,
            text=(
                "Main Gate → Search Algorithm → "
                "Lift / Stairs / Corridors → Target"
            ),
            font=("Arial", 11)
        )

        subtitle.pack(
            pady=(0, 10)
        )

        controls = tk.Frame(
            self.root
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            controls,
            text="Algorithm:"
        ).pack(
            side="left"
        )

        algorithm_box = ttk.Combobox(
            controls,
            textvariable=self.algorithm_name,
            values=list(ALGORITHMS.keys()),
            state="readonly",
            width=22
        )

        algorithm_box.pack(
            side="left",
            padx=7
        )

        tk.Label(
            controls,
            text="Target:"
        ).pack(
            side="left",
            padx=(15, 0)
        )

        target_box = ttk.Combobox(
            controls,
            textvariable=self.target_name,
            values=[
                "Floor 2 - B",
                "Floor 2 - E",
                "Floor 3 - D",
                "Floor 3 - E",
                "Floor 4 - D",
                "Floor 4 - E"
            ],
            state="readonly",
            width=16
        )

        target_box.pack(
            side="left",
            padx=7
        )

        tk.Label(
            controls,
            text="Speed:"
        ).pack(
            side="left",
            padx=(15, 0)
        )

        speed_box = ttk.Combobox(
            controls,
            values=[
                "Slow",
                "Normal",
                "Fast"
            ],
            state="readonly",
            width=10
        )

        speed_box.set("Normal")

        speed_box.pack(
            side="left",
            padx=7
        )

        speed_box.bind(
            "<<ComboboxSelected>>",
            self.change_speed
        )

        self.start_button = tk.Button(
            controls,
            text="▶ START",
            command=self.start_simulation,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        )

        self.start_button.pack(
            side="left",
            padx=10
        )

        self.pause_button = tk.Button(
            controls,
            text="Ⅱ PAUSE",
            command=self.pause_resume,
            state="disabled",
            padx=15
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="↻ RESET",
            command=self.reset,
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        main = tk.Frame(
            self.root
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.canvas = tk.Canvas(
            main,
            bg="#f8fafc",
            highlightthickness=1,
            highlightbackground="#cbd5e1"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        side = tk.Frame(
            main,
            width=250
        )

        side.pack(
            side="right",
            fill="y",
            padx=(15, 0)
        )

        self.status_label = tk.Label(
            side,
            text="READY",
            font=("Arial", 16, "bold")
        )

        self.status_label.pack(
            pady=10
        )

        self.current_label = tk.Label(
            side,
            text="Current: Main Gate",
            font=("Arial", 12),
            anchor="w"
        )

        self.current_label.pack(
            fill="x",
            pady=5
        )

        self.step_label = tk.Label(
            side,
            text="Step: 0",
            font=("Arial", 12),
            anchor="w"
        )

        self.step_label.pack(
            fill="x",
            pady=5
        )

        self.explored_label = tk.Label(
            side,
            text="Explored: 0",
            font=("Arial", 12),
            anchor="w"
        )

        self.explored_label.pack(
            fill="x",
            pady=5
        )

        self.cost_label = tk.Label(
            side,
            text="Final Cost: —",
            font=("Arial", 12),
            anchor="w"
        )

        self.cost_label.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            side,
            text="MOVEMENT LOG",
            font=("Arial", 11, "bold")
        ).pack(
            pady=(25, 5)
        )

        self.log = tk.Text(
            side,
            width=28,
            height=16,
            font=("Courier New", 9),
            state="disabled"
        )

        self.log.pack(
            fill="both",
            expand=True
        )

        legend = (
            "● Blue  = Agent\n"
            "● Orange = Explored\n"
            "● Green = Final Path\n"
            "● Red = Target\n"
            "━━ Corridor\n"
            "┅┅ Lift\n"
            "··· Stairs"
        )

        tk.Label(
            side,
            text=legend,
            justify="left",
            font=("Arial", 9)
        ).pack(
            pady=10,
            anchor="w"
        )

    # --------------------------------------------------------
    # Speed
    # --------------------------------------------------------

    def change_speed(self, event=None):

        # Combobox value is obtained from event widget
        value = event.widget.get()

        if value == "Slow":
            self.speed.set(900)

        elif value == "Normal":
            self.speed.set(500)

        else:
            self.speed.set(180)

    # --------------------------------------------------------
    # Convert target selection
    # --------------------------------------------------------

    def get_target(self):

        text = self.target_name.get()

        parts = text.replace(
            "Floor ",
            ""
        ).split(" - ")

        floor = int(parts[0]) - 1
        location = parts[1]

        return (
            floor,
            location
        )

    # --------------------------------------------------------
    # Draw complete building
    # --------------------------------------------------------

    def draw_building(self):

        self.canvas.delete(
            "all"
        )

        width = max(
            self.canvas.winfo_width(),
            800
        )

        height = max(
            self.canvas.winfo_height(),
            600
        )

        left = 100
        right = width - 100

        horizontal_gap = (
            right - left
        ) / 4

        bottom = height - 80
        vertical_gap = (
            min(
                120,
                (height - 160) / 3
            )
        )

        self.positions = {}

        for floor in range(FLOORS):

            y = bottom - (
                floor * vertical_gap
            )

            # Floor label
            self.canvas.create_text(
                35,
                y,
                text=f"FLOOR {floor + 1}",
                font=("Arial", 10, "bold"),
                fill="#475569"
            )

            for i, location in enumerate(
                LOCATIONS
            ):

                x = left + (
                    i * horizontal_gap
                )

                self.positions[
                    (floor, location)
                ] = (x, y)

        # Draw floor corridors
        for floor in range(FLOORS):

            for i in range(4):

                a = (
                    floor,
                    LOCATIONS[i]
                )

                b = (
                    floor,
                    LOCATIONS[i + 1]
                )

                x1, y1 = self.positions[a]
                x2, y2 = self.positions[b]

                self.canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#94a3b8",
                    width=4
                )

        # Draw stairs
        for floor in range(FLOORS - 1):

            a = (
                floor,
                "A"
            )

            b = (
                floor + 1,
                "A"
            )

            x1, y1 = self.positions[a]
            x2, y2 = self.positions[b]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#f59e0b",
                width=5,
                dash=(3, 5)
            )

            self.canvas.create_text(
                x1 - 25,
                (y1 + y2) / 2,
                text="STAIRS",
                angle=90,
                fill="#b45309",
                font=("Arial", 8, "bold")
            )

        # Draw lift
        for floor in range(FLOORS - 1):

            a = (
                floor,
                "C"
            )

            b = (
                floor + 1,
                "C"
            )

            x1, y1 = self.positions[a]
            x2, y2 = self.positions[b]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#8b5cf6",
                width=7,
                dash=(10, 6)
            )

        # Draw nodes
        target = self.get_target()

        for floor in range(FLOORS):

            for location in LOCATIONS:

                node = (
                    floor,
                    location
                )

                x, y = self.positions[node]

                radius = 17

                if node == START:

                    color = "#2563eb"

                elif node == target:

                    color = "#dc2626"

                else:

                    color = "#ffffff"

                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=color,
                    outline="#334155",
                    width=2,
                    tags=f"node_{node}"
                )

                self.canvas.create_text(
                    x,
                    y,
                    text=location,
                    fill="white" if node in (
                        START,
                        target
                    ) else "#0f172a",
                    font=("Arial", 10, "bold")
                )

                label = (
                    f"F{floor + 1}-{location}"
                )

                if node == START:
                    label += "\nMAIN GATE"

                elif node == target:
                    label += "\nTARGET"

                self.canvas.create_text(
                    x,
                    y + 32,
                    text=label,
                    font=("Arial", 8),
                    fill="#475569"
                )

        # Title
        self.canvas.create_text(
            width / 2,
            25,
            text=(
                "BUILDING NAVIGATION — "
                "LIVE SEARCH SIMULATION"
            ),
            font=("Arial", 17, "bold"),
            fill="#0f172a"
        )

    # --------------------------------------------------------
    # Draw explored node
    # --------------------------------------------------------

    def draw_explored(self, node):

        x, y = self.positions[node]

        if node in (
            START,
            self.get_target()
        ):
            return

        self.canvas.create_oval(
            x - 13,
            y - 13,
            x + 13,
            y + 13,
            fill="#f59e0b",
            outline="#b45309",
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text=node[1],
            fill="white",
            font=("Arial", 9, "bold")
        )

    # --------------------------------------------------------
    # Draw agent
    # --------------------------------------------------------

    def draw_agent(self, node):

        self.canvas.delete(
            "agent"
        )

        x, y = self.positions[node]

        self.canvas.create_oval(
            x - 22,
            y - 22,
            x + 22,
            y + 22,
            fill="#2563eb",
            outline="white",
            width=4,
            tags="agent"
        )

        self.canvas.create_text(
            x,
            y,
            text="YOU",
            fill="white",
            font=("Arial", 8, "bold"),
            tags="agent"
        )

    # --------------------------------------------------------
    # Draw movement arrow
    # --------------------------------------------------------

    def draw_movement(
        self,
        previous,
        current
    ):

        x1, y1 = self.positions[
            previous
        ]

        x2, y2 = self.positions[
            current
        ]

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#f59e0b",
            width=4,
            arrow=tk.LAST,
            tags="movement"
        )

    # --------------------------------------------------------
    # Draw final path
    # --------------------------------------------------------

    def draw_final_path(self):

        if not self.final_path:
            return

        self.canvas.delete(
            "final"
        )

        for a, b in zip(
            self.final_path,
            self.final_path[1:]
        ):

            x1, y1 = self.positions[a]
            x2, y2 = self.positions[b]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#10b981",
                width=8,
                arrow=tk.LAST,
                tags="final"
            )

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    def add_log(self, text):

        self.log.config(
            state="normal"
        )

        self.log.insert(
            tk.END,
            text + "\n"
        )

        self.log.see(
            tk.END
        )

        self.log.config(
            state="disabled"
        )

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

    def start_simulation(self):

        if self.running:
            return

        target = self.get_target()

        algorithm_name = (
            self.algorithm_name.get()
        )

        algorithm = ALGORITHMS[
            algorithm_name
        ]

        self.search_order, self.final_path = (
            algorithm(
                START,
                target
            )
        )

        self.running = True
        self.paused = False

        self.current_index = 0
        self.explored_nodes = []

        self.start_button.config(
            state="disabled"
        )

        self.pause_button.config(
            state="normal",
            text="Ⅱ PAUSE"
        )

        self.status_label.config(
            text=f"SEARCHING: {algorithm_name}"
        )

        self.cost_label.config(
            text="Final Cost: —"
        )

        self.log.config(
            state="normal"
        )

        self.log.delete(
            "1.0",
            tk.END
        )

        self.log.config(
            state="disabled"
        )

        self.canvas.delete(
            "movement"
        )

        self.canvas.delete(
            "final"
        )

        self.draw_building()

        self.add_log(
            f"Algorithm: {algorithm_name}"
        )

        self.add_log(
            f"Start: {node_name(START)}"
        )

        self.add_log(
            f"Target: {node_name(target)}"
        )

        self.animate_step()

    # --------------------------------------------------------
    # Animation
    # --------------------------------------------------------

    def animate_step(self):

        if not self.running:
            return

        if self.paused:
            return

        if self.current_index >= len(
            self.search_order
        ):

            self.finish_simulation()
            return

        current = self.search_order[
            self.current_index
        ]

        previous = None

        if self.current_index > 0:

            previous = self.search_order[
                self.current_index - 1
            ]

        if previous is not None:

            self.draw_movement(
                previous,
                current
            )

        self.draw_explored(
            current
        )

        self.draw_agent(
            current
        )

        self.explored_nodes.append(
            current
        )

        self.current_index += 1

        self.current_label.config(
            text=(
                f"Current: "
                f"{node_name(current)}"
            )
        )

        self.step_label.config(
            text=(
                f"Step: "
                f"{self.current_index}"
            )
        )

        self.explored_label.config(
            text=(
                f"Explored: "
                f"{len(self.explored_nodes)}"
            )
        )

        self.add_log(
            f"{self.current_index:02d}. "
            f"{node_name(current)}"
        )

        self.root.after(
            self.speed.get(),
            self.animate_step
        )

    # --------------------------------------------------------
    # Finish
    # --------------------------------------------------------

    def finish_simulation(self):

        self.running = False

        self.pause_button.config(
            state="disabled"
        )

        self.start_button.config(
            state="normal"
        )

        self.draw_final_path()

        if (
            self.final_path
            and self.final_path[-1]
            == self.get_target()
        ):

            cost = calculate_path_cost(
                self.final_path
            )

            self.status_label.config(
                text="✓ TARGET REACHED"
            )

            self.cost_label.config(
                text=f"Final Cost: {cost}"
            )

            self.add_log(
                ""
            )

            self.add_log(
                "FINAL ROUTE:"
            )

            self.add_log(
                " → ".join(
                    node_name(n)
                    for n in self.final_path
                )
            )

            self.add_log(
                f"Cost = {cost}"
            )

        else:

            self.status_label.config(
                text="SEARCH STOPPED"
            )

            self.cost_label.config(
                text="Final Cost: —"
            )

            self.add_log(
                "No complete route found."
            )

    # --------------------------------------------------------
    # Pause / Resume
    # --------------------------------------------------------

    def pause_resume(self):

        if not self.running:
            return

        self.paused = not self.paused

        if self.paused:

            self.pause_button.config(
                text="▶ RESUME"
            )

            self.status_label.config(
                text="Ⅱ PAUSED"
            )

        else:

            self.pause_button.config(
                text="Ⅱ PAUSE"
            )

            self.status_label.config(
                text="SEARCHING..."
            )

            self.animate_step()

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset(self):

        self.running = False
        self.paused = False

        self.current_index = 0

        self.search_order = []
        self.final_path = []

        self.explored_nodes = []

        self.pause_button.config(
            state="disabled",
            text="Ⅱ PAUSE"
        )

        self.start_button.config(
            state="normal"
        )

        self.status_label.config(
            text="READY"
        )

        self.current_label.config(
            text="Current: Main Gate"
        )

        self.step_label.config(
            text="Step: 0"
        )

        self.explored_label.config(
            text="Explored: 0"
        )

        self.cost_label.config(
            text="Final Cost: —"
        )

        self.log.config(
            state="normal"
        )

        self.log.delete(
            "1.0",
            tk.END
        )

        self.log.config(
            state="disabled"
        )

        self.draw_building()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BuildingSimulation(
        root
    )

    root.mainloop()
