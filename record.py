import re
from datetime import datetime as dada


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone_number: str):
        if re.match(r"^\d{10}$", phone_number):
            super().__init__(phone_number)
        else:
            raise ValueError(
                f"Phone number '{phone_number}' doesn't contain 10 numbers only."
            )


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            super().__init__(dada.strptime(value, "%d.%m.%Y").date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")
    
class Address(Field):
    def __init__(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value: str) -> None:
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            super().__init__(value)
        else:
            raise ValueError(f"Invalid email address: {value}")

class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def find_phone(self, phone_number: str) -> Phone:
        for phone in self.phones:
            if phone_number == phone.value:
                return phone
        raise ValueError("A phone with {phone_number} number is not found")

    def remove_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        self.phones.remove(phone)

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        phone = self.find_phone(old_phone_number)
        if new_phone_number:
            phone.value = new_phone_number
        else:
            raise ValueError(
                "To update a phone number the new value should't be empty."
            )

    def __str__(self) -> str:
        parts = [f"Name: {self.name.value}"]
        if self.phones:
            parts.append(f"Phones: {'; '.join(p.value for p in self.phones)}")
        if self.birthday:
            parts.append(f"Birthday: {self.birthday}")
        if self.address:
            parts.append(f"Address: {self.address}")
        if self.email:
            parts.append(f"Email: {self.email}")
        return ", ".join(parts)
