from typing import Optional, Iterable, List, Callable

from dnastack.client.constants import DATA_SERVICE_CLIENT_CLASSES, SERVICE_CLIENT_CLASS
from dnastack.client.models import ServiceEndpoint


class UnsupportedServiceTypeError(RuntimeError):
    """ Raised when the given client class is not supported """

    def __init__(self, endpoint: ServiceEndpoint):
        super().__init__(f'{endpoint.id}: {endpoint.type.group}:{endpoint.type.artifact}:{endpoint.type.version} '
                         'is not supported')


def create(endpoint: ServiceEndpoint) -> SERVICE_CLIENT_CLASS:
    for cls in DATA_SERVICE_CLIENT_CLASSES:
        if endpoint.type in cls.get_supported_service_types():
            return cls.make(endpoint)
    raise UnsupportedServiceTypeError(endpoint)


class EndpointRepository:
    def __init__(self,
                 endpoints: Iterable[ServiceEndpoint],
                 cacheable=True):
        self.__cacheable = cacheable
        self.__endpoints = self.__set_endpoints(endpoints)

    def all(self) -> List[ServiceEndpoint]:
        return self.__endpoints

    def get(self, id: str) -> Optional[SERVICE_CLIENT_CLASS]:
        for endpoint in self.__endpoints:
            if endpoint.id == id:
                return create(endpoint)
        return None

    def __set_endpoints(self, endpoints: Iterable[ServiceEndpoint]):
        return (
            [e for e in endpoints]
            if (self.__cacheable and not isinstance(endpoints, list))
            else endpoints
        )
