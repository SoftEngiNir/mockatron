from typing import Optional

from pydantic import BaseModel

from ddgen.enums import RelationshipType


class ForeignKeyModel(BaseModel):
    table: str
    source_col: str
    rtype: Optional[RelationshipType] = RelationshipType.one_to_many


class RelatedColumnModel(BaseModel):
    table: str
    source_col: str
    rtype: str


class EngineModel(BaseModel):
    name: str
    config: Optional[dict] = None


class ColumnModel(BaseModel):
    name: str
    dtype: Optional[str] = None
    engine: Optional[EngineModel] = None
    is_primary: Optional[bool] = False
    is_nullable: Optional[bool] = False
    percentage: Optional[int] = 5
    foreign_key: Optional[ForeignKeyModel] = None
    related_column: Optional[RelatedColumnModel] = None


class TableModel(BaseModel):
    name: str
    columns: list[ColumnModel]


class DatabaseModel(BaseModel):
    tables: list[TableModel]
    schema: Optional[str]
