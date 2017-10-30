class LinkedListNode(object):
    """
    Node of doubly linked list
    Stores one record of donation amount,
    and the smaller and larger donation 
    to one recipient in one area (with the same zip code)
    
    :param val: float, donation amount
    :param left: LinkedListNode object, with the donation smaller than self._val
    :param right: LinkedListNode object, with the donation larger than self._val
    
    """
    def __init__(self, val, left=None, right=None):
        self.left = left
        self.right = right
        self._val = val

    def __repr__(self):
        """
        :return: transaction amount 
        """
        return str(self._val)

    def get_value(self):
        """
        :return: transaction amount 
        """
        return self._val

    @staticmethod
    def insert_linkedlist_node(old_node, new_node, direction):
        """
        :param old_node: LinkedListNode object, 
            the donation node already in doubly linked list
        :param new_node: LinkedListNode object, 
            the new donation amount to be added to the linked list
        :param direction: string, stores the moving trend of the new node
            by comparing the new_node._val to old_node._val
            'r': new_node._val > old_node._val
            'l': new_node._val < old_node._val
        
        """
        # TODO: exit in cyclic linked list
        if direction not in ['l', 'r']:
            raise ValueError('Undefined argument value: direction')

        if not new_node.get_value():
            raise TypeError("One or more nodes are invalid")

        while True:
            if old_node.get_value() < new_node.get_value():
                # reaches the rightmost and
                # new_node._val is the largest of the linked list
                if not old_node.right:
                    old_node.right, new_node.left = new_node, old_node
                    break

                # old_node.right._val > new_node._val but old_node._val < new_node._val
                elif direction == 'l':
                    old_node.right.left, new_node.right = new_node, old_node.right
                    old_node.right, new_node.left = new_node, old_node
                    break

                # old_node.right._val < new_node._val and old_node._val < new_node._val
                # keep search by moving to right
                else:
                    old_node = old_node.right
            else:
                # if reaches the leftmost and
                # new_node._val is the smallest of the linked list
                if not old_node.left:
                    old_node.left, new_node.right = new_node, old_node
                    break

                # old_node.left._val < new_node._val but old_node._val > new_node._val
                elif direction == 'r':
                    old_node.left.right, new_node.left = new_node, old_node.left
                    old_node.left, new_node.right = new_node, old_node
                    break

                # old_node.left._val > new_node._val and old_node._val > new_node._val
                # keep searching my moving to left
                else:
                    old_node = old_node.left

