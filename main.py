from command_handlers import (
    add_contact,
    update_contact,
    delete_contact,
    show_phone,
    show_as_table,
    show_birthday,
    birthdays,
    search_contact,
    add_note,
    find_note,
    update_note,
    delete_note
)
from address_book import AddressBook
from data_service import save_data, load_data
from note_book import NoteBook


def parse_input(user_input: str) -> tuple[str, tuple[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    address_book, note_book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(address_book, note_book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add-contact":
            print(add_contact(address_book))
        elif command == "add-note":
            print(add_note(note_book))
        elif command == "update-contact":
            print(update_contact(address_book))
        elif command == "update-note":
            print(update_note(note_book))
        elif command == "delete-note":
            print(delete_note(note_book))
        elif command == "delete-contact":
            print(delete_contact(address_book))
        elif command == "search-contact":
            print(search_contact(address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all-contacts":
            print(show_as_table(list(address_book.values()), "All Contacts"))
        elif command == "all-notes":
            print(show_as_table(list(note_book.values()), "All Notes"))
        elif command == "find-note":
            print(find_note(note_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(address_book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
