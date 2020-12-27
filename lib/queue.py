from __future__ import annotations
from typing import Any, Union, List
from lib.linked_list import LinkedList


class Queue:
    """
    A FIFO queue data structure.
    """
    _items: Union[LinkedList, List]

    def __init__(self, items: list = None) -> None:
        """
        Creates a Queue with <items>
        :param items: Optional[list]
        """
        if items is None or not items:  # items == None or items == []
            self._items = LinkedList()
        else:
            self._items = LinkedList(items)

    def get_items(self) -> list:
        """
        Returns a list of items in the order they appear within self.

        >>> q = Queue()
        >>> q.get_items()
        []
        >>> q = Queue([])
        >>> q.get_items()
        []
        >>> q = Queue([4, 9, 3, 1])
        >>> q.get_items()
        [4, 9, 3, 1]
        """
        return self._items.get_items()

    def is_empty(self) -> bool:
        """
        Returns True iff _items is empty
        :return: bool
        >>> q = Queue([9, 14, 3, -1])
        >>> q.is_empty()
        False
        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q = Queue([])
        >>> q.is_empty()
        True
        """
        return self._items.size == 0

    def enqueue(self, item: Any) -> None:
        """
        Enqueues <item> into the Queue <self>
        :param item: Any
        :return: None
        >>> q = Queue()
        >>> q.enqueue(91)
        >>> q.is_empty()
        False
        >>> q.dequeue()
        91
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """
        Removes the first item in the Queue <self> if it is not empty.
        :return: Any
        >>> q = Queue([9, 10, 44, -2, -3])
        >>> q.dequeue()
        9
        >>> q.dequeue()
        10
        >>> q.dequeue()
        44
        >>> q.dequeue()
        -2
        >>> q.dequeue()
        -3
        """
        if not self.is_empty():
            return self._items.pop(0)
