from __future__ import annotations

import uuid
import datetime
from abc import ABC, abstractmethod

from drb import DrbNode
from drb.path import ParsedPath
from drb.predicat import Predicate
from drb.exceptions import DrbException

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from requests.auth import AuthBase

from . import ODataProductNode
from .odata_node import OdataNode
from .odata_utils import ODataUtils, OdataServiceType, ODataQueryPredicate


class ODataServiceNode(OdataNode, ABC):
    def __init__(self, url: str, auth: AuthBase = None):
        super(ODataServiceNode, self).__init__(url, auth)
        self.__path = ParsedPath(url)
        self._type = None

    @property
    def type_service(self) -> OdataServiceType:
        if self._type is None:
            self._type = ODataUtils.get_type_odata_svc(self._service_url,
                                                       self.get_auth())
        return self._type

    @property
    def name(self) -> str:
        return self._service_url

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> ParsedPath:
        return self.__path

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def children(self) -> List[DrbNode]:
        return ODataFilteredList(self)

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException('ODataNode has no attribute')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                try:
                    self._get_named_child(name=name)
                except DrbException:
                    return False
                return True
            return ODataUtils.req_svc_count(self) > 0
        return False

    def close(self) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(f"ODataNot doesn't support {impl} implementation")

    @abstractmethod
    def prepare_filter(self, user_filter: str, default: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0) \
            -> Union[DrbNode, List[DrbNode]]:
        raise NotImplementedError

    def __retrieve_child_from_tuple(self, t: tuple) -> \
            Union[List[DrbNode], DrbNode]:
        if len(t) == 2:
            # (name, namespace)
            if t[1] is None or isinstance(t[1], str):
                return self._get_named_child(name=t[0], namespace_uri=t[1])
            # (name, occurrence)
            elif isinstance(t[1], int) or isinstance(t[1], slice):
                return self._get_named_child(t[0], occurrence=t[1])
        # (name, namespace, occurrence)
        elif len(t) == 3:
            return self._get_named_child(*t)
        raise KeyError(f'Invalid key: {t}')

    @abstractmethod
    def retrieve_default_criteria(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_product(self, data: dict) -> ODataProductNode:
        raise NotImplementedError

    def __retrieve_child(self, key: Union[uuid.UUID, tuple, Predicate]) -> \
            Union[List[DrbNode], DrbNode]:
        try:
            if isinstance(key, uuid.UUID):
                prd_uuid = str(key)
                data = ODataUtils.req_product_by_uuid(self, prd_uuid)
                return ODataProductNode(self, str(prd_uuid), data=data)
            if isinstance(key, tuple):
                return self.__retrieve_child_from_tuple(key)
            if isinstance(key, str):
                return self._get_named_child(key)
            if isinstance(key, ODataQueryPredicate):
                return ODataFilteredList(self, qfilter=key.filter,
                                         qorder=key.order)
        except DrbException as ex:
            raise KeyError from ex
        raise TypeError('Invalid type for a DrbNode bracket: '
                        f'{key.__class__}')

    def __len__(self):
        return ODataUtils.req_svc_count(self)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.children[item]
        return self.__retrieve_child(item)


class ODataServiceNodeCSC(ODataServiceNode):

    @property
    def type_service(self) -> OdataServiceType:
        self._type = OdataServiceType.CSC
        return self._type

    def prepare_filter(self, user_filter: str, default: str) -> str:
        date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        if user_filter is None:
            return f'{default} lt {date}'
        if default in user_filter:
            return user_filter
        return f"({user_filter}) and {default} lt {date}"

    def retrieve_default_criteria(self) -> str:
        return 'PublicationDate'

    @property
    def namespace_uri(self) -> Optional[str]:
        return 'OData.CSC'

    def _get_named_child(self, name: str,
                         namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0
                         ) -> Union[DrbNode, List[DrbNode]]:
        if namespace_uri is None:
            products = ODataUtils.req_svc_products(
                self, filter=f"Name eq '{name}'")
            if len(products) <= 0:
                raise DrbException(f'No child ({name}, {namespace_uri},'
                                   f' {occurrence}) found')
            p = products[occurrence]
            if isinstance(p, list):
                return [ODataProductNode(self,
                                         x['Id'], data=x) for x in p]
            return ODataProductNode(self, p['Id'], data=p)
        raise DrbException(f'No child ({name}, {namespace_uri}, {occurrence}) '
                           'found')

    def generate_product(self, data: dict) -> ODataProductNode:
        return ODataProductNode(self, data['Id'], data=data)


class ODataServiceNodeDhus(ODataServiceNode):

    @property
    def type_service(self) -> OdataServiceType:
        self._type = OdataServiceType.DHUS
        return self._type

    def prepare_filter(self, user_filter: str, default: str) -> str:
        date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.0Z')
        if user_filter is None:
            return f'{default} lt {date}'
        if default in user_filter:
            return user_filter
        return f"({user_filter}) and {default} lt {date}"

    @property
    def children(self) -> List[DrbNode]:
        return ODataFilteredList(self, page_size=10)

    def retrieve_default_criteria(self) -> str:
        return 'CreationDate'

    @property
    def namespace_uri(self) -> Optional[str]:
        return 'OData.DHuS'

    def _get_named_child(self, name: str,
                         namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0
                         ) -> Union[DrbNode, List[DrbNode]]:
        if namespace_uri is None:
            products = ODataUtils.req_svc_products(
                self, filter=f"Name eq '{name}'")
            if len(products) <= 0:
                raise DrbException(f'No child ({name}, {namespace_uri},'
                                   f' {occurrence}) found')
            p = products[occurrence]
            if isinstance(p, list):
                return [ODataProductNode(self,
                                         x['Id'], data=x) for x in p]
            return ODataProductNode(self, p['Id'], data=p)
        raise DrbException(f'No child ({name}, {namespace_uri}, {occurrence}) '
                           'found')

    def generate_product(self, data: dict) -> ODataProductNode:
        return ODataProductNode(self, data['Id'], data=data)


class ODataServiceNodeDias(ODataServiceNode):

    @property
    def type_service(self) -> OdataServiceType:
        self._type = OdataServiceType.ONDA_DIAS
        return self._type

    def prepare_filter(self, user_filter: str, default: str) -> str:
        if user_filter is None:
            return f"%22creationDate:[1900-05-10T00:00:00.000Z TO NOW]%22"
        if default in user_filter:
            return user_filter
        return f"%22({user_filter}) and creationDate:" \
               f"[1900-05-10T00:00:00.000Z TO NOW]%22"

    def retrieve_default_criteria(self) -> str:
        return 'creationDate'

    @property
    def namespace_uri(self) -> Optional[str]:
        return 'Ens'

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: Union[int, slice] = 0
                         ) -> Union[DrbNode, List[DrbNode]]:
        if namespace_uri is None:
            products = ODataUtils.req_svc_products(
                self, search=f'"name:{name}"')
            if len(products) <= 0:
                raise DrbException(f'No child ({name}, {namespace_uri},'
                                   f' {occurrence}) found')
            p = products[occurrence]
            if isinstance(p, list):
                return [ODataProductNode(self,
                                         x['id'], data=x) for x in p]
            return ODataProductNode(self, p['id'], data=p)
        raise DrbException(f'No child ({name}, {namespace_uri}, {occurrence}) '
                           'found')

    def generate_product(self, data: dict) -> ODataProductNode:
        return ODataProductNode(self, data['id'], data=data)


class ODataFilteredList(list):

    def __init__(self, odata: OdataNode, qfilter: str = None,
                 qorder: str = None, page_size=100):
        super().__init__()
        self._count = -1
        self._page = None
        self._skip = 0
        self._page_size = page_size
        self._odata = odata
        default = odata.retrieve_default_criteria()
        self._filter = odata.prepare_filter(qfilter, default)
        self._order = self.__prepare_order(qorder, default)

    @classmethod
    def __prepare_order(cls, user_order: str, default: str) -> str:
        if user_order is None:
            return f'{default} desc'
        return user_order

    def __perform_query(self):
        count = False

        buffer, self._count = ODataUtils.req_svc_products(
            self._odata, count=self._count == -1, filter=self._filter,
            order=self._order, skip=self._skip, top=self._page_size)

        if self._count == -1 and not ODataUtils.is_count_accepted_in_request(
                self._odata):
            self._count = ODataUtils.req_svc_count_search(self._odata,
                                                          self._filter)

        self._page = [self._odata.generate_product(e) for e in buffer]

    def __compute_index(self, item: Union[int, slice]) -> Tuple[int, int]:
        if isinstance(item, int):
            if item < 0:
                return item + len(self), -1
            return item, -1
        # item is a slice
        start = item.start if item.start is not None else 0
        if start < 0:
            start = start + len(self)
        stop = item.stop if item.stop is not None else len(self)
        if stop < 0:
            stop = stop + len(self)
        return start, stop

    def append(self, obj: Any) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def copy(self) -> List[ODataProductNode]:
        raise NotImplementedError

    def count(self, value: Any) -> int:
        raise NotImplementedError

    def extend(self, iterable: Iterable[ODataProductNode]) -> None:
        raise NotImplementedError

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        raise NotImplementedError

    def insert(self, index: int, obj: ODataProductNode) -> None:
        raise NotImplementedError

    def pop(self, index: int = ...) -> ODataProductNode:
        raise NotImplementedError

    def remove(self, value: Any) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def sort(self: List, *, key: None = ..., reverse: bool = ...) -> None:
        raise NotImplementedError

    def __getitem_index(self, index):
        if index not in range(self._skip, self._skip + self._page_size):
            page_number = index // self._page_size
            self._skip = page_number * self._page_size
            self.__perform_query()
        return self._page[index % self._page_size]

    def __getitem__(self, item):
        if self._count == -1:
            self.__perform_query()

        if isinstance(item, int):
            index, _ = self.__compute_index(item)
            return self.__getitem_index(index)
        elif isinstance(item, slice):
            start, stop = self.__compute_index(item)
            result = []
            for index in range(start, stop):
                node = self.__getitem_index(index)
                result.append(node)
            return result
        else:
            raise KeyError(f'Invalid key: {type(item)}')

    def __iter__(self):
        def generator(qfilter, qorder, count, page_size):
            page_num = 0
            buffer = None
            for i in range(count):
                if i % page_size == 0:
                    skip = page_size * page_num
                    buffer = ODataUtils.req_svc_products(
                        self._odata, filter=qfilter, order=qorder, skip=skip,
                        top=page_size)
                    page_num += 1
                idx = i % page_size
                yield self._odata.generate_product(buffer[idx])

        return generator(self._filter, self._order, len(self), self._page_size)

    def __len__(self):
        if self._count == -1:
            self.__perform_query()
        return self._count

    def __contains__(self, item):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __imul__(self, other):
        raise NotImplementedError


class ProductList(list):
    """
    Specific read only list to access to OData CSC Product entities:
     * Any access generate a remote access to the associated OData service
     * Any inherited functions allowing to modify the list have no effect.
     * comparator functions are not supported except the equal comparator.
    """

    def __init__(self, odata: ODataServiceNode):
        super().__init__()
        self.__odata = odata
        if self.__odata.type_service == OdataServiceType.ONDA_DIAS:
            self.__id_identifier = 'id'
        else:
            self.__id_identifier = 'Id'

    def __getitem__(self, item):
        count = ODataUtils.req_svc_count(self.__odata)
        if isinstance(item, int):
            if -count < item >= count:
                raise IndexError
            if item >= 0:
                skip = item
            else:
                skip = item + count
            products = ODataUtils.req_svc_products(self.__odata, skip=skip,
                                                   top=1)
            prd = products[0]
            prd_uuid = products[0][self.__id_identifier]
            return ODataProductNode(self.__odata, prd_uuid, data=prd)
        if isinstance(item, slice):
            products = ODataUtils.req_svc_products(
                self.__odata, skip=item.start, top=item.stop)
            return [ODataProductNode(self.__odata, p[self.__id_identifier],
                                     data=p)
                    for p in products]
        raise TypeError

    def __iter__(self):
        def iterator():
            for index in range(0, len(self)):
                p = ODataUtils.req_svc_products(self.__odata, skip=index,
                                                top=1)
                yield ODataProductNode(self.__odata,
                                       p[0][self.__id_identifier], data=p[0])

        return iterator()

    def __len__(self):
        return ODataUtils.req_svc_count(self.__odata)

    def __sizeof__(self):
        super().__sizeof__()

    def append(self, obj: Any) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def copy(self) -> List[ODataProductNode]:
        raise NotImplementedError

    def count(self, value: Any) -> int:
        raise NotImplementedError

    def extend(self, iterable: Iterable[ODataProductNode]) -> None:
        raise NotImplementedError

    def index(self, value: Any, start: int = ..., stop: int = ...) -> int:
        raise NotImplementedError

    def insert(self, index: int, obj: ODataProductNode) -> None:
        raise NotImplementedError

    def pop(self, index: int = ...) -> ODataProductNode:
        raise NotImplementedError

    def remove(self, value: Any) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def sort(self: List, *, key: None = ..., reverse: bool = ...) -> None:
        raise NotImplementedError
