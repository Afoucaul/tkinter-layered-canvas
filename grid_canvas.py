import tkinter as tk
from layer import GriddedCanvasLayer


class GriddedCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_lines = []

    def draw_grid(self, cellWidth, cellHeight, widthInCells, heightInCells):
        for i in range(widthInCells + 1):
            step = 1 + i * (cellWidth + 1)
            self.create_line(1, step, 1+(1+cellWidth)*widthInCells, step)

        for i in range(heightInCells + 1):
            step = 1 + i * (cellHeight + 1)
            self.create_line(step, 1, step, 1+(1+cellHeight)*heightInCells)


class GriddedFrame(tk.Frame):
    def __init__(self, parent, widthInCells, heightInCells,
                 cellWidth, cellHeight,
                 xScrollable=True, yScrollable=True, **kwargs):
        super().__init__(parent)

        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.widthInCells = widthInCells
        self.heightInCells = heightInCells
        self.actualWidth = widthInCells*cellWidth
        self.actualHeight = heightInCells*cellHeight
        self.xScrollable = xScrollable
        self.yScrollable = yScrollable

        self.canvas = GriddedCanvas(
            self, width=self.actualWidth, height=self.actualHeight)

        self.layers = []
        self.add_layer("Base layer")
        self.currentLayer = self.layers[0]

        # Create and pack horizontal scrollbar
        if self.xScrollable:
            hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
            hbar['command'] = self.canvas.xview
            self.canvas['xscrollcommand'] = hbar.set
            hbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create and pack vertical scrollbar
        if self.yScrollable:
            vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
            vbar['command'] = self.canvas.yview
            self.canvas.configure(yscrollcommand=vbar.set)
            vbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pack canvas
        self.canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.draw()

    def select_layer(self, indicator):
        self.currentLayer = self.get_layer(indicator)

    def get_layer(self, indicator):
        if isinstance(indicator, int):
            return self.layers[indicator]
        elif isinstance(indicator, str):
            for layer in self.layers:
                if layer.name == indicator:
                    return layer
            raise KeyError("No layer named '{}'".format(indicator))

    def remove_layer(self, name):
        layer = self.get_layer(name)
        self.layers.remove(layer)

    def draw(self):
        self.canvas.draw_grid(
            self.cellWidth,
            self.cellHeight,
            self.widthInCells,
            self.heightInCells)

        if not self.xScrollable:
            self.config(width=self.actualWidth)

        self.update()

    def add_layer(self, name):
        self.layers.append(
            GriddedCanvasLayer(
                self, self.canvas, self.widthInCells, self.heightInCells, name))

    def get_center_of_cell(self, x, y):
        """Return the canvas coordinates of the center of a cell
        """
        return 1 + int((x+0.5)*self.cellWidth), 1 + int((y+0.5)*self.cellHeight)

    def hide_layer(self, indicator):
        self.get_layer(indicator).hide()

    def show_layer(self, indicator):
        self.get_layer(indicator).show()

    def clear_layer(self, indicator):
        self.get_layer(indicator).clear()

    def update_z(self):
        for layer in self.layers:
            layer.update_z()
