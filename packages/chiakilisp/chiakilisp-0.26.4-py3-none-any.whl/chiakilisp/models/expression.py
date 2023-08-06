# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-locals
# pylint: disable=arguments-renamed
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-return-statements

from copy import deepcopy
from typing import List, Any, Callable
import chiakilisp.spec as s
from chiakilisp.spec import rules
from chiakilisp.models.forward import\
    ExpressionType, CommonType
from chiakilisp.models.literal import\
    Literal, NotFound, Nil, identifier
from chiakilisp.utils import get_assertion_closure, pairs


class ArityError(SyntaxError):

    """ArityError (just for name)"""


class NotSupportedError(SyntaxError):

    """NotSupportedError (just for name)"""


NE_ASSERT = get_assertion_closure(NameError)  # <-------- raises NameError
SE_ASSERT = get_assertion_closure(SyntaxError)  # <---- raises SyntaxError
RE_ASSERT = get_assertion_closure(RuntimeError)  # <-- raises RuntimeError
TE_ASSERT = get_assertion_closure(TypeError)  # <-------- raises TypeError
NS_ASSERT = get_assertion_closure(NotSupportedError)   # NotSupportedError

TYPES = {'int': int, 'float': float,
         'str': str,
         'list': list, 'tuple': tuple, 'dict': dict, 'set': set}

CXX_TYPES = {'int': 'long', 'float': 'float', 'str': 'std::string'}


def IDENTIFIER_ASSERT(lit: Literal, message: str) -> None:

    """Handy shortcut to make assertion that Literal is Identifier"""

    SE_ASSERT(lit.token().position(), lit.token().is_identifier(), message)


def TAIL_IS_VALID(tail: list, rule: str, where: tuple, m_tmpl: str) -> int:

    """
    Validates tail with a certain rule, throws SyntaxError or returns arity
    """

    valid, arity, why = rules.get(rule).valid(tail)
    SE_ASSERT(where, valid, m_tmpl.format(why=why))
    return arity


class Expression(ExpressionType):

    """
    Expression is the class that indented to be used to calculate something
    """

    _children: list

    def __init__(self, children: list) -> None:

        """Initialize Expression instance"""

        self._children = children
        self._properties = {}

    def children(self) -> list:

        """Returns expression children"""

        return self._children

    def wrapped(self) -> str:

        """Wraps expression to str"""

        return '(' + ' '.join(
            map(lambda x: x.wrapped(),
                self.children())
        ) + ')'

    def unquote(self) -> None:

        """Recursively unquote am expression"""

        self.properties()['quoted'] = None
        for children in self.children():
            children.unquote()

    def dump(self, indent: int) -> None:

        """Dumps the entire expression"""

        # There is no need to annotate types, or assert() them

        children = self.children()
        if children:
            first, *rest = children
            first.dump(indent)
            for argument in rest:
                argument.dump(indent + 1)   # increment indent

    def lint(self, _: dict, rule: str, storage: dict, errors: list, places: dict) -> None:

        """React to the builtin linter visit event"""

        head: Literal
        head, *tail = self.children()

        assert isinstance(head, Literal), 'Expression[lint]: head should be a Literal, not an Expression instance'
        IDENTIFIER_ASSERT(head,                       'Expression[lint]: head of expression should be Identifier')

        where = head.token().position()  # <---------------------- remember head token position in the source code

        if head.token().value() == 'def':
            valid, _, why = rules.get('def').valid(tail)  # <---------------- validate tail with the def-form rule
            if not valid:
                errors.append([where, f'def: {why}'])  # <-- instead of raising SyntaxError, add to the error list
                return  # <--------------------------------- and return (do nothing) on current linter visit event
            name: Literal = tail[0]  # <----------------------------------------- assign name as a type of Literal

            if rule == 'UnusedGlobalVariables':
                places.update({name.token().position(): ['GlobalVariable', name.token().value()]})  # register var
                storage[name.token().value()] = 0    # since we define global variable with def, add it to storage

    def generate(self, dictionary: dict, cfg: dict, inline: bool):

        """Generate C++ representation of the ChiakiLisp expression"""

        head: Literal
        head, *tail = self.children()

        assert isinstance(head, Literal),  'Expression[generate]: head should be an instance of Literal'
        IDENTIFIER_ASSERT(head,      'Expression[generate]: head of expression should be an Identifier')

        where = head.token().position()  # <------------ remember current expression head token position

        NS_ASSERT(
            where,
            head.token().value() not in [
                'try',     # in cxx mode we do not support code generation for try form. TODO: implement
                'fn',       # in cxx mode we do not support code generation for lambdas. TODO: implement
                'def?',                 # in cxx mode we do not support def? form (yet). TODO: implement
                'defmacro',   # in cxx mode we do not support 'macros' generation (yet). TODO: implement
                'import',        # in cxx mode we do not support Python 3 modules (now). TODO: implement
                'require'    # in cxx mode we do not support ChiakiLisp modules require. TODO: implement
            ],
            f"Expression[generate]: '{head.token().value()}' special form: is not supported in cxx-mode"
        )

        if head.token().value() == 'or':
            if not tail:
                return 'NULL' + (';' if not inline else '')  # <----- if no tail, just return NULL value
            return '(' + ' || '.join(map(lambda e: e.generate(dictionary, cfg, True),
                                         tail)) + ')' + ('' if inline else ';')   # make 'or' expression

        if head.token().value() == 'and':
            if not tail:
                return 'true' + (';' if not inline else '')  # <----- if no rest, just return true value
            return '(' + ' && '.join(map(lambda e: e.generate(dictionary, cfg, True),
                                         tail)) + ')' + ('' if inline else ';')  # make 'and' expression

        # try...

        if head.token().value() == '->':
            if not tail:
                return 'NULL' + (';' if inline else '')  # <--------------------- if no tail, return nil

            if len(tail) == 1:
                return tail[-1].generate(dictionary, cfg, inline)  # <---- if only one form, generate it

            tail = deepcopy(tail)  # <----------- could be slow if tail is complex nested data structure

            target, *rest = tail  # <------------------------------ initialize target and rest variables
            while len(tail) > 1:  # <----- do not leave loop while there is at least one element in tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <------- cast each argument from the rest to Expression
                rest[0].children().insert(1, target)  # <---------------------------- insert an argument
                tail = [rest[0]] + rest[1:]  # <------------------------------------------ override tail
                target, *rest = tail  # <----------------- do the same we did before entering while-loop

            return target.generate(dictionary, cfg, inline)  # <------------ return generated expression

        if head.token().value() == '->>':
            if not tail:
                return 'NULL' + (';' if inline else '')  # <--------------------- if no tail, return nil

            if len(tail) == 1:
                return tail[-1].generate(dictionary, cfg, inline)  # <---- if only one form, generate it

            tail = deepcopy(tail)  # <----------- could be slow if tail is complex nested data structure

            target, *rest = tail  # <----------------------------- initialize target and _rest variables
            while len(tail) > 1:  # <----- do not leave loop while there is at least one element in tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <------- cast each argument from the rest to Expression
                rest[0].children().append(target)  # <----------------------- append argument to the end
                tail = [rest[0]] + rest[1:]  # <------------------------------------------ override tail
                target, *rest = tail  # <----------------- do the same we did before entering while-loop

            return target.generate(dictionary, cfg, inline)  # <------------ return generated expression

        if head.token().value().startswith('.') and not head.token().value() == '...':   # skip Ellipsis
            SE_ASSERT(where,
                      len(head.token().value()) > 1,
                      'Expression[generate]: dot-form: method name is mandatory, could not just be "."')
            TAIL_IS_VALID(tail, 'dot-form', where,              'Expression[generate]: dot-form: {why}')
            name: Literal   # <---------------------------------------- assign name as a type of Literal
            name, *args = tail  # <-------------------------------- assign args to a list of CommonTypes
            generated = name.generate(dictionary, cfg, True)  # <------------ generate C++ variable name
            accessor = '->' if generated in cfg['KNOWN_POINTERS'] else '.'   # <-- use '->' for pointers
            return f'{generated}{accessor}{head.token().value()[1:]}(' \
                   + ', '.join(map(lambda an_arg: an_arg.generate(dictionary, cfg, True), args)) + ')' \
                   + (';' if not inline else '')  # <---- return generated dot-expression representation

        if head.token().value() == 'if':
            arity = TAIL_IS_VALID(tail, 'if', where,                  'Expression[generate]: if: {why}')
            cond, true, false = (tail if arity == 3 else tail + [Nil])   # tolerate missing false-branch
            return f'({{{cond.generate(dictionary, cfg, True)} ' \
                   f'? {true.generate(dictionary, cfg, True)}' \
                   f': {false.generate(dictionary, cfg, False)}}})' + ('' if inline else ';')  # ternary

        if head.token().value() == 'when':
            TAIL_IS_VALID(tail, 'when', where,                      'Expression[generate]: when: {why}')
            cond, *extras = tail  # <---------------- false branch is always equals to nil for when-form
            consequences = '({'+''.join([true.generate(dictionary, cfg, False) for true in extras])+'})'
            return f'({{{cond.generate(dictionary, cfg, True)} ? {consequences}' \
                   f': NULL;}})' + ('' if inline else ';')  # <- ternary expression, but 'false' is NULL

        if head.token().value() == 'cond':
            if not tail:
                return '({ NULL; )}' + (';' if not inline else '')  # <- generate a block returning NULL
            TAIL_IS_VALID(tail, 'cond', where,                      'Expression[generate]: cond: {why}')
            return Expression([identifier('->>')] + [
                Expression([identifier('if')] + each_pair) for each_pair in reversed(tuple(pairs(tail)))
            ]).generate(dictionary, cfg, inline)  # <-- return generated (->> ...) expression with 'if's

        if head.token().value() == 'let':
            TAIL_IS_VALID(tail, 'let-cpp', where,                    'Expression[generate]: let: {why}')
            bindings: Expression  # <---------------------------- assign binding as a type of Expression
            bindings, *body = tail  # <---------------------------- assign body as a list of CommonTypes
            lines = []  # <------------------------------------------ initialize a list for a code lines
            for name, value in pairs(bindings.children()):  # <- for each pair in bindings form children
                name: Literal  # <----------------------------------- assign name as a type of a Literal
                rhs = value.generate(dictionary, cfg,  False)  # <------- right-hand-side generated code
                generated = name.generate(dictionary, cfg, True)  # <------- generated C++ variable name
                lhs = f'auto{"*" if rhs.startswith("new") else ""} {generated}'  # <- and left-hand-side
                if rhs.startswith("new"):  # <- if we've have encountered 'new ...' generated expression
                    cfg['KNOWN_POINTERS'].append(generated)  # <-- append lhs to the known pointers list
                lines.append(f'{lhs} = {rhs}')  # <--- register generated variable definition expression
            for each in body:
                lines.append(each.generate(dictionary, cfg, False))  # <--- and generate body code lines
            return '({' + '\n'.join(lines) + '})' + (';' if not inline else '')  # <- generate let-block

        # fn...

        if head.token().value() == 'def':
            TAIL_IS_VALID(tail, 'def', where,                        'Expression[generate]: def: {why}')
            name: Literal   # <---------------------------------------- assign name as a type of Literal
            name, value = tail  # <-------------------------------- assign value as a type of CommonType
            ty = CXX_TYPES.get(name.property("t"), "auto")  # <--------- take into account variable type
            generated = name.generate(dictionary, cfg, True)  # <------------ generate C++ variable name
            cfg['DEFS'].append(f'{ ty } {  generated  } = {  value.generate(dictionary, cfg, False)  }')
            return ''  # <------ def-form is not supposed to generate a line of code, only update config

        # def?...

        if head.token().value() == 'defn':
            TAIL_IS_VALID(tail, 'defn-cpp', where,                  'Expression[generate]: defn: {why}')
            name: Literal  # <----------------------------------------- assign name as a type of Literal
            parameters: Expression  # <----------------------- assign parameters as a type of Expression
            name, parameters, *body = tail  # <-------------------- assign body as a list of CommonTypes
            returns = CXX_TYPES.get(name.property("t"), "auto")  # <------ take into account return type
            built_name = name.generate(dictionary, cfg, True)  # <----------- generate C++ function name
            built_parameters = '(' + \
                               ', '.join(map(lambda par: f'{CXX_TYPES.get(par.property("t"),  "auto")} '
                                                         f'{par.generate(dictionary,    cfg,    True)}',
                                             parameters.children())) \
                               + ')'  # <------------------------------ generate C++ function parameters
            built_body = f'return ({{{" ".join([e.generate(dictionary, cfg, False) for e in body])}}});'
            cfg['DEFUNCTIONS'].append(f'{returns} {built_name} {built_parameters} {{  {built_body}  }}')
            return ''  # <--- defn function is not supposed to return generated code, only update config

        # import...

        # require...

        # defmacro ...

        if head.token().value() == 'new':
            TAIL_IS_VALID(tail, 'new', where,                        'Expression[generate]: new: {why}')
            definition: Expression = tail[0]  # <------------- assign definition as a type of Expression
            return f'new {definition.generate(dictionary, cfg, inline)}'  # return a generated statement

        if head.token().value() == 'link':
            TAIL_IS_VALID(tail, 'link', where,                      'Expression[generate]: link: {why}')
            name: Literal = tail[0]  # <------------------------------- assign name as a type of Literal
            cfg['LD_LINK_SRC_WITH'].append(name.token().value())  # <--- append name to LD_LINK_SRC_WITH
            return ''  # <------------------------- link form is not supposed to generate a line of code

        if head.token().value() == 'include':
            TAIL_IS_VALID(tail, 'include', where,                'Expression[generate]: include: {why}')
            path: Literal = tail[0]  # <------------------------------- assign path as a type of Literal
            cfg['SOURCE_INCLUDING'].append(path.token().value())  # <--- append name to SOURCE_INCLUDING
            return ''  # <---------------------- include form is not supposed to generate a line of code

        if head.token().value() == 'hpp-base-dir':
            TAIL_IS_VALID(tail, 'hpp-base-dir', where,      'Expression[generate]: hpp-base-dir: {why}')
            path: Literal = tail[0]  # <------------------------------- assign path as a type of Literal
            cfg['CXX_INCLUDE_DIRS'].append(path.token().value())  # <--- append path to CXX_INCLUDE_DIRS
            return ''  # <----------------- hpp-base-dir form is not supposed to generate a line of code

        if head.token().value() == 'lib-base-dir':
            TAIL_IS_VALID(tail, 'lib-base-dir', where,      'Expression[generate]: lib-base-dir: {why}')
            path: Literal = tail[0]  # <------------------------------- assign path as a type of Literal
            cfg['CXX_LIBRARY_DIRS'].append(path.token().value())  # <--- append path to CXX_LIBRARY_DIRS
            return ''  # <----------------- lib-base-dir form is not supposed to generate a line of code

        cpp_function_name = head.generate(dictionary, cfg, True)  # <--- get generated C++ function name
        lines = [f'{cpp_function_name}(']  # <- function call generation start: name and opening bracket
        arguments = []  # <------------------------------ a list of all the generated function arguments
        for each in tail:
            arguments.append(each.generate(dictionary, cfg, True))  # <---- populate a list of arguments
        lines.append(', '.join(arguments))  # <--- join all the function arguments by a 'coma' character
        lines.append(')' if inline else ');')  # <- close the function call with closing bracket and ';'
        return ''.join(lines)  # <------------------------------------------ return all the lines joined

    def execute(self, environ: dict, top: bool = True) -> Any:

        """Execute here, is the return Python value 3 related to the expression: string, number, and vice versa"""

        if self.quoted():

            return self  # <--------------------- return expression instance in case user have decided to quote it

        head: Literal

        assert self.children(),           'Expression[execute]: current expression is empty, unable to execute it'

        head, *tail = self.children()

        assert isinstance(head, Literal),        'Expression[execute]: head of the expression should be a Literal'
        IDENTIFIER_ASSERT(head,             'Expression[execute]: head of the expression should be an Identifier')

        where = head.token().position()  # <------------ when make assertions on expression head, this can be used

        NS_ASSERT(
            where,
            head.token().value() not in [
                'new'  # <------------- in ast mode we do not need to manipulate with pointers to object instances
                'link',  # <- in ast mode we do not need to define which library our program should be linked with
                'include',  # <-- in ast mode we not need to define what header we should include into our program
                'hpp-base-dir',  # in ast mode we do not need to define location whether to lookup for CXX headers
                'lib-base-dir',  # in ast mode we do not need to define location whether to lookup for CXX library
            ],
            f"Expression[generate]: sorry, but '{head.token().value()}' special form is not supported in ast-mode"
        )

        if head.token().value() == 'or':
            if not tail:
                return None  # <-------------------------- if there are no arguments given to the form, return nil
            result = None  # <----------------------------------------------- set result to the null pointer first
            for cond in tail:  # <-------------------------------------------- for each condition in the arguments
                result = cond.execute(environ, False)  # <------------------------------------- compute the result
                if result:
                    return result  # <------------------------------------ and if there is truthy value, return it
            return result  # <------- if all conditions have been evaluated to falsy ones, return the last of them

        if head.token().value() == 'and':
            if not tail:
                return True  # <------------------------- if there are no arguments given to the form, return true
            result = None  # <----------------------------------------------- set result to the null pointer first
            for cond in tail:  # <-------------------------------------------- for each condition in the arguments
                result = cond.execute(environ, False)  # <------------------------------------- compute the result
                if not result:
                    return result  # <----------------------------- and if there is None or False value, return it
            return result  # <------ if all conditions have been evaluated to truthy ones, return the last of them

        if head.token().value() == 'try':
            TAIL_IS_VALID(tail, 'try', where,                                   'Expression[execute]: try: {why}')
            main: CommonType = tail[0]  # <----------------------------------- assign main as a type of CommonType
            catch: Expression = tail[1]  # <--------------------------------- assign catch as a type of Expression
            TAIL_IS_VALID(catch.children(), 'catch', where,                   'Expression[execute]: catch: {why}')
            klass: Literal = catch.children()[1]  # <--------------------------- assign klass as a type of Literal
            alias: Literal = catch.children()[2]  # <--------------------------- assign alias as a type of Literal
            block: List[CommonType] = catch.children()[3:]  # <------------- assign block as a list of CommonTypes
            obj = klass.execute(environ, False)  # <---------------------------------- get actual exception object
            closure = {}  # <--------------------------------------------------- initialize a try-form environment
            closure.update(environ)  # <-------------------------------------------- update it with the global one
            try:
                return main.execute(environ, False)  # <-------------------------------- try to execute main block
            except obj as exception:  # <------------------------------------------ if exception has been occurred
                closure[alias.token().value()] = exception  # <-- associate exception instance with a chosen alias
                return [expr.execute(closure, False) for expr in block][-1]  # <- return exception handling result

        if head.token().value() == '->':
            if not tail:
                return None  # <------------------------------------------------- if there are no tail, return nil

            if len(tail) == 1:
                return tail[-1].execute(environ, False)  # <------------ if there is only one argument, execute it

            tail = deepcopy(tail)  # <--------- it could be slow when tail if really complex nested data structure

            target, *rest = tail  # <------- split tail for the first time to initialize target and rest variables
            while len(tail) > 1:  # <-- do not leave the loop while there is at least one element left in the tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <-------- each argument except first should be cast to Expression
                rest[0].children().insert(1, target)  # <- in case of first-threading-macro, insert as the 1st arg
                tail = [rest[0]] + rest[1:]  # <- override tail: modified expression and the tail rest with offset
                target, *rest = tail  # <--------------------------- do the same we did before entering while-loop

            return target.execute(environ, False)  # <----- at the end, return target' expression execution result

        if head.token().value() == '->>':
            if not tail:
                return None  # <------------------------------------------------- if there are no tail, return nil

            if len(tail) == 1:
                return tail[-1].execute(environ, False)  # <------------ if there is only one argument, execute it

            tail = deepcopy(tail)  # <--------- it could be slow when tail if really complex nested data structure

            target, *rest = tail  # <------- split tail for the first time to initialize target and rest variables
            while len(tail) > 1:  # <-- do not leave the loop while there is at least one element left in the tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <-------- each argument except first should be cast to Expression
                rest[0].children().append(target)  # <- in case of last-threading-macro, append to the end of args
                tail = [rest[0]] + rest[1:]  # <- override tail: modified expression and the tail rest with offset
                target, *rest = tail  # <--------------------------- do the same we did before entering while-loop

            return target.execute(environ, False)  # <----- at the end, return target' expression execution result

        if head.token().value().startswith('.') and not head.token().value() == '...':   # it could be an Ellipsis
            SE_ASSERT(where,
                      len(head.token().value()) > 1,    'Expression[execute]: dot-form: method name is mandatory')
            TAIL_IS_VALID(tail,                         'dot-form', where, 'Expression[execute]: dot-form: {why}')
            object_name: Literal  # <------------------------------------- assign object name as a type of Literal
            object_name, *method_args = tail  # <--------------- get the object name and method args from the tail
            method_alias = head.token().value()[1:]  # <------------------------------ get the method name (alias)
            object_instance = object_name.execute(environ, False)  # <---- get an object instance from environment
            SE_ASSERT(where,
                      hasattr(object_instance, '__class__'),
                      'Expression[execute]: dot-form: use object/method, module/method to invoke a static method')
            object_alias = object_instance.__class__.__name__  # <-------------- get an actual instance class name
            object_method: Callable = getattr(object_instance, method_alias, NotFound)  # <--- get a method object
            NE_ASSERT(where,
                      object_method is not NotFound,
                      f"Expression[execute]: dot-form: an '{object_alias}' object has no method '{method_alias}'")
            return object_method(*(child.execute(environ, False) for child in method_args))  # <-- return a result

        if head.token().value() == 'if':
            arity = TAIL_IS_VALID(tail, 'if', where,                             'Expression[execute]: if: {why}')
            cond, true, false = (tail if arity == 3 else tail + [Nil])  # <-- tolerate missing false-branch for if
            return true.execute(environ, False) if cond.execute(environ, False) else false.execute(environ, False)

        if head.token().value() == 'when' and environ.get('use-builtin-when-form'):  # if 'false', use a new macro
            TAIL_IS_VALID(tail, 'when', where,                                 'Expression[execute]: when: {why}')
            cond, *extras = tail  # <-------------------------- false branch is always equals to nil for when-form
            return [true.execute(environ, False) for true in extras][-1] if cond.execute(environ, False) else None

        if head.token().value() == 'cond':
            if not tail:
                return None  # <------------------------------------------ if nothing has been passed, return None
            TAIL_IS_VALID(tail, 'cond', where,                                 'Expression[execute]: cond: {why}')
            for cond, expr in pairs(tail):
                if cond.execute(environ, False):
                    return expr.execute(environ, False)
            return None  # <------------------------------------------------------ if nothing is true, return None

        if head.token().value() == 'let':
            TAIL_IS_VALID(tail, 'let', where,                                   'Expression[execute]: let: {why}')
            bindings: Expression  # <------------------------------------- assign bindings as a type of Expression
            bindings, *body = tail  # <--------------------------------------- assign body as a list of CommonType
            let = {}  # <---------------------------------------------- initialize a new environment for let-block
            let.update(environ)  # <------------------------------------------------ update it with the global one
            for raw, value in pairs(bindings.children()):  # <--------------------------------- for each next pair
                if isinstance(raw, Expression):  # <-------------------------------- if a left-hand-side is a form
                    get = environ.get('get')  # <--------------------- use handy 'get' from the ChiakiLisp corelib
                    RE_ASSERT(where, get,    "Expression[execute]: let: destructuring requires core/get function")
                    executed = value.execute(let, False)  # <-- store a value execution result; to treat as a coll
                    for idx, alias in enumerate(map(lambda v: v.token().value(), raw.children())):  # iterate form
                        let.update({alias: get(executed, idx, None)})  # <---- assign nil, or indexed item of coll
                else:  # <---------------------------------------------------- the left-hand-side is an identifier
                    let.update({raw.token().value(): value.execute(let, False)})  # <- assign value to its binding
            if not body:
                body = [Nil]  # <----------- let the ... let have an empty body, in this case, result would be nil
            return [child.execute(let, False) for child in body][-1]  # <------ return the last calculation result

        if head.token().value() == 'fn':
            TAIL_IS_VALID(tail, 'fn', where,                                     'Expression[execute]: fn: {why}')
            parameters: Expression  # <--------------------------------- assign parameters as a type of Expression
            parameters, *body = tail  # <-----------------------------------assign body as the list of CommonTypes
            names = []  # <------------------------------------------------------ define a list of parameter names
            types = []  # <------------------------------------------------------ define a list of parameter types
            children = parameters.children()  # <---- assign children as the reference to the parameter form items
            ampersand_found = tuple(filter(lambda p: p[1].token().value() == '&', enumerate(children)))   # find &
            ampersand_position: int = ampersand_found[0][0] if ampersand_found else -1  # get '&' position (or -1)
            positional_parameters = children[:ampersand_position] if ampersand_found else children   # positionals
            positional_parameters_length = len(positional_parameters)  # <------------ remember positionals length
            for parameter in positional_parameters:  # <---------------------------- for each positional parameter
                parameter: Literal  # <------------------------------------- assign parameter as a type of Literal
                names.append(parameter.token().value())  # <--------------- append parameter name to the name list
                types.append(TYPES.get(parameter.property('t'), object))  # append parameter type to the type list
            can_take_extras = False  # <-------------------- by default, function can not take any extra arguments
            if ampersand_found:  # <---------------- if user have specified that function can take extra arguments
                can_take_extras = True  # <- now we set this to true, as the function can now take extra arguments
                SE_ASSERT(where,
                          len(children) - 1 != ampersand_position,
                          'Expression[execute]: fn: you can only mention one alias for the extra arguments tuple')
                SE_ASSERT(where,
                          len(children) - 2 == ampersand_position,
                          'Expression[execute]: fn: you have to mention alias name for the extra arguments tuple')
                names.append(children[-1].token().value())   # append extra args param name to all parameter names
                types.append(tuple)  # <---------------------- append extra args param type to all parameter types
            if not body:
                body = [Nil]  # <-- let a function be defined with empty body, in such a case, it will return None
            integrity_spec_rule = s.Rule(s.Arity(s.AtLeast(positional_parameters_length)
                                                 if can_take_extras else s.Exactly(positional_parameters_length)))

            def handle(*c_arguments, **kwargs):

                """User-function handle object"""

                fn_valid, _, fn_why = integrity_spec_rule.valid(c_arguments)  # first, validate function integrity
                SE_ASSERT(where, fn_valid,                                    f'<anonymous function..>: {fn_why}')

                if can_take_extras:
                    if len(c_arguments) > positional_parameters_length:
                        e_arguments = c_arguments[positional_parameters_length:]
                        c_arguments = c_arguments[:positional_parameters_length] + (e_arguments,)  # new args list
                    else:
                        c_arguments = c_arguments + (tuple(),)  # <- if extras are possible but missing, set to ()

                for arg_value, arg_name, arg_type in zip(c_arguments, names, types):
                    arg_tname = arg_type.__name__
                    arg_value_tname = getattr(arg_value, '__name__', arg_value.__class__.__name__)   # actual name
                    TE_ASSERT(where,
                              isinstance(arg_value, arg_type),
                              f'<anonymous function..>: {arg_name}: {arg_tname} expected, got: {arg_value_tname}')

                fn = {}  # <------------------------------------------------- initialize new execution environment
                fn.update(environ)  # <--------------------------------------------- update it with the global one
                fn.update(dict(zip(names, c_arguments)))  # <-------------- associate parameters with their values
                fn.update({'kwargs': kwargs})  # <-------- update it with keyword arguments passed from a callback
                return [child.execute(fn, False) for child in body][-1]  # <--- return the last calculation result

            handle.x__custom_name__x = '<anonymous function>'  # <-- set function name to the <anonymous function>
            return handle  # <------------------------------------------------- return the function handler object

        if head.token().value() == 'def':
            SE_ASSERT(where, top,   'Expression[execute]: def: can only use (def) form at the top of the program')
            TAIL_IS_VALID(tail, 'def', where,                                   'Expression[execute]: def: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            name, value = tail  # <-------------------------------------------------- assign value as a CommonType
            executed = value.execute(environ, False)  # <-------------------------------- store the executed value
            environ.update({name.token().value(): executed})  # <------------------- assign it to its binding name
            return executed   # <----------------------------------------------------------- return executed value

        if head.token().value() == 'def?':
            SE_ASSERT(where, top, 'Expression[execute]: def?: can only use (def?) form at the top of the program')
            TAIL_IS_VALID(tail, 'def?', where,                                 'Expression[execute]: def?: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            name, value = tail  # <-------------------------------------------------- assign value as a CommonType
            from_env = environ.get(name.token().value()) if (name.token().value() in environ.keys()) else NotFound
            executed = value.execute(environ, False) if from_env is NotFound else from_env  # try to find existing
            environ.update({name.token().value(): executed})  # assign existing/executed value to its binding name
            return executed   # <----------------------------------------------------------- return executed value

        if head.token().value() == 'defn':
            SE_ASSERT(where, top, 'Expression[execute]: defn: can only use (defn) form at the top of the program')
            TAIL_IS_VALID(tail, 'defn', where,                                 'Expression[execute]: defn: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            parameters: Expression  # <--------------------------------- assign parameters as a type of Expression
            name, parameters, *body = tail  # <---------------------------- assign body as the list of CommonTypes
            expected_ret_type = TYPES.get(name.property('t'), object)  # <---- store function expected return type
            expected_ret_tname = expected_ret_type.__name__  # <-- store the name of expected function return type
            names = []  # <------------------------------------------------------ define a list of parameter names
            types = []  # <------------------------------------------------------ define a list of parameter types
            children = parameters.children()  # <---- assign children as the reference to the parameter form items
            ampersand_found = tuple(filter(lambda p: p[1].token().value() == '&', enumerate(children)))   # find &
            ampersand_position: int = ampersand_found[0][0] if ampersand_found else -1  # get '&' position (or -1)
            positional_parameters = children[:ampersand_position] if ampersand_found else children   # positionals
            positional_parameters_length = len(positional_parameters)  # <------------ remember positionals length
            for parameter in positional_parameters:  # <---------------------------- for each positional parameter
                parameter: Literal  # <------------------------------------- assign parameter as a type of Literal
                names.append(parameter.token().value())  # <--------------- append parameter name to the name list
                types.append(TYPES.get(parameter.property('t'), object))  # append parameter type to the type list
            can_take_extras = False  # <-------------------- by default, function can not take any extra arguments
            if ampersand_found:
                can_take_extras = True  # <- now we set this to true, as the function can now take extra arguments
                SE_ASSERT(where,
                          len(children) - 1 != ampersand_position,
                          'Expression[execute]: defn: you can only mention one alias for the extra args\' tuple.')
                SE_ASSERT(where,
                          len(children) - 2 == ampersand_position,
                          'Expression[execute]: defn: you have to mention alias name for the extra args\' tuple.')
                names.append(children[-1].token().value())   # append extra args param name to all parameter names
                types.append(tuple)  # <---------------------- append extra args param type to all parameter types
            if not body:
                body = [Nil]  # <-- let a function be defined with empty body, in such a case, it will return None
            integrity_spec_rule = s.Rule(s.Arity(s.AtLeast(positional_parameters_length)
                                                 if can_take_extras else s.Exactly(positional_parameters_length)))

            def handle(*c_arguments, **kwargs):  # pylint: disable=E0102  # <- handle object couldn't be redefined

                """User-function handle object"""

                fn_valid, _, fn_why = integrity_spec_rule.valid(c_arguments)  # first, validate function integrity
                SE_ASSERT(where, fn_valid,                                    f'{name.token().value()}: {fn_why}')

                if can_take_extras:
                    if len(c_arguments) > positional_parameters_length:
                        e_arguments = c_arguments[positional_parameters_length:]
                        c_arguments = c_arguments[:positional_parameters_length] + (e_arguments,)  # new args list
                    else:
                        c_arguments = c_arguments + (tuple(),)  # <- if extras are possible but missing, set to ()

                for arg_value, arg_name, arg_type in zip(c_arguments, names, types):
                    arg_tname = arg_type.__name__
                    arg_value_tname = getattr(arg_value, '__name__', arg_value.__class__.__name__)   # actual name
                    TE_ASSERT(where,
                              isinstance(arg_value, arg_type),
                              f'{name.token().value()}: {arg_name}: {arg_tname} expected, got: {arg_value_tname}')

                defn = {}  # <----------------------------------------------- initialize new execution environment
                defn.update(environ)  # <------------------------------------------- update it with the global one
                defn.update(dict(zip(names, c_arguments)))  # <------------ associate parameters with their values
                defn.update({'kwargs': kwargs})  # <------ update it with keyword arguments passed from a callback
                retval = [child.execute(defn, False) for child in body][-1]    # store the last calculation result
                actual_ret_tname = getattr(retval, '__name__', retval.__class__.__name__)  # name of retval object
                TE_ASSERT(where,
                          isinstance(retval, expected_ret_type),
                          f'{name.token().value()} have to return: {expected_ret_tname}, not: {actual_ret_tname}')
                return retval  # <--------------------------------------------- return the last calculation result

            handle.x__custom_name__x = name.token().value()  # assign custom function name to display it by pprint
            environ.update({name.token().value(): handle})   # in case of 'defn' we also need to update global env
            return handle  # <------------------------------------------------- return the function handler object

        if head.token().value() == 'defmacro':
            SE_ASSERT(where, top, 'Expression[execute]: defmacro: can only use (defmacro) form on top of program')
            TAIL_IS_VALID(tail, 'defmacro', where,                         'Expression[execute]: defmacro: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            parameters: Expression  # <--------------------------------- assign parameters as a type of Expression
            name, parameters, *body = tail  # <---------------------------- assign body as the list of CommonTypes
            names = []  # <------------------------------------------------------ define a list of parameter names
            types = []  # <------------------------------------------------------ define a list of parameter types
            children = parameters.children()  # <---- assign children as the reference to the parameter form items
            ampersand_found = tuple(filter(lambda p: p[1].token().value() == '&', enumerate(children)))   # find &
            ampersand_position: int = ampersand_found[0][0] if ampersand_found else -1  # get '&' position (or -1)
            positional_parameters = children[:ampersand_position] if ampersand_found else children   # positionals
            positional_parameters_length = len(positional_parameters)  # <------------ remember positionals length
            for parameter in positional_parameters:  # <---------------------------- for each positional parameter
                parameter: Literal  # <------------------------------------- assign parameter as a type of Literal
                names.append(parameter.token().value())  # <--------------- append parameter name to the name list
                types.append(TYPES.get(parameter.property('t'), object))  # append parameter type to the type list
            can_take_extras = False  # <----------------------- by default, macro can not take any extra arguments
            if ampersand_found:
                can_take_extras = True  # <---- now we set this to true, as the macro can now take extra arguments
                SE_ASSERT(where,
                          len(children) - 1 != ampersand_position,
                          'Expression[execute]: defmacro: you can only mention one alias for extra args\' tuple.')
                SE_ASSERT(where,
                          len(children) - 2 == ampersand_position,
                          'Expression[execute]: defmacro: you have to mention alias name for extra args\' tuple.')
                names.append(children[-1].token().value())   # append extra args param name to all parameter names
                types.append(tuple)  # <---------------------- append extra args param type to all parameter types
            if not body:
                body = [Nil]  # <----- let a macro be defined with empty body, in such a case, it will return None
            integrity_spec_rule = s.Rule(s.Arity(s.AtLeast(positional_parameters_length)
                                                 if can_take_extras else s.Exactly(positional_parameters_length)))

            def handle(*c_arguments, **kwargs):  # pylint: disable=E0102  # <- handle object couldn't be redefined

                """User-macro handle object"""

                mc_valid, _, mc_why = integrity_spec_rule.valid(c_arguments)  # <- first, validate macro integrity
                SE_ASSERT(where, mc_valid,                                    f'{name.token().value()}: {mc_why}')

                if can_take_extras:
                    if len(c_arguments) > positional_parameters_length:
                        e_arguments = c_arguments[positional_parameters_length:]
                        c_arguments = c_arguments[:positional_parameters_length] + (e_arguments,)  # new args list
                    else:
                        c_arguments = c_arguments + (tuple(),)  # <- if extras are possible but missing, set to ()

                for arg_value, arg_name, arg_type in zip(c_arguments, names, types):
                    arg_tname = arg_type.__name__
                    arg_value_tname = getattr(arg_value, '__name__', arg_value.__class__.__name__)   # actual name
                    TE_ASSERT(where,
                              isinstance(arg_value, arg_type),
                              f'{name.token().value()}: {arg_name}: {arg_tname} expected, got: {arg_value_tname}')

                defmacro = {}  # <------------------------------------------- initialize new execution environment
                defmacro.update(environ)  # <--------------------------------------- update it with the global one
                defmacro.update(dict(zip(names, c_arguments)))  # <-------- associate parameters with their values
                defmacro.update({'kwargs': kwargs})  # <-- update it with keyword arguments passed from a callback
                return deepcopy([child.execute(defmacro, False) for child in body][-1])   # return the last result

            handle.x__custom_name__x = name.token().value()  # <- assign custom macro name to display it by pprint
            handle.x__its_a_macro__x = True  # <-- set the `macro` flag, thus it couldn't be treated as a function
            environ.update({name.token().value(): handle})   # in case of 'defmacro', we need to update global env
            return handle  # <---------------------------------------------------- return the macro handler object

        if head.token().value() == 'import':
            SE_ASSERT(where, top,    'Expression[execute]: import: you should place all the (import)s at the top')
            TAIL_IS_VALID(tail, 'import', where,                             'Expression[execute]: import: {why}')
            name: Literal = tail[0]  # <----------------------------------------- assign name as a type of Literal
            alias: str = name.token().value()  # <--------------- get the alias (avoid name variable redefinition)
            parts = alias.split('.')  # <---------------- split the importable module name into a list by '.' char
            unqualified = parts[-1]  # <----------------- store the unqualified name of importable Python 3 module
            identifiers = iter(parts[1:])  # <----------------- make it possible to iterate over parts with next()
            module = __import__(alias)  # <-------------------------- import Python 3 module by its qualified name
            while module.__name__.split('.')[-1] != unqualified:  # while unqualified doesn't match an object name
                module = getattr(module, next(identifiers), None)  # lookup for an object inside of current object
            environ[unqualified] = module  # <---------------- assign module object to the unqualified module name
            return None  # <----------------------------------------------------------------------- and return nil

        if head.token().value() == 'require':
            SE_ASSERT(where, top,  'Expression[execute]: require: you should place all the (require)s at the top')
            TAIL_IS_VALID(tail, 'require', where,                           'Expression[execute]: require: {why}')
            name: Literal = tail[0]  # <----------------------------------------- assign name as a type of Literal
            module = type(name.token().value(),  (object,),  environ.get('require')(name.token().value() + '.cl'))
            environ[name.token().value().split('/')[-1]] = module  # <- assign module object to a unqualified name
            return None  # <----------------------------------------------------------------------- and return nil

        handle = head.execute(environ, False)  # resolve handle object by its name, this could raise a 'NameError'

        if hasattr(handle, 'x__its_a_macro__x'):  # <---------------------- if the user have invoked macro handler
            questionable = handle(*tuple(tail))   # <- 'expand' the macro by executing it using global environment
            if isinstance(questionable, (Literal,
                                         Expression)):  # <- if macro handler have generated expression or literal
                questionable.unquote()  # <- unquote it recursively, in case of Expression; could also be unquoted
                return questionable.execute(environ, False)  # <- execute 'expanded & unquoted' expression/literal
            return questionable  # <-- if macro handler have generated arbitrary Python 3 value, return it *as is*
        return handle(*tuple(map(lambda argument: argument.execute(environ,  False),  tail)))  # return the result
