# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

import re
from typing import List
from chiakilisp.models.token import Token  # Lexer returns a Token instances list


ALPHABET = ['+', '-', '*', '/', '=', '<', '>', '?', '!', '.', '_', '&', ':', '^']


class Lexer:

    """
    Lexer is the class that takes the source code, then produces a list of tokens
    """

    _source: str
    _file_name: str   # the name of source file we're lexing
    _pointer: int = 0  # <-------------- default pointer pos
    _tokens: List[Token]
    _line_num, _char_num = 1, 0   # <-- position in the file

    def __init__(self, source: str, file_name: str) -> None:

        """Initialize Lexer instance"""

        self._source = source
        self._file_name = file_name
        self._tokens = []

    def tokens(self) -> List[Token]:

        """Returns list of tokens"""

        return self._tokens

    def _increment_char_number(self) -> None:

        """Increments character number by 1"""

        self._char_num += 1

    def _increment_line_number_with_char_number_reset(self) -> None:

        """Increments line number by 1 and resets character number"""

        self._char_num = 0
        self._line_num += 1

    def _pos(self) -> tuple:

        """Returns a tuple containing current char and line number"""

        return tuple((self._file_name, self._line_num, self._char_num))

    def pos(self) -> tuple:

        """Returns the same as the self._pos, but it's a public method"""

        return self._pos()  # <--- instead of doing extra refactoring :)

    def lex(self) -> None:  # pylint: disable=R0912, disable=R0915  # :(

        """Process the source code, thus it populates the tokens list"""

        while self._has_next_symbol():

            if self._current_symbol_is_semicolon() or \
                    self._current_symbol_is_hash():
                self._advance()
                while self._has_next_symbol():
                    if self._current_symbol_is_nl():
                        break
                    self._advance()
                self._advance()
                self._increment_line_number_with_char_number_reset()

            elif self._current_symbol_is_number() \
                    or (self._current_symbol_is_sign()
                        and self._next_symbol_is_number()):
                value = self._current_symbol()
                self._advance()
                self._increment_char_number()
                while self._has_next_symbol():
                    if self._current_symbol_is_number():
                        value += self._current_symbol()
                        self._advance()
                        self._increment_char_number()
                    else:
                        break
                self._tokens.append(Token(Token.Number, value, self._pos()))

            elif self._current_symbol_is_letter():
                value = self._current_symbol()
                self._advance()
                self._increment_char_number()
                while self._has_next_symbol():
                    if self._current_symbol_is_letter() or \
                            self._current_symbol_is_number():
                        value += self._current_symbol()
                        self._advance()
                        self._increment_char_number()
                    else:
                        break
                if value == 'nil':
                    self._tokens.append(Token(Token.Nil, value, self._pos()))
                elif value in ['true', 'false']:
                    self._tokens.append(Token(Token.Boolean, value, self._pos()))
                else:
                    self._tokens.append(Token(Token.Identifier, value, self._pos()))

            elif self._current_symbol_is_double_quote():
                value = ''
                while self._has_next_symbol():
                    self._advance()
                    self._increment_char_number()
                    if self._current_symbol() == '\\':
                        self._advance()
                        self._increment_char_number()
                        if self._current_symbol() == 'n':
                            value += '\n'
                        if self._current_symbol_is_double_quote():
                            value += '"'
                        continue
                    if not self._current_symbol_is_double_quote():
                        value += self._current_symbol()
                    else:
                        self._tokens.append(Token(Token.String, value, self._pos()))
                        break
                self._advance()  # <-- call _advance()  to skip the leading '"' char
                self._increment_char_number()  # <-- increment character num as well

            elif self._current_symbol_is_single_quote():
                self._tokens.append(Token(Token.Quote,            "'", self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_opening_bracket():
                self._tokens.append(Token(Token.OpeningBracket,   '(', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_closing_bracket():
                self._tokens.append(Token(Token.ClosingBracket,   ')', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_cr_opening_bracket():
                self._tokens.append(Token(Token.OpeningBracket,   '(', self._pos()))
                self._tokens.append(Token(Token.Identifier,   'dicty', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_cr_closing_bracket():
                self._tokens.append(Token(Token.ClosingBracket,   ')', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_sq_opening_bracket():
                self._tokens.append(Token(Token.OpeningBracket,   '(', self._pos()))
                self._tokens.append(Token(Token.Identifier,   'listy', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_sq_closing_bracket():
                self._tokens.append(Token(Token.ClosingBracket,   ')', self._pos()))
                self._advance()
                self._increment_char_number()

            elif self._current_symbol_is_nl():
                self._advance()
                self._increment_line_number_with_char_number_reset()  # position upd

            else:
                self._advance()  # <----------- skip over all the garbage characters
                self._increment_char_number()  # <-- with character number increment

    def _advance(self) -> None:

        """Advance the pointer"""

        self._pointer += 1

    def _current_symbol(self) -> str:

        """Returns the current symbol"""

        return self._source[self._pointer]

    def _next_symbol(self) -> str:

        """Returns the next symbol (if possible, otherwise '')"""

        if (len(self._source) == 1 and not self._pointer) \
                or not self._has_next_symbol():
            return ''
        return self._source[self._pointer + 1]

    def _has_next_symbol(self) -> bool:

        """Returns whether source has next symbol"""

        return self._pointer < len(self._source)

    def _current_symbol_is_nl(self) -> bool:

        """Returns whether current symbol is a newline symbol"""

        return self._current_symbol() == '\n'

    def _current_symbol_is_sign(self) -> bool:

        """Returns whether current symbol is a number sign"""

        return self._current_symbol() in ['+', '-']

    def _current_symbol_is_hash(self) -> bool:

        """Returns whether current symbol is a hashtag symbol"""

        return self._current_symbol() == '#'

    def _current_symbol_is_semicolon(self) -> bool:

        """Returns whether current symbol is a semicolon symbol"""

        return self._current_symbol() == ';'

    def _current_symbol_is_single_quote(self) -> bool:

        """Returns whether current symbol is a single-quote symbol"""

        return self._current_symbol() == "'"

    def _current_symbol_is_double_quote(self) -> bool:

        """Returns whether current symbol is a double-quote symbol"""

        return self._current_symbol() == '"'

    def _current_symbol_is_opening_bracket(self) -> bool:

        """Returns whether current symbol is an opening bracket symbol"""

        return self._current_symbol() == '('

    def _current_symbol_is_closing_bracket(self) -> bool:

        """Returns whether current symbol is a closing bracket symbol"""

        return self._current_symbol() == ')'

    def _current_symbol_is_cr_opening_bracket(self) -> bool:

        """Returns whether current symbol is a curly-opening bracket symbol"""

        return self._current_symbol() == '{'

    def _current_symbol_is_cr_closing_bracket(self) -> bool:

        """Returns whether current symbol is a curly-closing bracket symbol"""

        return self._current_symbol() == '}'

    def _current_symbol_is_sq_opening_bracket(self) -> bool:

        """Returns whether current symbol is a square-opening bracket symbol"""

        return self._current_symbol() == '['

    def _current_symbol_is_sq_closing_bracket(self) -> bool:

        """Returns whether current symbol is a square-closing bracket symbol"""

        return self._current_symbol() == ']'

    def _next_symbol_is_number(self) -> bool:

        """Returns whether next symbol is a number, valid number is from 0 to 9"""

        return re.match(r'\d', self._next_symbol()) is not None

    def _current_symbol_is_number(self) -> bool:

        """Returns whether current symbol is a number, valid number is from 0 to 9"""

        return re.match(r'\d', self._current_symbol()) is not None

    def _current_symbol_is_letter(self) -> bool:

        """Returns whether current symbol is a letter: valid letter is from a-ZA-Z or from the alphabet"""

        return re.match(r'[a-zA-Z]', self._current_symbol()) is not None or self._current_symbol() in ALPHABET
