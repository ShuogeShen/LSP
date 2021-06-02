class NullType:
    NULL = 'null'

class NodeType:
    ATTRIBUTE = 'attribute'
    AGGREGATOR = 'aggregator'

class AggregatorType:
    GCD = 'gcd'
    CPA = 'cpa'
    DPA = 'dpa'
    NULL = ('null', -1.0)

class AggregatorGroupType:
    UGCD7 = 'ugcd7'
    UGCD15 = 'ugcd15'
    UGCD23 = 'ugcd23'
    GGCD9 = 'ggcd9'
    GGCD17 = 'ggcd17'
    GGCD25 = 'ggcd25'
    WPM17 = 'wpm17'

class EACFunctionType:
    LINEAR = 'linear'
    POLYNOMIAL = 'polynomial'