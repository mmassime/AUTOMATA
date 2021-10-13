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
        self.state_counter=0
        states = list(automaton1.states + automaton2.states)
        transitions = list(automaton1.transitions + automaton2.transitions)
        symbols = automaton1.symbols + automaton2.symbols
        initial = State(name="q"+str(self.state_counter),is_final=False)
        states.append(initial)
        self.state_counter+=1
        for state in states:
            if state != initial:
                for transition in transitions:
                    if transition.initial_state == state:
                        transition.initial_state.name = "q"+str(self.state_counter)
                    if transition.final_state == state:
                        transition.final_state.name = "q"+str(self.state_counter)
                state.name = "q"+str(self.state_counter)
                self.state_counter +=1
        transitions.append(Transition(initial_state = initial, symbol=None, final_state=automaton1.initial_state))
        transitions.append(Transition(initial_state = initial, symbol=None, final_state=automaton2.initial_state))
        final = State(name="f"+str(self.state_counter), is_final=True)
        self.state_counter+=1
        states.append(final)
        for state in states:
            if state.is_final and state != final:
                state.is_final = False
                transitions.append(Transition(initial_state = state, symbol=None, final_state=final))

        return FiniteAutomaton(initial_state=initial,states=states,symbols=symbols,transitions=transitions)
    
    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        self.state_counter=0
        symbols = automaton1.symbols + automaton2.symbols
        transitions = list(automaton1.transitions + automaton2.transitions)
        final = State(name="final", is_final=True)
        for state in automaton1.states:
            if state.is_final:
                state.is_final = False
                transitions.append(Transition(initial_state = state, symbol=None, final_state=automaton2.initial_state))
        for state in automaton2.states:
            if state.is_final:
                state.is_final = False
                transitions.append(Transition(initial_state = state, symbol=None, final_state=final))
        states = list(automaton1.states + automaton2.states)
        states.append(final)
        initial = State(name="q"+str(self.state_counter),is_final=False)
        self.state_counter+=1
        states.append(initial)
        for state in states:
            if state != initial:
                for transition in transitions:
                    if transition.initial_state == state:
                        transition.initial_state.name = "q"+str(self.state_counter)
                    if transition.final_state == state:
                        transition.final_state.name = "q"+str(self.state_counter)
                state.name = "q"+str(self.state_counter)
                self.state_counter +=1
        final.name="f"+str(self.state_counter)
        self.state_counter += 1
        transitions.append(Transition(initial_state = initial, symbol=None, final_state=automaton1.initial_state))
        return FiniteAutomaton(initial_state=initial,states=states,symbols=symbols,transitions=transitions)