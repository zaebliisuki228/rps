"""
Модуль реализации сортировки деревом (Tree Sort)
Алгоритм: построение бинарного дерева поиска и симметричный обход
"""

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
        """
        Сортировка массива методом дерева
        """
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
    def sort_with_stats(arr: List[int]) -> tuple[List[int], dict]:
        """
        Сортировка с подсчетом статистики
        
        Returns:
            (отсортированный_массив, статистика)
        """
        result = arr.copy()
        
        if len(result) <= 1:
            return result, {'comparisons': 0, 'insertions': 0, 'nodes': 0}
        
        comparisons = 0  # количество сравнений
        insertions = 0   # количество вставок
        
        # Строим дерево с подсчетом сравнений
        root = TreeNode(result[0])
        insertions += 1
        
        for value in result[1:]:
            comparisons += TreeSorter._insert_node_with_stats(root, value)
            insertions += 1
        
        # Обходим дерево
        sorted_result = []
        TreeSorter._inorder_traversal(root, sorted_result)
        
        statistics = {
            'comparisons': comparisons,
            'insertions': insertions,
            'nodes': insertions  # количество узлов равно количеству вставок
        }
        
        return sorted_result, statistics
    
    @staticmethod
    def _insert_node(node: TreeNode, value: int) -> None:
        """Вставка узла в дерево"""
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
    def _insert_node_with_stats(node: TreeNode, value: int) -> int:
        """
        Вставка узла с подсчетом сравнений
        Returns:
            количество выполненных сравнений
        """
        comparisons = 1  # одно сравнение value < node.value
        
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                comparisons += TreeSorter._insert_node_with_stats(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                comparisons += TreeSorter._insert_node_with_stats(node.right, value)
        
        return comparisons
    
    @staticmethod
    def _inorder_traversal(node: Optional[TreeNode], result: List[int]) -> None:
        """Симметричный обход дерева"""
        if node is None:
            return
        
        TreeSorter._inorder_traversal(node.left, result)
        result.append(node.value)
        TreeSorter._inorder_traversal(node.right, result)
    
    @staticmethod
    def is_sorted(arr: List[int]) -> bool:
        """Проверяет, отсортирован ли список"""
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True


# Для удобства импорта
tree_sort = TreeSorter.sort
tree_sort_with_stats = TreeSorter.sort_with_stats
is_sorted = TreeSorter.is_sorted
