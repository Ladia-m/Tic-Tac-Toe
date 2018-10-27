#!/usr/bin/env python
import os
from tkinter import *
from string import ascii_uppercase
import sys
from tkinter import messagebox

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
        self.master.title("Connect four!!")
        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        topbar.add_command(label="Exit", command=self.client_exit)
        topbar.add_command(label="About", command=self.client_about)

        self.img = PhotoImage(file='data/gifs/connect4')

        logo = Label(self.master, image=self.img)
        logo.grid(row=0, column=1, pady=10, padx=10)

        entry1label = Label(self.master, text="Enter size (5-10):")
        entry1label.grid(row=1, column=1, padx=100)

        self.entry1 = Entry(self.master)
        self.entry1.config(width=18)
        self.entry1.bind('<Return>', lambda e: entry_button.config(self.size_test()))
        self.entry1.grid(row=2, column=1)

        self.confirm_img = PhotoImage(file='data/gifs/ok')
        entry_button = Button(self.master, padx=4, command=self.size_test)
        entry_button.config(image=self.confirm_img, compound='left')
        entry_button.grid(row=5, column=1, rowspan=4)

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

        def draw_shape(shape, x, y ,magic_number=3):
            lettery = UPPERCASE_ASCII[y]
            x = x * self.square_size
            y = y * self.square_size
            self.bottom_infotable = Label(game_window)
            self.bottom_infotable.grid(row=4, column=1, pady=5)

            if shape == "X":
                grid_canvas.create_oval(x + magic_number,
                                        y + magic_number,
                                        x + self.square_size - magic_number,
                                        y + self.square_size - magic_number,
                                        outline='black', fill='yellow',
                                        width=magic_number)
                self.lastPlayer = 0
                self.top_infotable.configure(text='Player 1 is on turn.')
                self.bottom_infotable.configure(text="Player 2 played cell {}, {}".format(lettery, x // 25 + 1))

            elif shape == "O":
                grid_canvas.create_oval(x + magic_number,
                                        y + magic_number,
                                        x + self.square_size - magic_number,
                                        y + self.square_size - magic_number,
                                        outline='black', fill='red',
                                        width=magic_number)
                self.lastPlayer = 1
                self.top_infotable.configure(text='Player 2 is on turn.')
                self.bottom_infotable.configure(text="Player 1 played cell {}, {}".format(lettery, x // 25 + 1))

        def mouse_click(event):
            y, x = event.x, event.y
            y = y // self.square_size
            x = x // self.square_size


            if self.playGrid[x][y] == 2:
                if self.lastPlayer == 1:       # 1 == x
                    draw_shape("X", y, x)
                    self.playGrid[x][y] = 1
                else:
                    draw_shape("O", y, x)      # 0 == O
                    self.playGrid[x][y] = 0
            else:
                self.bottom_infotable.configure(text='Cell is already occupied!')   # 2 == occupied

        UPPERCASE_ASCII = ascii_uppercase

        game_window = Toplevel(self)
        game_window.title("You are playing size {} x {}".format(field_size, field_size))

        topbar = Menu(game_window)
        game_window.config(menu=topbar)
        topbar.add_command(label="Restart Game", command=self.client_restart)
        self.top_infotable = Label(game_window, text='Waiting for your first move:')
        self.top_infotable.grid(row=11, column=1)

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
            letter = UPPERCASE_ASCII[counter - 1]
            vertical_label.create_text(x, y, text=letter)
            counter += 1
        vertical_label.grid(row=1, column=0)

        grid_canvas.bind("<Button-1>", mouse_click)

    def client_exit(self):
        sys.exit()

    def client_restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def client_about(self):
        messagebox.showinfo("About", "Connect4 - Miko 2018\n Version 0.5\n")


if __name__ == '__main__':
    root = Tk()
    CFive = Main_window(root)
    CFive.mainloop()
