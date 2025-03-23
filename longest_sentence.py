import sys

def longest_sentence(input_stream):
    longest=""
    current=""

    for line in input_stream:
        for char in line:
            current+= char
            if char in ".!?":
                if len(current)>len(longest):
                    longest=current
                current=""
    print(longest.strip())

if __name__ == "__main__":
    longest_sentence(sys.stdin)