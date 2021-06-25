from typing import List, Tuple
from flasksrc.emulator.xmlParser import ToyTopoCfg, RouterCfg, SwitchCfg, HostCfg, InterfaceCfg


def makeToyTopoCfg(
        routers: List[str],
        switches: List[str],
        hosts: List[str],
        links: List[Tuple[str,str]],
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
