"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Whenwasi."""


if __name__ == "__main__":
    main(prog_name="whenwasi")  # pragma: no cover
