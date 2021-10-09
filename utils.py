from enum import Enum


class specialValues(Enum):
    PROTECTION = "###PROTECTION###"
    CONCAT = "###CONCAT###"
    ALTERNATE = "###ALTERNATE###"
    PLUS = "###PLUS###"
    STAR = "###STAR###"
    PARENTHESEOUVERTE = "###PARENTHESEOUVERTE###"
    PARENTHESEFERMEE = "###PARENTHESEFERMEE###"


def reIndexDict(inputDict : dict) -> dict:
    res = dict()
    corresDict = dict()
    newIndex = 0
    for e in inputDict:
        oldIndex = inputDict[e][0]
        if oldIndex not in corresDict:
            corresDict[oldIndex] = [newIndex]
            newIndex += 1
        res[e] = corresDict[oldIndex]
    return res
