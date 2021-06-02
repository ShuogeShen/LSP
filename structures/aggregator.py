from typing import Type, Tuple
from structures.lsp_node import LSPNode
from structures.aggregator_group import AggregatorGroup
from lsp_types import NullType, AggregatorType

class Aggregator(LSPNode):
    def __init__(
        self,
        id: int,
        aggregatorType: str = NullType.NULL,
        aggregatorGroup: AggregatorGroup = None,
    ) -> "Aggregator":
        super().__init__(id)
        self.aggregatorType = aggregatorType
        self.aggregatorGroup = aggregatorGroup

class PartialAbsorption(Aggregator):
    def __init__(
        self, 
        id: int,
        penalty: float = 0.0,
        reward: float = 0.0,
        innerWeight1: float = 0.0,
        innerWeight2: float = 0.0,
        optional: int = -1,
    ) -> "PartialAbsorption":
       super().__init__(id)
       self.penalty = penalty
       self.reward = reward
       self.innerWeight1 = innerWeight1
       self.innerWeight2 = innerWeight2
       self.optional = optional

class GCD_Aggregator(Aggregator):
    def __init__(
        self, 
        id: int,
        symbol: Tuple[str, float] = AggregatorType.NULL,
    ) -> "GCD_Aggregator":
        super().__init__(id)
        self.symbol = symbol

class CPA_Aggregator(PartialAbsorption):
    def __init__(
        self, 
        id: int,
        mandatory: int = -1,
    ) -> "CPA_Aggregator":
        super().__init__(id)
        self.mandatory = mandatory

class DPA_Aggregator(PartialAbsorption):
    def __init__(
        self, 
        id: int,
        sufficient: int = -1,
    ) -> "DPA_Aggregator":
        super().__init__(id)
        self.sufficient = sufficient