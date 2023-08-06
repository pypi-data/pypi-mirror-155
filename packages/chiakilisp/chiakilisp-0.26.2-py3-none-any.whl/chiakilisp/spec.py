# pylint: disable=invalid-name
# pylint: disable=arguments-differ
# pylint: disable=arguments-renamed
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import re
from typing import Tuple
from chiakilisp.utils import pairs
from chiakilisp.models.forward import ExpressionType, LiteralType

is_chiakilisp_literal = lambda x: isinstance(x, LiteralType)
is_chiakilisp_expression = lambda x: isinstance(x, ExpressionType)


class ArityVariantType:

    @staticmethod
    def valid(length: int) -> Tuple[bool, int, str]:

        """bool: valid or not; int: length; str: error message"""


class SignatureVariantType:

    @staticmethod
    def valid(test) -> Tuple[bool, str]:

        """bool: valid or not; str: why the test is not valid?"""


class RestOf(SignatureVariantType):

    _variant: SignatureVariantType

    def __init__(self,
                 variant: SignatureVariantType) -> None:

        self._variant = variant

    def valid(self, rest: list) -> Tuple[bool, str]:

        if not isinstance(rest, list):
            return False,\
                   'can not be verified due to spec error'

        rest = pairs(rest) \
            if isinstance(self._variant, Pair) \
            else rest

        template = 'each extra arguments pair {explain}' \
            if isinstance(self._variant, Pair) \
            else 'each extra argument {explain}'

        for element in rest:
            valid, why = self._variant.valid(element)
            if not valid:
                return False, template.format(explain=why)
        return True, ''


class Pair(SignatureVariantType):

    _lhs: SignatureVariantType
    _rhs: SignatureVariantType

    def __init__(self,
                 lhs: SignatureVariantType,
                 rhs: SignatureVariantType) -> None:

        self._lhs = lhs
        self._rhs = rhs

    def valid(self, items: list) -> Tuple[bool, str]:

        lhs, rhs = items

        l_valid, l_why = self._lhs.valid(lhs)

        if not l_valid:
            return False,\
                   f'should be a pair, where lhs {l_why}'

        r_valid, r_why = self._rhs.valid(rhs)

        if not r_valid:
            return False,\
                   f'should be a pair, where rhs {r_why}'

        return True, ''


class FormOf(SignatureVariantType):

    _even: bool = False
    _empty: bool = True
    _variant: SignatureVariantType

    def __init__(self,
                 variant: SignatureVariantType,
                 even: bool = False,
                 empty: bool = False) -> None:

        self._even = even
        self._empty = empty
        self._variant = variant

        if isinstance(self._variant, Pair):
            self._even = True

    def valid(self,
              form: ExpressionType) -> Tuple[bool, str]:

        if not is_chiakilisp_expression(form):
            return False, 'should be a form'

        if self._empty and not form.children():
            return False, \
                   'should be a non-empty form'

        if self._even \
                and not len(form.children()) % 2 == 0:
            return False,\
                   'should be a form with even args count'

        items = pairs(form.children()) \
            if isinstance(self._variant, Pair) \
            else form.children()

        for each in items:
            valid, why = self._variant.valid(each)
            if not valid:
                return False, \
                       f'should be a' \
                       f' form, where each argument {why}'

        return True, ''


class Or(SignatureVariantType):

    _variants: Tuple[SignatureVariantType]

    def __init__(
            self,
            *variants: SignatureVariantType) -> None:

        self._variants = variants

    def valid(self, something) -> Tuple[bool, str]:

        results = [
            v.valid(something) for v in self._variants
        ]

        if True not in map(lambda r: r[0], results):
            return False, f'(at least) {results[1][1]}'

        return True, ''


class _Anything(SignatureVariantType):

    @staticmethod
    def valid(_) -> Tuple[bool, str]:

        if isinstance(_, list):
            return False, \
                   'can not be verified due to spec error'
        return True, ''


Anything = _Anything()


class _Identifier(SignatureVariantType):

    @staticmethod
    def valid(literal: LiteralType) -> Tuple[bool, str]:

        if not literal.token().is_identifier():
            return False, 'should be an Identifier literal'

        return True, ''


Identifier = _Identifier()


class _String(SignatureVariantType):

    @staticmethod
    def valid(literal: LiteralType) -> Tuple[bool, str]:

        if not literal.token().is_string():
            return False, 'should be a String literal'

        return True, ''


String = _String()


class Literal(SignatureVariantType):

    _pattern: str = None
    _specification = SignatureVariantType

    def __init__(self,
                 spec: SignatureVariantType,
                 pattern: str = None):

        self._pattern = pattern
        self._specification = spec

    def valid(self, literal: LiteralType) -> Tuple[bool, str]:

        if not is_chiakilisp_literal(literal):
            return False, 'should be a literal'

        valid, why = self._specification.valid(literal)
        if not valid:
            return valid, why

        if self._pattern:
            if not re.match(self._pattern,
                            literal.token().value()):
                return False,\
                       f'value should match to [{self._pattern}]'

        return True, ''


class Signature:

    _specs: Tuple[SignatureVariantType]
    _specs_length: int

    def __init__(self,
                 *specs: SignatureVariantType):

        self._specs = specs
        self._specs_length = len(specs)

    def _last_spec_is_rest_of(self) -> bool:

        return isinstance(self._specs[-1], RestOf)

    def valid(self,
              body: list,
              length: int) -> Tuple[bool, int, str]:

        last_spec_is_rest_of = self._last_spec_is_rest_of()

        if length > self._specs_length and \
                not last_spec_is_rest_of:
            return False, \
                   length, \
                   f'got too many arguments: {length}' \
                   f' (max possible: {self._specs_length})'

        if last_spec_is_rest_of:
            test = body[:self._specs_length - 1]
            test.append(body[self._specs_length - 1:])
        else:
            test = body

        actual_length = len(test)

        for n, (itm, spec) in enumerate(zip(test, self._specs)):
            valid, why = spec.valid(itm)
            if not valid:
                return valid, \
                       actual_length, (
                            f'argument no [{n}] {why}'
                            if not (self._specs_length == 0
                                    and last_spec_is_rest_of) else why
                       )
        return True, actual_length, ''


class Exactly(ArityVariantType):

    _value: int

    def __init__(self, value: int) -> None:

        self._value = value

    def valid(self,
              length: int) -> Tuple[bool, int, str]:

        return length == self._value,\
               length, \
               f'expected exactly {self._value} arg(s)'


class AtLeast(ArityVariantType):

    _value: int

    def __init__(self, value) -> None:

        self._value = value

    def valid(self,
              length: int) -> Tuple[bool, int, str]:

        return length >= self._value,\
               length,\
               f'expected at least {self._value} arg(s)'


class _Even(ArityVariantType):

    @staticmethod
    def valid(length: int) -> Tuple[bool, int, str]:

        return length % 2 == 0,\
               length, 'expected an even number of args'


Even = _Even()


class Arity:

    _arity_specification: ArityVariantType

    def __init__(self,
                 arity_specification:
                 ArityVariantType) -> None:

        self._arity_specification = arity_specification

    def valid(self, body) -> Tuple[bool, int, str]:

        return self._arity_specification.valid(len(body))


class Rule:

    _arity: Arity
    _signature: Signature

    def __init__(self,
                 arity,
                 signature=None) -> None:

        self._arity = arity
        self._signature = signature

    def valid(self, body) -> Tuple[bool, int, str]:

        valid, arity, why = self._arity.valid(body)

        if not valid:
            return valid, arity, f'{why}, got {arity}'

        if self._signature:
            valid, arity, why = self._signature.valid(body[:arity],
                                                      arity)

            if not valid:
                return valid, arity, why

        return valid, arity, ''


rules = {
    'try': Rule(Arity(Exactly(2)),
                Signature(Anything,
                          FormOf(Anything))),
    'catch': Rule(Arity(AtLeast(4)),
                  Signature(Literal(Identifier, pattern=r'catch$'),
                            Literal(Identifier),
                            Literal(Identifier),
                            RestOf(Anything))),
    'dot-form': Rule(Arity(AtLeast(1)),
                     Signature(Anything, RestOf(Anything))),
    'if': Rule(Arity(AtLeast(2)),
               Signature(Anything, Anything, Anything)),
    'when': Rule(Arity(AtLeast(2)),
                 Signature(Anything, RestOf(Anything))),
    'cond': Rule(Arity(Even),
                 Signature(RestOf(Anything))),
    'let': Rule(Arity(AtLeast(1)),
                Signature(FormOf(Pair(Or(FormOf(Literal(Identifier)),
                                         Literal(Identifier)),
                                      Anything)),
                          RestOf(Anything))),
    'let-cpp': Rule(Arity(AtLeast(2)),
                    Signature(FormOf(Pair(Literal(Identifier),
                                          Anything),
                                     empty=False),
                              RestOf(Anything))),
    'fn': Rule(Arity(AtLeast(1)),
               Signature(FormOf(Literal(Identifier)),
                         RestOf(Anything))),
    'def': Rule(Arity(Exactly(2)),
                Signature(Literal(Identifier), Anything)),
    'def?': Rule(Arity(Exactly(2)),
                 Signature(Literal(Identifier), Anything)),
    'defn': Rule(Arity(AtLeast(2)),
                 Signature(Literal(Identifier),
                           FormOf(Literal(Identifier)),
                           RestOf(Anything))),
    'defmacro': Rule(Arity(AtLeast(2)),
                     Signature(Literal(Identifier),
                               FormOf(Literal(Identifier)),
                               RestOf(Anything))),
    'defn-cpp': Rule(Arity(AtLeast(3)),
                     Signature(Literal(Identifier),
                               FormOf(Literal(Identifier)),
                               RestOf(Anything))),
    'import': Rule(Arity(Exactly(1)), Signature(Literal(Identifier))),
    'require': Rule(Arity(Exactly(1)), Signature(Literal(Identifier))),
    'new': Rule(Arity(Exactly(1)), Signature(FormOf(Anything,
                                                    empty=False))),
    'link': Rule(Arity(Exactly(1)), Signature(Literal(Identifier))),
    'include': Rule(Arity(Exactly(1)), Signature(Literal(Identifier))),
    'hpp-base-dir': Rule(Arity(Exactly(1)), Signature(Literal(String))),
    'lib-base-dir': Rule(Arity(Exactly(1)), Signature(Literal(String))),
    # new rules for other internal forms will be added here a bit later.
}
