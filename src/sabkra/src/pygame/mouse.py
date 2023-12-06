class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_prev = 0
        self.y_prev = 0

    def update(self, x: int, y: int):
        self.x_prev, self.y_prev = self.x, self.y
        self.x, self.y = x, y

    def vector(self) -> (int, int):
        return (self.x_prev - self.x, self.y_prev - self.y)
