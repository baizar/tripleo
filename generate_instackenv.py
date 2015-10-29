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

"""
CEPH machines:

Disk /dev/sdb: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdf: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdd: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdh: 1200.2 GB, 1200243695616 bytes
Disk /dev/sde: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdk: 200.0 GB, 200049647616 bytes
Disk /dev/sdc: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdi: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdg: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdj: 200.0 GB, 200049647616 bytes
Disk /dev/sdl: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdm: 1200.2 GB, 1200243695616 bytes
Disk /dev/sdn: 1200.2 GB, 1200243695616 bytes
Disk /dev/sda: 1200.2 GB, 1200243695616 bytes
"""


def kvm_nodes():
  """KVM nodes.
  """

  return [
    # Controller
    ( IP('172.24.12.248'), [ '52:54:00:d4:c0:da', ], 24, 100, 512, ),
    ( IP('172.24.12.246'), [ '52:54:00:d4:c0:dc', ], 24, 100, 512, ),
    ( IP('172.24.12.244'), [ '52:54:00:d4:c0:de', ], 24, 100, 512, ),
  ]


def idrac_nodes():
  """iDRAC baremetal nodes.
  """

  return [
    # Ceph
    ( 'ESAH-OSTT-SN01P', IP('172.24.12.243'),
      [ 'b0:83:fe:ca:d1:b4', 'b0:83:fe:ca:d1:b6', ], 24, 131072, 1116, ),
    ( 'ESAH-OSTT-SN02P', IP('172.24.12.242'),
      [ 'b0:83:fe:cd:48:fc', 'b0:83:fe:cd:48:fe', ], 24, 131072, 1116, ),
    ( 'ESAH-OSTT-SN03P', IP('172.24.12.241'),
      [ 'b0:83:fe:cd:48:42', 'b0:83:fe:cd:48:44', ], 24, 131072, 1116, ),
    # Swift
    ( 'ESAH-OSTT-SN53P', IP('172.24.12.240'),
      [ 'b8:2a:72:d9:25:8a', 'b8:2a:72:d9:25:8c', ], 24, 131072, 1116, ),
    ( 'ESAH-OSTT-SN52P', IP('172.24.12.239'),
      [ 'b0:83:fe:ca:98:93', 'b0:83:fe:ca:98:95', ], 24, 131072, 1116, ),
    ( 'ESAH-OSTT-SN51P', IP('172.24.12.238'),
      [ 'b0:83:fe:cd:50:e5', 'b0:83:fe:cd:50:e7', ], 24, 131072, 1116, ),
    # Compute
    ( 'ESAH-OSTT-CN01P', IP('172.24.12.237'),
      [ 'c8:1f:66:f0:8e:e9', 'c8:1f:66:f0:8e:eb', ], 24, 196608, 2232, ),
    ( 'ESAH-OSTT-CN02P', IP('172.24.12.236'),
      [ 'b8:2a:72:d6:72:4b', 'b8:2a:72:d6:72:4d', ], 24, 196608, 2232, ),
# Reserved for the testbed environment
#   ( 'ESAH-OSTT-CN03P', IP('172.24.12.235'),
#     [ 'b8:2a:72:d6:81:5c', 'b8:2a:72:d6:81:5e', ], 24, 196608, 2232, ),
    ( 'ESAH-OSTT-CN04P', IP('172.24.12.234'),
      [ 'c8:1f:66:f5:8d:a2', 'c8:1f:66:f5:8d:a4', ], 24, 196608, 2232, ),
  ]

def generate_drac_nodes():
  """Generate information about iDRAC nodes."""

  nodes = []
  for _, pm_addr, mac, vcpu, memory, disk in idrac_nodes():
    d = OrderedDict()
    d.update({'pm_addr': str(pm_addr)})
    d.update({'pm_user': 'root'})
    d.update({'pm_password': '$deng2015'})
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
