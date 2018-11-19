#!/usr/bin/env python

from random import randint

class AI:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.play_grid = []
        for row in range(0, self.grid_size):
            columns = []
            for column in range(0, self.grid_size):
                columns.append(0)   # 0 = empty; 1 = rival; 2 = this AI
            self.play_grid.append(columns)

    def play(self, coordinates):
        if coordinates == 'start':
            x = randint(0, self.grid_size - 1)
            y = randint(0, self.grid_size - 1)

        else:
            x = coordinates[0]
            y = coordinates[1]
            self.play_grid[x][y] = 1

        while self.play_grid[x][y] != 0:
            x = randint(0, self.grid_size - 1)
            y = randint(0, self.grid_size - 1)
        self.play_grid[x][y] = 2
        return x, y
