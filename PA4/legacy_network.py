#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    #switches
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add switches\n')
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.0/24')  #IP assignment
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    r4 = net.addHost('r4', cls=Node, ip='192.168.0.0/30')  #IP assignment
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')

    r3 = net.addHost('r3', cls=Node, ip='10.0.1.0/24')  #IP assignment
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.0/24', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.0/24', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.0/24', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.0/24', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    net.addLink(s2, r5)
    net.addLink(s1, r3)

    net.addLink(r3, r4)
    
    net.addLink(r4, r5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()