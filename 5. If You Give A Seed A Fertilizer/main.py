class Result:
    def __init__(self, start: int = 0, end: int = 0, conversion: int = 0):
        self.start: int = start
        self.end: int = end
        self.conversion: int = conversion

    
    def exec_conversion(self) -> None:
        self.start += self.conversion
        self.end += self.conversion
        self.conversion = 0

    def __str__(self) -> str:
        return f"({self.start}, {self.end})"

    def __repr__(self) -> str:
        return str(self)
    

class Conversion:
    def __init__(self, destination_start: int, source_start: int, size: int):
        self.ds: int = destination_start
        self.ss: int = source_start
        self.se: int = source_start + size - 1
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
        new_result.start = conversion.ss
        rest_results[0] = Result(
            start = result.start, 
            end = conversion.ss-1,
        )
    else:
        new_result.start = result.start
    
    # Checks if the result range is further right than the conversion range
    if result.end > conversion.se:
        new_result.end = conversion.se
        rest_results[1] = Result(
            start = conversion.se+1, 
            end = result.end,
        )
    else:
        new_result.end = result.end
    
    new_result.conversion = conversion.difference
    return new_result, rest_results


def run_conversion_map(conversion_map: list[Conversion], results: list[Result]) -> list[Result]:
    # List for storing all the new results
    new_results: list[Result] = []

    # Run until all results have been converted
    while results:
        
        # Save the currently handled result from the result list 
        result = results.pop(0)

        # Find the conversion range that can be applied to the result
        for conversion in conversion_map:

            # If the conversion range is not applicable to the result, skip it
            if (ret := convert_result(result, conversion)) is None:
                continue
            
            # Add the new converted result to the new results list
            new_results.append(ret[0])

            # If there are any new unconverted ranges, add them to the results list
            [results.append(result) for result in ret[1] if result is not None]
            
            # Move on to the next result
            break
        else:
            # If no conversion range was applicable, add the result to the new results list
            new_results.append(result)
    
    return new_results

def run_all_maps(results: list[Result], maps: list[list[Conversion]]) -> list[Result]:
    for map in maps:
        results = run_conversion_map(map, results)
        [result.exec_conversion() for result in results]
    return results

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
    map_lines.append(curr_map)
    return [[Conversion(*(int(arg) for arg in conversion_line)) 
         for conversion_line in conversion_lines] 
         for conversion_lines in map_lines]
    
def part1(lines: list[str]) -> int:
    seed_line = lines[0].removeprefix("seeds: ").split(" ")
    results = [Result(int(seed), int(seed)) for seed in seed_line]
    conversion_maps = parse_maps(lines[2:])
    return min(result.start for result in run_all_maps(results, conversion_maps))

def part2(lines: list[str]) -> int:
    seed_line = lines[0].removeprefix("seeds: ").split(" ")
    results = [Result(start := int(seed_line[i]), start + int(seed_line[i+1]) - 1) for i in range(0, len(seed_line), 2)]
    conversion_maps = parse_maps(lines[2:])
    return min(result.start for result in run_all_maps(results, conversion_maps))

def main():
    with open("5. If You Give A Seed A Fertilizer/input.txt", "r") as f:
        lines = f.readlines()

    for i, part in enumerate([part1, part2]):
        print(f'Part {i+1}: {part(lines)}')

if __name__ == "__main__":
    main()