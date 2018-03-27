import tkinter as tk


class LayerController(tk.Frame):
    VISIBLE_CHAR = "☑"
    HIDDEN_CHAR = "☐"

    def __init__(self, master, canvas):
        super().__init__(master)
        self.canvas = canvas
        self.listbox = tk.Listbox(self, activestyle=tk.NONE)
        self.addButton = tk.Button(
            self, text="+", command=self.on_add_layer)
        self.removeButton = tk.Button(
            self, text="-", command=self.on_remove_layer)
        self.showButton = tk.Button(
            self, text="Show/Hide", command=self.on_show_hide)

        self.canvas.state.trace('w', self.on_layers_changed)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_selected)

        self.listbox.pack()
        self.addButton.pack(side=tk.LEFT)
        self.removeButton.pack(side=tk.LEFT)
        self.showButton.pack(side=tk.LEFT)

        self._update_listbox()

    def on_add_layer(self):
        toplevel = tk.Toplevel(self)
        entry = tk.Entry(toplevel)

        def _on_ok():
            text = entry.get()
            if text:
                self.canvas.add_layer(text)
                toplevel.destroy()

        button = tk.Button(toplevel, text="OK", command=_on_ok)

        entry.pack()
        button.pack()

    def on_remove_layer(self):
        layerIndex = self.listbox.curselection()[0]
        self.canvas.remove_layer(layerIndex)

    def on_show_hide(self):
        if self.canvas.currentLayer is not None:
            if self.canvas.currentLayer.visible:
                self.canvas.hide_layer(self.canvas.currentLayer)
            else:
                self.canvas.show_layer(self.canvas.currentLayer)

    def on_layers_changed(self, *_):
        self._update_listbox()

    def on_listbox_selected(self, _event):
        print(self.listbox.curselection())
        self.canvas.select_layer(self.listbox.curselection()[0])
        print(self.canvas.currentLayer)

    def _update_listbox(self):
        self.listbox.delete(0, tk.END)
        for layer in self.canvas.layers:
            self.listbox.insert(
                tk.END,
                (self.VISIBLE_CHAR if layer.visible
                 else self.HIDDEN_CHAR) + " " + layer.name)
            if layer is self.canvas.currentLayer:
                self.listbox.itemconfig(tk.END, bg="light blue")
