import random

SEA = 'S'
LAND = 'L'
GLACIER = 'G'
FOREST = 'F'
CITY = 'C'

CITY_DAY_AIR_POLLUTION = 30

# TODO check direction
wind_direction = {
    1: (0, -1),  # NORTH
    2: (0, 1),  # SOUTH
    3: (1, 0),  # EAST
    4: (-1, 0)  # WEST
}

cell_color = {
    SEA: 'cyan',
    LAND: 'yellow',
    GLACIER: 'white',
    FOREST: 'forestgreen',
    CITY: 'darkgrey'
}


class Cell:
    def __init__(self, cell_type):
        self.type = cell_type  # land, sea, glacier, forest, city
        if self.type == GLACIER:
            self.temperature = -20  # in celsius
        elif self.type == SEA:
            self.temperature = 10
        elif self.type == CITY:
            self.temperature = 25
        else:
            self.temperature = 20
        self.air_quality_index = 0  # air pollution in AQI(Air Quality Index) from 0 to 500
        # self.wind_speed = 0
        self.wind_speed = random.randint(0, 2) # in cells
        self.wind_direction = wind_direction.get(random.randint(1, 4))
        self.cloudiness = random.randint(0, 5) * 10  # from 0 to 100%, when it's 100% - will rain

    def day_transitions(self):
        # new values to apply:
        temperature_new = self.temperature
        air_quality_index_new = self.air_quality_index
        type_new = self.type

        # after rain: no clouds, temperature lowers, air quality index lowers
        if self.cloudiness >= 100:
            self.cloudiness = 0
            if self.temperature > 5:
                temperature_new -= 3
            air_quality_index_new = self.air_quality_index - 40
            # land became forest in good ecology after rain
            if self.type == LAND and self.air_quality_index < 100 and 10 <= self.temperature < 60:
                type_new = FOREST

        # evaporation of water forms clouds
        if self.type == SEA:
            self.cloudiness = self.cloudiness + 10

        # air pollution causes warming
        if self.air_quality_index > 100:
            temperature_new += int(self.air_quality_index / 100)

        # forest produces oxygen and decreases air pollution
        if self.type == FOREST:
            air_quality_index_new -= 20
            # when pollution is high, forest dies
            if self.air_quality_index >= 400:
                type_new = LAND

        # city increases air pollution
        if self.type == CITY:
            air_quality_index_new += CITY_DAY_AIR_POLLUTION

        # heat dissolves glaciers
        if self.type == GLACIER and self.temperature > 0:
            type_new = SEA

        # lower 0 sea became glacier
        if self.type == SEA and self.temperature < 0:
            type_new = GLACIER

        # high temperature kills city and forest
        if (self.type == CITY or self.type == FOREST) and self.temperature > 60:
            type_new = LAND

        # high temperature evaporates sea
        if self.type == SEA and self.temperature > 80:
            type_new = LAND

        # renew parameters
        self.type = type_new
        self.temperature = temperature_new
        self.air_quality_index = air_quality_index_new

    def get_color(self):
        return cell_color.get(self.type)
