# https://adventofcode.com/2023/day/12

from itertools import product
import re
import functools


""" *** Puzzle 1 ***

There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs
would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also
damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every
spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself
damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different
format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the
order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire
size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always
be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?).
For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
Equipped with this information, it is your job to figure out how many different arrangements of operational and broken
springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in
that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#),
making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ?
must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one
of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two;
if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are
four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and
second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of
unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#
In this example, the number of possible arrangements for each row is:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 4 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 1 arrangement
????.######..#####. 1,6,5 - 4 arrangements
?###???????? 3,2,1 - 10 arrangements
Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria.
What is the sum of those counts?
"""

records = [(line.strip().split()[0], [damaged for damaged in line.strip().split()[1].split(',')])
           for line in open('input/day_12.txt').readlines()]

counter = 0
for record in records:
    regex_format = '^[\\.]*?' + ''.join(['+[#]{%s}[\\.]' % a for a in record[1]])[1:] + '*?$'
    for possibility in product('.#', repeat=record[0].count('?')):
        line = record[0]
        for p in possibility:
            line = line.replace('?', p, 1)
        if re.match(regex_format, line):
            counter += 1

print("Solution for Puzzle 1: {}".format(counter))


""" *** Puzzle 2 ***

As you look out at the field of springs, you feel like there are way more springs than the condition records list. 
When you examine the records, you discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) 
and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).

So, this row:

.# 1
Would become:

.#?.#?.#?.#?.# 1,1,1,1,1
The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
In the above example, after unfolding, the number of possible arrangements for some rows is now much larger:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements
After unfolding, adding all of the possible arrangement counts together produces 525152.

Unfold your condition records; what is the new sum of possible arrangement counts?
"""

# https://github.com/morgoth1145/advent-of-code/blob/54c79b33cd38f77240d7133bc4458755cefc2ce3/2023/12/solution.py


def count_matches(pattern, splits):
    @functools.cache
    def gen(rem_pattern, rem_len, rem_splits):
        if len(rem_splits) == 0:
            if all(c in '.?' for c in rem_pattern):
                return 1
            return 0

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        count = 0

        for before in range(rem_len-after-a+1):
            cand = '.' * before + '#' * a + '.'
            if all(c0 == c1 or c0=='?'
                   for c0,c1 in zip(rem_pattern, cand)):
                rest_pattern = rem_pattern[len(cand):]
                count += gen(rest_pattern, rem_len-a-before-1, rest)

        return count

    return gen(pattern, len(pattern), tuple(splits))


records = [(line.strip().split()[0], [int(damaged) for damaged in line.strip().split()[1].split(',')])
           for line in open('input/day_12.txt').readlines()]

counter = 0
for a, b in records:
    counter += count_matches('?'.join((a, a, a, a, a)), b*5)

print("Solution for Puzzle 2: {}".format(counter))
