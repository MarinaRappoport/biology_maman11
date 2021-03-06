SEA = 'S'
LAND = 'L'
GLACIER = 'G'
FOREST = 'F'
CITY = 'C'

CITY_DAY_AIR_POLLUTION = 40

wind_direction = {
    1: (-1, 0, "", "↑"),  # NORTH
    2: (1, 0, "", "↓"),  # SOUTH
    3: (0, 1, "", "→"),  # EAST
    4: (0, -1, "", "←")  # WEST
}

cell_properties = {
    SEA: ('cyan', 10),
    LAND: ('yellow', 25),
    GLACIER: ('white', -15),
    FOREST: ('forestgreen', 15),
    CITY: ('darkgrey', 20)
}


class Cell:
    def __init__(self, cell_type, counter):
        self.type = cell_type  # land, sea, glacier, forest, city
        self.temperature = cell_properties.get(self.type)[1]
        if self.type == CITY:
            self.air_quality_index = 160
        else:
            self.air_quality_index = 0  # air pollution in AQI(Air Quality Index) from 0 to 500
        self.wind_speed = counter % 2  # 0 - no wind, 1 - wind
        self.wind_direction = self.get_wind_direction((int(counter / 2) % 4 + 1))
        self.cloudiness = counter % 6 * 10  # from 0 to 100%, when it's 100% - will rain

    def day_transitions(self):
        # new values to apply:
        temperature_new = self.temperature
        air_quality_index_new = self.air_quality_index
        type_new = self.type

        # after rain: no clouds, temperature lowers, air quality index lowers
        if self.cloudiness >= 100:
            self.cloudiness = 0
            if self.temperature > 5:
                temperature_new -= 2
            air_quality_index_new = self.air_quality_index - 30
            # land became forest in good ecology after rain
            if self.type == LAND and self.air_quality_index < 100 and 10 <= self.temperature < 50:
                type_new = FOREST

        # evaporation of water forms clouds
        if self.type == SEA:
            self.cloudiness = self.cloudiness + 10

        # air pollution causes warming
        if self.air_quality_index > 150:
            temperature_new += 1
        else:
            temperature_base = cell_properties.get(self.type)[1]
            if temperature_new - temperature_base > 3:
                temperature_new -= 1
            elif temperature_new - temperature_base < -1:
                temperature_new += 1

        # forest produces oxygen and decreases air pollution
        if self.type == FOREST:
            air_quality_index_new -= 30
            # when pollution is high, forest dies
            if self.air_quality_index >= 500:
                type_new = LAND

        if self.type == GLACIER:
            air_quality_index_new -= 20

        # city increases air pollution
        if self.type == CITY:
            air_quality_index_new += CITY_DAY_AIR_POLLUTION
        if air_quality_index_new > 500:
            air_quality_index_new = 500

        # heat dissolves glaciers
        if self.type == GLACIER and self.temperature > 0:
            type_new = SEA

        # high temperature kills city and forest
        if (self.type == CITY or self.type == FOREST) and self.temperature > 60:
            type_new = LAND

        # high temperature evaporates sea
        if self.type == SEA and self.temperature > 90:
            type_new = LAND

        # renew parameters
        self.type = type_new
        self.temperature = temperature_new
        if air_quality_index_new < 0:
            self.air_quality_index = 0
        else:
            self.air_quality_index = air_quality_index_new

    def get_color(self):
        return cell_properties.get(self.type)[0]

    def get_wind_direction(self, option):
        return wind_direction.get(option)
