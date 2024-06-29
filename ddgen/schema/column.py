
from ddgen.engines.base import Engine
from ddgen.engines.default import DataType
from ddgen.helper_functions import generate_uuid_as_str

class Column:
    def __init__(
        self,
        name,
        col_type: DataType,
        engine: Engine = None,
        is_primary=False,
        is_nullable=False,
        percentage=5
    ):
        self.id = generate_uuid_as_str()
        self.name = name
        self.col_type = col_type
        self.engine = engine
        self.is_primary = is_primary
        self.is_nullable = is_nullable
        self.percentage = percentage
        self.data = None
        self.table = None

    def __repr__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        if isinstance(other, Column):
            return self.id == other.id 
        return False
    
