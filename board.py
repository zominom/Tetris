from Shapes.Shape import Shape
from utils import WIDTH, HEIGHT

class Board:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self._width = width
        self._height = height
        self.grid = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def is_drawable(self, shape: Shape, position):
        x_offset, y_offset = position
        shape_coords = shape.get_shape()

        for dx, dy in shape_coords:
            x = x_offset + dx
            y = y_offset + dy

            if not (0 <= x < self._width and 0 <= y < self._height):
                return False

            if self.grid[y][x] != (0, 0, 0):
                return False
            
        return True
    def draw_shape(self, shape: Shape, position):
        x_offset, y_offset = position
        shape_coords = shape.get_shape()
        color = shape.get_color()

        if self.is_drawable(shape, position):
            for dx, dy in shape_coords:
                x, y = x_offset + dx, y_offset + dy
                self.grid[y][x] = color
            return True

        return False

    def _move_shape(self, shape: Shape, old_position, new_position):
        self._erase_shape( shape, old_position)

        if not self.is_drawable(shape, new_position):
            self.draw_shape(shape, old_position)
            return False

        self.draw_shape(shape, new_position)
        return True
    
    def rotate_shape(self, shape: Shape, position):
        self._erase_shape(shape, position)
        shape.rotate()

        if not self.is_drawable(shape, position):
            shape.rotate()
            
        self.draw_shape(shape, position)

    def _erase_shape(self, shape: Shape, position):
        x_offset_old, y_offset_old = position
        shape_coords = shape.get_shape()
        for dx, dy in shape_coords:
             x_old, y_old = x_offset_old + dx, y_offset_old + dy
             if 0 <= x_old < self._width and 0 <= y_old < self._height:
                self.grid[y_old][x_old] = (0, 0, 0)

    def move_shape_left(self, shape: Shape, position):
        x_offset, y_offset = position
        new_position = (x_offset - 1, y_offset)
        return new_position if self._move_shape(shape, position, new_position) else position
    
    def move_shape_right(self, shape: Shape, position):
        x_offset, y_offset = position
        new_position = (x_offset + 1, y_offset)
        return new_position if self._move_shape(shape, position, new_position) else position

    def move_shape_down(self, shape: Shape, position):
        x_offset, y_offset = position
        new_position = (x_offset, y_offset + 1)
        return new_position if self._move_shape(shape, position, new_position) else position
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(self._height):
            if all(self.grid[y][x] != (0, 0, 0) for x in range(self._width)):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            for x in range(self._width):
                self.grid[y][x] = (0, 0, 0)