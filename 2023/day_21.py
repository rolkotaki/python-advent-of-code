# https://adventofcode.com/2023/day/21

from collections import defaultdict


""" *** Puzzle 1 ***

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like
your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with
exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#).
For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south,
east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him
to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the
first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position (either by going
north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any
of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden
plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?
"""

garden_map = [[c for c in line.strip()] for line in open('input/day_21.txt').readlines()]
s_pos = tuple()
for row in range(len(garden_map)):
    if 'S' in garden_map[row]:
        s_pos = (row, garden_map[row].index('S'))
        break

directions = ((0, -1), (0, 1), (1, 0), (-1, 0))
visited = set()
possibilities_by_step = defaultdict(int)
steps = [(s_pos, 0)]
while steps:
    cur_pos, step_number = steps.pop(0)
    if step_number > 64 or cur_pos in visited:
        continue
    visited.add(cur_pos)
    possibilities_by_step[step_number] += 1
    for d in directions:
        if 0 <= cur_pos[0] + d[0] < len(garden_map) and 0 <= cur_pos[1] + d[1] < len(garden_map[0]):
            if (cur_pos[0] + d[0], cur_pos[1] + d[1]) not in visited:
                if garden_map[cur_pos[0] + d[0]][cur_pos[1] + d[1]] != '#':
                    steps.append(((cur_pos[0] + d[0], cur_pos[1] + d[1]), step_number + 1))
# to avoid repetitions
result = sum(count for step_number, count in possibilities_by_step.items() if step_number % 2 == 64 % 2)

print("Solution for Puzzle 1: {}".format(result))


""" *** Puzzle 2 ***

The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers 
that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would 
find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat
as far as you can see. The Elf still starts on the one middle tile marked S, though - every other repeated S is replaced
with a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of 
steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, how 
many garden plots could the Elf reach in exactly 26501365 steps?
"""

garden_map = [[c for c in line.strip()] for line in open('input/day_21.txt').readlines()]
s_pos = tuple()
for row in range(len(garden_map)):
    if 'S' in garden_map[row]:
        s_pos = (row, garden_map[row].index('S'))
        break

width = len(garden_map[0])
height = len(garden_map)
directions = ((0, -1), (0, 1), (1, 0), (-1, 0))


def count_possibilities(max_steps):
    visited = set()
    possibilities_by_step = defaultdict(int)
    steps = [(s_pos, 0)]
    while steps:
        cur_pos, step_number = steps.pop(0)
        if step_number > max_steps or cur_pos in visited:
            continue
        visited.add(cur_pos)
        possibilities_by_step[step_number] += 1
        for d in directions:
            if (cur_pos[0] + d[0], cur_pos[1] + d[1]) not in visited:
                if garden_map[(cur_pos[0] + d[0]) % height][(cur_pos[1] + d[1]) % width] != '#':
                    steps.append(((cur_pos[0] + d[0], cur_pos[1] + d[1]), step_number + 1))
    # to avoid repetitions
    return sum(count for step_number, count in possibilities_by_step.items() if step_number % 2 == max_steps % 2)


# https://github.com/CalSimmon/advent-of-code/blob/main/2023/day_21/solution.py
# Calculate the first three data points for use in the quadratic formula, and then return the output of quad
goal = 26501365
edge = width // 2
y = [count_possibilities((edge + i * width)) for i in range(3)]
# Use the quadratic formula to find the output at the large steps based on the first three data points
a = (y[2] - (2 * y[1]) + y[0]) // 2
b = y[1] - y[0] - a
c = y[0]
n = ((goal - edge) // width)
result = (a * n**2) + (b * n) + c

print("Solution for Puzzle 2: {}".format(result))
