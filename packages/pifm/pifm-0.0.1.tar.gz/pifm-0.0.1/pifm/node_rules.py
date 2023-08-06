import ast

"""
Stolen from the python documentation: https://docs.python.org/3.7/library/ast.html
We then copy this in below.

mod = Module(stmt* body)
        | Interactive(stmt* body)
        | Expression(expr body)

        -- not really an actual node but useful in Jython's typesystem.
        | Suite(stmt* body)

    stmt = FunctionDef(identifier name, arguments args,
                       stmt* body, expr* decorator_list, expr? returns)
          | AsyncFunctionDef(identifier name, arguments args,
                             stmt* body, expr* decorator_list, expr? returns)

          | ClassDef(identifier name,
             expr* bases,
             keyword* keywords,
             stmt* body,
             expr* decorator_list)
          | Return(expr? value)

          | Delete(expr* targets)
          | Assign(expr* targets, expr value)
          | AugAssign(expr target, operator op, expr value)
          -- 'simple' indicates that we annotate simple name without parens
          | AnnAssign(expr target, expr annotation, expr? value, int simple)

          -- use 'orelse' because else is a keyword in target languages
          | For(expr target, expr iter, stmt* body, stmt* orelse)
          | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse)
          | While(expr test, stmt* body, stmt* orelse)
          | If(expr test, stmt* body, stmt* orelse)
          | With(withitem* items, stmt* body)
          | AsyncWith(withitem* items, stmt* body)

          | Raise(expr? exc, expr? cause)
          | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
          | Assert(expr test, expr? msg)

          | Import(alias* names)
          | ImportFrom(identifier? module, alias* names, int? level)

          | Global(identifier* names)
          | Nonlocal(identifier* names)
          | Expr(expr value)
          | Pass | Break | Continue

          -- XXX Jython will be different
          -- col_offset is the byte offset in the utf8 string the parser uses
          attributes (int lineno, int col_offset)

          -- BoolOp() can use left & right?
    expr = BoolOp(boolop op, expr* values)
         | BinOp(expr left, operator op, expr right)
         | UnaryOp(unaryop op, expr operand)
         | Lambda(arguments args, expr body)
         | IfExp(expr test, expr body, expr orelse)
         | Dict(expr* keys, expr* values)
         | Set(expr* elts)
         | ListComp(expr elt, comprehension* generators)
         | SetComp(expr elt, comprehension* generators)
         | DictComp(expr key, expr value, comprehension* generators)
         | GeneratorExp(expr elt, comprehension* generators)
         -- the grammar constrains where yield expressions can occur
         | Await(expr value)
         | Yield(expr? value)
         | YieldFrom(expr value)
         -- need sequences for compare to distinguish between
         -- x < 4 < 3 and (x < 4) < 3
         | Compare(expr left, cmpop* ops, expr* comparators)
         | Call(expr func, expr* args, keyword* keywords)
         | Num(object n) -- a number as a PyObject.
         | Str(string s) -- need to specify raw, unicode, etc?
         | FormattedValue(expr value, int? conversion, expr? format_spec)
         | JoinedStr(expr* values)
         | Bytes(bytes s)
         | NameConstant(singleton value)
         | Ellipsis
         | Constant(constant value)

         -- the following expression can appear in assignment context
         | Attribute(expr value, identifier attr, expr_context ctx)
         | Subscript(expr value, slice slice, expr_context ctx)
         | Starred(expr value, expr_context ctx)
         | Name(identifier id, expr_context ctx)
         | List(expr* elts, expr_context ctx)
         | Tuple(expr* elts, expr_context ctx)

          -- col_offset is the byte offset in the utf8 string the parser uses
          attributes (int lineno, int col_offset)

    expr_context = Load | Store | Del | AugLoad | AugStore | Param

    slice = Slice(expr? lower, expr? upper, expr? step)
          | ExtSlice(slice* dims)
          | Index(expr value)

    boolop = And | Or

    operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift
                 | RShift | BitOr | BitXor | BitAnd | FloorDiv

    unaryop = Invert | Not | UAdd | USub

    cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

    # ... The rest is included in other things, and therefore
    # doesn't require checking.
}
"""

from enum import Enum

class Rules(Enum):
    DISALLOWED = 0
    ALLOWED = 1
    UNKNOWN = 2

# This is manually crafted to rules that seemed sensible to me. ~tfpk
NODE_RULES = {
    # mod:
    ast.Module: Rules.ALLOWED,
    ast.Interactive: Rules.ALLOWED,
    ast.Expression: Rules.DISALLOWED,

    # stmt:
    ast.FunctionDef: Rules.ALLOWED,
    ast.AsyncFunctionDef: Rules.DISALLOWED,
    ast.ClassDef: Rules.DISALLOWED,
    ast.Return: Rules.ALLOWED,

    ast.Delete: Rules.ALLOWED,
    ast.Assign: Rules.ALLOWED,
    ast.AugAssign: Rules.ALLOWED,
    ast.AnnAssign: Rules.ALLOWED,

    ast.For: Rules.ALLOWED,
    ast.AsyncFor: Rules.DISALLOWED,
    ast.While: Rules.ALLOWED,
    ast.If: Rules.ALLOWED,
    ast.With: Rules.DISALLOWED,
    ast.AsyncWith: Rules.DISALLOWED,

    ast.Raise: Rules.DISALLOWED,
    ast.Try: Rules.DISALLOWED,
    ast.Assert: Rules.DISALLOWED,

    ast.Import: Rules.ALLOWED,
    ast.ImportFrom: Rules.ALLOWED,

    ast.Global: Rules.DISALLOWED,
    ast.Nonlocal: Rules.DISALLOWED,
    ast.Expr: Rules.ALLOWED,
    ast.Pass: Rules.ALLOWED,
    ast.Break: Rules.ALLOWED,
    ast.Continue: Rules.ALLOWED,

    # expr:
    ast.BoolOp: Rules.ALLOWED,
    ast.BinOp: Rules.ALLOWED,
    ast.UnaryOp: Rules.ALLOWED,
    ast.Lambda: Rules.DISALLOWED,
    ast.IfExp: Rules.ALLOWED,
    ast.Dict: Rules.ALLOWED,
    ast.Set: Rules.ALLOWED,
    ast.ListComp: Rules.DISALLOWED,
    ast.SetComp: Rules.DISALLOWED,
    ast.DictComp: Rules.DISALLOWED,
    ast.GeneratorExp: Rules.DISALLOWED,
    ast.Await: Rules.DISALLOWED,
    ast.Yield: Rules.DISALLOWED,
    ast.YieldFrom: Rules.DISALLOWED,
    ast.Compare: Rules.ALLOWED,
    ast.Call: Rules.ALLOWED,
    ast.Num: Rules.ALLOWED,
    ast.Str: Rules.ALLOWED,
    ast.FormattedValue: Rules.ALLOWED,
    ast.JoinedStr: Rules.ALLOWED,
    ast.Bytes: Rules.ALLOWED,
    ast.NameConstant: Rules.ALLOWED,
    ast.Ellipsis: Rules.ALLOWED,
    ast.Constant: Rules.ALLOWED,

    ast.Attribute: Rules.ALLOWED,
    ast.Subscript: Rules.ALLOWED,
    ast.Starred: Rules.ALLOWED,
    ast.Name: Rules.ALLOWED,
    ast.List: Rules.ALLOWED,
    ast.Tuple: Rules.ALLOWED,

    ast.Load: Rules.ALLOWED,
    ast.Store: Rules.ALLOWED,
    ast.Del: Rules.ALLOWED,
    ast.AugLoad: Rules.ALLOWED,
    ast.AugStore: Rules.ALLOWED,
    ast.Param: Rules.ALLOWED,

    ast.Slice: Rules.ALLOWED,
    ast.ExtSlice: Rules.ALLOWED,
    ast.Index: Rules.ALLOWED,

    ast.And: Rules.ALLOWED,
    ast.Or: Rules.ALLOWED,

    ast.Add: Rules.ALLOWED,
    ast.Sub: Rules.ALLOWED,
    ast.Mult: Rules.ALLOWED,
    ast.MatMult: Rules.ALLOWED,
    ast.Div: Rules.ALLOWED,
    ast.Mod: Rules.ALLOWED,
    ast.Pow: Rules.ALLOWED,
    ast.LShift: Rules.ALLOWED,
    ast.RShift: Rules.ALLOWED,
    ast.BitOr: Rules.ALLOWED,
    ast.BitXor: Rules.ALLOWED,
    ast.BitAnd: Rules.ALLOWED,
    ast.FloorDiv: Rules.ALLOWED,

    ast.Invert: Rules.ALLOWED,
    ast.Not: Rules.ALLOWED,
    ast.UAdd: Rules.ALLOWED,
    ast.USub: Rules.ALLOWED,

    ast.Eq: Rules.ALLOWED,
    ast.NotEq: Rules.ALLOWED,
    ast.Lt: Rules.ALLOWED,
    ast.LtE: Rules.ALLOWED,
    ast.Gt: Rules.ALLOWED,
    ast.GtE: Rules.ALLOWED,
    ast.Is: Rules.ALLOWED,
    ast.IsNot: Rules.ALLOWED,
    ast.In: Rules.ALLOWED,
    ast.NotIn: Rules.ALLOWED,

    ast.comprehension: Rules.ALLOWED,
    ast.excepthandler: Rules.ALLOWED,
    ast.arguments: Rules.ALLOWED,
    ast.arg: Rules.ALLOWED,
    ast.keyword: Rules.ALLOWED,
    ast.alias: Rules.ALLOWED,
    ast.withitem: Rules.ALLOWED,
}

def get_rule_for_node(node):
    return NODE_RULES.get(type(node), Rules.UNKNOWN)
