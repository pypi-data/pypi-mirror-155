class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def add_node_at_head(self, element):
        node = Node(element)
        if self.head is None:
            self.head = node
            return
        
        node.next = self.head
        self.head = node
    
    def add_node_at_tail(self, element):
        node = Node(element)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node
    
    def add_node_before_element(self, item, element):
        try:
            if self.head is not None:
                if self.head.data == item:
                    node = Node(element)
                    node.next = self.head
                    self.head = node
                    return
                current = self.head
                while current.next:
                    if current.next.data == item:
                        break
                    current = current.next
                if current.next is None:
                    raise ValueError("{} not exists in the linkedlist".format(item))
                else:
                    node = Node(element)
                    node.next = current.next
                    current.next = node
        except ValueError as e:
            print(e)
    
    def add_node_after_element(self, item, element):
        try:
            if self.head is not None:
                if self.head.data == item:
                    node = Node(element)
                    node.next = self.head.next
                    self.head.next = node
                    return
                current = self.head
                while current:
                    if current.data == item:
                        break
                    current = current.next
                if current is None:
                    raise ValueError("{} not exists in the linkedlist".format(item))
                else:
                    node = Node(element)
                    node.next = current.next
                    current.next = node
        except ValueError as e:
            print(e)
    
    def delete_at_begin(self):
        try:
            if self.head is None:
                raise ValueError("List should not be empty")
            self.head = self.head.next
            return
        except ValueError as e:
            print(e)
    
    def pop(self, element=None):
        try:
            if self.head is None:
                raise ValueError("List should not be empty")
            if element is None:
                if self.head.next is None:
                    self.head = None
                    return
                current = self.head
                while current.next.next:
                    current = current.next
                current.next = None
            else:
                if self.head.data == element:
                    self.head = self.head.next
                    return
                current = self.head
                while current.next:
                    if current.next.data == element:
                        break
                    current = current.next
                if current.next is None:
                    raise ValueError("{} not exists in the linkedlist".format(element))
                current.next = current.next.next
        except ValueError as e:
            print(e)
                
                

    def length(self):
        size = 0
        current = self.head
        while current:
            size += 1
            current = current.next
        return size

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end='->')
            current = current.next

l = LinkedList()
l.print_list()
