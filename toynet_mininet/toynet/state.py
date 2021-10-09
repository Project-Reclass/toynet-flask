from toynet.toynet import ToyNet

class State():
    toynet_instance = None

    @staticmethod
    def getInstance():
        return State.toynet_instance

    @staticmethod
    def setInstance(instance:ToyNet):
        State.toynet_instance=instance
