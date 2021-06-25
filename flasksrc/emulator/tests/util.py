from typing import List, Tuple
from ..xmlParser import ToyTopoConfig, RouterConfig, SwitchConfig, HostConfig, InterfaceConfig


def makeToyTopoConfig(routers: List[str], switches: List[str], hosts: List[str], links: List[Tuple[str,str]],
    root: str=None)-> ToyTopoConfig:

    MOCK_IP: str = "X.X.X.X/Y"
    MOCK_INTF: List[str] = []
    MOCK_DEFLT_ROUTE: str = "via Z.Z.Z.Z"

    (mockRouterCfgs, mockSwitchCfgs, mockHostCfgs, mockLinkCfgs) = (dict(), dict(), dict(), list())

    for rName in routers:
        mockRouterCfgs[rName] = RouterConfig(rName, MOCK_IP, MOCK_INTF)
    for sName in switches:
        mockSwitchCfgs[sName] = SwitchConfig(sName)
    for hName in hosts:
        mockHostCfgs[hName] = HostConfig(hName, MOCK_IP, MOCK_DEFLT_ROUTE)

    for names in links:
        mockLinkCfgs.append((InterfaceConfig(names[0]), InterfaceConfig(names[1])))

    return ToyTopoConfig(mockRouterCfgs, mockSwitchCfgs, mockHostCfgs, mockLinkCfgs, root)
