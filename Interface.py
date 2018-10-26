#!/usr/bin/env Python
import os
from tkinter import *
from string import ascii_uppercase
import sys


class Main_window(Frame):
    counter = 0

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.playGrid = [] # player O = 0, player X = 1, empty = 2
        self.lastPlayer = 0
        self.square_size = 25
        self.init_window()
        self.grid(pady=20)

    def init_window(self):
        self.master.title("Connect five!")

        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        topbar.add_command(label="Exit", command=self.client_exit)

        self.img = PhotoImage(file='data/gifs/img.gif')
        logo = Label(self.master, image=self.img)
        logo.grid(row=0, column=1, pady=10, padx=10)

        entry1label = Label(self.master, text="Enter size (5-10):")
        entry1label.grid(row=1, column=1, padx=10)

        self.entry1 = Entry(self.master)
        self.entry1.config(width=10)
        self.entry1.grid(row=2, column=1)

        self.confirm_img = PhotoImage(file='data/gifs/1.gif')
        entry_button = Button(self.master, text="confirm",
                              padx=2, command=self.size_test)
        entry_button.config(image=self.confirm_img, compound='left')
        entry_button.grid(row=3, column=1)

    def size_test(self):
        error_message = Label(self.master, width=35)
        error_message.grid(row=4, column=1, padx=0)
        try:
            field_size = int(self.entry1.get())
            if field_size not in range(5, 11):
                error_message.configure(text='Size can be from 5x5 up to 10x10.')
                return None
        except ValueError:
            error_message.configure(text='Insert only whole #!')
            return None
        self.start_game(field_size)

    def start_game(self, field_size):

        def draw_cross(x, y):
            x = x * self.square_size
            y = y * self.square_size
            grid_canvas.create_line(x + 3,
                                    y + 3,
                                    x + self.square_size - 3,
                                    y + self.square_size - 3,
                                    fill='#0000ff',
                                    width=3)

            grid_canvas.create_line(x + self.square_size - 3,
                                    y + 3,
                                    x + 3,
                                    y + self.square_size - 3,
                                    fill='#0000ff',
                                    width=3)

        def draw_circle(x, y):
            x = x * self.square_size
            y = y * self.square_size
            grid_canvas.create_oval(x + 3,
                                    y + 3,
                                    x + self.square_size - 3,
                                    y + self.square_size - 3,
                                    outline='#ff0000',
                                    width=3)

        def mouse_click(event):
            y, x = event.x, event.y
            y = y // self.square_size
            x = x // self.square_size
            letterx = abc[x]

            if self.playGrid[x][y] == 2:
                if self.lastPlayer == 0:
                    draw_cross(y, x)
                    self.lastPlayer = 1
                    self.playGrid[x][y] = 1
                    top_infotable.configure(text='Player O is on turn.')
                    bottom_infotable.configure(text="X played cell {}, {}".format(letterx, y + 1))
                else:
                    draw_circle(y, x)
                    self.lastPlayer = 0
                    self.playGrid[x][y] = 0
                    top_infotable.configure(text='Player X is on turn.')
                    bottom_infotable.configure(text="O played cell {}, {}".format(letterx, y + 1))
            else:
                bottom_infotable.configure(text='Cell is already occupied!')

        abc = ascii_uppercase

        game_window = Toplevel(self)
        game_window.title("You are playing size {} x {}".format(field_size, field_size))

        topbar = Menu(game_window)
        game_window.config(menu=topbar)
        topbar.add_command(label="Restart Game", command=self.client_restart)

        for row in range(0, field_size):
            columns = []
            for column in range(0, field_size):
                columns.append(2)
            self.playGrid.append(columns)

        grid_width = field_size * self.square_size
        grid_height = grid_width
        grid_canvas = Canvas(game_window,
                             width=grid_width,
                             height=grid_height)
        grid_canvas.grid(row=1, column=1, padx=0, pady=0)
        grid_canvas.create_rectangle(0, 0, grid_width, grid_height, fill='#ffffff')
        for i in range(1, field_size):
            xy = self.square_size * i
            grid_canvas.create_line(xy, 0, xy, grid_height, fill="#000000")
            grid_canvas.create_line(0, xy, grid_width, xy, fill="#000000")


        label_width = field_size * self.square_size
        horizontal_label = Canvas(game_window,
                        width=label_width,
                        height=self.square_size)
        for num in range(1, field_size + 1):
            x = ((num - 1) * self.square_size) + self.square_size / 2
            y = self.square_size / 2
            horizontal_label.create_text(x, y, text=num)
        horizontal_label.grid(row=0, column=1)

        label_height = field_size * self.square_size
        vertical_label = Canvas(game_window,
                        width=self.square_size,
                        height=label_height)
        counter = 1
        while not counter > field_size:
            x = self.square_size / 2
            y = ((counter - 1) * self.square_size) + self.square_size / 2
            letter = abc[counter - 1]
            vertical_label.create_text(x, y, text=letter)
            counter += 1
        vertical_label.grid(row=1, column=0)

        if self.lastPlayer == 1:
            player = 'O'
        else:
            player = 'X'
        top_infotable = Label(game_window, text='Player {} is on turn.'.format(player))
        top_infotable.grid(row=3, column=1)
        bottom_infotable = Label(game_window)
        bottom_infotable.grid(row=4, column=1, pady=5)

        grid_canvas.bind("<Button-1>", mouse_click)

    def client_exit(self):
        sys.exit()

    def client_restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    root = Tk()
    CFive = Main_window(root)
    CFive.mainloop()
