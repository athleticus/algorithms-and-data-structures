class AVLNode:
    """Represents a node in an AVL tree"""
    __slots__ = ['height', 'left_child', 'right_child', 'key', 'value']

    def __init__(self, key, value=None):
        """
        Constructs an AVLNode.

        :param key: Orderable key (i.e. integer)
        :param value: Optional value associated with key.
        """
        self.height = 1
        self.key = key
        self.value = value
        self.left_child = None
        self.right_child = None

    def update_height(self):
        """
        Updates the height of the node according to the heights of its children.
        """
        self.height = max((self.left_child and self.left_child.height) or 0,
                          (
                              self.right_child and self.right_child.height) or 0) + 1

    def is_leaf(self):
        """
        :return: True iff this node is a leaf, else False.
        """
        return self.left_child is None and self.right_child is None

    def flatten(self, level=0):
        """
        Flattens this node and its children into a list of columns.
        :param level: The level to begin indenting.
        :return: A list of flattened nodes, with the first being the rightmost.
        """
        output = []
        if self.right_child:
            output.extend(self.right_child.flatten(level + 1))
        output.append("\t" * level + str(self))
        if self.left_child:
            output.extend(self.left_child.flatten(level + 1))

        return output

    def get_relative_left_height(self):
        """
        :return: Difference between left child's height and right's height.
        """
        return ((self.left_child and self.left_child.height) or 0) - (
            (self.right_child and self.right_child.height) or 0)

    def __str__(self):
        return "{} (h={})".format(self.key, self.height)

    def __repr__(self):
        return "AVLNode({!r})".format(self.key)

    def in_order_traversal(self):
        """
        Yields in-order traversal of this node and its children.

        :yield: In-order traversal of this node.
        """
        if self.left_child:
            yield from self.left_child.in_order_traversal()
        yield self
        if self.left_child:
            yield from self.right_child.in_order_traversal()

    def pre_order_traversal(self):
        """
        Yields pre-order traversal of this node and its children.

        :yield: Pre-order traversal of this node.
        """
        yield self
        if self.left_child:
            yield from self.left_child.pre_order_traversal()
        if self.left_child:
            yield from self.right_child.pre_order_traversal()

    def post_order_traversal(self):
        """
        Yields post-order traversal of this node and its children.

        :yield: Post-order traversal of this node.
        """
        if self.left_child:
            yield from self.left_child.post_order_traversal()
        if self.left_child:
            yield from self.right_child.post_order_traversal()
        yield self



class AVLTree:
    """Represents an AVL tree, with optional values.

    Provides O(log n) operations:
        - queries (find/predecessor/successor)
        - insertion/deletion
    """
    __slots__ = ['_root', '_length']

    def __init__(self, items=None):
        """
        Constructs AVLTree.

        :param items: Optional iterable of key, value pairs to insert.
        """
        self._root = None
        self._length = 0

        if items:
            for key, value in items:
                self.insert(key, value)

    @classmethod
    def from_keys(cls, keys, value=None):
        """
        Constructs an AVLTree from a set of keys.
        :param keys: Iterable of keys to insert.
        :param value: Value to be associated with each key. Defaults to None.
        :return: Newly constructed AVLTree.
        """
        tree = cls()

        for key in keys:
            tree.insert(key, value)

        return tree

    def get_root(self):
        """
        :return: The root node.
        """
        return self._root

    def insert(self, e, value=None):
        """
        Inserts key into this AVLTree.

        :param e: Key to be inserted.
        :param value: Optional value to be associated with key.
        :return: None
        """
        u = self._root
        z = AVLNode(e, value)

        if u is None:
            self._root = z
            self._length += 1
            return

        stack = []

        while True:
            stack.append(u)

            if e == u.key:
                u.value = e
            elif e < u.key:
                if u.left_child:
                    u = u.left_child
                else:
                    u.left_child = z
                    break
            else:
                if u.right_child:
                    u = u.right_child
                else:
                    u.right_child = z
                    break

        self._length += 1

        # balance
        self._balance_stack(stack)

    def _balance_stack(self, nodes):
        """
        Balances nodes in a stack.

        :param nodes: An iterable of nodes to balance. Last node in stack is first
            node to be balanced.
        :return: None
        """
        for i, node in enumerate(reversed(nodes)):

            i = len(nodes) - i - 1  # Reverse index

            node.update_height()
            dh = node.get_relative_left_height()
            # self.print()
            # print("Checking {} for balance (lh-rh={})".format(node, dh))

            # Already balanced
            if -1 <= dh <= 1:
                continue

            if dh > 0:  # left imbalance
                dh2 = node.left_child.get_relative_left_height()

                if dh2 >= 0:  # left-left imbalance
                    new_node = self._single_rotation_right(node)
                    # print(
                    #     'left-left => single rot right; {} replaced by {}'.format(
                    #         node, new_node))
                else:  # left-right imbalance
                    new_node = self._double_rotation_right(node)
                    # print(
                    #     'left-right => double rot right; {} replaced by {}'.format(
                    #         node, new_node))

            else:  # right imbalance
                dh2 = node.right_child.get_relative_left_height()

                if dh2 > 0:  # right-left imbalance
                    new_node = self._double_rotation_left(node)
                    # print(
                    #     'right-left => double rot left; {} replaced by {}'.format(
                    #         node, new_node))
                else:  # right-right imbalance
                    new_node = self._single_rotation_left(node)
                    # print(
                    #     'right-right => single rot left; {} replaced by {}'.format(
                    #         node, new_node))

            if i != 0:  # non-root node
                parent = nodes[i - 1]
                if parent.left_child is node:
                    parent.left_child = new_node
                else:
                    parent.right_child = new_node
            else:
                self._root = new_node
            new_node.update_height()

    @staticmethod
    def _single_rotation_right(node):
        """
        Performs a single right rotation on the given node.

        :param node: The node to singly rotate right.
        :return: The new node that takes the place of node.
        """
        a = node
        b = a.left_child

        a.left_child = b.right_child
        a.update_height()
        b.right_child = a
        b.update_height()

        return b

    @staticmethod
    def _double_rotation_right(node):
        """
        Performs a double right rotation on the given node.

        :param node: The node to doubly rotate right.
        :return: The new node that takes the place of node.
        """
        a = node
        b = a.left_child
        c = b.right_child

        a.left_child = c.right_child
        a.update_height()
        b.right_child = c.left_child
        b.update_height()
        c.left_child = b
        c.right_child = a
        c.update_height()

        return c

    @staticmethod
    def _single_rotation_left(node):
        """
        Performs a single left rotation on the given node.

        :param node: The node to singly rotate left.
        :return: The new node that takes the place of node.
        """
        a = node
        b = a.right_child

        a.right_child = b.left_child
        a.update_height()
        b.left_child = a
        b.update_height()

        return b

    @staticmethod
    def _double_rotation_left(node):
        """
        Performs a double left rotation on the given node.

        :param node: The node to doubly rotate left.
        :return: The new node that takes the place of node.
        """
        a = node
        b = a.right_child
        c = b.left_child

        a.right_child = c.left_child
        a.update_height()
        b.left_child = c.right_child
        b.update_height()
        c.right_child = b
        c.left_child = a
        c.update_height()

        return c

    def _predecessor_node(self, key, root=None, stack=None):
        """
        Returns the node with predecessor to key.

        :param key: Key to use for predecessor comparison.
        :param root: Node to begin searching from. Defaults to root.
        :param stack: Stack of nodes to extend with search path.
        :return:
        """
        pre = None
        if not root:
            node = self._root
        else:
            node = root

        if not stack:
            stack = []

        while True:
            if node is None:
                return pre

            stack.append(node)

            if node.key == key:
                pre = node
                return pre
            elif node.key > key:
                node = node.left_child
            else:
                pre = node
                node = node.right_child

    def predecessor(self, key):
        """
        Finds predecessor in tree.

        :param key: Key to use for predecessor comparison.
        :return: Predecessor of key, else None.
        """
        node = self._predecessor_node(key)
        if node:
            return node.key

    def _successor_node(self, key, root=None, stack=None):
        """
        Returns the node with successor to key.

        :param key: Key to use for successor comparison.
        :param root: Node to begin searching from. Defaults to root.
        :param stack: Stack of nodes to extend with search path.
        :return:
        """
        suc = None
        if not root:
            node = self._root
        else:
            node = root

        if not stack:
            stack = []

        while True:
            if node is None:
                return suc

            stack.append(node)

            if node.key == key:
                suc = node
                return suc
            elif node.key < key:
                node = node.right_child
            else:
                suc = node
                node = node.left_child

    def successor(self, key):
        """
        Finds successor in tree.

        :param key: Key to use for successor comparison.
        :return: Successor of key, else None.
        """
        node = self._successor_node(key)
        if node:
            return node.key

    def remove(self, e):
        """
        Removes key from tree.

        :param e: The key to remove.
        :return: Value formerly associated with key.
        """
        u = self._root

        stack = []

        while True:
            if u is None:
                raise KeyError(e)

            stack.append(u)

            if e == u.key:
                break
            elif e < u.key:
                if u.left_child:
                    u = u.left_child
                else:
                    u = None
            else:
                if u.right_child:
                    u = u.right_child
                else:
                    u = None

        value = u.value

        # # Case 1 - remove root
        # if u is self._root:
        #     self._root = None
        #     self._length = 0
        #     return

        # Case 1 - remove leaf
        if u.is_leaf():
            if u is self._root:
                self._root = None
            else:
                parent = stack[-2]
                if parent.left_child is u:
                    parent.left_child = None
                else:
                    parent.right_child = None

        # Case 2 - has right subtree
        elif u.right_child:
            # Find node with smallest key in right subtree (proper successor)
            self._successor_node(u.key, u.right_child, stack)
            # print(stack)

            # Delete successor and insert into place of node to be deleted
            v = stack.pop()
            u.key = v.key
            u.value = v.value

            parent = stack[-1]
            if parent.left_child is v:
                parent.left_child = v.right_child
            else:
                parent.right_child = v.right_child

            pass

            # Can't use predecessor since left subtree may be empty
            # (need to also invert case 2 & 3)
            # # Find node with largest key in left subtree (proper predecessor)
            # self._predecessor_node(u.key, u.left_child, stack)
            #
            # # Delete predecessor and insert into place of node to be deleted
            # v = stack.pop()
            # u.key = v.key
            # u.value = v.value
            #
            # print(v)
            #
            # print('SSS', stack)
            #
            # parent = stack[-1]
            # if parent.left_child is v:
            #     parent.left_child = v.left_child
            # else:
            #     parent.right_child = v.left_child

        # Case 3 - has no right subtree
        else:
            if u is self._root:
                self._root = u.left_child
            else:
                parent = stack[-2]
                if parent.left_child is u:
                    parent.left_child = u.left_child
                else:
                    parent.right_child = u.left_child

        self._length -= 1

        self._balance_stack(stack)

        return value

    def print(self):
        """
        Prints out a basic representation of this tree.

        :return: None
        """
        print(self)

    def in_order_traversal(self):
        """
        Yields an in-order traversal of this tree's nodes.

        :yield: In-order traversal of this tree's nodes.
        """
        if not self._root:
            return

        yield from self._root.in_order_traversal()

    def pre_order_traversal(self):
        """
        Yields an pre-order traversal of this tree's nodes.

        :yield: Pre-order traversal of this tree's nodes.
        """
        if not self._root:
            return

        yield from self._root.pre_order_traversal()

    def post_order_traversal(self):
        """
        Yields an post-order traversal of this tree's nodes.

        :yield: Post-order traversal of this tree's nodes.
        """
        if not self._root:
            return

        yield from self._root.post_order_traversal()

    def keys(self):
        """
        Returns an iterator over the keys in this tree.
        :return: Iterator over keys.
        """

        for node in self.in_order_traversal():
            yield node.key

    def values(self):
        """
        Returns an iterator over the associated values in this tree.
        :return: Iterator over associated values.
        """

        for node in self.in_order_traversal():
            yield node.value

    def items(self):
        """
        Returns an iterator over the key, value pairs in this tree.
        :return: Iterator over key, value pairs.
        """

        for node in self.in_order_traversal():
            yield node.key, node.value

    def copy(self):
        """
        Returns a deepcopy of this tree.
        :return: New AVLTree.
        """

        tree = AVLTree()

        for node in self.pre_order_traversal():
            tree.insert(node)

        return tree

    def __getitem__(self, key):
        node = self._successor_node(key)
        if not node or node.key != key:
            raise KeyError(key)

        return node.value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __len__(self):
        return self._length

    def __contains__(self, key):
        node = self._successor_node(key)
        return node and node.key == key

    def __iter__(self):
        yield from self.keys()

    def __repr__(self):
        return "AVLTree({!r})".format(tuple(node.key for node in self))

    def __str__(self):
        if self._root:
            return "\n".join(self._root.flatten())
        else:
            return "<empty>"




# Imports for tests
import random
import itertools
import time


def generate_unique_random(length, range_stop):
    """
    Returns a list of unique random integers.

    :param length: The length of the returned list.
    :param range_stop: Values are in range [0, range_stop)
    :return: list(int, ...)
    """

    elements = list(range(range_stop))
    random.shuffle(elements)
    return elements[:length]


def insertion_test():
    # keys = generate_unique_random(20, 100)
    # print(keys)
    keys = [92, 5, 41, 70, 20, 35, 12, 45, 14, 19, 53, 72, 71, 3, 76, 81, 48,
            49, 10, 84]

    # keys = keys[:5]

    auto_i = 0

    tree = AVLTree.from_keys(keys[:auto_i])

    tree.print()

    for key in keys[auto_i:]:
        print("#" * 80)
        print("#" * 80)
        print("#{:^78}#".format(key))
        print("#" * 80)
        print("#" * 80)
        tree.insert(key)

        # tree.print()

    tree.print()


def deletion_test():
    keys = [1, 5, 6, 8, 9, 10, 11, 12, 21, 23, 24, 25, 33, 42, 43, 7]

    N = 20
    U = 100
    DELETIONS = 10

    while True:
        insertions = generate_unique_random(20, 100)

        print("Tree from {}".format(insertions))

        for i in range(DELETIONS):
            tree = AVLTree.from_keys(insertions)
            deletions = insertions[:]
            random.shuffle(deletions)

            print("\tDeleting with {}".format(deletions))

            for key in deletions:
                tree.remove(key)

    return

    # Test all possibly combinations of insertion and deletion order.
    for insertion_order in itertools.permutations(keys, len(keys)):
        for deletion_order in itertools.permutations(keys, len(keys)):
            tree = AVLTree.from_keys(keys)
            for key in deletion_order:
                try:
                    tree.remove(key)
                except Exception as e:
                    print("Failed on insert: {}; delete: {}".format(
                        insertion_order, deletion_order))
                    raise e


def main():
    deletion_test()


if __name__ == "__main__":
    # Hack to synchronize stderr & stdout in Pycharm
    try:
        main()
    except Exception as e:
        time.sleep(0.1)
        raise e
