# https://adventofcode.com/2023/day/1

""" *** Puzzle 1 ***

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration
value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit
and the last digit (in that order) to form a single two-digit number.

For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
"""

DIGIT_LIST = '123456789'
n_list = []

with open('input/day_01.txt') as f:
    line = f.readline()
    while line:
        digits = [c for c in line if c in DIGIT_LIST]
        n_list.append(int(digits[0] + digits[-1]))
        line = f.readline()

print("Solution for Puzzle 1: {}".format(sum(n_list)))


""" *** Puzzle 2 ***

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, 
three, four, five, six, seven, eight, and nine also count as valid "digits".
Equipped with this new information, you now need to find the real first and last digit on each line.

For example:
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""

DIGIT_WORD_MAPPING = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
}
n_list = []

with open('input/day_01.txt') as f:
    line = f.readline()
    while line:
        for digit, word in DIGIT_WORD_MAPPING.items():
            line = line.replace(digit, word)
        start_digit_findings = {digit: line.find(word) for digit, word in DIGIT_WORD_MAPPING.items()
                                if line.find(word) != -1}
        end_digit_findings = {digit: line.rfind(word) for digit, word in DIGIT_WORD_MAPPING.items()
                              if line.rfind(word) != -1}
        n_list.append(int(min(start_digit_findings, key=start_digit_findings.get) +
                      max(end_digit_findings, key=end_digit_findings.get)))
        line = f.readline()

print("Solution for Puzzle 2: {}".format(sum(n_list)))
