import sys

def find_complex_sentence():
    current_sentence = ""
    comma_count = 0

    for line in sys.stdin:
        for char in line:
            current_sentence += char
            if char == ",":
                comma_count += 1
            if char in ".!?": 
                if comma_count > 1: 
                    return current_sentence.strip()
                current_sentence = ""
                comma_count = 0
    return "Brak zdania z więcej niż jednym zdaniem podrzędnym."

if __name__ == "__main__":
    result = find_complex_sentence()
    print(result)