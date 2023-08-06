# The code here has been borrowed from the examples given here:
# https://docs.pytest.org/en/latest/example/simple.html
import pytest


def pytest_addoption(parser):
    parser.addoption('--run-slow',
                     action='store_true',
                     default=False,
                     help='run tests marked as slow')


def pytest_configure(config):
    slow_info = 'slow: mark test as slow to run'
    neg_info = 'negative: marks tests that test invalid input'
    config.addinivalue_line('markers', slow_info)
    config.addinivalue_line('markers', neg_info)


def pytest_collection_modifyitems(config, items):
    if config.getoption('--run-slow'):
        return
    skipped = pytest.mark.skip(reason='slow tests are skipped by default; '
                                      'to run, call pytest with --run-slow.')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skipped)
