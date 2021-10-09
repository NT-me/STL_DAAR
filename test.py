import unittest
unittest.TestLoader.sortTestMethodsUsing = None

import regex as r
from regextree import RegExTree
import regextreeToAutomaton as rta
import determinization as deter
from automaton import NDFA, DFA
import kmp

class Test(unittest.TestCase):

    #################
    ## REGEX TESTS ##
    #################

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

    def test_minimization(self):
        print("\n== Minimization Tests ==\n")

        for i in range(len(self.regex)):
            self.dfa_results[i].mini()

            print(self.dfa_results[i])
            print(self.min_results[i])
            
            print("Testing on " + str(self.regex[i]) + " : ")
            self.assertEqual(self.dfa_results[i], self.min_results[i])
            print("OK")

        print("\n========================\n")

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

    ''' expected results for minimization '''
    min_results = []

    # ab
    a = [[-1 for i in range(256)] for j in range(3)]
    a[0][97] = 1
    a[1][98] = 2
    min_results.append(DFA(0, [2], a))

    # a|b
    a = [[-1 for i in range(256)] for j in range(3)]
    a[0][97] = 1
    a[0][98] = 2
    min_results.append(DFA(0, [1, 2], a))

    # a*
    a = [[-1 for i in range(256)] for j in range(2)]
    a[0][97] = 0
    min_results.append(DFA(0, [0], a))

    # a+
    a = a.copy()
    min_results.append(DFA(0, [1], a))

    # a|bc*
    a = [[-1 for i in range(256)] for j in range(4)]
    a[0][97] = 1
    a[0][98] = 2
    a[2][99] = 2
    min_results.append(DFA(0, [1, 2, 3], a))

    # a*
    min_results[2].tTab[0][97] = 0
    min_results[2].tTab[1][97] = -1
    min_results[2].finalStates = [0]

    min_results[4].tTab[2][99] = 2
    min_results[4].tTab[3][99] = -1

    ###############
    ## KMP TESTS ##
    ###############

    def test_precalcul_kmp(self):
        print("\n== PRECALCUL KMP ==\n")

        for i in range(len(self.words)):
            # print(self.ndfa_results[i])
            # print(deter.deter(self.ndfa_results[i]))
            
            print("Testing on " + str(self.words[i]) + " : ")
            self.assertEqual(kmp.precalcul(self.words[i]), self.precalcul_kmp_results[i])
            print("OK")

        print("\n===================\n")

    def test_kmp(self):
        print("\n== KMP ==\n")

        print("Testing on : " + self.text + "\n")

        for i in range(len(self.kmp_words)):
            # print(self.ndfa_results[i])
            # print(deter.deter(self.ndfa_results[i]))
            
            print("Searching for " + str(self.kmp_words[i]) + " : ")
            self.assertEqual(kmp.kmp(self.kmp_words[i], self.text), self.kmp_results[i])
            print("OK")

        print("\n=========\n")

    words = ["AAAA", "ABCDE", "AABAACAABAA", "AAACAAAAAC", "AAABAAA", "mamamia", "chicha", "Sargon"]
    text = "lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin at condimentum lacus, nec finibus orci. Nunc in lectus condimentum, egestas risus a, semper erat. Donec vitae lorem id metus venenatis aliquet ac in nisl. Donec lacinia nibh eget leo mattis tincidunt. Nulla nibh lacus, condimentum eu est non, dictum euismod libero. Aenean tincidunt arcu mauris, a blandit lectus volutpat vel. Curabitur bibendum mi consectetur nulla venenatis, eget ultrices diam iaculis. Maecenas condimentum, tortor sit amet vestibulum semper, turpis velit rhoncus mi, nec gravida risus neque vitae urna. Quisque tincidunt dignissim est, eget dictum sem congue ac. Phasellus vestibulum aliquam lorem"

    ''' expected results for precalcul_kmp '''

    precalcul_kmp_results = [
        [0, 1, 2, 3],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5],
        [0, 1, 2, 0, 1, 2, 3, 3, 4, 4],
        [0, 1, 2, 0, 1, 2, 3],
        [0, 0, 1, 2, 3, 0, 1],
        [0, 0, 0, 1, 2, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    ''' expected results for kmp '''

    kmp_words = ["lorem", "Donec", "mi", "est", "um"]

    kmp_results = [
        [[0, 5], [173, 178], [676, 681]],
        [[161, 166], [218, 223]],
        [[409, 411], [547, 549]],
        [[133, 136], [297, 300], [508, 511], [615, 618], [658, 661]],
        [[9, 11], [75, 77], [127, 129], [291, 293], [310, 312], [406, 408], [487, 489], [515, 517], [629, 631], [665, 667]]
    ]


if __name__ == "__main__":
    unittest.main()