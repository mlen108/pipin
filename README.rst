pipin
=====

Let's *pipin*!

``pipin`` is a little Python script to search for a given app(s) within your project's dependencies.

You could probably handle same needs with ``ack`` or ``grep``, but ``pipin`` is less characters to write, colorizes the output nicely etc.

.. image:: https://img.shields.io/pypi/v/pipin.svg
  :target: https://pypi.python.org/pypi/pipin/

.. image:: https://travis-ci.org/mattack108/pipin.svg?branch=master
  :target: https://travis-ci.org/mattack108/pipin

.. image:: https://coveralls.io/repos/mattack108/pipin/badge.png?branch=master
  :target: https://coveralls.io/r/mattack108/pipin?branch=master

.. image:: https://img.shields.io/pypi/dm/pipin.svg
  :target: https://pypi.python.org/pypi/pipin/

Requirements
------------

- Python 2.6+ or 3.3+
- `argparse <https://pypi.python.org/pypi/argparse>`_ if py2.6

Installation
------------

To install ``pipin``, simply run: ::

    sudo pip install pipin

Note: you probably want to install it as sudo in order to *pipin everywhere*.

Usage
-----

Go to folder where all your projects are stored: ::

    cd /home/projects/

Just tell *what* and *where* you want to pipin: ::

    pipin Django==1.4.2 .

This will search for "Django==1.4.2" in requirements.txt file in current directory (because ".").

Search within specific project only? Not a problem! ::

    pipin Django==1.4.2 /path/to/project/

Different requirements file? Not a problem too! ::

    pipin Django==1.4.2 . -f dev_requirements.txt

You might also need to search for multiple apps at once. Then do: ::

    pipin Django==1.4.2 South .

Also, literal asterisk (*) is supported: ::

    pipin Django*1.4 .

This will find occurences of ``Django==1.4`` and ``Django>=1.4`` as they are
both valid.
