import pickle
from address_book import AddressBook
from note_book import NoteBook


def save_data(*data: tuple, filename="userdata.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_data(filename="userdata.pkl") -> tuple:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return (AddressBook(), NoteBook())
