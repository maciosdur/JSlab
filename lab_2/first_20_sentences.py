import sys

def first_20_sentences(input_stream):
    sentence_count = 0
    current_sentence = ""

    for line in input_stream:
        for char in line:
            current_sentence += char
            if char in ".!?":
                sentence_count += 1
                print(current_sentence.strip())  
                current_sentence = "" 
                if sentence_count >= 20:
                    return

if __name__ == "__main__":
    first_20_sentences(sys.stdin)
