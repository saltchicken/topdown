INIT_X = 0
INIT_Y = 0
ROW_LENGTH = 20
COLUMN_LENGTH = 16

class Camera():
    def __init__(self, init_pos):
        self.init_pos = init_pos
        self.map_center = [self.init_pos[0], self.init_pos[1]]
        # self.row_length = 22
        # self.col_length = 18
        # TODO: Should this be initialized with offset? Or set to 0.0
        self._x = -32.0
        self._y = 10.0
        self.current_grid = [0, 0]
        # self.x_slice = slice(int(
        #     self.map_center[0] - self.row_length // 2), int(self.map_center[0] + self.row_length // 2))
        # self.y_slice = slice(int(
        #     self.map_center[1] - self.col_length // 2), int(self.map_center[1] + self.col_length // 2))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = round(value, 5)
        # TODO: Why is -1 needed here. Has to do with self._x offset
        self.map_center[0] = int(self.init_pos[0] - self._x // 64) - 1
        # self.x_slice = slice(int(
        #     self.map_center[0] - self.row_length // 2), int(self.map_center[0] + self.row_length // 2))
        # previous_grid = self.current_grid[0]
        self.current_grid[0] = (self.map_center[0] + ROW_LENGTH // 2) // ROW_LENGTH
        # if previous_grid != self.current_grid[0]:
        #     print('Grid changed')

    @y.setter
    def y(self, value):
        self._y = round(value, 5)
        # TODO: +16 is added so that the grid is properly calculated. Why?
        self.map_center[1] = int(self.init_pos[1] - (self._y + 16) // 64)
        # self.y_slice = slice(int(
        #     self.map_center[1] - self.col_length // 2), int(self.map_center[1] + self.col_length // 2))
        # previous_grid = self.current_grid[1]
        self.current_grid[1] = (self.map_center[1] + COLUMN_LENGTH // 2) // COLUMN_LENGTH
        # if previous_grid != self.current_grid[1]:
        #     print('Grid changed')