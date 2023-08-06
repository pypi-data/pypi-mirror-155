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
DEFAULT_TIMEOUT = 30
NETCONF_RPC_TIMEOUT = "NETCONF_RPC_TIMEOUT"

NETCONF_NS_URN = "urn:ietf:params:xml:ns:netconf:base:1.0"

VENDOR_NOKIA = "nokia"
VENDOR_CISCO = "cisco"
VENDOR_JUNIPER = "juniper"
VENDORS = (VENDOR_NOKIA, VENDOR_CISCO, VENDOR_JUNIPER)
