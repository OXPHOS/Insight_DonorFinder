class linkedListNode(object):
    '''
    Node of doubly linked list
    Stores one record of donation amount,
    and the smaller and larger donation 
    to one recipient in one area (with the same zip code)
    
    :param val: float, donation amount
    :param left: LinkedListNode object, with the donation smaller than self.val
    :param right: LinkedListNode object, with the donation larger than self.val
    
    '''
    def __init__(self, val, left = None, right = None):
        self.left = left
        self.right = right
        self.val = val

    def __repr__(self):
        return str(self.val)

    @staticmethod
    def insert_linkedlist_node(self, old_node, new_node, direction):
        '''
        :param old_node: LinkedListNode object, 
            the donation node already in doubly linked list
        :param new_node: LinkedListNode object, 
            the new donation amount to be added to the linked list
        :param direction: string, stores the moving trend of the new node
            by comparing the new_node.val to old_node.val
            'r': new_node.val > old_node.val
            'l': new_node.val < old_node.val

        '''
        if direction not in ['l', 'r']:
            raise ValueError('Undifined argument value: direction')

        if old_node.val > new_node.val:
            # if reaches the leftmost and
            # new_node.val is the smallest of the linked list
            if not old_node.left:
                old_node.left, new_node.right = new_node, old_node

            # old_node.left.val < new_node.val but old_node.value > new_node.value
            elif direction == 'r':
                old_node.left.right, new_node.left = new_node, old_node.left
                old_node.left, new_node.right = new_node, old_node

            # old_node.left.val > new_node.val and old_node.value > new_node.value
            else:
                self.insert_linkedlist_node(old_node.left, new_node, 'l')
        else:
            # reaches the rightmost and
            # new_node.val is the largest of the linked list
            if not old_node.right:
                old_node.right, new_node.left = new_node, old_node

            # old_node.right.val > new_node.val but old_node.value < new_node.value
            elif direction == 'l':
                old_node.right.left, new_node.right = new_node, old_node.left
                old_node.right, new_node.left = new_node, old_node

            # old_node.right.val < new_node.val and old_node.value < new_node.value
            else:
                self.insert_linkedlist_node(old_node.right, new_node, 'r')
