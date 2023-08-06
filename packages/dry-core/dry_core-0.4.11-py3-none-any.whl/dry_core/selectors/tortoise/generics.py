from typing import Generic, TypeVar, Type, Optional

import tortoise
from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model, QuerySetSingle, QuerySet

from dry_core.selectors.generics import BaseSelector

BaseModel = TypeVar("BaseModel", bound=Model)
PydanticBaseModel = TypeVar("PydanticBaseModel", bound=PydanticModel)


class TortoiseSelector(BaseSelector[BaseModel], Generic[BaseModel, PydanticBaseModel]):
    model: Type[BaseModel]
    pydantic_model: Type[PydanticBaseModel]
    id_field = "id"

    @classmethod
    async def get(cls, *args, **kwargs) -> Optional[BaseModel]:
        query_set = cls.get_as_qs(*args, **kwargs)
        if query_set is None:
            return None
        try:
            return await query_set
        except tortoise.exceptions.DoesNotExist:
            return None

    @classmethod
    def get_as_qs(cls, *args, **kwargs) -> QuerySetSingle[BaseModel]:
        try:
            id_value = args[0]
        except IndexError:
            id_value = kwargs.get(cls.id_field, None)
        if id_value is None:
            raise ValueError(f"id not provided. id must be first arg or kwarg with name '{cls.id_field}'")
        return cls.model.get(**{cls.id_field: id_value})

    @classmethod
    async def get_as_pydantic(cls, *args, **kwargs) -> Optional[PydanticBaseModel]:
        query_set = cls.get_as_qs(*args, **kwargs)
        if query_set is None:
            return None
        try:
            return await cls.convert_to_pydantic_from_query_set_single(query_set)
        except tortoise.exceptions.DoesNotExist:
            return None

    @classmethod
    async def list_get(cls, **kwargs) -> list[BaseModel]:
        return await cls.list_get_as_qs(**kwargs)

    @classmethod
    def list_get_as_qs(cls, **kwargs) -> QuerySet[BaseModel]:
        return cls.model.filter(**kwargs)

    @classmethod
    async def list_get_as_pydantic(cls, **kwargs) -> list[PydanticBaseModel]:
        query_set = cls.list_get_as_qs(**kwargs)
        return await cls.convert_to_pydantic_from_query_set(query_set)

    @classmethod
    async def list_get_all(cls) -> list[BaseModel]:
        return await cls.list_get_all_as_qs()

    @classmethod
    def list_get_all_as_qs(cls) -> QuerySet[BaseModel]:
        return cls.model.all()

    @classmethod
    async def list_get_all_as_pydantic(cls) -> list[PydanticBaseModel]:
        query_set = cls.list_get_all_as_qs()
        return await cls.convert_to_pydantic_from_query_set(query_set)

    # Utils

    @classmethod
    async def convert_to_pydantic_from_query_set(cls, query_set: QuerySet[BaseModel]) -> list[PydanticBaseModel]:
        cls._validate_pydantic_model()
        return await cls.pydantic_model.from_queryset(query_set)

    @classmethod
    async def convert_to_pydantic_from_query_set_single(cls, query_set: QuerySetSingle[BaseModel]) -> PydanticBaseModel:
        cls._validate_pydantic_model()
        return await cls.pydantic_model.from_queryset_single(query_set)

    @classmethod
    def _validate_pydantic_model(cls) -> None:
        if cls.pydantic_model is None:
            raise ValueError("'pydantic_model' field must be set")
