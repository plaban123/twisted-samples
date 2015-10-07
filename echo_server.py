from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.num_protocols = self.factory.num_protocols + 1
        self.transport.write(
            "Welcome! There are currently %d open connections. \n" % 
            (self.factory.num_protocols + 1))

    def connectionLost(self, reason):
        self.factory.num_protocols -= 1

    def dataReceived(self, data):
        print data
        self.transport.write(data)

class EchoFactory(Factory):
    def __init__(self, *args, **kwargs):
        self.num_protocols = 0
    def buildProtocol(self, addr):
        return Echo(self)
    

endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(EchoFactory())
reactor.run()
