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

    def __eq__(self, o: object) -> bool:
        if o == None:
            return False
        elif self.eTab != o.eTab:
            return False
        elif self.tTab != o.tTab:
            return False
        else:
            return True
        
    def goToMermaid(self):
        with open("NDFA.txt", "w") as f:
            f.write("graph TD\n")

            f.write("{0}[[{0}]]\n".format(len(self.tTab) - 1))

            f.write("{0}(({0}))\n".format(0))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col) + "| " + str(self.tTab[i][col]) + "\n")

            for i in range(0, len(self.eTab)):
                for s in self.eTab[i]:
                    f.write("  " + str(i) + " --> |" + 'ε' + "| " + str(s) + "\n")


class DFA:
    def __init__(self, initialState: int = 0, finalStates: List = [], tTab=[]) -> None:
        self.initialState = initialState
        self.finalStates = finalStates
        self.tTab = tTab

    def __str__(self) -> str:
        res = "Initial state : " + str(self.initialState) + "\nFinal States :" + str(self.finalStates) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.tTab[i][col]) + "\n"
        return res

    def __eq__(self, o: object) -> bool:
        if o == None:
            return False
        elif self.initialState != o.initialState:
            return False
        elif self.finalStates != o.finalStates:
            return False
        elif self.tTab != o.tTab:
            return False
        else:
            return True

    

    def goToMermaid(self):
        with open("DFA.txt", "w") as f:
            f.write("graph TD\n")

            for fs in self.finalStates:
                f.write("{0}[[{0}]]\n".format(fs))

            f.write("{0}(({0}))\n".format(self.initialState))

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
        currentState = self.initialState
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
                currentState = self.initialState
                wordStart = -1
        if currentState in self.finalStates:
            print(str[wordStart:i])
            if i == 0:
                i = 1
            return True, wordStart, i
        else:
            return False

        strLen = len(str)

    def checkString(self, inputString=""):
        res = []
        ret = True

        newStart = 0
        while ret != False:
            ret = self.checkSubString(inputString)

            if ret != False:
                res.append((ret[0], ret[1]+newStart, ret[2]+newStart))
                start = ret[1]
                end = ret[2]
                inputString = inputString[end:]
                newStart += end
            # print(ret)
        if not res or (len(res) == 1 and False in res):
            return []
        else:
            return res
