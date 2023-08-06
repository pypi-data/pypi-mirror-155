import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode
from typing import Optional


S3_BUCKET_OBJECT_KEY_ENCODING = 'utf-8'


class KeyDecodeException(Exception):
    """
    Raised if decoding an HEAObject id or name string to an AWS S3 bucket object key failed. A possible nested
    exception may provide more details about why, but the types of nested exception raised are specific to the
    decoding algorithm implementation and are not part of HEA's public API.
    """
    pass


def encode_key(key: str) -> str:
    """
    Encodes an AWS S3 bucket object key to a string that can be inserted into URL paths. Bucket keys are /-separated
    paths, and URLs with escaped slashes are rejected or handled incorrectly by many servers and clients. This
    function encodes bucket keys to a limited character set that is URL-safe. This implementation currently uses
    URL-safe base 64 encoding, described at https://datatracker.ietf.org/doc/html/rfc4648#section-5, but the encoding
    algorithm is not part of HEA's public API and is subject to change.

    :param key: an AWS S3 bucket key.
    :return: the encoded string.
    """
    return urlsafe_b64encode(key.encode(S3_BUCKET_OBJECT_KEY_ENCODING)).decode(S3_BUCKET_OBJECT_KEY_ENCODING)


def decode_key(encoded_key: str) -> str:
    """
    Decodes the provided string to an AWS S3 object bucket key. This implementation currently uses URL-safe base 64
    decoding, described at https://datatracker.ietf.org/doc/html/rfc4648#section-5, but the encoding algorithm is not
    part of HEA's public API and is subject to change.

    :param encoded_key: the encoded key, obtained from _encode_object_key().
    :return: the actual AWS S3 bucket key.
    :raises _DecodeException: if the provided string could not be decoded.
    """
    try:
        return urlsafe_b64decode(encoded_key.encode(S3_BUCKET_OBJECT_KEY_ENCODING)).decode(S3_BUCKET_OBJECT_KEY_ENCODING)
    except (UnicodeDecodeError, binascii.Error) as e:
        raise KeyDecodeException(f'Failed to decode {encoded_key} to an AWS S3 bucket key') from e


def is_folder(key: Optional[str]) -> bool:
    """
    Returns whether the provided key represents a folder (ends with a /).

    :param key: the key.
    :return: True if the key represents a folder, False if not.
    """
    return key.endswith('/') if key is not None else False
