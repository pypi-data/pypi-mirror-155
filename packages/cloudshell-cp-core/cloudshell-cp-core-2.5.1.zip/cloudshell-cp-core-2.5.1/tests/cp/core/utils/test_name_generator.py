import re

import pytest

from cloudshell.cp.core.utils.name_generator import NameGenerator


def test_name_generator():
    generate_name = NameGenerator()

    assert generate_name("test").startswith("test-")
    assert generate_name("test", "postfix") == "test-postfix"
    assert generate_name("x" * 101).startswith("x" * 91 + "-")


def test_name_generator_postfix_is_too_long():
    generate_name = NameGenerator(max_length=10)
    with pytest.raises(ValueError):
        generate_name("test", "postfix-too-long")


def test_symbols_removed():
    generate_name = NameGenerator()
    name = generate_name(r"name test-123.-|_[]\/!@#$%^&*()")
    name, postfix = name.rsplit("-", 1)
    assert name == "name test-123.-|_[]"
    assert re.search(r"[\d\w]{8}", postfix)
