from secrets import token_urlsafe
from random import choice
from string import digits as str_digits, ascii_letters as str_ascii_letters


def _generate_rand_str(full_url: str, len_of_hash: int = 5):
    chars = str_digits + str_ascii_letters  # 62 characters [A-Z|a-z|0-9]
    print(full_url)
    res_str = "".join(choice(chars) for _ in range(len_of_hash))
    # res_str = token_urlsafe(len_of_hash)[:len_of_hash]
    return res_str
