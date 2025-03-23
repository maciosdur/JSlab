import sys

def count_paragraphs(input_stream):
    paragraph_count = 0
    in_paragraph = False

    for line in input_stream:
        line = line.strip()

        if line == "":
            if in_paragraph:
                paragraph_count += 1
                in_paragraph = False
        else:
            in_paragraph = True

    if in_paragraph:
        paragraph_count += 1

    print(paragraph_count)

if __name__ == "__main__":
    count_paragraphs(sys.stdin)