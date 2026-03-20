"""
Non-assert exceptions should also be caught by check.
All of these should report "Failed Checks: 1"
"""

def test_index_error(check):
    a_list = []
    with check:
        assert a_list[-1] == "Expected Value"  


def test_key_error(check):
    a_dict = {}
    with check:
        assert a_dict["k"] == "v"  

def test_attribute_error(check):
    an_object = object
    with check:
        assert an_object.v == "obj"  

