import unittest
from lib.linked_list import LinkedList
from hypothesis.strategies import lists, integers
from hypothesis import given
from random import choice


class TestLinkedListInitializer(unittest.TestCase):
    """
    A test suite for the __init__ method of LinkedList
    """
    def test_no_argument(self) -> None:
        """
        Tests the initializer of LinkedList with no argument.
        :return: None
        """
        linky = LinkedList()
        self.assertEqual(0, linky.size)
        self.assertIsNone(linky.first)
        self.assertIsNone(linky.last)

    def test_length_one(self) -> None:
        """
        Tests the initializer of LinkedList with a list of length 1
        :return: None
        """
        linky = LinkedList([4])
        self.assertEqual(1, linky.size)
        self.assertEqual(4, linky.first.data)
        self.assertEqual(4, linky.last.data)

    def test_length_two(self) -> None:
        """
        Tests the initializer of LinkedList with a list of length 2
        :return: None
        """
        linky = LinkedList([3, 7])
        self.assertEqual(2, linky.size)  # Testing size
        # Testing values of each node
        self.assertEqual(3, linky.first.data)
        self.assertEqual(7, linky.last.data)
        # Testing references
        self.assertEqual(linky.first.next, linky.last)
        self.assertEqual(linky.first, linky.last.prev)
        self.assertIsNone(linky.first.prev)

    def test_length_three(self) -> None:
        """
        Tests the initializer of LinkedList with a list of length 3
        :return: None
        """
        lst = [9, 1, 43]
        linky = LinkedList(lst)
        self.assertEqual(3, linky.size)

        # Testing order/existence of items
        curr = linky.first
        for item in lst:
            self.assertEqual(curr.data, item)
            curr = curr.next

        curr = linky.last
        for item in lst[::-1]:
            self.assertEqual(curr.data, item)
            curr = curr.prev

        first_node, second_node = linky.first, linky.first.next
        third_node = linky.last

        self.assertEqual(second_node.prev, first_node)
        self.assertEqual(third_node.prev, second_node)
        self.assertIsNone(first_node.prev)
        self.assertIsNone(third_node.next)

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_random_lists(self, lst: list) -> None:
        """
        Tests the initializer with randomly generated deaths
        :param lst: list
        :return: None
        """
        linky = LinkedList(lst)
        curr = linky.first
        for item in lst:
            self.assertEqual(item, curr.data)
            curr = curr.next

        curr = linky.last
        for item in lst[::-1]:
            self.assertEqual(item, curr.data)
            curr = curr.prev


class TestLinkedListStr(unittest.TestCase):
    """
    A test suite for the __str__ method in LinkedList
    """
    def test_large_lists(self) -> None:
        """
        Tests the string representation method.
        :return:
        """
        lst1 = []
        str1 = '[]'
        lst2 = [57, -82, 77, -92, -95, 64, -87, 94, -80, 8]
        str2 = '[57 -> -82 -> 77 -> -92 -> -95 -> 64 -> -87 -> 94 -> -80 -> 8]'
        lst3 = [67, -96, -74, -66, 99, -1]
        str3 = '[67 -> -96 -> -74 -> -66 -> 99 -> -1]'
        lst4 = [100, -21, -20, -97, -6, -29]
        str4 = '[100 -> -21 -> -20 -> -97 -> -6 -> -29]'
        lst5 = [-84, 75, -48, -73, -54, -56, -13, -28, 38, -71, -37, 88]
        str5 = '[-84 -> 75 -> -48 -> -73 -> -54 -> -56 -> -13 -> -28 -> 38 -> '\
               '-71 -> -37 -> 88]'
        lst6 = [1]
        str6 = '[1]'

        self.assertEqual(str(LinkedList(lst1)), str1)
        self.assertEqual(str(LinkedList(lst2)), str2)
        self.assertEqual(str(LinkedList(lst3)), str3)
        self.assertEqual(str(LinkedList(lst4)), str4)
        self.assertEqual(str(LinkedList(lst5)), str5)
        self.assertEqual(str(LinkedList(lst6)), str6)


class TestLinkedListAppend(unittest.TestCase):
    """
    A test suite for the append method in LinkedList
    """
    def test_append_empty(self) -> None:
        """
        Tests the append method for an empty LinkedList
        :return: None
        """
        lst = LinkedList()
        lst.append(1)
        self.assertEqual(1, lst.size)
        self.assertEqual(1, lst.first.data)
        self.assertEqual(1, lst.last.data)
        self.assertEqual(lst.first, lst.last)

    def test_append_one_element(self) -> None:
        """
        Tests the append method for a LinkedList of size 1
        :return: None
        """
        lst = LinkedList([4])
        lst.append(91)
        self.assertEqual(2, lst.size)
        self.assertEqual(4, lst.first.data)
        self.assertEqual(91, lst.last.data)
        self.assertEqual(4, lst.last.prev.data)
        self.assertEqual(91, lst.first.next.data)

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_random_lists(self, lst: list) -> None:
        """
        Generates random lists and appends each item in the list to a LinkedList
        :param lst: list
        :return: None
        """
        linky = LinkedList()

        for item in lst:
            linky.append(item)

        self.assertEqual(len(lst), linky.size)

        curr = linky.first
        for item in lst:
            self.assertEqual(item, curr.data)
            curr = curr.next

        curr = linky.last
        for item in lst[::-1]:
            self.assertEqual(item, curr.data)
            curr = curr.prev


class TestLinkedListPrepend(unittest.TestCase):
    """
    A test suite for the prepend method in LinkedList
    """
    def test_prepend_empty(self) -> None:
        """
        Prepends to an empty LinkedList
        :return: None
        """
        lst = LinkedList()
        lst.prepend(14)
        self.assertEqual(1, lst.size)
        self.assertEqual(14, lst.first.data)
        self.assertEqual(14, lst.last.data)
        self.assertEqual(lst.first, lst.last)

    def test_prepend_one_element(self) -> None:
        """
        Prepends to a LinkedList of length 1
        :return: None
        """
        lst = LinkedList([51])
        lst.prepend(32)
        self.assertEqual(2, lst.size)
        self.assertEqual(32, lst.first.data)
        self.assertEqual(51, lst.last.data)
        self.assertEqual(lst.first.next, lst.last)
        self.assertEqual(lst.last.prev, lst.first)

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_random_lists(self, lst: list) -> None:
        """
        Tests prepend using randomly generated lists
        :param lst:
        :return: None
        """
        linky = LinkedList()

        for item in lst:
            linky.prepend(item)

        curr = linky.first
        for item in lst[::-1]:
            self.assertEqual(item, curr.data)
            curr = curr.next

        curr = linky.last
        for item in lst:
            self.assertEqual(item, curr.data)
            curr = curr.prev


class TestLinkedListPop(unittest.TestCase):
    """
    A test suite for the pop method in LinkedList
    """
    def test_pop_length_one(self) -> None:
        """
        Tests the pop method on a LinkedList of length 1
        :return: None
        """
        linky = LinkedList([5])
        self.assertEqual(5, linky.pop())

    def test_pop_length_three(self) -> None:
        """
        Tests the pop method on a LinkedList of length 3
        :return: None
        """
        linky = LinkedList([91, 3, 45])
        self.assertEqual(45, linky.pop())
        self.assertEqual(91, linky.first.data)
        self.assertEqual(3, linky.first.next.data)
        linky.append(45)
        self.assertEqual(3, linky.pop(1))
        self.assertEqual(45, linky.first.next.data)
        self.assertEqual(91, linky.pop(0))
        self.assertEqual(45, linky.first.data)

    @given(lst=lists(max_size=40, elements=integers(-100, 100)))
    def test_random_lists(self, lst: list) -> None:
        """
        Tests prepend using randomly generated lists
        :param lst:
        :return: None
        """
        lst2 = lst[:]
        lst3 = lst[:]
        lst4 = lst[:]

        linky = LinkedList(lst)
        for _ in range(len(lst)):
            self.assertEqual(lst.pop(), linky.pop())

        linky = LinkedList(lst2)
        for _ in range(len(lst2)):
            self.assertEqual(lst2.pop(0), linky.pop(0))

        linky = LinkedList(lst3)
        for _ in range(len(lst3)):
            j = (len(lst3) - 1) // 2
            self.assertEqual(lst3.pop(j), linky.pop(j))

        linky = LinkedList(lst4)
        for _ in range(len(lst4)):
            j = choice([0, -1])
            self.assertEqual(lst4.pop(j), linky.pop(j))


if __name__ == '__main__':
    unittest.main()
