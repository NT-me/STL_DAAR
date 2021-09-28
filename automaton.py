from typing import List


class NDFA:

    def __init__(self, tTab=[], eTab=[]) -> None:
        self.tTab = tTab
        self.eTab = eTab

    def __str__(self) -> str:
        res = "Initial state : 0\nFinal State :" + str(len(self.tTab)-1) + "\n"
        for i in range(0, len(self.eTab)):
            for s in self.eTab[i]:
                res += "  " + str(i) +" -- epsilon --> " + str(s) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.tTab[i][col]) + "\n"

        return res


class DFA:
    def __init__(self, initialState: int = 0, finalStates: List = [], tTab=[]) -> None:
        self.initalState = initialState
        self.finalStates = finalStates
        self.tTab = tTab

    def __str__(self) -> str:
        res = "Initial state : " + str(self.initalState) + "\nFinal States :" + str(self.finalStates) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.tTab[i][col]) + "\n"
        return res

    def goToMermaid(self):
        with open("DFA.txt", "w") as f:
            f.write("graph TD\n")

            for fs in self.finalStates:
                f.write("{0}[[{0}]]\n".format(fs))

            f.write("{0}(({0}))\n".format(self.initalState))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col) + "| " + str(self.tTab[i][col]) + "\n")

    def getNextState(self, parentId : int):
        row = self.tTab[parentId]
        res = []

        for i in range(0, len(row)):
            if row[i] != -1:
                res.append(row[i])
        return res

    def getTransitionAtState(self, parentId):
        row = self.tTab[parentId]
        res = []
        for i in range(0, len(row)):
            if row[i] != -1:
                res.append(chr(i))
        return res


    def checkSubString(self, str="") -> bool:
        if str == "":
            return False
        strLen = len(str)
        currentState = self.initalState
        wordStart = -1
        for i in range(0, strLen):
            strchar = str[i]
            if strchar in self.getTransitionAtState(currentState):
                # Si la lettre est dans les transisition de l'état
                if wordStart == -1:
                    wordStart = i
                currentState = self.tTab[currentState][ord(strchar)]
            elif currentState in self.finalStates:
                return True, wordStart, i
            elif strchar not in self.getTransitionAtState(currentState):
                currentState = self.initalState
                wordStart = -1
        if currentState in self.finalStates:
            return True, wordStart, i
        else:
            return False

        strLen = len(str)


    def checkString(self, str=""):
        res = []
        ret = True
        while ret != False:
            ret = self.checkSubString(str)

            if ret != False:
                res.append(ret)
                start = ret[1]
                end = ret[2]
                str = str[:start] + str[end:]
        print(str)
        if not res or (len(res) == 1 and False in res):
            return []
        else:
            return res
