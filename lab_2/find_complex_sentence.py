import sys

def find_complex_sentence(input_stream):
    current_sentence = ""
    comma_count = 0

    for line in input_stream:
        for char in line:
            current_sentence += char
            if char == ",":
                comma_count += 1
            if char in ".!?": 
                if comma_count > 1: 
                    print(current_sentence.strip())
                    return
                current_sentence = ""
                comma_count = 0
    print("Brak zdania z więcej niż jednym zdaniem podrzędnym.")

if __name__ == "__main__":
    find_complex_sentence(sys.stdin)