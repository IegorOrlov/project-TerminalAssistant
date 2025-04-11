from collections import UserDict
from record import Field


class Title(Field):
    pass


class Text(Field):
    pass


class Tag(Field):
    def __str__(self):
        return "#" + super().__str__()
    
    def __eq__(self, other):
        return self.value == other.value


class Note:
    def __init__(self) -> None:
        self.title = None
        self.text = None
        self.tags = []

    def add_title(self, title: str) -> None:
        self.title = Title(title)

    def add_text(self, text: str) -> None:
        self.text = Text(text)

    def add_tags(self, tags: str) -> None:
        self.tags = [Tag(tag) for tag in tags.split(" ")]

    def __str__(self) -> str:
        parts = [self.title.__str__()]
        if self.text:
            parts.append(self.text.__str__())
        if self.tags:
            parts.append(', '.join(tag.__str__() for tag in self.tags))
        return "; ".join(parts)


class NoteBook(UserDict[str, Note]):
    def add_note(self, note: Note) -> None:
        self.data[note.title.value] = note

    def find(self, title: str) -> Note:
        return self.data.get(title)

    def delete(self, title: str) -> Note:
        return self.data.pop(title)
