import tkinter as tk
import random
from tkinter import filedialog
import requests

class GameBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Pálya Generáló")
 
        self.size_label = tk.Label(root, text="Pálya mérete (sor x oszlop):")
        self.size_label.pack()

        self.rows_entry = tk.Entry(root)
        self.rows_entry.pack()
        self.rows_entry.insert(0, "10")

        self.cols_entry = tk.Entry(root)
        self.cols_entry.pack()
        self.cols_entry.insert(0, "10")
        ##### pálya létrehozása blokk         #####
        #### gomb elhelyezése + függvény hivás ####
        self.set_size_button = tk.Button(root, text="Pálya létrehozása", command=self.create_board)
        self.set_size_button.pack()

        self.canvas = None
        self.board_size = (0, 0)
        self.cell_size = 30
        self.obstacle_color = "magenta"
        self.grid = []

        self.random_button = None
        self.save_button = None
        self.mirror_v_button = None
        self.mirror_h_button = None
        self.rotate_button = None
        self.load_button = tk.Button(self.root, text="Pálya betöltése szerverről", command=self.load_board_from_server)
        self.load_button.pack()
        self.load_file_button = tk.Button(self.root, text="Pálya betöltése fájlból", command=self.load_board_from_file)
        self.load_file_button.pack()
        
    def load_board_from_server(self):
        try:
            url = "szervercim"  
            response = requests.get(url)
            response.raise_for_status()  
            data = response.text
            new_grid = []
            for line in data.strip().split("\n"):
                new_grid.append(list(map(int, line.split())))
            rows, cols = len(new_grid), len(new_grid[0])
            if rows <= 0 or cols <= 0:
                raise ValueError("Hibás pályaadat.")

            self.grid = new_grid
            self.board_size = (rows, cols)
            self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)
            self.create_table()
        except Exception as e:
            self.size_label.config(text=f"Hiba a szerverrel: {e}")

    def load_board_from_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if not file_path: 
                return

            with open(file_path, 'r') as file:
                data = file.readlines()
            new_grid = []
            for line in data:
                new_grid.append(list(map(int, line.strip().split())))
            rows, cols = len(new_grid), len(new_grid[0])
            if any(len(row) != cols for row in new_grid): 
                raise ValueError("Érvénytelen pálya.")
            self.grid = new_grid
            self.board_size = (rows, cols)
            if self.canvas:
                self.canvas.destroy()
            self.canvas = tk.Canvas(self.root, width=cols * self.cell_size, height=rows * self.cell_size)
            self.canvas.pack()
            self.create_table()
        except Exception as e:
            self.size_label.config(text=f"Hiba a fájl betöltésekor: {e}")


    def create_board(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
            self.board_size = (rows, cols)
            self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

            if self.canvas:
                self.canvas.destroy()
            self.canvas = tk.Canvas(self.root, width=cols * self.cell_size, height=rows * self.cell_size)
            self.canvas.pack()
            self.create_table()

            if self.random_button:
                self.random_button.destroy()
            self.random_button = tk.Button(self.root, text="Random falak", command=self.add_random_walls)
            self.random_button.pack()
            self.canvas.bind("<Button-1>", self.reserve_block)

            if not self.save_button:
                self.save_button = tk.Button(self.root, text="Mentés", command=self.save_board)
                self.save_button.pack()
            
            if not self.mirror_v_button:
                self.mirror_v_button = tk.Button(self.root, text="Függőleges tükrözés", command=self.mirror_vertical)
                self.mirror_v_button.pack()

            if not self.mirror_h_button:
                self.mirror_h_button = tk.Button(self.root, text="Vízszintes tükrözés", command=self.mirror_horizontal)
                self.mirror_h_button.pack()

            if not self.rotate_button:
                self.rotate_button = tk.Button(self.root, text="90 fokos forgatás", command=self.rotate_90)
                self.rotate_button.pack()

        except ValueError:
            self.size_label.config(text="Pozitív egész számokat adj meg!")
            
##### pálya lértehozása függvény               #####
    #### row + col -> sor és oszlop                 ####
    ### x1 + y1 bal felső - x2 + y2 jobb alsó sarok  ###
    ## GameBoard-ból szedi ki a foglalt szint         ##
    # create_rectangle koordináták alapján kocka 
    def create_table(self):
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black"
                if self.grid[row][col] == 1:
                    color = self.obstacle_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")
##### random falak generálása függvény     #####
    #### foglalások resetelése                  ####
    ### random falak testreszabása               ###
    ## num_walls -> foglalás random testreszabása #
    def add_random_walls(self):
        self.clear_grid()
        num_walls = random.randint(1, (self.board_size[0] * self.board_size[1]) // 2)
        for _ in range(num_walls):
            while True:
                row = random.randint(0, self.board_size[0] - 1)
                col = random.randint(0, self.board_size[1] - 1)
                if self.grid[row][col] == 0:
                    self.grid[row][col] = 1
                    break
        self.create_table()

##### foglalás kattra függvény     #####
    #### event lesz a katt koordinátája ####
    ### koordináta ellenőrzés            ###
    ## foglalás érték megforditás         ##
    # tábla létrehozása                    #
    def reserve_block(self, event):
        x, y = event.x, event.y
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.board_size[0] and 0 <= col < self.board_size[1]:
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
            self.create_table()

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]

    def save_board(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for row in self.grid:
                    file.write(' '.join(map(str, row)) + '\n')

    def mirror_vertical(self):
        self.grid = [row[::-1] for row in self.grid]
        self.create_table()

    def mirror_horizontal(self):
        self.grid = self.grid[::-1]
        self.create_table()

    def rotate_90(self):
        cols, rows = len(self.grid[0]), len(self.grid)
        rotated_grid = [[self.grid[rows - j - 1][i] for j in range(rows)] for i in range(cols)]
        self.grid = rotated_grid
        self.board_size = (cols, rows)  
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)
        self.create_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameBoard(root)
    root.mainloop()
