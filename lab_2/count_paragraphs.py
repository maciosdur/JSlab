import sys

def count_paragraphs():
    paragraph_count = 0
    in_paragraph = False

    for line in sys.stdin:
        line = line.strip()

        if line == "":
            if in_paragraph:
                paragraph_count += 1
                in_paragraph = False
        else:
            in_paragraph = True

    if in_paragraph:
        paragraph_count += 1

    return paragraph_count

if __name__ == "__main__":
    print(count_paragraphs())