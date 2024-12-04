import itertools


def generate_pairs(factors):
    """
    Generate all possible pairs of results for each combination of two factors.
    """
    pairs = []
    num_factors = len(factors)
    for i in range(num_factors):
        for j in range(i + 1, num_factors):
            for value_i in factors[i]:
                for value_j in factors[j]:
                    pairs.append(((i, value_i), (j, value_j)))
    return pairs


def find_best_test(factors, uncovered_pairs):
    """
    Find a test that covers the maximum number of uncovered pairs.
    """
    best_test = None
    best_coverage = 0
    covered_by_test = set()

    for potential_test in itertools.product(*factors):
        current_coverage = set()
        for (i, value_i), (j, value_j) in uncovered_pairs:
            if potential_test[i] == value_i and potential_test[j] == value_j:
                current_coverage.add(((i, value_i), (j, value_j)))

        if len(current_coverage) > best_coverage:
            best_test = potential_test
            best_coverage = len(current_coverage)
            covered_by_test = current_coverage

    return best_test, covered_by_test


def build_coverage_array(factors):
    """
    Construction of a minimal set of tests to cover all pairs.
    """
    uncovered_pairs = set(generate_pairs(factors))
    test_set = []

    while uncovered_pairs:
        best_test, covered_by_test = find_best_test(factors, uncovered_pairs)
        test_set.append(best_test)
        uncovered_pairs -= covered_by_test

    return test_set


def print_coverage_array(factors):
    covering_arrays = build_coverage_array(factors)

    print(f"CAN = {len(covering_arrays)}\nGenerated set of tests in CA:")
    for i, test in enumerate(covering_arrays, 1):
        print(f"\tTest {i}: {test}")


if __name__ == "__main__":
    factors = [
        ['1 страница', '2 страницы', '7 страниц'],
        ['Нет цветных рисунков', 'Есть цветные рисунки'],
        ['A4', 'A5', 'B5', 'Letter', 'Envelop'],
        ['HP', 'Epson', 'Canon', 'Xerox'],
        ['Internet Explorer', 'Mozilla Firefox', 'Opera'],
        ['Windows Me', 'Windows 2000', 'Windows XP', 'Linux SUSE 10.0', 'Linux RHEL 4.0']
    ]

    print_coverage_array(factors)
