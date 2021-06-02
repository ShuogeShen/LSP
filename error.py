class EACNotDefineError(Exception):
    def __init__(self, message: str = 'Elementary Attribute Criteria is not yet defined'):
        self.message = message
        super().__init__(self.message)

class ScoresAndWeightsDoesNotMatchError(Exception):
    def __init__(self, message: str = 'The length of scores does not match with the length of weights'):
        self.message = message
        super().__init__(self.message)

class JsonPropertyMissingError(Exception):
    def __init__(self, prop: str, message: str = 'The json object is missing: '):
        self.message = message + prop
        super().__init__(self.message)

class NodePropertyError(Exception):
    def __init__(self, nodeID: str, prop: str):
        self.message = 'The node [' + nodeID + ']: ' + prop
        super().__init__(self.message)

class AggregatorSymbolError(Exception):
    def __init__(self, nodeID: str):
        self.message = 'The node [' + nodeID + '] has an incorrect aggregator symbol'
        super().__init__(self.message)

class AggregationTreeError(Exception):
    def __init__(self):
        self.message = 'Aggregation tree error'
        super().__init__(self.message)

class AttributeValueError(Exception):
    def __init__(self, nodeID: str):
        self.message = 'The node [' + nodeID + '] does not exist or has incorrect value'
        super().__init__(self.message)

class NotAttributeError(Exception):
    def __init__(self, nodeID: str):
        self.message = 'The node [' + nodeID + '] is not a attribute and the value cannot be set'
        super().__init__(self.message)

class AggregatorTypeNotExistError(Exception):
    def __init__(self, nodeID: str):
        self.message = 'Aggregation type in node [' + nodeID + '] does not exist'
        super().__init__(self.message)