from Shapes.Shape import Shape

class TShape(Shape):
    def __init__(self):
        super().__init__()

    def _build_shape(self):
        if self.rotation == 0:
            self.shape = (
                [(i, j+self.BLOCK_SIZE) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(i+self.BLOCK_SIZE, j) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 1:
            self.shape = (
                [(i, j) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE * 3)] +
                [(i+self.BLOCK_SIZE, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 2:
            self.shape = (
                [(i, j) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(i+self.BLOCK_SIZE, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        else:
            self.shape = (
                [(i+self.BLOCK_SIZE, j) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE * 3)] +
                [(i, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )