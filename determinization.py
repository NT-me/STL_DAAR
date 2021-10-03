from enum import auto
from automaton import DFA as Automaton

def deter(automaton: Automaton) -> Automaton:

    res = Automaton()

    transitions = automaton.tTab
    e_transitions = automaton.eTab

    states = [[0]]
    states[0] = appendETransitions(states[0], [0], e_transitions)
    print(states[0])
    # states[0].extend(e_transitions[0])
    states[0].sort()

    for s in states[0]:
        if s == len(transitions) - 1:
            res.finalStates.append(0)
            break

    res.initialState = 0

    tTab = []

    i = 0
    while i < len(states):
        # print(tTab)
        tTab.append([-1 for j in range(0, len(transitions[0]))])

        state = states[i]
        # print(state)

        for col in range(0, len(transitions[i])):
            newState = []
            final = False
            
            for s in state:
                if transitions[s][col] != -1:
                    newState.append(transitions[s][col])
        
                    newState = appendETransitions(newState, [transitions[s][col]], e_transitions)

                    for k in newState:
                        if k == len(transitions) - 1:
                            final = True
                            break

            if len(newState) > 0:
                newState.sort()

                if newState not in states:
                    states.append(newState)
                    tTab[i][col] = len(states) - 1
                else:
                    ind = states.index(newState)
                    tTab[i][col] = ind

                if final and (len(states)-1) not in res.finalStates:
                    res.finalStates.append(len(states) - 1)

        i += 1
        # print(states)

    res.tTab = tTab
    return res

def appendETransitions(newState, next, eTab):
    for n in next:
        newState.extend(eTab[n])
        newState = appendETransitions(newState, eTab[n], eTab)
    
    return newState