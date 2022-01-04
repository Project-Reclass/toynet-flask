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

from typing import Dict, Any

from mininet.node import Node
from mininet.topo import Topo


from toynet.xmlParser import ToyTopoConfig

# To see Routing Table on a Router: print( net[ 'r0' ].cmd( 'route' ) )
# These classes are copied from examples/linuxrouter.py and modified

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class ToyTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, config:ToyTopoConfig, **_opts):
        devices: Dict[str,Any]= dict()

        for r in config.routers.values():
            devices[r.name] = self.addNode(r.name, cls=LinuxRouter, ip=r.ip)

        for s in config.switches.values():
            devices[s.name] = self.addSwitch(s.name)

        for h in config.hosts.values():
            devices[h.name] = self.addHost(h.name, ip=h.ip, defaultRoute=h.defaultRoute)

        for (l1,l2) in config.links:
            (intfName1, params1, intfName2, params2) = (None, None, None, None)

            if(l1.deviceName.startswith('r')): (intfName1, params1) = (l1.name, {'ip': l1.ip})
            if(l2.deviceName.startswith('r')): (intfName2, params2) = (l2.name, {'ip': l2.ip})

            self.addLink(
                devices[l1.deviceName],
                devices[l2.deviceName],
                intfName1=intfName1,
                intfName2=intfName2,
                params1=params1,
                params2=params2
            )
