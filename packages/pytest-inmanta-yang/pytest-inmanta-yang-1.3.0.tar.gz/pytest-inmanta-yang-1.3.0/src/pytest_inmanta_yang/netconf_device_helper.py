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
import os
from enum import Enum
from typing import Dict, Optional, Union

from lxml import etree  # type: ignore
from ncclient import manager as ncclient_manager  # type: ignore
from ncclient.operations.lock import LockContext  # type: ignore
from scrapli import Scrapli

from pytest_inmanta_yang.const import (
    VENDOR_CISCO,
    VENDOR_JUNIPER,
    VENDOR_NOKIA,
    VENDORS,
)

NETCONF_TIMEOUT = 30

LOGGER = logging.getLogger(__name__)


class NetconfOperation(str, Enum):
    """
    A netconf operation as can be passed to edit_config
    """

    MERGE = "merge"
    REPLACE = "replace"
    NONE = "none"


class MissingEnvVariableError(Exception):
    """
    Raised when the environment variable is missing
    """


class NetconfDeviceHelper(object):
    """
    Helper class containing NETCONF-enabled device credentials, other parameters and all the utilities methods.
    It has been designed to be used in one of two ways:
    1) Instantiation using environmental variables - a way dedicated for pytest fixture.
    There is class method `using_env_variables which returns an instance of NetconfDeviceHelper
    adjusted for given device described by environmental variables:
    YANG_DEVICE_HOST - hostname or IP address of device
    YANG_DEVICE_PORT - NETCONF port used by device
    YANG_DEVICE_USERNAME - NETCONF username
    YANG_DEVICE_PASSWORD - NETCONF password
    YANG_DEVICE_HOSTNAME - hostname of device - used to find proper initial config
    (currently supported are:
    sros-1`, `sros-2`, `bru-23-r301`, `bru-23-r302`, `bru-23-r309`, `yang-1-227`, `yang-1-228`, `yang-1-229`)
    YANG_DEVICE_VENDOR - vendor of device (one of `Nokia`, `Cisco`, `Juniper`)
    YANG_DEVICE_HUGE_TREE - set to `true` to enable huge tree XML support for device
    """

    ENV_VARIABLE_HOST = "YANG_DEVICE_HOST"
    ENV_VARIABLE_PORT = "YANG_DEVICE_PORT"
    ENV_VARIABLE_USERNAME = "YANG_DEVICE_USERNAME"
    ENV_VARIABLE_PASSWORD = "YANG_DEVICE_PASSWORD"
    ENV_VARIABLE_HOSTNAME = "YANG_DEVICE_HOSTNAME"
    ENV_VARIABLE_HUGE_TREE = "YANG_DEVICE_HUGE_TREE"
    ENV_VARIABLE_VENDOR = "YANG_DEVICE_VENDOR"

    @classmethod
    def using_env_variables(
        cls,
        password_env_var: str = None,
        username_env_var: str = None,
    ) -> "NetconfDeviceHelper":
        """
        Methods returns an instance of NetconfDeviceHelper
        adjusted to given device using environmental variables

        :param password_env_var: string to override the password environmental variable (suffix will be ignored)
        :param username_env_var: string to override the username environmental variable (suffix will be ignored)
        :return: instance of NetconfDeviceHelper
        """
        if password_env_var is None:
            password = cls._get_env_or_fail(cls.ENV_VARIABLE_PASSWORD)
        else:
            password = cls._get_env_or_fail(password_env_var)

        if username_env_var is None:
            username = cls._get_env_or_fail(cls.ENV_VARIABLE_USERNAME)
        else:
            username = cls._get_env_or_fail(username_env_var)

        huge_tree_raw = os.getenv(cls.ENV_VARIABLE_HUGE_TREE, "").strip()
        huge_tree = huge_tree_raw.lower() == "true" if huge_tree_raw else False

        return cls(
            host=cls._get_env_or_fail(cls.ENV_VARIABLE_HOST),
            port=int(cls._get_env_or_fail(cls.ENV_VARIABLE_PORT)),
            username=username,
            password=password,
            hostname=cls._get_env_or_fail(cls.ENV_VARIABLE_HOSTNAME),
            vendor=cls._get_env_or_fail(cls.ENV_VARIABLE_VENDOR).lower(),
            huge_tree=huge_tree,
        )

    @classmethod
    def _get_env_or_fail(cls, name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise MissingEnvVariableError(name)

        return value.strip()

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        hostname: str,
        vendor: str,
        huge_tree: bool = False,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.hostname = hostname
        self.vendor = vendor
        self.huge_tree = huge_tree

        if self.vendor not in VENDORS:
            raise ValueError(f"Provided vendor `{vendor}` is not one of {VENDORS}")

    @property
    def credentials(self) -> Dict[str, Union[int, str]]:
        """
        :return: device credentials as dictionary
        """
        return {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "hostname": self.hostname,
        }

    def _connect(self) -> ncclient_manager.Manager:
        netconf_client = ncclient_manager.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            hostkey_verify=False,
            look_for_keys=False,
            allow_agent=False,
        )
        # work around for https://github.com/CiscoTestAutomation/ncdiff/issues/11
        netconf_client._timeout = NETCONF_TIMEOUT
        netconf_client._huge_tree = self.huge_tree
        return netconf_client

    def get_config(
        self, datastore: str = "running", filter: Union[etree.Element, str, None] = None
    ) -> etree.Element:
        """
        Gets device configuration from given NETCONF datastore

        :param datastore: name of NETCONF datastore - possible values: 'running', 'candidate', 'startup'
        :param filter: Either XML tree or XML string representing filter.
        :return: XML tree containing configuration stored in given NETCONF datastore
        """
        if filter is not None and isinstance(filter, str):
            filter = etree.fromstring(filter)

        if filter is not None and not filter.tag == "filter":
            root = etree.Element("filter")
            root.append(filter)
            filter = root

        with self._connect() as connection:
            return connection.get_config(source=datastore, filter=filter).data

    def edit_config(
        self,
        config: Union[etree.Element, str],
        datastore: str = "candidate",
        default_operation: Optional[NetconfOperation] = None,
    ) -> None:
        """
        Edits config represented by XML tree in given NETCONF datastore.

        :param config: Element being root of XML tree representing config part which should be edited
        :param datastore: name of NETCONF datastore - possible values: 'running', 'candidate', 'startup'
        :param default_operation: can be either of "merge", "replace", "none", or None
        """
        parsed_default_operation: Optional[str] = None
        if default_operation is not None:
            # We ensure that the netconf operation we received is valid
            # A string with the correct value would be accepted as well
            # >>> replace = NetconfOperation("replace")
            # >>> replace
            # <NetconfOperation.REPLACE: 'replace'>
            # >>> NetconfOperation(replace)
            # <NetconfOperation.REPLACE: 'replace'>
            default_operation = NetconfOperation(default_operation)
            parsed_default_operation = str(default_operation.value)

        with self._connect() as connection:
            with self._lock(connection, datastore):
                connection.discard_changes()
                connection.edit_config(
                    target=datastore,
                    config=config,
                    default_operation=parsed_default_operation,
                )
                connection.commit()

    def get_ssh_connect(self, platform: Optional[str] = None):
        """Get a scrapli ssh connection"""
        platform_by_vendor = {
            VENDOR_CISCO: "cisco_iosxr",
            VENDOR_NOKIA: "nokia_sros",
            VENDOR_JUNIPER: "juniper_junos",
        }

        return Scrapli(
            host=self.host,
            port=self.port,
            auth_username=self.username,
            auth_password=self.password,
            auth_strict_key=False,
            platform=platform or platform_by_vendor[self.vendor],
            transport="paramiko",
        )

    def _lock(
        self, connection: ncclient_manager.Manager, datastore: str = "running"
    ) -> LockContext:
        return connection.locked(target=datastore)
