class Deque():

    def __init__(self):
        self.__items = []

    def is_empty(self):
        return self.__items == []

    def add_front(self, item):
        self.__items.append(item)

    def add_rear(self, item):
        self.__items.insert(0, item)

    def remove_front(self):
        return self.__items.pop()

    def remove_rear(self):
        return self.__items.pop(0)

    def size(self):
        return len(self.__items)
