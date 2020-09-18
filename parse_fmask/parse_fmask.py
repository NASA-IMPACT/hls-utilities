import click


@click.command()
@click.argument(
    "fmaskoutput",
    type=click.STRING,
)
def main(fmaskoutput):
    left = fmaskoutput.split("%")[0]
    spaced = left.split(" ")
    clear_percentage = spaced[len(spaced) - 1]
    try:
        value = float(clear_percentage)
    except ValueError:
        value = 50

    if value < 2:
        click.echo("invalid")
    else:
        click.echo("valid")


if __name__ == "__main__":
    main()
