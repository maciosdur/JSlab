import sys

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
from print_lexicographically_ordered_sentences import print_lexicographically_ordered_sentences

def main():
    try:
        count_paragraphs(clean_text(sys.stdin))  
        print("\n")
        sys.stdin.seek(0)
        count_chars(clean_text(sys.stdin)) 
        print("\n")
        sys.stdin.seek(0)
        proper_perc(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        longest_sentence(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        longest_unique_sentence(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        find_complex_sentence(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        filter_short_sentences(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        filter_questions_exclamations(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        first_20_sentences(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        filter_sentences_with_words(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        filter_quartile_sentences(clean_text(sys.stdin))
        print("\n")
        sys.stdin.seek(0)
        print_lexicographically_ordered_sentences(clean_text(sys.stdin))
        print("\n")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()