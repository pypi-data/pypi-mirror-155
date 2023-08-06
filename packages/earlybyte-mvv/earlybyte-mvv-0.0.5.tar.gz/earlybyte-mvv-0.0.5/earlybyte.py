from dataclasses import dataclass, field
from typing import List, Optional
import typer


@dataclass
class Earlybyte:
    mission: str = (
        "We collaboratively craft software that frees up time for what really matters."
    )

    vision: str = "We become a publicly trusted partner for solid software."

    values: List[str] = field(
        default_factory=lambda: [
            "Passion",
            "Simplicity",
            "Community",
            "Authenticity",
            "Curiosity",
        ]
    )


app = typer.Typer()
eb = Earlybyte()


@app.command()
def mission():
    """Show the mission statement of Earlybyte."""
    typer.secho(eb.mission, fg=typer.colors.BRIGHT_MAGENTA)


@app.command()
def vision():
    """Show the vision statement of Earlybyte."""
    typer.secho(eb.vision, fg=typer.colors.BRIGHT_MAGENTA)


@app.command()
def values(
    index: Optional[int] = typer.Argument(
        None, help="Index of the value to return. This is an optional parameter"
    )
):
    """Show the values of Earlybyte. Add optional index to get specific value."""

    if index is not None:
        if 0 <= index and index <= 4:
            typer.secho(eb.values[index], fg=typer.colors.BRIGHT_MAGENTA)
            return

    typer.secho(", ".join(eb.values), fg=typer.colors.BRIGHT_MAGENTA)


def main():
    app()


if __name__ == "__main__":
    app()
