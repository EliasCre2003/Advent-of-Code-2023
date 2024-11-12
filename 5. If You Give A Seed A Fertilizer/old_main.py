with open("test.txt", "r") as f:
    lines: list[str] = f.readlines()

class Map:
    def __init__(self, map_list: list[str]) -> None:
        self.name = map_list.pop(0)[0:-1]
        self.ranges = [line.split(" ") for line in map_list]
        self.ranges: list[MapRange] = [MapRange(int(range[0]), int(range[1]), int(range[2])) for range in self.ranges]
        
    def source_to_destination(self, source: int) -> int:
        for range in self.ranges:
            if range.src_start <= source < range.src_start + range.len:
                return range.dest_start + (source - range.src_start)
        return source
    
    def sources_to_destinations(self, source_range: tuple[int, int]) -> list[tuple[int, int]]:
        destination_ranges = []
        sub_src_ranges = [source_range]
        while len(sub_src_ranges) > 0:
            sub_src_range = sub_src_ranges.pop(0)
            for range in self.ranges:
                if range.src_start <= sub_src_range[0] <= range.src_start + range.len:
                    if range.len >= sub_src_range[1] + (sub_src_range[0] - range.src_start):
                        destination_ranges.append((sub_src_range[0] + (range.dest_start - range.src_start), sub_src_range[1]))          
                    else:
                        destination_ranges.append((sub_src_range[0] + (range.dest_start - range.src_start), range.len - (range.src_start - sub_src_range[0])))
                        sub_src_ranges.append((range.src_start + range.len, sub_src_range[1] - (range.src_start + range.len)))
                    break
                if sub_src_range[0] + sub_src_range[1] > range.src_start and sub_src_range[0] < range.src_start + range.len:
                    sub_src_ranges.append((sub_src_range[0], range.src_start - sub_src_range[0]))
                    if sub_src_range[0] + sub_src_range[1] > range.src_start + range.len:
                        destination_ranges.append((range.dest_start, range.len))
                        sub_src_ranges.append((range.src_start + range.len, sub_src_range[0] + sub_src_range[1] - (range.src_start + range.len)))
                    else:
                        destination_ranges.append((range.dest_start, sub_src_range[1] - (range.src_start - sub_src_range[0])))
                    break
            else:
                destination_ranges.append(sub_src_range)
        return destination_ranges


class MapRange:
    def __init__(self, dest_start, src_start, len):
        self.dest_start = dest_start
        self.src_start = src_start
        self.len = len


seed_line = lines[0]
lines = lines[2:]
seed_line = seed_line[7:-1]
seed_line = seed_line.split(" ")
seeds = [int(string) for string in seed_line]

map_lists: list[list[str]] = []
i = 0
for j in range(len(lines)):
    if lines[j] == "\n" or j == len(lines) - 1:
        map_lists.append(lines[i:j])
        map_lists[-1] = [map_list[0:-1] for map_list in map_lists[-1]]
        i = j + 1

maps = [Map(map_list) for map_list in map_lists]

def part1():
    locations = []
    for seed in seeds:
        current = seed
        for map in maps:
            current = map.source_to_destination(current)
        locations.append(current)
    print(min(locations))

def part2():
    seed_ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    location_ranges = []
    for seed_range in seed_ranges:
        current = [seed_range]
        for map in maps:
            new_current = []
            while len(current) > 0:
                output = map.sources_to_destinations(current.pop(0))
                for i in output:
                    new_current.append(i)
            current = new_current
        for i in current:
            location_ranges.append(i)
    lowest = location_ranges[0][0]
    for location_range in location_ranges:
        min(lowest, location_range[0])
    print(lowest)

part2()