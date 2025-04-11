from rich.table import Table
from rich.console import Console
from record import Record


def print_rich_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    table = Table(title=title)

    for col in columns:
        table.add_column(col, style="cyan", no_wrap=True)

    for row in rows:
        table.add_row(*row)

    Console().print(table)


def print_contact_table(title: str, record: Record) -> None:
    fields = {
        "Name": record.name.value,
        "Phone(s)": (
            ", ".join(p.value for p in record.phones) if record.phones else "Not set"
        ),
        "Address": str(record.address) if record.address else "Not set",
        "Email": str(record.email) if record.email else "Not set",
        "Birthday": str(record.birthday) if record.birthday else "Not set",
    }

    rows = [[field, value] for field, value in fields.items()]

    print_rich_table(title, ["Field", "Value"], rows)
