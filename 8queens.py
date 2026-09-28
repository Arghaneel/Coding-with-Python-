import tkinter as tk
import time

N = 8
CELL_SIZE = 70


class EightQueens:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Queens CSP Simulator")

        self.board = [-1] * N
        self.running = False

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=N * CELL_SIZE,
            height=N * CELL_SIZE
        )
        self.canvas.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(
            root,
            text="Start CSP",
            command=self.start
        )
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(
            root,
            text="Reset",
            command=self.reset
        )
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        # Status
        self.status = tk.Label(
            root,
            text="Ready",
            font=("Arial", 12, "bold")
        )
        self.status.pack(pady=10)

        self.draw_board()

    # -------------------------
    # Draw board
    # -------------------------
    def draw_board(self):

        self.canvas.delete("all")

        for row in range(N):
            for col in range(N):

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if (row + col) % 2 == 0:
                    color = "#F0D9B5"
                else:
                    color = "#131312"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color
                )

        # Draw queens
        for col in range(N):

            row = self.board[col]

            if row != -1:

                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2

                self.canvas.create_text(
                    x,
                    y,
                    text="♛",
                    font=("Arial", 40),
                    fill="red"
                )

    # -------------------------
    # CSP constraint
    # -------------------------
    def is_safe(self, row, col):

        for previous_col in range(col):

            previous_row = self.board[previous_col]

            # Same row
            if previous_row == row:
                return False

            # Same diagonal
            if abs(previous_row - row) == abs(previous_col - col):
                return False

        return True

    # -------------------------
    # Start
    # -------------------------
    def start(self):

        if self.running:
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)

        self.board = [-1] * N

        self.status.config(
            text="Starting CSP Backtracking..."
        )

        self.root.after(500, self.solve)

    # -------------------------
    # Backtracking
    # -------------------------
    def solve(self, col=0):

        # All 8 queens placed
        if col == N:

            self.status.config(
                text="Solution Found!"
            )

            self.running = False
            self.start_button.config(state=tk.NORMAL)

            return True

        # Try every row
        for row in range(N):

            self.status.config(
                text=f"Column {col + 1}: Trying Row {row + 1}"
            )

            self.root.update()

            time.sleep(0.2)

            # Check constraints
            if self.is_safe(row, col):

                # Assign queen
                self.board[col] = row

                self.draw_board()
                self.root.update()

                time.sleep(0.3)

                # Solve next column
                if self.solve(col + 1):
                    return True

                # Backtrack
                self.board[col] = -1

                self.draw_board()
                self.root.update()

                self.status.config(
                    text=f"Backtracking from Column {col + 1}"
                )

                time.sleep(0.3)

        return False

    # -------------------------
    # Reset
    # -------------------------
    def reset(self):

        self.running = False
        self.board = [-1] * N

        self.start_button.config(
            state=tk.NORMAL
        )

        self.status.config(
            text="Ready"
        )

        self.draw_board()


# ==================================
# MAIN PROGRAM
# ==================================

root = tk.Tk()

app = EightQueens(root)

root.mainloop()