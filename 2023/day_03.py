# https://adventofcode.com/2023/day/3

from functools import reduce


""" *** Puzzle 1 ***

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one.
If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a
"part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and
58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine
schematic?
"""

engine_number_list = list()
number_coordinates = list()
symbol_coordinates = {(line[0] + x, gear[0] + y) for line in enumerate(open('input/day_03.txt').readlines())
                      for gear in filter(lambda x: x[1] not in '.0123456789', enumerate(line[1].strip()))
                      for x in range(-1, 2) for y in range(-1, 2)}

with open('input/day_03.txt') as f:
    line = f.readline().strip()
    row = 0
    while line:
        digits = list(filter(lambda x: x[1] in '0123456789', enumerate(line)))
        number = ''
        coordinates = []
        last_index = 999
        for i in range(0, len(digits)):
            digit = digits[i]
            if digit[0] - last_index > 1:
                number_coordinates.append([int(number), coordinates])
                number = ''
                coordinates = []
            if i == len(digits) - 1:
                number += digit[1]
                coordinates.append((row, digit[0]))
                number_coordinates.append([int(number), coordinates])
                continue
            number += digit[1]
            coordinates.append((row, digit[0]))
            last_index = digit[0]
        row += 1
        line = f.readline().strip()
    # filter on the numbers adjacent to symbols
    engine_number_list = [item[0] for item in filter(lambda x: set(x[1]) & symbol_coordinates, number_coordinates)]

print("Solution for Puzzle 1: {}".format(sum(engine_number_list)))


""" *** Puzzle 2 ***

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is 
adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which 
gear needs to be replaced.

Consider the same engine schematic again:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio 
is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because 
it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

gear_ratio_list = list()
number_coordinates = list()
gear_coordinates = {(line[0], gear[0]) for line in enumerate(open('input/day_03.txt').readlines())
                    for gear in filter(lambda x: x[1] in '*', enumerate(line[1].strip()))}

with open('input/day_03.txt') as f:
    line = f.readline().strip()
    row = 0
    while line:
        digits = list(filter(lambda x: x[1] in '0123456789', enumerate(line)))
        number = ''
        coordinates = set()
        last_index = 999
        for i in range(0, len(digits)):
            digit = digits[i]
            if digit[0] - last_index > 1:
                number_coordinates.append([int(number), coordinates])
                number = ''
                coordinates = set()
            if i == len(digits) - 1:
                number += digit[1]
                coordinates |= {(row + x, digit[0] + y) for x in range(-1, 2) for y in range(-1, 2)}
                number_coordinates.append([int(number), coordinates])
                continue
            number += digit[1]
            coordinates |= {(row + x, digit[0] + y) for x in range(-1, 2) for y in range(-1, 2)}
            last_index = digit[0]
        row += 1
        line = f.readline().strip()

    gear_ratio_list = [reduce(lambda x, y: x[0] * y[0], filter(lambda x: gear in x[1], number_coordinates))
                       for gear in gear_coordinates
                       if len(list(filter(lambda x: gear in x[1], number_coordinates))) == 2]

print("Solution for Puzzle 2: {}".format(sum(gear_ratio_list)))
