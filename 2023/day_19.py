# https://adventofcode.com/2023/day/19

""" *** Puzzle 1 ***

As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a
formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has
a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is
true. The first rule that matches the part being considered is applied immediately, and the part moves on to the
destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex
were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns.
If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a
few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to
sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for
the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all
of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all
of the parts that ultimately get accepted?
"""

workflows = [line.strip()[0:-1].split('{') for line in open('input/day_19.txt').read().split('\n\n')[0].split('\n')]
workflows = {workflow[0]: {rule.split(':')[0] if rule.count(':') > 0 else 'last':
                           rule.split(':')[1] if rule.count(':') > 0 else rule
                           for rule in workflow[1].split(',')}
             for workflow in workflows}
parts = [line.strip()[1:-1].split(',') for line in open('input/day_19.txt').read().split('\n\n')[1].split('\n')]
parts = [{attribute.split('=')[0]: int(attribute.split('=')[1]) for attribute in part} for part in parts]

result = 0
for part in parts:
    cur_workflow = 'in'
    while cur_workflow is not None:
        for key, value in workflows[cur_workflow].items():
            passed = False
            if key == 'last':
                passed = True
            else:
                attribute = key.split('<')[0] if key.count('<') > 0 else key.split('>')[0]
                number = int(key.split('>')[1] if key.count('>') > 0 else key.split('<')[1])
                if key.count('<') > 0:
                    if part[attribute] < number:
                        passed = True
                elif part[attribute] > number:
                    passed = True
            if passed:
                if value == 'A':
                    cur_workflow = None
                    result += sum([value for value in part.values()])
                    break
                elif value == 'R':
                    cur_workflow = None
                    break
                else:
                    cur_workflow = value
                    break

print("Solution for Puzzle 1: {}".format(result))


""" *** Puzzle 2 ***

Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you
can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all
possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. 
How many distinct combinations of ratings will be accepted by the Elves' workflows?
"""

workflows = [line.strip()[0:-1].split('{') for line in open('input/day_19.txt').read().split('\n\n')[0].split('\n')]
workflows = {workflow[0]: {rule.split(':')[0] if rule.count(':') > 0 else 'last':
                           rule.split(':')[1] if rule.count(':') > 0 else rule
                           for rule in workflow[1].split(',')}
             for workflow in workflows}

result = 0
working_list = [['in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}]]
while working_list:
    item = working_list.pop()
    cur_workflow = item[0]
    cur_params = item[1]

    while cur_workflow is not None:
        for key, value in workflows[cur_workflow].items():
            passed = False
            if key == 'last':
                passed = True
            else:
                attribute = key.split('<')[0] if key.count('<') > 0 else key.split('>')[0]
                number = int(key.split('>')[1] if key.count('>') > 0 else key.split('<')[1])
                if key.count('<') > 0:
                    if cur_params[attribute][1] < number:
                        passed = True
                    elif cur_params[attribute][0] < number <= cur_params[attribute][1]:
                        x = cur_params.copy()
                        x[attribute] = (number, x[attribute][1])
                        working_list.append([cur_workflow, x])
                        cur_params[attribute] = (cur_params[attribute][0], number - 1)
                        passed = True
                else:
                    if cur_params[attribute][0] > number:
                        passed = True
                    elif cur_params[attribute][0] <= number < cur_params[attribute][1]:
                        x = cur_params.copy()
                        x[attribute] = (x[attribute][0], number)
                        working_list.append([cur_workflow, x])
                        cur_params[attribute] = (number + 1, cur_params[attribute][1])
                        passed = True
            if passed:
                if value == 'A':
                    cur_workflow = None
                    mul = 1
                    for param in cur_params.values():
                        mul *= param[1] - param[0] + 1
                    result += mul
                    break
                elif value == 'R':
                    cur_workflow = None
                    break
                else:
                    cur_workflow = value
                    break

print("Solution for Puzzle 2: {}".format(result))
