import graphviz as gz
from Graph import Node


class Graph(gz.Graph):
    def __init__(self, *atr, **kwargs):
        super().__init__(*atr, **kwargs)
        self._central = ''   # id центральной вершины

    def create_central_node(self, t: dict):
        user_id = str(t.get('id'))
        last_name = t.get('last_name', '')
        first_name = t.get('first_name', '')
        name = last_name + ' ' + first_name

        self._central = str(user_id)
        self.node(user_id, name)

    def update_node(self, t: Node):
        idt = str(t.get_item('id'))
        last_name = str(t.get_item('last_name', ''))
        first_name = str(t.get_item('first_name', ''))
        name = last_name + ' ' + first_name
        self.node(idt, name)

        self.edge(idt, self._central)

    def set_edge(self, user_id: str, friends: set, t):
        my_set = friends.intersection(set(t.central_fr.keys()))
        for idt in my_set:
            self.edge(str(idt), str(user_id))

    def my_view(self, directory='graph-output', view=True, engine='fdp'):
        return self.render(directory=directory, view=view, engine=engine, format='png').replace('\\', '/')


if __name__ == "__main__":
    pass
