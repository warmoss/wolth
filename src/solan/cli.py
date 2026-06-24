"""Console script for solan."""

import typer
from rich.console import Console

from solan import utils

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main() -> None:
    utils.do_something_useful()


if __name__ == "__main__":
    app()
