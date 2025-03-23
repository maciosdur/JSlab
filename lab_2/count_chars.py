import sys

def count_chars(input_stream):
    char_count = 0

    for line in input_stream:
        char_count += sum(1 for char in line if not char.isspace())

    print(char_count)

if __name__ == "__main__":
    count_chars(sys.stdin)
    