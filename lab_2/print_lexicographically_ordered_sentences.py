import sys

def is_lexicographically_ordered(sentence):
    words = sentence.lower().split()
    return all(words[i] <= words[i + 1] for i in range(len(words) - 1))

def get_lexicographically_ordered_sentences():
    sentence = ""
    ordered_sentences = []
    
    for line in sys.stdin:
        for char in line:
            sentence += char
            if char in ".!?":
                if is_lexicographically_ordered(sentence.strip()):
                    ordered_sentences.append(sentence.strip())
                sentence = ""
    
    return ordered_sentences

if __name__ == "__main__":
    result = get_lexicographically_ordered_sentences()
    for sentence in result:
        print(sentence)
