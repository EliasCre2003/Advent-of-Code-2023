lines = []
with open("1. Trebuchet/input2.txt", 'r') as f:
    for line in f:
        lines.append(line)

def part_1():
    output = 0
    for line in lines:
        foundFirst = False
        first, last = None, None
        for char in line:
            n = 0
            try:
                n = int(char)
            except ValueError:
                continue
            if foundFirst:
                last = n
            else:
                first = n
                foundFirst = True
        if last is None:
            last = first
        output += first * 10 + last
    print(output)

def part_2():
    output = 0
    for line in lines:
        line.lower()
        foundFirst = False
        first, last = None, None
        i = 0
        while i < len(line):
            n = 0
            try:
                n = int(line[i])
            except ValueError:
                n = string_is_digit(line, i)
                if n is None:
                    i += 1
                    continue
                else:
                    i += n[1] - 2
                    n = n[0]
            if foundFirst:
                last = n
            else:
                first = n
                foundFirst = True
            i+=1
        if last is None:
            last = first
        output += first * 10 + last
    print(output)

# def part_2():
#     for i in range(len(lines)):
#         lines[i] = convertLine(lines[i])
#     part_1()


# def convertLine(line: str) -> str:
#     digit_map = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", 
#                  "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
#     for string in digit_map:
#         line = line.replace(string, digit_map[string], )
#     return line


def string_is_digit(line: str, index: int) -> tuple[int, int]:
    digit_list = [[["one", 1], ["two", 2], ["six", 6]], 
                  [["zero", 0], ["four", 4], ["nine", 9], ["five", 5]], 
                  [["three", 3], ["seven", 7], ["eight", 8]]]
    for i in range(3, 6):
        if index + i >= len(line):
            return None
        string = line[index: index+i]
        for case in digit_list[i-3]:
            if string == case[0]:
                return (case[1], i)
    return None

part_2()