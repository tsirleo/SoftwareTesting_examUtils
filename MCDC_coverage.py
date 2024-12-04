import re
from typing import List
from itertools import product


class Condition:
    def __init__(self, value):
        args = re.findall(r'\w+|<=|>=|<|>|==|!=|\-?\d+(?:\.\d+)?', value)
        assert len(args) == 3

        self.name = args[0]
        self.sign = args[1]
        self.value = int(args[2])
        self.is_true = False

    def __str__(self):
        return f'{self.name} {self.sign} {self.value}'

    def __bool__(self):
        return self.is_true

    def set_true(self, is_true: bool):
        self.is_true = is_true

    def is_inverse(self, condition):
        if self.name != condition.name:
            return False

        if self.value != condition.value:
            return False

        pairs = [
            ['<', '>='],
            ['>', '<='],
            ['==', '!=']
        ]

        return [self.sign, condition.sign] in pairs or [condition.sign, self.sign] in pairs

    def __eq__(self, condition):
        if self.name != condition.name:
            return False

        if self.value != condition.value:
            return False

        pairs = [
            ['<', '<'],
            ['>', '>'],
            ['<=', '<='],
            ['>=', '>='],
            ['==', '=='],
            ['!=', '!='],
        ]

        return [self.sign, condition.sign] in pairs or [condition.sign, self.sign] in pairs

    def is_exists(self, condition):
        if self.name != condition.name or self.value != condition.value:
            return True

        if self.sign == '<' and condition.sign == '>':  # x < 1 vs x > 1
            return not (self.is_true and condition.is_true)

        if self.sign == '>' and condition.sign == '<':  # x < 1 vs x > 1
            return not (self.is_true and condition.is_true)

        return True


class Branch:
    def __init__(self, value):
        self.value = value
        self.conditions = [Condition(condition) for condition in re.split(r'\|\||&&', value)]

    def evaluate(self, filtered_conditions, is_debug=False):
        lexemes = re.findall(r'\|\||&&|(?:\w+ (?:<=|>=|<|>|==|!=) -?\d+(?:\.\d+)?)', self.value)
        expression = []

        for i, lexeme in enumerate(lexemes):
            if lexeme == '||':
                expression.append('or')
                continue

            if lexeme == '&&':
                expression.append('and')
                continue

            condition = Condition(lexeme)
            index = 0

            while index < len(filtered_conditions) and not (condition == filtered_conditions[index]) and not condition.is_inverse(filtered_conditions[index]):
                index += 1

            assert index < len(filtered_conditions)

            if condition.is_inverse(filtered_conditions[index]):
                expression.append(str(not filtered_conditions[index].is_true))
            else:
                expression.append(str(filtered_conditions[index].is_true))

        expression = ' '.join(expression)
        result = eval(expression)

        if is_debug:
            print(' '.join(lexemes), '=', expression, '=', result)

        return result

    def __contains__(self, item):
        for condition in self.conditions:
            if condition.is_inverse(item) or condition == item:
                return True

        return False

    def __str__(self):
        return self.value


def filter_conditions(conditions: List[Condition]):
    filtered = []

    for condition in conditions:
        index = 0

        while index < len(filtered) and not (filtered[index].is_inverse(condition) or filtered[index] == condition):
            index += 1

        if index == len(filtered):
            filtered.append(condition)

    return filtered


def is_exists(conditions):
    for i, condition in enumerate(conditions):
        for j in range(i + 1, len(conditions)):
            if not condition.is_exists(conditions[j]):
                return False

    return True


def make_table(conditions, branches):
    print('Table of conditions and branches:\n\t', '|     № |' + ''.join(['%6s |' % condition for condition in conditions]) + ''.join('%6s |' % ['I', 'II', 'III', 'IV'][i] for i in range(len(branches))))
    n = len(conditions)
    pos = 0

    total_values = []
    total_branch_values = []

    for i in range(1 << n):
        values = [(i >> j) & 1 for j in range(n)]

        for j in range(n):
            conditions[j].set_true(values[j] == 1)

        if not is_exists(conditions):
            continue

        branch_values = [1 if branch.evaluate(conditions) else 0 for branch in branches]
        total_values.append(values)
        total_branch_values.append(branch_values)
        pos += 1

        print('\t', ('| %5d |' % pos) + ''.join(['%6s |' % value for value in values + branch_values]))
    print('\n')

    return total_values, total_branch_values

def find_pairs_for_condition(values, branch_values, branch_index, index, indexes):
    pairs = []

    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            vi = [values[i][ind] for ind in indexes]
            vj = [values[j][ind] for ind in indexes]
            pos = indexes.index(index)

            if vi[pos] == vj[pos] or branch_values[i][branch_index] == branch_values[j][branch_index]:
                continue

            vi[pos] = -1
            vj[pos] = -1

            if vi == vj:
                pairs.append((i, j))

    return pairs


def print_table(columns, column_names):
    print('\t', '|     № |' + ''.join(['%6s |' % name for name in column_names]))

    for i in range(len(columns[0])):
        print('\t', ('| %5d |' % (i + 1)) + ''.join(['%6s |' % columns[j][i] for j in range(len(columns))]))


def transpose(v):
    n, m = len(v), len(v[0])
    vv = [[0 for j in range(n)] for i in range(m)]

    for i in range(n):
        for j in range(m):
            vv[j][i] = v[i][j]

    return vv


def find_pairs(conditions, branches, values, branch_values):
    m = len(values)
    branches_pairs = []

    for index, branch in enumerate(branches):
        branch_conditions = [condition for condition in conditions if condition in branch]
        indexes = [conditions.index(condition) for condition in branch_conditions]
        branch_pairs = []
        branch_test_pairs = []

        print(['I', 'II', 'III'][index] + ':', indexes)
        for i in indexes:
            pairs = find_pairs_for_condition(values, branch_values, index, i, indexes)

            if not pairs:
                pairs = [[-1, -1]]

            i1, i2 = pairs[0]
            pair = ['*' if j == i1 or j == i2 else ' ' for j in range(m)]
            branch_pairs.append(pair)
            branch_test_pairs.append(pairs)
            print(str(conditions[i]) + ':', [[i1 + 1, i2 + 1] for i1, i2 in pairs])

        branches_pairs.append(branch_test_pairs)
        print_table(transpose(values) + [transpose(branch_values)[index]] + branch_pairs, [str(c) for c in conditions] + [['I', 'II', 'III'][index]] + [str(c) for c in branch_conditions])
        print('\n')

    pairs1, pairs2 = branches_pairs

    min_sum = m
    min_pairs = []

    for pair1 in product(*pairs1):
        for pair2 in product(*pairs2):
            v = [0 for _ in range(m)]

            for p in pair1:
                if p[0] > -1:
                    v[p[0]] = 1

                if p[1] > -1:
                    v[p[1]] = 1

            for p in pair2:
                if p[0] > -1:
                    v[p[0]] = 1

                if p[1] > -1:
                    v[p[1]] = 1

            if sum(v) < min_sum:
                min_sum = sum(v)
                min_pairs = pair1 + pair2

    v = [' ' for _ in range(m)]

    for p in min_pairs:
        if p[0] > -1:
            v[p[0]] = '*'

        if p[1] > -1:
            v[p[1]] = '*'

    print('Final table with chosen conditions for MC/DC coverage:')
    print_table(transpose(values) + transpose(branch_values) + [v], [str(c) for c in conditions] + ['I', 'II', 'MC/DC'])

def build_mcdc(branches):
    print('Branches:\n\t' + '\n\t'.join([str(b) for b in branches]))

    conditions = branches[0].conditions + branches[1].conditions
    conditions.sort(key=lambda x: (len(str(x)), str(x)))
    print('\nParsed:', [str(c) for c in conditions])

    conditions = filter_conditions(conditions)

    print('Filtered:', [str(c) for c in conditions], '\n')

    values, branch_values = make_table(conditions, branches)
    find_pairs(conditions, branches, values, branch_values)

if __name__ == '__main__':
    branches = [
        Branch('z > 2 || x < 1 && y < 4'),
        Branch('x > 1 && z <= 2 || x >= 1 && y >= 4')
    ]

    build_mcdc(branches)


