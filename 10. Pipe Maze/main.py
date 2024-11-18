from math import ceil

class Maze:

    BENDING_PIPES = {'L', 'F', '7', 'J'}
    HORIZONTAL_PIPES = BENDING_PIPES.union({'-'})
    VERTICAL_PIPES = BENDING_PIPES.union({'|'})
    PIPE_TYPES = HORIZONTAL_PIPES.union(VERTICAL_PIPES)

    def __init__(self, data: list[list[str]]):
        self.data = data

    def __str__(self) -> str:
        return '\n'.join([''.join(row) for row in self.data])
    
    def __repr__(self) -> str:
        return str(self)
    
    def starting_position(self) -> tuple[int, int]:
        for y, row in enumerate(self.data):
            if "S" in row:
                return row.index("S"), y
            
    def get_pipe_at(self, coord: tuple[int, int]) -> str:
        return self.data[coord[1]][coord[0]]
    
    # def set_pipe_at(self, coord: tuple[int, int], pipe: str) -> None:
    #     self.data[coord[1]][coord[0]] = pipe
    
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
        next_pipe: str = ""
        loop_coords: list[tuple[int, int]] = []
        while next_pipe != "S":
            next_pipe, current, previous = self.next_pipe(current, previous)
            loop_coords.append(current)
        return loop_coords
    
    def loop_inside_area(self) -> int:

        pipe_loop = self.calculate_loop()

        def replace_s() -> list[list[tuple[int, int]]]:

            data = [row.copy() for row in self.data]
            s_coord = self.starting_position()

            def determine_pipe() -> str:
                if self.get_pipe_at((s_coord[0], s_coord[1] + 1)) in Maze.VERTICAL_PIPES:
                    if self.get_pipe_at((s_coord[0], s_coord[1] - 1)) in Maze.VERTICAL_PIPES:
                        return '|'
                    elif self.get_pipe_at((s_coord[0] - 1, s_coord[1])) in Maze.VERTICAL_PIPES:
                        return '7'
                    else:
                        return 'F'
                elif self.get_pipe_at((s_coord[0], s_coord[1] - 1)) in Maze.VERTICAL_PIPES:
                    if self.get_pipe_at((s_coord[0] - 1, s_coord[1])):
                        return 'J'
                    else:
                        return 'L'
                else:
                    return '-'
                
            data[s_coord[1]][s_coord[0]] = determine_pipe()
            return data
            
        data_without_s = replace_s()
        
        
        inside_coords: set[tuple[int, int]] = set()
        for y, row in enumerate(data_without_s):
            is_inside = False
            last_turn = ''
            for x, tile in enumerate(row):
                if (x, y) in pipe_loop:
                    if (tile == '|' or
                        (last_turn + tile in ['L7', 'FJ'])):
                        is_inside = not is_inside
                    elif tile in 'FL':
                        last_turn = tile
                elif is_inside:
                    inside_coords.add((x, y))
        return len(inside_coords)
    
    @staticmethod
    def horizontal_connection_possible(pipe1: str, pipe2: str) -> bool:
        """
        Checks if a left to right connecction is possible
        """
        return pipe1 in ('-', 'F', 'L') and pipe2 in ('7', 'J', '-')
    
    @staticmethod
    def vertical_connection_possible(pipe1: str, pipe2: str) -> bool:
        """
        Checks if a downwards connection is possible
        """
        return pipe1 in ('|', '7', 'F') and pipe2 in ('|', 'L', 'J')        

    def loop_length(self) -> int:
        return len(self.calculate_loop())


def part1(maze: Maze) -> int:
    return ceil(maze.loop_length() / 2)

def part2(maze: Maze) -> int:
    return maze.loop_inside_area()

def main():
    with open("10. Pipe Maze/input.txt") as f:
        lines = f.readlines()
    maze = Maze([list(line.strip()) for line in lines])
    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(maze)}')

if __name__ == "__main__":
    main()