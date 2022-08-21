# Changelog

* 1.0.7
  * Handle cases when context is None
* 1.0.6
  * Update pyproject.toml to use newer flit
  * Attempt to fix plugin name from pytest_check to pytest-check.
* 1.0.5
  * Add `raises`
* 1.0.4
  * Require Python >= 3.6
  * Remove old Manifest.in file.
* 1.0.3
    * Fix #64, modifications to maxfail behavior.
* 1.0.2
    * Add `excinfo` to call object in `pytest_runtest_makereport()`.
    * Intended to help with some report systems.
* 1.0.1
    * Remove Beta Classifier
    * Status is now "Development Status :: 5 - Production/Stable"
* 1.0.0
    * Jump to 1.0 version, API is fairly stable.
* 0.4.1
    * Fix #43/#44 tests with failing checks and failing asserts now report all issues.
* 0.4.0
    * added `is_()` and `is_not()`
    * Requires pytest 6.0 or above. (Removed some cruft to support pytest 5.x)
