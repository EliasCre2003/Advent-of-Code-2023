bag_content = {"red": 12, "green": 13, "blue": 14}

lines: list[str] = []

with open("2. Cube Conundrum/input.txt") as f:
    lines = f.readlines()
    
class Game:
    def __init__(self, line: str):
        line = line.split("\n")[0]
        temp_line = line.split(": ")
        temp_line[0] = temp_line[0].split(" ")
        self.id: int = int(temp_line[0][1])
        temp_line = temp_line[1].split("; ")
        self.rounds: list[dict[str, int]] = []
        for round in temp_line:
            round = round.split(", ")
            color_dict = {"red": 0, "green": 0, "blue": 0}
            for color in round:
                color = color.split(" ")
                color_dict[color[1]] = int(color[0])
            self.rounds.append(color_dict)

games: list[Game] = []
for line in lines:
    games.append(Game(line))

def part1():
    total = 0
    for game in games:
        game_max = {"red": 0, "green": 0, "blue": 0}
        keys = game_max.keys()
        for round in game.rounds:
            for key in keys:
                if round[key] > game_max[key]:
                    game_max[key] = round[key]
        possible = True
        for key in keys:
            if game_max[key] > bag_content[key]:
                possible = False
                break
        if possible:
            total += game.id
    print(total)

def part2():
    total = 0
    for game in games:
        game_minimum = {"red": 0, "green": 0, "blue": 0}
        keys = game_minimum.keys()
        for round in game.rounds:
            for key in keys:
                if round[key] > game_minimum[key]:
                    game_minimum[key] = round[key]
        power = 1
        for key in keys:
            power *= game_minimum[key]
        total += power
    print(total)
part2()
