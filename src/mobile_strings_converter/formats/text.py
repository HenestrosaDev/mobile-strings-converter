import codecs


def decode(data: bytes) -> str:
    """
    Decodes the content of a text file. UTF-16 files (e.g. `.strings` files created by
    older versions of Xcode) are detected by their byte order mark, and any other file
    is read as UTF-8.
    """

    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")
