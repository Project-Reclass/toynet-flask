from xml.etree import ElementTree
from typing import List, Tuple, Dict
import functools

from flasksrc.emulator.util.error import XMLParseError
from flasksrc.emulator.util import typecheck as tc


class Name(str):
    pass


class IP(str):
    pass


class InterfaceCfg():
    """A representation device interfaces in network configurations parsed from XML file.
        Currently, we only track interfaces on routers.
    Raises:
        TypeCheckError
    Attributes:
        deviceName:     Name -- name of device on which interface exists
        interfaceNum:   int -- identifying index on device used to generate interface name
        ip:             IP -- optional IP-address associated with interface for routing
    """
    def __init__(self, deviceName: Name, interfaceNum: int = 0, ip: IP = None):
        tc.inputTypeCheck(deviceName, 'deviceName', str)
        tc.inputTypeCheck(interfaceNum, 'interfaceNum', int)
        if ip is not None:
            tc.inputTypeCheck(ip, 'ip', str)

        self.deviceName: Name = deviceName
        self.name: str = deviceName + '-eth' + str(interfaceNum)
        self.ip: IP = ip

    def __str__(self) -> str:
        ipStr: str = ' | ip: ' + self.ip if self.ip is not None else ''
        return 'Interface { name: ' + self.name + ipStr + '}'

    def toShortString(self) -> str:
        ipStr: str = ' -> ' + self.ip if self.ip is not None else ''
        return '[' + self.name + ipStr + ']'


class DeviceConfig():
    """Abstraction for all Devices int network configurations parsed from XML file."""
    pass


class RouterCfg(DeviceConfig):
    """A representation routers in network configurations parsed from XML file.
        Interfaces are tracked on routers to enable default gateway configuratinos on hosts
    Raises:
        TypeCheckError
    Attributes:
        name:           Name -- unique identifying name of router in topology
        ip:             IP -- IP-address associated with interface for routing
        intfs:          List[IP] -- list of routable IP-addresses for interfaces
    """
    def __init__(self, name: Name, ip: IP, interfaces: List[IP]):
        tc.inputTypeCheck(name, 'name', str)
        tc.inputTypeCheck(ip, 'ip', str)
        tc.inputTypeCheck(interfaces, 'interfaces', list)

        self.name: Name = name
        self.ip: IP = ip
        self.intfs: List[InterfaceCfg] = list()

        for (i, intf) in enumerate(interfaces):
            self.intfs.append(InterfaceCfg(self.name, i, intf))

    def getIntfByIdx(self, idx: int) -> InterfaceCfg:
        return self.intfs[idx]

    def __str__(self) -> str:
        intfs: str = functools.reduce(
            lambda output, intfstr: (output + ', ' + intfstr),
            map(lambda intf: intf.toShortString(), self.intfs)
        )
        return 'Router { name: ' + self.name + ' | ip: ' + self.ip + ' | intfs: ' + intfs + ' }'


class SwitchCfg(DeviceConfig):
    """A representation switches in network configurations parsed from XML file.
        Interfaces are not currently tracked on switches.
    Raises:
        TypeCheckError
    Attributes:
        name:           Name -- unique identifying name of router in topology
    """
    def __init__(self, name: Name):
        tc.inputTypeCheck(name, 'name', str)
        self.name: Name = name

    def __str__(self) -> str:
        return 'Switch { name: ' + self.name + ' }'


class HostCfg(DeviceConfig):
    """A representation hosts in network configurations parsed from XML file.
        Interfaces are not currently tracked on hosts and we assume there is one
        interface per host.
    Raises:
        TypeCheckError
    Attributes:
        name:           Name -- unique identifying name of router in topology
        ip:             IP -- IP address associated with host and its interface
    """
    def __init__(self, name: Name, ip: IP, defaultRtrIp: IP):
        tc.inputTypeCheck(name, 'name', str)
        tc.inputTypeCheck(ip, 'ip', str)
        tc.inputTypeCheck(defaultRtrIp, 'defaultRtrIp', str)

        self.name: Name = name
        self.ip: IP = ip
        self.defaultRoute: str = 'via ' + defaultRtrIp.split('/')[0]

    def __str__(self) -> str:
        return 'Host { name: ' + self.name + ' | ip ' + self.ip + \
            ' | route: ' + self.defaultRoute + ' }'


class ToyTopoCfg():
    """A representation of all devices in network configurations parsed from XML file.
        Outputed by parseXML function. Ingested by Mininet to run their simulations.
    Attributes:
        name:           Name -- unique identifying name of router in topology
        ip:             IP -- IP address associated with host and its interface
    """
    def __init__(
            self,
            routers: List[RouterCfg],
            switches: List[SwitchCfg],
            hosts: List[HostCfg],
            links: List[Tuple[InterfaceCfg, InterfaceCfg]],
            root: str = None
            ):
        self.root: str = root
        self.routers: List[RouterCfg] = routers
        self.switches: List[SwitchCfg] = switches
        self.hosts: List[HostCfg] = hosts
        self.links: List[Tuple[InterfaceCfg, InterfaceCfg]] = links


def parseXML(data: str) -> ToyTopoCfg:
    """Converts XML structure in provided fiel into a ToyTopoCfg which can
        be processed by Mininet
    Raises:
        XMLParseError, TypeCheckError
    """
    tc.inputTypeCheck(data, 'data', str)

    try:
        XMLconfigurations: ElementTree = ElementTree.fromstring(data)
        root: str = XMLconfigurations.find('root').text
    except Exception as e:
        raise XMLParseError('error parsing ElementTree object: ' + str(e), data)

    XMLrouterList: ElementTree.ElementTree = XMLconfigurations.find('routerList')
    if XMLrouterList is None:
        raise XMLParseError('No routerList specified', data)

    XMLswitchList: ElementTree.ElementTree = XMLconfigurations.find('switchList')
    if XMLswitchList is None:
        raise XMLParseError('No switchList specified', data)

    XMLhostList: ElementTree.ElementTree = XMLconfigurations.find('hostList')
    if XMLhostList is None:
        raise XMLParseError('No hostList specified', data)

    XMLlinkList: ElementTree.ElementTree = XMLconfigurations.find('linkList')
    if XMLlinkList is None:
        raise XMLParseError('No linkList specified', data)

    routers: Tuple[Dict[str:RouterCfg]] = dict()
    for r in XMLrouterList.iter('router'):
        interfaces: List[IP] = [XMLintf.text for XMLintf in r.findall('intf')]
        routers[r.attrib['name']] = RouterCfg(r.attrib['name'], r.attrib['ip'], interfaces)

    switches: Tuple[Dict[str:SwitchCfg]] = dict()
    for s in XMLswitchList.iter('switch'):
        switchName: str = s.attrib['name']
        switches[switchName] = SwitchCfg(switchName)

    hosts: Tuple[Dict[str:HostCfg]] = dict()
    for h in XMLhostList.iter('host'):
        XMLdefaultRtr: ElementTree.ElementTree = h.find('defaultRouter')
        defName: Name = XMLdefaultRtr.find('name').text
        defIpIdx: int = int(XMLdefaultRtr.find('intf').text)

        interface: InterfaceCfg = routers[defName].getIntfByIdx(defIpIdx)
        hosts[h.attrib['name']] = HostCfg(h.attrib['name'], h.attrib['ip'], interface.ip)

    links: List[Tuple[InterfaceCfg, InterfaceCfg]] = list()
    for link in XMLlinkList.iter('link'):
        dvcs: List[InterfaceCfg] = list()
        for dvc in link.iter('dvc'):
            dvcNm: Name = dvc.attrib['name']
            if dvcNm.startswith('r'):
                dvcs.append(routers[dvcNm].getIntfByIdx(int(dvc.find('intf').text)))
            elif dvcNm.startswith('s'):
                dvcs.append(InterfaceCfg(dvcNm, int(dvc.find('intf').text)))
            else:
                dvcs.append(InterfaceCfg(dvcNm))
        links.append((dvcs[0], dvcs[1]))

    return ToyTopoCfg(routers, switches, hosts, links, root)
