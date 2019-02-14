============
pytest-check
============

A pytest plugin that allows multiple failures per test.

----

This `Pytest`_ plugin was a rewrite and a rename of `pytest-expect`_.



Installation
------------

From PPI:

.. code-block:: bash

    $ pip install pytest-check

Or from github.

.. code-block:: bash
    $ pip install git+https://github.com/okken/pytest-check


Usage
-----

For example test case code:

.. code-block:: python

    import pytest_check as check


    def test_example():
        a = 1
        b = 2
        c = [2, 4, 6]
        check.greater(a, b)
        check.less_equal(b, a)
        check.is_in(a, c, "Is 1 in the list")
        check.is_not_in(b, c, "make sure 2 isn't in list")

Test results:

.. code-block:: bash

    =================================== FAILURES ===================================
    _________________________________ test_example _________________________________
    FAILURE:
    assert 1 > 2
      test_check.py, line 14, in test_example() -> check.greater(a, b)
    FAILURE:
    assert 2 <= 1
      test_check.py, line 15, in test_example() -> check.less_equal(b, a)
    FAILURE: Is 1 in the list
    assert 1 in [2, 4, 6]
      test_check.py, line 16, in test_example() -> check.is_in(a, c, "Is 1 in the list")
    FAILURE: make sure 2 isn't in list
    assert 2 not in [2, 4, 6]
      test_check.py, line 17, in test_example() -> check.is_not_in(b, c, "make sure 2 isn't in list")
    ------------------------------------------------------------
    Failed Checks: 4
    =========================== 1 failed in 0.11 seconds ===========================


**Exist validations:**

- **check.equal** - *a == b*
- **check.not_equal** - *a != b*
- **check.is_true** - *bool(x) is True*
- **check.is_false** - *bool(x) is False*
- **check.is_none** - *x is None*
- **check.is_not_none** - *x is not None*
- **check.is_in** - *a in b*
- **check.not_in** - *a not in b*
- **check.is_instance** - *isinstance(a, b)*
- **check.not_is_instance** - *not isinstance(a, b)*
- **check.almost_equal** - *a == pytest.approx(b, rel, abs)* see at: `pytest.approx <https://docs.pytest.org/en/latest/reference.html#pytest-approx>`_
- **check.not_almost_equal** - *a != pytest.approx(b, rel, abs)* see at: `pytest.approx <https://docs.pytest.org/en/latest/reference.html#pytest-approx>`_
- **check.greater** - *a > b*
- **check.greater_equal** - *a >= b*
- **check.less** - *a < b*
- **check.less_equal** - *a <= b*


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-check" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/okken/pytest-check/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`pytest-expect`: https://github.com/okken/pytest-expect
