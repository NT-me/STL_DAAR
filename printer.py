import kmp

# SANS PRINT
""" def egrep(regexMode, file, match):
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"

    nbMatches = 0
    res = ""

    if not regexMode:
        match = match.toWord()

    for l in file:
        if regexMode:
            matches = match.checkString(l)
        else:
            matches = kmp.kmp(match, l)

        start = 0
        for m in matches:
            nbMatches += 1
            res += l[:m[0]]
            res += OKGREEN + l[m[0]: m[1]] + ENDC

        if start != 0 and start < len(l):
            res += l[start:] + "\n"

    print(res)
    print(str(nbMatches) + " matches found") """

# AVEC PRINT
def egrep(regexMode, file, match):
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"

    nbMatches = 0

    if not regexMode:
        match = match.toWord()

    for l in file:
        if regexMode:
            matches = match.checkString(l)
        else:
            matches = kmp.kmp(match, l)

        start = 0
        for m in matches:
            nbMatches += 1
            print(l[:m[0]], end="")
            print(OKGREEN + l[m[0]: m[1]] + ENDC, end="")
            start = m[1]+1

        if start != 0 and start < len(l):
            print(l[start:])

    print(str(nbMatches) + " matches found")