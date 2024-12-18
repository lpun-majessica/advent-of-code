# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:nomarker
#     text_representation:
#       extension: .py
#       format_name: nomarker
#       format_version: '1.0'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from pathlib import Path
from typing import Union


def get_session_cookie(
        path: Union[Path, str] = Path(__file__).parent/"session_cookie.txt"
    ):
    with Path(path).open(mode="r") as file:
        return file.read()

# to-do: update session cookie
