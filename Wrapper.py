class Wrapper:
    def __init__(self, obj):
        self._obj = obj

    def __getitem__(self, item):
        if isinstance(self._obj, dict):
            return Wrapper(self._obj.get(item))
        elif isinstance(self._obj, list):
            return Wrapper(self._obj[item])
        elif isinstance(self._obj, str):
            return self._obj[item]
        else:
            return Wrapper(self._obj.get(item))

    def __getattr__(self, item):
        def getter(obj):
            if item not in obj:
                return
            return obj.get(item)

        if self._obj is None:
            return
        if isinstance(self._obj, dict):
            return Wrapper(self._obj.get(item))
        elif isinstance(self._obj, list):
            return Wrapper(list(map(getter, self._obj)))
        else:
            return Wrapper(self._obj.get(item))

    def get_city(self):
        def getter(obj):
            if 'city' not in obj:
                return
            return obj.get('city').get('title')

        if isinstance(self._obj, list):
            return list(map(getter, self._obj))
        return getter(self._obj)

    def get_item(self, item, default=None):
        def getter(obj):
            if item not in obj:
                return
            if 'title' not in obj.get(item):
                return obj.get(item)
            return obj.get(item).get('title', default)

        if isinstance(self._obj, list):
            return list(map(getter, self._obj))
        return getter(self._obj)

    def __str__(self):
        return str(self._obj)

    def __int__(self):
        return int(self._obj)

    def __float__(self):
        return float(self._obj)

    def set(self):
        return set(self._obj)

    def __eq__(self, other):
        return self._obj == other

    def __bool__(self):
        return bool(self._obj)

    def get_real(self):
        return self._obj

    def get(self, item):
        return self._obj.get(item)


if __name__ == "__main__":
    t = Wrapper(['777', '6789'])
    print(t.set())
