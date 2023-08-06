"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import pytest
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--cache-dir",
        action="store",
        help="Set fixed cache directory",
    )

    parser.addoption(
        "--skip-deploy-tests",
        default=False,
        action="store_true",
        dest="skip_deploy_tests",
        help="Deploy tests will be skipped from execution (for development purposes)",
    )


def pytest_runtest_setup(item: Item):
    if "deploy_test" in item.keywords and item.config.getoption("--skip-deploy-tests"):
        pytest.skip("Deploy tests has been skipped")
