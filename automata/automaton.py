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

        AFD_states = []
        AFD_transitions = []
        num_states_AFD = 0

        all_temp_states = {} # dict of lists
        temp_states = []

        # AFN Initial State
        temp_states.append(self.initial_state)

        # States after initial from lambda transition
        for transition in self.transitions: 
            if transition.symbol == None or transition.symbol == "":
                if transition.initial_state in temp_states and not transition.final_state in temp_states :
                    temp_states.append(transition.final_state)

        # Init State name
        aux_name = ""
        for state in temp_states:
            aux_name += state.name
    
        # Save states from ADF init state in dict with id 0
        all_temp_states[num_states_AFD] = temp_states 

        # Create AFD init state
        initial_state_AFD = State(name=aux_name, is_final=any_final(temp_states)) # create state
        AFD_states.append(initial_state_AFD)
        temp_states = []

        num_states_AFD += 1

        # Sumidero
        empty = State(name="empty", is_final=False)
        for symbol in self.symbols:
            AFD_transitions.append(Transition(initial_state=empty, symbol=symbol, final_state=empty))

        i = 0
        reachable_states_exist = 0
        # For every new state
        while i != num_states_AFD:
            # For every symbol in AFN
            for symbol in self.symbols: 
                if symbol == None:
                    continue

                # From AFD new state
                for state in all_temp_states[i]:
                    for transition_AFN in self.transitions:
                        # If there is a reachable state
                        if transition_AFN.symbol == symbol:
                            if transition_AFN.initial_state == state:
                                reachable_states_exist = 1
                                temp_states.append(transition_AFN.final_state)
                                # States after from lambda transition
                                for transition in self.transitions: 
                                    if transition.symbol == None or transition.symbol == "":
                                        if transition.initial_state in temp_states and not transition.final_state in temp_states :
                                            temp_states.append(transition.final_state)

                if not temp_states:
                    # Sumidero
                    AFD_transitions.append(Transition(initial_state=AFD_states[i], symbol=symbol, final_state=empty))
    
                if reachable_states_exist:
                    prev = num_states_AFD

                    #Create state 
                    new_state_name = ""
                    for state in temp_states:
                        new_state_name += state.name

                    new_state = State(name=new_state_name, is_final=any_final(temp_states))

                    # Check existance
                    exists = False
                    for AFD_state in AFD_states:
                        if AFD_state == new_state:
                            exists = True
                            new_state = AFD_state
                    
                    if not exists:
                        AFD_states.append(new_state)
                        num_states_AFD += 1

                    # If new state is created
                    if prev < num_states_AFD:
                        # Save states from ADF init state in dict
                        all_temp_states[prev] = temp_states

                    temp_states = []
                    AFD_transitions.append(Transition(initial_state=AFD_states[i], symbol=symbol, final_state=new_state))
                    reachable_states_exist = 0   
            i += 1
        
        # Order State Name Correctly
        for state in AFD_states:
            state.name = order_name(state.name)

        # Order for transition states
        for t in AFD_transitions:
            t.initial_state.name = order_name(t.initial_state.name)
        
        for t in AFD_transitions:
            t.final_state.name = order_name(t.final_state.name)

        AFD_states.append(empty) #add empty

        # Create AFD
        return FiniteAutomaton(initial_state=initial_state_AFD, states=AFD_states, symbols=self.symbols, transitions=AFD_transitions)

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
        for s in range(j+1):
            if s == 0:
                new_states.append(State(name=str(s),is_final=True))
            else:
                new_states.append(State(name=str(s),is_final=False))
        transtion_matrix = self.compute_tranistions(set_to_complete, group_number,j)
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
    def EliminateInaccessible(self):
        visited = [False]*(len(self.states))
        queue = []
        newState  =[]
        queue.append(self.initial_state)
        visited[self.states.index(self.initial_state)] = True
        while queue:
            s = queue.pop(0)
            newState.append(s)
            for t in self.transitions:
                if t.initial_state == s:
                    if visited[self.states.index(t.final_state)] == False:
                        queue.append(t.final_state)
                        visited[self.states.index(t.final_state)] = True
        
        self.states = newState       
                                          
    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        self.EliminateInaccessible()
        self.minimize(list(self.states))
        
        
def any_final(
    states: Collection[State],
) -> bool:
    for state in states:
        if state.is_final:
            return True
    return False

def order_name(
    name : str,
) -> str:
    a_string = name
    
    unsorted_characters = a_string.split("q")
    sorted_characters = sorted(unsorted_characters)
    
    a_string = ""
    for i in sorted_characters:
        a_string += i
        a_string += "q"

    a_string = a_string[:-1]
    
    return a_string
