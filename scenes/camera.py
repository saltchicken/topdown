class Camera():
    def __init__(self, init_pos):
        self.init_pos = init_pos
        self.map_center = [self.init_pos[0], self.init_pos[1]]
        self.row_length = 22
        self.col_length = 18
        # TODO: Should this be initialized with offset? Or set to 0.0
        self._x = 32.0
        self._y = 10.0
        self.x_slice = slice(int(
            self.map_center[0] - self.row_length // 2), int(self.map_center[0] + self.row_length // 2))
        self.y_slice = slice(int(
            self.map_center[1] - self.col_length // 2), int(self.map_center[1] + self.col_length // 2))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        # TODO: Find better way to deal with precision issue
        self._x = round(value, 5)
        self.map_center[0] = int(self.init_pos[0] - self._x // 64)
        self.x_slice = slice(int(
            self.map_center[0] - self.row_length // 2), int(self.map_center[0] + self.row_length // 2))

    @y.setter
    def y(self, value):
        # TODO: Find better way to deal with precision issue
        self._y = round(value, 5)
        self.map_center[1] = int(self.init_pos[1] - self._y // 64)
        self.y_slice = slice(int(
            self.map_center[1] - self.col_length // 2), int(self.map_center[1] + self.col_length // 2))