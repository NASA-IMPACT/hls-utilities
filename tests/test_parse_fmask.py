from click.testing import CliRunner
from parse_fmask.parse_fmask import main


def test_parse_fmask_invalid():
    fmaskoutput = "for L1C_T37WFN_A017436_20200708T084600 with 0.01% clear pixels"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        fmaskoutput
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "invalid\n"


def test_parse_fmask_valid():
    fmaskoutput = "for L1C_T23XNB_A017440_20200708T152810 with 21.03% clear pixels"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        fmaskoutput
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "valid\n"


def test_parse_fmask_no_percent():
    fmaskoutput = "for L1C_T23XNB_A017440_20200708T152810 with clear pixels"

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [
        fmaskoutput
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.stdout == "valid\n"
