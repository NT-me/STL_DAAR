def precalcul(s):
    carryOver = [0]
    for i in range(1, len(s)):
        carryOver.append(0)
        suffix = s[i]
        prefix = ""
        for j in range(i):
            prefix += s[j]
            if suffix in prefix:
                carryOver[i] += 1
                if i-len(suffix) > 0:
                    suffix = s[i-len(suffix)] + suffix
                else:
                    break

    return carryOver

def kmp(match, search):
    if len(match) == 0:
        return search

    res = []
    lps = precalcul(match)

    i = 0
    while i <= len(search) - len(match):
        if search[i] == match[0]:
            found = True
            for j in range(1, len(match)):
                if search[i + j] != match[j]:
                    found = False
                    i += lps[j]
                    break
            if found:
                res.append([i, i + len(match)])
                i += len(match) - 1
        i += 1
    return res

if __name__ == "__main__":
    # print(precalcul("AABAACAABAA"))
    # print(precalcul("mamamia"))
    # print(precalcul_kmp("mamamia"))
    print(kmp("it", "paragraph where it is referenced. Many illustrations are composite"))