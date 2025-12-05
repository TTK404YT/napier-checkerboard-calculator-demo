import tkinter as tk
from math import floor

# ======================================================
# NEW SECTION: spinbox to choose ANY board size (Option B)
# ======================================================

def choose_board_size():
    popup = tk.Tk()
    popup.title("Choose Board Size")

    tk.Label(popup, text="Enter board size (e.g., 4, 5, 6, 8, 12...):",
             font=("Arial", 12)).pack(pady=10)

    size_var = tk.IntVar(value=8)

    size_box = tk.Spinbox(
        popup,
        from_=2,
        to=20,
        width=5,
        font=("Arial", 14),
        textvariable=size_var
    )
    size_box.pack(pady=5)

    def confirm():
        popup.destroy()
        launch_board(size_var.get())

    tk.Button(popup, text="Create Board", font=("Arial", 14),
              command=confirm).pack(pady=10)

    popup.mainloop()


def launch_board(size):
    """Create VALUES, LABELS, and BOARD based on selected size."""
    global CELL_SIZE, BOARD, GRID, CIRCLE_RADIUS
    global VALUES, BOTTOM_LABELS, RIGHT_LABELS

    CELL_SIZE = 70
    CIRCLE_RADIUS = 22

    BOARD = size
    GRID = BOARD + 1

    # Generate powers of 2 from biggest → smallest
    # Example 4×4 → [8, 4, 2, 1]
    VALUES = [2 ** i for i in range(BOARD - 1, -1, -1)]

    BOTTOM_LABELS = VALUES + [""]
    RIGHT_LABELS = VALUES + [""]

    run_original_main()


# ======================================================
# ORIGINAL CODE BELOW (unchanged except the delete feature)
# ======================================================

def run_original_main():
    root = tk.Tk()
    root.title("Napier Binary Board – Dynamic Size (Option B)")

    width = GRID * CELL_SIZE
    height = GRID * CELL_SIZE

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    draw_board(canvas)

    tk.Button(root, text="Spawn Counter", font=("Arial", 14),
              command=lambda: spawn_checker(canvas)).pack(pady=10)

    root.mainloop()


class DraggableChecker:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(
            x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
            x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
            fill="white", outline="black", width=2
        )
        self.dragging = False

        canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(self.id, "<ButtonPress-3>", self.delete_self)

    def delete_self(self, event):
        self.canvas.delete(self.id)

    def on_press(self, event):
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if not self.dragging:
            return
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.id, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

    def on_release(self, event):
        self.dragging = False
        self.snap_to_grid()

    def snap_to_grid(self):
        bbox = self.canvas.coords(self.id)
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2

        col = floor(cx / CELL_SIZE)
        row = floor(cy / CELL_SIZE)

        col = max(0, min(GRID - 1, col))
        row = max(0, min(GRID - 1, row))

        snap_x = col * CELL_SIZE + CELL_SIZE // 2
        snap_y = row * CELL_SIZE + CELL_SIZE // 2

        self.canvas.move(self.id, snap_x - cx, snap_y - cy)


def draw_board(canvas):
    # Draw checkerboard
    for r in range(BOARD):
        for c in range(BOARD):
            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color = "#d8b17a" if (r + c) % 2 == 0 else "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    # Bottom labels
    for c, label in enumerate(BOTTOM_LABELS):
        x1 = c * CELL_SIZE
        y1 = BOARD * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        if label != "":
            canvas.create_text(
                x1 + CELL_SIZE / 2,
                y1 + CELL_SIZE / 2,
                text=str(label),
                font=("Arial", 14, "bold")
            )

    # Right labels
    for r, label in enumerate(RIGHT_LABELS):
        x1 = BOARD * CELL_SIZE
        y1 = r * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        if label != "":
            canvas.create_text(
                x1 + CELL_SIZE / 2,
                y1 + CELL_SIZE / 2,
                text=str(label),
                font=("Arial", 14, "bold")
            )


def spawn_checker(canvas):
    DraggableChecker(canvas, CELL_SIZE * 0.5, CELL_SIZE * (BOARD + 0.5))


# Start program:
if __name__ == "__main__":
    choose_board_size()
