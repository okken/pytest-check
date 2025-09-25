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

From conda (conda-forge):
```
$ conda install -c conda-forge pytest-check
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

| Function    | Meaning    | Notes    |
|------------------------------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------|
| `equal(a, b, msg="")`    | `a == b`    |    |
| `not_equal(a, b, msg="")`    | `a != b`    |    |
| `is_(a, b, msg="")`    | `a is b`    |    |
| `is_not(a, b, msg="")`    | `a is not b`    |    |
| `is_true(x, msg="")`    | `bool(x) is True`    |    |
| `is_false(x, msg="")`    | `bool(x) is False`    |    |
| `is_none(x, msg="")`    | `x is None`    |    |
| `is_not_none(x, msg="")`    | `x is not None`    |    |
| `is_in(a, b, msg="")`    | `a in b`    |    |
| `is_not_in(a, b, msg="")`    | `a not in b`    |    |
| `is_instance(a, b, msg="")`    | `isinstance(a, b)`    |    |
| `is_not_instance(a, b, msg="")`    | `not isinstance(a, b)`    |    |
| `is_nan(x, msg="")`    | `math.isnan(x)`    | [math.isnan](https://docs.python.org/3/library/math.html#math.isnan)   |
| `is_not_nan(x, msg="")`    | `not math.isnan(x) `    | [math.isnan](https://docs.python.org/3/library/math.html#math.isnan)   | 
| `almost_equal(a, b, rel=None, abs=None, msg="")`    | `a == pytest.approx(b, rel, abs)` | [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)    |
| `not_almost_equal(a, b, rel=None, abs=None, msg="")` | `a != pytest.approx(b, rel, abs)` | [pytest.approx](https://docs.pytest.org/en/latest/reference.html#pytest-approx)    | 
| `greater(a, b, msg="")`    | `a > b`    |    |
| `greater_equal(a, b, msg="")`    | `a >= b`    |    |
| `less(a, b, msg="")`    | `a < b`    |    |
| `less_equal(a, b, msg="")`    | `a <= b`    |    |
| `between(b, a, c, msg="", ge=False, le=False)`    | `a < b < c`    |    |
| `between_equal(b, a, c, msg="")`    | `a <= b <= c`    | same as `between(b, a, c, msg, ge=True, le=True)`    |
| `raises(expected_exception, *args, **kwargs)`    | *Raises given exception*    | similar to [pytest.raises](https://docs.pytest.org/en/latest/reference/reference.html#pytest-raises) | 
| `fail(msg)`    | *Log a failure*    |    |

**Note: This is a list of relatively common logic operators. I'm reluctant to add to the list too much, as it's easy to add your own.**


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

### Using `@check.check_func`

The `@check.check_func` decorator allows you to wrap any test helper that has an assert statement in it to be a non-blocking assert function.


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


### Using `check.fail()`

Using `@check.check_func` is probably the easiest. 
However, it does have a bit of overhead in the passing cases 
that can affect large loops of checks.

If you need a bit of a speedup, use the following style with the help of `check.fail()`.

```python
from pytest_check import check

def is_four(a):
    __tracebackhide__ = True
    if a == 4:
        return True
    else: 
        check.fail(f"check {a} == 4")
        return False

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

def test_raises_exception_value():
    with check.raises(ValueError) as e:
        raise ValueError("This is a ValueError")
    check.equal(str(e.value) == "This is a ValueError")
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

* `--check-max-tb=5` - Only first 5 failures per test will include pseudo-tracebacks (rest without them).
    * The example shows `5` but any number can be used.
    * pytest-check uses custom traceback code I'm calling a pseudo-traceback.
    * This is visually shorter than normal assert tracebacks.
    * Internally, it uses introspection, which can be slow.
    * Allowing a limited number of pseudo-tracebacks speeds things up quite a bit.
    * Default is 1. 
        * Set a large number, e.g: 1000, if you want pseudo-tracebacks for all failures

* `--check-max-report=10` - limit reported failures per test.
    * The example shows `10` but any number can be used.
    * The test will still have the total nuber of failures reported.
    * Default is no maximum.

* `--check-max-fail=20` - Stop the test after this many check failures.
    * This is useful if your code under test is slow-ish and you want to bail early.
    * Default is no maximum.

* Any of these can be used on their own, or combined.

* Recommendation:
    * Leave the default, equivelant to `--check-max-tb=1`.
    * If excessive output is annoying, set `--check-max-report=10` or some tolerable number.

## Local speedups

The flags above are global settings, and apply to every test in the test run.  

Locally, you can set these values per test.

From `examples/test_example_speedup_funcs.py`:

```python
def test_max_tb():
    check.set_max_tb(2)
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
