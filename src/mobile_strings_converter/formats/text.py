def decode(data: bytes) -> str:
    """Decodes the content of a text file as UTF-8, with or without a byte order mark."""

    return data.decode("utf-8-sig")
