"""Automaton implementation."""
from typing import Collection

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
        
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        pass




    def minimize(self, set_to_complete):
        group_number = [1]*len(set_to_complete)
        check = True
        startingIndex = 0
        for index in range(len(set_to_complete)):
            if set_to_complete[index].is_final:
                group_number[index] = 0
            if set_to_complete[index] == self.initial_state:
                startingIndex = index
        i, j, counter = 1, 1, 1
        while check:
            check = False
            i = 1
            j = counter
            old_groups = []
            for e in group_number:
                old_groups.append(e)
            while i <= j:
                for index in range(len(set_to_complete)):
                    if group_number[index] == i:
                        for index2 in range(index +1 , len(set_to_complete)):
                            if group_number[index2] == i:
                                
                                if not self.check_stados_equivlentes(set_to_complete[index], set_to_complete[index2], set_to_complete, old_groups):
                                    group_number[index2] += 1
                                    if group_number[index2] > j:
                                        counter += 1
                                        check = True
                i += 1
        new_states = []
        new_transitions = []
        print(group_number)
        for s in range(j+1):
            if s == 0:
                new_states.append(State(name=str(s),is_final=True))
            else:
                new_states.append(State(name=str(s),is_final=False))
        transtion_matrix = self.compute_tranistions(set_to_complete, group_number,j)
        print(transtion_matrix)
        for state in new_states:
            for symbol in self.symbols:
                new_transitions.append(Transition(state,symbol,new_states[transtion_matrix[new_states.index(state)][self.symbols.index(symbol)]]))
        self.states = new_states
        self.transitions = new_transitions
        self.initial_state = new_states[group_number[startingIndex]]
    def compute_tranistions(self, set_states, groups, j):
        transitions = []
        for i in range(j+1):
            line = []
            for s in range(len(self.symbols)):
                state = set_states[groups.index(i)]
                for transition in self.transitions:
                    if transition.initial_state == state and transition.symbol == self.symbols[s]:
                        line.append(groups[set_states.index(transition.final_state)])
                        break
            transitions.append(line)
        return transitions
        
    def check_stados_equivlentes(self, s1, s2, set_status, groups):
        l1 = [0]*len(self.symbols)
        l2 = [0]*len(self.symbols)
        for i in range(len(self.symbols)):
            for t in self.transitions:
                if t.initial_state == s1 and t.symbol == self.symbols[i]:
                    l1[i] = groups[set_status.index(t.final_state)]
                if t.initial_state == s2 and t.symbol == self.symbols[i]:
                    l2[i] = groups[set_status.index(t.final_state)]  
        return l1 == l2
                                
    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        self.minimize(list(self.states))

    def _complete_lambdas(self, set_to_complete) -> None:
        """Tdos los estados alacanzables mediante transiciones lambda"""
        check = False
        for transition in self.transitions: 
            if transition.symbol == None and transition.initial_state in set_to_complete and not transition.final_state in set_to_complete :
                set_to_complete.add(transition.final_state)
                check = True
        if check:
            self._complete_lambdas(set_to_complete)
