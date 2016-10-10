# Algorithms & Data Structures

Implementations of Intermediate Algorithms & Data Structures, many of which are taught in COMP3506/COMP7505 at the University of Queensland.
http://staff.itee.uq.edu.au/taoyf/course/comp3506/www/

## AVL Tree
[avl_tree.py](avl_tree.py)

Maps distinct, orderable keys to optional values.

* Space: O(n)
* Time:
    - Get Item: O(log n)
    - Set Item/Insert: O(log n)
    - Delete Item/Remove: O(log n)
    - Existence of Item (key in tree): O(log n)
    - Get Length: O(1)
    - Iteration: O(n)
    - Copy: O(n)

See
* http://staff.itee.uq.edu.au/taoyf/course/comp3506/lec/bst.pdf
* http://staff.itee.uq.edu.au/taoyf/course/comp3506/lec/avl.pdf
* https://www.cs.usfca.edu/~galles/visualization/AVLtree.html

## Binary Search
[binary_search.py](binary_search.py)
Finds index of element in sorted iterable in O(log n) time.

http://staff.itee.uq.edu.au/taoyf/course/comp3506/lec/bin-srch-worst-analysis.pdf

## Priority Queue with Binary Heap
[binary_heap.py](binary_heap.py)

Stores a set of totally ordered keys (with optional associated values), and
supports insert & delete-min operations.

* Space: O(n)
* Time:
    - Insert: O(log n)
    - Delete-min: O(log n)

See
* http://staff.itee.uq.edu.au/taoyf/course/comp3506/lec/pq.pdf
* http://staff.itee.uq.edu.au/taoyf/course/comp3506/lec/pq-array.pdf