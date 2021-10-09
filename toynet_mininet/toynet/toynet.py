from toynet.toytopo import ToyTopo
import toynet.xmlParser as parser
from toynet.xmlParser import ToyTopoConfig

from mininet.net import Mininet
from mininet.cli import CLI

class ToyNet():
    def __init__(self, filename:str=None, filecontent:str=None):
        #can throw: XMLParseError, TypeCheckError
        if filename is not None and filecontent is not None:
            raise Exception('Can only specify one of filename or filecontent- not both')
        elif filename is not None:
            self.config:ToyTopoConfig = parser.parseXMLFilename(filename)
        elif filecontent is not None:
            self.config:ToyTopoConfig = parser.parseXMLContent(filecontent)
        else:
            raise Exception('Must specify filename or filecontent')

        self.topology = ToyTopo(self.config)
        self.mininet = Mininet(topo=self.topology)

    def interact(self):
        print('__INFO___ Generating Interactive Mininet Instance')
        #self.topology=ToyTopo(self.config) # ToyNet( topo=TreeTopo( depth=2, fanout=6 ) )
        #self.mininet = Mininet(topo=self.topology)

        self.mininet.start()
        CLI( self.mininet )
        self.mininet.stop()

    def start(self):
        if self.mininet is not None:
            self.mininet.start()

    def cmd(self, command:str):
        toks = command.split()
        host_one = None
        host_two = None
        execute_me = ''

        #validate that the minimum number of arguments are provided
        if len(toks) > 1:
            try:
                host_one = self.mininet.get(toks[0])
            except KeyError as e:
                return 'Invalid host: ' + toks[0]
        else:
            return 'Invalid command: ' + command
        
        cmd = toks[1]
        #handle ping separately because default behavior is infinite ping, and requires a target host
        if cmd == 'ping':
            try:
                host_two = self.mininet.get(toks[2])
            except KeyError:
                return 'Invalid host: ' + toks[2]
            except IndexError:
                return 'No destination host provided'
            execute_me = '%s -c 3 %s' % (cmd, host_two.IP())
        #all other commands are passed to the host directly; host will return errors as appropriate
        else:
            execute_me = ''.join(toks[1:])

        return host_one.cmd(execute_me)

    def stop(self):
        if self.mininet is not None:
            self.mininet.stop()

    def restart(self, new_topology=None):
        print(new_topology)
        self.stop()
        if new_topology is not None:
            #can throw: XMLParseError, TypeCheckError
            self.config:ToyTopoConfig = parser.parseXMLContent(new_topology)
            self.topology = ToyTopo(self.config)
            self.mininet = Mininet(topo=self.topology)
        self.start()

