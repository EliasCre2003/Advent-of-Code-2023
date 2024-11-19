class Universe:
    def __init__(self, universe: list[list[str]], expansion_factor: int = 1):
        self._galaxies: list[list[bool]] = [[cell == '#' for cell in row] for row in universe]
        self._expansion_factor: int = expansion_factor
        self._long_rows: list[int] = [i for i, row in enumerate(self._galaxies) if sum(row) == 0]
        self._long_cols: list[int] = [x for x in range(len(self._galaxies)) 
                                        if sum(self._galaxies[y][x] for y in range(len(self._galaxies))) == 0]
        
    def all_galaxies(self) -> list[tuple[int, int]]:
        galaxy_coords = []
        for y, row in enumerate(self._galaxies):
            for x, cell in enumerate(row):
                if cell: galaxy_coords.append((x, y))
        return galaxy_coords
    
    def shortest_distance(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> int:
        dist: int = 0
        for y in range(*sorted([coord1[1]+1, coord2[1]+1])):
            if y in self._long_rows: dist += self._expansion_factor
            else: dist += 1
        for x in range(*sorted([coord1[0]+1, coord2[0]+1])):
            if x in self._long_cols: dist += self._expansion_factor
            else: dist += 1
        return dist
    
    def all_distances(self) -> list[int]:
        all_galaxies = self.all_galaxies()
        distances: list[int] = []
        for i, galaxy1 in enumerate(all_galaxies):
            for galaxy2 in all_galaxies[i+1:]:
                distances.append(self.shortest_distance(galaxy1, galaxy2))
        return distances

def main():
    with open("11. Cosmic Expansion/input.txt", "r") as f:
        lines = f.readlines()

    for i, expansion in enumerate([2, 1_000_000]):
        universe = Universe([list(line.strip()) for line in lines], expansion)
        print(f"Part {i+1}: {sum(universe.all_distances())}")
    

if __name__ == "__main__":
    main()