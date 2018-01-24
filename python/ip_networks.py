# 'EStroev'
from ipaddress import IPv4Network
from ipaddress import IPv4Address
from ipaddress import ip_network
from ipaddress import summarize_address_range
from ipaddress import collapse_addresses
import socket, struct


def summarize(data):
    for line in data.split('\n'):
        if line:
            firstAddr, lastAddr = line.split('-')
            firstAddr = firstAddr.strip()
            lastAddr = lastAddr.strip()
            nets = [ipaddr for ipaddr in summarize_address_range(IPv4Address(firstAddr), IPv4Address(lastAddr))]
            yield nets


def summarize_2(net_1, net_2):
    return [ipaddr for ipaddr in summarize_address_range(IPv4Address(net_1), IPv4Address(net_2))]


def exclude(net_1, net_2):
    return list(ip_network(net_1).address_exclude(ip_network(net_2)))


def collapse(net_1, net_2, net_3, net_4, net_5, net_6, net_7):
    nets = [ipaddr for ipaddr in collapse_addresses(
        [
            IPv4Network(net_1),
            IPv4Network(net_2),
            IPv4Network(net_3),
            IPv4Network(net_4),
            IPv4Network(net_5),
            IPv4Network(net_6),
            IPv4Network(net_7),
        ]
    )]
    return nets


def networkToIP(network):
    return list(ip_network(network).hosts())


def networkToSubnetworks(network, prefixlen_diff=2):
    return list(ip_network(network).subnets(prefixlen_diff=prefixlen_diff))


def ipToNetwork(ip, network):
    return IPv4Address(ip) in IPv4Network(network)


def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def long2ip(long):
    return socket.inet_ntoa(struct.pack('!L', long))


def networkToSubnetworks(network, prefixlen_diff=2):
    return list(ip_network(network).subnets(prefixlen_diff=prefixlen_diff))


data = '''92.39.108.148 - 92.39.108.151'''
for net in summarize(data):
    print(net)