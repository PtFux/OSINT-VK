import tkinter as tk
import tkinter.font as tkf
from tkinter import messagebox

from collections.abc import Callable


class Application(tk.Frame):
    def __init__(
            self,
            master: tk.Tk = None,
            info_func: Callable[str] = None,
            to_go_func: Callable[str] = None,
            show_func: Callable[str] = None,
            create_gr: Callable[str] = None,
            base: int = 9
    ):
        super().__init__(master)
        self.master = master

        self._base = base

        self._fStyle = tkf.Font(family="Lucida Grande", size=12)

        self.info_func = info_func
        self.to_go_func = to_go_func
        self.show_func = show_func
        self.create_gr = create_gr
        self.widget = dict()

        self.start()

    def start(self):
        self.create_widgets()
        self.create_info()
        self.likely_info()
        self.create_butt_show()

    def create_widgets(self):
        self.master.title("Граф друзей в социальной сети VK")
        self.grid()

        self.plug(0)

        frame1 = tk.Frame(self)
        frame1.grid(row=1, column=0)
        self.widget.update({'Header': frame1})

        lbl1 = tk.Label(frame1, text="ID:", width=self._base, font=self._fStyle)
        lbl1.grid(row=1, column=0)

        name_id = tk.StringVar()
        entry = tk.Entry(frame1, width=int(2.5 * self._base), font=self._fStyle, textvariable=name_id)
        entry.grid(row=1, column=1)
        self.widget.update({'ID': name_id})

        name = " Имя:"
        lbl2 = tk.Label(frame1, text=name, width=len(name), font=self._fStyle)
        lbl2.grid(row=1, column=2)

        last_name = "Фамилия:"
        lb3 = tk.Label(frame1, text=last_name, width=len(last_name), font=self._fStyle)
        lb3.grid(row=1, column=4)

        some = 4 * self._base * "_"
        lb2a = tk.Label(frame1, text=some, width=len(some), font=self._fStyle)
        lb2a.grid(row=1, column=3)
        self.widget.update({'first_name': lb2a})

        some = 4 * self._base * "_"
        lb3a = tk.Label(frame1, text=some, width=len(some), font=self._fStyle)
        lb3a.grid(row=1, column=5)
        self.widget.update({'last_name': lb3a})

        city = "Город:"
        lb3 = tk.Label(frame1, text=city, width=len(city), font=self._fStyle)
        lb3.grid(row=1, column=6)

        some = 4 * self._base * "_"
        lb2a = tk.Label(frame1, text=some, width=len(some), font=self._fStyle)
        lb2a.grid(row=1, column=7)
        self.widget.update({'city': lb2a})

        text = "Инфо"
        to_go = tk.Button(frame1, text=text, command=self.clicked, font=self._fStyle)
        to_go.grid(row=1, column=9)
        self.widget.update({'to_go': to_go})

        text = "Запуск"
        to_go = tk.Button(frame1, text=text, command=self.clicked_go, font=self._fStyle)
        to_go.grid(row=1, column=10)
        self.widget.update({'to_go_info': to_go})

        text = "Clear"
        to_cl = tk.Button(frame1, text=text, command=self.clicked_cl, font=self._fStyle)
        to_cl.grid(row=1, column=11)
        self.widget.update({'to_cl': to_cl})

    def update_size(self, x: int, y: int):
        self.master.geometry(f'{x}x{y}')

    def create_info(self):
        frame = tk.Frame(self)
        frame.grid(row=2, column=0)

        info = 'Информация: '
        info_lb = tk.Label(frame, text=info, width=len(info), font=self._fStyle)
        info_lb.grid(row=2, column=1)

        self.plug(3)

        frame_inf = tk.Frame(self)
        frame_inf.grid(row=3, column=0)

        base = self._base ** 2

        name = "Фамилия"
        last_name = tk.Label(frame_inf, text=name, width=base, font=self._fStyle)
        last_name.grid(row=3, column=0)

        ans = tk.StringVar()
        spin = tk.Spinbox(frame_inf, from_=0, to=5, width=int(0.5 * self._base), font=self._fStyle, textvariable=ans)
        spin.grid(row=3, column=1)
        self.widget.update({'last_name_spin': ans})

        name = "Город"
        last_name = tk.Label(frame_inf, text=name, width=base, font=self._fStyle)
        last_name.grid(row=3, column=2)

        ans = tk.StringVar()
        spin = tk.Spinbox(frame_inf, from_=0, to=5, width=int(0.5 * self._base), font=self._fStyle, textvariable=ans)
        spin.grid(row=3, column=3)
        self.widget.update({'city_spin': ans})

        name = "Университет"
        last_name = tk.Label(frame_inf, text=name, width=base, font=self._fStyle)
        last_name.grid(row=3, column=4)

        ans = tk.StringVar()
        spin = tk.Spinbox(frame_inf, from_=0, to=5, width=int(0.5 * self._base), font=self._fStyle, textvariable=ans)
        spin.grid(row=3, column=5)
        self.widget.update({'university_spin': ans})

        name = "Форма обучения"
        last_name = tk.Label(frame_inf, text=name, width=base, font=self._fStyle)
        last_name.grid(row=3, column=6)

        ans = tk.StringVar()
        spin = tk.Spinbox(frame_inf, from_=0, to=5, width=int(0.5 * self._base), font=self._fStyle, textvariable=ans)
        spin.grid(row=3, column=7)
        self.widget.update({'education_spin': ans})

        all_items = ['last_name', 'city', 'university', 'education']

        for item in all_items:
            for i in range(5):
                name = '_' * base
                name_it = tk.Label(frame_inf, text=name, width=base, font=self._fStyle)
                name_it.grid(row=4 + i, column=all_items.index(item) * 2)
                self.widget.update({f'lab_{item}_{i}': name_it})

    def clicked(self):
        def table_user():
            info = self.info_func(self.widget.get('ID').get())
            if info == -1:
                self.show_message("Неверный ID")
                return
            items = ('first_name', 'last_name', 'city')
            for item in items:
                self.widget.get(item).config(text=info.get(item))
            return self.widget.get("ID").get()

        def table_info():
            def func(item: str):
                num = min(int(self.widget.get(f'{item}_spin').get()), 5)
                if self.widget.get('gr'):
                    ans = self.to_go_func(item, max(num, 1), self.widget.get('gr'))

                    item_max = item
                    if ans and ans[0]:
                        item_max = ans[0][0]

                    for i in range(min(num, len(ans))):
                        self.widget.get(f'lab_{item}_{i}').config(text=f'{ans[i][0]} - {ans[i][1]}')

                    for i in range(min(num, len(ans)), 5):
                        self.widget.get(f'lab_{item}_{i}').config(text=self._base ** 2 * '_')

                    self.widget.get(f'lab_{item}_ans').config(text=item_max)

            all_items = ['last_name', 'city', 'university', 'education']
            for item in all_items:
                func(item)

        self.clicked_cl()
        user_id = table_user()

        if not user_id:
            return

        table_info()

    def clicked_go(self):
        def info_user_id():
            if self.info_func:
                info = self.info_func(self.widget.get('ID').get())
                if info == -1:
                    self.show_message("Неверный ID")
                    return
            return self.widget.get('ID').get()

        user_id = info_user_id()
        if user_id is None:
            return

        if not user_id.isdigit():
            self.show_message('ID должен быть числовым!')
            return

        dot, gr = self.create_gr(user_id)

        self.widget.update({'dot': dot})

        self.widget.update({'gr': gr})

        self.clicked()

    def likely_info(self):
        self.plug(9)

        frame = tk.Frame(self)
        frame.grid(row=10, column=0)

        base = self._base ** 2

        all_items = ['Likely info: ', 'last_name', 'city', 'university', 'education']

        for item in all_items:
            name_it = tk.Label(frame, text=item, width=base, font=self._fStyle)
            name_it.grid(row=10, column=all_items.index(item) * 2)
            self.widget.update({f'lab_{item}_ans': name_it})

        self.plug(11)

    def create_butt_show(self):
        frame = tk.Frame(self)
        frame.grid(row=12, column=0)

        show_but = tk.Button(frame, text="Показать граф", command=self.show_graph, font=self._fStyle)
        show_but.grid(row=12, column=1)

        self.widget.update({'show': show_but})

        show_but = tk.Button(frame, text="Создать файл", command=self.show_file, font=self._fStyle)
        show_but.grid(row=12, column=3)

        self.widget.update({'show': show_but})

        self.plug(13)

    def show_graph(self):
        if self.widget.get('dot'):
            try:
                return self.show_func(self.widget.get('dot'))
            except:
                self.show_message('Граф слишком большой!')

        self.show_message('Запустите программу!')

    def plug(self, n: int):
        frame = tk.Frame(self)
        frame.grid(row=n, column=0)

        one = tk.Label(frame)
        one.grid()

    def clicked_cl(self):
        all_items = ['last_name', 'city', 'university', 'education']

        for item in all_items:
            for i in range(5):
                self.widget.get(f'lab_{item}_{i}').config(text=self._base ** 2 * '_')

        for item in all_items:
            self.widget.get(f'lab_{item}_ans').config(text=item)

        all_items = ['first_name', 'last_name', 'city']
        some = 4 * self._base * "_"
        for item in all_items:
            self.widget.get(item).config(text=some)

    def show_file(self):
        if not self.widget.get('gr'):
            return self.show_message('Запустите программу!')

        all_items = ['last_name', 'first_name', 'sex', 'city', 'universities']

        with open("Friends.txt", "w",  encoding='utf-16') as f:
            for id_node in self.widget.get('gr').central_fr:
                node = self.widget.get('gr').central_fr.get(id_node)
                ln = ''
                for item in all_items:
                    ln_str = node.get_item(item, '')
                    ln = f'{ln}  {ln_str}'
                f.write(f'{ln}\n')

    @staticmethod
    def show_message(text: str, name_file="Ошибка"):
        messagebox.showinfo(name_file, text)


def start(
        info_func: Callable[str] = None,
        to_go_func: Callable[str] = None,
        show_func: Callable[str] = None,
        create_gr: Callable[str] = None,
        base: int = 5):
    root = tk.Tk()
    app = Application(master=root, info_func=info_func, to_go_func=to_go_func,
                      show_func=show_func, base=base, create_gr=create_gr)
    return app


if __name__ == "__main__":
    pass
