import configparser
from collections.abc import Callable
from typing import Any

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod

from Wrapper import Wrapper
from Graph import Node
import graph_vie as gv
import Tkin


def load_config() -> Callable[[str], Any]:
    parser = configparser.ConfigParser()
    parser.read('AHTUNG.txt')
    config = lambda key: (parser.get('DEFAULT', key))
    return config


def get_api(config=load_config()) -> VkApiMethod:
    session = VkApi(login=config('login'), password=config('password'))
    session.auth()

    vk = session.get_api()
    return vk


def create_graph(vk: VkApi.get_api, dot: gv.Graph, user_id: str):
    """
    Создает граф в dot для визуализации и в Nod для подсчета статистики
    :param vk: экземпляр сессии вк
    :param dot: экземпляр класса граф из graphviz
    :param user_id: id человека, по которому собирается информация
    :return: Node: Node
    """
    # запрашиваем друзей человека с определенными сведениями
    friends = Wrapper(vk.friends.get(user_id=user_id, fields='city,country,sex,universities'))

    # создаем центральную вершину в графе
    dot.create_central_node(vk.users.get(user_ids=str(user_id), fields='last_name', strict=True)[0])

    Node.clear()

    for man in friends.items:
        if not man.get('deactivated'):
            t = Node(man)
            dot.update_node(t)

            if t.get_is_open():
                friend = Wrapper(vk.friends.get(user_id=man.id))
                t.update_friends(friend.items.set())
                dot.set_edge(t.get_item('id'), t.get_friends(), t)

    Node.update_likely_item()

    return Node


def main():
    def show_graph(dot: gv.Graph):
        return dot.my_view()

    def to_go_info(item: str, num: int = 5, gr=None):
        """
        Функция возвращает список длиной num наиболее часто встречающихся значений
        атрибута item у каждой вершины класса gr. Также канонизирует значение.
        :param item: имя атрибута
        :param num: количество элементов в итоговом списке
        :param gr: класс Node
        :return: list: длинной num с максимальными значениями атрибута item вершин класса gr
        """

        gr.update_likely_item()
        if item in ('last_name', 'city'):
            return gr.get_likely_item(item, num=num)
        elif item in ('education', 'university'):
            info = gr.get_university(num=num)
            if item == 'education':
                return info.get('education_status')
            else:
                def func_canonize(b):
                    a = b[0] + '\t\r\n-('
                    a = a[:min(a.index('\r'), a.index('\n'), a.index('-'), a.index('('), a.index('\t'))]
                    a = a.replace('Первый', '')
                    return tuple((a, b[1]))

                name = info.get('name')
                name = list(map(func_canonize, name))
                return name

    def info_func(user_id: str):
        """
        Функция возвращает словарь анс с основной информацией о пользователе с user_id
        :param user_id: id основного пользователя
        :return: dict: словарь основной информации о нем
        """
        try:
            all_info = Wrapper(vk.users.get(user_ids=str(user_id), fields='last_name,city')[0])
        except:
            return -1

        ans = dict()
        items = ['first_name', 'last_name', 'city']
        for item in items:
            ans.update({item: all_info.get_item(item, 'Не известно')})
        return ans

    def start(user_id: str):
        dot = gv.Graph('USER GRAPH', comment='table friends', format='png', engine='fdp')  # создаем граф viz
        gr = create_graph(vk, dot, user_id)  # создаем граф для подсчета
        return dot, gr

    try:
        vk = get_api()  # Начинаем сессию с вк
    except:
        print('Проверьте соединение!')
        return

    app = Tkin.start(info_func=info_func, create_gr=start, to_go_func=to_go_info, show_func=show_graph)
    app.mainloop()


if __name__ == '__main__':
    main() 