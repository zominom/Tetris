from Shapes.Shape import Shape

class IShape(Shape):
    def __init__(self):
        super().__init__()

    def _build_shape(self):
        if self.rotation == 0:
            self.shape = [(i, j) for i in range(self.BLOCK_SIZE * 4) for j in range(self.BLOCK_SIZE)]
        else:
            self.shape = [(j, i) for i in range(self.BLOCK_SIZE * 4) for j in range(self.BLOCK_SIZE)]