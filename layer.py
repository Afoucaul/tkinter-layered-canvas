import numpy as np


class GriddedCanvasLayer:
    def __init__(self,
                 manager, canvas, width, height, name="Default", elements=None):
        self.manager = manager
        self.canvas = canvas
        self.name = name
        if elements is not None:
            self.elements = elements
        else:
            self.elements = -np.ones((width, height), dtype=np.int16)

        self.visible = True

    def execute_draw(self, x, y, canvasMethodName: str, *args, **kwargs):
        if self[x, y] != -1:
            self.canvas.delete(self[x, y])
            print("Deleted item {}".format(self[x, y]))
        callback = getattr(self.canvas, canvasMethodName)
        self[x, y] = callback(*args, **kwargs, tag="layer_{}".format(self.name))
        self.manager.update_z()

    def clear(self, at=None):
        if at is not None:
            if self.elements[at] != -1:
                self.canvas.delete(self.elements[at])
                self.elements[at] = -1

        else:
            for element in self.elements.flat:
                self.canvas.delete(element)
            self.elements[:] = -1

    def hide(self):
        for element in self.elements.flat:
            self.canvas.itemconfigure(element, state="hidden")
        self.visible = False

    def show(self):
        for element in self.elements.flat:
            self.canvas.itemconfigure(element, state="normal")
        self.visible = True

    def configure_item(self, x, y, **kwargs):
        self.canvas.itemconfig(self[x, y], **kwargs)

    def update_z(self):
        for element in self.elements.flat:
            self.canvas.tag_raise(element)

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __repr__(self):
        return self.name
