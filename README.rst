============
pytest-check
============

A pytest plugin that allows multiple failures per test.

----

This `Pytest`_ plugin was a rewrite and a rename of `pytest-expect`_.


Features
--------

* TODO


Requirements
------------

- pytest>=3.1.1


Installation
------------

Eventually, you'll be able to install "pytest-check" via `pip`_ from `PyPI`_:

.. code-block:: bash
    $ pip install pytest-check

But for now, you'll have to install it from github.

.. code-block:: bash
    $ pip install git+https://github.com/okken/pytest-check


Usage
-----

**Use as pytest fixture**

.. code-block:: python

    def test_one(check):
        check.equal(1, 2, msg='Must be equal part one')
        check.equal(1, 3)  # msg None by default


Test results:

.. code-block:: bash
    FAILURE: Must be equal part one
      test_one.py, line 6, in test_one() -> check.equal(1, 2, 'Must be equal part one')
    AssertionError

    FAILURE:
      test_one.py, line 7, in test_one() -> check.equal(1, 3, 'Must be equal part two')
    AssertionError

    ------------------------------------------------------------
    Failed Checks: 2

**Or use some test case class**

For example test case code:

.. code-block:: python

    import pytest


    class TestCase:

        check = None

        @pytest.yield_fixture(scope='function', autouse=True)
        def setup(self, check):
            self.check = check
            yield self.check
            self.check = None


For example test code:

.. code-block:: python

    from base import TestCase


    class TestTwo(TestCase):

        def test_two(self):
            self.check.equal(1, 2, 'two test')


Test results:

.. code-block:: bash
    FAILURE: Must be equal, functional is bad
      test_one.py, line 13, in test_two() -> self.check.equal(1, 2, 'Must be equal, functional is bad')
    AssertionError

    ------------------------------------------------------------
    Failed Checks: 1


**Exist validations:**

- **check.equal** - *a == b*
- **check.not_equal** - *a != b*
- **check.is_true** - *bool(x) is True*
- **check.is_false** - *bool(x) is False*
- **check.is_not** - *a is not b*
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
