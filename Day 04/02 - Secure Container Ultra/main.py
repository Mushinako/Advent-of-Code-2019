#!/usr/bin/env python3
LOWER = 254032
UPPER = 789860


def main():
    count = 0
    for n in range(LOWER, UPPER + 1):
        ns = str(n)
        current_char = ""
        double = False
        combo = 1
        for char in ns:
            if current_char > char:
                break
            elif current_char == char:
                combo += 1
            else:
                if combo == 2:
                    double = True
                combo = 1
                current_char = char
        else:
            if double or combo == 2:
                count += 1
    print(count)


main()