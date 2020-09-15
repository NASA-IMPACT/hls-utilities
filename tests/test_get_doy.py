from click.testing import CliRunner
from get_doy.get_doy import main


def test_get_doy():
    year = "2020"
    month = "02"
    day = "02"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        year,
        month,
        day
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "033\n"
