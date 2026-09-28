import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# SIMULATED ANNEALING SIMULATOR
# ============================================================

# -----------------------------
# Configuration
# -----------------------------
START_X = -10
END_X = 10

INITIAL_TEMPERATURE = 100
COOLING_RATE = 0.97
MIN_TEMPERATURE = 0.1
STEP_SIZE = 0.8
ITERATIONS = 500


# ============================================================
# Objective / Cost Function
# ============================================================

def cost_function(x):
    """
    Function that Simulated Annealing tries to minimize.
    Multiple valleys make it possible to demonstrate
    local minima and global exploration.
    """
    return (
        0.15 * x**2
        + 4 * np.sin(1.5 * x)
        + 2 * np.sin(3 * x)
    )


# ============================================================
# Generate landscape
# ============================================================

x_values = np.linspace(START_X, END_X, 2000)
y_values = cost_function(x_values)


# ============================================================
# Initial State
# ============================================================

current_x = np.random.uniform(START_X, END_X)

current_cost = cost_function(current_x)

best_x = current_x
best_cost = current_cost

temperature = INITIAL_TEMPERATURE

iteration = 0
accepted_moves = 0
rejected_moves = 0


# ============================================================
# Matplotlib Figure
# ============================================================

fig, ax = plt.subplots(figsize=(12, 7))

fig.canvas.manager.set_window_title(
    "Simulated Annealing Simulator"
)

ax.plot(
    x_values,
    y_values,
    linewidth=2,
    label="Cost Landscape"
)

# Current position
current_point, = ax.plot(
    [current_x],
    [current_cost],
    marker="o",
    markersize=10,
    label="Current Solution"
)

# Best solution
best_point, = ax.plot(
    [best_x],
    [best_cost],
    marker="*",
    markersize=16,
    label="Best Solution"
)

# Movement history
history_line, = ax.plot(
    [],
    [],
    linewidth=1,
    alpha=0.7,
    label="Search Path"
)

# Text information
info_text = ax.text(
    0.02,
    0.97,
    "",
    transform=ax.transAxes,
    verticalalignment="top",
    fontsize=11,
    bbox=dict(
        boxstyle="round",
        alpha=0.85
    )
)

ax.set_title(
    "Simulated Annealing Search Simulator",
    fontsize=18
)

ax.set_xlabel("Solution Space")
ax.set_ylabel("Cost / Objective Value")

ax.grid(True, alpha=0.3)

ax.legend(
    loc="upper right"
)


# ============================================================
# Search History
# ============================================================

history_x = [current_x]
history_y = [current_cost]


# ============================================================
# Simulated Annealing Algorithm
# ============================================================

def simulated_annealing_step():
    global current_x
    global current_cost
    global best_x
    global best_cost
    global temperature
    global iteration
    global accepted_moves
    global rejected_moves

    # Stop after maximum iterations
    if iteration >= ITERATIONS:
        return

    iteration += 1

    # ---------------------------------------
    # Generate neighboring solution
    # ---------------------------------------

    new_x = current_x + np.random.uniform(
        -STEP_SIZE,
        STEP_SIZE
    )

    # Keep inside search space
    new_x = np.clip(
        new_x,
        START_X,
        END_X
    )

    new_cost = cost_function(new_x)

    # ---------------------------------------
    # Calculate difference
    # ---------------------------------------

    delta = new_cost - current_cost

    # ---------------------------------------
    # Acceptance rule
    # ---------------------------------------

    if delta < 0:

        # Better solution
        accept = True

    else:

        # Worse solution
        probability = np.exp(
            -delta / max(temperature, 0.000001)
        )

        accept = np.random.random() < probability

    # ---------------------------------------
    # Update current solution
    # ---------------------------------------

    if accept:

        current_x = new_x
        current_cost = new_cost

        accepted_moves += 1

        history_x.append(current_x)
        history_y.append(current_cost)

        # Update best solution
        if current_cost < best_cost:

            best_x = current_x
            best_cost = current_cost

    else:

        rejected_moves += 1

    # ---------------------------------------
    # Cool down
    # ---------------------------------------

    temperature *= COOLING_RATE

    temperature = max(
        temperature,
        MIN_TEMPERATURE
    )


# ============================================================
# Animation Update
# ============================================================

def update(frame):

    simulated_annealing_step()

    # Update current point
    current_point.set_data(
        [current_x],
        [current_cost]
    )

    # Update best point
    best_point.set_data(
        [best_x],
        [best_cost]
    )

    # Update search path
    history_line.set_data(
        history_x,
        history_y
    )

    # Update information panel
    info_text.set_text(
        f"Iteration        : {iteration}\n"
        f"Temperature      : {temperature:.4f}\n"
        f"Current Cost     : {current_cost:.4f}\n"
        f"Best Cost        : {best_cost:.4f}\n"
        f"Current Position : {current_x:.4f}\n"
        f"Best Position    : {best_x:.4f}\n"
        f"Accepted Moves   : {accepted_moves}\n"
        f"Rejected Moves   : {rejected_moves}"
    )

    return (
        current_point,
        best_point,
        history_line,
        info_text
    )


# ============================================================
# Start Animation
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    frames=ITERATIONS,
    interval=50,
    repeat=False
)

plt.tight_layout()

plt.show()