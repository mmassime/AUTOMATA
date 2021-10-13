"""Conversion from regex to automata."""
from automaton import (FiniteAutomaton, State, Transition)
from re_parser_interfaces import AbstractREParser
from automaton import State


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:

        states = []        

        i_state = State(name="inicial",is_final=False)
        f_state = State(name="final",is_final=True)

        states.append(i_state)
        states.append(f_state)
        
        a = FiniteAutomaton(i_state, states ,"", [])

        return a

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:       
        states = []

        f_state = State(name="final",is_final=True)

        states.append(f_state)

        a = FiniteAutomaton(f_state, states, "", [])
        
        return a

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        
        states = []
        transitions = []
        symbols = []

        symbols.append(symbol)

        i_state = State(name="q0", is_final=False)
        states.append(i_state)

        f_state = State(name="q1", is_final=True)
        states.append(f_state)

        t = Transition(initial_state=i_state, symbol=symbol, final_state=f_state)
        transitions.append(t)
      
        a = FiniteAutomaton(initial_state=i_state, states=states, symbols=symbols, transitions=transitions);
        
        return a 

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        states = automaton.states
        transitions = automaton.transitions
        symbols = automaton.symbols
        symbols.append(None)

        s1 = State(name="q0", is_final=False)
        s2 = State(name="q1", is_final=False)
        states.append(s1)
        states.append(s2)

        t1 = Transition(initial_state=s1, symbol=None, final_state=s2)
        t2 = Transition(initial_state=s1, symbol=None, final_state=automaton.initial_state)
        transitions.append(t1)
        transitions.append(t2)
        for state in automaton.states: 
            if state.is_final:
                t3 = Transition(initial_state=automaton.initial_state, symbol=None, final_state=state)
                t4 = Transition(initial_state=state, symbol=None, final_state=s2)
                transitions.append(t3)
                transitions.append(t4)
        a = FiniteAutomaton(initial_state=s1, states=states, symbols=symbols, transitions=transitions)
        
        return a

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")
