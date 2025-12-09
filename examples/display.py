#!/usr/bin/env python3
"""Display formatting functions using Rich library."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
error_console = Console(stderr=True)


def display_rooms_table(rooms: list[dict[str, str]]) -> None:
    """Displays rooms in a formatted table.

    Args:
        rooms: List of room dictionaries with 'id' and 'name' keys
    """
    if not rooms:
        console.print("[yellow]No rooms with thermostats found.[/yellow]")
        return

    table = Table(title=f"[bold cyan]Thermostat Rooms[/bold cyan] ({len(rooms)} found)")
    table.add_column("Room ID", style="cyan", no_wrap=True)
    table.add_column("Room Name", style="green")

    for room in rooms:
        table.add_row(room['id'], room['name'])

    console.print(table)


def display_temperature_result(room_name: str, temperature: float) -> None:
    """Displays success message for temperature change.

    Args:
        room_name: Name of the room
        temperature: Temperature value set
    """
    console.print(
        f"[green]✓[/green] Successfully set [cyan]{room_name}[/cyan] to "
        f"[bold yellow]{temperature}°C[/bold yellow]"
    )


def display_error_panel(title: str, message: str) -> None:
    """Displays error message in a prominent panel.

    Args:
        title: Error title
        message: Error message
    """
    error_console.print(
        Panel(
            message,
            title=f"[bold red]{title}[/bold red]",
            border_style="red",
            expand=False
        )
    )
