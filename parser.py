from regextree import RegExTree as Ret
import contains as cont
from utils import specialValues as sv


def parse(result):

    while cont.containParenthese(result):
        result = processParenthese(result)

    while cont.containEtoile(result):
        result = processEtoile(result)

    while cont.containPlus(result):
        result = processPlus(result)

    while cont.containConcat(result):
        result = processConcat(result)

    while cont.containAltern(result):
        result = processAltern(result)

    if len(result) > 1:
        raise Exception("result tree len is : "+str(len(result)))
    return removeProtection(result[0])


def preparse(inputRegex):
    result = []
    protecChar = False
    justreadPtc = False

    for char in inputRegex:
        if char == "\\" and not protecChar:
            protecChar = True
            justreadPtc = True

        if not protecChar:
            if char == ".":
                char = sv.CONCAT
            elif char == "|":
                char = sv.ALTERNATE
            elif char == "+":
                char = sv.PLUS
            elif char == "(":
                char = sv.PARENTHESEOUVERTE
            elif char == ")":
                char = sv.PARENTHESEFERMEE
            elif char == "*":
                char = sv.STAR

        if not justreadPtc:
            if char != sv.CONCAT:
                # Retrait des .
                result.append(Ret(char, []))
        else:
            justreadPtc = False

        if char != "\\" and protecChar:
            protecChar = False
    return parse(result)


def processParenthese(trees):
    res = []
    flagFound = False

    for t in trees:
        if not flagFound and t.root == sv.PARENTHESEFERMEE:
            done = False
            content = []
            while not done and not (len(res) == 0):
                if res[len(res)-1].root == sv.PARENTHESEOUVERTE:
                    done = True
                    res.pop(len(res)-1)
                else:
                    content.insert(0, res.pop(len(res)-1))
            if not done:
                raise Exception("Syntax error, miss closing parenthesis")
            flagFound = True
            subTrees = []
            subTrees.append(parse(content))
            res.append(Ret(sv.PROTECTION, subTrees))
        else:
            res.append(t)

    if not flagFound:
        raise Exception("Parenthesis problem")
    return res


def processEtoile(trees):
    result = []
    found = False
    for t in trees:
        if not found and t.root == sv.STAR and len(t.subTrees) == 0:
            if len(result) == 0:
                raise Exception("Something go bad near '*'")
            found = True
            last = result.pop(len(result)-1)
            subTrees = []
            subTrees.append(last)
            result.append(Ret("*", subTrees))
        else:
            result.append(t)
    return result


def processPlus(trees):
    result = []
    found = False
    for t in trees:
        if not found and t.root == sv.PLUS and len(t.subTrees) == 0:
            if len(result) == 0:
                raise Exception("Something go bad near '+'")
            found = True
            last = result.pop(len(result)-1)
            subTrees = []
            subTrees.append(last)
            result.append(Ret("+", subTrees))
        else:
            result.append(t)
    return result


def processConcat(trees):
    result = []
    found = False
    firstFound = False

    for t in trees:
        if not found and not firstFound and t.root != sv.ALTERNATE:
            firstFound = True
            result.append(t)
            continue

        elif not found and firstFound and t.root == sv.ALTERNATE:
            firstFound = False
            result.append(t)
            continue

        elif not found and firstFound and t.root != sv.ALTERNATE:
            found = True
            last = result.pop(len(result)-1)
            subTrees = []
            subTrees.append(last)
            subTrees.append(t)
            result.append(Ret(".", subTrees))

        else:
            result.append(t)
    return result


def processAltern(trees):
    result = []
    found = False
    gauche = None
    done = False

    for t in trees:
        if not found and t.root == sv.ALTERNATE and len(t.subTrees) == 0:
            if len(result) == 0:
                raise Exception("Nothing after '|' wtf")
            found = True
            gauche = result.pop(len(result)-1)
            continue
        if found and not done:
            if gauche == None:
                raise Exception
            done = True
            subTrees = []
            subTrees.append(gauche)
            subTrees.append(t)
            result.append(Ret("|", subTrees))
        else:
            result.append(t)
    return result


def removeProtection(tree):
    if tree.root == sv.PROTECTION and len(tree.subTrees) != 1:
        raise Exception
    if not tree.subTrees:
        return tree
    if tree.root == sv.PROTECTION:
        return removeProtection(tree.subTrees[0])

    subTrees = []

    for t in tree.subTrees:
        subTrees.append(removeProtection(t))
    return Ret(tree.root, subTrees)

def returnRet():
    inputRegex = input("Entrez une Regex valide:\n")
    return preparse(str(inputRegex))
