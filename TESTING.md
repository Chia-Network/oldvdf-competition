Set up your virtual environments as in the README.md.

Install pytest into your virtualenv:

    $ pip install pytest

Run all tests with:

    $ py.test tests

Use -s to view output from print statements (normally suppressed by py.test)

    $ py.test -s tests

You can run a subset of tests with something like:

    $ py.test tests/test_classgroup.py

There are text-based tests implemented in tests/test_cmds.py that use input
in tests/pot/. You can add easily add more tests of the command-line in here.
If the output of the tool changes, you can easily repairs these tests using
something like

    $ REPAIR_FAILURES=1 py.test tests/test_cmds.py
