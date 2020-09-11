import click


@click.command()
@click.argument(
    "fmaskoutput",
    type=click.STRING,
)
def main(fmaskoutput):
    lines = fmaskoutput.splitlines()
    if "0.00%" in lines[len(lines) - 3]:
        click.echo("invalid")
    else:
        click.echo("valid")


if __name__ == "__main__":
    main()
