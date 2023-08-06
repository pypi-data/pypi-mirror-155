import json
import esileapclient.tests.functional.utils.output_utils as utils


def offer_create(client, node_uuid, parse=True, fail_ok=False, **kwargs):
    valid_flags = ('resource_type', 'start_time', 'end_time',
                   'lessee', 'name', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer create', flags, node_uuid, fail_ok)
    return json.loads(output) if parse else output


def offer_delete(client, offer_uuid, fail_ok=False):
    return client.esi('offer delete', '', offer_uuid, fail_ok)


def offer_list(client, parse=True, fail_ok=False, **kwargs):
    valid_flags = ('long', 'status', 'project', 'resource_uuid',
                   'resource_type', 'time_range', 'availability_range')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer list', flags, '', fail_ok)
    return json.loads(output) if parse else output


def offer_show(client, offer_uuid, parse=True, fail_ok=False, **kwargs):
    flags = '-f json' if parse else ''
    output = client.esi('offer show', flags, offer_uuid, fail_ok)
    return json.loads(output) if parse else output


def offer_claim(client, offer_uuid, parse=True, fail_ok=False, **kwargs):
    valid_flags = ('start_time', 'end_time', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('offer claim', flags, offer_uuid, fail_ok)
    return json.loads(output) if parse else output


def lease_create(client, node_uuid, lessee, parse=True,
                 fail_ok=False, **kwargs):
    valid_flags = ('resource_type', 'start_time', 'end_time',
                   'name', 'properties')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('lease create', flags, '%s %s' %
                        (node_uuid, lessee), fail_ok)
    return json.loads(output) if parse else output


def lease_list(client, parse=True, fail_ok=False, **kwargs):
    valid_flags = ('long', 'all', 'status', 'offer_uuid', 'time_range',
                   'project', 'owner', 'resource_type', 'resource_uuid')
    flags = utils.kwargs_to_flags(valid_flags, kwargs)
    flags += ' -f json' if parse else ''

    output = client.esi('lease list', flags, '', fail_ok)
    return json.loads(output) if parse else output


def lease_delete(client, lease_uuid, fail_ok=False):
    return client.esi('lease delete', '', lease_uuid, fail_ok)


def lease_show(client, lease_uuid, parse=True, fail_ok=False):
    flags = '-f json' if parse else ''
    output = client.esi('lease show', flags, lease_uuid, fail_ok)
    return json.loads(output) if parse else output
