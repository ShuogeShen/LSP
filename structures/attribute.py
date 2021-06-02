from typing import Type, List, Tuple, Any
from structures.lsp_node import LSPNode
from eac.elementary_attribute_criteria import EAC
from lsp_types import NullType

class Attribute(LSPNode):
    def __init__(
        self, 
        id: int,
        value: float = 0.0,
        units: str = NullType.NULL,
        breakValues: List[Tuple[float, float]] = [],
        eac: EAC = None
    ) -> "Attribute":
        super().__init__(id)
        self.value = value
        self.units = units
        self.breakValues = breakValues
        self.eac = None