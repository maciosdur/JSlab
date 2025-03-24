import sys

def clean_text():
    preambula = True
    tresc = False
    empty_lines = 0
    checked_lines = 0
    buffer = []

    for line in sys.stdin:
        line = line.strip()
        checked_lines += 1

        if preambula:
            buffer.append(line)
            
            if line == "":
                empty_lines += 1
                nextline = next(sys.stdin, None)
                if nextline is not None:
                    nextline = nextline.strip()
                    buffer.append(nextline)
                    if nextline == "":
                        preambula = False
                        tresc = True
                        buffer = [] 
                continue

            if checked_lines >= 10:
                preambula = False
                tresc = True
                for saved_line in buffer:
                    yield saved_line  
                buffer = [] 
        
        if line.startswith("-----"):
            break

        if tresc:
            yield line

    if preambula:
        for saved_line in buffer:
            yield saved_line

if __name__ == "__main__":
    for line in clean_text():
        print(line)