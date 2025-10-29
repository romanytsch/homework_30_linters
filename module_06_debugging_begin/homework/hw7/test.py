import unittest
from binary_tree_walk import restore_tree

def get_node_value(node):
    return node.val if node else None

# Предположим, что функция restore_tree уже объявлена
class TestRestoreTree(unittest.TestCase):

    def test_basic_tree(self):
        root = restore_tree("test_log.txt")
        self.assertEqual(get_node_value(root), 1)
        self.assertEqual(get_node_value(root.left), 2)
        self.assertEqual(get_node_value(root.right), 3)
        self.assertEqual(get_node_value(root.left.left), 4)
        self.assertEqual(get_node_value(root.left.right), 5)
        self.assertIsNone(root.right.left)
        self.assertIsNone(root.right.right)

if __name__ == "__main__":
    unittest.main()