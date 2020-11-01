import itertools
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter
import random

ALL_TEMP_STATS = []
ALL_AIR_POLLUTION_STATS = []
GEN_TEMP_STATS = []
GEN_AIR_POLLUTION_STATS = []

class Cell:
    def __init__(self, grid, x, y, type_, temperature=25, wind_speed=0, wind_direction="N", cloud_precipitation=0, air_pollution=0, air_pollution_factor=0.1):
        self.grid = grid
        self.x = x
        self.y = y

        self.type = type_  # one of: land, city, forest, sea, iceberg
        self.temperature = temperature  # in celsius
        self.wind_speed = wind_speed  # in km/h
        self.wind_direction = wind_direction  # one of: N, S, W, E
        self.cloud_precipitation = cloud_precipitation  # when this reaches 1, it'll start raining.
        self.air_pollution = air_pollution  # 0 is not polluted at all, 1 is fully polluted.
        self.air_pollution_factor = air_pollution_factor

        self.base_temp = temperature

        # temp vars, for commiting afterwards
        self.t_type = self.type
        self.t_temperature = self.temperature
        self.t_wind_speed = self.wind_speed
        self.t_wind_direction = self.wind_direction
        self.t_cloud_precipitation = self.cloud_recipitation
        self.t_air_pollution = self.air_pollution

    def __repr__(self):
        return "<Cell<{},{}> object, Temp: {}>".format(self.x, self.y, self.temperature)

    def commit(self):
        self.type = self.t_type
        self.temperature = self.t_temperature
        self.wind_speed =  self.t_wind_speed
        self.wind_direction = self.t_wind_direction
        self.cloud_precipitation = self.t_cloud_precipitation
        self.air_pollution = self.t_air_pollution

    def calc_next_gen(self):
        # before wind
        if self.air_pollution >= 0.3:
            # air polution is bad. temprature goes up
            self.t_temperature = self.temperature + (self.air_pollution / 2)
        else:
            # air pollution is good. we should go slowly towards the base_temp.
            if (self.temperature - self.base_temp) > 0:
                # if we're above the base_temp, we go down
                self.t_temperature = self.temperature - 0.5
            elif (self.temperature - self.base_temp) < 0:
                # if we're below the base_temp, we go up
                self.t_temperature = self.temperature + 0.5

        if self.type == 'city':
            # a city creates air pollution
            self.t_air_pollution = self.t_air_pollution + self.air_pollution_factor
            self._normalize('t_air_pollution')

        if self.type == 'forest':
            # when a forest hits air polution of 1.0, it dies, and becomes a regular land
            if self.t_air_pollution >= 1.0:
                self.t_type = 'land'
            else:
                # if a forest lives, it creates oxygen which helps clean the air polution
                self.t_air_pollution = self.t_air_pollution - 0.1
                self._normalize('t_air_pollution')

        if self.type in ['forest', 'city']:
            if self.temperature > 65:
                # everything dies at 65 degrees
                self.t_type = 'land'

        if self.type == "sea":
            if self.temperature > 100:
                # water evaporates at 100 degrees
                self.t_type = 'land'

        if self.type == 'iceberg':
            if self.temperature > 0:
                # icebergs melt at positive degrees
                self.t_type = 'sea'
        
        # if it's raining
        if self.cloud_precipitation >= 1.0:
            # if it's raining, it's clears some of the air polution, and decreases the temprature by a little bit.
            self.t_air_pollution = self.t_air_pollution / 1.5
            self._normalize('t_air_pollution')
            if self.t_temperature > 10:
                self.t_temperature = self.t_temperature - 0.5
            # the cloud is now empty
            self.t_cloud_precipitation = 0
        
        elif random.random() > 0.5:
            # if it's not raining, there's a 50% chance the cloud will gain 10% rain precipitation.
            self.t_cloud_precipitation = self.cloud_precipitation + 0.1
        
        # wind
        wind_neighbours = self.get_incoming_wind_neighbours()
        if wind_neighbours:
            total_pollution = 0.0
            total_wind = 0
            total_relevant_neighbour = 0
            for neighbour in wind_neighbours:
                # the air pollution gets sucked to here
                if neighbour.air_pollution > 0:
                    total_pollution += neighbour.air_pollution
                    total_relevant_neighbour += 1
                    neighbour.t_air_pollution = 0

                total_wind += neighbour.wind_speed
            if total_relevant_neighbour > 0:
                self.t_air_pollution += total_pollution * 1.0 /total_relevant_neighbour
            
            self.t_wind_speed = total_wind / len(wind_neighbours)
            self._normalize('t_air_pollution')

        # there's a 30% chance the wind will change its course
        if random.random() > 0.7:
            self.t_wind_direction = "N" if self.t_wind_direction == "W" else "W"

    def get_neighbour(self, direction=None):
        return self.grid.get_neighbour(self.x, self.y, direction)

    def get_neighbours(self):
        return self.grid.get_neighbours(self.x, self.y)

    def get_incoming_wind_neighbours(self, wind_factor=10):
        
        radius1_neighbours = [cell for cell in self.get_neighbours() if cell.wind_speed > 0 and cell.get_neighbour(direction=cell.wind_direction) == self]
        radius2_neighbours = [cell for cell in list(itertools.chain(*[x.get_neighbours() for x in radius1_neighbours])) if cell.wind_speed > wind_factor * 1 and cell.get_neighbour(direction=cell.wind_direction) in radius1_neighbours]
        radius3_neighbours = [cell for cell in list(itertools.chain(*[x.get_neighbours() for x in radius2_neighbours])) if cell.wind_speed > wind_factor * 2 and cell.get_neighbour(direction=cell.wind_direction) in radius2_neighbours]

        total_neighbours = radius1_neighbours + radius2_neighbours + radius3_neighbours

        return total_neighbours

    def get_color(self):
        if self.type == "land":
            return "#732626"
        if self.type == "city":
            return random.choice(["#ffd11a", "#ffcc00", "#e6b800"])
        if self.type == "forest":
            return "#00802b"
        if self.type == "sea":
            return "#1a53ff"
        if self.type == "iceberg":
            return "#e6e6e6"

    def _normalize(self, var):
        v = getattr(self, var)
        if v > 1:
            v = 1
        elif v < 0:
            v= 0
        
        setattr(self, var, v)


class Grid:
    def __init__(self, length, cell_size, map_file, air_pollution_factor):
        self.length = length
        self.map_file = map_file
        self.air_pollution_factor = air_pollution_factor
        self.cells = self._create_cells()
        self.generation = 0

    def get_neighbours(self, x, y, direction=None):
        l = []

        if not direction or direction == 'E':
            if x == (self.length-1):
                # if we're at the border, we will overlap
                l.append(self.cells[0][y])
            else:
                l.append(self.cells[(x+1) % self.length][y])
        if not direction or direction == 'S':
            if y == (self.length):
                # if we're at the border, we will overlap
                l.append(self.cells[x][0])
            else:
                l.append(self.cells[x][(y+1) % self.length])
        if not direction or direction == 'W':
            if x == 0:
                # if we're at the border, we will overlap
                l.append(self.cells[self.length-1][y])
            else:
                l.append(self.cells[(x-1) % self.length][y])
        if not direction or direction == 'N':
            if y == 0:
                # if we're at the border, we will overlap
                l.append(self.cells[x][self.length-1])
            else:
                l.append(self.cells[x][(y-1) % self.length])

        return l

    def get_neighbour(self, x, y, direction):
        t = self.get_neighbours(x, y, direction)
        if not t:
            return None

        return t[0]

    def run_new_gen(self):
        self.generation += 1

        t_stat_temp = 0
        t_stat_air_pollution = 0

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].calc_next_gen()

                ALL_TEMP_STATS.append(self.cells[x][y].temperature)
                ALL_AIR_POLLUTION_STATS.append(self.cells[x][y].air_pollution)
                t_stat_temp += self.cells[x][y].temperature
                t_stat_air_pollution += self.cells[x][y].air_pollution

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].commit()

        GEN_TEMP_STATS.append((t_stat_temp * 1.0) / (self.length**2))
        GEN_AIR_POLLUTION_STATS.append((t_stat_air_pollution * 1.0) / (self.length**2))


    def _create_cells(self):
        # creates an empty self.length * self.length matrix
        cells = [[0]*self.length for i in range(self.length)]
        map = self._load_map(self.map_file)

        for x in range(self.length):
            for y in range(self.length):
                # calculating wind_speed.
                # The distribution is as follows:
                # 5% - no wind
                # 40% - 1-10 km/h wind
                # 40% - 11-20 km/h wind
                # 15% - 21-30 km/h wind

                rand = random.random()
                if rand < 0.05:
                    wind_speed = 0
                elif rand < 0.45:
                    wind_speed = random.randint(1,10)
                elif rand < 0.85:
                    wind_speed = random.randint(11,20)
                else:
                    wind_speed = random.randint(21,30)

                cells[x][y] = Cell(self, x, y,
                    type_ = map[x][y],
                    temperature = random.randint(22, 27) if map[x][y] != "iceberg" else random.randint(-12, -6),
                    wind_speed = wind_speed,
                    wind_direction = random.choice(["N", "W"]),
                    air_pollution_factor = self.air_pollution_factor
                )

        return cells

    def _load_map(self, path):
        """
        Loads the map structure from a text file. Each char represents a cell.
        Valid values are:
        L - land
        C - city
        F - forest
        S - sea
        I - iceberg
        """
        # length is +2 because we have an off-grid layout of 1 cell length, for calculation reasons.
        map = [[0]*(self.length+2) for i in range(self.length+2)]

        with open(path, 'r') as f:
            for y in range(self.length):
                for x in range(self.length):
                    c = f.read(1)

                    while c not in ['L', 'C', 'F', 'S', 'I']:
                        c = f.read(1)

                    if c == "L":
                        map[x][y] = "land"
                    if c == "C":
                        map[x][y] = "city"
                    if c == "F":
                        map[x][y] = "forest"
                    if c == "S":
                        map[x][y] = "sea"
                    if c == "I":
                        map[x][y] = "iceberg"

        return map


class App:
    def __init__(self, length, cell_size, map_file, refresh_rate=50, stop_gen=365, air_pollution_factor=0.1):
        self.length = length
        self.cell_size = cell_size
        self.refresh_rate = refresh_rate  # in ms
        self.stop_gen = stop_gen

        # creates an empty self.length * self.length matrix
        self.items = [[0]*self.length for i in range(self.length)]

        self.grid = Grid(self.length, self.cell_size, map_file=map_file, air_pollution_factor=air_pollution_factor)
        self.root = tkinter.Tk()
        self.root.title("Maman 11 - Biological computation Course - Brandes Itay")
        self.label = tkinter.Label(self.root)
        self.label.pack()
        self.canvas = tkinter.Canvas(self.root, height=self.length*self.cell_size, width=self.length*self.cell_size)
        self.canvas.pack()
        self.items = self.update_canvas(self.items)
        self.root.after(self.refresh_rate, self.refresh_screen)
        self.root.mainloop()

    def refresh_screen(self):
        self.grid.run_new_gen()
        

        if self.grid.generation >= self.stop_gen:
            self.update_canvas(canvas_done=True, canvas_items=self.items)
            self.label.config(text="Generation {} **DONE**".format(self.grid.generation))
        else:
            self.update_canvas(canvas_done=True, canvas_items=self.items)
            self.label.config(text="Generation {}".format(self.grid.generation))
            self.root.after(self.refresh_rate, self.refresh_screen)
        
    def update_canvas(self, canvas_items, canvas_done=False):
        cell_items = self.grid.cells

        if not canvas_done:
            for x in range(len(cell_items)):
                for y in range(len(cell_items)):
                    cell = cell_items[x][y]
                    cell_text = "{:.2f}".format(cell.air_pollution)
                    cell_text = int(cell.temperature)
                    rectangle_id = self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, (x+1)*self.cell_size, (y+1)*self.cell_size, fill=cell.get_color())
                    text_id = self.canvas.create_text((x+0.5)*self.cell_size, (y+0.5)*self.cell_size, text=cell_text, font="Arial 8 bold")
                    canvas_items[x][y] = (rectangle_id, text_id)

            return canvas_items

        else:
            if canvas_items:
                for x in range(len(canvas_items)):
                    for y in range(len(canvas_items)):
                        cell = cell_items[x][y]
                        cell_text = "{:.2f}".format(cell.air_pollution)
                        cell_text = int(cell.temperature)
                        (rectangle_id, text_id) = canvas_items[x][y]
                        self.canvas.itemconfig(rectangle_id, fill=cell.get_color())
                        self.canvas.itemconfig(text_id, text=cell_text)
            else:
                raise ValueError("No canvas_items given for re-iterating over canvas cells.")

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

if __name__ == '__main__':
    app = App(length=50, cell_size=17, refresh_rate=1, stop_gen=365, map_file="map.dat", air_pollution_factor=0.11)
    print("[Temperature]\t\tMax: {:.2f}\tMin: {:.2f}\tAvg: {:.2f}\tStd. Dev: {:.2f}".format(max(ALL_TEMP_STATS), min(ALL_TEMP_STATS), mean(ALL_TEMP_STATS), stddev(ALL_TEMP_STATS)))
    print("[Air Pollution]\t\tMax: {:.2f}\tMin: {:.2f}\tAvg: {:.2f}\tStd. Dev: {:.2f}".format(max(ALL_AIR_POLLUTION_STATS), min(ALL_AIR_POLLUTION_STATS), mean(ALL_AIR_POLLUTION_STATS), stddev(ALL_AIR_POLLUTION_STATS)))

    f = open('temp.txt', 'w')
    for n in GEN_TEMP_STATS: f.write("{}\n".format(n))
    f.close()

    f = open('air.txt', 'w')
    for n in GEN_AIR_POLLUTION_STATS: f.write("{}\n".format(n))
    f.close()
