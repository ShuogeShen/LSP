from typing import Type, Dict, List
from lsp_types import NodeType, AggregatorType
from utils import NodeTypeToClass
from core.lsp_core import gcd, cpa, dpa
from structures.lsp_node import LSPNode
import math

class LSPTree:
    def __init__(self, root: LSPNode = None) -> "LSPTree":
        self.root = root
    def setRoot(self, root: LSPNode):
        self.root = root
    @staticmethod
    def createNode(id: int, nodeType: str):
        return NodeTypeToClass[nodeType](id)
    def search(self, id: int) -> LSPNode:
        """
        e.g. 1
             |
             11 - 12 - 13
                   |
                   121 - 122
        """
        breakDowns = self._breakDownDigits(id)
        curr = self.root
        for i in range(0, len(breakDowns)):
            curr = self._searchHelper(breakDowns[i], curr)
            if curr is None:
                return None
            if i == len(breakDowns) - 1:
                return curr
            curr = curr.child
        return None
    def _searchHelper(self, id: int, node: LSPNode) -> LSPNode:
        while node is not None:
            if node.id == id:
                return node
            node = node.sibiling
        return None
    def _breakDownDigits(self, num: int):
        """
        e.g. 122 would become [1, 12, 122]
        """
        return [int(str(num)[0: i]) for i in range(1, len(str(num)) + 1)]
    def insert(self, returnsID: int, nodeType: str) -> LSPNode:
        """
        insert a new node to returns
        """
        returns = self.search(returnsID)
        cnt = 1
        if returns.child is None:
            returns.child = LSPTree.createNode(cnt, nodeType)
            return returns.child
        child = returns.child
        while child.sibiling is not None:
            child = child.sibiling
            cnt += 1
        child.sibiling = LSPTree.createNode(returns.id * 10 + cnt + 1, nodeType)
        return child.sibiling
    def remove(self, id: int) -> LSPNode:
        node = self.search(id)
        if node is None:
            return None
        if node == self.root:
            self.root = None
        elif node.returns is not None:
            node.returns.child = None
        else:
            returns = self.search(int(str(id)[0: len(id) - 1]))
            child = returns.child
            while child.sibiling is not None:
                if child.sibiling.id == id:
                    child.sibiling = None
                    break
        return node
    def scoring(self) -> float:
        self._postOrder(self.root)
        return self.root.score
    def _postOrder(self, node: LSPNode):
        if node is None:
            return
        if node.nodeType == NodeType.ATTRIBUTE:
            score = node.eac.solve(node.value)
            node.score = score if score != 0.0 else 0.01
            return
        if node.aggregatorType == AggregatorType.GCD:
            scores, weights, n = [], [], 0
            curr = node.child
            while curr is not None:
                self._postOrder(curr)
                scores.append(curr.score)
                weights.append(curr.weight)
                curr = curr.sibiling
                n += 1
            node.score = gcd(scores, weights, node.symbol[1], node.aggregatorGroup.threshold, n)
        elif node.aggregatorType == AggregatorType.CPA:
            optionalScore, mandatoryScore = 0.0, 0.0
            curr = node.child
            while curr is not None:
                self._postOrder(curr)
                if curr.id == node.optional:
                    optionalScore = curr.score
                if curr.id == node.mandatory:
                    mandatoryScore = curr.score
                curr = curr.sibiling
            node.score = cpa(node.innerWeight1, node.innerWeight2, mandatoryScore, optionalScore)
        elif node.aggregatorType == AggregatorType.DPA:
            optionalScore, sufficientScore = 0.0, 0.0
            curr = node.child
            while curr is not None:
                self._postOrder(curr)
                if curr.id == node.optional:
                    optionalScore = curr.score
                if curr.id == node.sufficient:
                    sufficientScore = curr.score
                curr = curr.sibiling
            node.score = dpa(node.innerWeight1, node.innerWeight2, sufficientScore, optionalScore)
    def printInfo(self, info: Dict):
        self._preOrder(self.root, info, lambda x : self._selfPrint(x))
    def _selfPrint(self, node):
        digits = len(str(node.id))
        space = ''
        for i in range(0, digits - 1):
            space += '  '
        if node.nodeType == NodeType.ATTRIBUTE:
            return space + str(node.id) + ' ' + node.name + ' || ' + str(node.breakValues) + ' || input: ' + str(node.value) + ' (' + node.units + ')'
        else:
            symbol = node.symbol[0] if node.aggregatorType == AggregatorType.GCD else ''
            penalty_reward = 'Penalty: ' + str(node.penalty) + ', Reward: ' + str(node.reward) if (node.aggregatorType == AggregatorType.CPA or node.aggregatorType == AggregatorType.DPA) else ''
            return space + str(node.id) + ' ' + node.name + ' || ' + node.aggregatorType.upper() + ' || ' + symbol + penalty_reward
    def _preOrder(self, node: LSPNode, info: Dict, func):
        if node is None:
            return
        info['nodes'].append(func(node))
        self._preOrder(node.child, info, func)
        self._preOrder(node.sibiling, info, func)
    
    def _getCount(self, node: LSPNode) -> int:
        if node is None:
            return 0
        return self._getCount(node.child) + self._getCount(node.sibiling) + 1
    
    def _deep_equals(self, nodeDict: Dict) -> bool:
        if not self._deep_equals_helper(self.root, nodeDict):
            return False
        if self._getCount(self.root) != len(nodeDict):
            return False
        return True
    
    def _deep_equals_helper(self, node: LSPNode, nodeDict: Dict) -> bool:
        if node is None:
            return True
        if str(node.id) not in nodeDict or not self._equals(node, nodeDict[str(node.id)]):
            return False
        if not self._deep_equals_helper(node.child, nodeDict):
            return False
        if not self._deep_equals_helper(node.sibiling, nodeDict):
            return False
        return True
    
    def _equals(self, node: LSPNode, newNode: Dict) -> bool:
        if node.nodeType != newNode['nodeType'].lower():
            return False
        if node.nodeType == NodeType.ATTRIBUTE:
            return self._attribute_equals(node, newNode)
        elif node.nodeType == NodeType.AGGREGATOR:
            return self._aggregator_equals(node, newNode)
        return False
    
    def _attribute_equals(self, node: LSPNode, newNode: Dict) -> bool:
        if node.name != newNode['name']:
            node.name = newNode['name']
        if node.units != newNode['details']['units']:
            node.units = newNode['details']['units']
        if node.id != 1 and 'weight' in newNode and node.weight != float(newNode['weight']):
            return False
        if not self._attribute_breaks_equals(node.breakValues, newNode['details']['breakValues']):
            return False
        return True
    
    def _attribute_breaks_equals(self, oldBreaks: List, newBreak: List) -> bool:
        if len(oldBreaks) != len(newBreak):
            return False
        for i in range(0, len(oldBreaks)):
            if oldBreaks[i][0] != float(newBreak[i][0]) or oldBreaks[i][1] != float(newBreak[i][1]):
                return False
        return True
    
    def _aggregator_equals(self, node: LSPNode, newNode: Dict) -> bool:
        if node.name != newNode['name']:
            node.name = newNode['name']
        if node.id != 1 and 'weight' in newNode and node.weight != float(newNode['weight']):
            return False
        if node.aggregatorType != newNode['details']['aggregatorType'].lower():
            return False
        if node.aggregatorType == AggregatorType.GCD:
            if node.symbol[0] != newNode['details']['symbol'].lower():
                return False
        elif node.aggregatorType == AggregatorType.CPA:
            if node.penalty != float(newNode['details']['penalty']):
                return False
            if node.reward != float(newNode['details']['reward']):
                return False
            if node.optional != int(newNode['details']['optional']):
                return False
            if node.mandatory != int(newNode['details']['mandatory']):
                return False
        elif node.aggregatorType == AggregatorType.DPA:
            if node.penalty != float(newNode['details']['penalty']):
                return False
            if node.reward != float(newNode['details']['reward']):
                return False
            if node.optional != int(newNode['details']['optional']):
                return False
            if node.sufficient != int(newNode['details']['sufficient']):
                return False
        return True