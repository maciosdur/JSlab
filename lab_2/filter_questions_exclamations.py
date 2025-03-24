import sys

def filter_questions_exclamations():
    current_sentence = ""
    filtered_sentences = []

    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char in "!?": 
                filtered_sentences.append(current_sentence.strip())
                current_sentence = ""  
            elif char == ".": 
                current_sentence = ""

    return filtered_sentences

if __name__ == "__main__":
    result = filter_questions_exclamations()
    for sentence in result:
        print(sentence)
