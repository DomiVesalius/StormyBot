from __future__ import annotations
from typing import Any, Optional


class Node:
    """
    A node of a linked list.

    ==Attributes==
    data: The information the node is storing.
    next: A reference to the node after <self>
    prev: A reference to the node before <self>

    ==Representation Invariant==
    Empty Node:
        - item is None
        - next is None
        - prev is None
    """
    data: Any
    next: Optional[Node]
    prev: Optional[Node]

    def __init__(self, data: Any) -> None:
        """
        Initializes a node in a linked list.
        :param data: Any
        """
        self.data, self.next, self.prev = data, None, None


class LinkedList:
    """
    A linked list.
    """
    first: Optional[Node]
    last: Optional[Node]
    size: int

    def __init__(self, elements: list = None) -> None:
        """
        :param elements: list
        Initializes a linked list with the elements within <elements>
        """
        if elements is None or not elements:
            self.first, self.last, self.size = None, None, 0
        else:
            self.first = Node(elements[0])
            current = self.first
            for i in range(1, len(elements)):
                current.next = Node(elements[i])
                current.next.prev = current
                current = current.next
            self.last = current
            self.size = len(elements)

    def __str__(self) -> str:
        """
        Returns a string representation of <self>
        :return: str

        >>> linky = LinkedList([10, 2, 4, -1, 2])
        >>> str(linky)
        '[10 -> 2 -> 4 -> -1 -> 2]'
        """
        if self.size == 0:
            return '[]'

        res = f"[{self.first.data}"  # Starts with the first element in the list

        curr = self.first.next  #
        while curr is not None:
            res += f" -> {curr.data}"
            curr = curr.next

        res += "]"

        return res

    def __repr__(self) -> str:
        """
        Returns a representation of <self>
        :return: str
        """
        return str(self)

    def __len__(self) -> int:
        """
        Returns the number of items within <self>
        :return: int
        """
        return self.size

    def append(self, item: Any) -> None:
        """
        Appends <item> to the end of <self>
        :return: None
        """
        if self.size == 0:
            self.first = Node(item)
            self.last = self.first
        else:
            new_node = Node(item)
            new_node.prev = self.last  # Sets up reference to the last element
            self.last.next = new_node
            self.last = new_node  # Sets new node to be the new last node
        self.size += 1  # Increases size by one

    def prepend(self, item: Any) -> None:
        """
        Adds an element to the start of the list
        :param item:
        :return: None
        """
        if self.size == 0:
            self.first = Node(item)
            self.last = self.first
        else:
            new_node = Node(item)
            new_node.next = self.first  # Sets up the reference to next element
            self.first.prev = new_node  # Sets previous reference to new_node
            self.first = new_node  # Sets the new node as the first one
        self.size += 1  # Increases size by 1

    def pop(self, index: int = -1) -> Any:
        """
        Removes and return the last element from <self>
        :return: Any
        """
        if index < -1 or index >= self.size:
            raise IndexError

        # Removing the first item from the linked list
        if index == 0:
            data = self.first.data
            if self.size == 1:
                self.first = None
                self.last = None
            else:
                self.first = self.first.next
                self.first.prev = None
            self.size -= 1
            return data

        # Removing the last item from the linked list
        if index == -1:
            data = self.last.data
            if self.size == 1:
                self.first = None
                self.last = None
            else:
                self.last = self.last.prev
                self.last.next = None
            self.size -= 1
            return data

        if index <= self.size // 2:
            curr, i = self.first, 0
            while i != index:
                curr = curr.next
                i += 1
        else:
            curr, i = self.first, self.size - 1
            while i != index:
                curr = curr.prev
                i -= 1

        data = curr.data
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self.size -= 1
        return data
