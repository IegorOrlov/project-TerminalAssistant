from rich.table import Table
from record import Record

def create_rich_table(title: str, columns: list[str], rows: list[list[str]]) -> Table:
    table = Table(title=title)
    
    for col in columns:
        table.add_column(col, style="cyan", no_wrap=True)
    
    for row in rows:
        table.add_row(*row)
    
    return table

def create_contact_table(title: str, record: Record) -> Table:
    fields = {
        "Name": record.name.value,
        "Phone(s)": ", ".join(p.value for p in record.phones) if record.phones else "Not set",
        "Address": str(record.address) if record.address else "Not set",
        "Email": str(record.email) if record.email else "Not set",
        "Birthday": str(record.birthday) if record.birthday else "Not set",
    }

    rows = [[field, value] for field, value in fields.items()]
    
    return create_rich_table(title, ["Field", "Value"], rows)
