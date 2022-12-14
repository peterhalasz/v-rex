import unittest

from nfa import Nfa


class NfaTest(unittest.TestCase):
    def test_convert_to_dfa_1(self):
        transition_function = {
            ("A", "0"): {"A", "B"},
            ("A", "1"): {"A"},
            ("B", "1"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(transition_function, starting_state, final_states)
        dfa = nfa.convert_to_dfa()

        expected_dfa_tranisition_function = {
            ("A", "0"): "A,B",
            ("A", "1"): "A",
            ("A,B", "1"): "A,C",
            ("A,B", "0"): "A,B",
            ("A,C", "1"): "A",
            ("A,C", "0"): "A,B",
        }

        self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)

    def test_convert_to_dfa_2(self):
        transition_function = {
            ("A", "0"): {"A"},
            ("A", "1"): {"B"},
            ("B", "0"): {"B", "C"},
            ("B", "1"): {"B"},
            ("C", "0"): {"C"},
            ("C", "1"): {"B", "C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(transition_function, starting_state, final_states)
        dfa = nfa.convert_to_dfa()

        expected_dfa_tranisition_function = {
            ("A", "0"): "A",
            ("A", "1"): "B",
            ("B", "1"): "B",
            ("B", "0"): "B,C",
            ("B,C", "0"): "B,C",
            ("B,C", "1"): "B,C",
        }

        self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)

    # TODO: Make this work. Bug when nfa-dfa and starting state changes.
    # def test_convert_to_dfa_3(self):
    #    transition_function = {
    #        ("A", "0"): {"A", "B"},
    #        ("A", "1"): {"A", "B"},
    #    }
    #    starting_state = "A"
    #    final_states = {"B"}

    #    nfa = Nfa(transition_function, starting_state, final_states)
    #    dfa = nfa.convert_to_dfa()

    #    expected_dfa_tranisition_function = {
    #        ('A,B', '0'): 'A,B',
    #        ('A,B', '1'): 'A,B',
    #    }

    #    self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)

    def test_convert_to_dfa_4(self):
        transition_function = {
            ("A", "0"): {"A"},
            ("A", "1"): {"A", "B"},
            ("B", "1"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(transition_function, starting_state, final_states)
        dfa = nfa.convert_to_dfa()

        expected_dfa_tranisition_function = {
            ("A", "0"): "A",
            ("A", "1"): "A,B",
            ("A,B", "0"): "A",
            ("A,B", "1"): "A,B,C",
            ("A,B,C", "0"): "A",
            ("A,B,C", "1"): "A,B,C",
        }

        self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)

    def test_convert_to_dfa_5(self):
        transition_function = {
            ("A", "0"): {"B"},
        }
        starting_state = "A"
        final_states = {"B"}

        nfa = Nfa(transition_function, starting_state, final_states)
        dfa = nfa.convert_to_dfa()

        expected_dfa_tranisition_function = {
            ("A", "0"): "B",
        }

        self.assertDictEqual(dfa.transition_function, expected_dfa_tranisition_function)
        self.assertEqual(dfa.final_states, {"B"})
