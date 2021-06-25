import unittest

from flasksrc.emulator.xmlParser import HostCfg
import flasksrc.emulator.xmlParser as parser


class TestXMLParserMethods(unittest.TestCase):
    sample_linuxrouter = './flasksrc/emulator/tests/sample_inputs/linuxrouter.xml'

    def test_XMLParser__linuxRouter(self):
        setOfRouterNames = {'r0'}
        setOfSwitchNames = {'s1', 's2', 's3'}
        setOfHostNames = {'h1', 'h2', 'h3'}

        xml_content = ''
        with open(self.sample_linuxrouter, 'r') as file_ptr:
            xml_content = file_ptr.read()
        config = parser.parseXML(xml_content)

        self.assertEqual(len(setOfRouterNames), len(config.routers))
        self.assertEqual(len(setOfSwitchNames), len(config.switches))
        self.assertEqual(len(setOfHostNames), len(config.hosts))

        for rNames in config.routers.keys():
            self.assertTrue(rNames in setOfRouterNames)
        for sNames in config.switches.keys():
            self.assertTrue(sNames in setOfSwitchNames)
        for hNames in config.hosts.keys():
            self.assertTrue(hNames in setOfHostNames)

        router0 = config.routers['r0']
        self.assertEqual(router0.name, 'r0')
        self.assertEqual(router0.ip, '192.168.1.1/24')
        self.assertEqual(len(router0.intfs), 3)
        setOfR0InterfaceIps = {'192.168.1.1/24', '172.16.0.1/12', '10.0.0.1/8'}
        setOfR0InterfaceNames = {'r0-eth0', 'r0-eth1', 'r0-eth2'}
        for intf in router0.intfs:
            self.assertTrue(intf.ip in setOfR0InterfaceIps)
            self.assertTrue(intf.name in setOfR0InterfaceNames)

        host1 = config.hosts['h1']
        self.assertEqual(host1.name, 'h1')
        self.assertEqual(host1.ip, '192.168.1.100/24')
        self.assertEqual(host1.defaultRoute, 'via 192.168.1.1')

        host2 = config.hosts['h2']
        self.assertEqual(host2.name, 'h2')
        self.assertEqual(host2.ip, '172.16.0.100/12')
        self.assertEqual(host2.defaultRoute, 'via 172.16.0.1')

        host3 = config.hosts['h3']
        self.assertEqual(host3.name, 'h3')
        self.assertEqual(host3.ip, '10.0.0.100/8')
        self.assertEqual(host3.defaultRoute, 'via 10.0.0.1')

        self.assertEqual(len(config.links), 6)

        mapOfLinks = dict()
        for (i1, i2) in config.links:
            mapOfLinks[(i1.deviceName, i2.deviceName)] = (i1, i2)

        self.assertTrue(('r0', 's1') in mapOfLinks)
        link = mapOfLinks[('r0', 's1')]
        self.assertEqual(link[0].deviceName, 'r0')
        self.assertEqual(link[0].name, 'r0-eth0')
        self.assertEqual(link[0].ip, '192.168.1.1/24')
        self.assertEqual(link[1].deviceName, 's1')
        self.assertEqual(link[1].name, 's1-eth0')

        self.assertTrue(('r0', 's2') in mapOfLinks)
        link = mapOfLinks[('r0', 's2')]
        self.assertEqual(link[0].deviceName, 'r0')
        self.assertEqual(link[0].name, 'r0-eth1')
        self.assertEqual(link[0].ip, '172.16.0.1/12')
        self.assertEqual(link[1].deviceName, 's2')
        self.assertEqual(link[1].name, 's2-eth0')

        self.assertTrue(('r0', 's3') in mapOfLinks)
        link = mapOfLinks[('r0', 's3')]
        self.assertEqual(link[0].deviceName, 'r0')
        self.assertEqual(link[0].name, 'r0-eth2')
        self.assertEqual(link[0].ip, '10.0.0.1/8')
        self.assertEqual(link[1].deviceName, 's3')
        self.assertEqual(link[1].name, 's3-eth0')

        self.assertTrue(('s1', 'h1') in mapOfLinks)
        link = mapOfLinks[('s1', 'h1')]
        self.assertEqual(link[0].deviceName, 's1')
        self.assertEqual(link[0].name, 's1-eth1')
        self.assertEqual(link[1].deviceName, 'h1')

        self.assertTrue(('s2', 'h2') in mapOfLinks)
        link = mapOfLinks[('s2', 'h2')]
        self.assertEqual(link[0].deviceName, 's2')
        self.assertEqual(link[0].name, 's2-eth1')
        self.assertEqual(link[1].deviceName, 'h2')

        self.assertTrue(('s3', 'h3') in mapOfLinks)
        link = mapOfLinks[('s3', 'h3')]
        self.assertEqual(link[0].deviceName, 's3')
        self.assertEqual(link[0].name, 's3-eth1')
        self.assertEqual(link[1].deviceName, 'h3')

    def test_XMLParser__HostCfg(self):
        hostCfg = HostCfg('hostName', '192.168.1.100/24', '192.168.1.1/24')

        self.assertEqual(hostCfg.name, 'hostName')
        self.assertEqual(hostCfg.ip, '192.168.1.100/24')
        self.assertEqual(hostCfg.defaultRoute, 'via 192.168.1.1')
