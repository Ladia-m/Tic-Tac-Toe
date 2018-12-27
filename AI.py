#!/usr/bin/env python
from random import randint
import test_gui


class AI:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.play_grid = []
        self.rival_moves = []
        self.my_moves = []
        self.directions = ['tt', 'tr', 'rr', 'br', 'bb', 'bl', 'll', 'tl']
        for column in range(0, self.grid_size + 1):
            rows = []
            for row in range(0, self.grid_size + 1):
                rows.append(0)   # 0 = empty; 1 = rival; 2 = this AI
            self.play_grid.append(rows)
        self.test = test_gui.TestGrid(grid_size) #test purpose

    def play(self, coordinates):
        self.score_grid = []
        for column in range(0, self.grid_size + 1):
            rows = []
            for row in range(0, self.grid_size + 1):
                rows.append(0)
            self.score_grid.append(rows)
        if coordinates == 'start':
            x, y = self.set_defense_score()
        else:
            x = coordinates[0]
            y = coordinates[1]
            self.play_grid[x][y] = 1
            self.rival_moves.append(coordinates)
            x, y = self.set_defense_score()
        self.play_grid[x][y] = 2
        self.my_moves.append([x, y])
        self.test.show_sb()
        return x, y

    def set_defense_score(self):
        default_score = 10
        rival_lines = []
        rival_singles = []
        for cell in self.rival_moves:
            center_cell = cell
            around = self.check_around(center_cell)
            if len(around) > 0:
                for i in range(0, 4):
                    if self.directions[i] in around or self.directions[i + 4] in around:
                        line = [center_cell]
                        no_break1 = True
                        no_break2 = True
                        distance = 1
                        while no_break1 or no_break2:
                            one_side = self.cellxy(center_cell, self.directions[i], distance)
                            other_side = self.cellxy(center_cell, self.directions[i + 4], distance)
                            if (one_side in self.rival_moves) and no_break1:
                                line.append(one_side)
                            else:
                                no_break1 = False
                            if (other_side in self.rival_moves) and no_break2:
                                line.append(other_side)
                            else:
                                no_break2 = False
                            distance += 1
                        line = self.sorter(line)
                        if line not in rival_lines:
                            rival_lines.append(line)
            else:
                rival_singles.append(center_cell)
        for i in rival_singles:
            for direction in self.directions:
                x, y = self.cellxy(i, direction, 1)
                if ([x, y] not in self.my_moves) and (self.within_grid([x, y])):
                    self.score_grid[x][y] += default_score
        for line in rival_lines:
            #add points at ends of rivals line
            direction_1 = self.check_direction(line[-1], line[0])
            x, y = self.cellxy(line[0], direction_1, 1)
            line_extension_1 = self.cells_on_line('empty&rival', direction_1, [x, y], 5 - len(line), True)
            direction_2 = self.check_direction(line[0], line[-1])
            x, y = self.cellxy(line[-1], direction_2, 1)
            line_extension_2 = self.cells_on_line('empty&rival', direction_2, [x, y], 5 - len(line), True)
            if len(line_extension_1) + len(line_extension_2) + len(line) >= 5:
                for line_extension in [line_extension_1, line_extension_2]:
                    variable_score = 0
                    distance = 0
                    if len(line_extension) + len(line) < 5:
                        variable_score -= default_score
                    if len(line) == 3 and len(line_extension_1) > 0 and len(line_extension_2) > 0:
                        variable_score += 10 * default_score
                    # pridej bonus v situaci "XXX X"
                    for x, y in line_extension:
                        self.score_grid[x][y] += default_score * (len(line) - distance) + variable_score
                        distance += 1
            #add points around rivals line
        for line in rival_lines:
            cells_around = []
            for direction in self.directions:
                if direction in [direction_1, direction_2]:
                    continue
                for cell in line:
                    x, y = self.cellxy(cell, direction, 1)
                    if [x, y] not in cells_around:
                        cells_around.append([x, y])
            for x, y in cells_around:
                if self.score_grid[x][y] < 2 * default_score:
                    self.score_grid[x][y] += default_score

        top_score = [0]
        for column in range(0, self.grid_size):
            for row in range(0, self.grid_size):
                x, y = column, row
                cell_value = self.score_grid[x][y]
                if [x, y] in self.my_moves or [x, y] in self.rival_moves:
                    cell_value = 0
                    self.test.insert_score(cell_value, x, y)
                if cell_value > top_score[0]:
                    top_score = [cell_value, [x, y]]
                    self.test.insert_score(cell_value, x, y)
                elif cell_value == top_score[0]:
                    top_score.append([x, y])
                    self.test.insert_score(cell_value, x, y)
                else:                                           #test
                    self.test.insert_score(cell_value, x, y)    #test
        cell_index = randint(1, len(top_score) - 1)
        return top_score[cell_index]

    def check_around(self, center_cell):
        cells_around = {}
        for direction in self.directions:
            coordinates = self.cellxy(center_cell, direction, 1)
            if coordinates in self.rival_moves:
                cells_around[direction] = coordinates
        return cells_around

    def within_grid(self, cell):
        if (cell[0] and cell[1]) in range(0, self.grid_size):
            return True
        else:
            return False

    def cellxy(self, center_cell, direction, distance):
        if direction == 'rr':
            return [center_cell[0] + distance, center_cell[1]]
        if direction == 'll':
            return [center_cell[0] - distance, center_cell[1]]
        if direction == 'tt':
            return [center_cell[0], center_cell[1] - distance]
        if direction == 'bb':
            return [center_cell[0], center_cell[1] + distance]
        if direction == 'tr':
            return [center_cell[0] + distance, center_cell[1] - distance]
        if direction == 'br':
            return [center_cell[0] + distance, center_cell[1] + distance]
        if direction == 'tl':
            return [center_cell[0] - distance, center_cell[1] - distance]
        if direction == 'bl':
            return [center_cell[0] - distance, center_cell[1] + distance]

    def check_direction(self, first_cell, second_cell):
        if first_cell[1] == second_cell[1]:
            if first_cell[0] < second_cell[0]:
                return 'rr'
            else:
                return 'll'
        if first_cell[0] == second_cell[0]:
            if first_cell[1] < second_cell[1]:
                return 'bb'
            else:
                return 'tt'
        if (first_cell[0] < second_cell[0]) and (first_cell[1] < second_cell[1]):
            return 'br'
        if (first_cell[0] > second_cell[0]) and (first_cell[1] > second_cell[1]):
            return 'tl'
        if (first_cell[0] < second_cell[0]) and (first_cell[1] > second_cell[1]):
            return 'tr'
        if (first_cell[0] > second_cell[0]) and (first_cell[1] < second_cell[1]):
            return 'bl'

    def sorter(self, the_list):
        sorted_list = []
        while len(the_list) > 0:
            lowest = the_list[0]
            for i in the_list:
                if lowest[0] + lowest[1] > i[0] + i[1]:
                    lowest = i
                elif lowest[0] + lowest[1] == i[0] + i[1] and lowest[0] > i[0]:
                    lowest = i
            sorted_list.append(lowest)
            the_list.remove(lowest)
        return sorted_list

    def cells_on_line(self, option, direction, start, length, stop=False):
        if length == 0:
            length = self.grid_size
        counter = 0
        whole_line = []
        next_cell = start
        while self.within_grid(next_cell):
            whole_line.append(next_cell)
            next_cell = self.cellxy(next_cell, direction, 1)
            counter += 1
            if counter == length:
                break
        if option == 'rival':
            return_line = []
            for cell in whole_line:
                if cell in self.rival_moves:
                    return_line.append(cell)
                elif stop:
                    break
            return return_line
        if option == 'me':
            return_line = []
            for cell in whole_line:
                if cell in self.my_moves:
                    return_line.append(cell)
                elif stop:
                    break
            return return_line
        if option == 'empty':
            return_line = []
            for cell in whole_line:
                if cell not in self.my_moves and cell not in self.rival_moves:
                    return_line.append(cell)
                elif stop:
                    break
            return return_line
        if option == 'empty&rival':
            return_line = []
            for cell in whole_line:
                if cell not in self.my_moves:
                    return_line.append(cell)
                elif stop:
                    break
            return return_line
        if option == 'all':
            return whole_line
