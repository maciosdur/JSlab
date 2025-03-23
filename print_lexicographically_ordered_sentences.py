import sys

def is_lexicographically_ordered(sentence):
    words = sentence.lower().split()
    return all(words[i] <= words[i + 1] for i in range(len(words) - 1))

def print_lexicographically_ordered_sentences(input_stream):
    sentence = ""
    
    for line in input_stream:
        for char in line:
            sentence += char
            if char in ".!?":
                if is_lexicographically_ordered(sentence.strip()):
                    print(sentence.strip())
                sentence = ""

if __name__ == "__main__":
    print_lexicographically_ordered_sentences(sys.stdin)
