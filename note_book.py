from collections import UserDict
from record import Field


class Title(Field):
    pass


class Text(Field):
    pass


class Tag(Field):
    def __str__(self):
        return "#" + super().__str__()


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
        self.tags.extend([Tag(tag) for tag in tags.split(" ")])

    def __str__(self) -> str:
        parts = [f"Title: {self.title}"]
        if self.text:
            parts.append(f"Text: {self.text}")
        if self.tags:
            parts.append(f"Tags: {'; '.join(tag.__str__() for tag in self.tags)}")
        return ", ".join(parts)


class NoteBook(UserDict[str, Note]):
    def add_note(self, note: Note) -> None:
        self.data[note.title.value] = note

    def find(self, title: str) -> Note:
        return self.data.get(title)

    def delete(self, title: str) -> Note:
        return self.data.pop(title)
