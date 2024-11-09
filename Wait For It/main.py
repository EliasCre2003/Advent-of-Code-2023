from math import floor, ceil, sqrt, prod


class Race:
    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance = distance

    def num_ways_to_win(self) -> int:
        lower_bound: int = ceil((self.time - sqrt(self.time**2 - 4 * self.distance)) / 2)
        upper_bound: int = floor((self.time + sqrt(self.time**2 - 4 * self.distance)) / 2)
        return upper_bound - lower_bound + 1


def part1(lines: list[str]) -> int:

    def extract_data(line: str) -> list[int]:
        line = line.strip().split(" ")
        result: list[int] = []
        for part in line:
            try: result.append(int(part))
            except: pass
        return result

    times: list[int] = extract_data(lines[0])
    distances: list[int] = extract_data(lines[1])
    races: list[Race] =  [Race(time, distance) for time, distance in zip(times, distances)]

    return prod(race.num_ways_to_win() for race in races)

def part2(lines: list[str]) -> int:

    def extract_data(line: str) -> int:
        line = line.strip().split(" ")[1:]
        return int("".join([part for part in line if line != ""]))
    
    return Race(extract_data(lines[0]), extract_data(lines[1])).num_ways_to_win()


def main():
    with open("Wait For It/input.txt", "r") as f:
        lines = f.readlines()

    print(part2(lines))

if __name__ == "__main__":
    main()