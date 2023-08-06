import ast
import sys
from pathlib import Path
from .node_rules import get_rule_for_node, Rules
from .pifm_errors import raise_pifm_error, format_code_block

class UsageValidator(ast.NodeVisitor):
    def __init__(self, file_path, *args, **kwargs):
        self.file_path = Path(file_path)
        self.file_text = self.file_path.read_text()
        self.file_ast = ast.parse(self.file_text)
        super().__init__(*args, **kwargs)

    def validate(self):
        self.generic_visit(self.file_ast)

    def raise_error_for_node(self, node, error_note):
        code_block = format_code_block(
            "The location where the error occured is shown below",
            self.file_text,
            self.file_path,
            node.lineno,
            node.col_offset,
            node.end_lineno,
            node.end_col_offset
        )

        raise_pifm_error(error_note, blocks=[code_block])

    def generic_visit(self, node):
        rule_for_node = get_rule_for_node(node)
        if rule_for_node == Rules.DISALLOWED:
            self.raise_error_for_node(node, f"pifm does not allow the use of {type(node).__name__}.")
        elif rule_for_node == Rules.UNKNOWN:
            self.raise_error_for_node(
                node,
                f"pifm does not know what a {type(node).__name__} node is.\n"
                f"It is likely this is a bug with pifm, please let the maintainers know."
            )
        super().generic_visit(node)
