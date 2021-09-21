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
