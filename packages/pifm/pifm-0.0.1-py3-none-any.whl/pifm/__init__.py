# Welcome to pifm (python in-formal methods), a wrapper for COMP6721
#
# The actions of this file break down into five parts:
# A: Introucing some new concepts to python (`requires`, `ensures`,
#    `holds_invariant`); and checking the importing code
#    uses them appropriately.
#
# B: Only allowing some python features in the calling file to ensure
#    students use a "pseudo-code" like function. Status: DONE.
#
# C: For named functions (i.e. ones the student has explicitly been asked to write);
#    we can use hypothesis testing to find assertion failures; by removing our
#    invariants. [EXPERIMENTALLY] We can even explore using students' `requires` functions as
#    predicates for hypothesis testing.
#
# D: Providing a simple utility that makes iFM a bit easier:
#     * Array
#
# E: [NOT DONE YET] using mypy to make sure we have types for students functions.

FILE_AST = None

import ast
import inspect
import os
import pathlib
import sys

from collections import defaultdict

from .astpp import dump as astpp_dump
from .array import Array
from .template_ast_validator import TemplateValidator
from .usage_ast_validator import UsageValidator

class PifmAssertionError(AssertionError):
    def __init__(self, message, info_tuple=(None, None)):
        self.message = message
        self.name, self.calling_function = info_tuple

    def as_tuple(self):
        return (self.name, self.calling_function)

    def __repr__(self):
        return f"PifmAssertionError<name={self.name}, calling_function={self.calling_function}>"

_ignored_assertions = []
_assertion_stats = defaultdict(lambda: 0)

def _ignore_assertion(assertion_tuple):
    print(_ignored_assertions)
    _ignored_assertions.append(assertion_tuple)

def _real_assert(assertion_name, arg):
    function_name = inspect.stack()[1].function
    assertion_tuple = (assertion_name, function_name)
    _assertion_stats[assertion_tuple] += 1
    if not arg and assertion_tuple not in _ignored_assertions:
        raise PifmAssertionError(
            f"Assertion {assertion_name} failed in function {function_name}.",
            info_tuple=assertion_tuple
        )

requires = _real_assert
ensures = _real_assert
holds_invariant = _real_assert


def pifm_initialise(template_name):
    """
    This function is  used to ensure elements A and B. It validates the entire
    AST of the called file.
    """
    calling_module_path = inspect.stack()[1].filename

    UsageValidator(calling_module_path).validate()

    current_path = pathlib.Path(__file__).parent.resolve()

    env_template_folder = os.getenv("PIFM_TEMPLATES_FOLDER")
    if env_template_folder:
        template_folder = pathlib.Path(env_template_folder)
    else:
        template_folder = current_path / "templates"

    template_path = template_folder / f"{template_name}.py"
    if not template_path.exists():
        print(f"pifm could not find the template {template_name}", file=sys.stderr)
        print(f"\tCheck your call to `pifm_initialise()`", file=sys.stderr)
        sys.exit(1)

    TemplateValidator(calling_module_path, template_path).validate()
