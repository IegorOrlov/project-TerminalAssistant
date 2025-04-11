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
    delete_note,
)
from address_book import AddressBook
from data_service import save_data, load_data
from note_book import NoteBook
from rich_helper import print_rich_table

HEADER = ["Comand", "Description"]

COMMANDS = [
    ["add-contact", "Add a new contact to the address book"],
    ["add-note", "Add a new note to the note book"],
    ["all-contacts", "Show all contacts in the address book"],
    ["all-notes", "Show all notes in the note book"],
    ["birthdays", "Show all upcoming birthdays in the address book"],
    ["close", "Close the application and save the data"],
    ["delete-contact", "Delete a contact from the address book"],
    ["delete-note", "Delete a note from the note book"],
    ["exit", "Exit the application and save the data"],
    ["find-note", "Find a specific note"],
    ["hello", "Start a dialog with the bot"],
    ["phone", "Show the phone number for a specific contact"],
    ["search-contact", "Search for a contact in the address book"],
    ["show-birthday", "Show birthday information for a specific contact"],
    ["update-contact", "Update an existing contact in the address book"],
    ["update-note", "Update an existing note in the note book"],
]


def parse_input(user_input: str) -> tuple[str, tuple[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    address_book, note_book = load_data()
    print("Welcome to the assistant bot!")
    print_rich_table("Available Commands", HEADER, COMMANDS)
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
