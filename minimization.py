from enum import auto
from automaton import DFA as Automaton

def min(automaton: Automaton) -> Automaton:

    res = Automaton()

    transitions = automaton.tTab
    e_transitions = automaton.eTab

    states = [[0]]
    states[0].extend(e_transitions[0])
    states[0].sort()

    res.initalState = 0

    tTab = []

    i = 0
    while i < len(states):
        # print(tTab)
        tTab.append([-1 for j in range(0, len(transitions[0]))])

        state = states[i]
        print(state)

        for col in range(0, len(transitions[i])):
            newState = []
            final = False
            
            for s in state:
                if transitions[s][col] != -1:
                    newState.append(transitions[s][col])
                    newState.extend(e_transitions[transitions[s][col]])

                    if s == len(transitions) - 1:
                        final = True

            if len(newState) > 0:
                newState.sort()

                if newState not in states:
                    states.append(newState)
                    tTab[i][col] = len(states) - 1
                else:
                    ind = states.index(newState)
                    tTab[i][col] = ind

                if final:
                    res.finalStates.append(len(states) - 1)

        i += 1

    res.tTab = tTab
    return res