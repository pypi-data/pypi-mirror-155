from __future__ import annotations
from dippy.extensions.listener import ListenerDecorator, Listener
from nextcord import Message
from types import MethodType
from typing import Any, Callable


class CommandDecorator(ListenerDecorator):
    def __init__(self, command_name: str):
        super().__init__("message")
        self._command_name = command_name

    def __get__(self, instance, owner):
        return Command(self._command_name, MethodType(self._handler, instance))


class Command(Listener):
    def __init__(self, command_name: str, handler: Callable[[Any, ...], Any]):
        super().__init__("message", handler)
        self._command_name = command_name

    @property
    def command_name(self) -> str:
        return self._command_name

    @property
    def handler(self) -> Callable[[Any, ...], Any]:
        return self._handler

    def __call__(self, message: Message, *args, **kwargs):
        if message.content.lower().startswith(self._command_name):
            return self._handler(message, *args, **kwargs)
