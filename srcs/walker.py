from srcs.coordinate import Coordinate


class Walker:
    def __init__(self, size):
        self.size = size

    def __iter__(self):
        x = 0
        y = 0
        x_right_limit = self.size - 1
        x_left_limit = 0
        y_upper_limit = 0
        y_down_limit = self.size - 1
        directions = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x, y + 1),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
        ]
        new_limits_for_directions = [
            lambda x_right_limit, x_left_limit, y_upper_limit, y_down_limit: (x_right_limit, x_left_limit, y_upper_limit + 1, y_down_limit),
            lambda x_right_limit, x_left_limit, y_upper_limit, y_down_limit: (x_right_limit - 1, x_left_limit, y_upper_limit, y_down_limit),
            lambda x_right_limit, x_left_limit, y_upper_limit, y_down_limit: (x_right_limit, x_left_limit, y_upper_limit, y_down_limit - 1),
            lambda x_right_limit, x_left_limit, y_upper_limit, y_down_limit: (x_right_limit, x_left_limit + 1, y_upper_limit, y_down_limit),
        ]
        direction = 0

        for line_index in range(self.size ** 2):
            yield Coordinate(x, y)

            new_x, new_y = directions[direction](x, y)

            if new_x < x_left_limit or new_x > x_right_limit or new_y < y_upper_limit or new_y > y_down_limit:
                x_right_limit, x_left_limit, y_upper_limit, y_down_limit = new_limits_for_directions[direction](x_right_limit, x_left_limit, y_upper_limit, y_down_limit)
                if direction == 3:
                    direction = 0
                else:
                    direction += 1
                new_x, new_y = directions[direction](x, y)

            x, y = new_x, new_y
