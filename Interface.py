#!/usr/bin/env python
import os
from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import sys

class GameController:
    def __init__(self, master, cell_size=None):
        self.master = master
        self.lastPlayer = 0
        self.cell_size = cell_size
        self.grid_size = None
        self.canvas = None
        self.top_infotable = None
        self.bottom_infotable = None
        self.abc = ascii_uppercase
        self.playGrid = []  # player O = 0, player X = 1, empty = 2
        self.playero_cells = []
        self.playerx_cells = []

    def play_grid_init(self, grid_size):
        self.grid_size = grid_size
        for row in range(0, self.grid_size):
            columns = []
            for column in range(0, self.grid_size):
                columns.append(2)
            self.playGrid.append(columns)

    def mouse_click(self, event):
        x, y = event.x, event.y
        y = y // self.cell_size
        x = x // self.cell_size
        letterx = ascii_uppercase[x]

        if self.playGrid[x][y] == 2:
            if self.lastPlayer == 0:
                self.draw_cross(x, y)
                self.lastPlayer = 1
                self.playGrid[x][y] = 1
                self.playerx_cells.append([x, y])
                self.top_infotable.configure(text='Player O is on turn.')
                self.bottom_infotable.configure(text="X played cell {}, {}".format(letterx, y + 1))
                self.end_game_test()
            else:
                self.draw_circle(x, y)
                self.lastPlayer = 0
                self.playGrid[x][y] = 0
                self.playero_cells.append([x, y])
                self.top_infotable.configure(text='Player X is on turn.')
                self.bottom_infotable.configure(text="O played cell {}, {}".format(letterx, y + 1))
                self.end_game_test()
        else:
            self.bottom_infotable.configure(text='Cell is already occupied!')

    def draw_cross(self, x, y):
        x = x * self.cell_size
        y = y * self.cell_size
        padding = self.cell_size // 8
        self.canvas.create_line(x + padding,
                                y + padding,
                                x + self.cell_size - padding,
                                y + self.cell_size - padding,
                                fill='#0000ff',
                                width=3)

        self.canvas.create_line(x + self.cell_size - padding,
                                y + padding,
                                x + padding,
                                y + self.cell_size - padding,
                                fill='#0000ff',
                                width=3)

    def draw_circle(self, x, y):
        padding = self.cell_size // 8
        x = x * self.cell_size
        y = y * self.cell_size
        self.canvas.create_oval(x + padding,
                                y + padding,
                                x + self.cell_size - padding,
                                y + self.cell_size - padding,
                                outline='#ff0000',
                                width=3)

    def end_game_test(self):
        for player_cells in self.playerx_cells, self.playero_cells:
            if player_cells == self.playerx_cells:
                player = 'X'
            else:
                player = 'O'
            if len(player_cells) >= 5:
                for position in player_cells:
                    finish_position = [position[0] + 4, position[1]]
                    if finish_position in player_cells:
                        between = []
                        for i in range(1, 4):
                            between.append((lambda l, x: [l[0] + x, l[1]])(position, i))
                        if all(i in player_cells for i in between):
                            self.end_game(player, position, finish_position)
                            return
                    finish_position = [position[0], position[1] + 4]
                    if finish_position in player_cells:
                        between = []
                        for i in range(1, 4):
                            between.append((lambda l, x: [l[0], l[1] + x])(position, i))
                        if all(i in player_cells for i in between):
                            self.end_game(player, position, finish_position)
                            return
                    finish_position = [position[0] + 4, position[1] + 4]
                    if finish_position in player_cells:
                        between = []
                        for i in range(1, 4):
                            between.append((lambda l, x: [l[0] + x, l[1] + x])(position, i))
                        if all(i in player_cells for i in between):
                            self.end_game(player, position, finish_position)
                            return
                    finish_position = [position[0] - 4, position[1] + 4]
                    if finish_position in player_cells:
                        between = []
                        for i in range(1, 4):
                            between.append((lambda l, x: [l[0] - x, l[1] + x])(position, i))
                        if all(i in player_cells for i in between):
                            self.end_game(player, position, finish_position)
                            return

    def end_game(self, player, start_position, finish_position):
        line_start_x = start_position[0] * self.cell_size + self.cell_size // 2
        line_start_y = start_position[1] * self.cell_size + self.cell_size // 2
        line_finish_x = finish_position[0] * self.cell_size + self.cell_size // 2
        line_finish_y = finish_position[1] * self.cell_size + self.cell_size // 2
        self.canvas.create_line(line_start_x, line_start_y, line_finish_x, line_finish_y,
                                width=5, fill='#000000')
        messagebox.showwarning(message='Player {} WON!!!'.format(player))
        self.top_infotable.configure(text='Player {} won!'.format(player))
        self.bottom_infotable.configure(text='Player {} won!'.format(player))


class MainWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(pady=5)
        self.cell_size = 25
        self.controller = GameController(self.master, self.cell_size)
        self.grid_size = None
        self.abc = ascii_uppercase
        self.active_window = 'init'

        self.init_frame = Frame(self.master)
        self.init_frame.grid()
        self.init_window()
        self.center_window()
        self.game_frame = Frame(self.master)

        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        topbar.add_command(label="Exit", command=sys.exit)
        topbar.add_command(label="Restart Game", command=self.client_restart)
        topbar.add_command(label="About", command=self.client_about)

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 0
        window_height = 0
        if self.active_window == 'init':
            # window_width = self.init_frame.winfo_reqwidth()
            # window_height = self.init_frame.winfo_reqheight()
            window_width = 200
            window_height = 200
        elif self.active_window == 'game':
            # window_width = self.game_frame.winfo_reqwidth()
            # window_height = self.game_frame.winfo_reqheight()
            window_width = self.grid_size * self.cell_size + 50
            window_height = window_width
            
        window_position_width = screen_width // 2 - window_width // 2
        window_position_height = screen_height // 2 - window_height // 2
        self.master.geometry("+{}+{}".format(window_position_width, window_position_height))

    def change_window(self):
        if self.active_window == 'init':
            self.active_window = 'game'
            self.init_frame.grid_forget()
            self.game_frame.grid()
            self.center_window()
        elif self.active_window == 'game':
            self.active_window = 'init'
            self.game_frame.grid_forget()
            self.init_frame.grid()
            self.center_window()

    def init_window(self):

        self.master.title("Piskvorky")

        self.img = PhotoImage(file='data/gifs/img.gif')
        logo = Label(self.init_frame, image=self.img)
        logo.grid(row=0, column=1, pady=10, padx=10)

        entry1label = Label(self.init_frame, text="Enter size (5-20):")
        entry1label.grid(row=1, column=1, padx=50)

        self.entry1 = Entry(self.init_frame)
        self.entry1.config(width=10)
        self.entry1.grid(row=2, column=1)
        self.entry1.focus()
        self.entry1.bind('<Return>', lambda e: entry_button.config(self.size_test()))

        self.confirm_img = PhotoImage(file='data/gifs/ok.gif')
        entry_button = Button(self.init_frame,
                              padx=2, command=self.size_test)
        entry_button.config(image=self.confirm_img, compound='left')
        entry_button.grid(row=3, column=1, pady=10)

    def size_test(self):
        error_message = Label(self.init_frame, width=30)
        error_message.grid(row=4, column=1, padx=0)
        try:
            self.grid_size = int(self.entry1.get())
            if self.grid_size not in range(5, 21):
                error_message.configure(text='Size can be from 5x5 up to 20x20.')
                return None
        except ValueError:
            error_message.configure(text='Insert only whole #!')
            return None
        self.controller.play_grid_init(self.grid_size)
        self.game_window()
        self.change_window()

    def game_window(self):

        grid_side = self.grid_size * self.cell_size
        grid_canvas = Canvas(self.game_frame,
                             width=grid_side,
                             height=grid_side)
        self.controller.canvas = grid_canvas
        grid_canvas.grid(row=1, column=1, padx=0, pady=0)
        grid_canvas.create_rectangle(0, 0, grid_side, grid_side, fill='#ffffff')

        for i in range(1, self.grid_size):
            xy = self.cell_size * i
            grid_canvas.create_line(xy, 0, xy, grid_side, fill="#000000")
            grid_canvas.create_line(0, xy, grid_side, xy, fill="#000000")

        label_height = self.grid_size * self.cell_size
        vertical_label = Canvas(self.game_frame,
                                  width=self.cell_size,
                                  height=label_height)
        for num in range(1, self.grid_size + 1):
            x = self.cell_size / 2
            y = ((num - 1) * self.cell_size) + self.cell_size / 2
            vertical_label.create_text(x, y, text=num)
        vertical_label.grid(row=1, column=0)

        label_width = self.grid_size * self.cell_size
        horizontal_label = Canvas(self.game_frame,
                                  width=label_width,
                                  height=self.cell_size)
        counter = 1
        while not counter > self.grid_size:
            x = ((counter - 1) * self.cell_size) + self.cell_size / 2
            y = self.cell_size / 2
            letter = self.abc[counter - 1]
            horizontal_label.create_text(x, y, text=letter)
            counter += 1
        horizontal_label.grid(row=0, column=1)

        if self.controller.lastPlayer == 1:
            player = 'O'
        else:
            player = 'X'
        top_infotable = Label(self.game_frame, text='Player {} is on turn.'.format(player))
        top_infotable.grid(row=3, column=1)
        self.controller.top_infotable = top_infotable
        bottom_infotable = Label(self.game_frame)
        bottom_infotable.grid(row=4, column=1, pady=5)
        self.controller.bottom_infotable = bottom_infotable

        grid_canvas.bind("<Button-1>", self.controller.mouse_click)

    def client_restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def client_about(self):
        messagebox.showinfo("About", "Piskvorky - Miko 2018\n Version 0.5\n")


if __name__ == '__main__':
    root = Tk()
    Piskvorky = MainWindow(root)
    Piskvorky.mainloop()
