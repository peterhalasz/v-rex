import unittest

from nfa import Nfa

class NfaTest(unittest.TestCase):

    def test_convert_to_dfa_1(self):
        states = {"A", "B", "C"}
        input_symbols = {"0", "1"}
        transition_function = {
            ("A", "0"): {"A", "B"},
            ("A", "1"): {"A"},
            ("B", "1"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(states, input_symbols, transition_function, starting_state, final_states)
        dfa = nfa.convert_to_dfa()

        expected_dfa_tranisition_function = {
            ('A', '0'): 'A,B',
            ('A', '1'): 'A',
            ('A,B', '1'): 'A,C',
            ('A,B', '0'): 'A,B',
            ('A,C', '1'): 'A',
            ('A,C', '0'): 'A,B'
        }

        self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)