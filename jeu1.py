import tkinter as tk
from tkinter import messagebox
import json
import random
import os
import winsound  

def in_bounds(n, r, c):
    return 0 <= r < n and 0 <= c < n

def path_clear(board, sr, sc, dr, dc):
    drow, dcol = dr - sr, dc - sc
    if not (drow == 0 or dcol == 0 or abs(drow) == abs(dcol)):
        return False
    step_r = 0 if drow == 0 else (1 if drow > 0 else -1)
    step_c = 0 if dcol == 0 else (1 if dcol > 0 else -1)
    r, c = sr + step_r, sc + step_c
    while (r, c) != (dr, dc):
        if board[r][c] != 0:
            return False
        r += step_r
        c += step_c
    return True

def moves_from(board, n, r, c):
    res = []
    dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        while in_bounds(n, nr, nc) and board[nr][nc] == 0:
            res.append((nr, nc))
            nr += dr
            nc += dc
    return res

def has_moves(board, n, player):
    for r in range(n):
        for c in range(n):
            if board[r][c] == player and moves_from(board, n, r, c):
                return True
    return False

def initial_positions(n):
    if n == 6:
        red = [(0,1),(0,4),(1,0),(1,5)]
        blue= [(4,0),(4,5),(5,1),(5,4)]
    elif n == 8:
        red = [(0,2),(0,5),(2,0),(2,7)]
        blue= [(5,0),(5,7),(7,2),(7,5)]
    elif n == 10:
        red = [(0,3),(0,6),(3,0),(6,0)]
        blue= [(9,3),(9,6),(6,9),(3,9)]
    else:
        red, blue = [], []
    return red, blue

def play_move_sound():
    try:
        winsound.Beep(300, 80)  
    except:
        pass

def play_arrow_sound():
    try:
        winsound.Beep(450, 60)  
    except:
        pass

class jeu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jeu de Adama et Ilyass")

        # UI top controls
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=8, pady=6)
        tk.Label(top, text="Taille du plateau:").pack(side="left")
        self.size_var = tk.StringVar(value="6")
        tk.OptionMenu(top, self.size_var, "6", "8", "10").pack(side="left", padx=6)
        tk.Button(top, text="Nouvelle partie", command=self.new_game).pack(side="left", padx=8)
        tk.Button(top, text="Rejouer", command=self.replay).pack(side="left", padx=8)
        tk.Button(top, text="Sauvegarder", command=self.save_game).pack(side="left", padx=8)
        tk.Button(top, text="Charger", command=self.load_game).pack(side="left", padx=8)
        tk.Button(top, text="Mode IA", command=self.toggle_ai).pack(side="left", padx=8)

        self.info = tk.Label(self.root, text="Clique sur Nouvelle partie pour commencer.", anchor="w")
        self.info.pack(fill="x", padx=8, pady=4)

        # Etat du jeu
        self.n = 6
        self.cell = 70
        self.board = [[0]*self.n for _ in range(self.n)]
        self.turn = 1
        self.phase = "select"
        self.selected = None
        self.ai_mode = False
        self.possible_moves = []
        self.possible_arrows = []

        self.canvas = tk.Canvas(self.root, width=self.n*self.cell, height=self.n*self.cell, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()
        self.redraw()

    def save_game(self):
        data = {
            "n": self.n,
            "board": self.board,
            "turn": self.turn,
            "phase": self.phase,
            "selected": self.selected,
            "ai_mode": self.ai_mode
        }
        with open("jeu_save.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Sauvegarde", "Partie sauvegardée dans jeu_save.json")

    def load_game(self):
        if not os.path.exists("jeu_save.json"):
            messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")
            return
        with open("jeu_save.json", "r") as f:
            data = json.load(f)
        self.n = data["n"]
        self.board = data["board"]
        self.turn = data["turn"]
        self.phase = data["phase"]
        self.selected = tuple(data["selected"]) if data["selected"] else None
        self.ai_mode = data.get("ai_mode", False)
        self.canvas.config(width=self.n*self.cell, height=self.n*self.cell)
        self.possible_moves = []
        self.possible_arrows = []
        self.info.config(text="Partie chargée.")
        self.redraw()

    def toggle_ai(self):
        self.ai_mode = not self.ai_mode
        self.info.config(text=f"Mode IA : {'activé' if self.ai_mode else 'désactivé'}")
        if self.ai_mode and self.turn == 2:
            self.root.after(500, self.ai_play)

    def ai_play(self):
        if not self.ai_mode or self.turn != 2:
            return
        pieces = [(r, c) for r in range(self.n) for c in range(self.n)
                  if self.board[r][c] == 2 and moves_from(self.board, self.n, r, c)]
        if not pieces:
            self.switch_turn()
            return
        sr, sc = random.choice(pieces)
        mvs = moves_from(self.board, self.n, sr, sc)
        dr, dc = random.choice(mvs)

        self.board[sr][sc] = 0
        self.board[dr][dc] = 2
        play_move_sound()
        # tir
        arrow_cells = moves_from(self.board, self.n, dr, dc)
        if arrow_cells:
            ar, ac = random.choice(arrow_cells)
            self.board[ar][ac] = -1
            play_arrow_sound()
        self.selected = None
        self.phase = "select"
        self.possible_moves = []
        self.possible_arrows = []
        self.redraw()
        self.switch_turn()

    def set_size(self, n):
        self.n = n
        self.canvas.config(width=self.n*self.cell, height=self.n*self.cell)

    def new_game(self):
        n = int(self.size_var.get())
        self.set_size(n)
        self.board = [[0]*self.n for _ in range(self.n)]
        red, blue = initial_positions(self.n)
        for r, c in red:
            self.board[r][c] = 1
        for r, c in blue:
            self.board[r][c] = 2
        self.turn = 1
        self.phase = "select"
        self.selected = None
        self.possible_moves = []
        self.possible_arrows = []
        self.info.config(text="Rouge sélectionne un pion.")
        self.redraw()

    def replay(self):
        self.new_game()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                x1, y1 = j*self.cell, i*self.cell
                fill = "#EEE" if (i+j) % 2 == 0 else "#DDD"
                self.canvas.create_rectangle(x1, y1, x1+self.cell, y1+self.cell,
                                             outline="#999", fill=fill)

    def redraw(self):
        self.draw_grid()

        for (r, c) in self.possible_moves:
            x1, y1 = c*self.cell, r*self.cell
            self.canvas.create_rectangle(x1+5, y1+5, x1+self.cell-5, y1+self.cell-5,
                                         outline="yellow", width=2)
        for (r, c) in self.possible_arrows:
            x1, y1 = c*self.cell, r*self.cell
            self.canvas.create_rectangle(x1+5, y1+5, x1+self.cell-5, y1+self.cell-5,
                                         outline="orange", width=2)

        
        if self.selected:
            sr, sc = self.selected
            x1, y1 = sc*self.cell, sr*self.cell
            self.canvas.create_rectangle(x1, y1, x1+self.cell, y1+self.cell,
                                         outline="#f0a", width=3)

        
        for r in range(self.n):
            for c in range(self.n):
                v = self.board[r][c]
                x1, y1 = c*self.cell, r*self.cell
                cx, cy = x1 + self.cell//2, y1 + self.cell//2
                if v == 1:
                    self.canvas.create_oval(cx-20, cy-20, cx+20, cy+20,
                                            fill="red", outline="#900")
                elif v == 2:
                    self.canvas.create_oval(cx-20, cy-20, cx+20, cy+20,
                                            fill="blue", outline="#004")
                elif v == -1:
                    self.canvas.create_text(cx, cy, text="✖", fill="#333",
                                            font=("Arial", 18, "bold"))

    def on_click(self, event):
        if self.ai_mode and self.turn == 2:
            return  # tour de l'IA
        r, c = event.y // self.cell, event.x // self.cell
        if not in_bounds(self.n, r, c):
            return

        if self.phase == "select":
            if self.board[r][c] == self.turn:
                self.selected = (r, c)
                self.possible_moves = moves_from(self.board, self.n, r, c)
                self.possible_arrows = []
                self.phase = "move"
                self.info.config(text="Déplace le pion sélectionné.")
                self.redraw()

        elif self.phase == "move":
            if self.selected and (r, c) in self.possible_moves:
                sr, sc = self.selected
                if path_clear(self.board, sr, sc, r, c):
                    self.board[sr][sc] = 0
                    self.board[r][c] = self.turn
                    play_move_sound()  
                    self.selected = (r, c)
                    self.possible_moves = []
                    self.possible_arrows = moves_from(self.board, self.n, r, c)
                    self.phase = "arrow"
                    self.info.config(text="Tire une flèche pour bloquer une case.")
                    self.redraw()

        elif self.phase == "arrow":
            if self.selected and (r, c) in self.possible_arrows and self.board[r][c] == 0:
                sr, sc = self.selected
                if path_clear(self.board, sr, sc, r, c):
                    self.board[r][c] = -1
                    play_arrow_sound()  
                    self.selected = None
                    self.possible_arrows = []
                    self.phase = "select"
                    self.redraw()
                    self.switch_turn()
                    if self.ai_mode and self.turn == 2:
                        self.root.after(500, self.ai_play)

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1
        if not has_moves(self.board, self.n, self.turn):
            winner = "Bleu" if self.turn == 1 else "Rouge"
            self.info.config(text=f"Partie terminée — {winner} gagne.")
            if messagebox.askyesno("Fin de partie", f"{winner} gagne.\nRejouer ?"):
                self.replay()
            return
        self.info.config(text=("Bleu sélectionne un pion."
                               if self.turn == 2 else "Rouge sélectionne un pion."))

if __name__ == "__main__":
    jeu().root.mainloop()
