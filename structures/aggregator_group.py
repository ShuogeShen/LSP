from typing import Type, List
from lsp_types import NullType, AggregatorGroupType

class AggregatorGroup:
    def __init__(
        self, 
        types: str, 
        threshold: float, 
    ) -> "AggregatorGroup":
        self.types = types
        self.threshold = threshold

class UGCD15(AggregatorGroup):
    def __init__(self, types: str = AggregatorGroupType.UGCD15, threshold: float = 0.75) -> "UGCD15":
        super().__init__(types, threshold)