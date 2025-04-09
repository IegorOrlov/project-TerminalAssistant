from error_handlers import input_error
from address_book import AddressBook
from record import Record

def add_contact_interactive(book: AddressBook) -> str:
    while True:
        name = input("Enter the name: ").strip()
        if name:
            break
        print("Name is required. Please enter a valid name.")

    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        print(f"Contact '{name}' created.")
    else:
        print(f"Contact '{name}' already exists. Its information will be updated.")

    while True:
        phone = input("Enter phone (or press Enter to skip): ").strip()
        if phone:
            try:
                record.add_phone(phone)
                print(f"Phone '{phone}' added.")
            except ValueError as e:
                print(f"Error adding phone: {e}")
                continue
            add_more = input("Do you want to enter one more phone number? (y/n): ").strip().lower()
            if add_more != "y":
                break
        else:
            break

    while True:
        email = input("Enter email (or press Enter to skip): ").strip()
        if not email:
            break
        try:
            record.add_email(email)
            print(f"Email '{email}' added.")
            break
        except ValueError as e:
            print(f"Error adding email: {e}")

    while True:
        address = input("Enter address (or press Enter to skip): ").strip()
        if not address:
            break
        try:
            record.add_address(address)
            print(f"Address '{address}' added.")
            break
        except ValueError as e:
            print(f"Error adding address: {e}")

    while True:
        birthday = input("Enter birthday (DD.MM.YYYY) (or press Enter to skip): ").strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            print(f"Birthday '{birthday}' added.")
            break
        except ValueError as e:
            print(f"Error adding birthday: {e}")

    return f"Contact '{name}' has been saved successfully."

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
    while True:
        days_input = input("Enter the number of days (default is 7): ").strip()
        if not days_input:
            days = 7
            break
        try:
            days = int(days_input)
            if days <= 0:
                print("Number of days cannot be zero or negative. Defaulting to 7.")
                days = 7
            break
        except ValueError:
            print("Invalid input. Please enter a valid number or press Enter to use default (7).")
    
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    return "\n".join(
        f"Upcoming {record.name.value}'s birthday is {record.birthday}" for record in upcoming
    )

@input_error
def add_address(args: tuple[str], book: AddressBook) -> str:
    name, address, *_ = args
    record = book.find(name)
    if record:
        record.add_address(address)
        return f"Address '{address}' has been added for contact '{name}'."
    else:
        return f"User {name} not found."


@input_error
def add_email(args: tuple[str], book: AddressBook) -> str:
    name, email, *_ = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return f"Email '{email}' has been added for contact '{name}'."
    else:
        return f"User {name} not found."
