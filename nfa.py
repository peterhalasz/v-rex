from dfa import Dfa

from plotter import plot_automaton
from printer import print_automaton

""" Non-deterministic Finite Automaton.

A simple implementation of an nfa.
"""


class Nfa:
    def __init__(self, transition_function, starting_state, final_states):
        # (state, input symbol) -> next states
        self.transition_function = transition_function

        self.starting_state = starting_state

        # A finite set of accepting states.
        self.final_states = final_states

    def plot(self):
        plot_automaton(self.transition_function, self.starting_state, self.final_states)

    def print(self):
        print_automaton(
            self.transition_function, self.starting_state, self.final_states
        )

    def _get_dfa_accepting_states(self, dfa_transition_function):
        dfa_accepting_states = set()

        reachable_states = [
            next_states for _, next_states in dfa_transition_function.items()
        ]

        # Creating the dfa's accepting states
        for state in reachable_states:
            if state.intersection(self.final_states):
                dfa_accepting_states.add(",".join(sorted(state)))

        return dfa_accepting_states

    def _delete_unreachable_transitions(self, dfa_transition_function, starting_state):
        # Collect all nodes that are an end of a non-self transition
        reachable_nodes = [
            end_state
            for transition, end_state in dfa_transition_function.items()
            if transition[0] != end_state
        ]

        result = {}

        for transition in dfa_transition_function:
            if transition[0] == {starting_state} or transition[0] in reachable_nodes:
                result[transition] = dfa_transition_function[transition]

        return result

    def _construct_dfa_transition_function(self, dfa_transition_function):
        input_symbols = ["0", "1"]

        # Get all states with an incoming edge
        reachable_states = [
            end_states for _, end_states in self.transition_function.items()
        ]

        for end_states in reachable_states:
            for input_symbol in input_symbols:

                combined_next_states = set()

                # Iterate over all states of the nfa
                # Collect all nfa reachable states from that state
                # This nfa state can include multiple dfa states
                for state in end_states:
                    if (state, input_symbol) in self.transition_function:
                        nfa_next_states = self.transition_function[
                            (state, input_symbol)
                        ]
                        combined_next_states.update(nfa_next_states)

                if combined_next_states:
                    dfa_transition_function[
                        (frozenset(end_states), input_symbol)
                    ] = combined_next_states

                    if (
                        combined_next_states != end_states
                        and combined_next_states not in reachable_states
                    ):
                        reachable_states.append(combined_next_states)

    def _format_dfa_transition_function(self, dfa_transition_function):
        formatted_dfa_transition_function = {}

        for key, next_states in dfa_transition_function.items():
            dfa_state, input_symbol = key
            formatted_dfa_transition_function[
                ",".join(sorted(dfa_state)), input_symbol
            ] = ",".join(sorted(next_states))

        return formatted_dfa_transition_function

    def convert_to_dfa(self):
        """Converts the nfa to a dfa.

        Returns:
            The dfa converted from the nfa.
        """
        # Initialize the dfa transition function
        dfa_transition_function = {
            (frozenset([key[0]]), key[1]): next_states
            for key, next_states in self.transition_function.items()
        }

        self._construct_dfa_transition_function(dfa_transition_function)

        dfa_transition_function = self._delete_unreachable_transitions(
            dfa_transition_function, self.starting_state
        )

        formatted_dfa_transition_function = self._format_dfa_transition_function(
            dfa_transition_function
        )

        dfa = Dfa(
            transition_function=formatted_dfa_transition_function,
            starting_state=self.starting_state,
            final_states=self._get_dfa_accepting_states(dfa_transition_function),
        )

        return dfa
