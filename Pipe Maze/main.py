from math import ceil

class Ground:

    BENDING_PIPES = {'L', 'F', '7', 'J'}
    HORIZONTAL_PIPES = BENDING_PIPES.union({'-'})
    VERTICAL_PIPES = BENDING_PIPES.union({'|'})
    PIPE_TYPES = HORIZONTAL_PIPES.union(VERTICAL_PIPES)
    


    def __init__(self, data: list[list[str]]):
        self.data = data
    
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

        loop = self.calculate_loop()

        def replace_s() -> list[list[tuple[int, int]]]:

            data = [row.copy() for row in self.data]
            s_coord = self.starting_position()

            def determine_pipe() -> str:
                if self.get_pipe_at((s_coord[0], s_coord[1] + 1)) in Ground.VERTICAL_PIPES:
                    if self.get_pipe_at((s_coord[0], s_coord[1] - 1)) in Ground.VERTICAL_PIPES:
                        return '|'
                    # elif self.get_pipe_at(s_coord[0] - 1, s_coord[1]) and self.get_pipe_at(s_coord[0] + 1, s_coord[1]) in Ground.VERTICAL_PIPES:
                    #     return '-'
                    elif self.get_pipe_at((s_coord[0] - 1, s_coord[1])) in Ground.VERTICAL_PIPES:
                        return '7'
                    else:
                        return 'F'
                elif self.get_pipe_at((s_coord[0], s_coord[1] - 1)) in Ground.VERTICAL_PIPES:
                    if self.get_pipe_at((s_coord[0] - 1, s_coord[1])):
                        return 'J'
                    else:
                        return 'L'
                else:
                    return '-'
                
            data[s_coord[1]][s_coord[0]] = determine_pipe()
            return data
            
        data_without_s = replace_s()
        
        v_inside_coords: set[tuple[int, int]] = set()
        for y, row in enumerate(data_without_s):
            intersections: list[int] = []
            for x, pipe in enumerate(row):
                last_tile: str = '' if x == 0 else row[x-1]
                if (x, y) in loop:
                    if (pipe == '|' or 
                        (pipe in ('7', 'J') and Ground.horizontal_connection_possible(last_tile, pipe)) or 
                        (pipe in ('L', 'F')) and len(intersections) == 1):
                        intersections.append(x)
                if len(intersections) < 2:
                    continue
                for i in range(intersections[0]+1, intersections[1]):
                    v_inside_coords.add((i, y))
                    data_without_s[y][i] = 'I'
                intersections.clear()

        h_inside_coords: set[tuple[int, int]] = set()
        for x in range(len(data_without_s[0])):
            intersections: list[int] = []
            for y in range(len(data_without_s)):
                last_tile: str = '' if y == 0 else data_without_s[y-1][x]
                pipe = data_without_s[y][x]
                if (x, y) in loop:
                    if (pipe == '-' or 
                        (pipe in ('L', 'F') and Ground.vertical_connection_possible(last_tile, pipe)) or
                        (pipe in ('7', 'J') and len(intersections) == 1)):
                        intersections.append(y)
                if len(intersections) < 2:
                    continue
                for i in range(intersections[0]+1, intersections[1]):
                    h_inside_coords.add((x, i))
                intersections.clear()

        for row in data_without_s:
            print(row)
        return len(v_inside_coords.intersection(h_inside_coords))
    
    @staticmethod
    def horizontal_connection_possible(pipe1: str, pipe2: str) -> bool:
        """
        Checks if a left to right connecction is possible
        """
        # if Ground.HORIZONTAL_PIPES.union({pipe1, pipe2}) != Ground.HORIZONTAL_PIPES:
        #     return False
        # if pipe1 in ('-', 'F', 'L'):
        #     return pipe2 in ('7', 'J', '-')
        # if pipe2 in ('-', '7', 'J'):
        #     return pipe1 in ('F', 'L', '-')
        # return False
        return pipe1 in ('-', 'F', 'L') and pipe2 in ('7', 'J', '-')
    
    @staticmethod
    def vertical_connection_possible(pipe1: str, pipe2: str) -> bool:
        """
        Checks if a downwards connection is possible
        """
        return pipe1 in ('|', '7', 'F') and pipe2 in ('|', 'L', 'J')

        
        
        

    def loop_length(self) -> int:
        return len(self.calculate_loop())


def part1(lines: list[str]) -> int:
    ground = Ground([list(line.strip()) for line in lines])
    return ceil(ground.loop_length() / 2)

def part2(lines: list[str]) -> int:
    ground = Ground([list(line.strip()) for line in lines])
    return ground.loop_inside_area()

def main():
    with open("Pipe Maze/test.txt") as f:
        lines = f.readlines()

    print(part2(lines))

if __name__ == "__main__":
    main()