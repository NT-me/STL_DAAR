from typing import List
from time import sleep


class NDFA:
    def __init__(self, tTab=[], eTab=[]) -> None:
        self.tTab = tTab
        self.eTab = eTab

    def __str__(self) -> str:
        res = "Initial state : 0\nFinal State :" + str(len(self.tTab)-1) + "\n"
        for i in range(0, len(self.eTab)):
            for s in self.eTab[i]:
                res += "  " + str(i) + " -- epsilon --> " + str(s) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + \
                                      " --> " + str(self.tTab[i][col]) + "\n"

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
            f.write("leg1((Init))\n")
            f.write("leg2[[Final]]\n")
            f.write("leg3[Transit state]\n")

            f.write("{0}[[{0}]]\n".format(len(self.tTab) - 1))

            f.write("{0}(({0}))\n".format(0))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col)
                                + "| " + str(self.tTab[i][col]) + "\n")

            for i in range(0, len(self.eTab)):
                for s in self.eTab[i]:
                    f.write("  " + str(i) + " --> |"
                            + 'epsilon' + "| " + str(s) + "\n")


class DFA:
    def __init__(self, initialState: int = 0, finalStates: List = [], tTab=[]) -> None:
        self.initialState = initialState
        self.finalStates = finalStates
        self.tTab = tTab
        self.sink = None
        self.lang = None

    def __str__(self) -> str:
        res = "Initial state : " + \
            str(self.initialState) + "\nFinal States :" + \
            str(self.finalStates) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + \
                                      " --> " + str(self.tTab[i][col]) + "\n"
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

    def getStates(self):
        """
        return dict
        ["noFinal"] = no final states
        ["final"] = final states
        """
        states = [x for x in range(0, len(self.tTab))
                  if x not in self.finalStates]
        res = dict()
        res["noFinal"] = states
        res["final"] = self.finalStates
        return res

    def getLang(self):
        if not self.lang:
            res = []
            for i in range(0, len(self.tTab)):
                tmp = [self.tTab[i].index(ele)
                       for ele in self.tTab[i] if ele != -1]
                if tmp:
                    res += [chr(ele) for ele in tmp if chr(ele) not in res]
            self.lang = res
            return res
        else:
            return self.lang

    def completeAutomaton(self):
        needed = False

        s = self.getStates()
        nestS = s["noFinal"]
        nestS += s["final"]

        for char in self.getLang():
            asciichar = ord(char)
            for i in nestS:
                if self.tTab[i][asciichar] == -1:
                    needed = True
                    break

        if not self.sink and needed:
            sink = len(self.tTab)
            self.sink = sink
            self.tTab.append([-1 for i in range(0, 256)])

            for char in self.getLang():
                asciichar = ord(char)
                for i in range(0, len(self.tTab)):
                    if self.tTab[i][asciichar] == -1:
                        self.tTab[i][asciichar] = sink

    def goToMermaid(self, fn=""):
        with open("DFA"+fn+".txt", "w") as f:
            f.write("graph TD\n")
            f.write("leg0[(Init & Final)]\n")
            f.write("leg1((Init))\n")
            f.write("leg2[[Final]]\n")
            f.write("leg3[Transit state]\n")

            for fs in self.finalStates:
                if fs == self.initialState:
                    f.write("{0}[({0})]\n".format(fs))
                elif fs != self.initialState:
                    f.write("{0}[[{0}]]\n".format(fs))

            if self.initialState not in self.finalStates:
                f.write("{0}(({0}))\n".format(self.initialState))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col)
                                + "| " + str(self.tTab[i][col]) + "\n")

    def getNextState(self, parentId: int):
        row = self.tTab[parentId]
        res = []

        for i in range(0, len(row)):
            if row[i] != -1:
                res.append(row[i])
        return res

    def getTransitionAtState(self, parentId):
        row = self.tTab[parentId]
        res = []
        for i in self.getLang():
            if row[ord(i)] != -1:
                res.append(i)
        return res

    def checkSubString(self, str="") -> bool:
        if str == "":
            return False
        strLen = len(str)
        currentState = self.initialState
        wordStart = -1

        for i in range(0, strLen):
            strchar = str[i]
            if ord(strchar) <= len(self.tTab[currentState]):
                # if strchar in self.getTransitionAtState(currentState):
                if self.tTab[currentState][ord(strchar)] != -1:
                    # Si la lettre est dans les transisition de l'état
                    if wordStart == -1:
                        wordStart = i
                    currentState = self.tTab[currentState][ord(strchar)]

                elif currentState in self.finalStates:
                    # Si on est dans un état final
                    if wordStart == -1:
                        # return False
                        currentState = self.initialState
                    else:
                        return True, wordStart, i, str[wordStart:i]

                # elif strchar not in self.getTransitionAtState(currentState):
                elif self.tTab[currentState][ord(strchar)] == -1:
                    # Si on est pas dans un état final et que la lettre n'a pas de
                    # transition
                    currentState = self.initialState
                    wordStart = -1

        if currentState in self.finalStates and wordStart != -1:
            # print(str)
            return True, wordStart, i+1, str[wordStart:i+1]
        else:
            return False

        strLen = len(str)

    def checkString(self, inputString=""):
        res = []
        ret = True

        newStart = 0

        iter = 0
        initialLen = len(inputString)
        while ret != False and iter <= initialLen:
            ret = self.checkSubString(inputString)
            iter += 1

            if ret != False:
                res.append((ret[0], ret[1]+newStart, ret[2]+newStart, ret[3]))
                start = ret[1]
                end = ret[2]
                inputString = inputString[end:]
                newStart += end

        if not res or (len(res) == 1 and False in res):
            return []
        else:
            return res

    def getListOfDeadStates(self) -> List:
        res = []

        s = self.getStates()

        nestS = []
        nestS += s["noFinal"]
        nestS += s["final"]

        for state in nestS:
            nbm1 = self.tTab[state].count(-1)
            nbself = self.tTab[state].count(state)

            if (nbm1 + nbself) >= len(self.tTab[state]) and state not in self.finalStates:
                res.append(state)

        return res

    def mini(self):
        self.completeAutomaton()
        s = self.getStates()

        nestS = []
        nestS += s["noFinal"]
        nestS += s["final"]

        descState = dict()
        famID = 0
        for nfs in s["noFinal"]:
            descState[nfs] = [famID]
        famID += 1
        for fs in s["final"]:
            descState[fs] = [famID]

        lastBilan = descState

        flag_continue = True
        i = 0

        # Algo de moore

        while flag_continue:
            i += 1
            for state in nestS:
                # sateFamId = descState[state][0]
                for t in self.getLang():
                    nextState = self.tTab[state][ord(t)]
                    nsFamId = descState[nextState][0]
                    descState[state].append(nsFamId)

            famId = 0
            currentBilan = dict()
            for desc in descState:
                currentBilan[desc] = [famId]
                famId += 1

            for desc in descState:
                current = descState[desc]

                for state in nestS:
                    if state != desc and current == descState[state]:
                        currentBilan[state] = currentBilan[desc]

            if currentBilan == lastBilan:
                flag_continue = False
            else:
                lastBilan = currentBilan


        # Suppression des états morts

        iterSec = 0
        while self.getListOfDeadStates() and iterSec <= len(nestS):
            iterSec += 1

            for deadState in self.getListOfDeadStates():
                del(self.tTab[deadState])
                del(currentBilan[deadState])

                nestS.remove(deadState)
                for state in nestS:
                    for asciichar in self.getLang():
                        if self.tTab[state][ord(asciichar)] == deadState:
                            self.tTab[state][ord(asciichar)] = -1

        # Changement des états finaux
        oldFs = self.finalStates
        newFs = []

        for ofs in oldFs:
            s = currentBilan[ofs][0]
            if s not in newFs:
                newFs.append(s)

        self.finalStates = newFs

        # nouvelle matrice
        matrixCanva = dict()
        for e in currentBilan:
            newStateId = currentBilan[e][0]
            try:
                matrixCanva[newStateId].append(e)
            except KeyError:
                matrixCanva[newStateId] = [e]

        matrixCanvaRes = dict()
        i = 0
        for e in matrixCanva:
            i += 1
            matrixCanvaRes[i] = [e]

        matrixCanva = matrixCanvaRes

        newtTab = [[-1 for i in range(0, 256)] for j in range(0, len(matrixCanva)+1)]

        for state in nestS:
            for asciichar in self.getLang():
                tDest = self.tTab[state][ord(asciichar)]
                if tDest != -1:
                    print(state)
                    newtTab[currentBilan[state][0]][ord(asciichar)] = currentBilan[tDest][0]
        self.tTab = newtTab
