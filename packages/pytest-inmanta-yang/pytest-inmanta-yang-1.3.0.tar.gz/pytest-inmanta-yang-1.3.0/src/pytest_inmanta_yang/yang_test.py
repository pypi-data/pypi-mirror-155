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
import logging
from typing import Dict, Optional

from inmanta.data.model import AttributeStateChange
from lxml import etree, objectify  # type: ignore
from pytest_inmanta.plugin import Project

from pytest_inmanta_yang.netconf_device_helper import NetconfDeviceHelper
from pytest_inmanta_yang.object_element import ObjectElement

LOGGER = logging.getLogger(__name__)


class YangTest:
    """Yang test fixture. This fixture currently assumes there is only one yang::Resource"""

    def __init__(self, project: Project, netconf_device: NetconfDeviceHelper) -> None:
        self._project = project
        self._device: NetconfDeviceHelper = netconf_device
        self._model: Optional[str] = None

        self._last_current_state: Optional[ObjectElement] = None
        self._last_desired_state: Optional[ObjectElement] = None

    def compile(self, model: str) -> None:
        """Run a project.compile before the compile the following variables will be replaced using a string
        formatter %(VAR)s

        HOSTNAME, MGMT_IP, PORT, USERNAME and PASSWORD
        """
        complete_model = model % {
            "HOSTNAME": self._device.hostname,
            "MGMT_IP": self._device.host,
            "PORT": self._device.port,
            "USERNAME": self._device.username,
            "PASSWORD": self._device.password,
        }

        LOGGER.info("Compiling model")
        try:
            self._project.compile(complete_model)
            LOGGER.debug("Used model:\n %s", complete_model)
        except Exception:
            LOGGER.error("Used following model that failed:\n %s", complete_model)
            raise

        self._model = complete_model

    def compile_purged(self) -> None:
        """Compile the previously compiled model with purged=true"""
        if self._model is None:
            raise Exception(
                "Can not find the original model, you need to first run compile"
            )

        new_model = self._model.replace("purged=false", "purged=true")
        LOGGER.info("Compiling purged model")
        LOGGER.debug("Using purged model:\n %s", new_model)

        if new_model == self._model:
            raise Exception(
                "For purged compile to work each entity that is purgeable requires 'purged=true,' "
                "to be present. Including the trailing comma."
            )

        self._project.compile(new_model)

    def get_desired_state(self, name: str = None) -> Optional[ObjectElement]:
        """
        Returns the desired state of the resource with the given name. If no name is provided
        it will return the resource if only one exists. If multiple yang resources exist the first
        matching one is returned.

        If no matching resource is found, None is returned.
        """
        if name is not None:
            LOGGER.info("Fetching desired state for yang::Resource with name %s", name)
            resource = self._project.get_resource("yang::Resource", name=name)  # type: ignore
        else:
            LOGGER.info("Fetching desired state for yang::Resource")
            resource = self._project.get_resource("yang::Resource")

        if resource is None:
            return None

        self._last_desired_state = ObjectElement(objectify.fromstring(resource.xml))  # type: ignore
        return self._last_desired_state

    def get_current_state(self, filter: str = None) -> ObjectElement:
        """
        Return the current (full) configuration of the device.

        :param filter: Provide an xml filter. This can be fetched from the resource you are testing.
        """
        LOGGER.info("Fetching current state from device.")
        if filter:
            LOGGER.info("Using filter %s", filter)

        tree = self._device.get_config()
        xml_data = etree.tostring(tree, pretty_print=True)
        object_tree = objectify.fromstring(xml_data)
        self._last_current_state = ObjectElement(object_tree)
        return self._last_current_state

    def dryrun(self) -> Dict[str, AttributeStateChange]:
        """Perform a dryrun and return the list of changes."""
        LOGGER.info("Running dryrun for yang::Resource")
        return self._project.dryrun_resource("yang::Resource")

    def deploy(self, pre_dryrun: bool = True, post_dryrun: bool = True) -> None:
        """Deploy the yang::Resource in the model. By default it asserts that before the deploy there are dryrun changes and
        after the deploy there are not dryrun changes.

        This can be disabled and dryruns can be run with self.dryrun.
        """
        if pre_dryrun:
            changes = self.dryrun()
            assert "xml" in changes

        LOGGER.info("Running deploy for yang::Resource")
        self._project.deploy_resource("yang::Resource")

        if post_dryrun:
            changes = self.dryrun()
            assert "xml" not in changes

    def report_state(self) -> None:
        """Report on the state collected during tests. This method should be called when a failure occurred."""
        print("\n")
        if self._model:
            print("=" * 80)
            print("Config model")
            print("=" * 80)
            print(self._model)
            print("\n")

        if self._last_desired_state:
            print("=" * 80)
            print("Desired state xml")
            print("=" * 80)
            print(self._last_desired_state.to_tree())
            print("\n")

        if self._last_current_state:
            print("=" * 80)
            print("Current state xml")
            print("=" * 80)
            print(self._last_current_state.to_tree())
            print("\n")

        print("=" * 80)
