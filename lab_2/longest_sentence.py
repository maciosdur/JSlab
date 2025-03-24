import sys

def longest_sentence():
    longest = ""
    current = ""

    for line in sys.stdin:
        for char in line:
            current += char
            if char in ".!?":
                if len(current) > len(longest):
                    longest = current
                current = ""
    return longest.strip()

if __name__ == "__main__":
    result = longest_sentence()
    print(result)