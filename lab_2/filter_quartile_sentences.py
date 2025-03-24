import sys

def filter_quartile_sentences():
    sentences = []
    current_sentence = ""

    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char in ".!?":
                sentences.append(current_sentence.strip())
                current_sentence = ""

    if len(sentences) < 4:
        return "Zbyt mało zdań, by obliczyć kwartyle."

    sentence_lengths = [len(sentence) for sentence in sentences]
    sentence_lengths.sort()
    quartile_4 = sentence_lengths[int(0.75 * len(sentence_lengths))]

    filtered_sentences = [sentence for sentence in sentences if len(sentence) >= quartile_4]
    return filtered_sentences

if __name__ == "__main__":
    result = filter_quartile_sentences()
    if isinstance(result, str):
        print(result)
    else:
        for sentence in result:
            print(sentence)
