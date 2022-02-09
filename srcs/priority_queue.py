from dataclasses import dataclass, field
from typing import Any
import heapq


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class PriorityQueue:
    def __init__(self):
        self.max_elements = 0
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, item, priority):
        if not isinstance(priority, int):
            raise ValueError('The priority must be set as an integer.')
        if item is None:
            raise ValueError('The value must be valid.')
        to_put = PrioritizedItem(priority=priority, item=item)
        heapq.heappush(self.data, to_put)
        if len(self.data) > self.max_elements:
            self.max_elements = len(self.data)

    def get(self):
        try:
            item_wrapper = heapq.heappop(self.data)
            return item_wrapper.item
        except IndexError as e:
            return None
