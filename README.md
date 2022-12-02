# pytest-check

A pytest plugin that allows multiple failures per test.

----

Normally, a test function will fail and stop running with the first failed `assert`.
That's totally fine for tons of kinds of software tests.
However, there are times where you'd like to check more than one thing, and you'd really like to know the results of each check, even if one of them fails.

`pytest-check` allows multiple failed "checks" per test function, so you can see the whole picture of what's going wrong.

## Installation

From PyPI:

```
$ pip install pytest-check
```


## Example

Quick example of where you might want multiple checks:

```python
import httpx
from pytest_check import check

def test_httpx_get():
    r = httpx.get('https://www.example.org/')
    # bail if bad status code
    assert r.status_code == 200
    # but if we get to here
    # then check everything else without stopping
    with check:
        assert r.is_redirect is False
    with check:
        assert r.encoding == 'utf-8'
    with check:
        assert 'Example Domain' in r.text
```

## Import vs fixture

The example above used import: `from pytest_check import check`.

You can also grab `check` as a fixture with no import:

```python
def test_httpx_get(check):
    r = httpx.get('https://www.example.org/')
    ...
    with check:
        assert r.is_redirect == False
    ...
```

## Validation functions

`check` also helper functions for common checks. 
These methods do NOT need to be inside of a `with check:` block.

- **check.equal** - *a == b*
- **check.not_equal** - *a != b*
- **check.is_** - *a is b*
- **check.is_not** - *a is not b*
- **check.is_true** - *bool(x) is True*
- **check.is_false** - *bool(x) is False*
- **check.is_none** - *x is None*
- **check.is_not_none** - *x is not None*
- **check.is_in** - *a in b*
- **check.is_not_in** - *a not in b*
- **check.is_instance** - *isinstance(a, b)*
- **check.is_not_instance** - *not isinstance(a, b)*
- **check.almost_equal** - *a == pytest.approx(b, rel, abs)* see at: [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)
- **check.not_almost_equal** - *a != pytest.approx(b, rel, abs)* see at: [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)
- **check.greater** - *a > b*
- **check.greater_equal** - *a >= b*
- **check.less** - *a < b*
- **check.less_equal** - *a <= b*
- **check.between** - *a < b < c*
- **check.raises** - *func raises given exception* similar to [pytest.raises](https://docs.pytest.org/en/latest/reference/reference.html#pytest-raises)

The httpx example can be rewritten with helper functions:

```python
def test_httpx_get_with_helpers():
    r = httpx.get('https://www.example.org/')
    assert r.status_code == 200
    check.is_false(r.is_redirect)
    check.equal(r.encoding, 'utf-8')
    check.is_in('Example Domain', r.text)
```

Which you use is personal preference.

## Defining your own check functions

The `@check.check_func` decorator allows you to wrap any test helper that has an assert
statement in it to be a non-blocking assert function.


```python
from pytest_check import check

@check.check_func
def is_four(a):
    assert a == 4

def test_all_four():
    is_four(1)
    is_four(2)
    is_four(3)
    is_four(4)
```

## Using raises as a context manager

`raises` is used as context manager, much like `pytest.raises`. The main difference being that a failure to raise the right exception won't stop the execution of the test method.


```python
from pytest_check import check

def test_raises():
    with check.raises(AssertionError):
        x = 3
        assert 1 < x < 4
```

## Pseudo-tracebacks

With `check`, tests can have multiple failures per test.
This would possibly make for extensive output if we include the full traceback for
every failure.
To make the output a little more concise, `pytest-check` implements a shorter version, which we call pseudo-tracebacks.

For example, take this test:

```python
def test_example():
    a = 1
    b = 2
    c = [2, 4, 6]
    check.greater(a, b)
    check.less_equal(b, a)
    check.is_in(a, c, "Is 1 in the list")
    check.is_not_in(b, c, "make sure 2 isn't in list")
```

This will result in:

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

## Red output

The failures will also be red, unless you turn that off with pytests `--color=no`.

## No output

You can turn off the failure reports with pytests `--tb=no`.

## Stop on Fail (maxfail behavior)

Setting `-x` or `--maxfail=1` will cause this plugin to abort testing after the first failed check.

Setting `-maxfail=2` or greater will turn off any handling of maxfail within this plugin and the behavior is controlled by pytest.

In other words, the `maxfail` count is counting tests, not checks.
The exception is the case of `1`, where we want to stop on the very first failed check.

## any_failures()

Use `any_failures()` to see if there are any failures.  
One use case is to make a block of checks conditional on not failing in a previous set of checks:

```python
from pytest_check import check

def test_with_groups_of_checks():
    # always check these
    check.equal(1, 1)
    check.equal(2, 3)
    if not check.any_failures():
        # only check these if the above passed
        check.equal(1, 2)
        check.equal(2, 2)
```

## Speedups

If you have lots of check failures, your tests may not run as fast as you want.  
There are a few ways to speed things up.

* `--check-no-tb` - report reason for failure, but not pseudo-traceback.
    * pytest-check uses custom traceback code I'm calling a pseudo-traceback. 
    * This is visually shorter than normal assert tracebacks.
    * Internally, it uses introspection, which can be slow.
    * Turning off pseudo-tracebacks speeds things up quite a bit.

* `--check-max-report=10` - limit reported failures per test.
    * The example shows `10` but any number can be used.
    * The test will still have the total nuber of failures reported.

* `--check-max-fail=20` - Stop the test after this many check failures.
    * This is useful if your code under test is slow-ish and you want to bail early.

* Any of these can be used on their own, or combined.

* Recommendation:
    * Don't worry about this unless you need to.
    * If you are using check a lot in tight loops with tons of data points, then speed it up significantly with all of these flags:
        * `--check-no-tb --check-max-report=10 --check-max-fail=20`.

## Local speedups

The flags above are global settings, and apply to every test in the test run.  

Locally, you can set these values per test.

From `examples/test_example_speedup_funcs.py`:

```python
def test_no_tb():
    check.set_no_tb()
    for i in range(1, 11):
        check.equal(i, 100)

def test_max_report():
    check.set_max_report(5)
    for i in range(1, 11):
        check.equal(i, 100)

def test_max_fail():
    check.set_max_fail(5)
    for i in range(1, 11):
        check.equal(i, 100)
```

## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/).
Test coverage is now 100%. Please make sure to keep it at 100%.
If you have an awesome pull request and need help with getting coverage back up, let me know.


## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-check" is free and open source software

## Issues

If you encounter any problems, please [file an issue](https://github.com/okken/pytest-check/issues) along with a detailed description.

## Changelog

See [changelog.md](https://github.com/okken/pytest-check/blob/main/changelog.md)
