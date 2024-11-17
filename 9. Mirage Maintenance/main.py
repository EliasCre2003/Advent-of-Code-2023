from typing import Callable

def differences(values: list[int]) -> list[int]:
    return [values[i+1] - values[i] for i in range(len(values) - 1)]

def predict_next(values: list[int]) -> int:
    diff = differences(values)
    if is_all_zeros(diff):
        return values[-1]
    return values[-1] + predict_next(diff)

def predict_previous(values: list[int]) -> int:
    diff = differences(values)
    if is_all_zeros(diff):
        return values[0]
    return values[0] - predict_previous(diff)

def is_all_zeros(lst: list[int]) -> bool:
    return lst == [0] * len(lst)

def apply_predictions(histories: list[list[int]], prediction_function: Callable[[list[int]], int]) -> list[int]:
    return [prediction_function(history) for history in histories] if callable(prediction_function) else None

def parse_histories(lines: list[str]) -> list[int]:
    return [[int(value) for value in line.strip().split(" ")] for line in lines]

def main():
    with open("9. Mirage Maintenance/input.txt", "r") as f:
        lines = f.readlines()
    histories = parse_histories(lines)
    for i, prediction_function in enumerate([predict_next, predict_previous]):
        print(f'Part {i+1}: {sum(apply_predictions(histories, prediction_function))}')

if __name__ == "__main__":
    main()