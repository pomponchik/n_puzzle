# NPuzzle - решатель пятнашек

Есть такая игра из жанра [комбинаторных](https://en.wikipedia.org/wiki/Combination_puzzle) - [пятнашки](https://en.wikipedia.org/wiki/15_puzzle). В ней игроку дается поле 4 на 4, на котором расположены 15 квадратиков с числами от 1 до 15 и еще один пустой слот. Задача игрока - сдвигать квадратики с числами на этот пустой слот до тех пор, пока числа не окажутся выстроенными в нужном порядке.

У данной игры есть вариации, чаще всего связанные с размерами полей (то есть не только 4 на 4, но и, к примеру, 5 на 5, или 3 на 3) или с порядком чисел, к которому по итогу нужно придти.

Алгоритмическое решение здесь сложно тем, что каждое действие игрока изменяет игровое поле. Поэтому обычно задачу решают с помощью алгоритмов поиска пути (чаще всего это вариации вокруг [A*](https://en.wikipedia.org/wiki/A*_search_algorithm)), где программа "путешествует" по веткам изменений состояния поля. Для оценки каждого нового состояния обычно используются эвристики, из которых самая популярная - [манхэттенское расстояние](https://en.wikipedia.org/wiki/Taxicab_geometry).

В данной реализации используется алгоритм A*, а эвристик на выбор предлагается 4 штуки. Итоговый порядок расстановки чисел не обычный линейный, а спиральный.


### Использование программы

Программа запускается и выводит результаты своей работы через консоль. Для запуска необходимо подать ей на вход путь к файлу, в котором описано стартовое состояние игрового поля, например вот так:

```bash
python3 npuzzle.py examples/5.txt
```

Но я советую вместо стандартного интерпретатора использовать [pypy](https://www.pypy.org/), обычно это ускоряет решение примерно в 100 раз.

Содержимое файла должно выглядеть примерно так:

```
# This puzzle is solvable
4
14  7 15  2
 5  8 10  1
12  4  3 11
 0 13  6  9
```

На первой строчке здесь указан размер игрового поля (то есть у поля размером 5 на 5 там будет 5), а последующие просто описывают расположение чисел на поле. Пустая клеточка здесь обозначается нулем.

Результат выводится в виде последовательности состояний поля, примерно вот так (здесь приведен только конец вывода для приведенного выше поля, поскольку иначе это заняло бы очень много места):

```
...
1  2  3  4
12 13 14 5
10 11 15 6
9  0  8  7
|
V
1  2  3  4
12 13 14 5
10 11 15 6
0  9  8  7
|
V
1  2  3  4
12 13 14 5
0  11 15 6
10 9  8  7
|
V
1  2  3  4
12 13 14 5
11 0  15 6
10 9  8  7

Complexity in time: 13035
Complexity in size: 6699
Number of moves: 500
```

Текст, который выводится в конце, позволяет оценить масштаб вычислений, которые пришлось проделать программе, чтобы придти к решению. "Complexity in time" - это общее число комбинаций полей, которое было просмотрено. "Complexity in size" - это максимальное число полей, которые одновременно лежали в очереди с приоритетом (чтобы узнать, зачем нужна эта очередь - читайте, как устроен алгоритм A*). "Number of moves" - итоговое число перестановок на поле, которое нужно, чтобы привести его в желаемое состояние.


## Выбор эвристики

По умолчанию для оценки поля программа использует эвристику "base". Она просто подсчитывает, сколько чисел в данный момент находятся не на своих местах (так называемое "[расстояние Хэмминга](https://en.wikipedia.org/wiki/Hamming_distance)"). Но поддерживаются еще 3 эвристики: "manhattan", "manhattan+" и "all". Указать эвристику можно передачей ее названия в качестве еще одного аргумента при запуске программы:

```bash
python3 npuzzle.py examples/5.txt manhattan
```

Эвристика "manhattan" подсчитывает классическое [манхэттенское расстояние](https://en.wikipedia.org/wiki/Taxicab_geometry) для каждого числа между его "идеальным" положением на поле (то есть таким, которого мы хотим добиться) и положением в данный момент. Сумма таких расстояний представляет собой оценку текущего отклонения поля от идеального состояния. Чем оно больше - тем хуже, а в идеале оно должно быть равно нулю.

Эвристика "manhattan+" еще прибавляет к оценке текущего состояния поля количество шагов, которые пришлось сделать, чтобы к нему придти. Если A* c обычным "manhattan" - это так называемый [жадный алгоритм](https://en.wikipedia.org/wiki/Greedy_algorithm), то с данной его вариацией - уже нет.

Различные эвристики могут давать разные результаты и требовать разного объема вычислений. К примеру, для приведенного выше поля эвристика "manhattan" выдает:

```
Complexity in time: 1943
Complexity in size: 1124
Number of moves: 172
```

Как видим, количество шагов сократилось примерно в 3 раза, также сильно упало число просмотренных вариантов. И сравним это с "manhattan+":

```
Complexity in time: 984296
Complexity in size: 509626
Number of moves: 84
```

Бросается в глаза, что, хоть мы и сократили количество шагов более чем в 2 раза, для этого пришлось проделать драматически больше работы - примерно в 500 раз. К слову, если на предыдущих эвристиках на моем компьютере (MacBook Air на m1) все считалось практически мгновенно, то тут ему пришлось заметно попотеть, на вычисления ушли примерно 1 час и 10 минут (на pypy - 1 минута и 20 секунд).

Последняя из эвристик - "all". Она является просто суммой всех прочих эвристик, но вес "manhattan" в ней удвоен - как выяснилось опытным путем, это резко повышает ее эффективность. Попробуем:

```
Complexity in time: 766392
Complexity in size: 393465
Number of moves: 70
```

Как видим, она выдала самое маленькое количество шагов, причем на это ушло меньше вычислений, чем на "manhattan+", но все еще намного больше, чем на просто "manhattan".

## Проверка поля на валидность

Решателя пятнашек легко завести в тупик. Для этого достаточно поменять местами числа в любых двух соседних клетках. В этом случае, как бы он ни перемещал числа по полю, он никогда не придет к правильному порядку. В данной программе перед запуском основного алгоритма происходит соответствующая проверка. Если поле ее не прошло, появится следующее сообщение:

```
This version of puzzle is unsolvable.
```
