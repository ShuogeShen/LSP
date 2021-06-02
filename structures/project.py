from typing import Type, Dict, List
from lsp_types import NodeType, AggregatorType
from structures.attribute import Attribute
from structures.lsp_tree import LSPTree
from structures.lsp_node import LSPNode
from structures.aggregator_group import AggregatorGroup
from eac.elementary_attribute_criteria import EAC
from converter.penalty_reward import PenaltyReward
from utils import load, NodeTypeToClass, AggregatorGroupTypeToClass, AggregatorGroupTypeToAggregatorSymbol
from error import JsonPropertyMissingError, NodePropertyError, AggregatorSymbolError, AggregationTreeError, AttributeValueError, NotAttributeError, AggregatorTypeNotExistError

class Project:
    def __init__(self, name: str, tree: LSPTree = None, aggregatorGroup: AggregatorGroup = None, offsetConverter: PenaltyReward = None) -> "Project":
        self.name = name
        self.tree = tree
        self.aggregatorGroup = aggregatorGroup
        self.offsetConverter = offsetConverter
    
    def _build(self, data: Dict):
        """
        please refer to /example/project_example.json for more information
        """
        self.name = data['project']
        self.aggregatorGroup = AggregatorGroupTypeToClass[data['aggregatorGroupType'].lower()]()
        self.offsetConverter = PenaltyReward()
        self.tree = self._buildTree(list(data['nodes'].values()))
    
    def _setValue(self, values: List):
        """
        please refer to /example/value_example.json for more information
        """
        if self.tree is None:
            raise AggregationTreeError()
        self._checkValues(values)
        for content in values:
            node = self.tree.search(int(content['id']))
            if node is None:
                raise AttributeValueError(node['id'])
            if node.nodeType != NodeType.ATTRIBUTE:
                raise NotAttributeError(str(node.id))
            node.value = float(content['value'])
    
    def _buildTree(self, nodes: List) -> LSPTree:
        tree = LSPTree()
        self._checkNodes(nodes)
        nodes.sort(key=lambda x : x['id'])
        nodeDict = self._createNodeDict(nodes)
        self._createNodeRelationship(nodeDict, tree)
        return tree
    
    def _createNodeDict(self, nodes: List) -> Dict:
        nodeDict = {} # {"id": LSPNode}
        for node in nodes:
            if 'attribute' in node['nodeType']:
                nodeDict[node['id']] = self._buildAttribute(node)
            elif 'aggregator' in node['nodeType']:
                nodeDict[node['id']] = self._buildAggregator(node)
            else:
                raise NodePropertyError(node['id'], 'missing property attribute or aggregator')
        return nodeDict
    
    def _createNodeRelationship(self, nodeDict: Dict, tree: LSPTree):
        if '1' not in nodeDict:
            raise JsonPropertyMissingError('node id 1')
        tree.setRoot(nodeDict['1'])
        self._appendChild(nodeDict, tree.root)
        self._appendSibiling(nodeDict, tree.root)
    
    def _appendChild(self, nodeDict: Dict, node: LSPNode):
        child = str(node.id) + '1'
        if child in nodeDict:
            node.child = nodeDict[child]
            nodeDict[child].returns = node
            self._appendChild(nodeDict, node.child)
            self._appendSibiling(nodeDict, node.child)
    
    def _appendSibiling(self, nodeDict: Dict, node: LSPNode):
        if node.id % 10 == 9:
            return
        sibiling = str(node.id + 1)
        if sibiling in nodeDict:
            node.sibiling = nodeDict[sibiling]
            self._appendChild(nodeDict, node.sibiling)
            self._appendSibiling(nodeDict, node.sibiling)
    
    def _buildAttribute(self, node: Dict) -> LSPNode:
        self._checkAttribute(node)
        attribute = NodeTypeToClass[node['nodeType'].lower()](int(node['id']))
        attribute.name = node['name'] if 'name' in node else ''
        attribute.weight = float(node['weight']) if 'weight' in node else -1.0
        attribute.nodeType = NodeType.ATTRIBUTE
        attribute.units = node['details']['units'] if 'units' in node['details'] else ''
        attribute.breakValues = [(float(breakPoint[0]), float(breakPoint[1])) for breakPoint in node['details']['breakValues']]
        attribute.eac = EAC()
        attribute.eac.define(attribute.breakValues)
        return attribute
    
    def _buildAggregator(self, node: Dict) -> LSPNode:
        self._checkAggregator(node)
        aggregator = NodeTypeToClass[node['details']['aggregatorType'].lower()](int(node['id']))
        aggregator.name = node['name'] if 'name' in node else ''
        aggregator.weight = float(node['weight']) if 'weight' in node else -1.0
        aggregator.nodeType = NodeType.AGGREGATOR
        aggregator.aggregatorGroup = self.aggregatorGroup
        if node['details']['aggregatorType'] == AggregatorType.GCD:
            aggregator.aggregatorType = AggregatorType.GCD
            if node['details']['symbol'].lower() not in AggregatorGroupTypeToAggregatorSymbol[aggregator.aggregatorGroup.types]:
                raise AggregatorSymbolError(node['id'])
            aggregator.symbol = AggregatorGroupTypeToAggregatorSymbol[aggregator.aggregatorGroup.types][node['details']['symbol'].lower()]
        else:
            if node['details']['aggregatorType'] != AggregatorType.CPA and node['details']['aggregatorType'] != AggregatorType.DPA:
                raise AggregatorTypeNotExistError(node['id'])
            aggregator.aggregatorType = node['details']['aggregatorType']
            aggregator.penalty = float(node['details']['penalty'])
            aggregator.reward = float(node['details']['reward'])
            aggregator.optional = int(node['details']['optional'])
            w1, w2 = self.offsetConverter.search(aggregator.penalty, aggregator.reward, aggregator.aggregatorType)
            aggregator.innerWeight1 = w1
            aggregator.innerWeight2 = w2
            if node['details']['aggregatorType'] == AggregatorType.CPA:
                aggregator.mandatory = int(node['details']['mandatory'])
            elif node['details']['aggregatorType'] == AggregatorType.DPA:
                aggregator.sufficient = int(node['details']['sufficient'])
        return aggregator

    def _run(self) -> float:
        if self.tree is None:
            raise AggregationTreeError()
        return self.tree.scoring()
    
    def perform(self, data: Dict, printInfo: bool) -> Dict:
        self._build(data)
        return self.perform_without_build(data, printInfo)
    
    def perform_without_build(self, data: Dict, printInfo: bool) -> Dict:
        self._setValue(data['values'])
        info = {}
        if printInfo:
            self._info(info)
        info['score'] = self._run()
        return info
    
    def _info(self, info: Dict):
        info['project'] = self.name
        info['aggregator_group'] = self.aggregatorGroup.types
        info['nodes'] = []
        self.tree.printInfo(info)
    
    def diff(self, new: Dict) -> bool:
        if self.aggregatorGroup.types != new['aggregatorGroupType'].lower():
            return False
        if not self.tree._deep_equals(new['nodes']):
            return False
        if self.name != new['project']:
            self.name = new['project']
        return True
    
    def _checkNodes(self, nodes: List):
        for node in nodes:
            if 'id' not in node:
                raise JsonPropertyMissingError('id')
            if 'nodeType' not in node:
                raise NodePropertyError(node['id'], 'missing nodeType')
            if 'details' not in node:
                raise NodePropertyError(node['id'], 'missing details')
    
    def _checkValues(self, values: List):
        pass
        
    def _checkAttribute(self, node: Dict):
        pass

    def _checkAggregator(self, node: Dict):
        pass