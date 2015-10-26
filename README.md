# tripleo
TripleO templates to deploy a nice OpenStack overcloud.

The command used to deploy this overcloud:

```
stack@director:~$ cd /home/stack/
stack@director:~$ source ~/stackrc
stack@director:~$ openstack overcloud deploy --templates ~/templates/my-overcloud -e ~/templates/my-overcloud/environments/network-isolation.yaml -e ~/templates/my-overcloud/environments/net-multiple-nic-with-vlans.yaml -e ~/templates/my-overcloud/environments/storage-environment.yaml --control-scale 3 --compute-scale 1 --ceph-storage-scale 3 --control-flavor control --compute-flavor compute --ceph-storage-flavor ceph --ntp-server 10.26.235.251 --neutron-network-type vxlan --neutron-tunnel-types vxlan
```
