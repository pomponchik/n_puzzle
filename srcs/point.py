from srcs.coordinate import Coordinate


class Point:
    def __init__(self, value, coordinate, field, index):
        self.coordinate = coordinate
        self.field = field
        self._value = value
        self.index = index
        self.error = self.estimate(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.reestimate(new_value)
        self._value = new_value
        if new_value == 0:
            self.field.cursor = self

    def estimate(self, value):
        expected_index = self.field.get_expected_index_by_value(value)

        expected_coordinate = Coordinate.by_index(expected_index, self.field.size)
        result = (expected_coordinate - self.coordinate).estimate()
        return result

    def reestimate(self, value):
        self.error = self.estimate(value)

    def find_neighbors(self):
        maybe_neighbors_coordinates = [self.coordinate.up(), self.coordinate.down(), self.coordinate.right(), self.coordinate.left()]
        neighbors_coordinates = []
        for candidate in maybe_neighbors_coordinates:
            if candidate.is_valid(self.field.size):
                neighbors_coordinates.append(candidate)
        neighbors = []
        for coordinate in neighbors_coordinates:
            neighbors.append(self.field.get_point_by_coordinate(coordinate))
        self.neighbors = neighbors

    def exchange_values(self, other):
        self.value, other.value = other.value, self.value

    def __lt__(self, other):
        if self.value != 0:
            raise ValueError('You can only move other cells to the cell with a zero value.')
        self.exchange_values(other)

    def __gt__(self, other):
        if other.value != 0:
            raise ValueError('You can only move other cells to the cell with a zero value.')
        self.exchange_values(other)
