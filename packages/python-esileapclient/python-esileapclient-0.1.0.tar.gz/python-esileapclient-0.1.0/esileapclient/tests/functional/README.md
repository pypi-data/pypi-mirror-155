# esi-leap Client Functional Tests

These tests are designed to ensure the esi-leap services and the esi-leap CLI client function as expected when interacting with each other.

### Prerequisites

These tests are intended to be ran against a functioning OpenStack cloud with esi-leap services enabled and running (https://github.com/CCI-MOC/esi-leap). It assumes that the esi-leap.conf file is located at `/etc/esi-leap/esi-leap.conf`; however if this is not the case, the location of the file can be specified by setting the environment variable `OS_ESI_CFG_PATH` equal to the file's location. This can also be used to provide a custom config file for use with these tests if desired. Additionally, since these tests make use of dummy nodes, the configuration file requires a value for the `dummy_node_dir` option in the `[dummy_node]` section of esi-leap.conf.

### Running the tests

By default, the functional tests will not run when invoking `tox` with no additional options. To run them, you must specify the 'functional' testenv like this:

```
$ tox -e functional
```

Some tests, such as the ones that check for a lease or offer to expire take a very long time to run (upwards of 90 seconds per test), and as such are skipped by default. To run these, pass the `--run-slow` flag to pytest (this project's test runner).

```
# via tox:
    $ tox -e functional -- --run-slow

# directly via pytest:
    $ py.test esileapclient/tests/functional --run-slow
```

Note that the policy tests included here may fail if your deployment makes use of a custom esi-leap policy file. See the section below for instructions on how to skip these tests if this is the case.

### Running specific tests

Since tests are run through pytest, any valid pytest flags can be set when running the tests. The `-k` flag can be used to specify a pattern each test to be run must match and can be used to include or exclude tests or classes of tests.

```
# run only the basic tests:
    $ tox -e functional -- -k "BasicTests"
# run everything except the time tests:
    $ tox -e functional -- -k "not TimeTests"
# run the test named test_offer_owner:
    $ tox -e functional -- -k "test_offer_create_basic"
# ...and so on
```

Additionally, the `-m` flag can be used to include or exclude tests that are marked with a certain attribute. For this project, this would be the slow tests and the negative tests (tests that ensure that invalid inputs are handled correctly), denoted by the "slow" and "negative" markers.

```
# only run the positive tests:
    $ tox -e functional -- -m "not negative"
# only run the negative tests:
    $ tox -e functional -- -m "negative"
# only run the slow tests:
    $ tox -e functional -- --run-slow -m "slow"
```
