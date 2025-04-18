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
        if re.fullmatch(r"\d{10}", phone_number):
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
        if re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w+", value):
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
        raise ValueError(f"A phone with {phone_number} number is not found")

    def remove_phone(self, phone_number: str) -> None:
        phone = self.find_phone(phone_number)
        self.phones.remove(phone)

        
    # For validating phone and email use class constructors
    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        if not new_phone_number:
            raise ValueError("New phone number must be provided.")
        
        phone_to_edit = self.find_phone(old_phone_number)
        validated_phone = Phone(new_phone_number)
        phone_to_edit.value = validated_phone.value

    def edit_email(self, new_email: str) -> None:
        if not new_email:
            raise ValueError("New email must be provided.")

        validated_email = Email(new_email)
        self.email = validated_email

    def __str__(self) -> str:
        parts = [self.name.value.__str__()]
        if self.phones:
            parts.append(', '.join(p.value.__str__() for p in self.phones))
        if self.birthday:
            parts.append(self.birthday.__str__())
        if self.address:
            parts.append(self.address.__str__())
        if self.email:
            parts.append(self.email.__str__())
        return "; ".join(parts)
