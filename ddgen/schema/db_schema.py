from ddgen.schema.table import TableSchema
from ddgen.schema.column import Column
from ddgen.schema.relationship import Relationship
from typing import List, Iterator, Set
from collections import defaultdict
from ddgen.graph import construct_graph, sorted_in_degree


class DBSchema:

    def __init__(
        self,
        schema_name: str,
        tables: List[TableSchema] = [],
        relationships: List[Relationship] = [],
    ) -> None:
        self.schema_name = schema_name
        self.tables = tables
        self.relationships = relationships
        self.graph_dict = defaultdict(list)
        for relation in relationships:
            self.graph_dict[relation.from_column].append(relation.to_column)

        self.to_from_cols = {
            relation.to_column: relation.from_column for relation in relationships
        }
        self.relation_map = {
            (relation.to_column, relation.from_column): relation.relationship_type
            for relation in relationships
        }

    def __iter__(self) -> Iterator[TableSchema]:
        return iter(self.tables)

    def get_table_dependencies(self):
        graph = construct_graph(self.graph_dict)
        return sorted_in_degree(graph)
