from ddgen.enums import RelationshipType
from ddgen.schema.column import Column


class Relationship:
    def __init__(self, from_column, to_column, relationship_type: RelationshipType):
        self.from_column: Column = from_column
        self.to_column: Column = to_column
        self.relationship_type = relationship_type

    def __repr__(self):
        return f"Relationship(From={self.from_column}, To={self.to_column}, Type={self.relationship_type})"
