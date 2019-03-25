from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self):
        "Create custom topology"
        Topo.__init__(self)

        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')

        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addswitch('s3')

        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        self.addLink(switch1, switch2)
        self.addLink(switch2, switch3)
        self.addLink(switch3, host3)
        self.addLink(switch3, host4)


topos = {'mytopo': (lambda: MyTopo())}