# from djantic import ModelSchema
from pydantic import BaseModel

from ..utils import camelcase, paginate

__all__ = [
    "FlatInput",
    "Input",
    "Output",
    "SearchInput",
    "SearchOutput",
    "Model",
]


class FlatInput(BaseModel):
    pass


class Input(FlatInput):
    class Config:
        alias_generator = camelcase
        # arbitrary_types_allowed = True

    def __contains__(self, attr):
        return attr in self.dict(exclude_unset=True)


class SearchInput(Input):
    page: int | None
    limit: int | None

    async def paginate(self, qs):
        return await paginate(qs, page=self.page, limit=self.limit)


class FlatOutput(BaseModel):
    pass


class Output(FlatOutput):
    class Config:
        alias_generator = camelcase
        orm_mode = True
        # arbitrary_types_allowed = True

    def __contains__(self, attr):
        return attr in self.dict(exclude_unset=True)


class SearchOutput(Input):
    page: int
    count: int
    rows: list
    limit: int | None


# Model = ModelSchema
