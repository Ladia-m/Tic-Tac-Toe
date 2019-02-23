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
        for column in range(0, self.grid_size):
            rows = []
            for row in range(0, self.grid_size):
                rows.append(0)   # 0 = empty; 1 = rival; 2 = this AI
            self.play_grid.append(rows)
        self.test = test_gui.TestGrid(grid_size) #test purpose

    def play(self, coordinates=None):
        self.score_grid = []
        for column in range(0, self.grid_size):
            rows = []
            for row in range(0, self.grid_size):
                rows.append(0)
            self.score_grid.append(rows)
        if not coordinates:
            x = randint(self.grid_size // 2 - 2, self.grid_size // 2 + 2)
            y = randint(self.grid_size // 2 - 2, self.grid_size // 2 + 2)
        else:
            x = coordinates[0]
            y = coordinates[1]
            self.play_grid[x][y] = 1
            self.rival_moves.append(coordinates)
            self.set_defense_score()
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
                    else:  # test
                        self.test.insert_score(cell_value, x, y)  # test
            x, y = top_score[randint(1, len(top_score) - 1)]
        self.play_grid[x][y] = 2
        self.my_moves.append([x, y])
        self.test.show_sb()
        return x, y

    def set_defense_score(self):
        default_score = 10
        rival_lines = []
        rival_singles = []
        defeat_in = 5
        for cell in self.rival_moves:
            center_cell = cell
            around = self.check_around(center_cell, 'rival')
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
        for cell in rival_singles:
            for direction in self.directions:
                x, y = self.cellxy(cell, direction, 1)
                if x < self.grid_size and y < self.grid_size:
                    if ([x, y] not in self.my_moves) and (self.within_grid([x, y])):
                        if defeat_in > 4:
                            defeat_in = 4
                        self.score_grid[x][y] += default_score
                        # if there are rival singles in 2 cells distance, add extra score
                        line = self.cells_on_line('empty&rival', direction, [x, y], 4, True)
                        if len(line) == 4 and line[1] in self.rival_moves:
                            if self.score_grid[x][y] < 2 * default_score:
                                self.score_grid[x][y] += default_score
                            if defeat_in > 3:
                                defeat_in = 3
                        # maybe create case for three singles situation X_X_X here
        # where the magic happens:
        for line in rival_lines:
            direction_1 = self.check_direction(line[-1], line[0])
            x, y = self.cellxy(line[0], direction_1, 1)
            line_extension_1 = self.cells_on_line('empty&rival', direction_1, [x, y], 5 - len(line), True)
            direction_2 = self.check_direction(line[0], line[-1])
            x, y = self.cellxy(line[-1], direction_2, 1)
            line_extension_2 = self.cells_on_line('empty&rival', direction_2, [x, y], 5 - len(line), True)
            if len(line_extension_1) + len(line_extension_2) + len(line) >= 5:
                for line_extension in [line_extension_1, line_extension_2]:
                    if len(line_extension) == 0:
                        continue
                    variable_score = 0
                    distance = 0
                    if len(line_extension_1) + len(line) < 5 or len(line_extension_2) + len(line) < 5:
                        variable_score -= default_score
                    if len(line_extension) + len(line) < 5:
                        variable_score -= default_score
                    if len(line) == 3 and len(line_extension_1) > 0 and len(line_extension_2) > 0:
                        variable_score += 4 * default_score
                    if len(line) == 4:
                        variable_score += 5 * default_score
                    counter = 0
                    for cell in line_extension:
                        if cell in self.rival_moves:
                            counter += 1
                    if len(line_extension) > 1 and line_extension[1] in self.rival_moves:
                            x, y = line_extension[0]
                            self.score_grid[x][y] += (len(line) + counter) * default_score
                    for x, y in line_extension:
                        self.score_grid[x][y] += default_score * (len(line) - distance + 1) + variable_score
                        if self.score_grid[x][y] < 0:
                            self.score_grid[x][y] = 0
                        distance += 1
                    if defeat_in > 5 - len(line) - counter:
                        defeat_in = 5 - len(line) - counter
        # Add some basic score around rival lines:
        for line in rival_lines:
            cells_around = []
            for direction in self.directions:
                for cell in line:
                    x, y = self.cellxy(cell, direction, 1)
                    if [x, y] not in cells_around:
                        cells_around.append([x, y])
            for x, y in cells_around:
                if x < self.grid_size and y < self.grid_size:
                    if self.score_grid[x][y] < 2 * default_score:
                        self.score_grid[x][y] += default_score
            # if two parallel lines with 1 cell gap, add extra score between them
            for direction in self.directions:
                for cell in line:
                    chkline = self.cells_on_line('empty&rival', direction, cell, 5, True)
                    if len(chkline) == 5 and chkline[1] not in self.rival_moves and chkline[2] in self.rival_moves:
                        x, y = chkline[1]
                        if self.score_grid[x][y] < 3 * default_score:
                            self.score_grid[x][y] = 3 * default_score
        return defeat_in

    def set_offense_score(self, defeat_in):
        win_in = 5
        default_score = 5
        my_lines = []
        my_singles = []
        for cell in self.my_moves:
            center_cell = cell
            around = self.check_around(center_cell, 'me')
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
                            if (one_side in self.my_moves) and no_break1:
                                line.append(one_side)
                            else:
                                no_break1 = False
                            if (other_side in self.my_moves) and no_break2:
                                line.append(other_side)
                            else:
                                no_break2 = False
                            distance += 1
                        line = self.sorter(line)
                        if line not in my_lines:
                            my_lines.append(line)
            else:
                my_singles.append(center_cell)



    def check_around(self, center_cell, competitor):
        cells_around = {}
        for direction in self.directions:
            coordinates = self.cellxy(center_cell, direction, 1)
            if coordinates in self.rival_moves and competitor == 'rival':
                cells_around[direction] = coordinates
            elif coordinates in self.my_moves and competitor == 'me':
                cells_around[direction] = coordinates
        return cells_around

    def within_grid(self, cell):
        if cell[0] in range(0, self.grid_size) and cell[1] in range(0, self.grid_size):
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
