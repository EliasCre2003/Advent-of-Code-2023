class Result:
    def __init__(self, start: int = 0, end: int = 0, conversion: int = 0):
        self.start: int = start + conversion
        self.end: int = end + conversion

    def __str__(self) -> str:
        return f"({self.start}, {self.end})"

    def __repr__(self) -> str:
        return str(self)
    

class Conversion:
    def __init__(self, destination_start: int, source_start: int, size: int):
        self.ds: int = destination_start
        self.de: int = destination_start + size
        self.ss: int = source_start
        self.se: int = source_start + size
        self.size: int = size
        self.difference: int = destination_start - source_start

    def __str__(self) -> str:
        return f"({self.ds}, {self.ss}, {self.size})"
    
    def __repr__(self) -> str:
        return str(self)


def convert_result(result: Result, conversion: Conversion) -> tuple[Result, list[Result]] | None:
    # Checks if the result range is outside of the conversion range
    if result.end < conversion.ss or result.start > conversion.se: return None
    
    # The new converted result
    new_result: Result = Result()
    
    # Potentially, the new unvonverted result ranges (left and right of the conversion range)
    rest_results: list[Result] = [None] * 2
    
    # Checks if the result range is further left than the conversion range
    if result.start < conversion.ss:
        new_result.start = conversion.ss + conversion.difference
        rest_results[0] = Result(
            start = result.start, 
            end = conversion.ss-1,
        )
    else:
        new_result.start = result.start + conversion.difference
    
    # Checks if the result range is further right than the conversion range
    if result.end > conversion.se:
        new_result.end = conversion.se + conversion.difference
        rest_results[1] = Result(
            start = conversion.se+1, 
            end = result.end,
        )
    else:
        new_result.end = result.end + conversion.difference
    
    return new_result, rest_results


def run_conversion_map(map: list[Conversion], results: list[Result]) -> list[Result]:
    new_results: list[Result] = []
    while len(results) > 0:
        result: Result = results.pop(0)
        for i, conversion in enumerate(map):
            if (ret := convert_result(result, conversion)) is None:
                continue
            new_results.append(ret[0])
            if ret[1][0] and ret[1][1]:
                map.pop(i)
            [results.append(result) for result in ret[1] if result is not None]
            break
        else:
            new_results.append(result)
    return new_results


def parse_maps(lines: list[str]) -> list[list[Conversion]]:
    lines: list[str] = [line for line in lines 
             if line[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\n']]
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

    
def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    seed_line = lines[0].split(" ")
    seed_ranges = [Result(int(seed_line[i]), int(seed_line[i]) + int(seed_line[i+1])) 
                   for i in range(1, len(seed_line), 2)]

    conversion_maps: list[list[Conversion]] = parse_maps(lines[2:])
    results: list[Result] = seed_ranges
    for map in conversion_maps:
        results = run_conversion_map(map, results)

    smallest = results[0].start
    for i in results:
        smallest = i.start if i.start < smallest else smallest
        
    print(smallest)

if __name__ == "__main__":
    main()
