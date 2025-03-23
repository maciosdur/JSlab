import sys

def filter_short_sentences(input_stream):
    current_sentence = ""
    
    for line in input_stream:
        for char in line:
            current_sentence += char
            if char in ".!?": 
                words = current_sentence.strip().split()
                if len(words) <= 4:
                    print(current_sentence.strip())
                current_sentence = "" 

if __name__ == "__main__":
    filter_short_sentences(sys.stdin)