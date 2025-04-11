from rich.table import Table

def create_rich_table(title: str, columns: list[str], rows: list[list[str]]) -> Table:
    table = Table(title=title)
    
    for col in columns:
        table.add_column(col, style="cyan", no_wrap=True)
    
    for row in rows:
        table.add_row(*row)
    
    return table
