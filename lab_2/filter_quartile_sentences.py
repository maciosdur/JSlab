import sys

def filter_quartile_sentences(input_stream):
    sentences = []
    current_sentence = ""

    for line in input_stream:
        for char in line:
            current_sentence += char
            if char in ".!?":
                sentences.append(current_sentence.strip())
                current_sentence = ""

    if len(sentences) < 4:
        print("Zbyt mało zdań, by obliczyć kwartyle.")
        return

    sentence_lengths = [len(sentence) for sentence in sentences]
    sentence_lengths.sort()
    quartile_4 = sentence_lengths[int(0.75 * len(sentence_lengths))]


    for sentence in sentences:
        if len(sentence) >= quartile_4:
            print(sentence)

if __name__ == "__main__":
    filter_quartile_sentences(sys.stdin)
