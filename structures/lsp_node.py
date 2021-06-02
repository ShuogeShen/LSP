from typing import Type
from lsp_types import NullType

class LSPNode:
    def __init__(
        self, 
        id: int, 
        name: str = NullType.NULL,
        child = None, 
        sibiling = None, 
        returns = None, 
        nodeType: str = NullType.NULL,
        weight: float = 0.0,
        score: float = 0.0,
    ) -> "LSPNode":
        self.id = id
        self.name = name
        self.child = child
        self.sibiling = sibiling
        self.returns = returns
        self.nodeType = nodeType
        self.weight = weight
        self.score = score