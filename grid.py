from cell import Cell

# TEMP_STATS = []
# AQI_STATS = []

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
        cloudiness_changes = [[0] * self.width for i in range(self.height)]
        polution_changes = [[0] * self.width for i in range(self.height)]
        temperature_changes = [[0] * self.width for i in range(self.height)]
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                # TEMP_STATS.append(cell.temperature)
                # AQI_STATS.append(cell.air_quality_index)
                speed = cell.wind_speed
                if speed > 0:
                    x_to_apply = (cell.wind_direction[0] * speed + x) % self.height
                    y_to_apply = (cell.wind_direction[1] * speed + y) % self.width
                    if cell.temperature < self.cells_matrix[x_to_apply][y_to_apply].temperature:
                        temp_difference = -1
                    else:
                        temp_difference = 0
                    cloudiness_changes[x_to_apply][y_to_apply] += cell.cloudiness
                    cloudiness_changes[x][y] -= cell.cloudiness
                    polution_changes[x_to_apply][y_to_apply] += cell.air_quality_index
                    polution_changes[x][y] -= cell.air_quality_index
                    temperature_changes[x_to_apply][y_to_apply] += temp_difference
                    temperature_changes[x][y] -= temp_difference
        # apply wind changes
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                cell.cloudiness += cloudiness_changes[x][y]
                cell.air_quality_index += polution_changes[x][y]
                cell.temperature += temperature_changes[x][y]
        # day transactions
        for x in range(self.height):
            for y in range(self.width):
                cell = self.cells_matrix[x][y]
                cell.day_transitions()
        # print(f"Day {day}")
        # print(f"Average temp: {sum(TEMP_STATS) / len(TEMP_STATS)}")
        # print(f"Average aqi: {sum(AQI_STATS) / len(AQI_STATS)}")
