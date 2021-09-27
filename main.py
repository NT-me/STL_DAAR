import regex as r
import regextreeToAutomaton as rta

if __name__ == '__main__':
    inputRegex = input("Entrez une Regex valide:\n")

    print("\n## AST ##\n")
    ast = r.preparse(str(inputRegex))
    print(ast)
    print("\n#########\n")

    print("## Automaton ##\n")
    automaton = rta.toAutomaton(ast)
    print(automaton)
    print("###############\n")