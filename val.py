#! /usr/bin/env python
"""
Show value of a fully-qualified symbol (in a module or builtins).

Usage:
    pyval [-r] [EXPR]...

Options:
    -r, --repr              Print `repr()` of object
    -pp, --pprint           Pretty-print using pprint

Examples:
    $ pyval sys.platform
    linux

    $ pyval math.pi**2
    9.869604401089358

    $ pyval 'math.sin(math.pi/4)'
    0.7071067811865475
"""

__version__ = '0.0.2'

import ast
import argparse
from pprint import pprint


def eval_(expr):
    """Eval an expression, resolve names by importing modules as necessary.
    Returns the resulting value."""
    locals = {}
    NameResolver(locals).visit(ast.parse(expr))
    return eval(expr, locals)


class NameResolver(ast.NodeVisitor):

    """Resolve names within the given expression and updates ``locals`` with
    the imported modules."""

    def __init__(self, locals):
        super(NameResolver, self).__init__()
        self.locals = locals

    def visit_Name(self, node):
        resolve(node.id, self.locals)

    def visit_Attribute(self, node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.insert(0, node.id)
            resolve('.'.join(parts), self.locals)
        else:
            # We landed here due to an attribute access on some other
            # expression (function call, literal, tuple, etc…), and must
            # recurse in order to handle attributes or names within this
            # subexpression:
            self.visit(node)


def resolve(symbol, locals):
    """Resolve a fully-qualified name by importing modules as necessary.
    Returns the object referenced by the name."""
    parts = symbol.split('.')
    for i in range(len(parts)):
        name = '.'.join(parts[:i+1])
        try:
            exec_('import ' + name, locals, locals)
        except ImportError:
            break
    return eval(symbol, locals)


def exec_(source, globals, locals):
    """Execute the given source string. This is a thin wrapper over ``exec``
    needed for python2 compatibility, where exec is a statement with
    restrictions on the scope in which it can be used."""
    exec(source, globals, locals)


def main(args=None):
    """Show the value for all given expressions."""
    parser = argument_parser()
    args = parser.parse_args()
    for expr in args.EXPRS:
        value = eval_(expr)
        if args.repr:
            print(repr(value))
        elif args.pprint:
            pprint(value)
        else:
            print(value)


def argument_parser():
    """Create parser for this script's command line arguments."""
    parser = argparse.ArgumentParser(
        description='Show value of given expressions, resolving names as'
        ' necessary through module imports.')
    parser.add_argument('--repr', '-r', action='store_true',
                        help='Print repr() of object')
    parser.add_argument('--pprint', '-pp', action='store_true',
                        help='Pretty-print using pprint')
    parser.add_argument('EXPRS', nargs='+', help='Expressions to be evaluated')
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
