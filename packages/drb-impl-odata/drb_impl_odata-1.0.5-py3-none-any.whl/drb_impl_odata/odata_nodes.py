from __future__ import annotations

import io
from drb import DrbNode
from drb.path import ParsedPath
from drb.exceptions import DrbException

from typing import Any, Dict, List, Optional, Tuple, Union

from .odata_node import OdataNode
from .odata_utils import ODataUtils, OdataServiceType
from .exceptions import OdataRequestException


class ODataProductNode(OdataNode):
    def __init__(self, source: Union[str, OdataNode],
                 product_uuid: str = None,
                 data: Dict = None,
                 **kwargs):
        self._type = OdataServiceType.UNKNOWN

        if isinstance(source, OdataNode):
            super(ODataProductNode, self).__init__(source.get_service_url(),
                                                   source.get_auth())
            self._type = source.type_service
            self.__parent = source
            self.__uuid = product_uuid
        elif isinstance(data, Dict):
            self.__parent = None
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super(ODataProductNode, self).__init__(
                source.split('/Products')[0],
                auth
            )
            self._type = ODataUtils.get_type_odata_svc(
                source.split('/Products')[0], auth)
            self.__uuid = data.get('id') if \
                self._type == OdataServiceType.ONDA_DIAS.value \
                else data.get('Id')
        else:
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super(ODataProductNode, self).__init__(
                source.split('/Products')[0],
                auth
            )
            self.__parent = None
            self.__uuid = product_uuid

        self.__path = ParsedPath(
            f'{self.get_service_url()}/Products({self.__uuid})')
        self.__product = data
        self.__attr = None

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    def __load_product(self):
        if self.__product is None:
            self.__product = ODataUtils.req_product_by_uuid(self, self.__uuid)

    @property
    def name(self) -> str:
        self.__load_product()
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__product['name']
        else:
            return self.__product['Name']

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        self.__load_product()
        return {(k, None): v for k, v in self.__product.items()}

    @property
    def children(self) -> List[DrbNode]:
        return [ODataProductAttributeNode(self, self.__uuid)]

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        self.__load_product()
        if namespace_uri is None:
            try:
                return self.__product[name]
            except KeyError:
                pass
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name == self.children[0].name
            return True
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        if self.type_service == OdataServiceType.ONDA_DIAS:
            online = not self.get_attribute('offline')
        else:
            online = self.get_attribute('Online')
        return online and (impl == io.BufferedIOBase or impl == io.BytesIO)

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            return ODataUtils.req_product_download(self, self.__uuid,
                                                   kwargs.get('start', None),
                                                   kwargs.get('end', None))
        raise DrbException(f'Not supported implementation: {impl}')

    def __eq__(self, other):
        if isinstance(other, ODataProductNode):
            return super().__eq__(other) and other.__uuid == self.__uuid
        return False

    def __hash__(self):
        return hash(self._service_url)


class ODataProductAttributeNode(OdataNode):
    __name = 'Attributes'

    def __init__(self, source: ODataProductNode, prd_uuid: str):
        super().__init__(source.get_service_url(), source.get_auth())
        self.__uuid = prd_uuid
        self.__parent = source
        self.__attr = None
        self._type = source.type_service

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    def __load_attributes(self) -> None:
        if self.__attr is None:
            self.__attr = ODataUtils.req_product_attributes(self, self.__uuid)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__parent.path / self.__name

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def children(self) -> List[DrbNode]:
        self.__load_attributes()
        return [ODataAttributeNode(self, data=x) for x in self.__attr]

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                for x in self.__attr:
                    if name in x.keys():
                        return True
                return False
            return len(self.__attr) > 0
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f'Do not support implementation: {impl}')


class ODataAttributeNode(OdataNode):
    def __init__(self, source: Union[str, ODataProductAttributeNode],
                 **kwargs):
        if isinstance(source, ODataProductAttributeNode):
            super().__init__(source.get_service_url(), source.get_auth())
            self.__parent = source
            self._type = source.type_service
        elif isinstance(source, str):
            auth = kwargs['auth'] if 'auth' in kwargs.keys() else None
            super().__init__(source, auth)
            self.__parent = None
            self._type = OdataServiceType.UNKNOWN
        else:
            raise OdataRequestException(f'Unsupported source: {type(source)}')
        self.__path = None
        self.__data = kwargs['data'] if 'data' in kwargs.keys() else None

    @property
    def type_service(self) -> OdataServiceType:
        return self._type

    @property
    def name(self) -> str:
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__data['name']
        else:
            return self.__data['Name']

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        if self._type == OdataServiceType.ONDA_DIAS:
            return self.__data['value']
        else:
            return self.__data['Value']

    @property
    def path(self) -> ParsedPath:
        if self.__path is None:
            if self.__parent is None:
                self.__path = ParsedPath(self.name)
            else:
                self.__path = self.__parent.path / self.name
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.__parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {(k, None): v for k, v in self.__data.items()}

    @property
    def children(self) -> List[DrbNode]:
        return []

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None and name in self.__data.keys():
            return self.__data[name]
        raise DrbException(f'Attribute not found: ({name}, {namespace_uri})')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f'Do not support implementation: {impl}')
