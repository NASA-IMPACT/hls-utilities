import os
import io
import pytest
import boto3
from click.testing import CliRunner
from moto import mock_s3
from download_landsat.download_landsat import get_landsat, main
from download_landsat.download_landsat import KeyDoesNotExist

BUCKET = "usgs-landsat1"
BASE_KEY = "collection02/level-1/standard/oli-tirs/2021/155/018"
RT_ROOT = "LC08_L1TP_155018_20210603_20210603_02_RT"
RT_KEY = f"{BASE_KEY}/{RT_ROOT}"
T1_ROOT = "LC08_L1TP_155018_20210603_20210608_02_T1"
T1_KEY = f"{BASE_KEY}/{T1_ROOT}"


@pytest.fixture(scope="module")
def clear_test_file():
    yield None
    os.system("rm ./test.json")


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=BUCKET)
        client.put_bucket_request_payment(
            Bucket=BUCKET,
            RequestPaymentConfiguration={
                "Payer": "Requester"
            },
        )
        yield client


def test_download(s3, tmp_path):
    fo = io.BytesIO(b"file object in RAM")
    filename = "rt.json"
    s3.upload_fileobj(fo, BUCKET, f"{RT_KEY}/{filename}")
    get_landsat(BUCKET, RT_KEY, str(tmp_path))
    assert os.path.isfile(tmp_path.joinpath(filename))


def test_download_no_keys(s3, tmp_path):
    with pytest.raises(KeyDoesNotExist):
        get_landsat(BUCKET, RT_KEY, str(tmp_path))


def test_download_updated_tier(s3, tmp_path):
    fo = io.BytesIO(b"file object in RAM")
    filename = "t1.json"
    s3.upload_fileobj(fo, BUCKET, f"{T1_KEY}/{filename}")
    actual = get_landsat(BUCKET, RT_KEY, str(tmp_path))
    assert os.path.isfile(tmp_path.joinpath(filename))
    assert actual == T1_ROOT


def test_download_landsat_cli(s3, tmp_path):
    fo = io.BytesIO(b"file object in RAM")
    filename = "rt.json"
    s3.upload_fileobj(fo, BUCKET, f"{RT_KEY}/{filename}")

    runner = CliRunner(echo_stdin=True)
    result = runner.invoke(main, [BUCKET, RT_KEY, str(tmp_path)])
    assert result.exit_code == 0
    assert result.output == f"{RT_ROOT}\n"
