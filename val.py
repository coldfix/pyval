#! /usr/bin/env python
"""
Show value of a fully-qualified symbol (in a module or builtins).

Usage:
    pyval [EXPR]...

Examples:
    $ pyval math.pi
    3.141592653589793

    $ pyval sys.platform
    linux
"""


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


def main(*expressions):
    """Show the value for all given expressions."""
    for expr in expressions:
        print(resolve(expr))


if __name__ == '__main__':
    import sys
    sys.exit(main(*sys.argv[1:]))
