class Conversion:
    def __init__(self, destination: int, source: int, size: int):
        self.destination: int = destination
        self.source: int = source
        self.size: int = size

    def last_source(self) -> int:
        return self.source + self.size - 1

    def __str__(self) -> str:
        return f"({self.destination}, {self.source}, {self.size})"
    
    def __repr__(self) -> str:
        return str(self)
    
    
class Result:
    def __init__(self, first: int = 0, size: int = 0):
        self.first: int = first
        self.size: int = size

    def last(self, value: int = None) -> int | None:
        if value is None:
            return self.first + self.size - 1
        self.size = value - self.first + 1

    def __str__(self) -> str:
        return f"({self.first}, {self.size})"

    def __repr__(self) -> str:
        return str(self)
    

def convert_result(result: Result, conversion: Conversion) -> tuple[Result, list[Result]] | None:
    if (result.last() < conversion.source or
        result.first > conversion.last_source()): return None
    
    converted_result: Result = Result()

    unconverted_parts: list[Result] = [None] * 2

    if result.first < conversion.source:
        converted_result.first = conversion.source
        unconverted_parts[0] = Result(
            result.first,
            conversion.source - result.first
        )
    else:
        converted_result.first = result.first

    if result.last() > conversion.last_source():
        converted_result.last(conversion.last_source())
        unconverted_parts[0] = Result(
            conversion.last_source() + 1,
            result.last() - conversion.last_source()
        )
    else:
        converted_result.last(result.last())

    converted_result.first -= conversion.source - conversion.destination

    return converted_result, unconverted_parts




def parse_maps(lines: list[str]) -> list[list[Conversion]]:
    lines: list[str] = [line for line in lines 
             if line[0] in '0123456789\n']
    map_lines: list[list[str]] = [] 
    curr_map: list[str] = []
    for line in lines:
        if line[0] != '\n':
            curr_map.append(line.strip().split(" "))
        else:
            map_lines.append(curr_map)
            curr_map = []

    return [[Conversion(*(int(arg) for arg in conversion_line)) 
         for conversion_line in conversion_lines] 
         for conversion_lines in map_lines]