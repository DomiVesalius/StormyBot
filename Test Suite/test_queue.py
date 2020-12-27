import unittest
from lib.queue import Queue
from random import randint
from hypothesis.strategies import lists, integers
from hypothesis import given


class TestQueueEnqueue(unittest.TestCase):
    """
    A test suite for Queue.enqueue method.
    """

    def test_enqueue_empty(self) -> None:
        """
        Tests the Queue.enqueue method on empty queues.
        """
        n = 0
        while n <= 10:
            q = Queue()
            queue_item = randint(-100, 100)
            q.enqueue(queue_item)
            self.assertEqual([queue_item], q.get_items())
            n += 1

    def test_enqueue_size_one(self) -> None:
        """
        Tests the Queue.enqueue method on queues with 1 item only.
        """
        n = 0
        while n <= 10:
            initial_item = randint(-1000, 1000)
            q = Queue([initial_item])
            new_item = randint(-1000, 1000)
            q.enqueue(new_item)
            self.assertEqual([initial_item, new_item], q.get_items())
            n += 1

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_enqueue_different_sizes(self, lst: list) -> None:
        """
        Tests the Queue.enqueue method on queues with different amounts of items.
        """
        q = Queue(lst)
        new_item = randint(-100, 100)

        q.enqueue(new_item)

        self.assertEqual(lst + [new_item], q.get_items())


class TestQueueDequeue(unittest.TestCase):
    """
    A test suite for Queue.enqueue method.
    """

    def test_dequeue_empty(self) -> None:
        """
        Tests the Queue.dequeue method on an empty queue.
        """
        q = Queue()
        self.assertIsNone(q.dequeue())

    def test_dequeue_size_one(self) -> None:
        """
        Tests the Queue.dequeue method on an empty queue.
        """
        q = Queue([14])
        self.assertEqual(14, q.dequeue())

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_dequeue_different_sizes(self, lst: list) -> None:
        """
        Tests the Queue.dequeue method on queues with different amounts of items.
        """
        q = Queue(lst)
        while not q.is_empty():
            self.assertEqual(lst.pop(0), q.dequeue())
