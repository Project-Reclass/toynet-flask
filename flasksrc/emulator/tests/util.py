# This file is part of Toynet-Flask.
# 
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Tuple
from flasksrc.emulator.xmlParser import ToyTopoCfg, RouterCfg, SwitchCfg, HostCfg, InterfaceCfg


def makeToyTopoCfg(
        routers: List[str],
        switches: List[str],
        hosts: List[str],
        links: List[Tuple[str, str]],
        root: str = None
        ) -> ToyTopoCfg:

    MOCK_IP: str = "X.X.X.X/Y"
    MOCK_INTF: List[str] = []
    MOCK_DEFLT_ROUTE: str = "via Z.Z.Z.Z"

    (mockRouterCfgs, mockSwitchCfgs, mockHostCfgs, mockLinkCfgs) = (dict(), dict(), dict(), list())

    for rName in routers:
        mockRouterCfgs[rName] = RouterCfg(rName, MOCK_IP, MOCK_INTF)
    for sName in switches:
        mockSwitchCfgs[sName] = SwitchCfg(sName)
    for hName in hosts:
        mockHostCfgs[hName] = HostCfg(hName, MOCK_IP, MOCK_DEFLT_ROUTE)

    for names in links:
        mockLinkCfgs.append((InterfaceCfg(names[0]), InterfaceCfg(names[1])))

    return ToyTopoCfg(mockRouterCfgs, mockSwitchCfgs, mockHostCfgs, mockLinkCfgs, root)
