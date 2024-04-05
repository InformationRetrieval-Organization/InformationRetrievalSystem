class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while(current_node.next):
            current_node = current_node.next
        current_node.next = new_node
            
    def insertSorted(self, data):
        new_node = Node(data)
        if self.is_empty() or self.data >= new_node.data: # if the list is empty or the data is smaller than the head
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next != None and current.next.data < new_node.data: # find the right position to insert
                current = current.next
                if current.data == new_node.data:   # if the data is already in the list, don't insert it again
                    return
            new_node.next = current.next
            current.next = new_node

    def delete(self, data):
        if self.is_empty():
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()
        