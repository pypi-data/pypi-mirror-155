""" Conftest for Fixtures """
# Copyright 2021 MosaicML. All Rights Reserved.

import os
import pathlib
from typing import List

import pytest

from mcli import config

# Add the path of any pytest fixture files you want to make global
pytest_plugins = ['tests.fixtures', 'tests.cli.fixtures', 'tests.api.fixtures']


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    for env_var in (config.MCLI_MODE_ENV,):
        os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('--include-api',
                     action='store_true',
                     help="""\
        Use this flag to include tests that will call the MosaicML API. Make
        sure that you have a valid API key either in the mcli_config or
        set as an environment variable before running these tests.""")
    parser.addoption('--integration',
                     action='store_true',
                     help="""\
        Use this flag to run integration tests. These tests take longer to run
        than unit tests, but can use microk8s to submit actual manifests to a real
        Kubernetes cluster. You will need to install microk8s.""")


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]) -> None:
    deselected = set()

    # Deselect api tests
    include_api = config.getoption('include_api')
    if not include_api:
        for item in items:
            if item.get_closest_marker('apitest') is not None:
                # ignore tests that involve querying the graphql api
                deselected.add(item)

    # We only run integration tests exclusively, and only if pytest is invoked accordingly
    integration = bool(config.getoption('integration'))
    integration_dir = config.rootpath / 'tests/integration'
    for item in items:
        if integration ^ (integration_dir in pathlib.Path(item.fspath).parents):
            deselected.add(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = [i for i in items if i not in deselected]
