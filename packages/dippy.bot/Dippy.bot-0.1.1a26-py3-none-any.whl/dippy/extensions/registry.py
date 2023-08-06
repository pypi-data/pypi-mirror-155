from collections import defaultdict


class ListenerRegistry:
    def __init__(self):
        self._listeners: dict[type, dict[str, str]] = defaultdict(dict)

    def __get__(self, instance, owner):
        return self._listeners[owner]
