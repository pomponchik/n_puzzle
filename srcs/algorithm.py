from srcs.errors import FieldIsNotValidError
from srcs.priority_queue import PriorityQueue
from srcs.battlefield import BattleField
from srcs.walker import Walker


class Algorithm:
    def __init__(self, size, data, heuristics):
        self.queue = PriorityQueue()
        self.root_field = BattleField(size, data, heuristics)
        self.queue.push(self.root_field, self.root_field.error)
        self.complexity_in_time = 1

    def check(self):
        points = self.root_field.points
        counter = 0
        for index, point in enumerate(self.root_field.iterate_by_spiral()):
            number = point.value
            if number == 0:
                number = len(points)
            for another_point in self.root_field.iterate_by_spiral(begin=index+1):
                another_number = another_point.value
                if another_number == 0:
                    another_number = len(points)
                if another_number < number:
                    counter += 1
                index += 1
        return not bool(counter % 2)

    def go(self):
        if not self.check():
            raise FieldIsNotValidError('Oh, you scoundrel! Brought me the wrong field! He decided to deceive me!')
        while True:
            field = self.queue.get()
            if field is None:
                return None
            if not field.error:
                return field
            childs = field.get_childs()
            for child in childs:
                self.complexity_in_time += 1
                self.queue.push(child, child.error)
