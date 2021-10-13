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
        raise NotImplementedError("This method must be implemented.")

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        raise NotImplementedError("This method must be implemented.")

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
