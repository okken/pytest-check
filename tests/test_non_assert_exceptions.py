
def test_index_error(pytester):
    pytester.copy_example("examples/test_example_non_assert_exceptions.py")
    result = pytester.runpytest("-k", "test_index_error")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["IndexError:*", "Failed Checks: 1"])



def test_key_error(pytester):
    pytester.copy_example("examples/test_example_non_assert_exceptions.py")
    result = pytester.runpytest("-k", "test_key_error")
    result.assert_outcomes(failed=1, passed=0)
    print('stdout:', result.stdout.str(), '---')
    print('stderr:', result.stderr.str(), '---')
    result.stdout.fnmatch_lines([ "KeyError:*", "Failed Checks: 1"])


def test_attribute_error(pytester):
    pytester.copy_example("examples/test_example_non_assert_exceptions.py")
    result = pytester.runpytest("-k", "test_attribute_error")
    result.assert_outcomes(failed=1, passed=0)
    result.stdout.fnmatch_lines(["AttributeError:*", "Failed Checks: 1"])