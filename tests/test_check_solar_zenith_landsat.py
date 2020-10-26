import os
from click.testing import CliRunner
from check_solar_zenith_landsat.check_solar_zenith_landsat import main


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_check_solar_zenith_angle_c1():
    inputmtl = os.path.join(
        test_dir,
        "LC08_L1TP_027039_20190901_20190901_01_RT_MTL.txt"
    )
    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        inputmtl
    ], catch_exceptions=False)
    assert result.exit_code == 0
    print(result.stdout)
    assert result.stdout == "valid\n"


def test_check_solar_zenith_angle_c2():
    inputmtl = os.path.join(
        test_dir,
        "LC08_L1TP_231089_20200807_20200808_02_RT_MTL.txt"
    )
    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        inputmtl
    ], catch_exceptions=False)
    assert result.exit_code == 0
    print(result.stdout)
    assert result.stdout == "valid\n"
