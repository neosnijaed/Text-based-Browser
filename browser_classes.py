from collections import deque


class BrowserHistory:
    def __init__(self):
        self.history = deque()
        self.buffer = ''

    def extend_queue(self, domain_name):
        self.history.append(self.buffer)
        self.buffer = domain_name
