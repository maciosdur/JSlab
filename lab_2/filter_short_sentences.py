import sys

def filter_short_sentences():
    current_sentence = ""
    filtered_sentences = []
    
    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char in ".!?": 
                words = current_sentence.strip().split()
                if len(words) <= 4:
                    filtered_sentences.append(current_sentence.strip())
                current_sentence = "" 

    return filtered_sentences

if __name__ == "__main__":
    result = filter_short_sentences()
    for sentence in result:
        print(sentence)