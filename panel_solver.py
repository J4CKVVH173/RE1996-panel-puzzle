from functools import reduce
from copy import deepcopy
from multiprocessing import Pool, cpu_count
import argparse

# Predefined commands and target configuration
COMMAND_MAP = {
    0: [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    1: [[1, 1, 0], [1, 0, 0], [0, 0, 0]],
    2: [[1, 1, 1], [0, 1, 0], [0, 0, 0]],
    3: [[0, 1, 1], [0, 0, 1], [0, 0, 0]],
    4: [[1, 0, 0], [1, 1, 0], [1, 0, 0]],
    5: [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    6: [[0, 0, 1], [0, 1, 1], [0, 0, 1]],
    7: [[0, 0, 0], [1, 0, 0], [1, 1, 0]],
    8: [[0, 0, 0], [0, 1, 0], [1, 1, 1]],
    9: [[0, 0, 0], [0, 0, 1], [0, 1, 1]],
}

TARGET_PANEL = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def get_user_input():
    """Collect and return user input for panel configuration and max length."""
    panel = read_panel()
    max_len = read_combination_length()
    return panel, max_len


def read_panel() -> list:
    """Read 3x3 panel configuration from user input."""
    print('Enter initial panel (3 rows of 3 digits 0/1 separated by spaces):')
    panel = []
    for i in range(3):
        while True:
            row = input(f'Row {i+1}: ').strip().split()
            if len(row) != 3 or not all(c in ('0', '1') for c in row):
                print('Error: enter exactly 3 digits (0 or 1) separated by spaces')
                continue
            panel.append([int(x) for x in row])
            break
    return panel


def read_combination_length() -> int:
    """Get maximum combination length from user."""
    while True:
        user_input = input('Maximum combination length [3]: ').strip()
        if not user_input:
            return 3
        try:
            length = int(user_input)
            if length < 1:
                print('Error: enter an integer greater than 0')
                continue
            return length
        except ValueError:
            print('Error: enter an integer greater than 0')


def apply_command(panel: list, command: list) -> list:
    """Apply command to panel using XOR operation and return new state."""
    return [
        [panel[i][j] ^ command[i][j] for j in range(3)]
        for i in range(3)
    ]


def process_combination(args):
    """Process combination range for multiprocessing."""
    initial_panel, start, end = args
    solutions = []
    current = start if start else 1

    while current <= end:
        temp = current
        current_state = deepcopy(initial_panel)

        while temp > 0:
            digit = temp % 10
            current_state = apply_command(current_state, COMMAND_MAP.get(digit, COMMAND_MAP[0]))
            temp //= 10

        if current_state == TARGET_PANEL:
            solutions.append(str(current)[::-1])
        current += 1

    return solutions


def generate_chunks(max_length, chunks_count):
    """Generate ranges for parallel processing."""
    max_value = 10**max_length - 1
    chunk_size = max_value // chunks_count
    return [(i*chunk_size + 1, (i+1)*chunk_size) for i in range(chunks_count)]


def dynamic_programming_solver(initial_panel, max_length):
    """Solve using dynamic programming approach."""
    max_combination = 10**max_length - 1
    dp = {0: deepcopy(initial_panel)}
    solutions = []

    for combination in range(1, max_combination + 1):
        prev_key = combination // 10
        command = combination % 10

        if prev_key not in dp:
            continue

        new_state = apply_command(dp[prev_key], COMMAND_MAP.get(command, COMMAND_MAP[0]))
        dp[combination] = new_state

        if new_state == TARGET_PANEL:
            solutions.append(str(combination)[::-1])

    return solutions


def run_multiprocessing_handler():
    """Run solution using multiprocessing."""
    panel, max_len = get_user_input()
    chunks = generate_chunks(max_len, cpu_count())

    with Pool(cpu_count()) as pool:
        results = pool.map(process_combination, [(deepcopy(panel), s, e) for s, e in chunks])
        solutions = reduce(lambda x, y: x + y, results)

    print_results(solutions)


def run_dp_handler():
    """Run solution using dynamic programming."""
    panel, max_len = get_user_input()
    solutions = dynamic_programming_solver(panel, max_len)
    print_results(solutions)


def print_results(solutions):
    """Display found solutions."""
    if not solutions:
        print('\nNo valid combinations found')
        return

    print('\nFirst 10 valid combinations:')
    for solution in solutions[:10]:
        print(solution)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--handler',
                        choices=['dp', 'multiprocessing'],
                        default='multiprocessing',
                        help='Processing handler type (dp/multiprocessing)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.handler == 'dp':
        run_dp_handler()
    else:
        run_multiprocessing_handler()
