from __future__ import annotations
from typing import Any, Union, List
from lib.linked_list import LinkedList
from random import shuffle


class Queue:
    """
    A FIFO queue data structure.
    """
    _items: Union[LinkedList, List]
    looping: bool

    def __init__(self, items: list = None) -> None:
        """
        Creates a Queue with <items>
        :param items: Optional[list]
        """
        if items is None or not items:  # items == None or items == []
            self._items = LinkedList()
        else:
            self._items = LinkedList(items)
        self.looping = False

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

    def is_looping(self) -> bool:
        """
        Returns True iff self is a looping queue.
        """
        return self.looping

    def string_formatted(self) -> str:
        """
        Returns a formatted version of the string representation of this queue.
        """
        if isinstance(self._items, list):
            res = ''
            for i, item in enumerate(self._items):
                if i == len(self._items) - 1:
                    res += f"{i + 1}. {item}"
                else:
                    res += f"{i + 1}. {item}\n"
            return res

        return self._items.string_formatted()

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
            item = self._items.pop(0)
            if self.looping:
                self.enqueue(item)
            return item

    def loop(self) -> None:
        """
        Sets this queue to looping.
        """
        self.looping = not self.looping

    def shuffle(self) -> None:
        """
        Shuffles the queue.
        """
        if isinstance(self._items, list):
            shuffle(self._items)
        else:
            self._items.shuffle()
