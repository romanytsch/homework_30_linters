"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    node_map = {}

    # Регулярные выражения для парсинга лога
    visit_re = re.compile(r"INFO:Visiting <BinaryTreeNode\[(\d+)\]>")
    left_re = re.compile(
        r"DEBUG:<BinaryTreeNode\[(\d+)\]> left is not empty. Adding <BinaryTreeNode\[(\d+)\]> to the queue")
    right_re = re.compile(
        r"DEBUG:<BinaryTreeNode\[(\d+)\]> right is not empty. Adding <BinaryTreeNode\[(\d+)\]> to the queue")

    root_value = None

    with open(path_to_log_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        visit_match = visit_re.match(line)
        if visit_match:
            node_val = int(visit_match.group(1))
            if node_val not in node_map:
                node_map[node_val] = BinaryTreeNode(node_val)
            if root_value is None:
                root_value = node_val
            continue

        left_match = left_re.match(line)
        if left_match:
            parent_val = int(left_match.group(1))
            left_val = int(left_match.group(2))
            if parent_val not in node_map:
                node_map[parent_val] = BinaryTreeNode(parent_val)
            if left_val not in node_map:
                node_map[left_val] = BinaryTreeNode(left_val)
            node_map[parent_val].left = node_map[left_val]
            continue

        right_match = right_re.match(line)
        if right_match:
            parent_val = int(right_match.group(1))
            right_val = int(right_match.group(2))
            if parent_val not in node_map:
                node_map[parent_val] = BinaryTreeNode(parent_val)
            if right_val not in node_map:
                node_map[right_val] = BinaryTreeNode(right_val)
            node_map[parent_val].right = node_map[right_val]
            continue

    return node_map[root_value]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="restore_log.txt",
    )

    root = get_tree(7)
    walk(root)
