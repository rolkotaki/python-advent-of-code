# https://adventofcode.com/2023/day/16

""" *** Puzzle 1 ***

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you
discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and
pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.),
mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of
the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it
encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For
instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a
rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter
were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same
direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two
directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter
would split into two beams: one that continues upward from the splitter's column and one that continues downward from
the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is
energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in
multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only
showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the
current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?
"""

contraption = [[c for c in line.strip()] for line in open('input/day_16.txt').readlines()]
contraption_energy = [['.' for c in row] for row in contraption]
contraption_energy[0][0] = '#'

if contraption[0][0] in '\\/':
    direction = 'D'
elif contraption[0][0] in '/':
    direction = 'U'
else:
    direction = 'R'

steps = [(direction, (0, 0))]
executed_steps = set()
while steps:
    if steps[-1] in executed_steps:
        steps.pop()
        continue
    direction, p = steps.pop()
    executed_steps.add((direction, p))

    if direction == 'R':
        for i in range(p[1] + 1, len(contraption[p[0]])):
            if contraption[p[0]][i] in ['\\', '/', '|']:
                next_encounter = (p[0], i)
                break
        else:
            next_encounter = (p[0], len(contraption[p[0]])-1)
        for i in range(p[1] + 1, next_encounter[1] + 1):
            contraption_energy[p[0]][i] = '#'
        if contraption[next_encounter[0]][next_encounter[1]] not in ['\\', '/', '|']:
            continue
        if contraption[next_encounter[0]][next_encounter[1]] == '\\':
            steps.append(('D', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '/':
            steps.append(('U', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '|':
            steps.append(('D', next_encounter))
            steps.append(('U', next_encounter))

    elif direction == 'L':
        for i in range(p[1] - 1, -1, -1):
            if contraption[p[0]][i] in ['\\', '/', '|']:
                next_encounter = (p[0], i)
                break
        else:
            next_encounter = (p[0], 0)
        for i in range(next_encounter[1], p[1]):
            contraption_energy[p[0]][i] = '#'
        if contraption[next_encounter[0]][next_encounter[1]] not in ['\\', '/', '|']:
            continue
        if contraption[next_encounter[0]][next_encounter[1]] == '\\':
            steps.append(('U', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '/':
            steps.append(('D', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '|':
            steps.append(('D', next_encounter))
            steps.append(('U', next_encounter))

    elif direction == 'U':
        for i in range(p[0] - 1, -1, -1):
            if [row[p[1]] for row in contraption][i] in ['\\', '/', '-']:
                next_encounter = (i, p[1])
                break
        else:
            next_encounter = (0, p[1])
        for i in range(next_encounter[0], p[0] + 1):
            contraption_energy[i][p[1]] = '#'
        if contraption[next_encounter[0]][next_encounter[1]] == 'O':
            continue
        if contraption[next_encounter[0]][next_encounter[1]] == '\\':
            steps.append(('L', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '/':
            steps.append(('R', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '-':
            steps.append(('L', next_encounter))
            steps.append(('R', next_encounter))

    elif direction == 'D':
        for i in range(p[0] + 1, len([row[p[1]] for row in contraption])):
            if [row[p[1]] for row in contraption][i] in ['\\', '/', '-']:
                next_encounter = (i, p[1])
                break
        else:
            next_encounter = (len([row[p[1]] for row in contraption])-1, p[1])
        for i in range(p[0], next_encounter[0] + 1):
            contraption_energy[i][p[1]] = '#'
        if contraption[next_encounter[0]][next_encounter[1]] == 'O':
            continue
        if contraption[next_encounter[0]][next_encounter[1]] == '\\':
            steps.append(('R', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '/':
            steps.append(('L', next_encounter))
        elif contraption[next_encounter[0]][next_encounter[1]] == '-':
            steps.append(('L', next_encounter))
            steps.append(('R', next_encounter))

print("Solution for Puzzle 1: {}".format(sum([row.count('#') for row in contraption_energy])))


""" *** Puzzle 2 ***

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. 
There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading 
away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if 
the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), 
any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, 
you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that 
configuration?
"""

contraption = [[c for c in line.strip()] for line in open('input/day_16.txt').readlines()]
energized_tiles = []

starting_points = [['D', (0, col)] for col in range(0, len(contraption[0]))] + \
                  [['U', (len(contraption[0]) - 1, col)] for col in range(0, len(contraption[0]))] + \
                  [['R', (row, 0)] for row in range(0, len(contraption))] + \
                  [['L', (row, len(contraption[0]) - 1)] for row in range(0, len(contraption))]

while starting_points:
    item = starting_points.pop()
    direction = item[0]
    starting_point = item[1]

    if contraption[starting_point[0]][starting_point[1]] == '\\':
        if direction == 'D':
            direction = 'R'
        elif direction == 'U':
            direction = 'L'
        elif direction == 'R':
            direction = 'D'
        elif direction == 'L':
            direction = 'U'
    elif contraption[starting_point[0]][starting_point[1]] == '/':
        if direction == 'D':
            direction = 'L'
        elif direction == 'U':
            direction = 'R'
        elif direction == 'R':
            direction = 'U'
        elif direction == 'L':
            direction = 'D'
    elif contraption[starting_point[0]][starting_point[1]] == '-':
        if direction in 'DU':
            direction = 'L'
            starting_points.append(['R', starting_point])
    elif contraption[starting_point[0]][starting_point[1]] == '|':
        if direction in 'RL':
            direction = 'D'
            starting_points.append(['U', starting_point])

    contraption_energy = [['.' for c in row] for row in contraption]
    contraption_energy[starting_point[0]][starting_point[1]] = '#'
    steps = [(direction, starting_point)]
    executed_steps = set()

    while steps:
        if steps[-1] in executed_steps:
            steps.pop()
            continue
        direction, p = steps.pop()
        executed_steps.add((direction, p))

        if direction == 'R':
            for i in range(p[1] + 1, len(contraption[p[0]])):
                if contraption[p[0]][i] in ['\\', '/', '|']:
                    next_encounter = (p[0], i)
                    break
            else:
                next_encounter = (p[0], len(contraption[p[0]]) - 1)
            for i in range(p[1] + 1, next_encounter[1] + 1):
                contraption_energy[p[0]][i] = '#'
            if contraption[next_encounter[0]][next_encounter[1]] not in ['\\', '/', '|']:
                continue
            if contraption[next_encounter[0]][next_encounter[1]] == '\\':
                steps.append(('D', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '/':
                steps.append(('U', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '|':
                steps.append(('D', next_encounter))
                steps.append(('U', next_encounter))

        elif direction == 'L':
            for i in range(p[1] - 1, -1, -1):
                if contraption[p[0]][i] in ['\\', '/', '|']:
                    next_encounter = (p[0], i)
                    break
            else:
                next_encounter = (p[0], 0)
            for i in range(next_encounter[1], p[1]):
                contraption_energy[p[0]][i] = '#'
            if contraption[next_encounter[0]][next_encounter[1]] not in ['\\', '/', '|']:
                continue
            if contraption[next_encounter[0]][next_encounter[1]] == '\\':
                steps.append(('U', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '/':
                steps.append(('D', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '|':
                steps.append(('D', next_encounter))
                steps.append(('U', next_encounter))

        elif direction == 'U':
            for i in range(p[0] - 1, -1, -1):
                if [row[p[1]] for row in contraption][i] in ['\\', '/', '-']:
                    next_encounter = (i, p[1])
                    break
            else:
                next_encounter = (0, p[1])
            for i in range(next_encounter[0], p[0] + 1):
                contraption_energy[i][p[1]] = '#'
            if contraption[next_encounter[0]][next_encounter[1]] == 'O':
                continue
            if contraption[next_encounter[0]][next_encounter[1]] == '\\':
                steps.append(('L', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '/':
                steps.append(('R', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '-':
                steps.append(('L', next_encounter))
                steps.append(('R', next_encounter))

        elif direction == 'D':
            for i in range(p[0] + 1, len([row[p[1]] for row in contraption])):
                if [row[p[1]] for row in contraption][i] in ['\\', '/', '-']:
                    next_encounter = (i, p[1])
                    break
            else:
                next_encounter = (len([row[p[1]] for row in contraption]) - 1, p[1])
            for i in range(p[0], next_encounter[0] + 1):
                contraption_energy[i][p[1]] = '#'
            if contraption[next_encounter[0]][next_encounter[1]] == 'O':
                continue
            if contraption[next_encounter[0]][next_encounter[1]] == '\\':
                steps.append(('R', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '/':
                steps.append(('L', next_encounter))
            elif contraption[next_encounter[0]][next_encounter[1]] == '-':
                steps.append(('L', next_encounter))
                steps.append(('R', next_encounter))

    energized_tiles.append(sum([row.count('#') for row in contraption_energy]))

print("Solution for Puzzle 2: {}".format(max(energized_tiles)))
