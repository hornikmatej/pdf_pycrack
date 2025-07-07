from rich.console import Console
from rich.panel import Panel

console = Console()


def print_error(title, message):
    """Prints an error message in a formatted panel."""
    panel = Panel(
        f"[white]{message}[/white]",
        title=f"[bold red]{title}[/bold red]",
        border_style="red",
        padding=(1, 2),
    )
    console.print(panel)
