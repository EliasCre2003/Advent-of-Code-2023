from math import lcm

def create_node_map(lines: list[str]) -> dict[str, tuple[str, str]]:
    """
    Returns a map with the same structure as in the input file
    """

    def parse_entry(line: str) -> tuple[str, tuple[str, str]]:
        """
        Turns a line into a map entry
        """
        key: str = line[0:3]
        left: str = line[7:10]
        right: str = line[12:15]
        return key, (left, right)
    
    return dict([parse_entry(line) for line in lines])


def next_key(node_map: dict[str, tuple[str, str]], current_key: str, lr: str) -> str:
    """
    Returns either the left or right value, coresponding to the given key in the map, given the lr argumet
    """
    return node_map[current_key][{"L": 0, "R": 1}[lr]]


def part1(lines: list[str]) -> int:
    lr_sequence: list[str] = list(lines[0].strip())
    node_map: dict[str, tuple[str, str]] = create_node_map(lines[2:])
    current_key: str = "AAA"
    num_steps: int = 0
    while current_key != "ZZZ":
        current_key = next_key(node_map, current_key, lr_sequence[num_steps % len(lr_sequence)])
        num_steps += 1
    return num_steps


def part2(lines: list[str]) -> int:
    lr_sequence: list[str] = list(lines[0].strip())
    node_map: dict[str, tuple[str, str]] = create_node_map(lines[2:])
    loop_lengths: list[int] = []
    current_keys: list[str] = [key for key in node_map.keys() if key[2] == "A"]
    num_steps: int = 0
    while len(current_keys) > 0:
        lr: str = lr_sequence[num_steps % len(lr_sequence)]
        current_keys = [next_key(node_map, key, lr) for key in current_keys]
        num_steps += 1
        for i, key in enumerate(current_keys):
            if key[2] == "Z":
                loop_lengths.append(num_steps)
                current_keys.pop(i)
    print(*(length % len(lr_sequence) for length in loop_lengths))
    return lcm(*loop_lengths)


def main():
    with open("Haunted Wasteland/input.txt", "r") as f:
        lines = f.readlines()
    print(f"Part 1: {part1(lines)}\nPart2: {part2(lines)}")


if __name__ == "__main__":
    main()