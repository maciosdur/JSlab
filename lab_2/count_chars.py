import sys

def count_chars():
    char_count = 0

    for line in sys.stdin:
        char_count += sum(1 for char in line if not char.isspace())

    return char_count

if __name__ == "__main__":
    print(count_chars())
