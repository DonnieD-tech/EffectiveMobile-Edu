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



def test_add_and_get_data():
    lst = LinkedList()
    lst.add_obj(ObjList('данные 1'))
    lst.add_obj(ObjList('данные 2'))
    lst.add_obj(ObjList('данные 3'))
    assert lst.get_data() == ['данные 1', 'данные 2', 'данные 3']
    print(f"{} passed")


def test_remove_last_element():
    lst = LinkedList()
    lst.add_obj(ObjList('one'))
    lst.add_obj(ObjList('two'))
    lst.remove_obj()
    assert lst.get_data() == ['one']
    print("✅ test_remove_last_element passed")


def test_remove_until_empty():
    lst = LinkedList()
    lst.add_obj(ObjList('single'))
    lst.remove_obj()
    assert lst.get_data() == []
    assert lst.head is None
    assert lst.tail is None
    print("✅ test_remove_until_empty passed")


def test_remove_from_empty():
    lst = LinkedList()
    lst.remove_obj()  # ничего не должно упасть
    assert lst.get_data() == []
    print("✅ test_remove_from_empty passed")


def test_node_links():
    node1 = ObjList('A')
    node2 = ObjList('B')
    node1.set_next(node2)
    node2.set_prev(node1)
    assert node1.get_next() == node2
    assert node2.get_prev() == node1
    assert node1.get_data() == 'A'
    node1.set_data('X')
    assert node1.get_data() == 'X'
    print("✅ test_node_links passed")


# Запуск всех тестов
test_add_and_get_data()
test_remove_last_element()
test_remove_until_empty()
test_remove_from_empty()
test_node_links()
