# https://adventofcode.com/2023/day/14

""" *** Puzzle 1 ***

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you
tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped
rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input).
For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't
collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of
the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load
caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
beams?
"""

input_data = [line.strip() for line in open('input/day_14.txt').readlines()]
columns = [[line.strip()[col] for line in input_data] for col in range(0, len(input_data[0]))]
for col in range(0, len(columns)):
    min_index = 0
    for i in range(0, len(columns[col])):
        if columns[col][i] == '#':
            min_index = i + 1
        elif columns[col][i] == 'O' and i > min_index:
            columns[col][min_index] = 'O'
            columns[col][i] = '.'
            min_index += 1
        elif columns[col][i] == 'O':
            min_index += 1

print("Solution for Puzzle 1: {}".format(sum([[col[row] for col in columns].count('O') * (len(input_data) - row)
                                              for row in range(0, len(input_data))])))


""" *** Puzzle 2 ***

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks 
to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to 
do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After 
each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, 
the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support beams. 
To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 
1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?
"""


def tilt(data):
    for n in range(0, len(data)):
        min_index = 0
        for i in range(0, len(data[n])):
            if data[n][i] == '#':
                min_index = i + 1
            elif data[n][i] == 'O' and i > min_index:
                data[n][min_index] = 'O'
                data[n][i] = '.'
                min_index += 1
            elif data[n][i] == 'O':
                min_index += 1


rows = [[c for c in line.strip()] for line in open('input/day_14.txt').readlines()]
cycle = 0
loads = {}
load_list = []
repeating_from = -1
while repeating_from == -1:
    cycle += 1
    columns = [list(sublist) for sublist in list(zip(*rows))]
    tilt(columns)
    rows = [list(sublist) for sublist in list(zip(*columns))]
    tilt(rows)
    columns = [list(sublist)[::-1] for sublist in list(zip(*rows))]
    tilt(columns)
    rows = [list(sublist)[::-1] for sublist in list(zip(*[col[::-1] for col in columns]))]
    tilt(rows)
    rows = [row[::-1] for row in rows]

    load = sum([rows[row].count('O') * (len(rows) - row) for row in range(0, len(rows))])
    if load in loads.keys():
        for r in loads.get(load):
            if r[1] == rows:
                repeating_from = r[0]
                break
        else:
            loads.get(load).append((cycle, rows))
    else:
        loads[load] = [(cycle, rows)]
    load_list.append(load)

result = load_list[repeating_from + ((1_000_000_000-repeating_from-1) % (len(load_list) - repeating_from))]

print("Solution for Puzzle 2: {}".format(result))
