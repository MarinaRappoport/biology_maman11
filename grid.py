from cell import Cell


def load_map(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
        map = [line.split(",") for line in lines]
        width = len(map[0])
        height = len(map)
        cells_matrix = [[0] * width for i in range(height)]
        for y in range(width):
            for x in range(height):
                cells_matrix[x][y] = Cell(map[x][y])
        return cells_matrix


class Grid:
    def __init__(self):
        self.cells_matrix = load_map("map.csv")
        self.width = len(self.cells_matrix[0])
        self.height = len(self.cells_matrix)

    def calculate_new_day(self):
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                cell.day_transitions()
