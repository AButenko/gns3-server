#
# Copyright (C) 2020 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from . import Category, TemplateBase
from gns3server.schemas.compute.ethernet_switch_nodes import EthernetSwitchPort

from pydantic import Field
from typing import Optional, List
from enum import Enum

DEFAULT_PORTS = [
    dict(port_number=0, name="Ethernet0", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=1, name="Ethernet1", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=2, name="Ethernet2", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=3, name="Ethernet3", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=4, name="Ethernet4", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=5, name="Ethernet5", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=6, name="Ethernet6", vlan=1, type="access", ethertype="0x8100"),
    dict(port_number=7, name="Ethernet7", vlan=1, type="access", ethertype="0x8100"),
]


class ConsoleType(str, Enum):
    """
    Supported console types for Ethernet switch nodes.
    """

    none = "none"
    telnet = "telnet"


class EthernetSwitchTemplate(TemplateBase):

    category: Optional[Category] = "switch"
    default_name_format: Optional[str] = "Switch{0}"
    symbol: Optional[str] = ":/symbols/ethernet_switch.svg"
    ports_mapping: Optional[List[EthernetSwitchPort]] = Field(DEFAULT_PORTS, description="Ports")
    console_type: Optional[ConsoleType] = Field("none", description="Console type")


class EthernetSwitchTemplateUpdate(EthernetSwitchTemplate):

    pass
