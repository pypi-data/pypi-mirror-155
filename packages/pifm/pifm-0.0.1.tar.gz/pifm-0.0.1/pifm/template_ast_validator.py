import ast
import sys
from pathlib import Path
from .pifm_errors import raise_pifm_error, format_code_block


class TemplateValidator(ast.NodeVisitor):
    def __init__(self, file_path, template_path, *args, **kwargs):
        self.file_path = Path(file_path)
        self.template_path = Path(template_path)

        self.file_text = self.file_path.read_text()
        self.template_text = self.template_path.read_text()

        self.file_ast = ast.parse(self.file_text)
        self.template_ast = ast.parse(self.template_text)

        self.valid_ast = self.template_ast.body

        self.node_parent = None

        super().__init__(*args, **kwargs)

    def validate(self):
        self.visit(self.file_ast)

    def generic_visit(self, node):
        old_node = self.node_parent
        self.node_parent = node
        super().generic_visit(node)
        self.node_parent = old_node

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

    @staticmethod
    def are_ast_trees_equal(tree1, tree2):
        if isinstance(tree1, list):
            tree1 = [ast.dump(node, include_attributes=False) for node in tree1]
        else:
            tree1 = ast.dump(tree1, include_attributes=False)

        if isinstance(tree2, list):
            tree2 = [ast.dump(node, include_attributes=False) for node in tree2]
        else:
            tree2 = ast.dump(tree2, include_attributes=False)

        return tree1 == tree2

    def parent_starts_with_functions_like(self, comparison_node):
        parent = self.node_parent
        for node in parent.body:
            if self.are_ast_trees_equal(node, comparison_node):
                return True

            if not isinstance(node, type(comparison_node)):
                return False

            if node.value.func.id != comparison_node.value.func.id:
                return False

        raise ValueError("It should not be possible for comparison_node to not be in the parent.")


    def visit_FunctionDef(self, node):
        top_level_functions = dict([
            (ast_node.name, ast_node)
            for ast_node in self.valid_ast
            if type(ast_node) == ast.FunctionDef
        ])
        if node.name not in top_level_functions:
            return

        current_function = top_level_functions[node.name]

        if not self.are_ast_trees_equal(node.args, current_function.args):
            self.raise_error_for_node(
                node,
                f"The function {node.name}'s arguments were not what was expected.\n"
                f"Check the arguments of that function are the same as the starter code."
            )

        containing_valid_ast = self.valid_ast
        self.valid_ast = current_function.body
        self.generic_visit(node)

        if self.valid_ast:
            self.raise_error_for_node(
                node,
                f"You are missing starter code that pifm expected you would have.\n"
                f"Make sure your code includes everything from the starter code."
            )
        else:
            containing_valid_ast.remove(current_function)
            self.valid_ast = containing_valid_ast

    def visit_Expr(self, node):
        if not self.valid_ast:
            # If we don't have any ast to validate, we can return.
            return

        if type(node.value) != ast.Call:
            # If we're not calling a function, we're all good.
            return

        if isinstance(self.node_parent, ast.Module):
            # We should ignore exprs that are in the root module
            return

        function_name = node.value.func.id

        valid_ast_node = self.valid_ast[0]
        valid_ast_node_name = valid_ast_node.value.func.id

        if valid_ast_node_name != function_name:
            return

        if not self.are_ast_trees_equal(node.value.args, valid_ast_node.value.args):
            self.raise_error_for_node(
                node,
                f"Pifm expected you to have a {valid_ast_node_name} call here that matched the starter code.\n"
                f"What you provided did not match the starter code."
            )

        if valid_ast_node_name == 'requires':
            if not isinstance(self.node_parent, ast.FunctionDef) or not self.parent_starts_with_functions_like(node):
                self.raise_error_for_node(
                    node,
                    f"You must always have your `requires` function at the start of a function's body."
                )

        if valid_ast_node_name == 'holds_invariant':
            if not type(self.node_parent) in [ast.While, ast.For] or not self.parent_starts_with_functions_like(node):
                self.raise_error_for_node(
                    node,
                    f"You must always have your `holds_invariant` function at the start of a function's body."
                )

        self.valid_ast.remove(valid_ast_node)
