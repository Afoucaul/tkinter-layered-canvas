from importlib import import_module


grid_canvas = import_module(".grid_canvas", __name__)

LayeredCanvas = grid_canvas.GriddedFrame
