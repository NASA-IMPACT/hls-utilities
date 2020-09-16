import datetime
import click


@click.command()
@click.argument(
    "year",
    type=click.STRING,
)
@click.argument(
    "month",
    type=click.STRING,
)
@click.argument(
    "day",
    type=click.STRING,
)
def main(year, month, day):
    year = int(year)
    month = int(month.lstrip("0"))
    day = int(day.lstrip("0"))
    date = datetime.date(year, month, day)
    day_of_year = date.timetuple().tm_yday
    # derive_s2nbar requires a three digit doy
    click.echo(str(day_of_year).zfill(3))


if __name__ == "__main__":
    main()
