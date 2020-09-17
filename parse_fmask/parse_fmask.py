import click
import re


@click.command()
@click.argument(
    "fmaskoutput",
    type=click.STRING,
)
def main(fmaskoutput):
    result = re.search(r"\d+%|([0-9]\d?)\.\d", fmaskoutput)
    if result is None:
        click.echo("valid")
    else:
        clear_percentage = result.group()
        value = float(clear_percentage)
        if value < 2:
            click.echo("invalid")
        else:
            click.echo("valid")


if __name__ == "__main__":
    main()
