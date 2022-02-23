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
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.import sys
import sys
from toynet.toynet import ToyNet

def run(filepath:str):
    """Takes an XML file and either visualizes or interacts with a network simulation
        depending on the flags passed in.
        Both use the ToyNet object's ToyTopoConfig as input.
        run script currently defaults to visualization but no iteraction if no flags set.
    """
    toynet = ToyNet(filename=filepath)
    toynet.interact()

if __name__ == '__main__':
    filepath = sys.argv[1]
    run(filepath)
