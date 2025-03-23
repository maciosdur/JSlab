import sys

def longest_unique_sentence(input_stream):
    longest=""
    current=""

    def is_unique(sentence):
        words = sentence.lower().split()
        first=None
        first2=""
        for word in words:
            first2=word[0]
            if first==first2:
                return False
            first=first2
        
        return True


    for line in input_stream:
        for char in line:
            current+= char
            if char in ".!?":
                if len(current)>len(longest):
                    if is_unique(current):
                        longest=current
                current=""
    print(longest.strip())

if __name__ == "__main__":
    longest_unique_sentence(sys.stdin)