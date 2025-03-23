import sys


def clean_text(input_stream):
    preambula=True
    tresc=False

    for line in sys.stdin:
        line=line.strip()

        if preambula:
            if line=="":
                nextline=next(sys.stdin, None)
                if nextline.strip()=="":
                    preambula=False
                    tresc=True
                    #line=line.strip()
            continue

        if line.startswith("-----"):
            break
        
        if tresc:
            print(line)

clean_text(sys.stdin)
