from .converter import enhance, to_dict


class EnhancedList(list):

    def __init__(self, iterable=()):
        super().__init__(enhance(item) for item in iterable)

    def __setitem__(self, index, value):
        super().__setitem__(index, enhance(value))

    def append(self, value):
        super().append(enhance(value))

    def extend(self, iterable):
        super().extend(enhance(item) for item in iterable)

    def insert(self, index, value):
        super().insert(index, enhance(value))

    def __getitem__(self, index):
        value = super().__getitem__(index)
        return enhance(value)

    def to_dict(self) -> list:
        return [to_dict(item) for item in self]
