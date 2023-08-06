# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=arguments-renamed
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-return-statements

from functools import partial
from typing import Any, Callable, Iterable
from chiakilisp.utils import simple_fuzzy_matched  # <- for proposals
from chiakilisp.utils import get_assertion_closure  # <- for ASSERT()
from chiakilisp.models.token import Token  # Literal needs Token  :*)
from chiakilisp.models.forward import LiteralType  # forward declared

_ASSERT: Callable = get_assertion_closure(NameError)  # <---- closure


def _proposals(glossary: Iterable, item: str) -> str:

    """A little wrapper upon simple_fuzzy_matched()"""

    return ', '.join(simple_fuzzy_matched(item, glossary))


class NotFound:  # pylint: disable=too-few-public-methods  # its okay

    """
    Stub class to display that there is no such a name in environment
    """


class Literal(LiteralType):

    """
    Literal is the class that encapsulates single Token and meant to be a part of Expression, but not always
    """

    _token: Token

    def __init__(self, token: Token) -> None:

        """Initialize Literal instance"""

        self._token = token
        self._properties = {}

    def unquote(self) -> None:

        """Unquote a literal"""

        self.properties()['quoted'] = None

    def dump(self, indent: int) -> None:

        """Dumps a single expression literal"""

        value = self.token().value()

        print(' ' * indent, (f'"{value}"'
                             if self.token().is_string()
                             else value))

    def token(self) -> Token:

        """Returns Token instance tied to the Literal"""

        return self._token

    def wrapped(self) -> str:

        """Wraps literal to str"""

        return f'"{self.token().value()}"' \
            if self.token().is_string() else self.token().value()

    def lint(self, _: dict, rule: str, storage: dict, errors: list, __: dict) -> None:

        """React to the builtin linter visit event"""

        if rule == 'UnusedGlobalVariables' and self.token().type() == Token.Identifier:
            name = self.token().value()  # <---------------------------- get the name of the global variable
            if name in storage:  # <-------------------------------------- if global variable has defined...
                storage[name] += 1  # <------------------------------------ ...increment its reference count
            else:
                errors.append([self.token().position(),  f"variable '{name}' referenced before assignment"])

    def generate(self, dictionary: dict, _: dict, inline: bool):           # pylint: disable=unused-argument

        """Generate C++ representation of the single ChiakiLisp Literal"""

        token = self.token()  # <------------------------------------------- to refer it for multimple times

        representation = ''

        if token.type() == Token.Nil:
            representation = 'NULL'
        if token.type() == Token.String:
            representation = f'"{token.value()}"'
        if token.type() in [Token.Number, Token.Boolean]:
            representation = token.value()  # <----------------------------- return 'token().value()' string
        if token.type() == Token.Identifier:
            # Try to resolve a C++ name from a dictionary first  ###########################################
            raw = token.value()
            found = dictionary.get(raw)
            if found:
                return found  # if dictionary already contains a C++ function name, return found value as is
            # A bit of demangle processing here for LISPy names  ###########################################
            representation = raw \
                .replace('?', '_QUESTION_MARK') \
                .replace('!', '_EXCLAMATION_MARK')
            if not token.value() == '-':
                representation = representation.replace('-', '_DASH_')  # <------- replace '-' with '_DASH_'
            if not token.value().startswith('/') \
                    and not token.value().endswith('/') and '/' in token.value():  # <----------- be careful
                representation = representation.replace('/', '::')  # <------ replace LISP accessor with C++

        return f'{representation}{";" if not inline else ""}'  # <- append semicolon character if not inline

    def execute(self, environment: dict, __=False) -> Any:  # pylint: disable=inconsistent-return-statements

        """Execute, here, is the return Python value tied to the literal: number, string, boolean, etc..."""

        if self.quoted():

            return self  # return a literal

        if self.token().type() == Token.Nil:

            return None

        if self.token().type() == Token.Number:

            return int(self.token().value())

        if self.token().type() == Token.String:

            return self.token().value()

        if self.token().type() == Token.Boolean:

            return self.token().value() == 'true'

        if self.token().type() == Token.Identifier:

            name = self.token().value()  # <------------- because we reference token().value() so many times
            where = self.token().position()  # <------------------------------------ remember token position

            ASSERT = partial(_ASSERT, where)  # <------ create partial function to simplify ASSERT() fn call
            proposals = partial(_proposals, environment.keys())  # <------- simplify proposals function call

            if not name.startswith('/') and not name.endswith('/') and '/' in name:  # <--------- be careful
                obj_name, member_name, *_ = name.split('/')  # <------ syntax is <object name>/<member name>
                obj_object = environment.get(obj_name, NotFound)  # <------- assign found object or NotFound
                ASSERT(obj_object is not NotFound,
                       f"no '{obj_name}' object/module in this scope. Possibilities: {proposals(obj_name)}")
                member_object = getattr(obj_object, member_name, NotFound)  # <-------- assign member object
                ASSERT(member_object is not NotFound,
                       f"object (or module) named '{obj_name}' has no such a member named '{member_name}'. "
                       f"Possibilities: {_proposals(dir(member_object), member_name)}")  # <--- maybe cache?
                return member_object  # <------------------ thus we return found module/object member object

            found = environment.get(name, NotFound)  # <-- handle case when identifier name is not qualified

            ASSERT(
                found is not NotFound, f"no '{name}' symbol in this scope. Possibilities: {proposals(name)}"
            )

            return found  # <- return found Python 3 value (from the current environment) or raise NameError


Nil = Literal(Token(Token.Nil, 'nil', ()))  # predefined Nil Literal; useful for empty defn, fn and let body
identifier = lambda identifier_name: Literal(Token(Token.Identifier, identifier_name, ()))  # <- tiny helper
