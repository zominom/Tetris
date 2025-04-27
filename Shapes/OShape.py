from Shapes.Shape import Shape

class OShape(Shape):
    def __init__(self):
        super().__init__()
        
    def _build_shape(self):
        self.shape = (
            [(i, j) for i in range(self.BLOCK_SIZE*2) for j in range(self.BLOCK_SIZE*2)]
        )