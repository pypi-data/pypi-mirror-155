#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Base utilities to build API operation managers and objects on top of.
"""

import logging
import abc
import six
import json

from osc_lib import exceptions


LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Manager(object):
    """Provides  CRUD operations with a particular API."""

    @property
    @abc.abstractmethod
    def resource_class(self):
        """The resource class
        """

    @property
    @abc.abstractmethod
    def _resource_name(self):
        """The resource name.
        """

    def __init__(self, api):
        self.api = api

    def _path(self, resource_id=None):
        """Returns a request path for a given resource identifier.
        :param resource_id: Identifier of the resource to generate the request
                            path.
        """

        return ('/v1/%s/%s' % (self._resource_name, resource_id)
                if resource_id else '/v1/%s' % self._resource_name)

    @staticmethod
    def _url_variables(variables):
        """Returns a url with variables set"""

        url_variables = '?'
        for k, v in variables.items():
            if v is not None:
                url_variables += k + '=' + v + '&'
        return url_variables[:-1]

    def _create(self, os_esileap_api_version=None, **kwargs):
        """Create a resource based on a kwargs dictionary of attributes.
        :param kwargs: A dictionary containing the attributes of the resource
                       that will be created.
        """

        new = {}
        invalid = []
        for (key, value) in kwargs.items():
            if key in self.resource_class._creation_attributes:
                new[key] = value
            else:
                invalid.append(key)
        if invalid:
            raise Exception('The attribute(s) "%(attrs)s" '
                            'are invalid; they are not '
                            'needed to create %(resource)s.' %
                            {'resource': self._resource_name,
                             'attrs': '","'.join(invalid)})

        headers = {}
        if os_esileap_api_version is not None:
            headers['headers'] = {'X-OpenStack-ESI-Leap-API-Version':
                                  os_esileap_api_version}

        url = self._path()
        resp, body = self.api.json_request('POST', url, body=new, **headers)

        if resp.status_code == 201:
            return self.resource_class(self, body)
        else:
            raise exceptions.CommandError(json.loads(resp.text)['faultstring'])

    def _list(self, url, obj_class=None, os_esileap_api_version=None):
        if obj_class is None:
            obj_class = self.resource_class

        kwargs = {}

        if os_esileap_api_version is not None:
            kwargs['headers'] = {'X-OpenStack-ESI-Leap-API-Version':
                                 os_esileap_api_version}

        resp, body = self.api.json_request('GET', url, **kwargs)

        if resp.status_code == 200:
            body = body[self._resource_name]

            return [obj_class(self, res) for res in body if res]
        else:
            raise exceptions.CommandError(json.loads(resp.text)['faultstring'])

    def _get(self, resource_id, obj_class=None, os_esileap_api_version=None):
        """Retrieve a resource.
        :param os_esileap_api_version: String version (e.g. "1.35") to use for
            the request.  If not specified, the client's default is used.
        """

        url = self._path(resource_id)

        if obj_class is None:
            obj_class = self.resource_class

        kwargs = {}

        if os_esileap_api_version is not None:
            kwargs['headers'] = {'X-OpenStack-ESI-Leap-API-Version':
                                 os_esileap_api_version}

        resp, body = self.api.json_request('GET', url, **kwargs)

        if resp.status_code == 200:
            return obj_class(self, body)

        else:
            raise exceptions.CommandError(json.loads(resp.text)['faultstring'])

    def _delete(self, resource_id, os_esileap_api_version=None):
        """Delete a resource.
        :param os_esileap_api_version: String version (e.g. "1.35") to use for
            the request.  If not specified, the client's default is used.
        """

        url = self._path(resource_id)

        kwargs = {}

        if os_esileap_api_version is not None:
            kwargs['headers'] = {'X-OpenStack-ESI-Leap-API-Version':
                                 os_esileap_api_version}

        resp, _ = self.api.json_request('DELETE', url, **kwargs)

        if resp.status_code != 200:
            raise exceptions.CommandError(json.loads(resp.text)['faultstring'])


@six.add_metaclass(abc.ABCMeta)
class Resource(object):
    """Base class for OpenStack resources (tenant, user, etc.).
    This is pretty much just a bag for attributes.
    """

    @property
    @abc.abstractmethod
    def fields(self):
        """A dictionary of attributes we expect a resource to have, mapping
        to a label for display purposes"""

    @property
    @abc.abstractmethod
    def detailed_fields(self):
        """A dictionary of all attributes to be displayed in a
        detailed request"""

    @property
    @abc.abstractmethod
    def _creation_attributes(self):
        """A list of required creation attributes for a resource type.
        """

    def __init__(self, manager, info):
        """Populate and bind to a manager.
        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        """

        self.manager = manager
        self._info = {k: v for (k, v) in info.items() if k
                      in self.detailed_fields.keys()}
        self._add_details(self._info)

    def _add_details(self, info):
        for (k, v) in info.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass
