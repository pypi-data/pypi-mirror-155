# python-esileapclient

Python API for interacting with ESI-Leap

### Overview

This is a client for the OpenStack Lease API. It provides:

   - a openstack command-line plugin: openstack lease

python-esileapclient is licensed under the Apache License, Version 2.0, like the rest of OpenStack.

### openstack lease CLI

The openstack lease command-line interface is available when the lease plugin (included in this package) is used with the `OpenStackClient https://docs.openstack.org/python-openstackclient/latest/

The client uses keystone to look for the lease service and currently does not allow for endpoint overriding.

To install this package,
 - clone this repository
 - install all requirements:  `pip install -r requirements.txt`
 - install:    `python setup.py install`

Examples:

    openstack esi offer list

will make a GET request to ESI-Leap and print to screen a list of all the offers in the ESI-Leap database.

    openstack esi offer show <uuid>

will make a GET request and print fields for offer with the given uuid.

    openstack esi offer create --resource-type dummy_node --resource-uuid 1718

will make a POST request to ESI-Leap to create the offer with the given credentials. Prints to the screen the newly created offer with resource type 'dummy_node' and resource uuid '1718'.

    openstack esi offer delete <uuid>
    
will make a DELETE request to ESI-Leap to delete the request with the given uuid. Prints to the screen whether the command was a success or not.
    
    
This repository is currently a work in progress