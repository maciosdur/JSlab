import sys
from io import StringIO

from count_paragraphs import count_paragraphs
from count_chars import count_chars
from reader import clean_text
from proper_perc import proper_perc
from longest_sentence import longest_sentence
from longest_unique_sentence import longest_unique_sentence
from find_complex_sentence import find_complex_sentence
from filter_short_sentences import filter_short_sentences
from filter_questions_exclamations import filter_questions_exclamations
from first_20_sentences import first_20_sentences
from filter_sentences_with_words import filter_sentences_with_words
from filter_quartile_sentences import filter_quartile_sentences
from print_lexicographically_ordered_sentences import get_lexicographically_ordered_sentences

def main():
    try:
        # Read and clean the text
        original_text = sys.stdin.read()
        sys.stdin = StringIO(original_text)
        cleaned_text = "\n".join(clean_text())
        sys.stdin = StringIO(cleaned_text)
        
        print(count_paragraphs())
        print("\n")
        sys.stdin.seek(0)
        
        print(count_chars())
        print("\n")
        sys.stdin.seek(0)
        
        print(proper_perc())
        print("\n")
        sys.stdin.seek(0)
        
        print(longest_sentence())
        print("\n")
        sys.stdin.seek(0)
        
        print(longest_unique_sentence())
        print("\n")
        sys.stdin.seek(0)
        
        print(find_complex_sentence())
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in filter_short_sentences():
            print(sentence)
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in filter_questions_exclamations():
            print(sentence)
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in first_20_sentences():
            print(sentence)
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in filter_sentences_with_words():
            print(sentence)
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in filter_quartile_sentences():
            print(sentence)
        print("\n")
        sys.stdin.seek(0)
        
        for sentence in get_lexicographically_ordered_sentences():
            print(sentence)
        print("\n")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()