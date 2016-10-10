class BinaryHeapNode:
    """Represents a node in an Binary Heap"""
    __slots__ = ['index', 'key', 'value']

    def __init__(self, key, value=None):
        """
        Constructs an BinaryHeapNode.

        :param key: Orderable key (i.e. integer)
        :param value: Optional value associated with key.
        """
        self.key = key
        self.value = value
        self.index = None

    def __str__(self):
        return "{}".format(self.key)

    def __repr__(self):
        return "BinaryHeapNode({!r})".format(self.key)


class PriorityQueue:
    """Represents a PriorityQueue on a set of items with unique, orderable keys,
    implemented with a dynamic array (list)."""
    __slots__ = ['_nodes']

    def __init__(self, items=None):
        self._nodes = []

        if items:
            for key, value in items:
                self.insert(key, value)

    def from_keys(self, keys, value=None):
        heap = self.__class__()

        for key in keys:
            heap.insert(key, value)

        return heap

    def get_root(self):
        """
        :return: The root node.
        """
        return self._nodes[0]

    def get_child_indices(self, i):
        return 2 * i + 1, 2 * i + 2

    def get_left_index(self, i):
        return 2 * i + 1

    def get_right_index(self, i):
        return 2 * i + 2

    def get_parent_index(self, i):
        return (i - 1)// 2

    def print(self):
        """
        Prints out a basic representation of this tree.

        :return: None
        """

    def in_order_traversal(self):
        """
        Yields an in-order traversal of this tree's nodes.

        :yield: In-order traversal of this tree's nodes.
        """
        if not self._nodes:
            return

        traversal = []

        # 1) Create an empty stack S.
        stack = []

        # 2) Initialize current node as root
        i = 0
        depth = 0

        # 3) Push the current node to S and set current = current->left until current is NULL
        while True:
            while i < len(self._nodes):
                stack.append((i, depth))
                i = self.get_left_index(i)
                depth += 1


            # 4) If current is NULL and stack is not empty then
            if len(stack):
                # a) Pop the top item from stack.
                i, depth = stack.pop()

                # b) Print the popped item, set current = popped_item->right
                yield self._nodes[i], depth
                i = self.get_right_index(i)
                depth += 1

                # c) Go to step 3.

            # 5) If current is NULL and stack is empty then we are done.
            else:
                return




        node = self._nodes[0]

    def pre_order_traversal(self):
        """
        Yields an pre-order traversal of this tree's nodes.

        :yield: Pre-order traversal of this tree's nodes.
        """

        # 1. Create a Stack.
        stack = []

        i = 0
        depth = 0

        # 2. Print the root and push it to Stack and go left i.e root=root.left and till it hits the NULL.
        while True:
            while i < len(self._nodes):
                yield self._nodes[i], depth
                stack.append((i, depth))
                i = self.get_left_index(i)
                depth += 1

            # 3. If root is null and Stack is empty Then done
            if not len(stack):
                return

            # 4. Else
            # a) Pop the top Node from the Stack and set it as, root = popped_Node.
            i, depth = stack.pop()

            # b) Go right, root = root.right.
            i = self.get_right_index(i)

            # c) Go to step 2.


    def post_order_traversal(self):
        """
        Yields an post-order traversal of this tree's nodes.

        :yield: Post-order traversal of this tree's nodes.
        """

        for node, depth in reversed(list(self.pre_order_traversal())):
            yield node, depth

    def level_order_traversal(self):
        """
        Yields a level-order traversal of this tree's nodes.

        :yield: Level-order traversal of this tree's nodes.
        """
        if not self._nodes:
            return

        # Yield root
        yield self._nodes[0], 0

        depth = 0

        for i in range(1, len(self._nodes)):
            if (i + 1) % 2 == 0:
                depth += 1
            yield self._nodes[i], depth

    def keys(self):
        """
        Returns an iterator over the keys in this tree.
        :return: Iterator over keys.
        """

        for node, depth in self.in_order_traversal():
            yield node.key

    def values(self):
        """
        Returns an iterator over the associated values in this tree.
        :return: Iterator over associated values.
        """

        for node, depth in self.in_order_traversal():
            yield node.value

    def items(self):
        """
        Returns an iterator over the key, value pairs in this tree.
        :return: Iterator over key, value pairs.
        """

        for node, depth in self.in_order_traversal():
            yield node.key, node.value

    def copy(self):
        """
        Returns a deepcopy of this PriorityQueue.
        :return: New PriorityQueue.
        """

        tree = PriorityQueue()

        for node in self.level_order_traversal():
            tree._nodes.append(node)

        return tree

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        yield from self.keys()

    def __repr__(self):
        return "PriorityQueue({!r})".format(tuple(node.key for node in self))

    def __str__(self):
        if self._nodes:
            return "\n".join(reversed(['\t' * d + str(n) for n, d in self.in_order_traversal()]))
        else:
            return "<empty>"

    def insert(self, key, value=None):
        i = len(self._nodes)
        self._nodes.append(BinaryHeapNode(key, value))

        while True:
            if i == 0:
                return

            parent_i = self.get_parent_index(i)

            if self._nodes[i].key > self._nodes[parent_i].key:
                return
            else:
                # swap
                self._nodes[i], self._nodes[parent_i] = self._nodes[parent_i], self._nodes[i]
                i = parent_i

    def delete_min(self):
        root = self._nodes[0]

        rightmost_leaf = self._nodes.pop(-1)

        if len(self._nodes) > 1:
            self._nodes[0] = rightmost_leaf

            i = 0

            while True:
                left_i, right_i = self.get_child_indices(i)
                if left_i >= len(self._nodes):
                    break

                has_left_child = left_i < len(self._nodes)
                has_right_child = right_i < len(self._nodes)
                if has_left_child:
                    left_child = self._nodes[left_i]
                if has_right_child:
                    right_child = self._nodes[right_i]
                u = self._nodes[i]
                if (not has_left_child or u.key < left_child.key) and (not has_right_child or u.key < right_child.key):
                    break

                if not has_right_child or left_child.key < right_child.key:
                    # left child is smaller
                    v_i = left_i
                else:
                    # right child is smaller
                    v_i = right_i

                self._nodes[v_i], self._nodes[i] = self._nodes[i], self._nodes[v_i]
                i = v_i

        return root.key, root.value

from utility import generate_unique_random
def main():
    #keys = generate_unique_random(20, 100)
    #print(keys)
    keys = [10, 50, 11, 38, 13, 87, 71, 55, 22, 23, 4, 58, 5, 62, 6, 59, 46, 83, 20, 31]

    pq = PriorityQueue()

    for key in keys:
        pq.insert(key)

    print(pq)

    for node, depth in pq.post_order_traversal():
        print(node, depth)

    for key in keys:
        print(pq.delete_min())


import time
if __name__ == "__main__":
    # Hack to synchronize stderr & stdout in Pycharm
    try:
        main()
    except Exception as e:
        time.sleep(0.1)
        raise e






