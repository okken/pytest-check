# pytest-check

A pytest plugin that allows multiple failures per test.

----

This [pytest](https://github.com/pytest-dev/pytest) plugin was a rewrite and a
rename of [pytest-expect](https://github.com/okken/pytest-expect).



## Installation

From PPI:

```
$ pip install pytest-check
```

Or from github.

```
$ pip install git+https://github.com/okken/pytest-check
```


## Usage

Example using import:

```python
import pytest_check as check


def test_example():
    a = 1
    b = 2
    c = [2, 4, 6]
    check.greater(a, b)
    check.less_equal(b, a)
    check.is_in(a, c, "Is 1 in the list")
    check.is_not_in(b, c, "make sure 2 isn't in list")
```


Test results:

```
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
```


Example using fixture:

```python
def test_example(check):
    a = 1
    b = 2
    c = [2, 4, 6]
    check.greater(a, b)
    check.less_equal(b, a)
    check.is_in(a, c, "Is 1 in the list")
    check.is_not_in(b, c, "make sure 2 isn't in list")
```


## validation functions

- **check.equal** - *a == b*
- **check.not_equal** - *a != b*
- **check.is_true** - *bool(x) is True*
- **check.is_false** - *bool(x) is False*
- **check.is_none** - *x is None*
- **check.is_not_none** - *x is not None*
- **check.is_in** - *a in b*
- **check.is_not_in** - *a not in b*
- **check.is_instance** - *isinstance(a, b)*
- **check.not_is_instance** - *not isinstance(a, b)*
- **check.almost_equal** - *a == pytest.approx(b, rel, abs)* see at: [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)
- **check.not_almost_equal** - *a != pytest.approx(b, rel, abs)* see at: [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)
- **check.greater** - *a > b*
- **check.greater_equal** - *a >= b*
- **check.less** - *a < b*
- **check.less_equal** - *a <= b*

## Defining your own check functions

The `@check_func` decorator allows you to wrap any test helper that has an assert
statement in it to be a non-blocking assert function.


```python
from pytest_check import check_func

@check_func
def is_four(a):
    assert a == 4

def test_all_four():
    is_four(1)
    is_four(2)
    is_four(3)
    is_four(4)
```

The above will result in:

```
...
________________________________ test_all_four _________________________________
FAILURE: assert 1 == 4
  test_fail.py, line 8, in test_all_four() -> is_four(1)
FAILURE: assert 2 == 4
  test_fail.py, line 9, in test_all_four() -> is_four(2)
FAILURE: assert 3 == 4
  test_fail.py, line 10, in test_all_four() -> is_four(3)
------------------------------------------------------------
Failed Checks: 3
=========================== 1 failed in 0.12 seconds ===========================
```

## Using check as a context manager

You can use the `check()` context manager to wrap any assert that you want to continue after in a test.

```python
from pytest_check import check


def test_context_manager():
    with check:
        x = 3
        assert 1 < x < 4
```

Within any `with check:`, however, you still won't get past the assert statement,
so you will need to use multiple `with check:` blocks for multiple asserts:

```python
    def test_multiple_failures():
        with check: assert 1 == 0
        with check: assert 1 > 2
        with check: assert 1 < 5 < 4

```

## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/). 
Test coverage is now 100%. Please make sure to keep it at 100%.
If you have an awesome pull request and need help with getting coverage back up, let me know.


## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-check" is free and open source software


## Issues

If you encounter any problems, please [file an issue](https://github.com/okken/pytest-check/issues) along with a detailed description.

