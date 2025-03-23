import sys

def proper_perc(input_stream):
    proper = 0
    sentence=0
    big=0

    for line in input_stream:
        for char in line:
            if char in ".!?":
                if big>1:
                    proper+=1
                sentence+=1
                big=0
            elif 'A' <= char <= 'Z':
                big+=1
    if sentence > 0:
        print(proper/sentence)
    else:
        print("no sentences")

if __name__ == "__main__":
    proper_perc(sys.stdin)
    