def pytest_runtest_makereport(item, call):
    """Hook to detect test failures"""
    if call.excinfo is not None:
        item.module.pytest_failed = True
