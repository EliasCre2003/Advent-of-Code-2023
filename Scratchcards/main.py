with open("Scratchcards/input.txt", "r") as file:
    lines: list[str] = file.readlines()


class Card:
    def __init__(self, line: str = None) -> None:
        if line ==  None: return
        line: list[str] = line[5:-1].split(": ")
        self.id: int = int(line[0])
        line: str = line[1]
        line: list[str] = line.split(" | ")
        for i in range(2):
            line[i]: list[str] = line[i].split(" ")
            while True:
                try: line[i].remove("")
                except ValueError: break
            line[i] = [int(n) for n in line[i]]
        self.winning_numbers, self.numbers = line
        self.been_processed = False
        self.matches = 0
        for num in self.numbers:
            if num in self.winning_numbers:
                self.matches += 1

    def calculate_points(self) -> int:
        if self.matches == 0: return 0
        return 1 << (self.matches - 1)
    
    def copy(self) -> "Card":
        new_card = Card()
        new_card.id = self.id
        new_card.winning_numbers = self.winning_numbers
        new_card.numbers = self.numbers
        new_card.been_processed = False
        new_card.matches = self.matches
        return new_card

def part1():
    total = 0
    for line in lines:
        total += Card(line).calculate_points()
    print(total)

def part2():
    cards = [Card(line) for line in lines]
    original_cards = [card.copy() for card in cards]
    while True:
        done = True
        for card in cards:
            if card.been_processed: continue
            matches = card.matches
            if matches == 0: continue
            done = False
            card.been_processed = True
            for i in range(matches):
                cards.append(original_cards[card.id + i].copy())
        if done:
            break
    print(len(cards))
part2()