from error_handlers import input_error
from address_book import AddressBook
from record import Record


@input_error
def add_contact(args: tuple[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: tuple[str], book: AddressBook) -> str:
    name, phone_old, phone_new, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(phone_old, phone_new)
        return "Contact updated."
    return f"User {name} not found."


@input_error
def show_phone(args: tuple[str], book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"
    return f"User {name} not found."


@input_error
def show_all(book: AddressBook) -> str:
    result = ""
    for name, record in book.items():
        result = result + f"{record}\n"
    return result.strip()


@input_error
def add_birthday(args: tuple[str], book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"The birthday date {birthday} has been added into {name}'s record."
    else:
        return f"User {name} not found."


@input_error
def show_birthday(args: tuple[str], book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name}'s birthday is {record.birthday}"
    return f"User {name} not found."


@input_error
def birthdays(book: AddressBook) -> str:
    return "\n".join(
        f"Upcoming {record.name}'s birthday is {record.birthday}"
        for record in book.get_upcoming_birthdays()
    )
