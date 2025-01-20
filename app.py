import tkinter as tk
import random
from tkinter import filedialog
import requests


class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Főoldal")
        self.root.geometry("400x300")

        self.size_label = tk.Label(root, text="Pálya mérete (sor x oszlop):")
        self.rows_entry = tk.Entry(root)
        self.rows_entry.insert(0, "10")
        self.cols_entry = tk.Entry(root)
        self.cols_entry.insert(0, "10")
        self.set_size_button = tk.Button(root, text="Pálya létrehozása", command=self.create_new_board)
        self.load_button = tk.Button(self.root, text="Pálya betöltése szerverről", command=self.load_board_from_server)
        self.load_file_button = tk.Button(self.root, text="Pálya betöltése fájlból", command=self.load_board_from_file)
        self.exit_button = tk.Button(root, text="Kilépés", command=self.shutdown)
        
        self.size_label.pack(pady=10)
        self.rows_entry.pack(pady=10)
        self.cols_entry.pack(pady=10)
        self.set_size_button.pack(pady=10)
        self.load_button.pack(pady=10)
        self.load_file_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    def create_new_board(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
            self.root.destroy()
            root = tk.Tk()
            app = GameBoard(root, self)
            app.create_board(rows, cols)
            root.mainloop()
        except ValueError:
            self.size_label.config(text="Pozitív egész számokat adj meg!")

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
            self.root.destroy()
            root = tk.Tk()
            app = GameBoard(root, self)
            app.create_board(rows, cols)
            app.grid = new_grid
            app.create_table()
            root.mainloop()
        except Exception as e:
            self.size_label.config(text=f"Hiba a szerverről való betöltéskor: {e}")

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
            self.root.destroy()
            root = tk.Tk()
            app = GameBoard(root, self)
            app.create_board(rows, cols)
            app.grid = new_grid
            app.create_table()
            root.mainloop()

        except Exception as e:
            self.size_label.config(text=f"Hiba a fájl betöltésekor: {e}")

    def run(self):
        self.root.mainloop()
        
    def shutdown(self) -> None:
        self.root.destroy()

class GameBoard:
    def __init__(self, root, main_page):
        self.root = root
        self.main_page = main_page
        self.root.title("Pálya Generáló")

        self.canvas = None
        self.board_size = (0, 0)
        self.cell_size = 30
        self.obstacle_color = "magenta"
        self.green_cell_color = "green"
        self.blue_cell_color = "blue"
        self.grid = []
        self.is_selecting = False

        self.random_button = None
        self.save_button = None
        self.mirror_v_button = None
        self.mirror_h_button = None
        self.rotate_button = None
        
        self.select_area_button = None  
        self.load_area_button = None
        self.first_cell = None  
        self.second_cell = None 
        self.green_cell = None  
        self.blue_cell = None 

    def create_board(self, rows, cols):
        try:
            if rows <= 0 or cols <= 0:
                raise ValueError
            self.board_size = (rows, cols)
            self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
            self.add_green_and_blue_cells()

            if self.canvas:
                self.canvas.destroy()
            self.canvas = tk.Canvas(self.root, width=cols * self.cell_size, height=rows * self.cell_size)
            self.canvas.pack()
            self.create_table()
            
    

            if self.random_button:
                self.random_button.destroy()
            self.random_button = tk.Button(self.root, text="Random falak", command=self.add_random_walls)
            self.random_button.pack(pady=10)
            self.canvas.bind("<Button-1>", self.reserve_block)

            if not self.save_button:
                self.save_button = tk.Button(self.root, text="Mentés", command=self.save_board)
                self.save_button.pack(pady=10)
            
            if not self.mirror_v_button:
                self.mirror_v_button = tk.Button(self.root, text="Függőleges tükrözés", command=self.mirror_vertical)
                self.mirror_v_button.pack(pady=10)

            if not self.mirror_h_button:
                self.mirror_h_button = tk.Button(self.root, text="Vízszintes tükrözés", command=self.mirror_horizontal)
                self.mirror_h_button.pack(pady=10)

            if not self.rotate_button:
                self.rotate_button = tk.Button(self.root, text="90 fokos forgatás", command=self.rotate_90)
                self.rotate_button.pack(pady=10)
                
            if not self.select_area_button:
                self.select_area_button = tk.Button(self.root, text="Terület kijelölése", command=self.enable_select_area)
                self.select_area_button.pack(pady=10)
                
            if not self.load_area_button:
                self.load_area_button = tk.Button(self.root, text="Terület betöltése", command=self.load_selected_area)
                self.load_area_button.pack(pady=10)
                
            self.back_button = tk.Button(self.root, text="Vissza a főoldalra", command=self.back_to_main_page)
            self.back_button.pack(pady=(10, 0))        
                
        except ValueError:
            self.main_page.size_label.config(text="Pozitív egész számokat adj meg!")

    
    def create_table(self):
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.grid[row][col] == 1:
                    color = self.obstacle_color
                elif self.grid[row][col] == 2:
                    color = "blue"
                elif self.grid[row][col] == 3:
                    color = "green"
                else:
                    color = "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")


    def add_green_and_blue_cells(self):
        rows, cols = self.board_size
        while True:
            green_row = random.randint(0, rows - 1)
            green_col = random.randint(0, cols - 1)
            blue_row = random.randint(0, rows - 1)
            blue_col = random.randint(0, cols - 1)
            if (green_row, green_col) != (blue_row, blue_col): 
                break
        self.grid[green_row][green_col] = 3  
        self.grid[blue_row][blue_col] = 2    
        
    def add_random_walls(self):
        self.clear_grid()
        num_walls = random.randint(1, (self.board_size[0] * self.board_size[1]) // 2)
        for _ in range(num_walls):
            while True:
                row = random.randint(0, self.board_size[0] - 1)
                col = random.randint(0, self.board_size[1] - 1)
                if self.grid[row][col] == 0:  # fal csak ures cellara
                    self.grid[row][col] = 1
                    break
        self.create_table()

    def reserve_block(self, event):
        x, y = event.x, event.y
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.board_size[0] and 0 <= col < self.board_size[1]:
            if self.grid[row][col] not in (2, 3):  # kek/zold cellara nem lesz fal
                self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
                self.create_table()

    def clear_grid(self):
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                if self.grid[row][col] not in (2, 3):  # ha nem kek v zold a cella akkor clear
                    self.grid[row][col] = 0

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
    
    def back_to_main_page(self):
        self.root.destroy()
        new_root = tk.Tk()
        main_page = MainPage(new_root)
        main_page.run()
        
    def enable_select_area(self):
        """Aktiválja a terület kijelölésének módját."""
        self.first_cell = None
        self.second_cell = None
        self.canvas.bind("<Button-1>", self.select_cell)
        self.select_area_button.config(state=tk.DISABLED)  # kijelolo gomb kikapcs

    def select_cell(self, event):
        """cellak kijelolese."""
        x, y = event.x, event.y
        row = y // self.cell_size
        col = x // self.cell_size
        
        if 0 <= row < self.board_size[0] and 0 <= col < self.board_size[1]:
            if not self.first_cell:
                self.first_cell = (row, col)
                self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size, 
                                              (col + 1) * self.cell_size, (row + 1) * self.cell_size, 
                                              outline="yellow", width=2)
            elif not self.second_cell:
                self.second_cell = (row, col)
                self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size, 
                                              (col + 1) * self.cell_size, (row + 1) * self.cell_size, 
                                              outline="yellow", width=2)
                self.save_selected_area()  
                self.canvas.unbind("<Button-1>")  
                self.select_area_button.config(state=tk.NORMAL)  # gomb visszakapcsolas

    def save_selected_area(self):
        """ket cella kozotti terulet mentes."""
        if self.first_cell and self.second_cell:
            row1, col1 = self.first_cell
            row2, col2 = self.second_cell

            # terulet koordinatak
            top_left = (min(row1, row2), min(col1, col2))
            bottom_right = (max(row1, row2), max(col1, col2))

            # mentes
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    for row in range(top_left[0], bottom_right[0] + 1):
                        file.write(' '.join(str(self.grid[row][col]) for col in range(top_left[1], bottom_right[1] + 1)) + '\n')
                        
    def load_selected_area(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                data = file.readlines()
            
            for i, line in enumerate(data):
                row_data = list(map(int, line.strip().split()))
                for j, value in enumerate(row_data):
                    if 0 <= i < self.board_size[0] and 0 <= j < self.board_size[1]:
                        self.grid[i][j] = value
            
            self.create_table()  
    

if __name__ == "__main__":
    root = tk.Tk()
    main_page = MainPage(root)
    main_page.run()