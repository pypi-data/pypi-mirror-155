from typing import Any, Optional, Type

from pydantic import BaseModel as PydanticBaseModel


class PaginatedRequest(PydanticBaseModel):
    url: str
    query_params: Optional[dict[str, str]] = None
    body_params: Optional[dict[str, Any]] = None


class BasePaginationModel(PydanticBaseModel):
    request: PaginatedRequest

    @property
    def have_next_page(self) -> bool:
        raise NotImplementedError

    @property
    def have_prev_page(self) -> bool:
        raise NotImplementedError

    @classmethod
    def get_first_page_request_params(cls, request: PaginatedRequest) -> PaginatedRequest:
        raise NotImplementedError

    def get_next_page_request_params(self, request: Optional[PaginatedRequest]) -> Optional[PaginatedRequest]:
        raise NotImplementedError

    def get_prev_page_request_params(self, request: Optional[PaginatedRequest]) -> Optional[PaginatedRequest]:
        raise NotImplementedError

    def get_page_results(self, model_class: Type) -> list[Any]:
        raise NotImplementedError


class LimitOffsetPaginationModel(BasePaginationModel):
    _default_limit: int = 50

    limit: int = _default_limit
    offset: int = 0
    count: int = 0
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[Any] = []

    @property
    def results_count(self) -> int:
        return len(self.results)

    @property
    def have_next_page(self) -> bool:
        return self.next is not None or self.offset + self.limit < self.count

    @property
    def have_prev_page(self) -> bool:
        return self.previous is not None or (self.offset > 0 and self.count > 0)

    @classmethod
    def get_first_page_request_params(cls, request: PaginatedRequest) -> PaginatedRequest:
        query_params = request.query_params or {}
        return PaginatedRequest(
            url=request.url,
            query_params=query_params
            | {
                "limit": query_params.get("limit", None) or cls._default_limit,
                "offset": query_params.get("offset", None) or 0,
            },
        )

    def get_next_page_request_params(self, request: Optional[PaginatedRequest] = None) -> Optional[PaginatedRequest]:
        if not self.have_next_page:
            return
        if self.next is not None:
            return PaginatedRequest(
                url=self.next,
                query_params=request.query_params if request is not None else None,
                body_params=request.body_params if request is not None else None,
            )
        if request is not None:
            query_params = request.query_params
        else:
            new_offset = self.offset + self.limit
            query_params = {
                "limit": self.count - new_offset if (new_offset + self.limit) >= self.count else self.limit,
                "offset": new_offset,
            }
        return PaginatedRequest(
            url=(request or self.request).url,
            query_params=query_params,
            body_params=request.body_params if request is not None else None,
        )

    def get_prev_page_request_params(self, request: Optional[PaginatedRequest] = None) -> Optional[PaginatedRequest]:
        if not self.have_prev_page:
            return
        if self.previous is not None:
            return PaginatedRequest(
                url=self.previous,
                query_params=request.query_params if request is not None else None,
                body_params=request.body_params if request is not None else None,
            )
        if request is not None:
            query_params = request.query_params
        else:
            new_offset = self.offset - self.limit
            query_params = {
                "limit": self.offset if new_offset > 0 else self.limit,
                "offset": new_offset if new_offset > 0 else 0,
            }
        return PaginatedRequest(
            url=(request or self.request).url,
            query_params=query_params,
            body_params=request.body_params if request is not None else None,
        )

    def get_page_results(self, model_class: Optional[Type] = None) -> list[Any]:
        if model_class is None:
            return self.results
        return [
            model_class(**instance_data) if isinstance(instance_data, dict) else model_class(instance_data)
            for instance_data in self.results
        ]
