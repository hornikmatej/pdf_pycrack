import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def print_start_info(
    pdf_file, min_length, max_length, charset, batch_size, cores, start_time
):
    """Prints the starting information in a formatted panel."""

    grid = Table.grid(expand=True)
    grid.add_column(justify="left", style="bold")
    grid.add_column(justify="left")

    grid.add_row("PDF File:", f"[cyan]{pdf_file}[/cyan]")
    grid.add_row("Password Length:", f"[cyan]{min_length} to {max_length}[/cyan]")
    grid.add_row("Character Set:", f"[cyan]{charset}[/cyan]")
    grid.add_row("Batch Size:", f"[cyan]{batch_size}[/cyan]")
    grid.add_row("CPU Cores:", f"[cyan]{cores}[/cyan]")
    grid.add_row("Start Time:", f"[cyan]{time.ctime(start_time)}[/cyan]")

    panel = Panel(
        grid,
        title="[bold yellow]PDF PyCrack Initializing[/bold yellow]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)


def print_end_info(result):
    """Prints the final result and duration in a formatted panel."""

    status = result.get("status")
    duration = result.get("elapsed_time", 0)
    password = result.get("password")

    if status == "found":
        end_message = Text.from_markup(
            f"Password found: [bold green]{repr(password)}[/bold green]"
        )
        panel_title = "[bold green]Cracking Successful[/bold green]"
        border_style = "green"
    elif status == "interrupted":
        end_message = Text.from_markup("Cracking process interrupted by user.")
        panel_title = "[bold yellow]Cracking Interrupted[/bold yellow]"
        border_style = "yellow"
    else:  # not_found
        end_message = Text.from_markup(
            "Password not found within the specified constraints."
        )
        panel_title = "[bold red]Cracking Failed[/bold red]"
        border_style = "red"

    grid = Table.grid(expand=True)
    grid.add_column(justify="left", style="bold")
    grid.add_column(justify="left")

    grid.add_row("Status:", end_message)
    grid.add_row("Duration:", f"[cyan]{duration:.2f} seconds[/cyan]")

    passwords_checked = result.get("passwords_checked", 0)
    passwords_per_second = result.get("passwords_per_second", 0)

    if passwords_checked > 0:
        grid.add_row("Passwords Checked:", f"[cyan]{passwords_checked}[/cyan]")
        grid.add_row("Passwords/Second:", f"[cyan]{passwords_per_second:.2f}[/cyan]")

    panel = Panel(grid, title=panel_title, border_style=border_style, padding=(1, 2))
    console.print(panel)
