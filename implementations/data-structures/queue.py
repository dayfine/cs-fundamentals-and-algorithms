class Queue():

    def __init__(self):
        self.__items =[]

    def is_empty(self):
        return self.__items == []

    def enqeue(self, items):
        self.__items.insert(0, item)

    def dequeue(self):
        return self.__items.pop()

    def size(self):
        return len(self.__items)
