import tkinter as tk
import grid_canvas


class MyLayeredCanvas(grid_canvas.GriddedFrame):
    def draw_circle(self, x, y):
        cx, cy = self.get_center_of_cell(x, y)
        self.currentLayer.execute_draw(
            x, y, "create_oval", cx-10, cy-10, cx+10, cy+10, fill="red")

    def draw_square(self, x, y):
        cx, cy = self.get_center_of_cell(x, y)
        self.currentLayer.execute_draw(
            x, y, "create_rectangle", cx-20, cy-20, cx+20, cy+20, fill="blue")


def test_operations():
    delay = 100

    root = tk.Tk()
    f = MyLayeredCanvas(root, 4, 4, 64, 64)
    f.pack()
    f.layers.pop()

    f.add_layer("squares")
    f.add_layer("circles")
    root.update()
    f.after(delay)

    f.select_layer("squares")
    f.draw_square(1, 1)
    root.update()
    f.after(delay)

    f.select_layer("circles")
    f.draw_circle(2, 2)
    root.update()
    f.after(delay)

    f.hide_layer("squares")
    root.update()
    f.after(delay)

    f.show_layer("squares")
    root.update()
    f.after(delay)

    f.clear_layer("squares")

    root.mainloop()


def test_occlusion():
    delay = 1000

    root = tk.Tk()
    f = MyLayeredCanvas(root, 4, 4, 64, 64)
    f.pack()
    f.layers.pop()

    f.add_layer("circles")
    f.add_layer("squares")
    root.update()
    f.after(delay)

    f.select_layer("squares")
    f.draw_square(1, 1)
    print("Drawing square")
    root.update()
    f.after(delay)

    f.select_layer("circles")
    f.draw_circle(1, 1)
    print("Drawing circle")
    root.update()
    f.after(delay)

    f.raise_layer("circles")
    print("Raising circles")
    root.update()
    f.after(delay)

    f.raise_layer("squares")
    print("Raising squares")
    root.update()
    f.after(delay)

    f.lower_layer("squares")
    print("Lowering squares")
    root.update()
    f.after(delay)

    f.remove_layer("squares")
    print("Removing squares")

    root.mainloop()


test_occlusion()
