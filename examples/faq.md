# pytest-check FAQ

## How can I determine immediately after a check if it passed or failed?

All of the check methods, like `check.equal()`, return `True` or `False`. 

So, you can just do something like:

```python
from pytest_check import check

def test_something()
    ...
    if check.equal(a, b):
        # they are equal
        ...
    else
        # they are not equal
        # and a failure was registered by the check method
        ...
```