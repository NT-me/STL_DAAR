import regex as r
import regextreeToAutomaton as rta
import determinization as deter
import kmp as kmp

if __name__ == '__main__':
    inputRegex = input("Entrez une Regex valide:\n")

    print("\n== AST ==\n")
    ast = r.preparse(str(inputRegex))
    print(ast)
    print("\n==========\n")

    if ast.isWord():
        print("KMP")
        word = ast.toWord() 
        print(word)

        book = open('./books/46446-0.txt', 'r')

        i = 0
        for l in book:
            # print(kmp.kmp(word, l))
            matches = kmp.kmp(word, l)
            for m in matches:
                print("Match found on line " + str(i) + " : " + l[m[0]:m[1]+1])
            i += 1
            if i >= 56:
                break


    else:

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
        print(automaton.checkString("azzzzzzbccczzezbcc"))

    # book = open('./books/46446-0.txt', 'r')
    #
    # i = 0
    # for l in book:
    #     print(automaton.checkString(l))
    #     i += 1
    #     if i >= 56:
    #         break
    # print("\n====================\n")
