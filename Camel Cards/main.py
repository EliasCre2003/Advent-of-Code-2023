from enum import Enum

class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other: 'HandType') -> bool:
        return self.value < other.value


class AbstractHand:
    def __init__(self, cards: list[str], bid: int):
        self.cards: list[str] = cards
        self.bid: int = bid

    def card_value(self, card: str) -> int: ...

    def hand_type(self) -> HandType: ...

    def __eq__(self, other: 'AbstractHand') -> bool:
        if type(self) != type(other): 
            return False 
        if self.hand_type() != other.hand_type():
            return False
        for i, card1 in enumerate(self.cards):
            card2: str = other.cards[i]
            if self.card_value(card1) != other.card_value(card2):
                return False
        return True
    
    def __lt__(self, other: 'AbstractHand') -> bool:
        if type(self) != type(other): 
            return False
        if self.hand_type() != other.hand_type():
            return self.hand_type() < other.hand_type()
        for i, card1 in enumerate(self.cards):
            card2: str = other.cards[i]
            if self.card_value(card1) != other.card_value(card2):
                return self.card_value(card1) < other.card_value(card2)
        return False
    
    def __le__(self, other: 'AbstractHand') -> bool:
        return self.__eq__(other) or self.__lt__(other)

    @classmethod
    def from_str(cls, string: str) -> 'AbstractHand':
        args = string.strip().split(" ")
        return cls(list(args[0]), int(args[1]))
    
    @staticmethod
    def _hand_type_helper(cards: list[str]) -> HandType:
        match len(card_set := set(cards)):
            case 1:
                return HandType.FIVE_OF_A_KIND
            case 2:
                if len([card for card in cards if card != cards[0]]) in (3, 2):
                    return HandType.FULL_HOUSE
                else:
                    return HandType.FOUR_OF_A_KIND
            case 3:
                most_occuring: str = max(card_set, key=cards.count)
                if sum(1 for card in cards if card == most_occuring) == 3:
                    return HandType.THREE_OF_A_KIND
                else:
                    return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case 5:
                return HandType.HIGH_CARD
            case _:
                print("Something is seriously wrong")
                return

class Part1(AbstractHand):

    def card_value(self, card: str) -> int | None:
        return {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }[card]

    def hand_type(self) -> HandType:
        return super()._hand_type_helper(self.cards)


class Part2(AbstractHand):

    def card_value(self, card: str) -> int:
        return {
            "J": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "Q": 12,
            "K": 13,
            "A": 14
        }[card]
    
    def hand_type(self) -> HandType:
        card_set: set[str] = set(cards := self.cards.copy())
        cards_without_J: list[str] = [card for card in cards if card != 'J']
        most_occuring_card: str = max(card_set, key=cards_without_J.count)
        cards = [most_occuring_card if card == 'J' else card for card in cards]
        return super()._hand_type_helper(cards)

def main():
    with open("Camel Cards/input.txt", "r") as f:
        lines = f.readlines()

    PART = Part1
    result = sum(
        hand.bid * (i+1) for i, hand in enumerate(
                sorted([PART.from_str(line) for line in lines])
            )
        )
    print(result)


if __name__ == "__main__":
    main()