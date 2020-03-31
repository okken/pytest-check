pytest_plugins = "pytester"


def pytest_check_onfailure(e):
    print(e)
