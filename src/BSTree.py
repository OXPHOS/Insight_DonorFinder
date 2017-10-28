class nodeBase(object):
    """
    Base class that saves node information of self balanced binary search tree
    
    :param left: object of NodeBase or derived, left child of the node
    :param right: object of NodeBase or derived, right child of the node
    :param key_idx: generic, the key used for comparison
    :param height: int, the height of the node in the tree
    
    """
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        self.key_idx = None
        self.val = None
        self.height = 0

    def output(self):
        """
        :return: key | val.output()
        """
        return self.key + '|' + self.val.output()

    def __eq__(self, other):
        return self.key_idx == other.key_idx

    def __ne__(self, other):
        return self.key_idx != other.key_idx

    def __gt__(self, other):
        return self.key_idx > other.key_idx

    def __ge__(self, other):
        return self.key_idx >= other.key_idx

    def __lt__(self, other):
        return not self.key_idx <= other.key_idx

    def __le__(self, other):
        return not self.key_idx <= other.key_idx

class nodeID(nodeBase):
    """
    Structure that saves information of each recipient
        - self.key: string, id Cxxxxxxxxx
        - self.key_idx: int, extracted from self._key to simplify comparison
        - self.val: self-balanced binary search tree that saves donation
            information to specific recipient grouped by transaction date
              
    :param id: string, id of the recipient
    :param date: FECDate, transaction date, to construct nested tree
    :param info_by_date: object of InfoByDate, with information of median, count, 
        and total, to construct nested tree
    :param left: object of NodeBase or derived, left child of the node
    :param right: object of NodeBase or derived, right child of the node
    """
    def __init__(self, id, date, info_by_date, left=None, right=None):
        nodeBase.__init__(self, left, right)
        self.key = id
        self.key_idx = int(self._key[1:])
        self.val = BSTree(nodeDate(date, info_by_date))

    def update_node(self, node):
        """
        When a transaction date exists for specific recipient, 
        update the nested tree constructed from the date
        :param node: object of NodeID, the donation information to be added 
        """
        self.val.update_tree(node.val)

class nodeDate(nodeBase):
    """
    Structure that saves donation information from different dates 
    to specific recipient 
        - self.key: FECDate
        - self.key_idx: FECDate
        - self.val: object of infoByDate, saves median, count and total information

    :param date: FECDate, transaction date, to construct nested tree
    :param info_by_date: object of InfoByDate, with information of median, count, 
        and total, to construct nested tree
    :param left: object of NodeBase or derived, left child of the node
    :param right: object of NodeBase or derived, right child of the node
    """
    def __init__(self, date, info_by_date, left=None, right=None):
        nodeBase.__init__(self, left, right)
        self.key = date
        self.key_idx = date
        self.val = info_by_date

    def update_node(self, node):
        self.val = node.val

class BSTree(object):
    """
    A self-balanced binary search tree for rapid insertion of new donation info
    """
    def __init__(self, root=None):
        self.root = root

    def height(self, node):
        """
        :param node: nodeBase or derived type 
        :return: int, height of the node
        """
        if node:
            return node.height
        else:
            return -1

    def update_tree(self, node):
        """
        Insert a new node to the tree
        
        :param node: nodeBase or derived type 
        """
        if self.root:
            self.root = self._update_tree(self.root, node)
        else:
            self.root = node

    def output_tree_inorder(self):
        """
        Output the tree from smallest node to largest node
        
        :return: id|transaction date|median|count|total
        """
        node = self.root
        yield self._output_tree_inorder(node)

    def _output_tree_inorder(self, node):
        """
        Implementation of recursive in-order traversal of the tree
        output the tree from smallest node to largest node
        
        :return: id|transaction date|median|count|total
        """
        if not node:
            return
        self._output_tree_inorder(node.left)
        yield node.output()
        self._output_tree_inorder(node.right)

    def _single_left_rotate(self, node):
        """
        switch -  to:
        parent - right child,
        left child - parent,
        left grandchild - left child
        """
        tmp = node.left
        node.left = tmp.right
        tmp.right = node
        node.height = max(self.height(node.right),self.height(node.left))+1
        tmp.height = max(self.height(tmp.left),node.height)+1
        return tmp

    def _single_right_rotate(self, node):
        """
        switch -  to:
        parent - left child,
        right child - parent,
        right grandchild - right child
        """
        tmp = node.right
        node.right = tmp.left
        tmp.left = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        tmp.height = max(self.height(tmp.right), node.height) + 1
        return tmp

    def _double_left_rotate(self, node):
        """
        switch -  to:
        parent - right child,
        left child - left child,
        right grandchild - parent
        """
        node.left=self._single_right_rotate(node.left)
        return self._single_left_rotate(node)

    def _double_right_rotate(self, node):
        """
        switch -  to:
        parent - left child,
        right child - right child,
        left grandchild - parent
        """
        node.right = self._single_left_rotate(node.right)
        return self._single_right_rotate(node)


    def _update_tree(self, node, new_node):
        """
        Implementation of node insertion

        :param node: nodeBase or derived type, the parent node
        :param new_node: nodeBase or derived type, the new node to be added 
        """
        if new_node < node:
            node.left = self._update_tree(node.left, new_node)
            # if the added node results in height in-balance: turn the nodes
            if (self.height(node.left) - self.height(node.right)) == 2:
                if new_node < node.left:
                    node = self._single_left_rotate(node)
                else:
                    node = self._double_left_rotate(node)
        elif new_node > node:
            node.right = self._update_tree(node.right, new_node)
            # if the added node results in height in-balance: turn the nodes
            if (self.height(node.right) - self.height(node.left)) == 2:
                if new_node < node.right:
                    node = self._double_right_rotate(node)
                else:
                    node = self._single_right_rotate(node)
        # if new_node == node: update median, count, and total information in-place
        else:
            node.update_node(new_node)

        # update the height of the (parent) node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        return node
