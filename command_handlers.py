from error_handlers import input_error
from address_book import AddressBook
from record import Record
from rich_helper import print_rich_table, print_contact_table
from note_book import NoteBook, Note, Tag
from typing import Callable, Any

REQUIRED_MSG = "Enter required value of {}: "
UPDATE_MSG = "Enter new {} (or press Enter to skip): "


def add_contact(book: AddressBook) -> str:
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
            add_more = (
                input("Do you want to enter one more phone number? (y/n): ")
                .strip()
                .lower()
            )
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
        birthday = input(
            "Enter birthday (DD.MM.YYYY) (or press Enter to skip): "
        ).strip()
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
def find_note(note_book: NoteBook) -> None:
    key = input("Enter a title or tag to search: ")
    note = note_book.find(key)
    if not note:
        key_tag = Tag(key)
        show_as_table(
            [note for note in note_book.values() if key_tag in note.tags],
            f"Matched notes to '{key}' tag",
        )
    else:
        show_as_table([note], "The note for '{key}' title")


@input_error
def delete_note(note_book: NoteBook) -> None:
    key = input("Enter a title to delete note: ")
    note = note_book.delete(key)
    if note:
        show_as_table([note], "The note has been deleted")
    else:
        print(f"There isn't ant note with '{key}' title.")


@input_error
def update_note(note_book: NoteBook) -> None:
    title = input("Enter a title of note to update: ")

    note = note_book.find(title)
    show_as_table([note], "This note is being updated")

    __enter_value("title", note.add_title, False, UPDATE_MSG)
    __enter_value("text", note.add_text, False, UPDATE_MSG)
    __enter_value(
        "tags",
        note.add_tags,
        False,
        "Enter new {} separated by spaces (or press Enter to skip): ",
    )


@input_error
def add_note(note_book: NoteBook) -> None:
    note = Note()
    __enter_value("title", note.add_title, True, REQUIRED_MSG)
    __enter_value("text", note.add_text, True, REQUIRED_MSG)
    __enter_value(
        "tags",
        note.add_tags,
        False,
        "Enter {} separated by spaces (or press Enter to skip): ",
    )
    note_book.add_note(note)


def __enter_value(
    value_name: str,
    consumer: Callable[[str], None],
    is_required=False,
    input_msg: str = "Enter {} (or press Enter to skip): ",
):
    while True:
        value = input(input_msg.format(value_name)).strip()
        if not value and not is_required:
            break
        try:
            consumer(value)
            print(f"{value_name.capitalize()} '{value}' added.")
            break
        except ValueError as e:
            print(f"Error adding {value_name}: {e}")


@input_error
def update_contact(book: AddressBook) -> str:

    while True:
        name = input("Enter the contact name to update: ").strip()
        if name:
            break
        print("Contact name cannot be empty.")
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    print_contact_table("Current Record", record)

    available_fields = ["phone", "address", "email", "birthday"]
    fields_rows = [[field] for field in available_fields]
    print_rich_table("Available Fields to Change", ["Field"], fields_rows)

    while True:
        field_to_change = input("Enter field to change: ").strip().lower()
        if field_to_change in available_fields:
            break
        print("Invalid field. Please choose one of: phone, address, email, birthday.")

    if field_to_change in ["address", "email", "birthday"]:
        current_value = getattr(record, field_to_change)
        print(
            f"Current {field_to_change}: {current_value if current_value else 'Not set'}"
        )
        new_value = input(
            f"Enter new {field_to_change} (or press Enter to cancel): "
        ).strip()
        if new_value:
            try:
                if field_to_change == "address":
                    record.add_address(new_value)
                elif field_to_change == "email":
                    record.edit_email(new_value)
                elif field_to_change == "birthday":
                    record.add_birthday(new_value)
                return f"{field_to_change.capitalize()} updated for contact '{name}'."
            except ValueError as e:
                return f"Error updating {field_to_change}: {e}"
        else:
            return f"No changes made to {field_to_change}."

    elif field_to_change == "phone":
        if not record.phones:
            return "No phone numbers to change."
        else:
            phone_rows = [
                [str(idx), phone.value]
                for idx, phone in enumerate(record.phones, start=1)
            ]
            print_rich_table("Phone Numbers", ["Index", "Phone"], phone_rows)

            while True:
                index_input = input(
                    "Enter the number corresponding to the phone you want to change: "
                ).strip()
                if index_input.isdigit():
                    index = int(index_input)
                    if 1 <= index <= len(record.phones):
                        break
                    else:
                        print("Invalid number. Try again.")
                else:
                    print("Please enter a valid number.")
            old_phone = record.phones[index - 1].value
            new_phone = input(
                "Enter new phone (or press Enter to delete this phone): "
            ).strip()
            if new_phone:
                try:
                    record.edit_phone(old_phone, new_phone)
                    return "Phone number updated."
                except ValueError as e:
                    return f"Error updating phone: {e}"
            else:
                try:
                    record.remove_phone(old_phone)
                    return "Phone number removed."
                except ValueError as e:
                    return f"Error removing phone: {e}"


@input_error
def search_contact(book: AddressBook) -> str:
    from rich.console import Console
    from rich_helper import print_rich_table

    search_term = input("Enter search term (name, phone or email): ").strip().lower()
    if not search_term:
        return "Search term cannot be empty."

    matching_records = []

    for name, record in book.items():
        if search_term in record.name.value.lower():
            matching_records.append(record)
            continue

        if record.email and search_term in str(record.email).lower():
            matching_records.append(record)
            continue

        for phone in record.phones:
            if search_term in phone.value:
                matching_records.append(record)
                break

    if not matching_records:
        return "No matching contacts found."

    columns = ["Name", "Phones", "Email"]
    rows = []
    for rec in matching_records:
        phones_str = ", ".join(p.value for p in rec.phones) if rec.phones else "Not set"
        email_str = str(rec.email) if rec.email else "Not set"
        rows.append([rec.name.value, phones_str, email_str])

    print_rich_table("Search Results", columns, rows)
    return ""


@input_error
def delete_contact(book: AddressBook) -> str:
    while True:
        name = input("Enter the contact name to delete: ").strip()
        if name:
            break
        print("Contact name cannot be empty.")

    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    print_contact_table("Contact to Delete", record)

    confirmation = (
        input(f"Are you sure you want to delete contact '{name}'? (y/n): ")
        .strip()
        .lower()
    )
    if confirmation != "y":
        return "Deletion cancelled."

    try:
        book.delete(name)
        return f"Contact '{name}' was deleted successfully."
    except KeyError:
        return f"Error: Contact '{name}' not found during deletion."


@input_error
def show_phone(args: tuple[str], book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"
    return f"User {name} not found."


@input_error
def show_as_table(items: list, table_name: str) -> None:
    columns = [key.capitalize() for key in vars(items[0]).keys()] if items else items
    rows = [item.__str__().split(";") for item in items]

    print_rich_table(table_name, columns, rows)


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
            print(
                "Invalid input. Please enter a valid number or press Enter to use default (7)."
            )

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    return "\n".join(
        f"Upcoming {record.name.value}'s birthday is {record.birthday}"
        for record in upcoming
    )
