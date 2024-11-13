from itertools import product

PROGRESS = 1

class SpringRow:
    def __init__(self, line: str, multiplier: int = 1) -> None:
        parts: list[str] = line.split(" ")
        self.conditions: list[str] = list(parts[0]) * multiplier
        self.group_sizes: list[int] = [int(group) for group in parts[1].split(",")] * multiplier

    def possible_combinations(self) -> list[list[str]]:
        num_unknown: int = sum(1 for condition in self.conditions if condition == '?')
    
        def integrate_combination(combination: list[str]) -> list[str]:
            combination = iter(combination)
            return [next(combination) if condition == '?' else condition 
                    for condition in self.conditions]
        
        return [integrate_combination(combination) for combination in 
                [list(springs) for springs in product('.#', repeat=num_unknown)]]



    def num_allowed_combinations(self) -> int:
        
        
        combinations = self.possible_combinations()

        def is_combination_allowed(combination: list[str]):
            global PROGRESS
            if '?' in combination:
                print("Combination contains '?'. FUCK!")
                exit()
            groups: list[list[str]] = [group for group in list(''.join(combination).split('.')) if group != '']
            if len(groups) != len(self.group_sizes):
                return False
            print(PROGRESS)
            PROGRESS += 1
            return sum(len(group) != group_size for group, group_size in zip(groups, self.group_sizes)) == 0

        

        return len([combination for combination in combinations 
                    if is_combination_allowed(combination)])





def main():
    with open("12. Hot Springs/input.txt") as f:
        lines = f.readlines()

    spring_rows: list[SpringRow] = [SpringRow(line.strip(), 1) for line in lines]
    print(sum(spring_row.num_allowed_combinations() for spring_row in spring_rows))

if __name__ == "__main__":
    main()
    # print([None, None] * 2)
    # print([list(springs) for springs in product('.#', repeat=5)])