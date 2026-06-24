class Counter(object):

    def __init__(self, count=0) -> None:
        self._count_ = count

    def get(self):
        return self._count_

    def incr(self):
        self._count_ += 1

    def incr_and_get(self):
        self._count_ += 1
        return self._count_

    def get_and_incr(self):
        old_value = self._count_
        self._count_ += 1
        return old_value
