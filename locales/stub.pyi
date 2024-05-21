from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    command: Command
    notes: Notes
    add: Add
    enter: Enter
    no: No

    @staticmethod
    def delete() -> Literal["""Delete"""]: ...

    @staticmethod
    def success() -> Literal["""Success"""]: ...

    @staticmethod
    def back() -> Literal["""Back"""]: ...

    @staticmethod
    def cancel() -> Literal["""Cancel"""]: ...


class Command:
    @staticmethod
    def select() -> Literal["""Select a command"""]: ...


class Notes:
    @staticmethod
    def list() -> Literal["""List of notes"""]: ...


class Add:
    @staticmethod
    def note() -> Literal["""Add a note"""]: ...


class Enter:
    @staticmethod
    def title() -> Literal["""Enter a note title"""]: ...

    @staticmethod
    def note() -> Literal["""Enter a note"""]: ...


class No:
    @staticmethod
    def notes() -> Literal["""There are no notes"""]: ...

