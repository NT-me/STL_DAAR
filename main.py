import regex as r
import regextreeToAutomaton as rta
import determinization as deter
import printer as printer
import sys
import time as t


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Error : Not enough arguments")
        sys.exit(1)

    inputRegex = sys.argv[1]
    fileName = sys.argv[2]

    viewMode = False
    timeMode = False

    if len(sys.argv) > 3:
        # if sys.argv[3] == '-v' or sys.argv[3] == '-view':
        if "-v" in sys.argv or "--view" in sys.argv:
            viewMode = True
        if "-t" in sys.argv or "--time" in sys.argv:
            timeMode = True
        else:
            print("Error : invalid option -- " + "'" + sys.argv[3] + "'")
            sys.exit(1)

    try:
        file = open(fileName, 'r')
    except IOError:
        print("the file " + "'" + fileName + "'" + " doesn't exist")
        sys.exit(1)

    # inputRegex = input("Entrez une String ou une Regex:\n")

    if timeMode:
        genStart = t.time()
        timedict = dict()

    ast = r.preparse(inputRegex)

    if timeMode:
        timedict["Parsing : "] = t.time() - genStart

    if ast.isWord():
        printer.egrep(0, file, ast)
        if timeMode:
            timedict["KMP : "] = t.time() - genStart

    else:
        automatonNDFA = rta.toAutomaton(ast)

        if timeMode:
            timedict["AST -> Automaton : "] = t.time() - genStart

        automatonDFA = deter.deter(automatonNDFA)

        if timeMode:
            timedict["Deter : "] = t.time() - genStart

        if viewMode:
            automatonDFA.goToMermaid("deter")
        automatonDFA.mini()

        if timeMode:
            timedict["Mini : "] = t.time() - genStart

        if viewMode:
            automatonDFA.goToMermaid("mini")
        printer.egrep(1, file, automatonDFA)

    if timeMode:
        timedict["Text Matching : "] = t.time() - genStart
        timedict["General : "] = t.time() - genStart
        print("\n== TIME ==\n")
        for et in timedict:
            print("{0} {1}\n".format(et, timedict[et]))

    if viewMode:

        print("\n== AST ==\n")
        print(ast)
        print("\n==========\n")

        if not ast.isWord():
            print("== NDFA ==\n")
            print(automatonNDFA)
            automatonNDFA.goToMermaid()
            print("==========\n")

            print("== DFA ==\n")
            print(automatonDFA)
            automatonDFA.goToMermaid()
