"""Automaton implementation."""
from typing import Collection
from automaton_evaluator import FiniteAutomatonEvaluator

from interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def any_final(
    states: Collection[State],
) -> bool:
    for state in states:
        if state.is_final:
            return True
    return False

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

        # CREATE STATE

        # CREATE TRANSITION
    


    def AFD_state (
        state_counter: int,
        AFD_states: Collection[State],
        reached_states: Collection[State],
    ) -> State:

        # Order !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Make new name
        new_state_name = ""
        for state in reached_states:
            new_state_name += state.name

        # Check existance
        for AFD_state in AFD_states:
            if AFD_state.name == new_state_name:
                return AFD_state
        
        state_counter += 1
        return State(name=new_state_name, is_final=any_final(reached_states))

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
        self._complete_lambdas(set(temp_states))
        
        # Init State name
        aux_name = ""
        for state in temp_states:
            aux_name += state.name

        # Save states from ADF init state in dict with id 0
        all_temp_states[num_states_AFD] = temp_states 
        temp_states = []

        # Create AFD init state
        initial_state_AFD = State(name=aux_name, is_final=False) # create state
        AFD_states.append(initial_state_AFD)
        current_state_AFD = initial_state_AFD

        num_states_AFD += 1

        i = 0    
        reachable_states_exist = 0
        # For every new state
        while i != num_states_AFD:
            # For every symbol in AFN
            for symbol in self.symbols: 
                if symbol == None:
                    continue
                
                for transition_AFN in self.transitions:
                    # If there is a reachable state
                    if transition_AFN.symbol == symbol:
                        # From AFD new state
                        for state in all_temp_states[i]:
                            if transition_AFN.init_state == state:
                                reachable_states_exist = 1
                                temp_states.append(state)
                                self._complete_lambdas(set(temp_states))

            if reachable_states_exist:
                prev = num_states_AFD
                s = AFD_states(num_states_AFD, AFD_states, temp_states)
                
                # If new state is created
                if prev < num_states_AFD:
                    # Save states from ADF init state in dict
                    all_temp_states[prev] = temp_states 
                
                temp_states = []
                AFD_transitions.append(Transition(initil_state=current_state_AFD, symbol=symbol, final_state=s))

            current_state_AFD = all_temp_states[i]    
            i += 1

        AFD_symbols = ""
        for t in AFD_transitions:
            AFD_symbols += t.symbol
        
        AFD_symbols = list(dict.fromkeys(AFD_symbols))

        # Create AFD
        return FiniteAutomaton(initial_state=initial_state_AFD, states=AFD_states, symbols=AFD_symbols, transitions=AFD_transitions)


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")

