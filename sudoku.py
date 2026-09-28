import tkinter as tk
from tkinter import ttk

# ============================================================
# SUDOKU CSP SIMULATOR
# ============================================================

PUZZLES = {
    "Easy":
        "530070000"
        "600195000"
        "098000060"
        "800060003"
        "400803001"
        "700020006"
        "060000280"
        "000419005"
        "000080079",

    "Medium":
        "003020600"
        "900305001"
        "001806400"
        "008102900"
        "700000008"
        "006708200"
        "002609500"
        "800203009"
        "005010300",

    "Hard":
        "000000907"
        "000420180"
        "000705026"
        "100904000"
        "050000040"
        "000507009"
        "920108000"
        "034059000"
        "507000000"
}


class SudokuCSP:

    def __init__(self, puzzle, use_mrv=True):

        # Convert puzzle into list
        self.board = [
            int(x) for x in puzzle
        ]

        # Store original cells
        self.given = {
            i for i, value in enumerate(self.board)
            if value != 0
        }

        self.use_mrv = use_mrv

        self.placements = 0
        self.backtracks = 0

        self.solved = False

    # ========================================================
    # CHECK WHETHER A NUMBER CAN BE PLACED
    # ========================================================

    def is_valid(self, position, number):

        row = position // 9
        col = position % 9

        # Check row
        for c in range(9):

            index = row * 9 + c

            if index != position:
                if self.board[index] == number:
                    return False

        # Check column
        for r in range(9):

            index = r * 9 + col

            if index != position:
                if self.board[index] == number:
                    return False

        # Check 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):

                index = r * 9 + c

                if index != position:
                    if self.board[index] == number:
                        return False

        return True

    # ========================================================
    # GET POSSIBLE VALUES
    # ========================================================

    def possible_values(self, position):

        values = []

        for number in range(1, 10):

            if self.is_valid(position, number):
                values.append(number)

        return values

    # ========================================================
    # SELECT EMPTY CELL
    # ========================================================

    def select_cell(self):

        empty_cells = [
            i for i in range(81)
            if self.board[i] == 0
        ]

        if not empty_cells:
            return None

        # Without MRV
        if not self.use_mrv:
            return empty_cells[0]

        # MRV = Minimum Remaining Values
        best_cell = empty_cells[0]
        best_count = 10

        for cell in empty_cells:

            count = len(
                self.possible_values(cell)
            )

            if count < best_count:

                best_count = count
                best_cell = cell

        return best_cell

    # ========================================================
    # BACKTRACKING SOLVER
    # ========================================================

    def solve(self):

        cell = self.select_cell()

        # No empty cells = solved
        if cell is None:

            self.solved = True
            yield ("solved", None, None)

            return

        values = self.possible_values(cell)

        # Try every possible value
        for number in values:

            # Place number
            self.board[cell] = number

            self.placements += 1

            yield ("place", cell, number)

            # Continue solving
            yield from self.solve()

            if self.solved:
                return

            # Backtrack
            self.board[cell] = 0

            self.backtracks += 1

            yield ("backtrack", cell, number)


# ============================================================
# GUI
# ============================================================

class SudokuApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Sudoku CSP Simulator"
        )

        self.root.configure(
            bg="#f5f5f5"
        )

        self.solver = None
        self.generator = None

        self.running = False

        self.current_cell = None
        self.backtrack_cell = None

        self.cells = []

        self.create_ui()

        self.reset()

    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="Sudoku CSP Simulator",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5"
        )

        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.root,
            text="Constraint Satisfaction Problem + Backtracking",
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#555555"
        )

        subtitle.pack()

        # ----------------------------------------------------
        # BOARD
        # ----------------------------------------------------

        board_frame = tk.Frame(
            self.root,
            bg="black"
        )

        board_frame.pack(
            padx=15,
            pady=15
        )

        for i in range(81):

            row = i // 9
            col = i % 9

            label = tk.Label(
                board_frame,
                text="",
                width=3,
                height=1,
                font=("Arial", 18, "bold"),
                relief="solid",
                borderwidth=1
            )

            # Extra spacing between 3x3 boxes
            padx = (
                2 if col % 3 == 0 else 0,
                2 if col % 3 == 2 else 0
            )

            pady = (
                2 if row % 3 == 0 else 0,
                2 if row % 3 == 2 else 0
            )

            label.grid(
                row=row,
                column=col,
                padx=padx,
                pady=pady
            )

            self.cells.append(label)

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        controls.pack()

        tk.Label(
            controls,
            text="Puzzle:",
            bg="#f5f5f5"
        ).grid(row=0, column=0, padx=5)

        self.puzzle_var = tk.StringVar(
            value="Easy"
        )

        puzzle_box = ttk.Combobox(
            controls,
            textvariable=self.puzzle_var,
            values=list(PUZZLES.keys()),
            state="readonly",
            width=10
        )

        puzzle_box.grid(
            row=0,
            column=1,
            padx=5
        )

        puzzle_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.reset()
        )

        # MRV
        self.mrv_var = tk.BooleanVar(
            value=True
        )

        tk.Checkbutton(
            controls,
            text="Use MRV",
            variable=self.mrv_var,
            bg="#f5f5f5"
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        buttons.pack(
            pady=10
        )

        ttk.Button(
            buttons,
            text="▶ Run",
            command=self.run
        ).grid(
            row=0,
            column=0,
            padx=4
        )

        ttk.Button(
            buttons,
            text="⏸ Pause",
            command=self.pause
        ).grid(
            row=0,
            column=1,
            padx=4
        )

        ttk.Button(
            buttons,
            text="⏭ Step",
            command=self.step
        ).grid(
            row=0,
            column=2,
            padx=4
        )

        ttk.Button(
            buttons,
            text="↻ Reset",
            command=self.reset
        ).grid(
            row=0,
            column=3,
            padx=4
        )

        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        speed_frame = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        speed_frame.pack()

        tk.Label(
            speed_frame,
            text="Speed:",
            bg="#f5f5f5"
        ).pack(
            side="left"
        )

        self.speed = tk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            orient="horizontal",
            length=200,
            bg="#f5f5f5"
        )

        self.speed.set(200)

        self.speed.pack(
            side="left"
        )

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        )

        self.status.pack(
            pady=5
        )

        self.stats = tk.Label(
            self.root,
            text="",
            font=("Consolas", 10),
            bg="#f5f5f5"
        )

        self.stats.pack(
            pady=(0, 15)
        )

    # ========================================================
    # DRAW BOARD
    # ========================================================

    def draw_board(self):

        for i in range(81):

            value = self.solver.board[i]

            # Given cell
            if i in self.solver.given:

                bg = "#d9d9d9"
                fg = "black"

            # Solver cell
            else:

                bg = "white"
                fg = "#1769aa"

            # Current cell
            if i == self.current_cell:

                bg = "#ffe066"

            # Backtracked cell
            if i == self.backtrack_cell:

                bg = "#ff9999"

            # Solved
            if self.solver.solved:

                bg = "#b7e4c7"

            self.cells[i].config(
                text=value if value != 0 else "",
                bg=bg,
                fg=fg
            )

        self.update_stats()

    # ========================================================
    # UPDATE STATISTICS
    # ========================================================

    def update_stats(self):

        empty = self.solver.board.count(0)

        self.stats.config(
            text=
            f"Empty Cells: {empty}    "
            f"Placements: {self.solver.placements}    "
            f"Backtracks: {self.solver.backtracks}"
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.running = False

        self.current_cell = None
        self.backtrack_cell = None

        self.solver = SudokuCSP(
            PUZZLES[self.puzzle_var.get()],
            self.mrv_var.get()
        )

        self.generator = self.solver.solve()

        self.status.config(
            text="Ready"
        )

        self.draw_board()

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        if self.running:
            return

        self.running = True

        self.status.config(
            text="Solving..."
        )

        self.animate()

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        if not self.running:
            return

        if not self.process_step():
            return

        self.root.after(
            self.speed.get(),
            self.animate
        )

    # ========================================================
    # STEP
    # ========================================================

    def step(self):

        if self.running:
            return

        self.process_step()

    # ========================================================
    # PROCESS ONE CSP STEP
    # ========================================================

    def process_step(self):

        try:

            action, cell, value = next(
                self.generator
            )

        except StopIteration:

            self.running = False

            return False

        # ----------------------------------------------------
        # PLACE
        # ----------------------------------------------------

        if action == "place":

            self.current_cell = cell
            self.backtrack_cell = None

            row = cell // 9 + 1
            col = cell % 9 + 1

            self.status.config(
                text=f"Place {value} → Row {row}, Column {col}"
            )

        # ----------------------------------------------------
        # BACKTRACK
        # ----------------------------------------------------

        elif action == "backtrack":

            self.current_cell = None
            self.backtrack_cell = cell

            row = cell // 9 + 1
            col = cell % 9 + 1

            self.status.config(
                text=f"Backtracking from Row {row}, Column {col}"
            )

        # ----------------------------------------------------
        # SOLVED
        # ----------------------------------------------------

        elif action == "solved":

            self.current_cell = None
            self.backtrack_cell = None

            self.running = False

            self.status.config(
                text="✓ Sudoku Solved!"
            )

        self.draw_board()

        return True

    # ========================================================
    # PAUSE
    # ========================================================

    def pause(self):

        self.running = False

        self.status.config(
            text="Paused"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SudokuApp(root)

    root.mainloop()