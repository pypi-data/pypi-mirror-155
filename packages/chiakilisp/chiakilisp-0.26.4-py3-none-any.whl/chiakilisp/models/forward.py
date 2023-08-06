# pylint: disable=arguments-renamed
# pylint: disable=too-few-public-methods

"""Forward declaration of some models"""

from chiakilisp.models.token import Token


class CommonType:

    """Forward declaration for both models"""

    _properties: dict

    def lint(self,                         # pylint: disable=too-many-arguments
             env: dict,
             rule: str,
             storage: dict,
             error: list,
             places: dict) -> None:

        """Just to define 'lint()' signature"""

    def execute(self, env: dict, top: bool):

        """Just to define 'execute()' signature"""

    def set_properties(self, _properties: list) -> None:

        """Converts the properties list to a dictionary of them"""

        self._properties = dict(map(lambda prop: prop.split(':'), _properties))

    def property(self, name: str, default=None) -> str:

        """Returns a property by its name"""

        return self._properties.get(name, default)

    def properties(self) -> dict:

        """Returns properties"""

        return self._properties

    def quoted(self) -> bool:

        """Returns whether is quoted or not"""

        return bool(self.properties().get('quoted'))


class LiteralType(CommonType):

    """Forward declaration for Literal model"""

    def token(self) -> Token:

        """Just to define 'token()' signature"""

    def wrapped(self) -> str:

        """Just to define 'wrapped()' signature"""


class ExpressionType(CommonType):

    """Forward declaration for Expression model"""

    def wrapped(self) -> str:

        """Just to define 'wrapped()' signature"""

    def children(self) -> list:

        """Just to define 'children()' signature"""
