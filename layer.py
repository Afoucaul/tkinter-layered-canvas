import numpy as np


class GriddedCanvasLayer:
    def __init__(self, canvas, width, height, name="Default"):
        self.canvas = canvas
        self.elements = np.zeros((width, height), dtype=np.int16)
        self.name = name

    def execute_draw(self, x, y, canvasMethodName: str, *args):
        if self[x, y]:
            self.delete((x, y))
        self[x, y] = getattr(self.canvas, canvasMethodName)(*args)

    def clear(self, at=None):
        if at is not None:
            if self.elements[at]:
                self.canvas.delete(self.elements[at])
                self.elements[at] = 0

        else:
            width, height = self.elements.shape
            for x, y in zip(range(width), range(height)):
                self.clear((x, y))

    def hide(self):
        for element in self.elements.flat:
            self.canvas.itemconfigure(element, state="hidden")

    def show(self):
        for element in self.elements.flat:
            self.canvas.itemconfigure(element, state="normal")

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value
