class SpringRow:
    def __init__(self, line: str) -> None:
        parts: list[str] = line.split(" ")
        self.conditions: list[str] = list(parts[0])
        self.groups: list[int] = [int(group) for group in parts[1].split(",")]

    def num_possible_combinations(self) -> int:
        pass

def main():
    with open("12. Hot Springs/input.txt") as f:
        lines = f.readlines()

    spring_rows: list[SpringRow] = [SpringRow(line.strip()) for line in lines]
    print(sum(spring_row.num_possible_combinations() for spring_row in spring_rows))

if __name__ == "__main__":
    main()