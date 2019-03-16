#!/usr/bin/env python3
import os
from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
from random import randint
import sys
from BOT import BOT


class GameController:
    def __init__(self, master, cell_size=None):
        self.master = master
        self.cell_size = cell_size
        self.grid_size = None
        self.canvas = None
        self.top_infotable = None
        self.bottom_infotable = None
        self.abc = ascii_uppercase
        self.player_on_move = randint(1, 2)
        self.player_names = ['', 'O', 'X']
        self.playGrid = []  # circle = 1, cross = 2, empty = 0
        self.playero_cells = []
        self.playerx_cells = []
        self.bot_switch = 0
        self.game_over = False


    def play_grid_init(self, grid_size, bot_switch):
        self.grid_size = grid_size
        for row in range(0, self.grid_size):
            columns = []
            for column in range(0, self.grid_size):
                columns.append(0)
            self.playGrid.append(columns)
        self.bot_switch = bot_switch
        if self.bot_switch == 1:
            self.BOT = BOT(self.grid_size)
            if self.player_names[self.player_on_move] == 'PC':
                self.run_bot()

    def play_grid_click(self, event):
        valid_move = True
        if not self.game_over:
            x, y = event.x, event.y
            y = y // self.cell_size
            x = x // self.cell_size
            valid_move = self.next_turn(x, y)
        if self.bot_switch == 1 and valid_move and not self.game_over:
            self.run_bot([x, y])

    def run_bot(self, coordinates=None):
        x, y = self.BOT.play(coordinates)
        self.next_turn(x, y)

    def next_turn(self, x, y):
        letterx = ascii_uppercase[x]
        if self.playGrid[x][y] == 0:
            if self.player_on_move == 2:
                self.draw_cross(x, y)
                self.playGrid[x][y] = 2
                self.playerx_cells.append([x, y])
                self.top_infotable.configure(text='{} is on turn.'.format(self.player_names[1]))
                self.bottom_infotable.configure(text="{} played cell {}, {}".format(self.player_names[2],
                                                                                    letterx, y + 1))
                self.end_game_test()
                self.player_on_move = 1
                return True
            else:
                self.draw_circle(x, y)
                self.playGrid[x][y] = 1
                self.playero_cells.append([x, y])
                self.top_infotable.configure(text='{} is on turn.'.format(self.player_names[2]))
                self.bottom_infotable.configure(text="{} played cell {}, {}".format(self.player_names[1],
                                                                                    letterx, y + 1))
                self.end_game_test()
                self.player_on_move = 2
                return True
        else:
            self.bottom_infotable.configure(text='Cell is already occupied!')
            return False

    def draw_cross(self, x, y):
        x = x * self.cell_size
        y = y * self.cell_size
        padding = self.cell_size // 7
        line_width = self.cell_size // 8
        self.canvas.create_line(x + padding,
                                y + padding,
                                x + self.cell_size - padding,
                                y + self.cell_size - padding,
                                fill='#0000ff',
                                width=line_width)

        self.canvas.create_line(x + self.cell_size - padding,
                                y + padding,
                                x + padding,
                                y + self.cell_size - padding,
                                fill='#0000ff',
                                width=line_width)

    def draw_circle(self, x, y):
        x = x * self.cell_size
        y = y * self.cell_size
        padding = self.cell_size // 7
        line_width = self.cell_size // 8
        self.canvas.create_oval(x + padding,
                                y + padding,
                                x + self.cell_size - padding,
                                y + self.cell_size - padding,
                                outline='#ff0000',
                                width=line_width)

    def end_game_test(self):
        for player_cells in self.playerx_cells, self.playero_cells:
            if player_cells == self.playerx_cells:
                player = self.player_names[2]
            else:
                player = self.player_names[1]
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
        messagebox.showwarning(message='{} WON!!!'.format(player))
        self.top_infotable.configure(text='{} won!'.format(player))
        self.bottom_infotable.configure(text='{} won!'.format(player))
        self.game_over = True


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
        self.bot_switch = IntVar()
        self.bot_switch.set(0)

        self.init_frame = Frame(self.master)
        self.init_frame.grid()
        self.init_window()
        self.center_window()
        self.game_frame = Frame(self.master)
        self.game_frame.grid(padx=10)

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
        logo.grid(row=0, column=1)

        player_entry = Frame(self.init_frame)
        player_entry.grid(row=1, column=1, pady=10)
        player_entry_label = Label(player_entry, text="Names:")
        player_entry_label.grid(row=0, column=0, columnspan=3)
        self.player1_entry = Entry(player_entry, width=6)
        self.player1_entry.insert(0, self.controller.player_names[1])
        self.player1_entry.grid(row=1, column=0)
        self.player2_entry = Entry(player_entry, width=6)
        self.player2_entry.insert(0, self.controller.player_names[2])
        self.player2_entry.grid(row=1, column=2)
        player_canvas = Canvas(player_entry, width=65, height=30)
        player_canvas.grid(row=1, column=1)
        player_canvas.create_oval(5, 5, 25, 25, outline="#ff0000", width=5)
        player_canvas.create_line(33, 0, 33, 30, fill="#000000", width=3)
        player_canvas.create_line(40, 5, 60, 25, fill="#0000ff", width=5)
        player_canvas.create_line(60, 5, 40, 25, fill="#0000ff", width=5)

        entry1label = Label(self.init_frame, text="Enter size (5-20):")
        entry1label.grid(row=2, column=1, padx=50)

        self.entry1 = Entry(self.init_frame)
        self.entry1.config(width=10)
        self.entry1.grid(row=3, column=1)
        self.entry1.focus()
        self.entry1.bind('<Return>', lambda e: entry_button.config(self.start_game()))
        bot_choice_frame = Frame(self.init_frame)
        bot_label = Label(bot_choice_frame, text='Player vs PC:')
        bot_label.grid(row=0, column=0)
        bot_on_choice = Radiobutton(bot_choice_frame, text='ON', variable=self.bot_switch, value=1, command=self.set_bot_name)
        bot_on_choice.grid(row=0, column=1)
        bot_off_choice = Radiobutton(bot_choice_frame, text='OFF', variable=self.bot_switch, value=0, command=self.set_bot_name)
        bot_off_choice.grid(row=0, column=2)
        bot_choice_frame.grid(row=4, column=1, pady=10)

        self.confirm_img = PhotoImage(file='data/gifs/ok.gif')
        entry_button = Button(self.init_frame,
                              padx=2, command=self.start_game)
        entry_button.config(image=self.confirm_img, compound='left')
        entry_button.grid(row=5, column=1, pady=10)

    def set_bot_name(self):
        on_off = self.bot_switch.get()
        player1_entry = self.player1_entry.get()
        player2_entry = self.player2_entry.get()
        player1 = self.controller.player_names[1]
        player2 = self.controller.player_names[2]
        if on_off == 1:
            if player1_entry != player1 or player2_entry != player2:
                if player1_entry == player1:
                    self.player1_entry.delete(0, END)
                    self.player1_entry.insert(0, 'PC')
                else:
                    self.player2_entry.delete(0, END)
                    self.player2_entry.insert(0, 'PC')
            else:
                if randint(1, 2) == 1:
                    self.player1_entry.delete(0, END)
                    self.player1_entry.insert(0, 'PC')
                else:
                    self.player2_entry.delete(0, END)
                    self.player2_entry.insert(0, 'PC')
        else:
            if self.player1_entry.get() == 'PC':
                self.player1_entry.delete(0, END)
                self.player1_entry.insert(0, player1)
            if self.player2_entry.get() == 'PC':
                self.player2_entry.delete(0, END)
                self.player2_entry.insert(0, player2)

    def start_game(self):
        error_message = Label(self.init_frame, width=30)
        error_message.grid(row=6, column=1, padx=0)
        try:
            self.grid_size = int(self.entry1.get())
            if self.grid_size not in range(5, 21):
                error_message.configure(text='Size can be from 5x5 up to 20x20.')
                return None
        except ValueError:
            error_message.configure(text='Insert only whole #!')
            return None
        self.controller.player_names[1] = self.player1_entry.get()
        self.controller.player_names[2] = self.player2_entry.get()
        self.game_window()
        self.controller.play_grid_init(self.grid_size, self.bot_switch.get())
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

        top_infotable = Label(self.game_frame)
        if self.controller.player_on_move == 1:
            top_infotable.configure(text='{} is on turn'.format(self.controller.player_names[1]))
        else:
            top_infotable.configure(text='{} is on turn'.format(self.controller.player_names[2]))
        top_infotable.grid(row=3, column=1)
        self.controller.top_infotable = top_infotable
        bottom_infotable = Label(self.game_frame)
        bottom_infotable.grid(row=4, column=1, pady=5)
        self.controller.bottom_infotable = bottom_infotable

        grid_canvas.bind("<Button-1>", self.controller.play_grid_click)

    def client_restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def client_about(self):
        messagebox.showinfo("About", "Piskvorky - Miko 2018\n Version 0.5\n")


if __name__ == '__main__':
    root = Tk()
    Piskvorky = MainWindow(root)
    Piskvorky.mainloop()
