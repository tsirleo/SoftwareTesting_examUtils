from itertools import product

def fsm_transition(fsm, start_state, input_sequence):
    state = start_state
    output_sequence = []
    for inp in input_sequence:
        next_state, output = fsm[state][inp]
        state = next_state
        output_sequence.append(output)
    return state, output_sequence

def fsm_transition_for_covering(fsm, start_state, input_sequence):
    state = start_state
    for inp in input_sequence:
        next_state, _ = fsm[state][inp]
        state = next_state
    return state

def generate_input_sequences(inputs, max_length):
    sequences = []
    for length in range(1, max_length + 1):
        sequences.extend(product(inputs, repeat=length))
    return sequences

def distinguish_state(fsm, states, target_state, input_sequences):
    w_set = set()
    for other_state in states:
        if other_state == target_state:
            continue
        for seq in input_sequences:
            _, output_target = fsm_transition(fsm, target_state, seq)
            _, output_other = fsm_transition(fsm, other_state, seq)
            if output_target != output_other:
                w_set.add("".join(seq))
                break
    return w_set

def distinguish_states(fsm, states, input_sequences):
    distinguishable = {}
    for p in states:
        for q in states:
            if p < q:
                for seq in input_sequences:
                    _, output_p = fsm_transition(fsm, p, seq)
                    _, output_q = fsm_transition(fsm, q, seq)
                    if output_p != output_q:
                        distinguishable.setdefault((p, q), []).append("".join(seq))
                        break
    return distinguishable

def find_distinguishing_sequence(fsm, states, input_sequences):
    for seq in input_sequences:
        outputs = {}
        is_distinguishing = True
        for state in states:
            _, output_sequence = fsm_transition(fsm, state, seq)
            output_sequence = tuple(output_sequence)
            if output_sequence in outputs:
                is_distinguishing = False
                break
            outputs[output_sequence] = state
        if is_distinguishing:
            return "".join(seq)
    return None

def get_state_cover(fsm, initial_state, states, inputs):
    input_sequences = generate_input_sequences(inputs, max_length=len(states))
    state_cover = {}
    for seq in input_sequences:
        reached_state = fsm_transition_for_covering(fsm, initial_state, seq)
        if reached_state not in state_cover.values():
            state_cover["".join(seq)] = reached_state
        if len(state_cover) == len(states):
            break
    return state_cover

def get_distinguishing_sequence(fsm, states, inputs):
    input_sequences = generate_input_sequences(inputs, max_length=4)
    distinguishing_sequence = find_distinguishing_sequence(fsm, states, input_sequences)
    return distinguishing_sequence

def get_characterizing_set(fsm, states, inputs):
    input_sequences = generate_input_sequences(inputs, max_length=4)
    distinguishable = distinguish_states(fsm, states, input_sequences)
    w_set_fsm = set()
    for pair, seqs in distinguishable.items():
        w_set_fsm.update(seqs)
    return w_set_fsm

def get_identifying_sets(fsm, states, inputs):
    input_sequences = generate_input_sequences(inputs, max_length=4)
    w_sets_per_state = {}
    for state in states:
        w_set = distinguish_state(fsm, states, state, input_sequences)
        w_sets_per_state[state] = w_set
    return w_sets_per_state

def print_fsm_stats(fsm, states, inputs, initial_state):
    state_cover = get_state_cover(fsm, initial_state, states, inputs)
    covering_set = list(state_cover.keys())
    distinguishing_sequence = get_distinguishing_sequence(fsm, states, inputs)
    w_set_fsm = get_characterizing_set(fsm, states, inputs)
    w_sets_per_state = get_identifying_sets(fsm, states, inputs)
    print("1. Distinguishing sequence (d):", f"'{distinguishing_sequence}'")
    print("2. Characterizing set for the FSM (W):", w_set_fsm)
    print("3. Identifying sets for each state (Ws):")
    for state, w_set in w_sets_per_state.items():
        print(f"\t\tState {state}: {w_set}")
    print("4. Covering set (C):", covering_set)

def generate_rciw_tests(reset_symbol, covering_set, inputs, w_set):
    input_sequences = generate_input_sequences(inputs, max_length=1)
    rciw_tests = []
    for c in covering_set:
        for i in input_sequences:
            for w in w_set:
                test_sequence = reset_symbol + ".".join([c, "".join(i), w])
                rciw_tests.append(test_sequence)
    return sorted(rciw_tests, key=len)

def print_w_method_tests(fsm, states, inputs, reset_symbol, initial_state):
    state_cover = get_state_cover(fsm, initial_state, states, inputs)
    covering_set = list(state_cover.keys())
    w_set = get_characterizing_set(fsm, states, inputs)
    w_tests = generate_rciw_tests(reset_symbol, covering_set, inputs, w_set)
    print(f"5. W-method test (RCIW) [{len(w_tests)}]: {w_tests}")

def generate_rcw_tests(reset_symbol, covering_set, w_set):
    rcw_tests = set()
    for c in covering_set:
        for w in w_set:
            test_sequence = reset_symbol + ".".join([c, w])
            rcw_tests.add(test_sequence)
    return rcw_tests

def generate_rciws_tests(fsm, state_cover, inputs, reset_symbol, w_sets_per_state):
    rciws_tests = set()
    input_sequences = generate_input_sequences(inputs, max_length=1)
    for c, s in state_cover.items():
        for i in input_sequences:
            i_str = "".join(i)
            next_state, _ = fsm[s][i_str]
            for w in w_sets_per_state[next_state]:
                test_sequence = reset_symbol + ".".join([c, i_str, w])
                rciws_tests.add(test_sequence)
    return rciws_tests

def generate_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state):
    state_cover = get_state_cover(fsm, initial_state, states, inputs)
    covering_set = list(state_cover.keys())
    w_set = get_characterizing_set(fsm, states, inputs)
    w_sets_per_state = get_identifying_sets(fsm, states, inputs)
    rcw_tests = generate_rcw_tests(reset_symbol, covering_set, w_set)
    rciws_tests = generate_rciws_tests(fsm, state_cover, inputs, reset_symbol, w_sets_per_state)
    wp_tests = rcw_tests.union(rciws_tests)
    return sorted(set(wp_tests), key=len)

def print_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state):
    wp_tests = generate_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state)
    print(f"6. Wp-method test (RCW + RCIWs) [{len(wp_tests)}]: {wp_tests}")

def preprocess(s):
    if s.startswith("R.") and len(s) > 2:
        return "R" + s[2:]
    return s

def is_prefix(small, large):
    return large.startswith(small)

def remove_prefixes(strings):
    processed_strings = [preprocess(s) for s in strings]
    result = []
    for i, s in enumerate(processed_strings):
        if not any(is_prefix(s, other) for j, other in enumerate(processed_strings) if i != j):
            result.append(strings[i])
    return result

def print_minimized_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state):
    wp_tests = generate_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state)
    minimized_wp_tests = remove_prefixes(wp_tests)
    print(f"7. Minimized Wp-method test (reduced subsequences) [{len(minimized_wp_tests)}]: {minimized_wp_tests}")

if __name__ == "__main__":
    fsm = {
        0: {'A': (0, 'X'), 'B': (1, 'Y')},
        1: {'A': (2, 'Y'), 'B': (3, 'X')},
        2: {'A': (3, 'X'), 'B': (0, 'X')},
        3: {'A': (3, 'X'), 'B': (0, 'Y')},
    }
    states = list(fsm.keys())
    inputs = ['A', 'B']
    reset_symbol = 'R'
    initial_state = 0

    print_fsm_stats(fsm, states, inputs, initial_state)
    print_w_method_tests(fsm, states, inputs, reset_symbol, initial_state)
    print_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state)
    print_minimized_wp_method_tests(fsm, states, inputs, reset_symbol, initial_state)