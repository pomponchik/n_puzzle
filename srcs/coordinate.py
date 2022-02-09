from functools import total_ordering


@total_ordering
class Coordinate:
    def __init__(self, x, y, is_difference=False):
        self.x = x
        self.y = y
        self.is_difference = is_difference

    def __repr__(self):
        is_diff = ', is_difference=True' if self.is_difference else ''
        return f'{type(self).__name__}({self.x}, {self.y}{is_diff})'

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError('You can only subtract coordinate objects from each other.')
        x = max((self.x, other.x)) - min((self.x, other.x))
        y = max((self.y, other.y)) - min((self.y, other.y))
        return type(self)(x, y, is_difference=True)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise ValueError('Impossible comparison.')
        if self.y < other.y:
            return True
        if self.x < other.x:
            return True
        return False

    def down(self):
        return type(self)(self.x, self.y + 1)

    def up(self):
        return type(self)(self.x, self.y - 1)

    def left(self):
        return type(self)(self.x - 1, self.y)

    def right(self):
        return type(self)(self.x + 1, self.y)

    def is_valid(self, size_of_field, exception=None):
        result = size_of_field > self.x >= 0 and size_of_field > self.y >= 0
        if exception is not None and not result:
            raise exception
        return result

    def estimate(self):
        if self.is_difference:
            return self.x + self.y
        raise ValueError('The evaluation can only be performed for the difference between the coordinates.')

    @classmethod
    def by_index(cls, index, size_of_field):
        if index < 0:
            raise ValueError('Index must be >= 0.')
        y = index // size_of_field
        x = index - (y * size_of_field)
        return cls(x, y)

    @staticmethod
    def to_index(coordinate, size_of_field):
        return coordinate.y * size_of_field + coordinate.x
