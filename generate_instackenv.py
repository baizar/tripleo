#!/usr/bin/python
#
# Copyright(C) 2015 Felipe Alfaro Solana
#
# Python script used to populate 'instackenv.json' file, which describes
# the Ironic nodes used to deploy an OpenStack Overcloud.
#
# This script supports both baremetal nodes and KVM-based virtual machines.

from collections import OrderedDict
from IPy import IP
import json

def kvm_nodes():
  """KVM nodes.
  """

  return [
    # Controller
    ( IP('10.95.247.20'), [ '52:54:00:fa:fd:34', ], 8, 28, 150, ),
    ( IP('10.95.247.21'), [ '52:54:00:97:d8:c2', ], 8, 42, 512, ),
    ( IP('10.95.247.22'), [ '52:54:00:95:0d:a8', ], 8, 42, 512, ),
  ]


def idrac_nodes():
  """iDRAC baremetal nodes.
  """

  return [
    # Ceph
    #( 'ESAH-OSTT-SN01P', IP('172.24.12.243'), 
    #  [ 'b0:83:fe:ca:d1:b4', 'b0:83:fe:ca:d1:b6', ], 24, 131072, 1116, ),
    #( 'ESAH-OSTT-SN02P', IP('172.24.12.242'),
    #  [ 'b0:83:fe:cd:48:fc', 'b0:83:fe:cd:48:fe', ], 24, 131072, 1116, ),
    #( 'ESAH-OSTT-SN03P', IP('172.24.12.241'),
    #  [ 'b0:83:fe:cd:48:42', 'b0:83:fe:cd:48:44', ], 24, 131072, 1116, ),
    # Swift
    #( 'ESAH-OSTT-SN53P', IP('172.24.12.240'),
    #  [ 'b8:2a:72:d9:25:8a', 'b8:2a:72:d9:25:8c', ], 24, 131072, 1116, ),
    #( 'ESAH-OSTT-SN52P', IP('172.24.12.239'),
    #  [ 'b0:83:fe:ca:98:93', 'b0:83:fe:ca:98:95', ], 24, 131072, 1116, ),
    #( 'ESAH-OSTT-SN51P', IP('172.24.12.238'),
    #  [ 'b0:83:fe:cd:50:e5', 'b0:83:fe:cd:50:e7', ], 24, 131072, 1116, ),
    # Compute
    ( 'PROD-EPG-OSTKN-01', IP('10.95.66.91'),
      [ '74:86:7A:DA:29:A4'], 24, 196608, 1232, ),
    ( 'PROD-EPG-OSTKN-02', IP('10.95.66.71'),
      [ 'E0:DB:55:08:57:14' ], 24, 196608, 1232, ),
    ( 'PROD-EPG-OSTKN-03', IP('10.95.65.128'),
      [ 'E0:DB:55:03:59:E4', ], 24, 196608, 1232, ),
  ]

def generate_drac_nodes():
  """Generate information about iDRAC nodes."""

  with open('.idrac_password', 'r') as f:
    idrac_password = f.read().strip()
  print idrac_password

  nodes = []
  for _, pm_addr, mac, vcpu, memory, disk in idrac_nodes():
    d = OrderedDict()
    d.update({'pm_addr': str(pm_addr)})
    d.update({'pm_user': 'root'})
    d.update({'pm_password': idrac_password})
    d.update({'pm_type': 'pxe_drac'})
    d.update({'mac': mac})
    d.update({'cpu': str(vcpu)})
    d.update({'memory': str(memory)})
    d.update({'disk': str(disk)})
    d.update({'arch': 'x86_64'})
    nodes.append(d)
  return nodes

def generate_kvm_nodes():
  """Generate information about SSH nodes."""

  # Read the SSH private key used to connect to QEMU+SSH (to control KVM
  # virtual machines with libvirtd).
  with open('.ssh/id_rsa', 'r') as f:
    ssh_key = ''.join(f.readlines())

  nodes = []
  for pm_addr, mac, vcpu, memory, disk in kvm_nodes():
    d = OrderedDict()
    d.update({'pm_addr': str(pm_addr)})
    d.update({'pm_user': 'stack'})
    d.update({'pm_password': ssh_key})
    d.update({'pm_type': 'pxe_ssh'})
    d.update({'mac': mac})
    d.update({'cpu': str(vcpu)})
    d.update({'memory': str(memory * 1024)})
    d.update({'disk': str(disk)})
    d.update({'arch': 'x86_64'})
    nodes.append(d)
  return nodes

nodes = []
nodes += generate_kvm_nodes()
nodes += generate_drac_nodes()

print (json.dumps({"nodes": nodes}, sort_keys=False, indent=2))
