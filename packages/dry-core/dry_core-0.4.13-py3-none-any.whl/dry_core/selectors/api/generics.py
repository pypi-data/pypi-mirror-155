from typing import Optional, Generic, Type, AsyncIterable, Iterable, Union, TypeVar

from httpx import Client as HttpClient, AsyncClient as HttpAsyncClient, URL

from dry_core.exceptions import NotFoundError
from dry_core.selectors.generics import BaseSelector
from .pagination import BasePaginationModel, PaginatedRequest


SelectorInstance = TypeVar("SelectorInstance")
SelectorListItemInstance = TypeVar("SelectorListItemInstance")


class BaseAPIMixin:
    base_url: Optional[Union[str, URL]] = None
    connection_timeout: Optional[float] = 10.0
    headers: dict[str, str] = {}

    @classmethod
    def client(cls) -> HttpClient:
        return HttpClient(
            base_url=cls.base_url,
            headers=cls.headers,
            timeout=cls.connection_timeout,
        )

    @classmethod
    def async_client(cls) -> HttpAsyncClient:
        return HttpAsyncClient(
            base_url=cls.base_url,
            headers=cls.headers,
            timeout=cls.connection_timeout,
        )


class BaseAPISelector(
    BaseAPIMixin, BaseSelector[SelectorInstance], Generic[SelectorInstance, SelectorListItemInstance]
):
    list_item_model: Optional[SelectorListItemInstance] = None
    list_api_endpoint: str
    list_api_endpoint_pagination_model: Optional[Type[BasePaginationModel]] = None
    entity_api_endpoint: str

    # utils
    @classmethod
    def get_list_item_model_class(cls) -> Union[SelectorInstance, SelectorListItemInstance]:
        return cls.list_item_model or cls.model

    # selecting method
    @classmethod
    def get(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[SelectorInstance]:
        with cls.client() as client:
            endpoint = cls.entity_api_endpoint.format(**kwargs)
            response = client.get(endpoint, params=query_params)
            if response.status_code != 200:
                if raise_exception:
                    raise NotFoundError(
                        f"Error when trying get object (HTTP status code: {response.status_code}, response: {response.text}). "
                        f"Url: {endpoint}, {query_params=}, {kwargs=}"
                    )
                else:
                    return None
            return cls.model(**response.json())

    @classmethod
    async def aget(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[SelectorInstance]:
        async with cls.async_client() as client:
            endpoint = cls.entity_api_endpoint.format(**kwargs)
            response = await client.get(endpoint, params=query_params)
            if response.status_code != 200:
                if raise_exception:
                    raise NotFoundError(f"Error when trying get object. Url: {endpoint}, {query_params=}, {kwargs=}")
                else:
                    return None
            return cls.model(**response.json())

    @classmethod
    def list_get_all_g(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Iterable[SelectorInstance]:
        with cls.client() as client:
            endpoint = cls.list_api_endpoint.format(**kwargs)
            if cls.list_api_endpoint_pagination_model is None:
                response = client.get(endpoint, params=query_params)
                yield [cls.get_list_item_model_class()(**model_data) for model_data in response.json()]
            else:
                paginated_request = cls.list_api_endpoint_pagination_model.get_first_page_request_params(
                    PaginatedRequest(url=endpoint, query_params=query_params)
                )
                response = client.get(paginated_request.url, params=paginated_request.query_params)
                page = cls.list_api_endpoint_pagination_model(**response.json())
                yield page.get_page_results(model_class=cls.get_list_item_model_class())
                while page.have_next_page:
                    paginated_request = page.get_next_page_request_params(
                        request=PaginatedRequest(url=cls.list_api_endpoint, query_params=query_params)
                    )
                    if paginated_request is None:
                        return
                    response = client.get(paginated_request.url, params=paginated_request.query_params)
                    page = cls.list_api_endpoint_pagination_model(**response.json())
                    yield page.get_page_results(model_class=cls.get_list_item_model_class())

    @classmethod
    def list_get_all(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[list[SelectorInstance]]:
        results = []
        for part in cls.list_get_all_g(query_params=query_params, raise_exception=raise_exception, **kwargs):
            results += part
        return results

    @classmethod
    async def alist_get_all_g(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> AsyncIterable[list[SelectorInstance]]:
        async with cls.async_client() as client:
            endpoint = cls.list_api_endpoint.format(**kwargs)
            if cls.list_api_endpoint_pagination_model is None:
                response = await client.get(endpoint, params=query_params)
                yield [cls.get_list_item_model_class()(**model_data) for model_data in response.json()]
            else:
                paginated_request = cls.list_api_endpoint_pagination_model.get_first_page_request_params(
                    request=PaginatedRequest(url=endpoint, query_params=query_params)
                )
                response = await client.get(paginated_request.url, params=paginated_request.query_params)
                page = cls.list_api_endpoint_pagination_model(**response.json())
                yield page.get_page_results(model_class=cls.get_list_item_model_class())
                while page.have_next_page:
                    paginated_request = page.get_next_page_request_params(
                        request=PaginatedRequest(url=cls.list_api_endpoint, query_params=query_params),
                    )
                    if paginated_request is None:
                        return
                    response = await client.get(paginated_request.url, params=paginated_request.query_params)
                    page = cls.list_api_endpoint_pagination_model(**response.json())
                    yield page.get_page_results(model_class=cls.get_list_item_model_class())

    @classmethod
    async def alist_get_all(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[list[SelectorInstance]]:
        results = []
        async for part in cls.alist_get_all_g(query_params=query_params, raise_exception=raise_exception, **kwargs):
            results += part
        return results
