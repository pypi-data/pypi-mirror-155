import io
import os
from abc import ABC
from typing import Optional, Any, List, Dict, Tuple

from boto3.s3.transfer import TransferConfig
from drb import AbstractNode, DrbNode
from drb.exceptions import DrbException
from drb.path import ParsedPath
from drb_impl_http import DrbHttpNode

from drb_impl_s3 import Auth, Connection
from drb_impl_s3.utility import Requests, Download


class DrbS3Node(AbstractNode, ABC):
    """
    Common DrbS3Node interface
    """

    def __init__(self, auth: Auth):
        super(DrbS3Node, self).__init__()
        self._auth = auth
        self._conn = None

    def close(self) -> None:
        """
        Close The s3 connection
        """
        if self._conn is not None:
            self._conn.close()

    def get_auth(self) -> Auth:
        """
        Return the Auth object created to access the service.
        """
        return self._auth

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    def __eq__(self, other):
        return isinstance(other, DrbS3Node) and \
               self._auth == other._auth

    def __hash__(self):
        return hash(self.auth)


class DrbS3Object(DrbS3Node):
    def __init__(self, obj, parent: DrbS3Node):
        super().__init__(auth=parent.get_auth())
        self.req = Requests(parent.get_auth())
        self._obj = obj
        self._name = obj.key
        self._path = os.path.join(parent.path.original_path, self._name)
        self._attributes = obj.get_available_subresources()
        self._children = None
        self._parent = parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None:
            if name in self.attributes:
                return self._obj.name
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_impl(self, impl: type) -> bool:
        return issubclass(io.BytesIO, impl)

    def get_impl(self, impl: type, **kwargs) -> Any:
        """
        These class allow the download of object in a bucket.

        Parameters:
            impl (type): The type supported by this implementation,
                         here only subclass of io.BytesIO are supported.
            temp_url (Boolean): If using temp url set a secret key to download.
        """
        if self.has_impl(impl):
            if kwargs.get('temp_url', False):
                tmp_url = self.req.get_temp_url(self.parent.name, self.name)
                return DrbHttpNode(tmp_url).get_impl(impl)
            else:
                return Download(self.req.get_obj(
                    self.parent.name,
                    self.name), kwargs.get('chunk_size', 4*1048576))
        raise DrbException(
            f"SwiftService doesn't support {impl} implementation")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False


class DrbS3Bucket(DrbS3Node):

    def __init__(self, obj, parent: DrbS3Node):
        super().__init__(auth=parent.get_auth())
        self.req = Requests(parent.get_auth())
        self._bucket = obj
        self._name = obj.name
        self._path = os.path.join(parent.path.path, self._name)
        self._attributes = obj.get_available_subresources()
        self._children = None
        self._parent = parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None:
            if name in self.attributes:
                return self._bucket.name
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        self._conn = Connection(self._auth)
        if self._children is None:
            objects = self.req.list_objects(self.name)
            self._children = [
                DrbS3Object(obj, self)
                for obj in objects
            ]
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(
            f"SwiftService doesn't support {impl} implementation")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name in [x.name for x in self.children]
            return len(self.children) > 0
        return False


class DrbS3Service(DrbS3Node):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)
        self.req = Requests(auth)
        self._attributes = {}
        self._children = None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(os.path.sep)

    @property
    def children(self) -> List[DrbNode]:
        self._conn = Connection(self._auth)
        if self._children is None:
            buckets = self.req.list_buckets()
            self._children = [
                DrbS3Bucket(bucket, self)
                for bucket in buckets
            ]
        return self._children

    @property
    def name(self) -> str:
        return self._auth.service_name

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(
            f"SwiftService doesn't support {impl} implementation")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name in [x.name for x in self.children]
            return len(self.children) > 0
        return False
