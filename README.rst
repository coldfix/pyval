pyval
=====

Show the value of a python object via command line.

Examples:

.. code-block:: bash

    $ pyval sys.platform
    linux

This is meant to provide a more convenient alternative to:

.. code-block:: bash

    python -c "import sys; print(sys.platform)"

More complex expressions are possible too:

.. code-block:: bash

    $ pyval math.pi**2
    9.869604401089358

    $ pyval 'math.sin(math.pi/4)'
    0.7071067811865475


Installation
------------

The utility can be installed as follows::

    pip install --user eval

It is also possible to simply download ``val.py`` and symlink or move under
the name of your choice into your PATH, e.g.:

.. code-block:: bash

    wget https://raw.githubusercontent.com/coldfix/pyval/master/val.py \
        -O ~/.local/bin/pyval

Once either of these is done, it can be used within any python enviroment on
your system, as long as it is accessible in PATH.

By default it uses the currently activated environment. In order to use it
with unactivated python interpreter, you currently have to call the
interpreter manually as follows::

    /path/to/python ~/.local/bin/pyval 'math.sin(math.sin/3)'

This module is kept deliberately simple and avoids any dependencies not in the
standard library. This allows running the script in any python environment
once it is installed on the system, without having to install it in each
environment individually.
