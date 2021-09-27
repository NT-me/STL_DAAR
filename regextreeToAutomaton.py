from regextree import RegExTree
from automaton import Automaton


# ast = returnRet()
# print(ast)

def toAutomaton(tree: RegExTree):

    if len(tree.subTrees) < 1:
        tTab = [[-1 for i in range(0, 256)] for j in range(0, 2)]
        eTab = [[], []]

        tTab[0][ord(tree.root)] = 1

        return Automaton(tTab, eTab)

    if tree.root == '.':

        gauche = toAutomaton(tree.subTrees[0])
        tTab_g = gauche.tTab
        eTab_g = gauche.eTab

        droite = toAutomaton(tree.subTrees[1])
        tTab_d = droite.tTab
        eTab_d = droite.eTab

        lg = len(tTab_g)
        ld = len(tTab_d)

        tTab = [[-1 for i in range(0, 256)] for j in range(0, lg + ld)]
        eTab = [[] for i in range(0, lg + ld)]

        eTab[lg - 1].append(lg)

        for i in range(0, lg):
            for col in range(0, 256):
                if tTab_g[i][col] != -1:
                    tTab[i][col] = tTab_g[i][col]

        for i in range(0, lg):
            eTab[i].extend(eTab_g[i])

        for i in range(lg, lg+ld-1):
            for col in range(0, 256):
                if tTab_d[i - lg][col] != -1:
                    tTab[i][col] = tTab_d[i - lg][col] + lg

        for i in range(lg, lg+ld-1):
            for s in eTab_d[i - lg]:
                eTab[i].append(s + lg)

        return Automaton(tTab, eTab)

    if tree.root == '|':
        gauche = toAutomaton(tree.subTrees[0])
        tTab_g = gauche.tTab
        eTab_g = gauche.eTab

        droite = toAutomaton(tree.subTrees[1])
        tTab_d = droite.tTab
        eTab_d = droite.eTab

        lg = len(tTab_g)
        ld = len(tTab_d)

        tTab = [[-1 for i in range(0, 256)] for j in range(0, lg + ld + 2)]
        eTab = [[] for i in range(0, lg + ld + 2)]

        eTab[0].append(1)
        eTab[0].append(1 + lg)
        eTab[lg].append(1 + lg + ld)
        eTab[lg + ld].append(1 + lg + ld)

        for i in range(1, lg + 1):
            for col in range(0, 256):
                if tTab_g[i-1][col] != -1:
                    tTab[i][col] = tTab_g[i-1][col] + 1

        for i in range(1, lg + 1):
            for s in eTab_g[i-1]:
                eTab[i].append(s + 1)

        for i in range(lg + 1, lg + ld):
            for col in range(0, 256):
                if tTab_d[i - lg - 1][col] != -1:
                    tTab[i][col] = tTab_d[i-lg-1][col] + lg + 1

        for i in range(lg + 1,lg + ld + 1):
            for s in eTab_d[i-1-lg]:
                eTab[i].append(s + 1 + lg)

        return Automaton(tTab, eTab)

    if tree.root == '*':

        fils = toAutomaton(tree.subTrees[0])
        tTab_f = fils.tTab
        eTab_f = fils.eTab

        l = len(tTab_f)

        tTab = [[-1 for i in range(0, 256)] for j in range(0, l+2)]
        eTab = [[] for i in range(0, l + 2)]

        eTab[0].append(1)
        eTab[0].append(l + 1)
        eTab[l].append(l + 1)
        eTab[l].append(1)

        for i in range(1, l + 1):
            for col in range(0, 256):
                if tTab_f[i-1][col] != -1:
                    tTab[i][col] = tTab_f[i-1][col]+1

        for i in range(1, l + 1):
            for s in eTab_f[i-1]:
                eTab[i].append(s+1)

        return Automaton(tTab, eTab)

    if tree.root == '+':

        fils = toAutomaton(tree.subTrees[0])
        tTab_f = fils.tTab
        eTab_f = fils.eTab

        l = len(tTab_f)

        tTab = [[-1 for i in range(0, 256)] for j in range(0, l + 2)]
        eTab = [[] for i in range(0, l + 2)]

        eTab[0].append(1)
        eTab[0].append(l + 1)
        eTab[l].append(l + 1)

        for i in range(1, l + 1):
            for col in range(0, 256):
                if tTab_f[i-1][col] != -1:
                    tTab[i][col] = tTab_f[i-1][col]

        for i in range(1, l + 1):
            for s in eTab_f[i-1]:
                eTab[i].append(s+1)

        return Automaton(tTab, eTab)

    return None
#############


# automaton = toAutomaton(ast)
# print(automaton)