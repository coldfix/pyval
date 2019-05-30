#! /usr/bin/env python
"""
Show value of a fully-qualified symbol (in a module or builtins).

Usage:
    pyval [-r] [EXPR]...

Options:
    -r, --repr              Print `repr()` of object

Examples:
    $ pyval math.pi
    3.141592653589793

    $ pyval sys.platform
    linux
"""

import argparse


def resolve(symbol):
    """Resolve a fully-qualified name by importing modules as necessary.
    Returns the object referenced by the name."""
    locals = {}
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
        value = resolve(expr)
        if args.repr:
            print(repr(value))
        else:
            print(value)


def argument_parser():
    """Create parser for this script's command line arguments."""
    parser = argparse.ArgumentParser(
        description='Show value of a fully-qualified symbol (in a module or builtins).')
    parser.add_argument('--repr', '-r', action='store_true',
                        help='Print repr() of object')
    parser.add_argument('EXPRS', nargs='+', help='Symbols to be resolved')
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
