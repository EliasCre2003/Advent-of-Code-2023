from collections.abc import Callable



def differences(values: list[int]) -> list[int]:
    '''
    Returns a list of length n-1 with all of the difference 
    between each succesive int in the input list of size n
    '''
    return [values[i+1] - values[i] for i in range(len(values) - 1)]

def predict_next(sequence: list[int]) -> int:
    '''
    Returns a prediction for the next value in the input in sequence
    '''
    diff = differences(sequence)
    if is_all_zeros(diff):
        return sequence[-1]
    return sequence[-1] + predict_next(diff)

def predict_previous(sequence: list[int]) -> int:
    '''
    Returns a prediction for the value that came 
    before the first value in the input sequence
    '''
    diff = differences(sequence)
    if is_all_zeros(diff):
        return sequence[0]
    return sequence[0] - predict_previous(diff)

def is_all_zeros(lst: list[int]) -> bool:
    '''
    Returns true if the input list is just filled with 0
    '''
    return lst == [0] * len(lst)

def apply_predictions(sequences: list[list[int]], prediction_function: Callable[[list[int]], int]) -> list[int] | None:
    '''
    Applies a prediction function to a list of sequences and returns a list of 
    all of the results. Return None if prediction function is not callable
    '''
    return [prediction_function(history) for history in sequences] if callable(prediction_function) else None

def parse_sequences(lines: list[str]) -> list[int]:
    '''
    Parses a sequence for each line in in input list of lines and returns a list of all parses
    '''
    return [[int(value) for value in line.strip().split(" ")] for line in lines]

def main():
    with open("9. Mirage Maintenance/input.txt", "r") as f:
        lines = f.readlines()
    sequences = parse_sequences(lines)
    for i, prediction_function in enumerate([predict_next, predict_previous]):
        print(f'Part {i+1}: {sum(apply_predictions(sequences, prediction_function))}')

if __name__ == "__main__":
    main()