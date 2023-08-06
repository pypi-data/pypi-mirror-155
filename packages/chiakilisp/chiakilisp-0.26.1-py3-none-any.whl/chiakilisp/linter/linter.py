# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

from chiakilisp.parser import Children

# Rules implemented right now:
#  - UnusedGlobalVariables - check the source code for unused global variables

# User could define Rules dictionary in their ~/.chiakilang-linter-rc.cl file:
# (def config {"Rules" [... ]}), where each ... is a string (name of the rule)

# For example: ```lisp\n (def config {"Rules" ["UnusedGlobalVariables"]})\n```

_DEFAULTS = {
    'Rules': []  # no rules enabled by default, user should edit their rc file
}


class BuiltinLinter:

    """ChiakiLisp Linter"""

    _env: dict
    _wood: Children
    _errors: list
    _places: dict
    _config: dict
    _report: dict
    _global_variables_counts: dict

    def __init__(self, wood: Children, env: dict, config: dict = None) -> None:

        """Initializes a built-in BuiltinLinter class"""

        self._env = env
        self._wood = wood
        self._errors = []
        self._places = {}
        self._global_variables_counts = {}
        self._report = {
            'UnusedGlobalVariables': []
        }
        self._config = config or _DEFAULTS

    def find(self, kind: str, name: str) -> tuple or None:

        """Find position in file by kind, name; or None"""

        for pos, (inner_kind, inner_name) \
                in self._places.items():
            if kind == inner_kind \
                    and name == inner_name:
                return pos
        return None

    def report(self) -> dict:

        """Return built linter report"""

        return self._report

    def fancy_print_report(self) -> None:

        """Fancy print generated report"""

        if not self._config.get('Rules'):
            print('There are no rules to run/report')

        for pos, why in self._errors:
            print('ERR', ':'.join(map(str, pos)), '=>')
            print('    :::', why)

        for rule in self._config.get('Rules'):
            print(f'>>> {rule}')
            body = self.report().get(rule)
            if not body:
                print('    ::: Nothing to report here')
            else:
                self._fancy_print_report_for_rule(rule)

    def _fancy_print_report_for_rule(self, rule) -> None:

        """Print the fancy report for the concrete rule"""

        if rule == 'UnusedGlobalVariables':
            self._fancy_print_report_for_unused_global_variables()

    def _fancy_print_report_for_unused_global_variables(self) -> None:

        for each in self._report.get('UnusedGlobalVariables'):
            print(f'    ::: global variable \'{each}\' is not used anywhere')

    def run(self) -> None:

        """Run all implemented linter rules"""

        if 'UnusedGlobalVariables' in self._config.get('Rules'):
            self._run_check_for_unused_global_variables()

    def _run_check_for_unused_global_variables(self) -> None:

        """Rule that iterates over the wood to check for unused global variables"""

        storage = self._global_variables_counts

        for each in self._wood:
            each.lint(self._env, 'UnusedGlobalVariables',
                      storage, self._errors, self._places)

        for global_variable_name, global_variable_refer_count in storage.items():
            if not global_variable_refer_count:
                self._report['UnusedGlobalVariables'].append(global_variable_name)
