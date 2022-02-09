def base_heuristic(field):
    counter = 0

    for index, point in enumerate(field.points):
        if point.value != field.standard.points[index].value:
            counter += 1
    return counter

def manhattan(field):
    accumulate = 0

    for number in range(field.size ** 2):
        point = field.search_point_by_value(number)
        expected_point = field.standard.search_point_by_value(number)

        sub = point.coordinate - expected_point.coordinate
        accumulate += sub.x + sub.y

    return accumulate

def manhattan_plus(field):
    return manhattan(field) * (field.generation_number + 1)
