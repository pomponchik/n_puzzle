from sys import argv

from srcs.goodbye import goodbye
from srcs.reader import Reader
from srcs.algorithm import Algorithm

from srcs.heuristics import base_heuristic, manhattan, manhattan_plus, all

from srcs.errors import FieldIsNotValidError



def main():
    if not (len(argv) == 2 or len(argv) == 3):
        goodbye('Usage: python3 npuzzle.py [path to the file]')

    path = argv[1]
    size, data = Reader(path).get_size_and_data_from_file()

    heuristics = {
        'base': base_heuristic,
        'manhattan': manhattan,
        'manhattan+': manhattan_plus,
        'all': all,
    }

    if len(argv) == 2:
        heuristic_name = 'base'
    else:
        heuristic_name = argv[2]

    heuristic = heuristics.get(heuristic_name, None)

    if heuristic is None:
        goodbye(f'A heuristic named "{heuristic_name}" is not provided.')

    try:
        algo = Algorithm(size, data, heuristic)
        result = algo.go()
        print(result.get_full_string_representation())
        print()
        print(f'Complexity in time: {algo.complexity_in_time}')
        print(f'Complexity in size: {algo.queue.max_elements}')
        print(f'Number of moves: {result.generation_number}')

    except FieldIsNotValidError:
        goodbye('This version of the puzzle is unsolvable.')


if __name__ == '__main__':
    main()
