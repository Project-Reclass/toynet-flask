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

from typing import List
from xml.etree import ElementTree as ET
from flasksrc.emulator.util.error import XMLParseError


def getDeviceList(deviceType: str, xmlTopology: ET):
    tag = deviceType + 'List'
    deviceList: ET.ElementTree = xmlTopology.find(tag)
    if deviceList is None:
        raise XMLParseError('No ' + tag + ' specified', xmlTopology)
    return deviceList


def addToDeviceListByName(names: List[str], deviceType: str, xmlTopology: ET):
    deviceList = getDeviceList(deviceType, xmlTopology)

    if deviceType == 'link':
        link = ET.Element('link')

        dvc1 = ET.Element('dvc')
        dvc1.attrib['name'] = names[0]
        dvc1Intf = ET.Element('intf')
        dvc1Intf.text = '0'  # TODO: must be real for mininet

        dvc2 = ET.Element('dvc')
        dvc2.attrib['name'] = names[1]
        dvc2Intf = ET.Element('intf')
        dvc2Intf.text = '0'  # TODO: must be real for mininet

        dvc1.append(dvc1Intf)
        dvc2.append(dvc2Intf)
        link.append(dvc1)
        link.append(dvc2)
        deviceList.append(link)

    elif deviceType == 'router':
        router = ET.Element('router')
        router.attrib['name'] = names[0]
        router.attrib['ip'] = '0.0.0.0/0'  # TODO: must be real for mininet
        routerIntf = ET.Element('intf')
        routerIntf.text = '0'  # TODO: must be real for mininet

        router.append(routerIntf)  # TODO: may be a list
        deviceList.append(router)

    elif deviceType == 'switch':
        switch = ET.Element('switch')
        switch.attrib['name'] = names[0]

        deviceList.append(switch)

    elif deviceType == 'host':
        host = ET.Element('host')
        host.attrib['name'] = names[0]
        host.attrib['ip'] = '0.0.0.0/0'  # TODO: must be real for mininet

        defaultRouter = ET.Element('defaultRouter')
        defaultRouterName = ET.Element('name')
        defaultRouterIntf = ET.Element('intf')
        defaultRouterName.text = 'r0'  # TODO: must be real for mininet
        defaultRouterIntf.text = '0'  # TODO: must be real for mininet

        defaultRouter.append(defaultRouterName)
        defaultRouter.append(defaultRouterIntf)
        host.append(defaultRouter)
        deviceList.append(host)

    else:
        pass
        # raise error

    return xmlTopology


def removeFromDeviceListByName(names: List[str], deviceType: str, xmlTopology: ET):
    deviceList = getDeviceList(deviceType, xmlTopology)

    if deviceType == 'link':
        for link in deviceList.findall('link'):
            dvcs = [dvc.attrib['name'] for dvc in link.findall('dvc')]
            [n0, n1, d0, d1] = [names[0], names[1], dvcs[0], dvcs[1]]

            if (n0 == d0 and n1 == d1) or (n0 == d1 and n1 == d0):
                deviceList.remove(link)
                return xmlTopology
    else:
        for device in deviceList.iter(deviceType):
            if device.attrib['name'] == names[0]:
                deviceList.remove(device)
                return xmlTopology


def parseModificationCommand(command: str, xmlTopology: ET.ElementTree):
    tokens = command.split(' ')

    action = tokens[0]
    deviceType = tokens[1]
    names = tokens[2:]

    if action == 'add':
        return addToDeviceListByName(names, deviceType, xmlTopology)
    if action == 'remove':
        return removeFromDeviceListByName(names, deviceType, xmlTopology)
