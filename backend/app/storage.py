"""S3-compatible object storage helpers (PRD FR-5).

boto3 talks to Garage today and would talk to MinIO or R2 unchanged.
Garage speaks a subset of the S3 API, so the verification run (presign →
PUT → HEAD → presign GET) doubles as the compatibility test.
"""

from functools import lru_cache

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from . import config


def build_client(
    endpoint: str,
    region: str,
    access_key_id: str,
    secret_access_key: str,
):
    """Build a SigV4 path-style client.

    Path-style addressing keeps the bucket in the path, which is what
    Garage (and any non-DNS endpoint) expects; virtual-host style would
    try to resolve `<bucket>.s3.garage` and fail.
    """
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


@lru_cache(maxsize=1)
def get_client():
    """Shared client from config. Cached — building one is expensive."""
    return build_client(
        config.S3_ENDPOINT,
        config.S3_REGION,
        config.S3_ACCESS_KEY_ID,
        config.S3_SECRET_ACCESS_KEY,
    )


def ensure_bucket(client, bucket: str) -> None:
    """Create the bucket if missing.

    A 403 from `head_bucket` means the bucket exists but this key cannot
    list it, which is not an error worth failing startup over.
    """
    try:
        client.head_bucket(Bucket=bucket)
        return
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code not in ("404", "NoSuchBucket"):
            return
    # No CreateBucketConfiguration: Garage, MinIO and R2 all default to
    # the unsigned region, and adding one would only risk a mismatch.
    client.create_bucket(Bucket=bucket)


def presign_put(client, bucket: str, key: str, expires_in: int) -> str:
    """Presigned PUT URL.

    ContentType is deliberately left out of the signed params: if it were
    signed, the browser would have to echo a byte-identical header or S3
    would reject the upload with SignatureDoesNotMatch.
    """
    return client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def presign_get(client, bucket: str, key: str, expires_in: int) -> str:
    """Presigned GET URL for the gated file viewer (FR-5)."""
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def head_size(client, bucket: str, key: str) -> int | None:
    """Object size in bytes, or None when the object does not exist.

    HEAD has no response body, so botocore reports the status-derived
    string `"404"` rather than `NoSuchKey` (boto3 #2442).
    """
    try:
        return client.head_object(Bucket=bucket, Key=key)["ContentLength"]
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "")
        status_code = exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if code in ("404", "NoSuchKey") or status_code == 404:
            return None
        raise


def delete_object(client, bucket: str, key: str) -> None:
    """Best-effort delete, used to roll back an oversize upload."""
    try:
        client.delete_object(Bucket=bucket, Key=key)
    except ClientError:
        # Cleanup is advisory: an orphan is recoverable by the sweeper,
        # so a failed delete must not mask the original error.
        pass
