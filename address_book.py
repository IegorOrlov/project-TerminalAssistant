from record import Record
from collections import UserDict
import birthday_service as bs


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> Record:
        return self.data.pop(name)

    def get_upcoming_birthdays(self, days: int = 7) -> list[Record]:
        return bs.get_upcoming_birthdays(self.data.values(), days)

