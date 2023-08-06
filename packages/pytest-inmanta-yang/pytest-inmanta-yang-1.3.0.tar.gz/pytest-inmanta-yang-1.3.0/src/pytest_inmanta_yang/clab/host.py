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
import ipaddress
import os

from pydantic import BaseModel, Field

from pytest_inmanta_yang.clab.config import HostConfig
from pytest_inmanta_yang.netconf_device_helper import NetconfDeviceHelper


class ClabHost(BaseModel):
    lab_name: str
    lab_path: str = Field(alias="labPath")
    name: str
    container_id: str
    image: str
    kind: str
    state: str
    ipv4_address: ipaddress.IPv4Interface
    ipv6_address: ipaddress.IPv6Interface

    def config(self, cwd: str) -> HostConfig:
        lab_prefix = f"clab-{self.lab_name}"

        return HostConfig(
            username=os.getenv(NetconfDeviceHelper.ENV_VARIABLE_USERNAME, "admin"),
            password=os.getenv(NetconfDeviceHelper.ENV_VARIABLE_PASSWORD, "admin"),
            hostname=self.name,
            node_name=self.name[len(lab_prefix) + 1 :],
            ip_address=self.ipv4_address,
            lab_directory=os.path.join(cwd, lab_prefix),
        )
