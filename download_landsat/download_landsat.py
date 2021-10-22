import boto3
import click
from pathlib import Path


class KeyDoesNotExist(Exception):
    pass


def key_exists(client, bucket, path):
    result = client.list_objects_v2(
        Bucket=bucket,
        Prefix=path,
        RequestPayer="requester"
    )
    if result.get("KeyCount") > 0:
        return True
    else:
        return False


def download_files(client, bucket, path, output_directory):
    result = client.list_objects_v2(
        Bucket=bucket,
        Prefix=path,
        RequestPayer="requester"
    )
    contents = result.get("Contents")
    for content in contents:
        key = content.get("Key")
        filename = Path(key).name
        output_file = Path(output_directory).joinpath(filename)
        client.download_file(bucket, key, str(output_file), ExtraArgs={
            "RequestPayer": "requester"
        })


def get_updated_key(client, bucket, path):
    path_root = Path(path).parent
    result = client.list_objects_v2(
        Bucket=bucket,
        Prefix=str(path_root) + "/",
        RequestPayer="requester",
        Delimiter="/"
    )
    if result.get("KeyCount") == 0:
        raise KeyDoesNotExist
    else:
        updated_key = [
            prefix["Prefix"] for prefix in result.get("CommonPrefixes")
            if prefix["Prefix"].split("_")[3] == path.split("_")[3]
        ]
        if len(updated_key) == 0:
            raise KeyDoesNotExist
        else:
            return updated_key[0]


def get_landsat(bucket, path, output_directory):
    client = boto3.client("s3")
    if(key_exists(client, bucket, path)):
        download_files(client, bucket, path, output_directory)
        id = Path(path).parts[-1]
        return id
    else:
        updated_path = get_updated_key(client, bucket, path)
        download_files(client, bucket, updated_path, output_directory)
        updated_id = Path(updated_path).parts[-1]
        return updated_id


@click.command()
@click.argument(
    "bucket",
    type=click.STRING
)
@click.argument(
    "path",
    type=click.STRING,
)
@click.argument(
    "output_directory",
    type=click.Path(),
)
def main(bucket, path, output_directory):
    id = get_landsat(bucket, path, output_directory)
    click.echo(id)
