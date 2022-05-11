#! /usr/bin/env python
#
# Simple calculator interpreter
#
# This is the resolution of the exercise proposed by Ruslan Spivak
# on his guide "Let’s Build A Simple Interpreter. Part 3" on his
# blog https://ruslanspivak.com/lsbasi-part3/
#
# Instruction of the exercise made by Ruslan Spivak:
# - Write an interpreter that handles arithmetic expressions like “7 - 3 + 2 - 1” from scratch.
# - Use any programming language you’re comfortable with and write it off the top of your head
# - think about components involved:
# -- a lexer that takes an input and converts it into a stream of tokens,
# -- a parser that feeds off the stream of the tokens provided by the lexer and tries to recognize a structure in that stream,
# -- an interpreter that generates results after the parser has successfully parsed (recognized) a valid arithmetic expression.
# - String those pieces together.
# - Spend some time translating the knowledge you’ve acquired into a working interpreter for arithmetic expressions.
#


"""Simple calculator interpreter"""


# Operator tokens types
PLUS  = '+'
MINUS = '-'
MUL   = '*'
DIV   = '/'
EXP   = '^' 


class Token():
    """Token base class"""

    # NOTE: this is an abstract method
    # pylint: disable=no-self-use
    def value(self):
        """Return value of the token"""
        return 0


class IntToken(Token):
    """Integer token class"""

    def __init__(self, value):
        self._value = value

    def value(self):
        """Return value of the token"""
        return self._value


class EofToken():
    """End of file token class"""

    # NOTE: this is an empty class.


class OperatorToken(Token):
    """Operator base token class"""

    def __init__(self, first=IntToken(0), last=IntToken(0)):
        self.first = first
        self.last = last

    def set_childs(self, first, last):
        """Set child values of the operator token"""
        self.first = first
        self.last = last

    # NOTE: this is an abstract method
    # pylint: disable=no-self-use
    def value(self):
        """Return value of the token"""
        return 0


class PlusToken(OperatorToken):
    """Plus operator token"""

    def value(self):
        """Return value of the token"""
        return self.first.value() + self.last.value()


class MinusToken(OperatorToken):
    """Minus operator token"""

    def value(self):
        """Return value of the token"""
        return self.first.value() - self.last.value()


class MulToken(OperatorToken):
    """Mul operator token"""

    def value(self):
        """Return value of the token"""
        return self.first.value() * self.last.value()


class DivToken(OperatorToken):
    """Div operator token"""

    def value(self):
        """Return value of the token"""
        return self.first.value() / self.last.value()


class ExpToken(OperatorToken):
    """Exp operator token"""

    def value(self):
        """Return value of the token"""
        return self.first.value() ** self.last.value()


class Interpreter():
    """Simple interpreter to do simple calculations"""


    def __init__(self, text):
        self.text = text
        self.index = 0
        self.current_char = self.text[self.index]


    def is_index_in_range(self):
        """Returns if the index is in range"""
        return self.index < len(self.text) - 1


    def advance(self):
        """Advance index and current char"""

        if self.is_index_in_range():
            self.index += 1
            self.current_char = self.text[self.index]
        else:
            self.current_char = None


    def get_current_token(self):
        """Lexer that return tokenized current chars"""

        # Return end of file token
        if self.current_char is None:
            return EofToken()

        # Spaces are ignored
        while self.current_char.isspace():
            self.advance()

        # Return integer token,
        # this could be getted from multiples chars (e.g. "324")
        if self.current_char.isdigit():
            digits = self.current_char

            while self.is_index_in_range():
                temp_char = self.text[self.index + 1]
                if temp_char and temp_char.isdigit():
                    self.advance()
                    digits += self.current_char
                else:
                    break

            return IntToken(int(digits))

        # Return operator token
        if self.current_char == PLUS:
            return PlusToken()
        if self.current_char == MINUS:
            return MinusToken()
        if self.current_char == MUL:
            return MulToken()
        if self.current_char == DIV:
            return DivToken()
        if self.current_char == EXP:
            return ExpToken()


    def expr(self):
        """Arithmetic expression parser / interpreter"""

        # Get first integer token
        first = self.get_current_token()
        if isinstance(first, EofToken):
                return None
        self.advance()

        while True:
            # Get operator token
            operator = self.get_current_token()
            if isinstance(operator, EofToken):
                break
            self.advance()

            # Get last integer token
            last = self.get_current_token()
            if isinstance(last, EofToken):
                break
            self.advance()

            # Operate using the first and last integer tokens
            # Store result on first token to the next iteration
            operator.set_childs(first, last)
            first = IntToken(operator.value())

        return first.value()


def main():
    """Main script entry"""

    while True:
        text = input("calc> ")

        if not text:
            continue

        if text.lower() in ("exit", "quit", "q"):
            break

        interpreter = Interpreter(text)
        print(interpreter.expr())


if __name__ == '__main__':
    main()
