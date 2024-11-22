class Stack:
    def __init__(self):
        self._stack = list()

    def push(self, new_value):
        self._stack.append(new_value)

    def peek(self):
        return self._stack[-1]

    def pop(self):
        deleted_val = self._stack[-1]
        del self._stack[-1]
        return deleted_val

    @property
    def available(self):
        return self._stack
