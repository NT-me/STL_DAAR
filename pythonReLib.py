import re
import time as t

if __name__ == "__main__":

    fps = [
        "books/AlicesAdventuresinWonderland.txt",
        "books/MobyDick.txt",
        "books/Frankenstein.txt",
        "books/PrideAndPrejudice.txt",
        "books/TheAdventuresofSherlockHolmes.txt"
    ]
    res = dict()
    for bp in fps:
        i = 0
        file = open(bp, 'r')
        genStart = t.time()
        for l in file:
            # reg = re.compile("a|(th*e+)")
            reg = re.compile("the")
            if reg.search(l):
                print(l)
                i += 1
        res[bp] = t.time() - genStart
        res[bp + "nb"] = i

    for e in res:
        print(e)
        print(res[e])
        print("\n\n ===")
