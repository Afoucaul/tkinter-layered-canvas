import numpy as np


class GriddedCanvasLayer:
    def __init__(self, manager, canvas, width, height, name="Default"):
        self.manager = manager
        self.canvas = canvas
        self.elements = np.zeros((width, height), dtype=np.int16)
        self.name = name

    def execute_draw(self, x, y, canvasMethodName: str, *args, **kwargs):
        if self[x, y]:
            self.delete((x, y))
        callback = getattr(self.canvas, canvasMethodName)
        self[x, y] = callback(*args, **kwargs, tag="layer_{}".format(self.name))
        self.manager.update_z()

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

    def configure_item(self, x, y, **kwargs):
        self.canvas.itemconfig(self[x, y], **kwargs)

    def update_z(self):
        for element in self.elements.flat:
            self.canvas.tag_raise(element)

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value
