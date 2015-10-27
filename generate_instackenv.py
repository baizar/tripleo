#!/usr/bin/python
#
# Copyright(C) 2015 Felipe Alfaro Solana
#
# Python script used to populate 'instackenv.json' file, which describes
# the Ironic nodes used to deploy an OpenStack Overcloud.
#
# This script supports both baremetal nodes and KVM-based virtual machines.

from collections import OrderedDict
import json

# Read the SSH private key used to connect to QEMU+SSH (to control KVM
# virtual machines with libvirtd).
with open('.ssh/id_rsa', 'r') as f:
  ssh_key = ''.join(f.readlines())

ssh_nodes = [
  ( '172.24.12.248', '52:54:00:d4:c0:da', 24, 104857600, 512, ),
  ]

def generate_ssh_nodes():
  """Generate information about SSH nodes."""

  nodes = []
  for pm_addr, mac, vcpu, memory, disk in ssh_nodes:
    d = OrderedDict()
    d.update({'pm_addr': pm_addr})
    d.update({'pm_user': 'stack'})
    d.update({'pm_password': ssh_key})
    d.update({'pm_type': 'pxe_ssh'})
    d.update({'mac': [ mac ]})
    d.update({'cpu': str(vcpu)})
    d.update({'memory': str(memory)})
    d.update({'disk': str(disk)})
    d.update({'arch': 'x86_64'})
    nodes.append(d)
  return nodes

nodes = []
nodes += generate_ssh_nodes()

# Generate the output 'instackenv.json'
with open('instackenv.json', 'w') as f:
  print >>f, json.dumps({"nodes": nodes}, sort_keys=False, indent=2)
