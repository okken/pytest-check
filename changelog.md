# Changelog

All notable changes to this project  be documented in this file.

<!--

## [Unreleased] - yyyy-month-dd

### Added

- nothing so far

### Fixed

- nothing so far

### Changed

- nothing so far

-->

## [2.2.2] - 2023-Sept-22

### fixed

- Issue #7

## [2.2.1] - 2023-Aug-11

### Changed

- Increase Python range to include 3.7.0. Thanks [EliahKagan](https://github.com/EliahKagan)

## [2.2.0] - 2023-July-14

### Added
- 
- pseudo traceback additions
- `-l` or `--showlocals` shows locals
- `__tracebackhide__ = True` is honored.
- if `assert` or other exception is involved,
  - the exception is included as part of the traceback.

### Changed

- pseudo traceback changes
- The red color is used more selectively.
  - this is intended to help readability
- Other minor formatting changes.
  - Please let me know if you have any issues with the changes

## [2.1.5] - 2023-June-6

### Fixed

- Fix [127](https://github.com/okken/pytest-check/issues/127) IndexError when running a check in a thread -  Thanks [fperrin](https://github.com/fperrin)

## [2.1.4] - 2023-Feb-13

### Added

- include tests an examples in sdist -  [pr 121](https://github.com/okken/pytest-check/pull/121)

## [2.1.3] - 2023-Feb-9

### Added

- publish-to-pypi.yml workflow

## [2.1.2] - 2023-Jan-13

### Changed

- README.md - clean up documentation for `--check-max-tb`. Thanks alblasco.
- Minor internal cleanup - removed some debug code.


## [2.1.1] - 2023-Jan-12

### Modified

- `check.call_on_fail(func)` - ***Experimental***
  - *Experimental feature - may change with any release, even a minor release*
  - Name changed from `check.set_failure_callback(func)`.
  - Also, I warned you I could change that at any time. 
    - No tomatoes thrown, please.
    - It's better, right? Thanks to Hynek for the suggestion.

## [2.1.0] - 2023-Jan-10

### Added

- `check.set_failure_callback(func)` - ***Experimental***
  - *Experimental feature - may change with any release, even a minor release*
  - Function to allow a callback function to be registered. 
  - This "func" function will be called for each failed check, and needs to accept a string parameter.
  - Examples:
    - `print` : `check.set_failure_callback(print)` 
      - allows stdout printing while test is running (provided `-s` is used).
    - `logging.error` : `check.set_failure_callback(logging.error)` 
      - failure reports to logging 
  - See `examples/test_example_logging.py` for runnable examples

## [2.0.0] - 2023-Jan-8

### Added

- With the following change, the default is now pretty darn fast, and most people will not need to modify any settings to get most of the speed improvements.
- `--check-max-tb=<int>` - sets the max number of pseudo-traceback reports per test function.
  - Default is 1.
  - After this, error is still reported 
    - The error reports continue, they just won't have a traceback.
    - If you set `--check-max-report`, then the reports stop at that number, with or without tracebacks.a
- `check.set_max_tb(int)` - overrides `--check-max-tb` for the test function it's called from. Value is reset after one test function.

### Deprecated

- `check.set_no_tb` and `--set-no-tb` will be removed in a future release. (probably soon)
- `check.set_no_tb` is deprecated.
  - For now, it internally calls `set_max_tb(0)`. See discussion below.
- `--check-no-tb` is deprecated.
  - It's also short lived. 
  - Since `--check-max-tb` is more useful, the default for `--check-max-tb` is 1, which is already pretty fast.
    And `--check-max-tb=0` has the same effect as `--check-no-tb`.

### Changed

- [PR 109](https://github.com/okken/pytest-check/pull/109). Update README.md with conda install instructions. Thanks Abel Aoun.

### Reason for major version bump

The default behavior has changed. Since `--check-max-tb=1` is the default, the default behavior is now:

- Show traceback for the first failure per test. (controlled by `--check-max-tb`, default is 1)
- Show error report for the remaining failures in a test. (controlled by `--check-max-report`, default is None)

Old default behavior was the same except all tracebacks would be reported.

My logic here:

- The actual error message, like `check 1 == 3`, is more useful than the traceback.
- The first traceback is still useful to point you to the test file, line number, of first failure.
- Other failures are probably close by. 

If this logic doesn't hold for you, you can always set `--check-max-tb=1000` or some other large number.


## [1.3.0] - 2022-Dec-2

- Most changes are related to speedup improvements.
  - use `--check-no-tb --check-max-report=10` to get super zippy.
- `check.between()` added just for fun

### Changed

- Rewrote `check.equal()` and other helper functions to not use assert.  
- Check functions report things like `FAILURE: check 1 < 2` now.
  - It used to say `FAILURE: assert 1 < 2`, but that's not really true anymore.

### Added

- `--check-no-tb` - turn off tracebacks
- `--check-max-report` - limit reported failures per test function
- `--check-max-fail` - limit failures per test function
- `check.set_no_tb()` - turn off tracebacks for one test function
- `check.set_max_report()` - limit reports for one test function
- `check.set_max_fail()` - limit failures for one test function
- `check.between(b, a, c)` - check that a < b < c

## [1.2.1] - 2022-Nov-30

### Changed

- Remove colorama as a dependency, and simplify how we do "red".

- Change the formatting of context manager checks such that if a msg is included, we see both the message and the assert failure. Previoulsy, the message would replace the assert failure.

## [1.2.0] - 2022-Nov-25

### Added

- Add `any_failures()`. Thank you [@alblasco](https://github.com/alblasco)

## [1.1.3] - 2022-Nov-22

### Fixed

- While using the `check` fixture, allow `check.check` as a context manager.
  - this is unnecessary, the `check` fixture now works as a context manager.
  - but apparently some people have been using `with check.check:`
  - so this fix makes that work.

## [1.1.2] - 2022-Nov-21

### Added

- Allow `raises` from `check` object. 
  - Now `with check.raises(Exception):` works.

## [1.1.1] - 2022-Nov-21

### Changed 

- README update

## [1.1.0] - 2022-Nov-21

### Added

- Red output in pseudo-traceback

### Changed 

- Refactored code into more modules
- All functionality now possible through `check` fixture or `from pytest_check import check`.
  - The `check` object from either of these methods can be used as either a context manager or to access the check helper functions.
- Lots of rewrite in README

### Deprecated
- API change.
  - Access to check helper functions via `import pytest_check as check` is deprecated.
  - It still works, but will be removed in a future version.
  - However, there is no deprecation warning for this.

## [1.0.10] - 2022-09-29

### Fixed

- [issue 80](https://github.com/okken/pytest-check/issues/80) --tb=no should remove tracebacks from xml output

## [1.0.9] - 2022-08-24

### Fixed 

- [issue 55](https://github.com/okken/pytest-check/issues/55) a problem with multiple drive letters.
  - code is using `os.path.relpath()`, but sometimes it can fail.
  - when it does fail, fall back to `os.path.abspath()`.
  - thanks [rloutrel](https://github.com/rloutrel) and [kr1zo](https://github.com/kr1zo) for your patience and persistence, and for the solution. 

## [1.0.8] - 2022-08-24

### Fixed

- Support check failures not blowing up if called outside of a test.
  - should also fix [85](https://github.com/okken/pytest-check/issues/85)
  - thanks [zerocen](https://github.com/zerocen) for the excellent toy example that helped me to get this fixed quickly.

### Changed

- changelog.md format. :)
- tox.ini cleanup
- refactoring tests to use examples directory instead of embedding example tests in test code.
  - this is easier to understand and debug issues.
  - also provides extra documentation through examples directory

## [1.0.7] - 2022-08-21

### Fixed

- Handle cases when context is None

## [1.0.6] - 2022-08-19

### Changed

- Update pyproject.toml to use newer flit
- Changed plugin name from pytest_check to pytest-check.


## [1.0.5] - 2022-03-29

### Added

- Add `raises`

## [1.0.4] - 2021-09-12

### Changed

- Require Python >= 3.6
- Remove old Manifest.in file.

## [1.0.3] - 2021-09-12

### Fixed

- Fix #64, modifications to maxfail behavior.

## [1.0.2] - 2021-08-12

### Added

- Add `excinfo` to call object in `pytest_runtest_makereport()`.
  - Intended to help with some report systems.

## [1.0.1] - 2020-12-27

### Changed

- Remove Beta Classifier
- Status is now "Development Status :: 5 - Production/Stable"

## [1.0.0] - 2020-12-27

### Changed

- Jump to 1.0 version, API is fairly stable.

## [0.4.1] - 2020-12-27

### Fixed

- Fix #43/#44 tests with failing checks and failing asserts now report all issues.

## [0.4.0] - 2020-12-14

### Added

- added `is_()` and `is_not()`

### Changed

- Requires pytest 6.0 or above. (Removed some cruft to support pytest 5.x)
