# https://adventofcode.com/2023/day/17

import itertools
from heapq import heappop, heappush
from collections import defaultdict


""" *** Puzzle 1 ***

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up:
half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the
lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high
speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the
crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a
route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds
of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city
block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block.
The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the
bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless
you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three
blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction;
after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive
blocks in the same direction, what is the least heat loss it can incur?
"""

# https://github.com/tmo1/adventofcode/blob/main/2023/17.py


# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
pq = []  # list of entries arranged in a heap
entry_finder = {}  # mapping of tasks to entries
REMOVED = '<removed-task>'  # placeholder for a removed task
counter = itertools.count()  # unique sequence count


def add_task(task, priority=0):
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)


def remove_task(task):
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED


def pop_task():
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')


heat_map = [[int(n) for n in line.strip()] for line in open('input/day_17.txt')]
movement = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
for y in range(len(heat_map)):
    for x in range(len(heat_map[0])):
        for direction in range(4):
            for consecutive in range(1, 4):
                add_task((x, y, direction, consecutive), 1000000)
add_task((0, 0, 1, 0))
total_heat = defaultdict(lambda: 1000000)
total_heat[(0, 0, 1, 0)] = 0
result = 1000000
while True:
    t = pop_task()
    x, y, direction, consecutive = t
    if x == len(heat_map[0]) - 1 and y == len(heat_map) - 1:
        result = total_heat[t]
        break
    neighbors = [((direction + 1) % 4, 1), ((direction - 1) % 4, 1)]
    if consecutive < 3:
        neighbors.append((direction, consecutive + 1))
    for neighbor in neighbors:
        new_direction, new_consecutive = neighbor
        new_x, new_y = x + movement[new_direction][0], y + movement[new_direction][1]
        new_t = (new_x, new_y, new_direction, new_consecutive)
        if 0 <= new_x < len(heat_map[0]) and 0 <= new_y < len(heat_map):
            new_heat = total_heat[t] + heat_map[new_y][new_x]
            if new_heat < total_heat[new_t]:
                total_heat[new_t] = new_heat
                add_task(new_t, new_heat)

print("Solution for Puzzle 1: {}".format(result))


""" *** Puzzle 2 ***

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. 
Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a 
straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before 
it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible 
can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?
"""

# https://github.com/tmo1/adventofcode/blob/main/2023/17b.py


# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
pq = []  # list of entries arranged in a heap
entry_finder = {}  # mapping of tasks to entries
REMOVED = '<removed-task>'  # placeholder for a removed task
counter = itertools.count()  # unique sequence count


def add_task(task, priority=0):
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)


def remove_task(task):
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED


def pop_task():
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')


heat_map = [[int(n) for n in line.strip()] for line in open('input/day_17.txt')]
movement = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
for y in range(len(heat_map)):
    for x in range(len(heat_map[0])):
        for direction in range(4):
            for consecutive in range(1, 11):
                add_task((x, y, direction, consecutive), 1000000)
add_task((0, 0, 1, 0))
add_task((0, 0, 2, 0))
total_heat = defaultdict(lambda: 1000000)
total_heat[(0, 0, 1, 0)], total_heat[(0, 0, 2, 0)] = 0, 0
result = 1000000
while True:
    t = pop_task()
    x, y, direction, consecutive = t
    if x == len(heat_map[0]) - 1 and y == len(heat_map) - 1 and consecutive >= 4:
        result = total_heat[t]
        break
    neighbors = []
    if consecutive >= 4:
        neighbors = [((direction + 1) % 4, 1), ((direction - 1) % 4, 1)]
    if consecutive < 10:
        neighbors.append((direction, consecutive + 1))
    for neighbor in neighbors:
        new_direction, new_consecutive = neighbor
        new_x, new_y = x + movement[new_direction][0], y + movement[new_direction][1]
        new_t = (new_x, new_y, new_direction, new_consecutive)
        if 0 <= new_x < len(heat_map[0]) and 0 <= new_y < len(heat_map):
            new_heat = total_heat[t] + heat_map[new_y][new_x]
            if new_heat < total_heat[new_t]:
                total_heat[new_t] = new_heat
                add_task(new_t, new_heat)

print("Solution for Puzzle 2: {}".format(result))
