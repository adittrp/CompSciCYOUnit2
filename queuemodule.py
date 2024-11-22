class Queue:
    def __init__(self):
        self._queue = list()

    def enqueue(self, new_value):
        self._queue.append(new_value)

    def display(self):
        return self._queue[0]

    def dequeue(self):
        deleted_val = self._queue[0]
        del self._queue[0]
        return deleted_val
