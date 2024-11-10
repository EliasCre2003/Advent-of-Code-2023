from typing import Callable

class Solution:
    def __init__(self, part1: Callable[[list[str]], int], part2: Callable[[list[str]], int]):
        self.part1: Callable[[list[str]], int] = part1
        self.part2: Callable[[list[str]], int] = part2

    @staticmethod
    def _lines(input_path: str) -> list[str]:
        with open(input_path, "r") as f:
            return f.readlines()

    def solve_all(self, input_path: str) -> tuple[int, int]:
        lines = Solution._lines(input_path)
        return self.part1(lines), self.part2(lines)
    
    def solve_part1(self, input_path: str) -> int:
        return self.part1(Solution._lines(input_path))
    
    def solve_part2(self, input_path: str) -> int:
        return self.part2(Solution._lines(input_path))