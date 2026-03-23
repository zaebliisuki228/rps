from typing import List, Optional


class TreeNode:
    """Узел бинарного дерева поиска"""
    
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class TreeSorter:
    """Класс для сортировки методом дерева"""
    
    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        
        if not arr:
            return []
        
        # Строим дерево
        root = TreeNode(arr[0])
        for value in arr[1:]:
            TreeSorter._insert_node(root, value)
        
        # Обходим дерево в порядке возрастания
        result = []
        TreeSorter._inorder_traversal(root, result)
        
        return result
    
    @staticmethod
    def _insert_node(node: TreeNode, value: int) -> None:
    
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                TreeSorter._insert_node(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                TreeSorter._insert_node(node.right, value)
    
    @staticmethod
    def _inorder_traversal(node: Optional[TreeNode], result: List[int]) -> None:
        
        if node is None:
            return
        
        TreeSorter._inorder_traversal(node.left, result)
        result.append(node.value)
        TreeSorter._inorder_traversal(node.right, result)
