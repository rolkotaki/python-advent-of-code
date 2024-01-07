# https://adventofcode.com/2023/day/13

""" *** Puzzle 1 ***

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping
them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at
strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to
run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully
analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between
two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns
point at the line between the columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not
perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored;
every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9,
column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8,
but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches
row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that,
also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first
pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total
of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your
notes?
"""

nodes = [[[n for n in node_line] for node_line in node_lines.split('\n')]
         for node_lines in open('input/day_13.txt').read().strip().split('\n\n')]
result = 0
for node in nodes:
    for row in range(0, len(node)-1):
        if node[row] == node[row + 1]:
            for row_diff in range(1, min(row, len(node) - (row + 2)) + 1):
                if node[row - row_diff] != node[row + 1 + row_diff]:
                    break
            else:
                result += (row + 1) * 100
                break
    for col in range(0, len(node[0]) - 1):
        if [n[col] for n in node] == [n[col + 1] for n in node]:
            for col_diff in range(1, min(col, len(node[0]) - (col + 2)) + 1):
                if [n[col - col_diff] for n in node] != [n[col + 1 + col_diff] for n in node]:
                    break
            else:
                result += col + 1
                break

print("Solution for Puzzle 1: {}".format(result))


""" *** Puzzle 2 ***

You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, 
because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the 
opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. 
(The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, 
horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. 
Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, 
row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's
new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to 
the value 400.

In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the 
new reflection line in each pattern in your notes?
"""

nodes = [[[n for n in node_line] for node_line in node_lines.split('\n')]
         for node_lines in open('input/day_13.txt').read().strip().split('\n\n')]
result = 0
for node in nodes:
    for row in range(1, len(node)):
        differences = 0
        top_rows = node[0:row][::-1]
        bottom_rows = node[row:min(len(node), row + row)]
        for top_row, bottom_row in zip(top_rows, bottom_rows):
            for top_x, bottom_x in zip(top_row, bottom_row):
                if top_x != bottom_x:
                    differences += 1
        if differences == 1:
            result += row * 100
            break

    for col in range(1, len(node[0])):
        differences = 0
        left_cols = [[node_row[a] for node_row in node] for a in range(0, len(node[0]))][0:col][::-1]
        right_cols = [[node_row[a] for node_row in node] for a in range(0, len(node[0]))][col:min(len(node[0]), col + col)]
        for left_col, right_col in zip(left_cols, right_cols):
            for left_y, right_y in zip(left_col, right_col):
                if left_y != right_y:
                    differences += 1
        if differences == 1:
            result += col
            break

print("Solution for Puzzle 2: {}".format(result))
