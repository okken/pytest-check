import pytest

@pytest.mark.parametrize('x', range(100))
def test_loop(check, x):
  check.less(x, 1000)
  for y in range(10):
     check.less(y, 1000)
    
  
