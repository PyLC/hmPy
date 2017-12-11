hmPy
====

|travis| |docs| |pypi|

Purpose
-------

hmPy is a Python library for building HMIs.

Installing hmPy
---------------

To install the latest version of hmPy using pip::

    $ pip install hmPy

Running Tests
-------------
hmPy's test suite can be run using ``tox``::

    $ tox

Note that pep8 compliance is required for the tests to pass.

Example Code
------------
For those of you who want to hit the ground running::

    from hmpy import Interface
    from hmpy.views import ButtonView, LCDView

    # Create the base interface
    hmi = Interface()

    # Initialize counter to 0
    count = 0

    # Initialize an LCD View and a button View
    lcd = LCDView()
    btn = ButtonView("Increment")

    def increment_count():
        lcd.value += 1

    # Call the increment count method whenever the button is pressed
    btn.on_press(increment_count)

    # Add the views to the interface
    hmi.add_view(lcd)
    hmi.add_view(btn)

    # Launch the interface
    hmi.start()

For more detailed documentation and advanced examples, see the full documentation.

Documentation
-------------

Full documentation and tutorial available at `Read the Docs`_.

.. _Read The Docs: https://pylc-hmpy.readthedocs.io

.. |docs| image:: https://readthedocs.org/projects/pylc-hmpy/badge/?version=latest
    :target: https://pylc-hmpy.readthedocs.io/en/latest/?badge=latest

.. |travis| image:: https://travis-ci.org/PyLC/hmPy.svg?branch=master
    :target: https://travis-ci.org/PyLC/hmPy

.. |pypi| image:: https://badge.fury.io/py/hmPy.svg
    :target: https://pypi.python.org/pypi/hmPy/
