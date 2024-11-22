class Node:
    def __init__(self, desc, priority, scheduled_time, nextVal):
        self.description = desc
        self.priority = priority
        self.scheduled_time = scheduled_time

        self.next = nextVal
