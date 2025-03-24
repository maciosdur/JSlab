import sys

def filter_sentences_with_words():
    target_words = {"i", "oraz", "ale", "że", "lub"} 
    current_sentence = ""
    filtered_sentences = []
    
    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char in ".!?":
                words = current_sentence.strip().lower().split()
                count = sum(1 for word in words if word in target_words)
                
                if count >= 2: 
                    filtered_sentences.append(current_sentence.strip())
                
                current_sentence = ""

    return filtered_sentences

if __name__ == "__main__":
    result = filter_sentences_with_words()
    for sentence in result:
        print(sentence)
