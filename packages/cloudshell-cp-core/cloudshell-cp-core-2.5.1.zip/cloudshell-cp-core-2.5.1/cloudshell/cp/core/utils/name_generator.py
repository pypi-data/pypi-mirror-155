from __future__ import annotations

import re
import uuid

import attr

CS_MAX_NAME_LENGTH = 100
CS_ALLOWED_SYMBOLS = re.escape(".-|_[]")
CS_PATTER_REMOVE_SYMBOLS = re.compile(rf"[^\w\d\s{CS_ALLOWED_SYMBOLS}]")


def generate_name(name: str, postfix: str | None = None, max_length: int = 24) -> str:
    """Generate name based on the given one with a maximum allowed length.

    Will replace all special characters (some Azure resources have this requirements).
    :param name: App name
    :param postfix: If postfix is empty method will generate unique 8 char long id
    :param max_length: Maximum allowed length for the generated name
    :return: (str) generated name
    """
    if postfix is None:
        postfix = generate_short_unique_string()
    if len(postfix) >= max_length:
        raise ValueError(f"Postfix '{postfix}' is bigger than name length {max_length}")

    # replace special characters. Remove dash character only if at the beginning.
    name = re.sub("[^a-zA-Z0-9-]|^-+", "", name)

    name = name[: max_length - len(postfix) - 1]
    name.rstrip("-")

    return f"{name}-{postfix}"


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NameGenerator:
    """Generate name based on the given one with a maximum allowed length.

    Will replace all special characters.
    """

    pattern_remove_symbols: re.Pattern = CS_PATTER_REMOVE_SYMBOLS
    max_length: int = CS_MAX_NAME_LENGTH
    prefix_length: int = 8

    def __call__(self, app_name: str, postfix: str | None = None) -> str:
        if postfix is None:
            postfix = self._generate_postfix()
        if len(postfix) >= self.max_length - 4:  # min 3 chars from app_name and -
            raise ValueError(
                f"Postfix '{postfix}' is too big. Max name length is {self.max_length}"
            )

        app_name = self._edit_app_name(app_name)

        max_length = min(self.max_length, CS_MAX_NAME_LENGTH)
        app_name = app_name[: max_length - len(postfix) - 1].rstrip("-")

        return f"{app_name}-{postfix}"

    def _generate_postfix(self) -> str:
        return generate_short_unique_string(self.prefix_length)

    def _edit_app_name(self, app_name: str) -> str:
        return self.pattern_remove_symbols.sub("", app_name)


def generate_short_unique_string(length: int = 8) -> str:
    """Generate a short unique string.

    Method generates an uuid and return the first 8 characters of the new uuid
    """
    unique_id = str(uuid.uuid4()).replace("-", "")[:length]
    return unique_id
