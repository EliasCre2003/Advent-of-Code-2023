from math import ceil

class Ground:

    PIPE_TYPES = {'-', '|', 'L', 'J', 'F', '7', 'S'}
    HORIZONTAL_PIPES = {'-', 'L', 'F', '7'}
    VERTICAL_PIPES = {'|', 'L', 'F', '7', 'J'}


    def __init__(self, data: list[list[str]]):
        self.data = data
    
    def starting_position(self) -> tuple[int, int]:
        for y, row in enumerate(self.data):
            if "S" in row:
                return row.index("S"), y
            
    def get_pipe_at(self, coord: tuple[int, int]) -> str:
        return self.data[coord[1]][coord[0]]
    
    def next_pipe(self, current_coord: tuple[int, int], previous_coord: tuple[int, int]) -> tuple[str, tuple[int, int], tuple[int, int]]:
        current_pipe = self.get_pipe_at(current_coord)
        direction_list = {
            '-': [(1, 0), (-1, 0)],
            '|': [(0, 1), (0, -1)],
            'L': [(0, -1), (1, 0)],
            'J': [(0, -1), (-1, 0)],
            'F': [(0, 1), (1, 0)],
            '7': [(0, 1), (-1, 0)],
            'S': [(1, 0), (-1, 0), (0, 1), (0, -1)]
        }[current_pipe]
        if (not_allowed_direction := (previous_coord[0] - current_coord[0], 
                                      previous_coord[1] - current_coord[1])) in direction_list:
            direction_list.remove(not_allowed_direction)
        
        for direction in direction_list:
            next_coord = (current_coord[0] + direction[0], current_coord[1] + direction[1])
            next_pipe = self.get_pipe_at(next_coord)
            return_value = next_pipe, next_coord, current_coord
            if current_pipe != "S":
                return return_value
            match direction:
                case (0, 1):
                    if next_pipe in ['|', 'L', 'J']: return return_value
                case (0, -1):
                    if next_pipe in ['|', '7', 'F']: return return_value
                case (-1, 0):
                    if next_pipe in ['-', 'L', 'F']: return return_value
                case (1, 0):
                    if next_pipe in ['-', 'J', '7']: return return_value


    def calculate_loop(self) -> list[tuple[int, int]]:
        current = previous = self.starting_position()
        next_pipe: str
        length: int = 0
        loop_coords: list[tuple[int, int]] = []
        while next_pipe != "S":
            next_pipe, current, previous = self.next_pipe(current, previous)
            loop_coords.append(current)
            length += 1
        return length
    
    def loop_inside_area(self) -> int:

        def replace_s() -> list[list[tuple[int, int]]]:
            data = [row.copy() for row in self.data]
            s_coord = self.starting_position()
            if self.get_pipe_at(s_coord[0], s_coord[1] + 1) in Ground.VERTICAL_PIPES:
                ...

        loop = self.calculate_loop()
        area: int = 0
        data_without_s = replace_s(self.data)
        for y, row in enumerate(data_without_s):
            inside: bool = False
            last_pipe: str
            for x, pipe in enumerate(row):
                if (x, y) in loop:
                    if not (last_pipe in Ground.HORIZONTAL_PIPES and pipe in Ground.HORIZONTAL_PIPES):
                        inside = not inside
                    last_pipe = pipe
                else:
                    area += inside
    
    def loop_length(self) -> int:
        return len(self.calculate_loop())


def main():
    with open("Pipe Maze/input.txt") as f:
        lines = f.readlines()

    ground = Ground([list(line) for line in lines])
    print(ceil(ground.loop_length() / 2))

if __name__ == "__main__":
    main()