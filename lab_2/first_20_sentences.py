import sys

def first_20_sentences():
    sentence_count = 0
    current_sentence = ""
    sentences = []

    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char in ".!?":
                sentence_count += 1
                sentences.append(current_sentence.strip())
                current_sentence = ""
                if sentence_count >= 20:
                    return sentences

    return sentences

if __name__ == "__main__":
    result = first_20_sentences()
    for sentence in result:
        print(sentence)
