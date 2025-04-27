from Shapes.Shape import Shape
class JShape(Shape):
    def __init__(self):
        super().__init__()

    def _build_shape(self):
        if self.rotation == 0:
            self.shape = (
                [(i, j+self.BLOCK_SIZE) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(4 + i, j) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 1:
            self.shape = (
                [(j + self.BLOCK_SIZE, i) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(self.BLOCK_SIZE*self.BLOCK_SIZE+j, 4 + i) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 2:
            self.shape = (
                [(i, j) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(i, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
        else:
            self.shape = (
                [(j+self.BLOCK_SIZE, i) for i in range(3 * self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)] +
                [(i, j) for i in range(self.BLOCK_SIZE) for j in range(self.BLOCK_SIZE)]
            )
