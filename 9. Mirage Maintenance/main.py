class History:
    def __init__(self, values: list[int]):
        self.values: list[int] = values

    @staticmethod
    def differences(values: list[int]) -> list[int]:
        return [values[i+1] - values[i] for i in range(len(values) - 1)]

    @staticmethod 
    def _next(values: list[int]) -> int:
        differences = History.differences(values)
        if is_all_zeros(differences):
            return values[-1]
        return values[-1] + History._next(differences) 
    
    @staticmethod
    def _previous(values: list[int]) -> int:
        differences = History.differences(values)
        if is_all_zeros(differences):
            return values[0]
        return values[0] - History._previous(differences)

    def predict_next(self) -> int:
        return History._next(self.values)
    
    def predict_previous(self) -> int:
        return History._previous(self.values)


def is_all_zeros(lst: list[int]) -> bool:
    return lst == [0] * len(lst)

def part1(lines: list[str]) -> int:
    histories = [History([int(value) for value in line.strip().split(" ")]) for line in lines]
    return sum(history.predict_next() for history in histories)

def part2(lines: list[str]) -> int:
    histories = [History([int(value) for value in line.strip().split(" ")]) for line in lines]
    return sum(history.predict_previous() for history in histories)

def main():
    with open("9. Mirage Maintenance/input.txt", "r") as f:
        lines = f.readlines()
    print(part2(lines))
    
if __name__ == "__main__":
    main()