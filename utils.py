from typing import Dict
from lsp_types import NodeType, AggregatorType, AggregatorGroupType
from aggregator_symbol import UGCD15_Symbol
from structures.attribute import Attribute
from structures.aggregator import GCD_Aggregator, CPA_Aggregator, DPA_Aggregator
from structures.aggregator_group import UGCD15
import json

NodeTypeToClass = {
    NodeType.ATTRIBUTE: Attribute,
    AggregatorType.GCD: GCD_Aggregator,
    AggregatorType.CPA: CPA_Aggregator,
    AggregatorType.DPA: DPA_Aggregator,
}

AggregatorGroupTypeToClass = {
    AggregatorGroupType.UGCD15: UGCD15
}

AggregatorGroupTypeToAggregatorSymbol = {
    AggregatorGroupType.UGCD15: UGCD15_Symbol
}

def load(file_path: str) -> Dict:
    """
    please refer to /example/project_example.json for more information
    """
    with open(file_path) as json_file:
        return json.load(json_file)