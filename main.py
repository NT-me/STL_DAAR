import regex as r
import regextreeToAutomaton as rta
import determinization as deter
import printer as printer
import sys

if __name__ == '__main__':
    print(sys.argv)

    if len(sys.argv) < 3:
        print("Error : Not enough arguments")
        sys.exit(1)

    inputRegex = sys.argv[1]
    fileName = sys.argv[2]

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

        # print(automaton.checkString("azzzzzzbccczzezbcc"))

    # book = open('./books/46446-0.txt', 'r')
    #
    # i = 0
    # for l in book:
    #     print(automaton.checkString(l))
    #     i += 1
    #     if i >= 56:
    #         break
    # print("\n====================\n")
