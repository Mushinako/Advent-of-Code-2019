#!/usr/bin/env python3
TARGET = 19690720


def main():
    with open("input.txt", "r") as fp:
        code_orig = [int(i.strip()) for i in fp.readline().split(",")]
    for i in range(100):
        for j in range(100):
            code = code_orig[:]
            code[1] = i
            code[2] = j
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
            if code[0] == TARGET:
                print(100 * i + j)
                return


main()