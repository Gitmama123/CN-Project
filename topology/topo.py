#!/usr/bin/env python3
r"""Triangle topology: 3 OpenFlow 1.3 switches, 6 hosts, remote Ryu controller.

        s1 ------ s2
         \        /
          \      /
            s3

h1,h2 -> s1   h3,h4 -> s2   h5,h6 -> s3
A NAT node (root namespace, 10.0.0.254) lets hosts send UDP telemetry to the
controller machine: agents send to 10.0.0.254:9999.

Run:  sudo python3 topo.py
"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info


class TriangleTopo(Topo):
    def build(self):
        s1, s2, s3 = [self.addSwitch(f"s{i}", protocols="OpenFlow13") for i in (1, 2, 3)]
        hosts = [self.addHost(f"h{i}") for i in range(1, 7)]

        # hosts: two per switch
        for h, s in zip(hosts, [s1, s1, s2, s2, s3, s3]):
            self.addLink(h, s)

        # triangle links (TCLink so tc netem / bandwidth limits work)
        self.addLink(s1, s2, cls=TCLink)
        self.addLink(s2, s3, cls=TCLink)
        self.addLink(s1, s3, cls=TCLink)


def run():
    net = Mininet(
        topo=TriangleTopo(),
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True,
    )
    net.addController("c0", controller=RemoteController, ip="127.0.0.1", port=6653)

    # NAT lives in the root namespace so hosts can reach the Ryu collector
    nat = net.addNAT(connect="s1", ip="10.0.0.254/8")
    net.start()
    nat.configDefault()

    info("*** Telemetry collector address for agents: 10.0.0.254:9999\n")
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
