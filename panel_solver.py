from functools import reduce
from copy import deepcopy
import math
from multiprocessing import Pool, cpu_count

# Predefined commands (remain unchanged)
COM_0 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
COM_1 = [[1, 1, 0], [1, 0, 0], [0, 0, 0]]
COM_2 = [[1, 1, 1], [0, 1, 0], [0, 0, 0]]
COM_3 = [[0, 1, 1], [0, 0, 1], [0, 0, 0]]
COM_4 = [[1, 0, 0], [1, 1, 0], [1, 0, 0]]
COM_5 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
COM_6 = [[0, 0, 1], [0, 1, 1], [0, 0, 1]]
COM_7 = [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
COM_8 = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
COM_9 = [[0, 0, 0], [0, 0, 1], [0, 1, 1]]

AVAILABLE_COMMANDS = {
    0: COM_0,
    1: COM_1,
    2: COM_2,
    3: COM_3,
    4: COM_4,
    5: COM_5,
    6: COM_6,
    7: COM_7,
    8: COM_8,
    9: COM_9,
}

TARGET = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def read_panel() -> list:
    """
    Reads initial 3x3 panel configuration from user input.

    Returns:
        list: 3x3 matrix with 0/1 elements

    Raises:
        ValueError: On invalid input
    """
    print("Enter initial panel (3 rows of 3 digits 0/1 separated by spaces):")
    panel = []
    for i in range(3):
        while True:
            row = input(f"Row {i+1}: ").strip().split()
            if len(row) != 3 or not all(c in ('0', '1') for c in row):
                print("Error: enter exactly 3 digits (0 or 1) separated by spaces")
                continue
            panel.append([int(x) for x in row])
            break
    return panel


def read_combination_length() -> int:
    """
    Gets maximum combination length from user with default value.

    Returns:
        int: Positive integer (default: 3)
    """
    while True:
        user_input = input("Maximum combination length [3]: ").strip()
        if not user_input:
            return 3
        try:
            length = int(user_input)
            if length < 1:
                print("Error: enter an integer greater than 0")
                continue
            return length
        except ValueError:
            print("Error: enter an integer greater than 0")


def apply_toggle(panel: list, command: list) -> None:
    """
    Applies command to panel using XOR operation.

    Args:
        panel (list): Current panel state
        command (list): Command to apply

    Example:
        >>> panel = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
        >>> apply_toggle(panel, COM_1)
    """
    for i in range(3):
        for j in range(3):
            panel[i][j] ^= command[i][j]


def find_solutions(*args) -> list:
    """
    Finds all valid combinations to reach target panel.

    Args:
        initial_panel (list): Initial panel state
        max_length (int): Maximum combination length

    Returns:
        list: Found valid combinations
    """

    initial_panel, start_from, end_to = args[0]
    solutions = []
    combination = start_from if start_from else 1

    print(f"\nSearching for solutions form {start_from} to {end_to} ...")
    while combination and combination <= end_to:
        current_panel = deepcopy(initial_panel)
        temp = combination

        while temp > 0:
            digit = temp % 10
            if digit in AVAILABLE_COMMANDS:
                apply_toggle(current_panel, AVAILABLE_COMMANDS[digit])
            temp //= 10

        if current_panel == TARGET:
            solutions.append(str(combination)[::-1])

        combination += 1

    return solutions


def make_chunks(end, steps):
    max_length = 10**end - 1
    start = 0

    def calc_slice(step):
        nonlocal start
        old_start = start
        start = round(max_length / steps) * (step + 1)
        return (old_start, start)

    return (calc_slice(i) for i in range(steps))


def clear_apply_toggle(panel: list, command: list) -> list:
    """
    Applies command to panel using XOR operation.

    Args:
        panel (list): Current panel state
        command (list): Command to apply

    Example:
        >>> panel = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
        >>> apply_toggle(panel, COM_1)
    """
    result = deepcopy(panel)
    for i in range(3):
        for j in range(3):
            result[i][j] ^= command[i][j]
    return result


def DP_solving(panel, end_to):
    dp = [None for _ in range(end_to + 1)]
    dp[0] = deepcopy(panel)

    solutions = []
    combination = 1
    while combination and combination <= end_to:
        tmp = combination

        testing_panel = None
        prev_combination_key = tmp // 10

        testing_panel = dp[prev_combination_key]

        new_command = tmp % 10

        testing_panel = clear_apply_toggle(testing_panel, AVAILABLE_COMMANDS[new_command])
        dp[tmp] = testing_panel

        if testing_panel == TARGET:
            solutions.append(str(combination)[::-1])

        combination += 1

    return solutions


def dp_main():
    """Main program logic"""
    panel = read_panel()
    max_len = read_combination_length()
    last_number = 10**max_len - 1
    result = DP_solving(panel, last_number)
    print(result[0:10])


def main():
    """Main program logic"""
    panel = read_panel()
    max_len = read_combination_length()
    step_size = cpu_count()
    all_combinations = make_chunks(max_len, step_size)
    with Pool(step_size) as pool:
        result = pool.map(find_solutions, ((deepcopy(panel), start, end) for start, end in all_combinations))
        result = reduce(lambda x, y: x + y, result)

    if result:
        print("\nValid combinations found:")
        for combination in result[0:10]:
            print(combination)


if __name__ == "__main__":
    # main()
    dp_main()
