pipin
=====

Let's *pipin*!

pipin is a little Python script to search for a given app within your dependencies.
It simply searches in your project's requirements file (yes, it leaves the 'pip freeze' alone).
You could probably handle same needs with ack or grep, but pipin is less characters to write, colorizes the output nicely etc.

.. image:: https://travis-ci.org/mattack108/pipin.png?branch=master
   :target: https://travis-ci.org/mattack108/pipin

.. image:: https://pypip.in/v/pipin/badge.png
   :target: https://pypi.python.org/pypi/pipin

.. image:: https://pypip.in/d/pipin/badge.png
   :target: https://pypi.python.org/pypi/pipin

Requirements
------------

- Python 2.6, 2.7, 3.2 or 3.3
- `argparse <https://pypi.python.org/pypi/argparse>`_ if py2.6

Installation
------------

To install ``pipin``, simply run: ::

    sudo pip install pipin

Note: you probably want to install it as sudo in order to *pipin everywhere*.

Usage
-----

Just tell *what* and *where* you want to pipin: ::

    pipin Django==1.4.2 .

This will search for "Django==1.4.2" in requirements.txt file in current directory (because ".").

Different requirements file? Not a problem! ::

    pipin Django==1.4.2 . -f dev_requirements.txt

You might also need to search for multiple apps at once. Then do: ::

    pipin Django==1.4.2 South .


This is pretty beta, so means it is probably broken. If so, please report any bugs
as issues or PRs.

