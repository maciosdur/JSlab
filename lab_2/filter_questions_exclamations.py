import sys

def filter_questions_exclamations(input_stream):
    current_sentence = ""

    for line in input_stream:
        for char in line:
            current_sentence += char
            if char in "!?": 
                print(current_sentence.strip())
                current_sentence = ""  
            elif char == ".": 
                current_sentence = ""

if __name__ == "__main__":
    filter_questions_exclamations(sys.stdin)
