import itertools
import random


def generate_mixed_covering_array(params_values):
    """
    Generates a minimized mixed covering array of strength 2 for the given parameters and their possible values.
    :param params_values: A list where each element is the number of values for each parameter.
    :return: A 2D list representing the covering array.
    """
    num_params = len(params_values)
    param_pairs = list(itertools.combinations(range(num_params), 2))
    all_pairs = set(
        (i, j, v_i, v_j)
        for i, j in param_pairs
        for v_i in range(params_values[i])
        for v_j in range(params_values[j])
    )

    covering_array = []

    while all_pairs:
        current_row = [-1] * num_params
        pairs_covered = set()

        for pair in sorted(all_pairs, key=lambda x: random.random()):
            i, j, v_i, v_j = pair
            if (current_row[i] in {-1, v_i}) and (current_row[j] in {-1, v_j}):
                current_row[i] = v_i
                current_row[j] = v_j
                pairs_covered.add(pair)

        for idx in range(num_params):
            if current_row[idx] == -1:
                current_row[idx] = random.randint(0, params_values[idx] - 1)

        covering_array.append(current_row)
        all_pairs -= pairs_covered

    return covering_array


def print_coverage_array(params_values):
    covering_arrays = generate_mixed_covering_array(params_values)

    print(f"CAN = {len(covering_arrays)}\nGenerated set of tests in CA:")

    for i, test in enumerate(covering_arrays, 1):
        print(f"\tTest {i}: {test}")


if __name__ == "__main__":
    params_values = [4, 2, 2, 2, 2, 2, 2, 2]

    print_coverage_array(params_values)
