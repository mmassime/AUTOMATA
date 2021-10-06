"""Evaluation of automata."""
from typing import Set

from automaton import FiniteAutomaton, State
from interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        new_states = []
        if not symbol in self.automaton.symbols:
            raise ValueError("Unknown symbol")
        for state in self.current_states:
            for transition in self.automaton.transitions:
                if transition.symbol == symbol and transition.initial_state == state:
                    new_states.append(transition.final_state)
        self.current_states = set(new_states)

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        new_states = []
        if not symbol in self.automaton.symbols:
            raise ValueError("Unknown symbol")
        for state in self.current_states:
            for transition in self.automaton.transitions:
                if transition.symbol == symbol and transition.initial_state == state:
                    new_states.append(transition.final_state)
        self.current_states = set(new_states)

    def is_accepting(self) -> bool:
        for state in self.current_states:
            if state.is_final == True:
                return True
        return False
