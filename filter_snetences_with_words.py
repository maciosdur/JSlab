import sys

def filter_sentences_with_words(input_stream):
    target_words = {"i", "oraz", "ale", "że", "lub"} 
    current_sentence = ""
    
    for line in input_stream:
        for char in line:
            current_sentence += char
            if char in ".!?":
                words = current_sentence.strip().lower().split()
                count = sum(1 for word in words if word in target_words)
                
                if count >= 2: 
                    print(current_sentence.strip())  
                
                current_sentence = ""

if __name__ == "__main__":
    filter_sentences_with_words(sys.stdin)
