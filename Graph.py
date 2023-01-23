from dataclasses import dataclass

from Wrapper import Wrapper


@dataclass
class NodeData:
    city: dict = None
    sex: dict = None
    country: dict = None
    last_name: dict = None


class Node:
    central_fr = dict()  # Центральные вершины
    _all: NodeData = NodeData()

    def __init__(self, man: Wrapper):
        self._id = man.id

        city = man.city
        if city:
            self._city = city.title
        else:
            self._city = None

        self._universities = man.universities[0] if man.universities else None

        self._sex = man.sex
        self._first_name = man.first_name
        self._last_name = man.last_name

        self._is_closed = man.is_closed
        self._status = man.status

        self._friends = set()

        Node.central_fr.update({int(self._id): self})

    def update_friends(self, ids: set):
        self._friends.update(set(ids))

    def get_friends(self):
        return self._friends

    @staticmethod
    def get_likely_item(item: str, num: int = 3):
        all_item = getattr(Node._all, item)
        return sorted(list(all_item.items()), key=lambda x: x[1], reverse=True)[:num]

    @staticmethod
    def update_likely_item(items: tuple = ("city", "last_name", "sex")):
        for item in items:
            my_items = dict()
            for node in Node.central_fr.values():  # проходим по всем друзьям
                name = str(node.get_item('_' + item)).replace('ё', 'е')  # имя атрибута

                if item == 'last_name':
                    if name and name != 'None':
                        if node.get_item('sex') == 1:  # стандартизация фамилий
                            if len(name) > 1 and name[-2:] in ('ва', 'на'):
                                name = name[:-1]

                        pr_value = my_items.get(name, 0)  # значение этого атрибута у вершины
                        my_items.update({name: pr_value + 1})  # увеличиваю значение этого имени в словаре
                else:
                    if name and name != 'None':
                        pr_value = my_items.get(name, 0)  # значение этого атрибута у вершины
                        my_items.update({name: pr_value + 1})  # увеличиваю значение этого имени в словаре

            setattr(Node._all, item, my_items)

    def get_is_open(self):
        return not bool(self._is_closed)

    def get_item(self, item: str, default=None):
        if item[0] != '_':
            item = '_' + item

        if not hasattr(self, item):
            return default

        return getattr(self, item)

    def set_item(self, item: str, value):
        setattr(self, item, value)

    @staticmethod
    def clear():
        for node in Node.central_fr:
            t = Node.central_fr.get(node)
            del t

        Node.central_fr = dict()  # Центральные вершины
        Node._all = NodeData()

    @staticmethod
    def get_university(uni_items: tuple = ('name', 'education_status'), num: int = 3):
        all_items = dict()
        for item in uni_items:
            my_items = dict()
            for node in Node.central_fr.values():  # проходим по всем друзьям
                if node.get_item('universities'):
                    name = node.get_item('universities').get(item)
                    if name:
                        pr_value = my_items.get(name, 0)  # значение этого атрибута у вершины
                        my_items.update({name: pr_value + 1})  # увеличиваю значение этого имени в словаре

            all_items.update({item: sorted(list(my_items.items()), key=lambda x: x[1], reverse=True)[:num]})
        return all_items
