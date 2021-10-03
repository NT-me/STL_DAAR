import regex as r
import regextreeToAutomaton as rta
import determinization as deter

if __name__ == '__main__':
    inputRegex = input("Entrez une Regex valide:\n")

    print("\n== AST ==\n")
    ast = r.preparse(str(inputRegex))
    print(ast)
    print("\n==========\n")

    print("== NDFA ==\n")
    automaton = rta.toAutomaton(ast)
    print(automaton)
    automaton.goToMermaid()
    print("==========\n")

    print("== DFA ==\n")
    automaton = deter.deter(automaton)
    print(automaton)
    automaton.goToMermaid()

    print("== Check Matches ==\n")
    print(automaton.checkString("azzzzzzbccccc"))

    # book = open('./books/46446-0.txt', 'r')

    # i = 0
    # for l in book:
    #     print(automaton.checkString(l))
    #     i += 1
    #     if i >= 56:
    #         break
    print("\n====================\n")
