"""
Conversion of format placeholders between Android (Java) and iOS (Objective-C/Swift).

- Android: `%s`, `%1$s`, `%d`, `%.2f`...
- iOS: `%@`, `%1$@`, `%d`, `%ld`, `%lu`...

Both platforms share most conversions (`%d`, `%f`, `%x`...), so only the ones that
differ are changed. Values are converted when they are written to Android or iOS files,
so any other file type keeps the placeholders of the original file.
"""

import re

# `%[position$][flags][width][.precision][length]conversion`. The space flag is not
# matched so that text such as `100% sure` is not mistaken for a placeholder.
_PLACEHOLDER_PATTERN = re.compile(
    r"%(?P<position>\d+\$)?"
    r"(?P<flags>[-#+0,(]*)"
    r"(?P<width>\d+)?"
    r"(?P<precision>\.\d+)?"
    r"(?P<length>hh|h|ll|l|q|z|t|j)?"
    r"(?P<conversion>[@sSdDiuUxXoOfFeEgGcCaA%])"
)

# Conversions that Java doesn't have, mapped to their Java equivalent
_TO_ANDROID_CONVERSIONS = {"@": "s", "D": "d", "i": "d", "u": "d", "U": "d", "O": "o"}

# Conversions that iOS doesn't have, mapped to their iOS equivalent
_TO_IOS_CONVERSIONS = {"s": "@", "S": "@"}


def to_android(value: str) -> str:
    """
    Converts iOS placeholders to Android ones, e.g. `%1$@` -> `%1$s` and `%ld` -> `%d`.
    """

    def replace(match):
        if match.group("conversion") == "%":
            return match.group(0)

        conversion = match.group("conversion")
        return _build(
            match,
            # Java doesn't have length modifiers
            length="",
            conversion=_TO_ANDROID_CONVERSIONS.get(conversion, conversion),
        )

    return _PLACEHOLDER_PATTERN.sub(replace, value)


def to_ios(value: str) -> str:
    """Converts Android placeholders to iOS ones, e.g. `%1$s` -> `%1$@`."""

    def replace(match):
        conversion = match.group("conversion")
        if conversion not in _TO_IOS_CONVERSIONS:
            return match.group(0)

        return _build(match, conversion=_TO_IOS_CONVERSIONS[conversion])

    return _PLACEHOLDER_PATTERN.sub(replace, value)


def _build(match: re.Match[str], **overrides: str) -> str:
    parts = {**match.groupdict(), **overrides}
    return "%" + "".join(
        parts[group] or ""
        for group in (
            "position",
            "flags",
            "width",
            "precision",
            "length",
            "conversion",
        )
    )


def remove(value: str) -> str:
    """Returns the value without its placeholders, e.g. `%1$s has %d` -> ` has `."""

    return _PLACEHOLDER_PATTERN.sub("", value)


def signature(value: str) -> list[tuple[int, str]]:
    """
    Returns the (position, conversion) of each placeholder of the value, sorted by
    position, so that values with the same arguments have the same signature on both
    platforms, e.g. `%1$@ has %2$ld` and `%s has %d` -> `[(1, "s"), (2, "d")]`.
    Flags, width and precision are ignored.
    """

    placeholders = []
    for index, match in enumerate(
        (
            m
            for m in _PLACEHOLDER_PATTERN.finditer(value)
            if m.group("conversion") != "%"
        ),
        start=1,
    ):
        position = match.group("position")
        conversion = match.group("conversion")
        placeholders.append(
            (
                int(position[:-1]) if position else index,
                _TO_ANDROID_CONVERSIONS.get(conversion, conversion),
            )
        )

    return sorted(placeholders)
