from Shapes.Shape import Shape

class SShape(Shape):
    def __init__(self):
        super().__init__()

    def _build_shape(self):
        if self.rotation == 0:
            self.shape = (
                [(i, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)] +
                [(i+self.BLOCK_SIZE, j) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 1:
            self.shape = (
                [(j, i) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)] +
                [(j+self.BLOCK_SIZE, i+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)]
            )
        elif self.rotation == 2: # Same as rotation 0
            self.shape = (
                [(i, j+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE*2) for j in range(self.BLOCK_SIZE)] +
                [(i+self.BLOCK_SIZE, j) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)]
            )
        else: # Same as rotation 1
            self.shape = (
                [(j, i) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)] +
                [(j+self.BLOCK_SIZE, i+self.BLOCK_SIZE) for i in range(self.BLOCK_SIZE * 2) for j in range(self.BLOCK_SIZE)]
            )
