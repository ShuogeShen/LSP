from typing import Any

class ListNode:
    def __init__(self, key: str, value: Any) -> 'ListNode':
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self) -> 'DoublyLinkedList':
        self.dummyHead = ListNode('null', -1)
        self.dummyTail = ListNode('null', -1)
        self.size = 0
        self.dummyHead.next = self.dummyTail
        self.dummyTail.prev = self.dummyHead
    def addToHead(self, node: ListNode):
        node.prev = self.dummyHead
        node.next = self.dummyHead.next
        self.dummyHead.next.prev = node
        self.dummyHead.next = node
        self.size += 1
    def removeNode(self, node: ListNode):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
    def moveToHead(self, node: ListNode):
        self.removeNode(node)
        self.addToHead(node)

class LRUcache:
    def __init__(self, capacity: int = 100) -> 'LRUcache':
        self.keys = DoublyLinkedList()
        self.cache = {}
        self.capacity = capacity
        self.size = 0
    def contains(self, key: str) -> bool:
        return key in self.cache
    def get(self, key: str) -> Any:
        if key not in self.cache:
            return None
        node = self.cache[key]
        self.keys.moveToHead(node)
        return node.value
    def put(self, key: str, value: Any):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.keys.moveToHead(node)
        else:
            if self.keys.size == self.capacity:
                del self.cache[self.keys.dummyTail.prev.key]
                self.keys.removeNode(self.keys.dummyTail.prev)
            newNode = ListNode(key, value)
            self.cache[key] = newNode
            self.keys.addToHead(newNode)