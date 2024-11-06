import tkinter as tk
import random

#Működés megéréséhez hagytam bent a saját kommentjeimet.

class GameBoard:
    def __init__(self, root):
        # root elem létrehozása
        self.root = root
        self.root.title("Pálya Generáló") # ez lesz az ablak neve

        
        ##### pálya méretének megadása blokk #####
        #### pack metódus középre helyez      ####
        ### insert kezdeti szöveg megadása     ###
        self.size_label = tk.Label(root, text="Pálya mérete (sor x oszlop):")
        self.size_label.pack()

        self.rows_entry = tk.Entry(root)
        self.rows_entry.pack()
        self.rows_entry.insert(0, "Sorok")

        self.cols_entry = tk.Entry(root)
        self.cols_entry.pack()
        self.cols_entry.insert(0, "Oszlopok")
        ##### blokk vége #####


        ##### pálya létrehozása blokk         #####
        #### gomb elhelyezése + függvény hivás ####
        self.set_size_button = tk.Button(root, text="Pálya létrehozása", command=self.create_board)
        self.set_size_button.pack()

        self.canvas = None
        self.board_size = (0, 0)    # pálya méret
        self.cell_size = 30         # cella méret
        self.obstacle_color = "red" # foglalt cella szin
        self.grid = []              # cella állapotok
        
        self.random_button = None   # random foglalás gomb
        ##### blokk vége #####


    def create_board(self):
        try:
            rows = int(self.rows_entry.get())   # GameBoard-ban megadott értékek alapján kerül feltöltésre
            cols = int(self.cols_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
            self.board_size = (rows, cols)      # foglalás nélküli pálya generálás
            self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

            ##### pálya frissitése blokk            #####
            #### destroy törli a korábbi pályát      ####
            ### pack kitölti az ablakot a pályával    ###
            ## create_table kell a pálya létrehozásához   ##
            if self.canvas:
                self.canvas.destroy()
            self.canvas = tk.Canvas(self.root, width=cols * self.cell_size, height=rows * self.cell_size)
            self.canvas.pack()
            self.create_table()
            ##### blokk vége #####


            ##### gomb blokk                                     #####
            #### korábbi gombot törölni kell, mert duplázza       ####
            ### add_random_walls gomb a random falak generálásához ###
            ## egér bal kattra foglalja le a cellát                 ##
            if self.random_button:
                self.random_button.destroy()
            self.random_button = tk.Button(self.root, text="Véletlenszerű falak", command=self.add_random_walls)
            self.random_button.pack()
            self.canvas.bind("<Button-1>", self.reserve_block)
            ##### blokk vége #####


        except ValueError:
            self.size_label.config(text="Kérlek, adj meg pozitív egész számokat!")


    ##### pálya lértehozása függvény               #####
    #### row + col -> sor és oszlop                 ####
    ### x1 + y1 bal felső - x2 + y2 jobb alsó sarok  ###
    ## GameBoard-ból szedi ki a foglalt szint         ##
    # create_rectangle koordináták alapján kocka       #
    def create_table(self):
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white"
                if self.grid[row][col] == 1:
                    color = self.obstacle_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    ##### függvény vége #####


    ##### random falak generálása függvény     #####
    #### foglalások resetelése                  ####
    ### random falak testreszabása               ###
    ## num_walls -> foglalás random testreszabása ##
    def add_random_walls(self):
        self.clear_grid()
        num_walls = random.randint(1, (int(self.rows_entry.get()) * int(self.cols_entry.get())) // 2)
        for _ in range(num_walls):
            while True:
                row = random.randint(0, self.board_size[0] - 1)
                col = random.randint(0, self.board_size[1] - 1)
                if self.grid[row][col] == 0:
                    self.grid[row][col] = 1
                    break
        self.create_table()
    ##### függvény vége #####


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
            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            else:
                self.grid[row][col] = 0
            self.create_table()
    ##### függvény vége #####


    ##### összes akadály törlése függvény #####
    def clear_grid(self):
        self.grid = [[0 for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
    ##### függvény vége #####
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GameBoard(root)
    root.mainloop()
