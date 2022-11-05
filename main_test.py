import unittest

from dfa import Dfa
from nfa import Nfa
from enfa import ENfa, EPS

from main import compile_and_test_dfa, compile_and_test_nfa, compile_and_test_enfa

class MainTest(unittest.TestCase):
    def test_main_dfa_1(self):
        transition_function = {
            ("A", "0"): "A", ("A", "1"): "B",
            ("B", "0"): "C",
            ("B", "1"): "D",
            ("C", "1"): "E",
            ("D", "0"): "E",
            ("E", "0"): "F",
            ("F", "1"): "G",
        }
        starting_state = "A"
        final_states = {"G"}
        dfa = Dfa(transition_function, starting_state, final_states)

        self.assertTrue(compile_and_test_dfa(dfa, "011001"))
        self.assertTrue(compile_and_test_dfa(dfa, "0000011001"))
        self.assertTrue(compile_and_test_dfa(dfa, "011001"))

        self.assertFalse(compile_and_test_dfa(dfa, ""))
        self.assertFalse(compile_and_test_dfa(dfa, "1"))
        self.assertFalse(compile_and_test_dfa(dfa, "1011001"))

    def test_main_nfa_1(self):
        transition_function = {
            ("A", "0"): {"A", "B"},
            ("A", "1"): {"A"},
            ("B", "1"): {"C"},
        }
        starting_state = "A"
        final_states = {"C"}

        nfa = Nfa(transition_function, starting_state, final_states)

        self.assertTrue(compile_and_test_nfa(nfa, "011001"))
        self.assertTrue(compile_and_test_nfa(nfa, "0000011001"))
        self.assertTrue(compile_and_test_nfa(nfa, "011001"))

        self.assertFalse(compile_and_test_nfa(nfa, ""))
        self.assertFalse(compile_and_test_nfa(nfa, "1"))
        self.assertFalse(compile_and_test_nfa(nfa, "1011011"))

    def test_main_enfa_1(self):
        transition_function = {
            ("A", "0"): {"H"},
            ("B", EPS): {"C", "I"},
            ("C", EPS): {"F", "G"},
            ("D", EPS): {"B"},
            ("E", EPS): {"B"},
            ("F", "0"): {"D"},
            ("G", "1"): {"E"},
            ("H", EPS): {"C", "I"},
            ("I", "1"): {"J"},
        }
        starting_state = "A"
        final_states = {"J"}

        enfa = ENfa(transition_function, starting_state, final_states)

        self.assertTrue(compile_and_test_enfa(enfa, "011001"))
        self.assertTrue(compile_and_test_enfa(enfa, "0000011001"))
        self.assertTrue(compile_and_test_enfa(enfa, "011001"))

        self.assertFalse(compile_and_test_enfa(enfa, ""))
        self.assertFalse(compile_and_test_enfa(enfa, "1"))
        self.assertFalse(compile_and_test_enfa(enfa, "1011011"))
