import regex as r
import regextreeToAutomaton as rta
import determinization as deter
import printer as printer
import sys

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Error : Not enough arguments")
        sys.exit(1)

    inputRegex = sys.argv[1]
    fileName = sys.argv[2]

    viewMode = False

    if len(sys.argv) > 3:
        if sys.argv[3] == '-v' or sys.argv[3] == '-view':
            viewMode = True
        else:
            print("Error : invalid option -- " + "'" + sys.argv[3] + "'")
            sys.exit(1)

    try:
        file = open(fileName, 'r')
    except IOError:
        print("the file " + "'" + fileName + "'" + " doesn't exist")
        sys.exit(1)

    # inputRegex = input("Entrez une String ou une Regex:\n")

    ast = r.preparse(inputRegex)

    if ast.isWord():
        printer.egrep(0, file, ast)

    else:
        automatonNDFA = rta.toAutomaton(ast)
        automatonDFA = deter.deter(automatonNDFA)
        automatonDFA.mini()
        printer.egrep(1, file, automatonDFA)

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
