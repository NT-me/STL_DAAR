class Automaton:

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