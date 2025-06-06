class ObjList:
    def __init__(self, data):
        self.__next = None
        self.__prev = None
        self.__data = data


    def set_next(self, obj):
        self.__next = obj


    def set_prev(self, obj):
        self.__prev = obj


    def get_next(self):
        return self.__next


    def get_prev(self):
        return self.__prev


    def set_data(self, data):
        self.__data = data


    def get_data(self):
        return self.__data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None


    def add_obj(self, obj):
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj


    def remove_obj(self):
        if self.tail is None:
            return

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            prev = self.tail.get_prev()
            prev.set_next(None)
            self.tail = prev


    def get_data(self):
        data_list = []
        current_object = self.head
        while current_object:
            data_list.append(current_object.get_data())
            current_object = current_object.get_next()
        return data_list

