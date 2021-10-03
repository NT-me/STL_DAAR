import unittest
import regex as r
from regextree import RegExTree
import regextreeToAutomaton as rta
import determinization as deter
from automaton import NDFA, DFA

class Test(unittest.TestCase):

    def test_ast(self):
        print("== AST Tests ==\n")

        for i in range(len(self.regex)):
            print("Testing on " + self.regex[i] + " : ")
            self.assertEqual(r.preparse(self.regex[i]), self.ast_results[i], "Not equal")
            print("OK")

        print("\n===============\n")

    def test_regex_to_automaton(self):
        print("\n== NDFA Tests ==\n")

        for i in range(len(self.regex)):
            # print(self.ndfa_results[i])
            # print(rta.toAutomaton(self.ast_results[i]))

            print("Testing on " + str(self.ast_results[i]) + " : ")
            self.assertEqual(rta.toAutomaton(self.ast_results[i]), self.ndfa_results[i])
            print("OK") 

        print("\n================\n")

    def test_determinization(self):
        print("\n== DFA Tests ==\n")

        for i in range(len(self.regex)):
            # print(self.ndfa_results[i])
            # print(deter.deter(self.ndfa_results[i]))
            print("Testing on " + str(self.regex[i]) + " : ")
            self.assertEqual(deter.deter(self.ndfa_results[i]), self.dfa_results[i])
            print("OK")

        print("\n================\n")

    regex = ["ab", "a|b", "a*", "a+", "a|bc*"]

    ''' expected results for AST tests '''
    ast_results = [
        RegExTree('.', [RegExTree('a', []), RegExTree('b', [])]),
        RegExTree('|', [RegExTree('a', []), RegExTree('b', [])]),
        RegExTree('*', [RegExTree('a', [])]),
        RegExTree('+', [RegExTree('a', [])]),
        RegExTree('|', [RegExTree('a', []), RegExTree('.', [RegExTree('b', []), RegExTree('*', [RegExTree('c', [])])])])
    ]
    
    ''' expected results for NDFA tests '''
    ndfa_results = []

    # ab
    a = [[-1 for i in range(256)] for j in range(4)]
    b = [[] for i in range(4)]
    a[0][97] = 1
    a[2][98] = 3
    b[1] = [2]
    ndfa_results.append(NDFA(a, b))

    # a|b
    a = [[-1 for i in range(256)] for j in range(6)]
    b = [[] for i in range(6)]
    a[1][97] = 2
    a[3][98] = 4
    b[0] = [1, 3]
    b[2] = [5]
    b[4] = [5]
    ndfa_results.append(NDFA(a, b))

    # a*
    a = [[-1 for i in range(256)] for j in range(4)]
    b = [[] for i in range(4)]
    print(id(b))
    a[1][97] = 2
    b[0] = [1, 3]
    b[2] = [3, 1]
    ndfa_results.append(NDFA(a, b))

    # a+
    a = a.copy()
    b = b.copy()
    b[0] = [1]
    ndfa_results.append(NDFA(a, b))

    # a|bc*
    a = [[-1 for i in range(256)] for j in range(10)]
    b = [[] for i in range(10)]
    a[1][97] = 2
    a[3][98] = 4
    a[6][99] = 7
    b[0] = [1, 3]
    b[2] = [9]
    b[4] = [5]
    b[5] = [6, 8]
    b[7] = [8, 6]
    b[8] = [9]
    ndfa_results.append(NDFA(a, b))

    ''' expected results for DFA tests'''
    dfa_results = []

    # ab
    a = [[-1 for i in range(256)] for j in range(3)]
    a[0][97] = 1
    a[1][98] = 2
    dfa_results.append(DFA(0, [2], a))

    # a|b
    a = [[-1 for i in range(256)] for j in range(3)]
    a[0][97] = 1
    a[0][98] = 2
    dfa_results.append(DFA(0, [1, 2], a))

    # a*
    a = [[-1 for i in range(256)] for j in range(2)]
    a[0][97] = 1
    a[1][97] = 1
    dfa_results.append(DFA(0, [0, 1], a))

    # a+
    a = a.copy()
    dfa_results.append(DFA(0, [1], a))

    # a|bc*
    a = [[-1 for i in range(256)] for j in range(4)]
    a[0][97] = 1
    a[0][98] = 2
    a[2][99] = 3
    a[3][99] = 3
    dfa_results.append(DFA(0, [1, 2, 3], a))


if __name__ == "__main__":
    unittest.main()