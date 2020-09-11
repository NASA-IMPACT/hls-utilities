import os
from click.testing import CliRunner
from check_solar_zenith_sentinel.check_solar_zenith_sentinel import main


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_check_solar_zenith_angle():
    inputxml = os.path.join(test_dir, "MTD_TL.xml")
    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        inputxml
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "valid\n"
