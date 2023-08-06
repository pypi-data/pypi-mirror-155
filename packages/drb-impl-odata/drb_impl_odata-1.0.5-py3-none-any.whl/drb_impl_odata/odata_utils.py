import json
import io
from enum import Enum

from requests.auth import AuthBase
from typing import List
from defusedxml import ElementTree
from defusedxml.ElementTree import ParseError
from drb.predicat import Predicate
from drb.exceptions import DrbException
from drb_impl_http import DrbHttpNode

from .odata_node import OdataNode
from .exceptions import OdataRequestException


class OdataServiceType(Enum):
    UNKNOWN = 0
    CSC = 1
    DHUS = 2
    ONDA_DIAS = 3


class ODataUtils:
    @staticmethod
    def get_url_uuid_product(odata: OdataNode, prd_uuid: str):
        if odata.type_service == OdataServiceType.DHUS:
            return f"{odata.get_service_url()}/Products('{prd_uuid}')"
        return f'{odata.get_service_url()}/Products({prd_uuid})'

    @staticmethod
    def get_url_attributes(odata: OdataNode, prd_uuid: str):
        base_url = ODataUtils.get_url_uuid_product(odata, prd_uuid)
        if odata.type_service == OdataServiceType.ONDA_DIAS:
            return base_url + '/Metadata'
        else:
            return base_url + '/Attributes'

    @staticmethod
    def http_node_to_json(node: DrbHttpNode) -> dict:
        try:
            with node.get_impl(io.BytesIO) as stream:
                data = json.load(stream)
                if 'error' in data.keys():
                    raise OdataRequestException(str(data['error']))
                return data
        except json.JSONDecodeError:
            raise OdataRequestException(f'Invalid json from {node.path.name}')
        except DrbException:
            raise OdataRequestException(f'Invalid node: {type(node)}')

    @staticmethod
    def get_type_odata_svc(service_url: str, auth: AuthBase = None) \
            -> OdataServiceType:
        """
        Retrieve with the given URL the OData service type (CSC or DHuS).

        Parameters:
            service_url (str): service URL
            auth (AuthBase): authentication mechanism required by the service
                             (default: ``None``)
        Returns:
            OdataServiceType: value corresponding to service
        """
        try:
            url = f'{service_url}/$metadata'
            node = DrbHttpNode(url, auth=auth)
            tree = ElementTree.parse(node.get_impl(io.BytesIO))
            ns = tree.getroot()[0][0].get('Namespace', None)
            if 'OData.CSC'.lower() == ns.lower():
                return OdataServiceType.CSC
            elif 'OData.DHuS'.lower() == ns.lower():
                return OdataServiceType.DHUS
            elif 'Ens'.lower() == ns.lower():
                return OdataServiceType.ONDA_DIAS
            return OdataServiceType.UNKNOWN
        except (DrbException, ParseError) as ex:
            return OdataServiceType.UNKNOWN

    @staticmethod
    def req_svc(odata: OdataNode) -> dict:
        node = DrbHttpNode(odata.get_service_url(), auth=odata.get_auth(),
                           params={'$format': 'json'})
        data = ODataUtils.http_node_to_json(node)
        return data

    @staticmethod
    def req_svc_count(odata: OdataNode) -> int:
        url = f'{odata.get_service_url()}/Products/$count'
        node = DrbHttpNode(url, auth=odata.get_auth())
        stream = node.get_impl(io.BytesIO)
        value = stream.read().decode()
        stream.close()
        return int(value)

    @staticmethod
    def req_svc_count_search(odata: OdataNode, search: str) -> int:
        url = f'{odata.get_service_url()}/Products/$count?$search={search}'
        node = DrbHttpNode(url, auth=odata.get_auth())
        stream = node.get_impl(io.BytesIO)
        value = stream.read().decode()
        stream.close()
        return int(value)

    @staticmethod
    def req_svc_products(odata: OdataNode, **kwargs) -> list:
        params = {'$format': 'json'}
        ret_count = False

        if 'filter' in kwargs.keys() and kwargs['filter'] is not None:
            params[ODataUtils.get_filter_keyword(odata)] = \
                kwargs['filter'].replace('\'', '%27')
        # For future use if we make search in GSS or Dhus...
        elif 'search' in kwargs.keys() and kwargs['search'] is not None:
            params[ODataUtils.get_search_keyword(odata)] = kwargs['search']
        if 'order' in kwargs.keys() and kwargs['order'] is not None:
            params['$orderby'] = kwargs['order']

        if 'skip' in kwargs.keys() and kwargs['skip'] is not None:
            params['$skip'] = kwargs['skip']

        if 'top' in kwargs.keys() and kwargs['top'] is not None:
            params['$top'] = kwargs['top']

        if 'count' in kwargs.keys() and kwargs['count']:
            ret_count = True
            if ODataUtils.is_count_accepted_in_request(odata):
                params['$count'] = 'true'

        query = '&'.join(map(lambda k: f'{k[0]}={k[1]}', params.items()))
        url = f'{odata.get_service_url()}/Products?{query}'
        node = DrbHttpNode(url, auth=odata.get_auth())
        data = ODataUtils.http_node_to_json(node)
        if ret_count:
            if '@odata.count' in data.keys():
                return data['value'], data['@odata.count']
            else:
                return data['value'], -1
        return data['value']

    @staticmethod
    def req_product_by_uuid(odata: OdataNode, prd_uuid: str) -> dict:
        url = ODataUtils.get_url_uuid_product(odata, prd_uuid)
        params = {'$format': 'json'}
        node = DrbHttpNode(url, auth=odata.get_auth(), params=params)
        return {
            k: v for k, v in ODataUtils.http_node_to_json(node).items()
            if not k.startswith('@odata.')
        }

    @staticmethod
    def req_product_attributes(odata: OdataNode, prd_uuid: str) -> List[dict]:
        url = ODataUtils.get_url_attributes(odata, prd_uuid)
        params = {'$format': 'json'}
        node = DrbHttpNode(url, auth=odata.get_auth(), params=params)
        data = ODataUtils.http_node_to_json(node)
        return data['value']

    @staticmethod
    def req_product_download(odata: OdataNode, prd_uuid: str, start=None,
                             end=None) -> io.BytesIO:
        url = ODataUtils.get_url_uuid_product(odata, prd_uuid) + '/$value'
        node = DrbHttpNode(url, auth=odata.get_auth())
        if start is None or end is None:
            return node.get_impl(io.BytesIO)
        return node.get_impl(io.BytesIO, start=start, end=end)

    @staticmethod
    def get_filter_keyword(odata: OdataNode) -> str:
        if odata.type_service == OdataServiceType.ONDA_DIAS:
            return '$search'
        return '$filter'

    @staticmethod
    def get_search_keyword(odata: OdataNode) -> str:
        if odata.type_service == OdataServiceType.ONDA_DIAS:
            return '$search'
        return '$filter'

    @staticmethod
    def is_count_accepted_in_request(odata: OdataNode) -> bool:
        if odata.type_service == OdataServiceType.ONDA_DIAS:
            return False
        return True


class ODataQueryPredicate(Predicate):
    """
    This predicate allowing to customize an OData query request.
    Customizable OData query elements:
     - filter
     - search
     - orderby

    Keyword Arguments:
        filter (str): the OData filter query element
        search (str): the OData search query element
        order (str): the OData orderby query element
    """

    def __init__(self, **kwargs):
        self.__filter = kwargs['filter'] if 'filter' in kwargs.keys() else None
        self.__search = kwargs['search'] if 'search' in kwargs.keys() else None
        self.__order = kwargs['order'] if 'order' in kwargs.keys() else None

    @property
    def filter(self) -> str:
        return self.__filter

    @property
    def order(self) -> str:
        return self.__order

    @property
    def search(self) -> str:
        return self.__search

    def matches(self, key) -> bool:
        return False
