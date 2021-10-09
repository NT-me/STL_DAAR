import kmp

# SANS PRINT
# def egrep(regexMode, file, match):
#     OKGREEN = "\033[92m"
#     ENDC = "\033[0m"

#     res = ""

#     if not regexMode:
#         match = match.toWord()

#     for l in file:
#         if regexMode:
#             matches = match.checkString(l)
#         else:
#             matches = kmp.kmp(match, l)

#         start = 0
#         for m in matches:
#             res += l[:m[0]]
#             res += OKGREEN + l[m[0]: m[1]+1] + ENDC

#         if start != 0 and start < len(l):
#             res += l[start:] + "\n"

#     print(res)

# AVEC PRINT
def egrep(regexMode, file, match):
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"

    if not regexMode:
        match = match.toWord()

    for l in file:
        if regexMode:
            matches = match.checkString(l)
        else:
            matches = kmp.kmp(match, l)

        start = 0
        for m in matches:
            print(l[:m[0]], end="")
            print(OKGREEN + l[m[0]: m[1]+1] + ENDC, end="")
            start = m[1]+1

        if start != 0 and start < len(l):
            print(l)
