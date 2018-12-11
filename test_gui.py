#!/usr/bin/env python

from tkinter import *

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
        self.grid_canvas.grid(row=0, column=0)
        for i in range(1, self.grid_size):
            line_position = i * self.cell_size
            self.grid_canvas.create_line(0, line_position, canvas_size, line_position, fill='#000000')
            self.grid_canvas.create_line(line_position, 0, line_position, canvas_size, fill='#000000')
        for score in self.score_board:
            for cell in self.score_board[score]:
                x, y = cell
                self.write_score(score, x, y)
        exitbutton = Button(self.master, text='Quit', command=self.master.destroy)
        exitbutton.grid(row=1, column=0)


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
