from functools import partial

from srcs.walker import Walker
from srcs.point import Point
from srcs.coordinate import Coordinate


class BattleField:
    casts = set()

    def __init__(self, size, data, heuristics, previous=None, standard=None, generation_number=0):
        self.size = size
        self.points = self.get_points_from_source(data)
        self.link_points()
        self.cursor = self.search_point_by_value(0)
        self.heuristics = heuristics
        self.previous = previous
        self.standard = self.create_standard(size) if standard is None else standard
        self.generation_number = generation_number

    def get_generation_number(self):
        field = self
        count = 0

        while field is not None:
            count += 1
            field = field.previous

        return count

    def iterate_by_spiral(self, begin=0):
        for index, coordinate in enumerate(Walker(self.size)):
            if begin <= index:
                point = self.get_point_by_coordinate(coordinate)
                yield point

    def get_full_string_representation(self):
        field = self
        fields = []

        while field is not None:
            fields.append(str(field))
            field = field.previous

        fields.reverse()

        result = '\n|\nV\n'.join(fields)
        return result

    @classmethod
    def create_standard(cls, size):
        points = []

        for index, coordinate in enumerate(Walker(size)):
            number = 0 if (size ** 2) - 1 == index else index + 1
            points.append((number, coordinate))

        points.sort(key=lambda x: f'{x[1].y}{x[1].x}')
        numbers = [x[0] for x in points]

        result = cls(size, numbers, None, standard=True)
        result.standard = result

        return result

    @property
    def error(self):
        return self.estimate()

    def __str__(self):
        max_len = max([len(str(x.value)) for x in self.points])
        slots = []
        for point in self.points:
            value = point.value
            post_spaces = ' ' * (max_len - len(str(point.value)) + 1)
            slot = f'{value}{post_spaces}'
            slots.append(slot)
        lines = []
        line = []
        for index, slot in enumerate(slots):
            line.append(slot)
            if (index + 1) % (self.size) == 0:
                lines.append(line)
                line = []
        ended_lines = [''.join(slots) for slots in lines]
        result = '\n'.join(ended_lines)
        return result

    def link_points(self):
        for point in self.points:
            point.find_neighbors()

    def estimate(self):
        result = self.heuristics(self)
        return result

    def get_expected_index_by_value(self, value):
        if value == 0:
            return self.size ** 2 - 1
        return value - 1

    def get_points_from_source(self, source):
        result = []
        for index, number in enumerate(source):
            point = Point(number, Coordinate.by_index(index, self.size), self, index)
            result.append(point)
        return result

    def search_point_by_value(self, value):
        for point in self.points:
            if point.value == value:
                return point

    def check_coordinate(self, coordinate):
        coordinate.is_valid(self.size, exception=ValueError(f'Coordinate {coordinate} is not valid.'))

    def get_point_by_coordinate(self, coordinate):
        index = Coordinate.to_index(coordinate, self.size)
        return self.points[index]

    def generate_cast(self):
        return tuple([x.value for x in self.points])

    def copy(self):
        return type(self)(self.size, self.generate_cast(), self.heuristics, previous=self, standard=self.standard, generation_number=self.generation_number+1)

    def get_childs(self):
        coordinates = [x for x in (self.cursor.coordinate.up(), self.cursor.coordinate.down(), self.cursor.coordinate.left(), self.cursor.coordinate.right()) if x.is_valid(self.size)]
        childs = []
        for coordinate in coordinates:
            field = self.copy()
            field.cursor < field.get_point_by_coordinate(coordinate)
            cast = field.generate_cast()
            if cast not in self.casts:
                self.casts.add(cast)
                childs.append(field)
        return childs
