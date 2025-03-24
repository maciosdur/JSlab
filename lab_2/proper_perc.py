import sys

def proper_perc():
    proper = 0
    sentence = 0
    big = 0

    for line in sys.stdin:
        for char in line:
            if char in ".!?":
                if big > 1:
                    proper += 1
                sentence += 1
                big = 0
            elif 'A' <= char <= 'Z':
                big += 1

    if sentence > 0:
        return proper / sentence
    else:
        return "no sentences"

if __name__ == "__main__":
    result = proper_perc()
    print(result)
