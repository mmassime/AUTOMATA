"""Evaluation of automata."""
from typing import Set

from automaton import FiniteAutomaton, State
from interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    """        new_states = []
        if not symbol in self.automaton.symbols:
            raise ValueError("Unknown symbol")
        for state in self.current_states:
            for transition in self.automaton.transitions:
                if transition.symbol == symbol and transition.initial_state == state:
                    new_states.append(transition.final_state)
        self.current_states = set(new_states)
        
    """
    
    def process_symbol(self, symbol: str) -> None:
            """Como procesa simbolo de cadena, current state == final state del symbolo"""
            """set of new states"""
            new = []

            if not symbol in self.automaton.symbols:
                        raise ValueError("Symbol not in language")

            for state in self.current_states:
                for transition in self.automaton.transitions:
                    if transition.symbol == symbol and transition.initial_state == state:
                        new.append(transition.final_state)
            
            self._complete_lambdas(set(new))

            self.current_states = set(new)

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """Tdos los estados alacanzables mediante transiciones lambda"""
        for transition in self.automaton.transitions: 
            if transition.symbol == None:
                """if transition.final_state in set_to_complete:
                    continue"""
                set_to_complete.add(transition.final_state)
                

    def is_accepting(self) -> bool:
        for state in self.current_states:
            if state.is_final:
                return True
        return False