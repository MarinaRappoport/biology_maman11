from cell import Cell

TEMP_STATS = []
AQI_STATS = []

# wind_changes_matrix = {
#     (-10, -29, -31): (1, 1),
#     (-20, -30, -21, -19): (1, 2),
#     (10, 29, 31): (2, 1),
#     (20, 30, 19, 21): (2, 2),
#     (1, -7, 13): (3, 1),
#     (2, 3, -8, 12): (3, 2),
#     (-1, 7, -13): (4, 1),
#     (-2, -3, 8, -12): (4, 2)
# }

wind_changes_matrix = {
    (-10, -9): (1, 1),
    (10, 9): (2, 1),
    (1, 11): (3, 1),
    (-1, -11): (4, 1),
}


def load_map(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
        map = [line.split(",") for line in lines]
        width = len(map[0])
        height = len(map)
        cells_matrix = [[0] * width for i in range(height)]
        counter = 0
        for y in range(width):
            for x in range(height):
                cells_matrix[x][y] = Cell(map[x][y], counter)
                counter += 1
        return cells_matrix


class Grid:
    def __init__(self):
        self.day = 1
        self.cells_matrix = load_map("map.csv")
        self.width = len(self.cells_matrix[0])
        self.height = len(self.cells_matrix)

    def calculate_new_day(self):
        NORTH = 0
        SOUTH = 0
        EAST = 0
        WEST = 0
        self.day += 1
        cloudiness_changes = [[0] * self.width for i in range(self.height)]
        polution_changes = [[0] * self.width for i in range(self.height)]
        wind_changes = [[0] * self.width for i in range(self.height)]
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                TEMP_STATS.append(cell.temperature)
                AQI_STATS.append(cell.air_quality_index)
                speed = cell.wind_speed
                if speed > 0:
                    x_to_apply = (cell.wind_direction[0] * speed + x) % self.height
                    y_to_apply = (cell.wind_direction[1] * speed + y) % self.width
                    cloudiness_changes[x_to_apply][y_to_apply] += cell.cloudiness
                    cloudiness_changes[x][y] -= cell.cloudiness
                    polution_changes[x_to_apply][y_to_apply] += cell.air_quality_index
                    polution_changes[x][y] -= cell.air_quality_index
                    wind_changes[x_to_apply][y_to_apply] += cell.wind_direction[0] * speed * 10 \
                                                            + cell.wind_direction[1] * speed
        # apply wind changes
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                cell.cloudiness += cloudiness_changes[x][y]
                cell.air_quality_index += polution_changes[x][y]
                # change wind
                for i in wind_changes_matrix:
                    if wind_changes[x][y] in i:
                        cell.wind_direction = cell.get_wind_direction(wind_changes_matrix.get(i)[0])
                        cell.wind_speed = wind_changes_matrix.get(i)[1]
                        break
                else:
                    cell.wind_speed = (cell.wind_speed + 1) % 2

                w = cell.wind_direction[0] * 10 + cell.wind_direction[1]
                if w == -10:
                    NORTH += 1
                elif w == 10:
                    SOUTH += 1
                elif w == 1:
                    EAST += 1
                else:
                    WEST += 1
        print(f"{self.day} N: {NORTH}, S: {SOUTH}, E: {EAST}, W: {WEST}")

        # day transactions
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                cell.day_transitions()
        # print("-------------------")
        # print(f"Day {self.day}")
        # print(f"Average temp: {sum(TEMP_STATS) / len(TEMP_STATS)}")
        # print(f"Average aqi: {sum(AQI_STATS) / len(AQI_STATS)}")
