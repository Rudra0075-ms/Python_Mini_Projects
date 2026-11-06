import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import chess


class ChessGUI:
    LIGHT = "#EEEED2"
    DARK = "#769656"
    SELECTED = "#F6F669"
    LEGAL = "#A9D18E"
    CAPTURE = "#E57373"
    LAST = "#CDD26A"
    CHECK = "#E85D5D"
    BG = "#20242B"
    PANEL = "#2B313B"
    BUTTON = "#394552"
    WHITE_PIECE = "#FFFDF2"
    BLACK_PIECE = "#151515"
    WHITE_OUTLINE = "#303030"
    BLACK_OUTLINE = "#E8E8E8"

    # Filled symbols are used for both sides, then recolored and outlined.
    SYMBOLS = {
        chess.KING: "♚", chess.QUEEN: "♛", chess.ROOK: "♜",
        chess.BISHOP: "♝", chess.KNIGHT: "♞", chess.PAWN: "♟"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess")
        self.root.configure(bg=self.BG)
        self.root.minsize(760, 570)

        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        width, height = min(1120, sw - 60), min(850, sh - 90)
        x, y = max(0, (sw - width) // 2), max(0, (sh - height) // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        self.board = chess.Board()
        self.selected = None
        self.legal_moves = []
        self.last_move = None
        self.game_over = False
        self.flipped = False
        self.resize_job = None
        self.board_x = self.board_y = 0
        self.square_size = 60
        self.piece_family = self.find_piece_font()

        self.create_ui()
        self.bind_shortcuts()
        self.root.after(100, self.resize_board)

    def find_piece_font(self):
        available = set(tkfont.families(self.root))
        for name in ("DejaVu Sans", "Segoe UI Symbol", "Arial Unicode MS"):
            if name in available:
                return name
        return "TkDefaultFont"

    def create_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        tk.Label(self.root, text="♟  PYTHON CHESS", font=(self.piece_family, 22, "bold"),
                 bg=self.BG, fg="white").grid(row=0, column=0, pady=(12, 6))

        main = tk.Frame(self.root, bg=self.BG)
        main.grid(row=1, column=0, sticky="nsew", padx=16, pady=5)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=1, minsize=250)

        board_box = tk.Frame(main, bg=self.BG)
        board_box.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        self.canvas = tk.Canvas(board_box, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Configure>", self.schedule_resize)

        side = tk.Frame(main, bg=self.PANEL, padx=14, pady=14)
        side.grid(row=0, column=1, sticky="nsew")
        side.grid_columnconfigure(0, weight=1)
        side.grid_rowconfigure(3, weight=1)

        tk.Label(side, text="GAME STATUS", font=("Arial", 13, "bold"),
                 bg=self.PANEL, fg="white").grid(row=0, column=0, pady=(0, 8))
        self.status = tk.Label(side, text="White to move", font=("Arial", 12, "bold"),
                               bg="#303640", fg="white", height=3, wraplength=220)
        self.status.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        tk.Label(side, text="MOVE HISTORY", font=("Arial", 13, "bold"),
                 bg=self.PANEL, fg="white").grid(row=2, column=0, pady=(0, 8))

        history_box = tk.Frame(side, bg=self.PANEL)
        history_box.grid(row=3, column=0, sticky="nsew")
        history_box.grid_rowconfigure(0, weight=1)
        history_box.grid_columnconfigure(0, weight=1)
        self.history = tk.Listbox(history_box, font=("Consolas", 11), bg="#303640",
                                  fg="white", selectbackground="#596779",
                                  highlightthickness=0, relief="flat")
        self.history.grid(row=0, column=0, sticky="nsew")
        scroll = tk.Scrollbar(history_box, command=self.history.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.history.config(yscrollcommand=scroll.set)

        controls = tk.Frame(self.root, bg=self.BG)
        controls.grid(row=2, column=0, pady=(6, 12))
        items = [("↶ Undo", self.undo_move), ("↻ Restart", self.restart_game),
                 ("⇅ Flip", self.flip_board), ("Claim Draw", self.claim_draw),
                 ("Resign", self.resign)]
        for col, (text, command) in enumerate(items):
            tk.Button(controls, text=text, command=command, font=("Arial", 10, "bold"),
                      bg=self.BUTTON, fg="white", activebackground="#596779",
                      activeforeground="white", width=12, pady=8, relief="flat",
                      cursor="hand2").grid(row=0, column=col, padx=4)

    def bind_shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self.undo_move())
        self.root.bind("<Control-r>", lambda e: self.restart_game())
        self.root.bind("<Control-f>", lambda e: self.flip_board())
        self.root.bind("<Escape>", lambda e: self.cancel_selection())

    def schedule_resize(self, event=None):
        if self.resize_job:
            self.root.after_cancel(self.resize_job)
        self.resize_job = self.root.after(40, self.resize_board)

    def resize_board(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        available = max(280, min(w, h) - 24)
        self.square_size = max(35, available // 8)
        pixels = self.square_size * 8
        self.board_x, self.board_y = max(8, (w - pixels) // 2), max(8, (h - pixels) // 2)
        self.draw_board()

    def display_to_square(self, row, col):
        file_index = 7 - col if self.flipped else col
        rank_index = row if self.flipped else 7 - row
        return chess.square(file_index, rank_index)

    def draw_piece(self, x, y, piece):
        symbol = self.SYMBOLS[piece.piece_type]
        size = max(24, int(self.square_size * 0.68))
        fill = self.WHITE_PIECE if piece.color else self.BLACK_PIECE
        outline = self.WHITE_OUTLINE if piece.color else self.BLACK_OUTLINE
        # Eight outline copies make every piece, especially pawns, visible on both colors.
        stroke = max(1, self.square_size // 32)
        for dx, dy in ((-stroke, 0), (stroke, 0), (0, -stroke), (0, stroke),
                       (-stroke, -stroke), (-stroke, stroke),
                       (stroke, -stroke), (stroke, stroke)):
            self.canvas.create_text(x + dx, y + dy, text=symbol,
                                    font=(self.piece_family, size), fill=outline)
        self.canvas.create_text(x, y, text=symbol,
                                font=(self.piece_family, size), fill=fill)

    def draw_board(self):
        self.canvas.delete("all")
        targets = {m.to_square for m in self.legal_moves}
        captures = {m.to_square for m in self.legal_moves if self.board.is_capture(m)}
        checked_king = self.board.king(self.board.turn) if self.board.is_check() else None

        for row in range(8):
            for col in range(8):
                square = self.display_to_square(row, col)
                x1 = self.board_x + col * self.square_size
                y1 = self.board_y + row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                color = self.LIGHT if (row + col) % 2 == 0 else self.DARK
                if self.last_move and square in (self.last_move.from_square, self.last_move.to_square):
                    color = self.LAST
                if square in targets:
                    color = self.CAPTURE if square in captures else self.LEGAL
                if square == self.selected:
                    color = self.SELECTED
                if square == checked_king:
                    color = self.CHECK
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                piece = self.board.piece_at(square)
                if piece:
                    self.draw_piece((x1 + x2) / 2, (y1 + y2) / 2, piece)

                label_color = self.DARK if (row + col) % 2 == 0 else self.LIGHT
                label_size = max(8, self.square_size // 8)
                if row == 7:
                    file_name = chess.FILE_NAMES[chess.square_file(square)]
                    self.canvas.create_text(x2 - 4, y2 - 2, text=file_name, anchor="se",
                                            font=("Arial", label_size, "bold"), fill=label_color)
                if col == 0:
                    rank = str(chess.square_rank(square) + 1)
                    self.canvas.create_text(x1 + 4, y1 + 2, text=rank, anchor="nw",
                                            font=("Arial", label_size, "bold"), fill=label_color)
        self.update_status()

    def canvas_click(self, event):
        if self.game_over:
            return
        col = (event.x - self.board_x) // self.square_size
        row = (event.y - self.board_y) // self.square_size
        if 0 <= row < 8 and 0 <= col < 8:
            self.square_click(self.display_to_square(row, col))

    def square_click(self, square):
        piece = self.board.piece_at(square)
        if self.selected is None:
            if piece and piece.color == self.board.turn:
                self.select_square(square)
            return
        if piece and piece.color == self.board.turn:
            self.select_square(square)
            return
        moves = [m for m in self.legal_moves if m.to_square == square]
        if not moves:
            self.cancel_selection()
        elif any(m.promotion for m in moves):
            self.choose_promotion(moves)
        else:
            self.make_move(moves[0])

    def select_square(self, square):
        self.selected = square
        self.legal_moves = [m for m in self.board.legal_moves if m.from_square == square]
        self.draw_board()

    def cancel_selection(self):
        self.selected, self.legal_moves = None, []
        self.draw_board()

    def choose_promotion(self, moves):
        window = tk.Toplevel(self.root)
        window.title("Pawn Promotion")
        window.configure(bg=self.PANEL)
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()
        tk.Label(window, text="Choose promotion piece", font=("Arial", 13, "bold"),
                 bg=self.PANEL, fg="white").pack(padx=25, pady=14)
        for name, piece_type in (("Queen", chess.QUEEN), ("Rook", chess.ROOK),
                                 ("Bishop", chess.BISHOP), ("Knight", chess.KNIGHT)):
            move = next(m for m in moves if m.promotion == piece_type)
            tk.Button(window, text=name, width=16, pady=6, bg=self.BUTTON, fg="white",
                      activebackground="#596779", activeforeground="white", relief="flat",
                      command=lambda m=move: self.finish_promotion(window, m)).pack(pady=3)
        window.protocol("WM_DELETE_WINDOW", lambda: self.cancel_promotion(window))

    def finish_promotion(self, window, move):
        window.destroy()
        self.make_move(move)

    def cancel_promotion(self, window):
        window.destroy()
        self.cancel_selection()

    def make_move(self, move):
        if move not in self.board.legal_moves:
            return
        san = self.board.san(move)
        number, white = self.board.fullmove_number, self.board.turn == chess.WHITE
        self.board.push(move)
        self.last_move = move
        if white:
            self.history.insert(tk.END, f"{number}. {san}")
        else:
            i = self.history.size() - 1
            if i >= 0:
                old = self.history.get(i)
                self.history.delete(i)
                self.history.insert(tk.END, f"{old:<18} {san}")
            else:
                self.history.insert(tk.END, f"{number}... {san}")
        self.history.see(tk.END)
        self.selected, self.legal_moves = None, []
        self.draw_board()

    def update_status(self):
        if self.game_over:
            return
        outcome = self.board.outcome(claim_draw=False)
        if outcome:
            self.game_over = True
            result = "DRAW" if outcome.winner is None else (
                "WHITE WINS" if outcome.winner == chess.WHITE else "BLACK WINS")
            reason = outcome.termination.name.replace("_", " ").title()
            self.status.config(text=f"{result}\n{reason}", bg="#344D3C")
            self.root.after(100, lambda: messagebox.showinfo(
                "Game Over", f"{result}\nReason: {reason}"))
            return
        player = "White" if self.board.turn else "Black"
        text = player + " to move" + ("\nCHECK!" if self.board.is_check() else "")
        self.status.config(text=text, bg="#713B3B" if self.board.is_check() else "#303640")

    def undo_move(self):
        if not self.board.move_stack:
            messagebox.showinfo("Undo", "There are no moves to undo.")
            return
        self.board.pop()
        self.last_move = self.board.peek() if self.board.move_stack else None
        self.selected, self.legal_moves, self.game_over = None, [], False
        self.rebuild_history()
        self.draw_board()

    def rebuild_history(self):
        self.history.delete(0, tk.END)
        temp, entries = chess.Board(), []
        for move in self.board.move_stack:
            san = temp.san(move)
            if temp.turn == chess.WHITE:
                entries.append([temp.fullmove_number, san, ""])
            elif entries:
                entries[-1][2] = san
            temp.push(move)
        for number, white, black in entries:
            text = f"{number}. {white}"
            self.history.insert(tk.END, f"{text:<18} {black}" if black else text)
        self.history.see(tk.END)

    def restart_game(self):
        if not messagebox.askyesno("Restart", "Restart the current game?"):
            return
        self.board.reset()
        self.selected, self.legal_moves = None, []
        self.last_move, self.game_over = None, False
        self.history.delete(0, tk.END)
        self.draw_board()

    def flip_board(self):
        self.flipped = not self.flipped
        self.draw_board()

    def claim_draw(self):
        if self.game_over:
            return
        if self.board.can_claim_draw():
            self.game_over = True
            self.status.config(text="GAME DRAW\nDraw claimed", bg="#344D3C")
            messagebox.showinfo("Draw", "The draw was successfully claimed.")
        else:
            messagebox.showwarning("Draw", "A draw cannot currently be claimed.")

    def resign(self):
        if self.game_over:
            return
        player = "White" if self.board.turn else "Black"
        if not messagebox.askyesno("Resign", f"Should {player} resign?"):
            return
        winner = "Black" if self.board.turn else "White"
        self.game_over = True
        self.status.config(text=f"{winner.upper()} WINS\nOpponent resigned", bg="#344D3C")
        messagebox.showinfo("Game Over", f"{winner} wins by resignation.")


if __name__ == "__main__":
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()
