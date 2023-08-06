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
import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Generator, Sequence

import pytest

from pytest_inmanta_yang.clab.config import HostConfig
from pytest_inmanta_yang.clab.host import ClabHost

if TYPE_CHECKING:
    # Local type stub for mypy that works with both pytest < 7 and pytest >=7
    # https://docs.pytest.org/en/7.1.x/_modules/_pytest/legacypath.html#TempdirFactory
    import py

    class TempdirFactory:
        def mktemp(self, path: str) -> py.path.local:
            ...


from inmanta.agent import config as inmanta_config
from paramiko import sftp_client
from pytest_inmanta.plugin import Project

from pytest_inmanta_yang.const import VENDOR_CISCO
from pytest_inmanta_yang.netconf_device_helper import (
    NetconfDeviceHelper,
    NetconfOperation,
)
from pytest_inmanta_yang.yang_test import YangTest

LOGGER = logging.getLogger(__name__)

logging.getLogger("ncclient").setLevel(logging.ERROR)
logging.getLogger("ncdiff.model").setLevel(logging.CRITICAL)
logging.getLogger("paramiko").setLevel(logging.INFO)


@pytest.fixture()
def clab_topology() -> str:
    """
    Overwrite this fixture to point to the topology file of your choice.

        .. code_block:: python

            import os
            import pytest
            import pytest_inmanta_yang

            @pytest.fixture()
            def clab_topology() -> str:
                return os.path.join(os.path.dirname(__file__), "clab/srlinux.topology.yml")

    """
    return os.path.join(os.path.dirname(__file__), "clab/srlinux.topology.yml")


@pytest.fixture()
def clab_workdir(clab_topology: str) -> Generator[str, None, None]:
    """
    Create a temporary directory in which we copy the topology file.

    Once the test is done, we take care to remove any root-owned file from the directory.
    The directory itself is then removed by exiting the TemporaryDirectory context.

    If you need to add additional files on the side of the topology file, you can
    overwrite this fixture (and call the original one).

        .. code_block:: python

            import os
            import pytest
            import pytest_inmanta_yang

            @pytest.fixture()
            def clab_workdir(clab_workdir: str) -> str:
                config = os.path.join(os.path.dirname(__file__), "srlinux/docs/config.json")
                shutil.copy(config, os.path.join(clab_workdir, "config.json"))

                return clab_workdir

    """
    cleanup_command = "sudo rm -r"

    with tempfile.TemporaryDirectory() as tmp:
        LOGGER.debug(f"Using folder {tmp} as clab working directory")
        shutil.copy(clab_topology, os.path.join(tmp, "topology.yml"))

        yield tmp

        LOGGER.info("Removing root owned files")
        for path in os.listdir(tmp):
            file = Path(tmp, path)
            if file.owner() != "root":
                continue

            cleanup_command = f"{cleanup_command} {file.name}"

        LOGGER.debug(cleanup_command)
        cleanup = subprocess.Popen(
            cleanup_command.split(),
            cwd=tmp,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = cleanup.communicate()
        assert cleanup.returncode == 0, stderr
        LOGGER.debug(stdout)


@pytest.fixture()
def clab_hosts(
    clab_workdir: str, use_session_temp_dir: str
) -> Generator[Sequence[HostConfig], None, None]:
    """
    Execute a few clab command in the clab working directory to start a lab, and once
    the tests are done, clean it up.
    """

    clab_deploy = "sudo clab deploy --topo topology.yml"
    clab_inspect = [
        "bash",
        "-c",
        "sudo clab inspect --format json --topo topology.yml | grep -vG time=.*level=.*msg=.*",
    ]
    clab_destroy = "sudo clab destroy --topo topology.yml"

    # Destroy the lab
    LOGGER.info("Ensuring the lab is not deployed")
    LOGGER.debug(clab_destroy)
    destroy = subprocess.Popen(
        clab_destroy.split(),
        cwd=clab_workdir,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = destroy.communicate()
    assert destroy.returncode == 0, stderr
    LOGGER.debug(stdout)

    # Deploy the lab
    LOGGER.info("Deploying the clab topology")
    LOGGER.debug(clab_deploy)
    deploy = subprocess.Popen(
        clab_deploy.split(),
        cwd=clab_workdir,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = deploy.communicate()
    assert deploy.returncode == 0, stderr
    LOGGER.debug(stdout)

    # Get the container ip
    LOGGER.info("Getting deployed host information")
    LOGGER.debug(clab_inspect)
    inspect = subprocess.Popen(
        clab_inspect,
        cwd=clab_workdir,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = inspect.communicate()
    assert inspect.returncode == 0, stderr
    LOGGER.debug(stdout)

    hosts = [ClabHost(**host) for host in json.loads(stdout)]
    yield [host.config(clab_workdir) for host in hosts]

    # Destroy the lab
    LOGGER.info("Destroying the clab topology")
    LOGGER.debug(clab_destroy)
    destroy = subprocess.Popen(
        clab_destroy.split(),
        cwd=clab_workdir,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = destroy.communicate()
    assert destroy.returncode == 0, stderr
    LOGGER.debug(stdout)


@pytest.fixture(scope="session")
def netconf_device_initial_config_path_file() -> str:
    """
    Empty fixture to be overridden.

    It should return the path to the file containing startup config for the device.

        .. code_block:: python

            import os
            import pytest
            from pytest_inmanta_yang import NetconfDeviceHelper

            @pytest.fixture(scope="session")
            def netconf_device_initial_config_path_file() -> str:
                hostname = os.getenv(NetconfDeviceHelper.ENV_VARIABLE_HOSTNAME)
                return os.path.join(os.path.dirname(__name__), f"resources/{hostname}.xml")

    """
    raise NotImplementedError("You should overwrite this fixture")


@pytest.fixture(scope="session")
def session_temp_dir(
    tmpdir_factory: "TempdirFactory", request: pytest.FixtureRequest
) -> Generator[str, None, None]:
    fixed_cache_dir = request.config.getoption("--cache-dir")
    if not fixed_cache_dir:
        LOGGER.info(
            "Using temporary cache folder, this will require reloading of all yang files. Use --cache-dir to prevent this"
        )
        session_temp_dir = tmpdir_factory.mktemp("session")
        yield str(session_temp_dir)
        session_temp_dir.remove(ignore_errors=True)
    else:
        # fixed cache
        LOGGER.info("Using fixed cache folder")
        abspath = os.path.abspath(fixed_cache_dir)
        os.makedirs(fixed_cache_dir, exist_ok=True)
        yield str(abspath)


@pytest.fixture
def use_session_temp_dir(session_temp_dir: str) -> Generator[str, None, None]:
    inmanta_config.state_dir.set(str(session_temp_dir))
    yield inmanta_config.state_dir.get()


def cisco_cleanup(netconf_device: NetconfDeviceHelper, initial_path: str) -> None:
    """
    Cleanup for Cisco IOS-XR device.
    It is done by uploading and overriding startup config file using SSH
    """
    LOGGER.info(
        f"Cleaning up Cisco device: `{netconf_device.hostname}` - startup config file will be uploaded using SSH"
    )
    LOGGER.debug(f"read config and upload to : `{netconf_device.hostname}`")
    with netconf_device.get_ssh_connect() as ssh:
        # copy the file first
        client = sftp_client.SFTPClient.from_transport(ssh.channel.transport.session)
        assert client is not None
        client.put(initial_path, "disk0:/baseconfig.cfg")
        ssh.send_command("copy disk0:/baseconfig.cfg running-config replace")

    LOGGER.info(f"Cleanup done for Cisco device: `{netconf_device.hostname}`")


def netconf_cleanup(netconf_device: NetconfDeviceHelper, initial_path: str) -> None:
    """
    Cleanup for device using netconf.
    It is done by editing the device config with the config located in initial_path.
    """
    LOGGER.info(
        f"Cleaning up {netconf_device.hostname} (vendor: {netconf_device.vendor})"
    )
    initial_config = Path(initial_path).read_text()

    LOGGER.debug(f"Deploying initial config on device: \n{initial_config}")
    netconf_device.edit_config(
        initial_config, default_operation=NetconfOperation.REPLACE
    )

    LOGGER.info("Cleanup done")


@pytest.fixture(scope="session")
def netconf_device_global(
    netconf_device_initial_config_path_file: str,
) -> Generator[NetconfDeviceHelper, None, None]:
    """
    Building the netconf device helper and cleaning up the router after the tests.
    """
    device = NetconfDeviceHelper.using_env_variables()
    yield device

    LOGGER.info("Running end of session cleanup")
    if device.vendor == VENDOR_CISCO:
        cisco_cleanup(device, netconf_device_initial_config_path_file)
    else:
        netconf_cleanup(device, netconf_device_initial_config_path_file)


@pytest.fixture(scope="function")
def netconf_device(
    netconf_device_global: NetconfDeviceHelper,
    netconf_device_initial_config_path_file: str,
) -> Generator[NetconfDeviceHelper, None, None]:
    """
    Cleanup the router before the test

    This fixture is picked up automatically when using the yang fixture from pytest_inmanta_yang.
    Other modules using pytest_inmanta_yang will have to overwrite it with their own cleanup.
    """
    LOGGER.info("Running pre-test cleanup")
    if netconf_device_global.vendor == VENDOR_CISCO:
        cisco_cleanup(netconf_device_global, netconf_device_initial_config_path_file)
    else:
        netconf_cleanup(netconf_device_global, netconf_device_initial_config_path_file)

    yield netconf_device_global


@pytest.fixture
def yang(
    request: pytest.FixtureRequest,
    project: Project,
    netconf_device: NetconfDeviceHelper,
    use_session_temp_dir: str,
) -> Generator[YangTest, None, None]:
    mgr = YangTest(project, netconf_device)
    yield mgr

    if not request.node.rep_call.passed:
        mgr.report_state()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> Generator[None, None, None]:
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()  # type: ignore

    # set a report attribute for each phase of a call, when can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
