lines: list[str]
nonsymbols: set[str] = {".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
digits: set[str] = set()
for i in range(10):
    digits.add(str(i))

with open("Gear Ratios/input.txt", "r") as f:
    lines = f.readlines()
lines = [line[0:-1] for line in lines]

def isPartNumber(line: int, start: int, stop: int) -> bool:
    adjacents: set[str] = set()
    if start != 0:
        start -= 1
    if stop != len(lines[line]) - 1:
        stop += 1
    if line != 0:
        for i in range(start, stop+1):
            adjacents.add(lines[line-1][i])
    adjacents.add(lines[line][start])
    adjacents.add(lines[line][stop])
    if line != len(lines) - 1:
        for i in range(start, stop+1):
            adjacents.add(lines[line+1][i])
    return len(adjacents.difference(nonsymbols)) != 0

def part1():
    total = 0
    for i in range(len(lines)):
        
        j = 0
        while j < len(lines[i]):
            n = 0
            isNumber = False
            while j < len(lines[i]) and lines[i][j] in digits:
                isNumber = True
                n *= 10
                n += int(lines[i][j])
                j += 1 
            if not isNumber:
                j += 1
                continue
            if isPartNumber(i, j - len(str(n)), j-1):
                total += n
    print(total)

stars: dict[tuple[int,int], list[int]] = {}
def findStarReferences(line: int, start: int, stop: int, n: int):
    if start != 0:
        start -= 1
    if stop != len(lines[line]) - 1:
        stop += 1
    if line != 0:
        for i in range(start, stop+1):
            if lines[line-1][i] == '*':
                stars[(line-1, i)].append(n)
    if lines[line][start] == '*':
        stars[(line, start)].append(n)
    if lines[line][stop] == '*':
        stars[(line, stop)].append(n)
    if line != len(lines) - 1:
        for i in range(start, stop+1):
            if lines[line+1][i] == '*':
                stars[(line+1, i)].append(n)

def part2():
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '*':
                stars[(i, j)] = []
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]):
            n = 0
            isNumber = False
            while j < len(lines[i]) and lines[i][j] in digits:
                isNumber = True
                n *= 10
                n += int(lines[i][j])
                j += 1 
            if not isNumber:
                j += 1
                continue
            findStarReferences(i, j - len(str(n)), j-1, n)
    total = 0
    keys = stars.keys()
    for key in keys:
        if len(stars[key]) == 2:
            total += stars[key][0] * stars[key][1]
    print(total)
    
part2()