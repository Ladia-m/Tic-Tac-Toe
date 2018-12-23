#!/usr/bin/env python

from tkinter import *
from string import ascii_uppercase

class Grid(Frame):
    def __init__(self, grid_size, score_board):
        self.master = Tk()
        Frame.__init__(self, self.master)
        self.score_board = score_board
        self.grid_size = grid_size
        self.cell_size = 25
        self.gui_window()

    def gui_window(self):
        canvas_size = self.grid_size * self.cell_size
        self.grid_canvas = Canvas(self.master, width=canvas_size, height=canvas_size, bg='#ffffff')
        self.grid_canvas.grid(row=1, column=1)
        for i in range(1, self.grid_size):
            line_position = i * self.cell_size
            self.grid_canvas.create_line(0, line_position, canvas_size, line_position, fill='#000000')
            self.grid_canvas.create_line(line_position, 0, line_position, canvas_size, fill='#000000')
        top_coordinates = Canvas(self.master, width=canvas_size, height=self.cell_size)
        top_coordinates.grid(row=0, column=1)
        side_coordinates = Canvas(self.master, width=self.cell_size, height=canvas_size)
        side_coordinates.grid(row=1, column=0)
        for i in range(0, self.grid_size):
            x = i * self.cell_size + self.cell_size // 2
            y = self.cell_size // 2
            letter = ascii_uppercase[i]
            number = i + 1
            top_coordinates.create_text(x, y, text=letter)
            side_coordinates.create_text(y, x, text=number)
        for score in self.score_board:
            for cell in self.score_board[score]:
                x, y = cell
                self.write_score(score, x, y)
        exitbutton = Button(self.master, text='Quit', command=self.master.destroy)
        exitbutton.grid(row=2, column=0, columnspan=2)


    def write_score(self, score, x, y):
        x = x * self.cell_size + self.cell_size / 2
        y = y * self.cell_size + self.cell_size / 2
        score = str(score)
        self.grid_canvas.create_text(x, y, text=score)


class TestGrid:
    def __init__(self, size):
        self.grid_size = size
        self.score_board = {}

    def insert_score(self, score, x, y):
        score = str(score)
        for key in self.score_board:
            if [x, y] in self.score_board[key]:
                self.score_board[key].remove([x, y])
        if score in self.score_board.keys():
            self.score_board[score].append([x, y])
        else:
            self.score_board[score] = [[x, y]]

    def show_sb(self):
        self.run_gui = Grid(self.grid_size, self.score_board)
