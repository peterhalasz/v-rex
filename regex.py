from enfa import ENfa, EPS

KLEENEE = ("*", 2)
CONCATENATION = (".", 1)
UNION = ("+", 0)

ALPHABET = {"0", "1"}
OPERATORS = {KLEENEE[0], CONCATENATION[0], UNION[0]}


class Regex:
    def __init__(self, regex):
        self.regex = regex
        self.node_name_generator = self._create_node_name_generator()

    def _create_node_name_generator(self):
        for i in range(ord("a"), ord("z") + 1):
            for j in range(ord("a"), ord("z") + 1):
                yield chr(i) + chr(j)

    def _get_operator(self, operator):
        if operator == "*":
            return KLEENEE
        elif operator == ".":
            return CONCATENATION
        else:
            return UNION

    def _is_operator_higher_precedence(self, operator1, operator2):
        return self._get_operator(operator1)[1] >= self._get_operator(operator2)[1]

    def _add_explicit_concatenation_symbols(self, regex):
        new_regex = ""

        prev = ""
        for c in regex:
            if (c in ALPHABET or c == "(") and (
                prev in ALPHABET or prev == ")" or prev == "*"
            ):
                new_regex += "."

            new_regex += c
            prev = c

        return new_regex

    def shunting_yard(self):
        regex = self._add_explicit_concatenation_symbols(self.regex)

        output = ""
        operator_stack = []

        for symbol in regex:
            if symbol in ALPHABET:
                output += symbol
            elif symbol in OPERATORS:
                if operator_stack:
                    top_operator = operator_stack[-1]

                    if top_operator != "(":
                        while self._is_operator_higher_precedence(top_operator, symbol):
                            output += operator_stack.pop()
                            if operator_stack:
                                top_operator = operator_stack[-1]
                            else:
                                break

                operator_stack.append(symbol)
            elif symbol == "(":
                operator_stack.append("(")
            elif symbol == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output += operator_stack.pop()
                operator_stack.pop()

        while operator_stack:
            output += operator_stack.pop()

        return output

    def _handle_empty_expression(self):
        starting_state = self.node_name_generator.__next__()
        final_state = self.node_name_generator.__next__()

        enfa = ENfa(
            {
                (starting_state, EPS): {final_state},
            },
            starting_state,
            {final_state},
        )

        return enfa

    def _handle_symbol(self, symbol):
        starting_state = self.node_name_generator.__next__()
        final_state = self.node_name_generator.__next__()

        enfa = ENfa(
            {
                (starting_state, symbol): {final_state},
            },
            starting_state,
            {final_state},
        )

        return enfa

    def _handle_union(self, enfa1, enfa2):
        starting_state = self.node_name_generator.__next__()
        final_state = self.node_name_generator.__next__()

        enfa = ENfa(
            {
                (starting_state, EPS): {enfa1.starting_state, enfa2.starting_state},
                (list(enfa1.final_states)[0], EPS): {final_state},
                (list(enfa2.final_states)[0], EPS): {final_state},
            },
            starting_state,
            {final_state},
        )

        for k, v in enfa1.transition_function.items():
            enfa.transition_function[k] = v

        for k, v in enfa2.transition_function.items():
            enfa.transition_function[k] = v

        return enfa

    def _handle_concatenation(self, enfa1, enfa2):
        new_mid_state = self.node_name_generator.__next__()

        enfa = ENfa(
            {},
            enfa1.starting_state,
            enfa2.final_states,
        )

        for k, v in enfa1.transition_function.items():
            enfa.transition_function[k] = v

        for k, v in enfa2.transition_function.items():
            enfa.transition_function[k] = v

        for k, v in enfa.transition_function.items():
            if list(enfa1.final_states)[0] in v:
                enfa.transition_function[k] = enfa.transition_function[k] | {
                    new_mid_state
                }
                enfa.transition_function[k] = (
                    enfa.transition_function[k] - enfa1.final_states
                )

        for k, v in enfa.transition_function.items():
            if k[0] == enfa2.starting_state:
                enfa.transition_function[(new_mid_state, k[1])] = v
                del enfa.transition_function[k]
                break

        return enfa

    def _handle_kleene_star(self, enfa1):
        starting_state = self.node_name_generator.__next__()
        final_state = self.node_name_generator.__next__()

        enfa = ENfa(
            {
                (starting_state, EPS): {final_state, enfa1.starting_state},
                (list(enfa1.final_states)[0], EPS): {final_state, enfa1.starting_state},
            },
            starting_state,
            {final_state},
        )

        for k, v in enfa1.transition_function.items():
            enfa.transition_function[k] = v

        return enfa

    def thomsons_construction(self, postfix_regex):
        if postfix_regex == "":
            return self._handle_empty_expression()

        nfa_stack = []
        for e in postfix_regex:
            if e in ALPHABET:
                symbol_nfa = self._handle_symbol(e)
                nfa_stack.append(symbol_nfa)

            if e == CONCATENATION[0]:
                enfa2 = nfa_stack.pop()
                enfa1 = nfa_stack.pop()

                concatenation_enfa = self._handle_concatenation(enfa1, enfa2)
                nfa_stack.append(concatenation_enfa)

            if e == UNION[0]:
                enfa2 = nfa_stack.pop()
                enfa1 = nfa_stack.pop()

                union_enfa = self._handle_union(enfa1, enfa2)
                nfa_stack.append(union_enfa)

            if e == KLEENEE[0]:
                enfa1 = nfa_stack.pop()

                kleene_star_nfa = self._handle_kleene_star(enfa1)
                nfa_stack.append(kleene_star_nfa)

        result_enfa = nfa_stack.pop()
        return result_enfa

    def create_enfa_from_regex(self):
        """Creates an e-nfa from a regular expression.

        Args:
            regex: the regular expression as a string

        Returns:
            The e-nfa converted from a regex.
        """
        postfix_regex = self.shunting_yard()

        return self.thomsons_construction(postfix_regex)
