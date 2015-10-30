# tripleo
TripleO templates to deploy a nice OpenStack overcloud.

The command used to deploy this overcloud:

```
stack@director:~$ cd /home/stack/
stack@director:~$ source ~/stackrc
```

Nova always requires a flavor to match; and OSP director attempts to use a hard coded flavor known as "baremetal". The specifications don't have to be exact to our overcloud nodes, but at the least they must be satisfied by our nodes capabilities:

```
stack@esah-ostt-uc01p:~$ openstack flavor create --id auto --ram 65535 --disk 100 --vcpus 16 baremetal
stack@esah-ostt-uc01p:~$ openstack flavor set --property "cpu_arch"="x86_64" --property "capabilities:boot_option"="local" baremetal
```

Now, let's create appropriately sized flavors, noting that we need to specify the disk size slightly smaller than our nodes have so partitioning works properly.

## Control

```
stack@esah-ostt-uc01p:~$ openstack flavor create --id auto --ram 102400 --disk 500 --vcpus 24 control
stack@esah-ostt-uc01p:~$ openstack flavor set --property "cpu_arch"="x86_64" --property "capabilities:boot_option"="local" --property "capabilities:profile"="control" control

for NODE in c67e91bd-df51-4cdd-9602-2fc6d70cc41a 446c959d-1698-4016-8fcf-26fd3c2a7715 8a7a89a1-4184-4b8f-aff5-8d44059e9f66; do
  ironic node-update $NODE add properties/capabilities='profile:control,boot_option:local'
done
```

## Compute

```
stack@esah-ostt-uc01p:~$ openstack flavor create --id auto --ram 196608 --disk 2000 --vcpus 2 compute
stack@esah-ostt-uc01p:~$ openstack flavor set --property "cpu_arch"="x86_64" --property "capabilities:boot_option"="local" --property "capabilities:profile"="compute" compute

for NODE in a31392bd-3b61-4183-8220-aff1369c44a4 91af555a-2866-4904-adf4-a3f48b130c73 10fe46f9-3403-4160-962f-8ae384cd913c; do
  ironic node-update $NODE add properties/capabilities='profile:compute,boot_option:local'
done
```

## CEPH storage

```
stack@esah-ostt-uc01p:~$ openstack flavor create --id auto --ram 131072 --disk 180 --vcpus 24 ceph-storage
stack@esah-ostt-uc01p:~$ openstack flavor set --property "cpu_arch"="x86_64" --property "capabilities:boot_option"="local" --property "capabilities:profile"="ceph-storage" ceph-storage

for NODE in 3e04f421-4650-4498-9b2b-66e1d06d036f 5e247f75-db78-4982-9ba8-a57ca37b19b2 167f7b35-dbfd-4d57-84e7-97b027e703f9; do
  ironic node-update $NODE add properties/capabilities='profile:ceph-storage,boot_option:local'
done
```

## Swift storage

```
stack@esah-ostt-uc01p:~$ openstack flavor create --id auto --ram 131072 --disk 1000 --vcpus 24 swift-storage
stack@esah-ostt-uc01p:~$ openstack flavor set --property "cpu_arch"="x86_64" --property "capabilities:boot_option"="local" --property "capabilities:profile"="swift-storage" swift-storage

for NODE in f4ced329-d991-4021-8df6-64a61407d1d4 7ff1c3b8-c786-4e01-88aa-4d1187e0f770 ab270fa6-14ae-433d-869d-06da0ebc87cc; do
  ironic node-update $NODE add properties/capabilities='profile:swift-storage,boot_option:local'
done
```

# Deploy

```
stack@director:~$ openstack overcloud deploy --templates ~/templates/my-overcloud -e ~/templates/my-overcloud/environments/network-isolation.yaml -e ~/templates/my-overcloud/environments/network-environment.yml -e ~/templates/my-overcloud/environments/storage-environment.yaml --control-scale 3 --compute-scale 1 --ceph-storage-scale 3 --control-flavor control --compute-flavor compute --ceph-storage-flavor ceph-storage --ntp-server 10.26.235.251 --neutron-network-type vxlan --neutron-tunnel-types vxlan
```
