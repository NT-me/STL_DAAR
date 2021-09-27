from regextree import RegExTree as Ret
from utils import specialValues as sv

def containAltern(trees):
    for t in trees:
        if t.root == sv.ALTERNATE and not t.subTrees:
            return True
    return False


def containParenthese(trees):
    for t in trees:
        if t.root == sv.PARENTHESEOUVERTE or t.root == sv.PARENTHESEFERMEE:
            return True
    return False


def containEtoile(trees):
    for t in trees:
        if t.root == sv.STAR and not t.subTrees:
            return True
    return False


def containPlus(trees):
    for t in trees:
        if t.root == sv.PLUS and not t.subTrees:
            return True
    return False


def containConcat(trees):
    flagFound = False
    # print(trees)
    for t in trees:
        if not flagFound and t.root != sv.ALTERNATE:
            flagFound = True
            continue
        if flagFound:
            if t.root != sv.ALTERNATE:
                return True
            else:
                flagFound = False
    return False
