from plotter import plot_automaton
from utils import validate_automaton, validate_symbols

""" Epsilon Non-deterministic Finite Automaton.

A simple implementation of an e-nfa.
"""
class ENfa():
    def __init__(self, states, input_symbols, transition_function, starting_state, final_states):
        # A finite set of states. Usually denoted by Q.
        self.states = states

        # A finite set of input symbols. Usually denoted by epsilon.
        self.input_symbols = input_symbols

        # Transition function. Usually denoted by delta.
        # Here implemented as a tuple to set of strings dict.
        # (state, input symbol) -> next states
        self.transition_function = transition_function

        # Start state. Usually denoted by q0.
        self.starting_state = starting_state

        # A finite set of accepting / final states. Usually denoted by F.
        # F has to be a subset of Q.
        self.final_states = final_states

    def validate_automaton(self):
        if not validate_automaton(self.input_symbols, self.states, self.starting_state, self.final_states, self.transition_function):
            print("Incorrect automaton")
            return False
        return True

    def plot(self):
        plot_automaton(self.transition_function, self.starting_state, self.final_states)

    def is_string_accepted(self, input_string):
        if not validate_symbols(self.input_symbols, input_string):
            print("Input string is not part of the input symbols")
            return False
        print("Not implemented")
        return False

if __name__ == "__main__":
    states = {"A", "B", "C", "D"}
    input_symbols = {"0", "1", "ε"}
    transition_function = {
        ("A", "0"): {"A", "B"},
        ("A", "1"): {"B"},
        ("B", "0"): {"C"},
        ("B", "1"): {"A", "C"},
        ("C", "ε"): {"D"},
    }
    starting_state = "A"
    final_states = {"D"}

    # The string the dfa will process.
    test_input_string = "0000011001"

    e_nfa = ENfa(states, input_symbols, transition_function, starting_state, final_states)

    e_nfa.plot()