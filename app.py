import tkinter

from grid import Grid

CELL_SIZE = 40

class Gui:
    def __init__(self):
        self.grid = Grid()
        matrix = self.grid.cells_matrix
        self.window = tkinter.Tk()
        self.window.title("Maman 11")
        self.label = tkinter.Label(text="Day 1")
        self.label.pack()
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.item_ids = [[0] * self.width for i in range(self.height)]
        self.canvas = tkinter.Canvas(self.window, height=self.height * CELL_SIZE, width=self.width * CELL_SIZE)
        self.canvas.pack()
        for x in range(self.width):
            for y in range(self.height):
                cell = matrix[y][x]
                cell_id = self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE,
                                                       (y + 1) * CELL_SIZE,
                                                       fill=cell.get_color())
                temp_id = self.canvas.create_text((x + 0.3) * CELL_SIZE, (y + 0.7) * CELL_SIZE,
                                                  text="{}C".format(cell.temperature))
                cloud_id = self.canvas.create_text((x + 0.7) * CELL_SIZE, (y + 0.3) * CELL_SIZE,
                                                   text="{}%".format(cell.cloudiness),
                                                   fill="navy")
                self.item_ids[y][x] = (cell_id, temp_id, cloud_id)


class TimerUpdate:
    def __init__(self, gui):
        self.gui = gui
        self.day = 1
        self.update()

    def update(self):
        if self.day == 365:
            gui.label.config(text="COMPLETE!")
        else:
            self.day += 1
            gui.grid.calculate_new_day()
            gui.window.after(100, self.update)
            gui.label.config(text="Day {}".format(self.day))
            for x in range(gui.width):
                for y in range(gui.height):
                    cell = gui.grid.cells_matrix[y][x]
                    (cell_id, temp_id, cloud_id) = gui.item_ids[y][x]
                    gui.canvas.itemconfig(cell_id, fill=cell.get_color())
                    gui.canvas.itemconfig(temp_id, text="{}C".format(cell.temperature))
                    gui.canvas.itemconfig(cloud_id, text="{}%".format(cell.cloudiness))


gui = Gui()
tkinter.Button(text="Start", command=lambda: TimerUpdate(gui)).pack()
gui.window.mainloop()
