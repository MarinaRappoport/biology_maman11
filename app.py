import tkinter

from grid import Grid

CELL_SIZE = 40


# def refresh_screen(grid, window):
#     if grid.day >= 365:
#         # window.after_cancel(update_job)
#         # update_job = None
#         pass
#     else:
#         grid.calculate_new_day()
#         label.config(text="Generation {}".format(grid.day))
#         # update canvas
#         for x in range(GRID_WIDTH):
#             for y in range(GRID_HEIGHT):
#                 cell = matrix[y][x]
#                 canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
#                                         fill=cell.get_color())
#                 canvas.create_text((x + 0.3) * CELL_SIZE, (y + 0.7) * CELL_SIZE, text="{}C".format(cell.temperature))
#                 canvas.create_text((x + 0.7) * CELL_SIZE, (y + 0.3) * CELL_SIZE, text="{}%".format(cell.cloudiness),
#                                    fill="navy")
#         window.after(50, refresh_screen(grid=matrix, window=window))


class Gui:
    def __init__(self):
        grid = Grid()
        self.matrix = grid.cells_matrix
        self.window = tkinter.Tk()
        self.window.title("Maman 11")
        self.label = tkinter.Label(text="Day 1")
        self.label.pack()
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)
        self.item_ids = [[0] * self.width for i in range(self.height)]
        self.canvas = tkinter.Canvas(self.window, height=self.width * CELL_SIZE, width=self.height * CELL_SIZE)
        for x in range(self.width):
            for y in range(self.height):
                cell = self.matrix[y][x]
                cell_id = self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE,
                                                       (y + 1) * CELL_SIZE,
                                                       fill=cell.get_color())
                temp_id = self.canvas.create_text((x + 0.3) * CELL_SIZE, (y + 0.7) * CELL_SIZE,
                                                  text="{}C".format(cell.temperature))
                cloud_id = self.canvas.create_text((x + 0.7) * CELL_SIZE, (y + 0.3) * CELL_SIZE,
                                                   text="{}%".format(cell.cloudiness),
                                                   fill="navy")
                self.item_ids[y][x] = (cell_id, temp_id, cloud_id)
        self.canvas.pack()


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
            gui.window.after(50, self.update)
            gui.label.config(text="Day {}".format(self.day))
            for x in range(gui.width):
                for y in range(gui.height):
                    cell = gui.matrix[y][x]
                    (cell_id, temp_id, cloud_id) = gui.item_ids[y][x]
                    gui.canvas.itemconfig(cell_id, fill=cell.get_color())
                    gui.canvas.itemconfig(temp_id, text=cell.temperature)
                    gui.canvas.itemconfig(cloud_id, text=cell.cloudiness)


# update_job = window.after(50, refresh_screen(grid=grid, window=window))
gui = Gui()
tkinter.Button(text="Start", command=lambda: TimerUpdate(gui)).pack()
gui.window.mainloop()
