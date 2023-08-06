import random
import string

import _x21


def _get_random_string(length, seed=None):
    """Returns random len(16) alphanumeric string."""
    if seed is not None:
        random.seed(seed)
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _encrypt(key_tag: str, message: str, iv: str) -> bytes:
    if key_tag == "22b":
        assert len(iv) == 16
        return _x21.encrypt_22b(message, iv)

    elif key_tag == "22a":
        raise ValueError("Need x21 < 0.3")

    else:
        raise ValueError(f"Unknown key {key_tag}")


def __dex__(glob: dict, key_tag: str, smessage: bytes) -> None:
    assert key_tag == "22a"
    raise ValueError("Need x21 < 0.3")


def __dex_22b__(glob: dict, iv: bytes, smessage: bytes) -> None:
    _x21.decrypt_and_exec_22b(smessage, iv, glob)
