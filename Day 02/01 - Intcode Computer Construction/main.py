#!/usr/bin/env python3
def main():
    with open("input.txt", "r") as fp:
        code = [int(i.strip()) for i in fp.readline().split(",")]
    code[1] = 12
    code[2] = 2
    pointer = 0
    while True:
        action = code[pointer]
        if action == 99:
            break
        a = code[code[pointer + 1]]
        b = code[code[pointer + 2]]
        if action == 1:
            c = a + b
        elif action == 2:
            c = a * b
        else:
            raise ValueError()
        code[code[pointer + 3]] = c
        pointer += 4
    print(code[0])


main()